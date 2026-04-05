"""
Synthetic Demo Data Generator for Qylatrix CustomerIQ
Generates a realistic e-commerce transaction dataset mirroring the
UCI Online Retail format. Called automatically when data/customer_data.csv
is missing, ensuring the app works on Streamlit Cloud out-of-the-box.
"""
import pandas as pd
import numpy as np
import os
import datetime

# ── Reproducibility ─────────────────────────────────────────────────────────
SEED = 42
np.random.seed(SEED)

# ── Catalogue of realistic products ─────────────────────────────────────────
PRODUCTS = [
    ("CREAM HANGING HEART T-LIGHT HOLDER",   1.25),
    ("WHITE HANGING HEART T-LIGHT HOLDER",   2.10),
    ("KNITTED UNION FLAG HOT WATER BOTTLE",  3.39),
    ("RED WOOLLY HOTTIE WHITE HEART",        3.39),
    ("SET 7 BABUSHKA NESTING BOXES",         7.65),
    ("GLASS STAR FROSTED T-LIGHT HOLDER",    4.25),
    ("HAND WARMER UNION JACK",               1.85),
    ("JUMBO BAG RED RETROSPOT",              1.95),
    ("ASSORTED COLOUR BIRD ORNAMENT",        1.69),
    ("POPPY'S PLAYHOUSE BEDROOM",           3.75),
    ("FELTCRAFT PRINCESS CHARLOTTE DOLL",   5.35),
    ("IVORY KNITTED MUG COSY",              1.65),
    ("BOX OF 6 ASSORTED COLOUR TEASPOONS",  2.10),
    ("BOX OF VINTAGE JIGSAW BLOCKS",        4.50),
    ("HOME SWEET HOME METAL SIGN",          2.95),
    ("PACK 3 BOXES CHRISTMAS PANNETONE",    5.99),
    ("CHRISTMAS GINGERBREAD MAN",           0.85),
    ("WOODEN STAR CHRISTMAS SCANDINAVIAN",  1.95),
    ("WORLD WAR 2 GLIDERS ASSTD DESIGNS",   0.85),
    ("WOODLAND CHARLOTTE BAG",              6.75),
    ("VINTAGE BILLBOARD DRINK ME MUG",      3.25),
    ("DECORATION HANGING BUNNIES",          2.55),
    ("FELTCRAFT CUSHION OWL",               5.95),
    ("NIGHT LIGHT STAR IN YOUR POCKET",     1.65),
    ("SAVE THE PLANET MUG",                 1.85),
]

# ── Country distribution ─────────────────────────────────────────────────────
COUNTRIES = [
    "United Kingdom", "Germany", "France", "Spain", "Netherlands",
    "Australia", "United States", "Belgium", "Switzerland", "Norway",
]
COUNTRY_WEIGHTS = [0.85, 0.04, 0.04, 0.02, 0.01, 0.01, 0.01, 0.01, 0.005, 0.005]


def _make_customer_profile(customer_id: int, start_date: datetime.datetime,
                            end_date: datetime.datetime) -> list[dict]:
    """
    Returns a list of transaction rows for one customer.
    Customers are sampled from log-normal frequency/spend distributions
    so we naturally get Whale / Loyalist / Occasional / At-Risk clusters.
    """
    row_type = np.random.choice(
        ["whale", "loyalist", "occasional", "at_risk"],
        p=[0.05, 0.25, 0.45, 0.25],
    )

    total_days = (end_date - start_date).days

    if row_type == "whale":
        n_orders = np.random.randint(40, 90)
        qty_mult = np.random.uniform(3, 8)
        recency_days = np.random.randint(1, 30)         # bought recently
    elif row_type == "loyalist":
        n_orders = np.random.randint(12, 40)
        qty_mult = np.random.uniform(1.5, 3)
        recency_days = np.random.randint(15, 90)
    elif row_type == "occasional":
        n_orders = np.random.randint(3, 12)
        qty_mult = np.random.uniform(1, 2)
        recency_days = np.random.randint(60, 200)
    else:  # at_risk
        n_orders = np.random.randint(1, 5)
        qty_mult = np.random.uniform(1, 1.5)
        recency_days = np.random.randint(180, 360)     # hasn't bought in ages

    rows = []
    country = np.random.choice(COUNTRIES, p=COUNTRY_WEIGHTS)

    for order_idx in range(n_orders):
        # Spread invoices across the date range, biased by recency_days
        days_ago = np.random.randint(recency_days, min(total_days, recency_days + 300))
        invoice_date = end_date - datetime.timedelta(days=int(days_ago))

        invoice_no = f"INV{np.random.randint(500000, 600000)}"
        n_items = np.random.randint(1, 6)
        chosen = np.random.choice(len(PRODUCTS), size=n_items, replace=False)

        for stock_idx in chosen:
            desc, base_price = PRODUCTS[stock_idx]
            stock_code = f"SC{stock_idx:04d}"
            qty = max(1, int(np.random.poisson(3) * qty_mult))
            price = round(base_price * np.random.uniform(0.9, 1.1), 2)
            rows.append({
                "InvoiceNo": invoice_no,
                "StockCode": stock_code,
                "Description": desc,
                "Quantity": qty,
                "InvoiceDate": invoice_date.strftime("%Y-%m-%d %H:%M:%S"),
                "UnitPrice": price,
                "CustomerID": float(customer_id),
                "Country": country,
            })

    return rows


def generate_demo_dataset(n_customers: int = 800,
                           output_path: str = "data/customer_data.csv") -> str:
    """
    Generates a synthetic retail dataset and writes it to output_path.
    Returns the path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    end_date   = datetime.datetime(2011, 12, 9)
    start_date = datetime.datetime(2010, 12, 1)

    all_rows: list[dict] = []
    customer_start_id = 12000

    for i in range(n_customers):
        cid = customer_start_id + i
        rows = _make_customer_profile(cid, start_date, end_date)
        all_rows.extend(rows)

    df = pd.DataFrame(all_rows)
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)   # shuffle
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"[data_generator] Demo dataset with {len(df):,} rows written to '{output_path}'")
    return output_path


if __name__ == "__main__":
    generate_demo_dataset()
