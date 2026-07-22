# ACAS (Aleksandrov Customer Activity Scoring) Methodology
How Linear Algebra Saves B2B Marketing from "Empty" Customer.

## Overview
The topic of customer scoring is capable of drastically simplifying sales managers' workflows, revealing the true LTV (Lifetime Value) of counterparties, and providing an accurate assessment of their activity. This approach is strictly necessary when an enormous amount of a manager's working time is spent on a single customer with zero financial return. For instance, a customer may request an endless number of invoices or commercial proposals throughout the year without ever making a payment, or the payments are disproportionately small compared to the effort expended. This solution is primarily designed for B2B trading companies.

## Architecture and Calculation Stages
The ACAS mathematical model is a multi-level engineering system where calculations are divided into three sequential stages.

### Stage 1: Base Parameters and Hard Rating (R2) Formula
At this level, calendar dates from the CRM are converted into discrete time intervals to compute the rigid mathematical core.

**Base Variables:**
*   **WE (Weighted Efficiency)**
*   **VI (Volume of Invoices)**
*   **VP (Volume of Paid)**
*   **VR (Volume of Refunds)**
*   **AI (Amount Invoiced)**
*   **AP (Amount Paid)**
*   **AR (Amount Refunded)**
*   **PL (Period of Life)**
*   **PA (Period of Activity)**
*   **AG (Activity Gap)**
*   **ZP (Zero Pressure)**
*   **WI (Waste Index)**
*   **PM (Point of Maturation)**
*   **w(Pl) (Weight Period of Life)**
*   **R1 (Rating 1):** Fixed starting rating for a newcomer.
*   **R2 (Rating 2):** Strict calculated rating.
*   **k:** Transition steepness coefficient

**Calculation Sequence:**
*   **Period of Life (PL):** The number of 30-day intervals from the very first invoice to the current calculation date, rounded to one decimal place. Formula: `PL = (Calculation Date - First Invoice Date) / 30`. Calculations are strictly performed within a 12-month Rolling Window, so PL cannot exceed 12. This limits the denominator's growth and accounts for recency (if a customer has been silent for the last 6 months, their old merits stop affecting the current rating).
*   **Period of Activity (PA):** The count of unique discrete 30-day segments in which the customer was issued at least one invoice.
*   **Weighted Efficiency (WE):** A refund-adjusted weighted efficiency metric reflecting the customer's accuracy in fulfilling obligations (strictly ranging from 0 to 1). Formula: `WE = 0.5 * ((VP - VR)/VI + (AP - AR)/AI)`.
*   **Activity Gap (AG):** Demonstrates the density of the counterparty's interaction with the company. If invoices were issued every month, AG=0 (perfect density). If active for only 2 out of 12 months, AG = 1 - 2/12 = 0.84. Formula: `AG = 1 - (PA / PL)`.
*   **Zero Pressure (ZP):** Calculates the quantitative underpayment per active period, reflecting the level of "idle" operational load on managers. Formula: `ZP = (VI - VP + VR) / PA`.
*   **Waste Index (WI):** A comprehensive index of operational and time losses. Formula: `WI = 0.5 * (AG + ZP)`.
*   **Hard Rating (R2):** The unified synergistic formula. Formula: `R2 = WE * (1 - WI)`. The `(1 - WI)` multiplier acts as a penalty for passivity and destructive behavior. If this multiplier approaches 0, the rating of "sleeping" customers who request massive amounts of documents without regular purchases will drop exponentially hard.

### Stage 2: Lifecycle Smoothing (Adapted Hill Function)
To prevent artificial rating jumps caused by discrete IF-ELSE conditions at period boundaries, a dynamic attenuation weight function `w(PL)` is introduced.
The final rating is calculated as: `R_acas = w(PL) * R1 + (1 - w(PL)) * R2`.
Logistic smoothing function: `w(PL) = 1 / (1 + (PL / PM)^k)`.
*   **PM = 3:** The median point where the weight of the starting rating and real calculations is exactly 50/50.
*   **R1 = 0.5:** Fixed starting rating.
*   **k = 2:** Steepness coefficient.

### Stage 3: Status Matrix and Visualization
For operational convenience, the rating is converted into visual business statuses:
*   **< 0%:** Critical
*   **0% - 0,99%:** Zero
*   **1% - 5%:** Very Low
*   **5.01% - 25%:** Low
*   **25.01% - 65%:** Medium
*   **65.01% - 95%:** High
*   **95.01% - 100%:** Very High

## Sales & Marketing Alignment (Lead Routing)
customers with a low ACAS rating are removed from the sales department and transferred to marketing. Marketing initiates classical RFM analysis and begins to "wake up" this segment with automated emails and retargeting. Once their ACAS rating recovers, they return to the managers.

## Practical Calculation Examples

**customer 1: Promising Newbie**
*   **Inputs:** PL = 1.5, PA = 1, VI = 2, AI = 1.0, VP = 2, AP = 0.9.
*   **WE:** 0.5 * (2/2 + 0.9/1.0) = 0.95.
*   **AG:** 1 - (1/1.5) = 0.3333.
*   **ZP:** (1.0 - 0.9 + 0)/1 = 0.1.
*   **WI:** 0.5 * (0.3333 + 0.1) = 0.2167.
*   **R2:** 0.95 * (1 - 0.2167) = 0.7441.
*   **w(1.5):** 1 / (1 + (1.5/3)^2) = 0.8.
*   **Acas:** 0.8 * 0.5 + (1 - 0.8) * 0.7441 = 54.88% (Status: Medium).

**customer 2: Old "Time Burner" (Passive customer)**
*   **Inputs:** PL = 12, PA = 2, VI = 50, AI = 1.0, VP = 2, AP = 0.2.
*   **WE:** 0.5 * (2/50 + 0.2/1.0) = 0.12.
*   **AG:** 1 - (2/12) = 0.8333.
*   **ZP:** (1.0 - 0.2 + 0)/2 = 0.4.
*   **WI:** 0.5 * (0.8333 + 0.4) = 0.6167.
*   **R2:** 0.12 * (1 - 0.6167) = 0.0460.
*   **w(12):** 1 / (1 + (12/3)^2) = 0.0588.
*   **Acas:** 0.0588 * 0.5 + (1 - 0.0588) * 0.0460 = 7.27% (Status: Low).

**customer 3: Reliable Partner**
*   **Inputs:** PL = 6, PA = 6, VI = 12, AI = 1.0, VP = 12, AP = 1.0.
*   **WE:** 1.0.
*   **AG:** 0.
*   **ZP:** 0.
*   **WI:** 0.
*   **R2:** 1.0.
*   **w(6):** 0.2.
*   **Acas:** 0.2 * 0.5 + (1 - 0.2) * 1.0 = 90.0% (Status: High).

## Business Impact: Results in Company "N"
Implementation over 6 months revealed that 21% of the customer base had been generating invoices totaling over 1 billion rubles for years with zero final payments.
*   ACAS filtered out 81% of these unprofitable counterparties from managers' daily routines.
*   The active base load decreased by 17%.
*   Empty invoices decreased by 2%.
*   Invoice-to-payment conversion increased by 2%, and amount conversion grew by 5%.

## FAQ: Addressing Analyst Doubts
1.  **Why do newbies get a head start?** To prevent a "cold start" penalty during the initial 30-90 day onboarding period. The smoothing function grants them a temporary trust credit. As the customer ages, the math fully switches to the hard facts of their activity.
2.  **Why calculate amounts and quantities independently?** To prevent a scenario where a single large payment masks hundreds of unpaid small invoices that paralyze backend operations. Both metrics must be disciplined to maintain priority.
3.  **What if a strategic VIP is blocked?** The architecture mandates a "Whitelisting" mechanism at the CRM level. Strategic partners are excluded to protect them from automatic restrictions, leaving ACAS as a fair judge for the remaining 95% of the base.

## Live Demo (API Microservice):
**Test ACAS Methodology API here:** https://acas-methodology.onrender.com/docs
