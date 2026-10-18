"""Log a product's price and report changes.
Usage: python price_tracker.py URL "CSS selector" [--log prices.csv] [--email]
Run daily via cron / Task Scheduler. Only track pages whose terms allow it.
Email (optional) uses SMTP_HOST, SMTP_USER, SMTP_PASS, MAIL_TO environment variables.
"""
import argparse, csv, datetime as dt, os, re, smtplib, sys
from email.message import EmailMessage
import requests
from bs4 import BeautifulSoup

def fetch_price(url, selector):
    r = requests.get(url, timeout=20, headers={"User-Agent": "price-tracker-demo/1.0"})
    r.raise_for_status()
    el = BeautifulSoup(r.text, "html.parser").select_one(selector)
    if not el: raise ValueError("selector not found")
    m = re.search(r"[\d.,]+", el.get_text())
    return float(m.group().replace(",", ""))

def last_price(path, url):
    if not os.path.exists(path): return None
    rows = [r for r in csv.DictReader(open(path)) if r["url"] == url]
    return float(rows[-1]["price"]) if rows else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("selector")
    ap.add_argument("--log", default="prices.csv"); ap.add_argument("--email", action="store_true")
    a = ap.parse_args()
    price = fetch_price(a.url, a.selector)
    prev = last_price(a.log, a.url)
    new = not os.path.exists(a.log)
    with open(a.log, "a", newline="") as f:
        w = csv.writer(f)
        if new: w.writerow(["timestamp", "url", "price"])
        w.writerow([dt.datetime.now().isoformat(timespec="seconds"), a.url, price])
    msg = f"{a.url}: {price}" + ("" if prev is None else f" (was {prev}, change {price-prev:+.2f})")
    print(msg)
    if a.email and prev is not None and price != prev:
        m = EmailMessage(); m["Subject"] = "Price change detected"; m["From"] = os.environ["SMTP_USER"]; m["To"] = os.environ["MAIL_TO"]
        m.set_content(msg)
        with smtplib.SMTP_SSL(os.environ["SMTP_HOST"]) as s:
            s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"]); s.send_message(m)

if __name__ == "__main__":
    main()
