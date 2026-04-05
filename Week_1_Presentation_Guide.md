# Week 1 College Presentation Guide & Script

This guide provides exactly what you need to **say** and what **screenshots (proof)** you should show during your college presentation for Week 1.

## Slide 1: Title & Objective
**What to show (Screenshot):** 
Take a screenshot of the top section of your Streamlit Dashboard showing the title "Customer Segmentation & Recommendation Engine" and the 4 top metrics (Total Active Customers, Total Revenue, etc.).

**What to say:**
> "Good morning/afternoon everyone. My project is the 'AI-Driven E-Commerce Customer Segmentation & Recommendation Engine'. For the first week, my primary objective was to build the foundation of this system: establishing the data pipeline, calculating customer value metrics, and developing the core Machine Learning clustering model to understand our customer base."

---

## Slide 2: Data Engineering & Preprocessing
**What to show (Screenshot):** 
Take a screenshot of the `customer_data.csv` file opened in Excel, or a screenshot of your VS Code showing the `preprocess.py` code.

**What to say:**
> "The first major step was data engineering. I created a robust script to generate over 100,000 realistic e-commerce transaction records. Once I had the data, I built a preprocessing pipeline in Python using Pandas. This pipeline cleans the data by removing canceled orders and null values. Most importantly, it calculates the **RFM metrics**—Recency, Frequency, and Monetary value—which mathematically represent a customer's buying behavior."

---

## Slide 3: The Machine Learning Model (K-Means)
**What to show (Screenshot):** 
Take a screenshot of the **"Segment Analytics"** tab in your dashboard, specifically showing the **2D PCA Scatter Plot** with the different colored clusters.

**What to say:**
> "For the core intelligence of the system, I implemented a **K-Means Clustering** machine learning algorithm using Scikit-Learn. I set the model to identify 4 distinct personas based on the RFM data. To make this high-dimensional data visible to humans, I used PCA (Principal Component Analysis) to reduce it to 2 dimensions. As you can see in the scatter plot, the AI successfully separated our customers into clear groups: Whales, Loyalists, Occasional Buyers, and At-Risk customers."

---

## Slide 4: Web Dashboard Integration (Proof of Concept)
**What to show (Screenshot):** 
Take a full-screen screenshot of the **"Cluster Profiles"** tab showing the Radar chart, demonstrating that your backend ML model is actually connected to a working UI.

**What to say:**
> "To prove that the backend machine learning model works and can deliver business value, I integrated it into an interactive web dashboard using Streamlit. I implemented a custom 'Glassmorphism' CSS design to give it a premium feel. This Radar chart dynamically visualizes the DNA of each AI-generated segment, proving that the model successfully differentiates between high-value VIPs and churning customers."

---

## Slide 5: Next Steps (Week 2)
**What to show (No specific screenshot needed, just text):**
Bullet points:
- Refine Recommendation Engine
- User Acceptance Testing (UAT)
- Power BI Integration

**What to say:**
> "For our next week, the focus will be entirely on refining the AI Recommendation Engine, which uses Collaborative Filtering to suggest products based on a user's cluster. I will also be exporting this segmented data into Power BI to create enterprise-ready visual reports. Thank you."

---

### 💡 How to get these screenshots right now:
1. Open your terminal in VS Code.
2. Ensure you are in the folder: `C:\Users\preta\.gemini\antigravity\scratch\customer_segmentation`
3. If the app isn't already running, type: `streamlit run app.py`
4. It will open in your internet browser at `http://localhost:8501`.
5. Use the **Snipping Tool** (Win + Shift + S) on your Windows laptop to capture the sections mentioned above and paste them directly into your PowerPoint slides!
