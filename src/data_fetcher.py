import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_records=50000, output_path='data/customer_data.csv'):
    """
    Generates a synthetic e-commerce dataset resembling the UCI Online Retail dataset
    with the exact columns needed for the RFM and K-Means clustering pipeline.
    """
    print(f"Generating {num_records} synthetic transaction records...")

    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)

    # 1. Define typical eCommerce products & prices
    products = [
        ("WHITE HANGING HEART T-LIGHT HOLDER", 2.55),
        ("WHITE METAL LANTERN", 3.39),
        ("CREAM CUPID HEARTS COAT HANGER", 2.75),
        ("KNITTED UNION FLAG HOT WATER BOTTLE", 3.39),
        ("RED WOOLLY HOTTIE WHITE HEART.", 3.39),
        ("SET 7 BABUSHKA NESTING BOXES", 7.65),
        ("GLASS STAR FROSTED T-LIGHT HOLDER", 4.25),
        ("HAND WARMER UNION JACK", 1.85),
        ("HAND WARMER RED POLKA DOT", 1.85),
        ("ASSORTED COLOUR BIRD ORNAMENT", 1.69),
        ("POPPY'S PLAYHOUSE BEDROOM", 2.10),
        ("POPPY'S PLAYHOUSE KITCHEN", 2.10),
        ("FELTCRAFT PRINCESS CHARLOTTE DOLL", 3.75),
        ("IVORY KNITTED MUG COSY", 1.65),
        ("BOX OF 6 ASSORTED COLOUR TEASPOONS", 4.25),
        ("BOX OF VINTAGE JIGSAW BLOCKS", 4.95),
        ("BOX OF VINTAGE ALPHABET BLOCKS", 9.95),
        ("HOME BUILDING BLOCK WORD", 5.95),
        ("LOVE BUILDING BLOCK WORD", 5.95),
        ("RECIPE BOX WITH METAL HEART", 7.95),
        ("DOORMAT NEW ENGLAND", 7.95)
    ]

    # Generate product codes for these products
    stock_codes = [f"{random.randint(10000, 99999)}{random.choice(['A', 'B', 'C', ''])}" for _ in range(len(products))]

    # 2. Define customer personas to ensure good clusters form naturally
    # Persona weights:
    # 0. Loyalists (30%): Moderate spend, high freq, long tenure -> Buy 3-10 items, moderate prices
    # 1. Whales (10%): High spend, high freq -> Buy 10-50 items, high prices
    # 2. Occasional (40%): Low freq, low spend -> Buy 1-5 items, low prices
    # 3. At-Risk (20%): Haven't bought recently, low spend -> Buy 1-3 items, old dates
    
    # Let's generate 4000 unique customers with predefined personas
    num_customers = 4000
    customer_ids = np.arange(12000, 12000 + num_customers)
    personas = np.random.choice(
        ['loyalist', 'whale', 'occasional', 'at_risk'],
        size=num_customers,
        p=[0.30, 0.10, 0.40, 0.20]
    )

    # Base dates
    end_date = datetime(2025, 12, 31)
    start_date = end_date - timedelta(days=365) # 1 year of data

    records = []
    invoice_counter = 500000

    for idx, cid in enumerate(customer_ids):
        persona = personas[idx]
        
        # Determine number of invoices (transactions) for this customer
        if persona == 'whale':
            num_invoices = random.randint(10, 30)
        elif persona == 'loyalist':
            num_invoices = random.randint(5, 15)
        elif persona == 'occasional':
            num_invoices = random.randint(1, 4)
        elif persona == 'at_risk':
            num_invoices = random.randint(1, 3)
            
        # Determine recency behavior
        for _ in range(num_invoices):
            if persona == 'at_risk':
                # bought a long time ago (150-365 days ago)
                inv_date = end_date - timedelta(days=random.randint(150, 365))
            elif persona == 'occasional':
                # bought sporadically (30-200 days ago)
                inv_date = end_date - timedelta(days=random.randint(30, 200))
            else:
                # loyalists and whales bought recently too (0-365 days)
                inv_date = end_date - timedelta(days=random.randint(0, 365))
            
            # Format InvoiceNo as string
            inv_no = str(invoice_counter)
            invoice_counter += 1
            
            # Formatting Date to string matching typical pandas parsing dd/mm/yyyy hh:mm
            inv_date_str = inv_date.strftime("%d/%m/%Y %H:%M")

            # Determine items in this invoice
            if persona == 'whale':
                num_items = random.randint(10, 50)
            elif persona == 'loyalist':
                num_items = random.randint(3, 15)
            else:
                num_items = random.randint(1, 5)
                
            # Randomly select items to "purchase"
            for _ in range(num_items):
                prod_idx = random.randint(0, len(products)-1)
                desc, price = products[prod_idx]
                stock_code = stock_codes[prod_idx]
                
                # Determine quantity
                if persona == 'whale':
                    qty = random.randint(5, 50)
                else:
                    qty = random.randint(1, 10)
                
                # Introduce some noise: 'C' prefixed cancelled invoices (~2% chance)
                is_cancelled = random.random() < 0.02
                final_inv = f"C{inv_no}" if is_cancelled else inv_no
                final_qty = -qty if is_cancelled else qty
                
                # Some noise: Missing descriptions (~1% chance)
                final_desc = np.nan if random.random() < 0.01 else desc
                
                # Some noise: Missing CustomerID (~2% chance)
                final_cid = np.nan if random.random() < 0.02 else float(cid)

                records.append({
                    'InvoiceNo': final_inv,
                    'StockCode': stock_code,
                    'Description': final_desc,
                    'Quantity': final_qty,
                    'InvoiceDate': inv_date_str,
                    'UnitPrice': price,
                    'CustomerID': final_cid,
                    'Country': 'United Kingdom' # Default
                })
                
                if len(records) >= num_records:
                    break
            
            if len(records) >= num_records:
                break
        if len(records) >= num_records:
            break

    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} records at {output_path}")
    print("Sample Output:")
    print(df.head())

if __name__ == "__main__":
    generate_synthetic_data(num_records=100000, output_path='data/customer_data.csv')
