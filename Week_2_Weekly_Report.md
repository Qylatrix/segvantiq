# Weekly Progress Report (Week 2)

**Project Title:** AI-Driven E-Commerce Customer Segmentation & Recommendation Engine
**Student Name:** Pretam Saha
**Date:** March 14, 2026

## Objective for the Week
To significantly upgrade the analytical capabilities of the Week 1 prototype by integrating advanced predictive metrics (Customer Lifetime Value), model-tuning visualizations (Elbow Method), and an actionable AI-generated marketing strategy engine. The interface was also refactored into a clean, highly professional Glassmorphism enterprise dashboard.

## Tasks Accomplished This Week

**1. Data Engineering Enhancements**
* Upgraded the feature engineering pipeline (`src/preprocess.py`) to systematically calculate **Customer Tenure** (time since first purchase). This allowed for more complex predictive analytics algorithms.
* Resolved robust data pipelining issues to ensure `preprocess_pipeline()` serves the frontend without manual intervention.

**2. Advanced Machine Learning Integration**
* Implemented the **Elbow Method calculation algorithm** (Within-Cluster Sum of Squares) directly into the backend `src/model.py`. This mathematically justifies the selection of $k=4$ for the K-Means algorithm.
* Developed a predictive **Customer Lifetime Value (CLV)** algorithm leveraging Average Order Value, Purchase Frequency, and Average Lifespan to project the future financial value of customer clusters.

**3. Enterprise Dashboard & Analytics Expansion (Streamlit)**
* Engineered a highly professional, pristine **Glassmorphism Theme** using a distraction-free dark gradient, prioritizing data visibility and corporate presentation standards.
* Designed and published Three Brand New Analytical Modules (Tabs):
  * **Tab 4 (Model Tuning):** Visualizes the K-Means WCSS Elbow Curve perfectly plotted with Plotly.
  * **Tab 5 (CLV Prediction):** Renders bar charts comparing Average expected revenue by Persona, identifying crucial High-Value Customers.
  * **Tab 6 (Actionable Marketing Plan):** A smart, rule-based system that outputs specific, business-oriented email templates, marketing goals, and retention strategies based on the selected clustering Persona.

## Challenges Faced & Solutions
* **Challenge:** Ensuring Streamlit's base light/dark theme didn't clash with our custom Glassmorphism components and render text invisible.
* **Solution:** Overrode internal CSS attributes to force strict, high-contrast white text parsing across all Plotly data visualizations (Elbow, Radar, and CLV charts).
* **Challenge:** The initial frontend code was missing its bridging `preprocess_pipeline` function.
* **Solution:** Rebuilt the data execution pipeline dynamically to guarantee continuous preprocessing of raw data for the new analytical models.

## Plan for Next Week
* Perform final polishing and deploy the web application to a live server layout (e.g., Streamlit Community Cloud or Heroku).
* Prepare the final project report for TCS evaluators.
* Create the complementary Power BI dashboard utilizing the "Export to Power BI" module developed in Week 1.
