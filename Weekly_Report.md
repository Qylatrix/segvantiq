# Weekly Progress Report

**Project Title:** AI-Driven E-Commerce Customer Segmentation & Recommendation Engine
**Student Name:** Pretam Saha
**Date:** March 8, 2026

## Objective for the Week
To design and implement the foundation of a machine learning-based customer analytics platform that processes raw e-commerce transaction data, segments customers using K-Means clustering, and provides personalized product recommendations through an interactive web dashboard.

## Tasks Accomplished This Week

**1. Project Setup & Data Engineering**
* Initialized the project environment and installed required data science and web development dependencies (`pandas`, `scikit-learn`, `streamlit`, `plotly`).
* Developed a Python script (`src/data_fetcher.py`) to generate a robust, synthetic e-commerce transactional dataset (100,000+ records) mirroring the structure of the UCI Online Retail dataset. This ensures the model has sufficient data volume for training.

**2. Data Preprocessing Pipeline**
* Created `src/preprocess.py` to handle data cleaning.
* Implemented logic to remove invalid transactions (e.g., canceled orders, negative quantities) and handle missing values.
* Engineered new features by writing functions to calculate **RFM metrics** (Recency, Frequency, Monetary value) and customer Tenure, transforming raw transaction logs into a customer-centric dataset suitable for machine learning.

**3. Machine Learning Model Development**
* Developed the core analytics engine in `src/model.py`.
* Successfully implemented the **K-Means Clustering algorithm** ($k=4$) using Scikit-Learn to segment customers into distinct behavioral personas (Whales, Loyalists, Occasional Buyers, and At-Risk).
* Applied **Principal Component Analysis (PCA)** to reduce the multi-dimensional RFM features into 2D space for visualization.
* Built a hybrid, cluster-based **Collaborative Filtering Recommendation Engine** to suggest top-selling products within a specific user's cluster, filtering out items they have already purchased.

**4. Interactive Dashboard Development (Streamlit)**
* Built the frontend interface (`app.py`) using Streamlit.
* Implemented a premium "Glassmorphism" UI design using custom CSS.
* Created the "Segment Analytics" tab integrating interactive Plotly charts (PCA Scatter plot, Donut charts, Bar charts) to visualize the AI clusters.
* Created the "Cluster Profiles" tab utilizing a Radar chart to display the RFM "DNA" of each customer segment.
* Integrated the Recommendation Engine into the UI, allowing stakeholders to select a specific Customer ID and view personalized AI-generated product suggestions.
* Added a functional "Export Data" module to allow seamless integration with Power BI/Tableau.

## Challenges Faced & Solutions
* **Challenge:** The original dataset was missing from the local environment.
* **Solution:** Researched the structure of standard retail datasets and engineered a custom Python script to dynamically generate programmatic synthetic data that mathematically supports distinct customer clusters, allowing development to proceed without delays.

## Plan for Next Week
* Perform end-to-end user acceptance testing (UAT) on the Streamlit dashboard.
* Fine-tune the K-Means clustering hyperparameters (e.g., testing different $k$ values using the Elbow Method) if necessary.
* Finalize project documentation and deployment preparations for hosting the web application on Streamlit Community Cloud.
* Create the Power BI visual report using the exported dataset from the application.
