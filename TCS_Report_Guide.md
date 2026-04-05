# TCS Project Report & Presentation Guide
**AI-Driven E-Commerce Customer Segmentation & Recommendation Engine**

If you are presenting this to TCS or submitting a formal project report, you need to show a mix of **Code Architecture**, **AI/ML Proof**, **Web UI**, and **Power BI Integration**.

---

## 📸 1. The Power BI Proof (crucial for TCS)

TCS values Business Intelligence (BI) tools. We built an "Export Data" module specifically for this.

**What you need to do to get the Power BI screenshots:**
1. Open your Streamlit App (`http://localhost:8501`).
2. Go to the left sidebar and click **"Download Data for Power BI"**. This downloads a file called `segmented_customers_for_bi.csv`.
3. Open **Power BI Desktop** on your computer.
4. Click **Get Data -> Text/CSV**, and select that downloaded file.
5. Create a basic dashboard as outlined in your original project requirements:
   - **Bar Chart:** Drag `Cluster` to X-axis, `Monetary` to Y-axis. (Shows which cluster spends the most).
   - **Donut Chart:** Drag `Cluster` to Legend, `CustomerID` to Values. (Shows how many people are in each segment).
   - **Scatter Chart:** Drag `Frequency` to X-axis, `Monetary` to Y-axis, `Cluster` to Legend.
6. Add a Text Box title: **"Customer Segmentation Report"**. 

**Screenshot to take:** Take a full-screen screenshot of this finished Power BI dashboard.
**What to write/say:** "To ensure our AI insights integrate with enterprise workflows, I built a data pipeline that exports the exact clustered personas directly into Power BI, allowing stakeholders to generate real-time business reports."

---

## 📸 2. What Code to Include in the Report

Do not copy-paste the entire code—it's too long. Only take screenshots of the **core logic** that proves you wrote the Machine Learning pipeline.

**Screenshot 1: The Model Logic (`src/model.py`)**
- Open `src/model.py` in VS Code.
- Take a screenshot of the `build_clustering_model` function (lines 9 to 30 roughly).
- **Caption:** *Implementation of the K-Means algorithm using Scikit-Learn, including data scaling using StandardScaler.*

**Screenshot 2: The Recommendation Engine (`src/model.py`)**
- Take a screenshot of the `get_recommendations` function (lines 48 to 78 roughly).
- **Caption:** *The Hybrid Cluster-Based Collaborative Filtering logic developed to generate personalized product recommendations.*

**Screenshot 3: The Data Engineering (`src/preprocess.py`)**
- Take a screenshot of the `calculate_rfm` function.
- **Caption:** *Feature engineering pipeline transforming raw transactional logs into actionable Recency, Frequency, and Monetary (RFM) metrics.*

---

## 📸 3. The App UI Proof (Streamlit)

You need to show the finished product.

**Screenshot 1:** The **Segment Analytics** Tab (showing the PCA Scatter Plot).
**Screenshot 2:** The **Cluster Profiles** Tab (showing the Radar Chart).
**Screenshot 3:** The **AI Recommendations** Tab (showing the actual product suggestions for a user).

---

## 📝 Summary: What exactly goes into the Weekly Document vs TCS Final Report?

### For the Weekly Report (Week 1):
Focus on having built the **Pipeline and Model**. 
- Show **1 screenshot of the Python code** (the K-Means function).
- Show **1 screenshot of the Streamlit App** (the PCA Scatter Plot) to prove the model is running.

### For the Final TCS Report/Presentation:
Focus on the **End-to-End Solution**.
Your slides/document should flow exactly like this:
1. **Introduction:** The goal (Customer Segmentation).
2. **Data Pipeline:** Screenshot of RFM code.
3. **AI Model:** Screenshot of K-Means code.
4. **The Product:** 3 Screenshots of the Streamlit App (Analytics, Radar Chart, Recommendations).
5. **Enterprise Integration:** The screenshot of your **Power BI Dashboard**.
6. **Conclusion:** How this drives business value.
