# Big Tech Financial KPI Comparison
### SEC EDGAR · FY 2023 · 10-K Annual Filings

A clean, self-contained financial dashboard comparing **Apple, Microsoft, Alphabet, Meta, and Amazon** across 5 key performance indicators derived from U.S. SEC 10-K filings.

---

## Files

| File | Purpose |
|---|---|
| `analysis.py` | Computes KPIs from SEC 10-K data → writes `data.json` |
| `build_html.py` | Embeds `data.json` into `index.html` (standalone, no server needed) |
| `data.json` | Generated KPI data |
| `index.html` | Dashboard frontend (open directly in browser) |

---

## KPIs Evaluated

| KPI | What It Measures |
|---|---|
| Net Profit Margin | How much profit per dollar of revenue |
| Return on Equity (ROE) | Profitability relative to shareholder investment |
| Debt-to-Equity Ratio | Balance sheet leverage (lower = safer) |
| Earnings Per Share (EPS) | Per-share profitability |
| Revenue Growth YoY | Year-over-year top-line momentum |

---

## How to Run (any PC)

**Requirements:** Python 3 only — no pip installs needed.

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/sec-financial-comparison.git
cd sec-financial-comparison

# 2. Generate the data
python analysis.py

# 3. Embed data into the HTML (makes it standalone)
python build_html.py

# 4. Open in browser — just double-click index.html
#    OR serve it:
python -m http.server 8765
# then open http://localhost:8765
```

---

## Data Source

All financial figures are sourced from official **U.S. SEC EDGAR 10-K Annual Filings** for Fiscal Year 2023:

- Apple — [CIK 0000320193](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=10-K)
- Microsoft — [CIK 0000789019](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K)
- Alphabet — [CIK 0001652044](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001652044&type=10-K)
- Meta — [CIK 0001326801](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001326801&type=10-K)
- Amazon — [CIK 0001018724](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001018724&type=10-K)

> For educational and analytical purposes only. Not investment advice.
