"""Clean a messy product catalog and write a change log.
Usage: python clean_catalog.py catalog_raw.csv catalog_clean.csv changelog.csv
"""
import re, sys
import pandas as pd

def to_price(v):
    m = re.search(r"\d[\d.,]*", str(v))
    if not m: return None
    return round(float(m.group().replace(",", ".")), 2)

def to_grams(v):
    m = re.match(r"\s*([\d.]+)\s*(kg|g|oz)?", str(v).lower())
    if not m: return None
    n, u = float(m.group(1)), m.group(2) or "g"
    return round(n*{"kg":1000,"g":1,"oz":28.35}[u])

def main(src, out, log):
    raw = pd.read_csv(src, dtype=str).fillna("")
    changes, rows = [], []
    def note(i, field, old, new, why):
        changes.append({"row": i+2, "field": field, "old": old, "new": new, "reason": why})
    for i, r in raw.iterrows():
        sku = r["SKU"].strip().upper()
        if sku != r["SKU"]: note(i, "SKU", r["SKU"], sku, "trim/uppercase")
        title = r["Title"].strip().title()
        if title != r["Title"]: note(i, "Title", r["Title"], title, "trim/title case")
        price = to_price(r["Price"])
        if price is None: note(i, "Price", r["Price"], "", "unparseable, needs review")
        elif str(price) != r["Price"]: note(i, "Price", r["Price"], price, "normalised to number")
        grams = to_grams(r["Weight"])
        if grams is None: note(i, "Weight", r["Weight"], "", "missing")
        else: note(i, "Weight", r["Weight"], grams, "converted to grams")
        stock = r["Stock"].strip()
        if stock.isdigit(): stock = int(stock)
        else: note(i, "Stock", stock, "", "invalid stock, needs review"); stock = None
        rows.append({"SKU": sku, "Title": title, "Price": price, "Weight (g)": grams, "Stock": stock})
    df = pd.DataFrame(rows)
    before = len(df)
    df["_score"] = df.notna().sum(axis=1) + (df["Title"] != "")
    df = df.sort_values("_score", ascending=False).drop_duplicates("SKU").sort_index().drop(columns="_score")
    changes.append({"row": "", "field": "rows", "old": before, "new": len(df), "reason": f"removed {before-len(df)} duplicate SKU rows (kept most complete)"})
    df["Weight (g)"] = df["Weight (g)"].astype("Int64"); df["Stock"] = df["Stock"].astype("Int64")
    df["Needs review"] = (df["Title"] == "") | df["Price"].isna() | df["Stock"].isna()
    df.to_csv(out, index=False)
    pd.DataFrame(changes).to_csv(log, index=False)
    print(f"{before} -> {len(df)} rows, {int(df['Needs review'].sum())} flagged, {len(changes)} changes logged")

if __name__ == "__main__":
    main(*sys.argv[1:4])
