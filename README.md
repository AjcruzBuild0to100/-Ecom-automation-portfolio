# E-commerce automation portfolio (sample projects)

All data is fake. Python 3.10+, `pip install pandas openpyxl requests beautifulsoup4`.

1. `sales_report/` - raw Shopify-style orders CSV to a formatted Excel report with charts.
   `python make_sample.py && python sales_report.py orders.csv report.xlsx`
2. `catalog_cleaner/` - messy product catalog to clean CSV plus a change log; flags rows needing review.
   `python make_sample.py && python clean_catalog.py catalog_raw.csv catalog_clean.csv changelog.csv`
3. `price_tracker/` - logs a product price on each run and reports/emails changes.
   `python price_tracker.py URL ".price-selector" --log prices.csv` (schedule daily; respect site terms).
