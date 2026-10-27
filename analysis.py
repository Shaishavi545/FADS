"""
SEC Financial Statement Analysis — Big Tech Sector Comparison
--------------------------------------------------------------
Data Source: U.S. SEC EDGAR 10-K Annual Filings (Fiscal Year 2023)
Companies  : Apple (AAPL), Microsoft (MSFT), Alphabet (GOOGL),
             Meta Platforms (META), Amazon (AMZN)
KPIs       : Revenue, Net Profit Margin, Return on Equity (ROE),
             Debt-to-Equity Ratio, Earnings Per Share (EPS)

Run this script first to generate 'data.json', then open index.html.
Requires: Python 3 standard library only (no pip installs needed)
"""

import json

# ---------------------------------------------------------------------------
# RAW FINANCIAL DATA  (USD Millions, FY 2023 — sourced from SEC 10-K filings)
# ---------------------------------------------------------------------------
# All figures from SEC EDGAR CIK filings:
#   Apple     CIK 0000320193  | 10-K filed 2023-11-02
#   Microsoft CIK 0000789019  | 10-K filed 2023-07-27
#   Alphabet  CIK 0001652044  | 10-K filed 2024-01-30
#   Meta      CIK 0001326801  | 10-K filed 2024-02-01
#   Amazon    CIK 0001018724  | 10-K filed 2024-02-01
# ---------------------------------------------------------------------------

companies_raw = {
    "Apple": {
        "ticker":  "AAPL",
        "color":   "#60a5fa",
        "revenue_fy23":      383_285,
        "revenue_fy22":      394_328,
        "net_income_fy23":    96_995,
        "total_equity_fy23":  62_146,
        "total_debt_fy23":   111_088,
        "shares_outstanding": 15_634,
        "sector": "Technology",
        "hq":     "Cupertino, CA",
        "founded": 1976,
    },
    "Microsoft": {
        "ticker":  "MSFT",
        "color":   "#34d399",
        "revenue_fy23":      211_915,
        "revenue_fy22":      198_270,
        "net_income_fy23":    72_361,
        "total_equity_fy23": 206_223,
        "total_debt_fy23":    59_965,
        "shares_outstanding":  7_432,
        "sector": "Technology",
        "hq":     "Redmond, WA",
        "founded": 1975,
    },
    "Alphabet": {
        "ticker":  "GOOGL",
        "color":   "#fbbf24",
        "revenue_fy23":      307_394,
        "revenue_fy22":      282_836,
        "net_income_fy23":    73_795,
        "total_equity_fy23": 283_379,
        "total_debt_fy23":    13_253,
        "shares_outstanding": 12_823,
        "sector": "Technology",
        "hq":     "Mountain View, CA",
        "founded": 1998,
    },
    "Meta": {
        "ticker":  "META",
        "color":   "#a78bfa",
        "revenue_fy23":      134_902,
        "revenue_fy22":      116_609,
        "net_income_fy23":    39_098,
        "total_equity_fy23": 153_168,
        "total_debt_fy23":    37_228,
        "shares_outstanding":  2_547,
        "sector": "Technology",
        "hq":     "Menlo Park, CA",
        "founded": 2004,
    },
    "Amazon": {
        "ticker":  "AMZN",
        "color":   "#f87171",
        "revenue_fy23":      574_785,
        "revenue_fy22":      513_983,
        "net_income_fy23":    30_425,
        "total_equity_fy23": 201_875,
        "total_debt_fy23":   145_200,
        "shares_outstanding": 10_333,
        "sector": "Technology",
        "hq":     "Seattle, WA",
        "founded": 1994,
    },
}

# ---------------------------------------------------------------------------
# KPI COMPUTATION
# ---------------------------------------------------------------------------

def compute_kpis(data):
    rev       = data["revenue_fy23"]
    rev_prev  = data["revenue_fy22"]
    ni        = data["net_income_fy23"]
    eq        = data["total_equity_fy23"]
    debt      = data["total_debt_fy23"]
    shares    = data["shares_outstanding"]

    revenue_bn  = round(rev / 1_000, 1)                           # USD Billions
    net_margin  = round((ni / rev) * 100, 2)                      # %
    roe         = round((ni / eq) * 100, 2)                       # %
    de_ratio    = round(debt / eq, 2)                             # ratio
    eps         = round(ni / shares, 2)                           # USD
    rev_growth  = round(((rev - rev_prev) / rev_prev) * 100, 2)  # %

    return {
        "revenue_bn":  revenue_bn,
        "net_margin":  net_margin,
        "roe":         roe,
        "de_ratio":    de_ratio,
        "eps":         eps,
        "rev_growth":  rev_growth,
    }


# ---------------------------------------------------------------------------
# SCORING  (normalise each KPI to 0-100 across companies)
# ---------------------------------------------------------------------------

def score_companies(results):
    kpi_keys        = ["net_margin", "roe", "de_ratio", "eps", "rev_growth"]
    lower_is_better = {"de_ratio"}
    scores          = {name: {} for name in results}

    for kpi in kpi_keys:
        values = {name: results[name]["kpis"][kpi] for name in results}
        mn, mx = min(values.values()), max(values.values())
        span   = mx - mn if mx != mn else 1

        for name, val in values.items():
            if kpi in lower_is_better:
                norm = (mx - val) / span
            else:
                norm = (val - mn) / span
            scores[name][kpi] = round(norm * 100, 1)

    return scores


# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------

def verdict(results, scores):
    kpi_keys   = ["net_margin", "roe", "de_ratio", "eps", "rev_growth"]
    best_kpi   = {}
    cumulative = {name: 0.0 for name in scores}

    for kpi in kpi_keys:
        best = max(scores, key=lambda n: scores[n][kpi])
        best_kpi[kpi] = best
        for name in scores:
            cumulative[name] += scores[name][kpi]

    ranking = sorted(cumulative, key=lambda n: cumulative[n], reverse=True)
    return {
        "best_per_kpi": best_kpi,
        "cumulative":   {n: round(cumulative[n], 1) for n in cumulative},
        "overall_best": ranking[0],
        "ranking":      ranking,
    }


# ---------------------------------------------------------------------------
# ASSEMBLE
# ---------------------------------------------------------------------------

results = {}
for name, raw in companies_raw.items():
    results[name] = {
        "ticker":  raw["ticker"],
        "color":   raw["color"],
        "sector":  raw["sector"],
        "hq":      raw["hq"],
        "founded": raw["founded"],
        "kpis":    compute_kpis(raw),
        "raw": {
            "revenue_fy23":      raw["revenue_fy23"],
            "revenue_fy22":      raw["revenue_fy22"],
            "net_income_fy23":   raw["net_income_fy23"],
            "total_equity_fy23": raw["total_equity_fy23"],
            "total_debt_fy23":   raw["total_debt_fy23"],
            "shares_outstanding": raw["shares_outstanding"],
        },
    }

scores       = score_companies(results)
verdict_data = verdict(results, scores)

for name in results:
    results[name]["scores"] = scores[name]

output = {
    "meta": {
        "title":       "Big Tech — SEC Financial KPI Comparison (FY 2023)",
        "sector":      "Technology",
        "fiscal_year": "FY 2023",
        "data_source": "U.S. SEC EDGAR 10-K Annual Filings",
        "currency":    "USD",
    },
    "companies": results,
    "verdict":   verdict_data,
    "kpi_definitions": {
        "revenue_bn":  "Total annual revenue in USD Billions.",
        "net_margin":  "Net Profit Margin (%) — Net Income divided by Revenue. Shows how much profit is generated per dollar of revenue.",
        "roe":         "Return on Equity (%) — Net Income divided by Shareholders Equity. Measures profitability relative to shareholder investment.",
        "de_ratio":    "Debt-to-Equity Ratio — Total Debt divided by Shareholders Equity. Lower values indicate a stronger balance sheet.",
        "eps":         "Earnings Per Share (USD) — Net Income divided by Diluted Shares Outstanding.",
        "rev_growth":  "Year-over-Year Revenue Growth (%) — (FY23 Revenue minus FY22 Revenue) divided by FY22 Revenue.",
    },
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

# ---------------------------------------------------------------------------
# CONSOLE SUMMARY
# ---------------------------------------------------------------------------

kpi_labels = {
    "revenue_bn":  "Revenue (USD Bn)",
    "net_margin":  "Net Margin (%)",
    "roe":         "ROE (%)",
    "de_ratio":    "D/E Ratio",
    "eps":         "EPS (USD)",
    "rev_growth":  "YoY Growth (%)",
}

print("\n" + "=" * 68)
print("  SEC Financial KPI Analysis -- Big Tech Sector  (FY 2023)")
print("=" * 68)
col_w = 14
header = f"{'Company':<13}" + "".join(f"{v:>{col_w}}" for v in kpi_labels.values())
print(header)
print("-" * len(header))

for name, info in results.items():
    row = f"{name:<13}"
    for kpi in kpi_labels:
        row += f"{info['kpis'][kpi]:>{col_w}}"
    print(row)

print()
print("-- KPI Leaders --")
for kpi, winner in verdict_data["best_per_kpi"].items():
    print(f"  {kpi_labels.get(kpi, kpi):<22}  ->  {winner}")

print()
print("-- Overall Ranking (cumulative normalised score) --")
for rank, name in enumerate(verdict_data["ranking"], 1):
    score  = verdict_data["cumulative"][name]
    marker = "  ** OVERALL BEST **" if rank == 1 else ""
    print(f"  {rank}. {name:<12}  {score:.1f} pts{marker}")

print()
print("  data.json written -- open index.html in your browser.")
print("=" * 68 + "\n")
