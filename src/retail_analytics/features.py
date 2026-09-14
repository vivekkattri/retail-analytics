import pandas as pd

def compute_rfm(df):
    snapshot = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("Customer ID").agg({
         "InvoiceDate": lambda x: (snapshot - x.max()).days,
        "Invoice": "nunique",
        "Revenue": "sum",
    })
    rfm.columns = ["Recency", "Frequency", "Monetary"]
    return rfm

def add_scores(rfm):
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1,2,3,4,5])
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5])
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5,4,3,2,1])
    rfm["RFM"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
    return rfm

def segment(row):
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
    if r >= 4 and f >= 4:
        return "Champions"
    if r >= 3 and f >= 3:
        return "Loyal"
    if r >= 4 and f <= 2:
        return "New"
    if r <= 2 and f >= 3:
        return "At Risk"
    if r <= 2 and f <= 2:
        return "Lost"
    return "Other"

def add_segments(rfm):
    rfm["Segment"] = rfm.apply(segment, axis=1)
    return rfm

def build_rfm(df):
    rfm=compute_rfm(df)
    rfm=add_scores(rfm)
    rfm=add_segments(rfm)
    return rfm