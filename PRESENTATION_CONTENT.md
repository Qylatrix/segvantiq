# INTERNSHIP PRESENTATION CONTENT — SEGVANTIQ (by Qylatrix)
*Use this guide to fill your PPT Template for the April 6th Review.*

---

## Slide 1: Title Slide
- **Title**: SEGVANTIQ — AI-Powered Customer Intelligence SaaS Platform
- **Sub-title**: Transforming Raw Transaction Data into Strategic Business Action
- **Presented by**: Pretam Saha (Qylatrix Brand)
- **Organization**: TCS iON Data Analytics Internship
- **Key Focus**: Machine Learning, Predictive Analytics, and Multi-Tenant SaaS Architecture.

---

## Slide 2: Problem Statement
- **Context**: SMBs (Retail, Restaurants, Salons) collect data but lack the tools to analyze it.
- **The Gap**: Enterprise analytics (Salesforce/Adobe) are too expensive and complex for local store owners.
- **Problem**: 90% of small business data goes unused, leading to missed revenue and high churn.
- **Goal**: Build a self-service AI platform that turns "Raw CSVs" into "Marketing Strategies."

---

## Slide 3: The Solution — SEGVANTIQ
- **Overview**: A multi-tenant SaaS platform where business owners upload their transaction history.
- **Core Value**:
    - AI-driven customer segmentation.
    - Predictive Lifetime Value (CLV).
    - Anomaly / Fraud detection.
    - Market Basket Analysis (MBA).
    - **Qyla AI**: An embedded virtual analyst for instant business queries.

---

## Slide 4: System Architecture
- **Frontend**: Streamlit (Python) with a premium glassmorphism UI.
- **Backend**: Python (Scikit-Learn, Pandas, Numpy).
- **AI Layer**: Llama 3.1-70b via Groq API (High-speed inference).
- **Database**: Supabase (Persistent multi-tenant business accounts).
- **Security**: BCrypt hashing for password protection.
- **Deployment**: Streamlit Community Cloud (GitHub: Qylatrix/segvantiq).

---

## Slide 5: Data Pipeline & Preprocessing
- **Step 1: ETL**: Extraction from CSV (UCI Retail format).
- **Step 2: RFM Engineering**:
    - **Recency**: Days since last purchase.
    - **Frequency**: Total number of orders.
    - **Monetary**: Total lifetime spend.
- **Step 3: Scaling**: Standardizing features for ML compatibility.
- **Step 4: Demo Mode**: Built-in synthetic data generator (probabilistic archetypes).

---

## Slide 6: Machine Learning — Segmentation
- **Algorithm**: K-Means Clustering.
- **Optimization**: Elbow Method (WCSS) to find the optimal 'k'.
- **Validation**: Silhouette Score (~0.45) and Calinski-Harabasz Index.
- **Visualization**: PCA (Principal Component Analysis) to reduce 3D RFM to 2D for interactive scatter plots.
- **Output**: 4 Specific Personas (Whales, Loyalists, Occasional, At-Risk).

---

## Slide 7: Predictive Analytics — CLV & ROI
- **Customer Lifetime Value (CLV)**:
    - Formula: `Annual Revenue / Churn Rate`.
    - Purpose: Identified segments worth 5x more in marketing investment.
- **Marketing Action Plan**:
    - AI-generated email templates for each persona.
    - Automated "Win-back" strategies for At-Risk customers.
    - Upsell triggers for Loyalists.

---

## Slide 8: Advanced Modules (MBA & Anomaly)
- **Market Basket Analysis (MBA)**:
    - Algorithm: Apriori (Support, Confidence, Lift).
    - Result: Identified high-lift product pairs for smart bundling.
- **Anomaly Detection**:
    - Algorithm: Isolation Forest.
    - Result: Found the top 5% most unusual transaction profiles to prevent revenue leakage.
- **Cohort Analysis**: Monthly retention heatmaps to track business health.

---

## Slide 9: Qyla AI — The Virtual Analyst
- **Technology**: Llama 3.1-70b (Context-aware).
- **Features**:
    - Clinical, data-driven analysis of user datasets.
    - Answers specific questions: "How do I retain my top 5%?"
    - Smart Fallback: Rule-based analyst for offline/no-API scenarios.
    - Business-tailored system prompts.

---

## Slide 10: SaaS Pivot & Final Results
- **Outcome**: Successfully re-architected a demo script into a production-ready B2B platform.
- **Intership Goals Met**:
    - Mastery of Python ML libraries.
    - Deployment of a live cloud-based solution.
    - Integration of Commercial GenAI APIs.
- **Next Steps**: real-time webhook integration for POS systems & Mobile App development.

---

## Slide 11: Conclusion
- **Key Takeaway**: SEGVANTIQ democratizes data science for small businesses.
- **Impact**: +15% potential revenue growth via targeted segment marketing.
- **GitHub**: `github.com/Qylatrix/segvantiq`
- **Future**: "Turning bytes into business."
