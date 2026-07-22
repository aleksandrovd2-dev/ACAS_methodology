from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="ACAS Methodology API",
    description="Микросервис для расчета рейтинга клиентов по методологии ACAS",
    version="1.0.0"

    @app.get("/")
def read_root():
    return {
        "message": "Добро пожаловать в ACAS API. Перейдите на /docs для тестирования расчетной модели."
    }
)

# Форма для входящих данных клиента
class ClientMetrics(BaseModel):
    vi: float  # Количество выставленных счетов
    vp: float  # Количество оплаченных счетов
    vr: float  # Количество возвратов
    ai: float  # Сумма выставленных счетов
    ap: float  # Сумма оплат
    ar: float  # Сумма возвратов
    pa: float  # Период активности (в месяцах)
    pl: float  # Длина периода сотрудничества (в месяцах)

@app.post("/calculate-acas/")
def calculate_acas(metrics: ClientMetrics):
    # Константы модели
    R1, PM, K = 0.5, 3.0, 2.0
    
    # 1. Защита от деления на ноль и расчет Weighted Efficiency (WE)
    if metrics.vi == 0 or metrics.ai == 0:
        we = 0.0
    else:
        we = max(0.0, min(1.0, 0.5 * (((metrics.vp - metrics.vr) / metrics.vi) + ((metrics.ap - metrics.ar) / metrics.ai))))
        
    # 2. Расчет Age Gap (AG) и Zero Pressure (ZP)
    ag = max(0.0, 1.0 - (metrics.pa / metrics.pl))
    zp = max(0.0, (metrics.vi - metrics.vp + metrics.vr) / metrics.pa)
    
    # 3. Индекс потерь (WI) и жесткий рейтинг (R2)
    wi = 0.5 * (ag + zp)
    r2 = we * max(0.0, 1.0 - wi)
    
    # 4. Взвешенный рейтинг по длительности (PL) и итоговый Score
    w_pl = 1.0 / (1.0 + (metrics.pl / PM) ** K)
    acas_score = (w_pl * R1 + (1.0 - w_pl) * r2) * 100
    
    # 5. Присвоение статуса
    if acas_score < 0.0:
        status = "Critical"
    elif acas_score <= 1.0:
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

    # Ответ микросервиса
    return {
        "WE": round(we, 2),
        "WI": round(wi, 2),
        "ACAS_Score_Percent": round(acas_score, 2),
        "Status": status
    }
