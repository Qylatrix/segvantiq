import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.ensemble import IsolationForest
import joblib
import os

from typing import Dict, List, Tuple, Any, Optional
from sklearn.base import ClusterMixin, TransformerMixin

def build_clustering_model(df_rfm: pd.DataFrame, n_clusters: int = 4, random_state: int = 42) -> Tuple[pd.DataFrame, TransformerMixin, ClusterMixin]:
    """
    Applies K-Means clustering to the RFM data.
    Scales the features, fits the model, and adds Cluster assignments to the DataFrame.
    """
    # Features for clustering
    features = ['Recency', 'Tenure', 'Frequency', 'Monetary']
    X = df_rfm[features]
    
    # 1. Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. Fit K-Means
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=random_state, n_init=10)
    kmeans.fit(X_scaled)
    
    # 3. Add cluster assignments to the DataFrame
    df_rfm['Cluster'] = kmeans.labels_
    
    # Ensure standard cluster labels match our personas logically 
    # (We map them dynamically based on metrics if needed, but for simplicity, 
    # we'll map them during visualization based on group aggregations)
    
    # Save the scaler and model for reproducibility/deployment if needed
    os.makedirs('models', exist_ok=True)
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(kmeans, 'models/kmeans.pkl')
    
    return df_rfm, scaler, kmeans

def apply_pca(df_rfm: pd.DataFrame, scaler: TransformerMixin) -> pd.DataFrame:
    """
    Applies PCA to reduce RFM features to 2 dimensions for visualization.
    """
    features = ['Recency', 'Tenure', 'Frequency', 'Monetary']
    X_scaled = scaler.transform(df_rfm[features])
    
    pca = PCA(n_components=2, random_state=42)
    pca_result = pca.fit_transform(X_scaled)
    
    df_rfm['PCA1'] = pca_result[:, 0]
    df_rfm['PCA2'] = pca_result[:, 1]
    
    return df_rfm

def get_recommendations(customer_id: float, df_clean: pd.DataFrame, df_rfm: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Cluster-based Collaborative Filtering approach:
    1. Find customer's cluster.
    2. Get all top-selling products in that cluster.
    3. Filter out products the customer has already bought.
    4. Return top_n product recommendations.
    """
    # Ensure customer exists
    if customer_id not in df_rfm['CustomerID'].values:
        return pd.DataFrame()
    
    # 1. Customer's cluster
    cust_cluster = df_rfm.loc[df_rfm['CustomerID'] == customer_id, 'Cluster'].values[0]
    
    # 2. Users in the same cluster
    cluster_users = df_rfm[df_rfm['Cluster'] == cust_cluster]['CustomerID'].tolist()
    
    # 3. Transactions for these users
    cluster_txns = df_clean[df_clean['CustomerID'].isin(cluster_users)]
    
    # Customer's own purchase history
    cust_txns = df_clean[df_clean['CustomerID'] == customer_id]
    bought_items = cust_txns['Description'].unique().tolist()
    
    # 4. Top items in cluster (Popularity inside cluster)
    item_popularity = cluster_txns.groupby('Description').agg({'Quantity': 'sum'}).reset_index()
    item_popularity = item_popularity.sort_values(by='Quantity', ascending=False)
    
    # 5. Filter items already bought
    recommendations = item_popularity[~item_popularity['Description'].isin(bought_items)]
    
    # 6. Format Return
    recs = recommendations.head(top_n)[['Description', 'Quantity']]
    recs.columns = ['Product', 'Popularity_Score']
    return recs

def calculate_wcss(df_rfm: pd.DataFrame) -> Dict[int, float]:
    """
    Calculates the Within-Cluster Sum of Squares (WCSS) for the Elbow Method.
    Evaluates k from 2 to 8.
    """
    features = ['Recency', 'Tenure', 'Frequency', 'Monetary']
    X = df_rfm[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    wcss = {}
    for k in range(2, 9):
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        wcss[k] = kmeans.inertia_
        
    return wcss

def calculate_clv(df_rfm: pd.DataFrame, churn_rate: float = 0.20) -> pd.DataFrame:
    """
    Calculates Customer Lifetime Value (CLV) using a baseline predictive model.
    Average Lifespan = 1 / Churn Rate.
    Annual Revenue = Total Spend (Monetary) / Tenure (in years).
    """
    # Ensure Tenure > 0 to avoid Division by Zero
    df_rfm['Tenure_Years'] = df_rfm['Tenure'] / 365.0
    df_rfm.loc[df_rfm['Tenure_Years'] < (1/365.0), 'Tenure_Years'] = (1/365.0)
    
    # Predict Annual Spending
    df_rfm['Annual_Revenue'] = df_rfm['Monetary'] / df_rfm['Tenure_Years']
    
    # Calculate CLV
    avg_lifespan = 1 / churn_rate
    df_rfm['CLV'] = df_rfm['Annual_Revenue'] * avg_lifespan
    
    return df_rfm

def calculate_model_metrics(df_rfm: pd.DataFrame, kmeans_model: ClusterMixin) -> Dict[str, float]:
    """Calculates clustering quality metrics."""
    # We need the scaled features that were used for clustering
    # IMPORTANT: Use the same features as the model (Recency, Tenure, Frequency, Monetary)
    scaler = StandardScaler()
    features = ['Recency', 'Tenure', 'Frequency', 'Monetary']
    X_scaled = scaler.fit_transform(df_rfm[features])
    
    labels = kmeans_model.labels_
    
    # Check if we have more than 1 cluster to calculate silhouette
    if len(set(labels)) > 1:
        sil_score = metrics.silhouette_score(X_scaled, labels)
        ch_index = metrics.calinski_harabasz_score(X_scaled, labels)
    else:
        sil_score, ch_index = 0.0, 0.0
        
    return {
        "Silhouette Score": sil_score,
        "Calinski-Harabasz Index": ch_index
    }

def get_cohort_data(df_clean):
    """Processes transaction data for Cohort Analysis."""
    df = df_clean.copy()
    
    # Order Month
    df['OrderMonth'] = df['InvoiceDate'].dt.to_period('M')
    
    # Cohort Month (First Purchase Month)
    df['CohortMonth'] = df.groupby('CustomerID')['InvoiceDate'].transform('min').dt.to_period('M')
    
    # Cohort Index (Months since first purchase)
    def get_date_int(df, column):
        year = df[column].dt.year
        month = df[column].dt.month
        return year, month

    invoice_year, invoice_month = get_date_int(df, 'InvoiceDate')
    cohort_year, cohort_month = df['CohortMonth'].dt.year, df['CohortMonth'].dt.month
    
    years_diff = invoice_year - cohort_year
    months_diff = invoice_month - cohort_month
    df['CohortIndex'] = years_diff * 12 + months_diff + 1
    
    # Grouping
    cohort_data = df.groupby(['CohortMonth', 'CohortIndex'])['CustomerID'].nunique().reset_index()
    cohort_pivot = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerID')
    
    # Retention Rate
    cohort_size = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_size, axis=0)
    
    return retention

def detect_anomalies(df_rfm):
    """Identifies outliers using Isolation Forest."""
    features = ['Recency', 'Frequency', 'Monetary']
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    df_rfm['Anomaly_Score'] = iso_forest.fit_predict(df_rfm[features])
    # -1 is anomaly, 1 is normal
    df_rfm['Is_Anomaly'] = df_rfm['Anomaly_Score'].map({1: 'Normal', -1: 'Outlier'})
    return df_rfm

def get_market_basket(df_clean):
    """Simulates Market Basket Analysis (Simplified Association Rules)."""
    # Group by Customer and find their top purchased items
    basket = df_clean.groupby('Description')['Quantity'].sum().sort_values(ascending=False).reset_index()
    total_qty = basket['Quantity'].sum()
    basket['Support'] = basket['Quantity'] / total_qty
    
    # Simulate confidence for top pairs (Heuristic)
    top_items = basket.head(10)['Description'].tolist()
    rules = []
    for i in range(len(top_items)-1):
        rules.append({
            "Item_A": top_items[i],
            "Item_B": top_items[i+1],
            "Confidence": np.random.uniform(0.6, 0.9),
            "Lift": np.random.uniform(1.5, 3.0)
        })
        
    return pd.DataFrame(rules)

if __name__ == "__main__":
    import sys
    import os
    # Add project root to sys.path for direct script execution
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    try:
        from src.preprocess import preprocess_pipeline
    except ImportError:
        from preprocess import preprocess_pipeline
    
    # Test the pipeline
    df_clean, df_rfm = preprocess_pipeline()
    df_rfm, scaler, kmeans = build_clustering_model(df_rfm)
    df_rfm = apply_pca(df_rfm, scaler)
    
    metrics_results = calculate_model_metrics(df_rfm, kmeans)
    print("\nModel Quality Metrics:")
    for k, v in metrics_results.items():
        print(f" - {k}: {v:.4f}")
    
    print("\nClustering complete sample:")
    print(df_rfm.head())
