"""Generate a fake Shopify-style orders export (no real customer data)."""
import random, csv, datetime as dt
random.seed(7)
products = {"Ceramic Mug":14.5,"Linen Tote Bag":22,"Soy Candle":18,"Notebook A5":9.5,"Enamel Pin Set":12,"Wall Print":30}
start = dt.date(2026,1,1)
with open("orders.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["Order ID","Created at","Product","Quantity","Unit Price","Discount"])
    for i in range(1,801):
        p = random.choice(list(products))
        d = start + dt.timedelta(days=random.randint(0,270))
        w.writerow([f"#{1000+i}", d.isoformat(), p, random.randint(1,4), products[p], random.choice([0,0,0,1,2,5])])
