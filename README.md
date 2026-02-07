IRRBB Risk Engine – ALM Simulation Project

Goal of the project?

This project was built to understand how banks measure Interest Rate Risk in the Banking Book (IRRBB) in practice.
Rather than focusing only on formulas, the goal is to simulate how a large balance sheet is transformed into risk metrics that are commonly discussed in Asset-Liability Management 
(ALM): repricing gaps, Net Interest Income (NII) sensitivity, and Economic Value of Equity (EVE) sensitivity.

Project Overview

The model simulates an end-to-end IRRBB framework using a large synthetic balance sheet (1,000,000 instruments).It evaluates the impact of a parallel interest rate shock on:

* Repricing Gap structure
* Net Interest Income (NII)
* Economic Value of Equity (EVE)
* EVE / Capital ratio (as a simplified risk indicator)

The focus is on understanding risk mechanics, not on building a production or regulatory reporting system.

Financial Perspective

Two common IRRBB perspectives are modeled, inspired by standard ALM approaches:

1. Earnings Perspective (NII Sensitivity)

Measures the short-term impact of interest rate changes on 12-month net interest income, based on repricing gaps across maturity buckets.

2. Economic Value Perspective (EVE Sensitivity)

Measures the long-term sensitivity of the bank’s economic value using a duration-based approximation.

These two perspectives often move in different directions, highlighting the trade-off between short-term earnings and long-term value.

---

Model Components

1. Synthetic Balance Sheet Generation

A large-scale synthetic balance sheet is generated using random sampling:

* Assets: Commercial loans, consumer loans, government bonds, project finance
* Liabilities: Demand deposits, time deposits, interbank funding, issued eurobonds

Each instrument has an amount, contractual maturity, and interest rate.

---

2. Behavioral Maturity Adjustment

Demand deposits are treated as non-maturity deposits (NMDs).
Instead of their contractual overnight maturity, they are assigned a behavioral maturity of 36 months to reflect funding stability.

This highlights how behavioral assumptions can materially affect interest rate risk outcomes.

---

3. Selective Repricing Beta

To reflect realistic repricing behavior:

* Demand deposits: 40% repricing beta (sticky pricing)
* All other instruments: 100% repricing beta

The beta is applied in the economic value (EVE) calculation to adjust price sensitivity.

---

4. Duration Approximation

Price sensitivity is approximated using a simple duration proxy:

> Duration ≈ (Adjusted Maturity / 12) × 0.85

This approximation is used for educational purposes and avoids explicit cash-flow modeling.

---

Risk Calculations

1. Repricing Gap Analysis

Instruments are allocated into maturity buckets:

* 0–1M
* 1–3M
* 3–6M
* 6–12M
* 12M+

For each bucket:

> Gap = Rate-Sensitive Assets − Rate-Sensitive Liabilities

Both period gaps and cumulative gaps are reported.

---

2. NII Sensitivity (Parallel Shock)

A +200 basis point parallel interest rate shock is applied.

NII impact is calculated using bucket-level gaps and time weights:

> NII Impact ≈ Gap × Shock × Time Weight

This provides an intuitive view of short-term earnings exposure.

---

3. EVE Sensitivity (Duration-Based)

Economic value sensitivity is calculated using dollar duration:

> ΔEVE ≈ − (Asset Dollar Duration − Liability Dollar Duration) × Shock

The model also reports:

> EVE / Capital Ratio

This ratio is used as a simplified indicator of balance sheet vulnerability , not as a formal regulatory test.

---

Assumptions & Simplifications

This project intentionally simplifies reality:

* Parallel and instantaneous interest rate shocks
* No explicit cash-flow modeling
* Fixed behavioral maturity for demand deposits
* Duration used as a proxy, not a full valuation model
* No optionality or convexity effects

These simplifications help keep the focus on core IRRBB concepts.


Technical Implementation

* Implemented in Python using NumPy and Pandas
* Fully vectorized (no loops)
* Processes 1,000,000 instruments in ~2 seconds on a standard machine

The focus is on clarity, scalability, and transparent logic rather than production optimization.

---

What This Project Shows

* How maturity transformation drives interest rate risk
* Why NII and EVE sensitivities can move in opposite directions
* The impact of behavioral assumptions on measured risk
* How large portfolios can be analyzed efficiently using vectorized operations

---

How to Run

```bash
python irrbb_model.py
```

The script outputs:

* Repricing gap table
* Total NII impact
* ΔEVE
* EVE / Capital ratio
* Execution time

---

Intended Use

This project is designed as:

* A learning tool for IRRBB and ALM concepts
* A discussion piece for interviews
* A demonstration of financial modeling and data-handling skills

It is not intended for regulatory reporting or production use.
