#IRRBB Risk Engine – ALM Simulation Project
#Author: Selim Cebe
#Description: 
#   A high-performance simulation of Interest Rate Risk in the Banking Book (IRRBB).
#   Calculates NII and EVE sensitivity for a 1,000,000 instrument balance sheet 
#    using vectorized operations.
    
import pandas as pd
import numpy as np
import time
#Three main libraries we use. 
#Pandas for data acquiring and vectorization.
#Numpy is our "calculation" tool
#Time is our time ruler

# PARAMETERS. Core assumptions for interest rate scenario analysis
BANK_CAPITAL = 5_000_000_000  # Example Tier 1 capital
N_ROWS = 1_000_000
SHOCK_RATE = 0.02                # 200 bps parallel shock
DEPOSIT_BETA = 0.40              # Liability repricing beta
BEHAVIORAL_MATURITY_DEMAND = 36  # Non-maturity deposits (months)

# DATA GENERATION
# I created a synthetic balance sheet with diverse financial instruments
# I generated data and frame it by pandasy. df is our main executer.
# I created arrays for assets and liabilities.

def generate_balance_sheet(n=N_ROWS):

    sides = np.array(['Asset', 'Liability'])

    df = pd.DataFrame({
        "Instrument_ID": np.arange(n),
        "Side": np.random.choice(sides, n, p=[0.45, 0.55]),
        "Amount": np.random.uniform(50_000, 1_000_000, n),
        "Contractual_Maturity": np.random.choice([0,1,3,6,12,24,60], n),
        "Rate": np.random.uniform(0.15, 0.45, n)})

    asset_cats = np.array(["Commercial Loan","Consumer Loan",
        "Gov Bond","Project Finance"])

    liab_cats = np.array(["Demand Deposit","Time Deposit",
        "Interbank Loan","Eurobond Issued"])

    df["Category"] = np.where(
        df["Side"] == "Asset",
        np.random.choice(asset_cats, n),
        np.random.choice(liab_cats, n))

    #Mapping non-maturity deposits to behavioral profiles instead of contractual terms
    df["Maturity_Adj"] = np.where(
        df["Category"] == "Demand Deposit",
        BEHAVIORAL_MATURITY_DEMAND,
        df["Contractual_Maturity"])

    # Approximating price sensitivity for each instrument based on adjusted maturity
    df["Duration"] = (df["Maturity_Adj"] / 12) * 0.85

    # Effective repricing beta
    df["Effective_Beta"] = np.where(
    df["Category"] == "Demand Deposit",
    DEPOSIT_BETA,
    1.0
)


    return df



# IRRBB RISK ENGINE

def run_irrbb_engine(df, shock=SHOCK_RATE):

    # ---------- BUCKETS ----------
    bins = [-1, 1, 3, 6, 12, 120]
    labels = ["0-1M", "1-3M", "3-6M", "6-12M", "12M+"]

    df["Bucket"] = pd.cut(df["Maturity_Adj"],bins=bins,labels=labels)

    #GAP REPORT
    gap = (df.groupby(["Bucket", "Side"])["Amount"].sum().unstack().fillna(0))

    # Guarantee both columns exist
    gap = gap.reindex(columns=["Asset", "Liability"], fill_value=0)
    gap = gap.sort_index()

    gap["Gap"] = gap["Asset"] - gap["Liability"]
    gap["Cum_Gap"] = gap["Gap"].cumsum()



    #NII SENSITIVITY
    bucket_weights = {"0-1M": 0.5,"1-3M": 2,"3-6M": 4.5,"6-12M": 9,"12M+": 18}

    # Numeric-safe mapping
    weights = np.array([
        bucket_weights[str(b)]
        for b in gap.index
    ])

    gap["NII_Impact"] = (
        gap["Gap"].values * shock * (weights / 12)
    )

    total_nii = gap["NII_Impact"].sum()

    # ---------- EVE SENSITIVITY ----------
    df["Dollar_Duration"] = (
        df["Amount"]
        * df["Duration"]
        * df["Effective_Beta"]
    )

    asset_dd = df.loc[df["Side"]=="Asset", "Dollar_Duration"].sum()
    liab_dd  = df.loc[df["Side"]=="Liability", "Dollar_Duration"].sum()

    delta_eve = -(asset_dd - liab_dd) * shock
    eve_ratio = delta_eve / BANK_CAPITAL

    return gap, total_nii, delta_eve, eve_ratio


# EXECUTION

start = time.time()

df = generate_balance_sheet()
report, total_nii, delta_eve, eve_ratio = run_irrbb_engine(df)

print("\n==============================")
print("IRRBB RESULTS (200bps Shock)")
print("==============================")
print(report[["Asset","Liability","Gap","NII_Impact"]])
print(f"\nTotal NII Impact : {total_nii:,.0f}")
print(f"Delta EVE Impact : {delta_eve:,.0f}")
print(f"EVE / Capital    : {abs(eve_ratio):.2%}")
print(f"Execution Time   : {time.time()-start:.2f} seconds")
