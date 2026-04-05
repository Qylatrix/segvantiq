# SEGVANTIQ (by Qylatrix) — AI Customer Intelligence Platform 🚀

**SEGVANTIQ** is a professional, multi-tenant SaaS platform designed for business owners to transform raw customer transaction data into actionable strategy. Built for the **TCS iON Data Analytics Internship**, it delivers board-level insights through 12 advanced analytical modules.

![SEGVANTIQ Banner](https://img.shields.io/badge/Status-Live_v1.0-blue?style=for-the-badge&logo=appveyor)
![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red?style=for-the-badge&logo=streamlit)

---

## 🌟 Key Features

- **Multi-Tenant SaaS Architecture**: Each business gets its own secure workspace and isolated data cache.
- **Qyla AI Chat Assistant**: An embedded AI analyst (Llama 3.1) to answer questions about your customer data in plain language.
- **Enterprise Analytics Suite (12 Modules)**:
    - **RFM Segmentation**: K-Means clustering with automated persona labeling.
    - **Predictive CLV**: Forecasting Customer Lifetime Value.
    - **Cohort Analysis**: Visualizing customer retention trends over time.
    - **Market Basket Analysis**: Uncovering product cross-sell opportunities.
    - **Anomaly Detection**: Flagging unusual / fraudulent behavior using Isolation Forest.
    - **Executive BI Report**: A Power BI-style unified visual dashboard.
- **Power BI Ready**: One-click rich CSV export optimized for Power BI Desktop.
- **Demo Mode**: Includes a self-generating synthetic dataset for immediate evaluation.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python-based)
- **ML Engine**: Scikit-Learn, Pandas, Numpy
- **Visuals**: Plotly, Seaborn, Matplotlib
- **AI Backend**: Groq API (Llama 3.1-70b)
- **Database**: Supabase (Persistent OAuth & Business Profiles)
- **Security**: Bcrypt password hashing

---

## 🚀 Quick Start (Local Setup)

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/Qylatrix/segvantiq.git
   cd segvantiq
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Secrets**:
   Create a `.streamlit/secrets.toml` file with:
   ```toml
   GROQ_API_KEY = "your_groq_key"
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_key"
   ```

4. **Run the App**:
   ```bash
   streamlit run app.py
   ```
   *Login with `demo / demo` for the interactive experience.*

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

**Developed & Maintained by [Pretam Saha](https://github.com/Qylatrix)**  
*Building the future of Customer Intelligence.*
