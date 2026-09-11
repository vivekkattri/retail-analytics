import pandas as pd

def fix_types(df):
    df = df.copy()
    df["Description"] = df["Description"].str.strip().str.upper()
    df["Customer ID"] = df["Customer ID"].astype("Int64")
    df["StockCode"] = df["StockCode"].astype(str)
    df["Invoice"]= df["Invoice"].astype(str)
    df["Country"]=df["Country"].replace("EIRE","Ireland")
    not_countries=["Unspecified","European Community"]
    df["Country"]=df["Country"].replace(not_countries,"Other")
    return df

def split_Quantity(df):
    sales=df[df["Quantity"]>0].copy()
    returns=df[df["Quantity"]<0].copy()
    return sales,returns

def remove_bad_rows(df):
     df = df.copy()
     df = df[df["Description"].notna()]
     non_products = ["POST", "D", "M", "C2", "DOT", "BANK CHARGES", "PADS", "CRUK"]
     df = df[~df["StockCode"].isin(non_products)]
     # ~ sign here means not true which means it will remove the rows which have entries of 
     # items in non_products list from df dataframe.
     df=df[df["Price"]>=0]
     return df

def add_revenue(df):
    #adding revenue column to track revenue 
    df = df.copy()
    df["Revenue"] = df["Quantity"] * df["Price"]
    return df

def make_customer_table(df):
    """I cant just drop all the customers will null id bacause that will disturb my revenue
    calculation but i need customer id for certain questions on cohort retention,so i make a new table by dropping
    null or emplty customer id rows"""
    return df[df["Customer ID"].notna()].copy()

def clean(df):
    """The problem it solves is now every table is structured here only and i dont need to import every func
    and assign new dataframes.
    """
    df = fix_types(df)
    sales, returns = split_Quantity(df)
    sales = remove_bad_rows(sales)
    sales = add_revenue(sales)
    customers = make_customer_table(sales)
    return sales, returns, customers