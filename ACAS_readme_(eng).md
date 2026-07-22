# ACAS (Aleksandrov Customer Activity Scoring) Methodology[cite: 1]
How Linear Algebra Saves B2B Marketing from "Empty" Clients[cite: 1]

## Overview[cite: 1]
The topic of customer scoring is capable of drastically simplifying sales managers' workflows, revealing the true LTV (Lifetime Value) of counterparties, and providing an accurate assessment of their activity[cite: 1]. This approach is strictly necessary when an enormous amount of a manager's working time is spent on a single client with zero financial return[cite: 1]. For instance, a client may request an endless number of invoices or commercial proposals throughout the year without ever making a payment, or the payments are disproportionately small compared to the effort expended[cite: 1]. This solution is primarily designed for B2B trading companies[cite: 1].

## Architecture and Calculation Stages[cite: 1]
The ACAS mathematical model is a multi-level engineering system where calculations are divided into three sequential stages[cite: 1].

### Stage 1: Base Parameters and Hard Rating (R2) Formula[cite: 1]
At this level, calendar dates from the CRM are converted into discrete time intervals to compute the rigid mathematical core[cite: 1].

**Base Variables:**
*   **WE (Weighted Efficiency):** Взвешенная эффективность[cite: 1].
*   **VI (Volume of Invoices):** Количество счетов[cite: 1].
*   **VP (Volume of Paid):** Количество оплат[cite: 1].
*   **VR (Volume of Refunds):** Количество возвратов[cite: 1].
*   **AI (Amount Invoiced):** Сумма счетов[cite: 1].
*   **AP (Amount Paid):** Сумма оплат[cite: 1].
*   **AR (Amount Refunded):** Сумма возвратов[cite: 1].
*   **PL (Period of Life):** Период жизни клиента[cite: 1].
*   **PA (Period of Activity):** Период активности клиента[cite: 1].
*   **AG (Activity Gap):** Коэффициент потери активности[cite: 1].
*   **ZP (Zero Pressure):** Коэффициент нулевого давления[cite: 1].
*   **WI (Waste Index):** Индекс потерь[cite: 1].
*   **PM (Point of Maturation):** Точка медианного созревания[cite: 1].
*   **w(Pl) (Weight Period of Life):** Весовая функция периода жизни клиента[cite: 1].
*   **R1 (Rating 1):** Фиксированный стартовый рейтинг новичка[cite: 1].
*   **R2 (Rating 2):** Жесткий расчетный рейтинг[cite: 1].
*   **k:** Коэффициент крутизны перехода[cite: 1].

**Calculation Sequence:**
*   **Period of Life (PL):** The number of 30-day intervals from the very first invoice to the current calculation date, rounded to one decimal place[cite: 1]. Formula: `PL = (Calculation Date - First Invoice Date) / 30`[cite: 1]. Calculations are strictly performed within a 12-month Rolling Window, so PL cannot exceed 12[cite: 1]. This limits the denominator's growth and accounts for recency (if a client has been silent for the last 6 months, their old merits stop affecting the current rating)[cite: 1].
*   **Period of Activity (PA):** The count of unique discrete 30-day segments in which the client was issued at least one invoice[cite: 1].
*   **Weighted Efficiency (WE):** A refund-adjusted weighted efficiency metric reflecting the client's accuracy in fulfilling obligations (strictly ranging from 0 to 1)[cite: 1]. Formula: `WE = 0.5 * ((VP - VR)/VI + (AP - AR)/AI)`[cite: 1].
*   **Activity Gap (AG):** Demonstrates the density of the counterparty's interaction with the company[cite: 1]. If invoices were issued every month, AG=0 (perfect density)[cite: 1]. If active for only 2 out of 12 months, AG = 1 - 2/12 = 0.84[cite: 1]. Formula: `AG = 1 - (PA / PL)`[cite: 1].
*   **Zero Pressure (ZP):** Calculates the quantitative underpayment per active period, reflecting the level of "idle" operational load on managers[cite: 1]. Formula: `ZP = (VI - VP + VR) / PA`[cite: 1].
*   **Waste Index (WI):** A comprehensive index of operational and time losses[cite: 1]. Formula: `WI = 0.5 * (AG + ZP)`[cite: 1].
*   **Hard Rating (R2):** The unified synergistic formula[cite: 1]. Formula: `R2 = WE * (1 - WI)`[cite: 1]. The `(1 - WI)` multiplier acts as a penalty for passivity and destructive behavior[cite: 1]. If this multiplier approaches 0, the rating of "sleeping" clients who request massive amounts of documents without regular purchases will drop exponentially hard[cite: 1].

### Stage 2: Lifecycle Smoothing (Adapted Hill Function)[cite: 1]
To prevent artificial rating jumps caused by discrete IF-ELSE conditions at period boundaries, a dynamic attenuation weight function `w(PL)` is introduced[cite: 1].
The final rating is calculated as: `R_acas = w(PL) * R1 + (1 - w(PL)) * R2`[cite: 1].
Logistic smoothing function: `w(PL) = 1 / (1 + (PL / PM)^k)`[cite: 1].
*   **PM = 3:** The median point where the weight of the starting rating and real calculations is exactly 50/50[cite: 1].
*   **R1 = 0.5:** Fixed starting rating[cite: 1].
*   **k = 2:** Steepness coefficient[cite: 1].

### Stage 3: Status Matrix and Visualization[cite: 1]
For operational convenience, the rating is converted into visual business statuses[cite: 1]:
*   **< 0%:** Critical[cite: 1]
*   **0% - 1%:** Zero[cite: 1]
*   **1.01% - 5%:** Very Low[cite: 1]
*   **5.01% - 25%:** Low[cite: 1]
*   **25.01% - 65%:** Medium[cite: 1]
*   **65.01% - 95%:** High[cite: 1]
*   **95.01% - 100%:** Very High[cite: 1]

## Sales & Marketing Alignment (Lead Routing)[cite: 1]
Clients with a low ACAS rating are removed from the sales department and transferred to marketing[cite: 1]. Marketing initiates classical RFM analysis and begins to "wake up" this segment with automated emails and retargeting[cite: 1]. Once their ACAS rating recovers, they return to the managers[cite: 1].

## Practical Calculation Examples[cite: 1]

**Client 1: Promising Newbie[cite: 1]**
*   **Inputs:** PL = 1.5, PA = 1, VI = 2, AI = 1.0, VP = 2, AP = 0.9[cite: 1].
*   **WE:** 0.5 * (2/2 + 0.9/1.0) = 0.95[cite: 1].
*   **AG:** 1 - (1/1.5) = 0.3333[cite: 1].
*   **ZP:** (1.0 - 0.9 + 0)/1 = 0.1[cite: 1].
*   **WI:** 0.5 * (0.3333 + 0.1) = 0.2167[cite: 1].
*   **R2:** 0.95 * (1 - 0.2167) = 0.7441[cite: 1].
*   **w(1.5):** 1 / (1 + (1.5/3)^2) = 0.8[cite: 1].
*   **R_acas:** 0.8 * 0.5 + (1 - 0.8) * 0.7441 = 54.88% (Status: Medium)[cite: 1].

**Client 2: Old "Time Burner" (Passive Client)[cite: 1]**
*   **Inputs:** PL = 12, PA = 2, VI = 50, AI = 1.0, VP = 2, AP = 0.2[cite: 1].
*   **WE:** 0.5 * (2/50 + 0.2/1.0) = 0.12[cite: 1].
*   **AG:** 1 - (2/12) = 0.8333[cite: 1].
*   **ZP:** (1.0 - 0.2 + 0)/2 = 0.4[cite: 1].
*   **WI:** 0.5 * (0.8333 + 0.4) = 0.6167[cite: 1].
*   **R2:** 0.12 * (1 - 0.6167) = 0.0460[cite: 1].
*   **w(12):** 1 / (1 + (12/3)^2) = 0.0588[cite: 1].
*   **R_acas:** 0.0588 * 0.5 + (1 - 0.0588) * 0.0460 = 7.27% (Status: Low)[cite: 1].

**Client 3: Reliable Partner[cite: 1]**
*   **Inputs:** PL = 6, PA = 6, VI = 12, AI = 1.0, VP = 12, AP = 1.0[cite: 1].
*   **WE:** 1.0[cite: 1].
*   **AG:** 0[cite: 1].
*   **ZP:** 0[cite: 1].
*   **WI:** 0[cite: 1].
*   **R2:** 1.0[cite: 1].
*   **w(6):** 0.2[cite: 1].
*   **R_acas:** 0.2 * 0.5 + (1 - 0.2) * 1.0 = 90.0% (Status: High)[cite: 1].

## Business Impact: Results in Company "N"[cite: 1]
Implementation over 6 months revealed that 21% of the client base had been generating invoices totaling over 1 billion rubles for years with zero final payments[cite: 1].
*   ACAS filtered out 81% of these unprofitable counterparties from managers' daily routines[cite: 1].
*   The active base load decreased by 17%[cite: 1].
*   Empty invoices decreased by 2%[cite: 1].
*   Invoice-to-payment conversion increased by 2%, and amount conversion grew by 5%[cite: 1].

## FAQ: Addressing Analyst Doubts[cite: 1]
1.  **Why do newbies get a head start?** To prevent a "cold start" penalty during the initial 30-90 day onboarding period[cite: 1]. The smoothing function grants them a temporary trust credit[cite: 1]. As the client ages, the math fully switches to the hard facts of their activity[cite: 1].
2.  **Why calculate amounts and quantities independently?** To prevent a scenario where a single large payment masks hundreds of unpaid small invoices that paralyze backend operations[cite: 1]. Both metrics must be disciplined to maintain priority[cite: 1].
3.  **What if a strategic VIP is blocked?** The architecture mandates a "Whitelisting" mechanism at the CRM level[cite: 1]. Strategic partners are excluded to protect them from automatic restrictions, leaving ACAS as a fair judge for the remaining 95% of the base[cite: 1].
