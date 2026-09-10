# Retail Sales & Customer Analytics

Analysis of ~1.07M transactions from a UK-based online gift retailer
(Dec 2009 – Dec 2011). Covers data cleaning, exploratory analysis,
RFM customer segmentation, and cohort retention analysis.

## Data

Online Retail II, UCI Machine Learning Repository (CC BY 4.0).
Not included in this repository. Download `online_retail_II.xlsx`
from the UCI dataset page and place it in `data/raw/`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```

## Cleaning decisions

Raw data: 1,067,371 rows across two sheets (Dec 2009 – Dec 2011).

**Returns split out.** 22,950 rows have negative quantities — these are
cancellations, marked by an invoice number starting with C. Kept as a
separate table so return rates can be measured without distorting
sales figures.

**Non-product rows removed.** X rows had stock codes for postage,
manual adjustments, and bank charges rather than products. Removed
so they don't appear in product rankings.

**Zero-price rows removed.** X rows had a price of 0 or less.

**Missing descriptions removed.** 4,382 rows.

**Two output tables.** 243,007 rows (23%) have no Customer ID but are
real sales. These are kept for revenue analysis and excluded only from
the customer table used for RFM and cohort analysis.

Final: 1038186 sales rows ,22950 return rows