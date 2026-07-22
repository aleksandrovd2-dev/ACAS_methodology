from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="ACAS Methodology API",
    description="Microservice for calculating customer activity ratings based on the ACAS (Aleksandrov Customer Activity Scoring) methodology.",
    version="1.0.0"
)

# Input data model with descriptions for the Swagger UI
class customerMetrics(BaseModel):
    vi: float = Field(..., description="Volume of Invoices (Number of invoices issued)")
    vp: float = Field(..., description="Volume of Paid (Number of invoices paid)")
    vr: float = Field(..., description="Volume of Refunds (Number of refunds)")
    ai: float = Field(..., description="Amount Invoiced (Total sum of invoices)")
    ap: float = Field(..., description="Amount Paid (Total sum paid)")
    ar: float = Field(..., description="Amount Refunded (Total sum refunded)")
    pa: float = Field(..., description="Period of Activity (in months)")
    pl: float = Field(..., description="Period of Life (in months)")

# Route to handle the root URL (fixes the 404 error)
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the ACAS Scoring API. Please append '/docs' to the URL to access the interactive testing interface."
    }

# Main route for calculating the ACAS rating
@app.post("/calculate-acas/")
def calculate_acas(metrics: customerMetrics):
    # Model constants
    R1, PM, K = 0.5, 3.0, 2.0
    
    # 1. Protection against division by zero and calculation of Weighted Efficiency (WE)
    if metrics.vi == 0 or metrics.ai == 0:
        we = 0.0
    else:
        we = max(0.0, min(1.0, 0.5 * (((metrics.vp - metrics.vr) / metrics.vi) + ((metrics.ap - metrics.ar) / metrics.ai))))
        
    # 2. Calculation of Activity Gap (AG) and Zero Pressure (ZP)
    ag = max(0.0, 1.0 - (metrics.pa / metrics.pl))
    zp = max(0.0, (metrics.vi - metrics.vp + metrics.vr) / metrics.pa)
    
    # 3. Waste Index (WI) and Hard Rating (R2)
    wi = 0.5 * (ag + zp)
    r2 = we * max(0.0, 1.0 - wi)
    
    # 4. Lifecycle Smoothing (w_pl) and final ACAS Score
    w_pl = 1.0 / (1.0 + (metrics.pl / PM) ** K)
    acas_score = (w_pl * R1 + (1.0 - w_pl) * r2) * 100
    
    # 5. Status Matrix assignment based on business rules
    if acas_score < 0.0:
        status = "Critical"
    elif acas_score <= 0.99:
        status = "Zero"
    elif acas_score <= 5.0:
        status = "Very Low"
    elif acas_score <= 25.0:
        status = "Low"
    elif acas_score <= 65.0:
        status = "Medium"
    elif acas_score <= 95.0:
        status = "High"
    else:
        status = "Very High"

    # API Response
    return {
        "Weighted_Efficiency_WE": round(we, 2),
        "Waste_Index_WI": round(wi, 2),
        "ACAS_Score_Percent": round(acas_score, 2),
        "Status": status
    }
