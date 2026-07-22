from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="ACAS Methodology API",
    description="Микросервис для расчета рейтинга активности клиентов по методологии ACAS (Aleksandrov Customer Activity Scoring).",
    version="1.0.0"
)

# Модель входящих данных с русскоязычными описаниями для Swagger UI
class ClientMetrics(BaseModel):
    vi: float = Field(..., description="Количество выставленных счетов (VI)")
    vp: float = Field(..., description="Количество оплаченных счетов (VP)")
    vr: float = Field(..., description="Количество возвратов (VR)")
    ai: float = Field(..., description="Общая сумма выставленных счетов (AI)")
    ap: float = Field(..., description="Общая сумма оплат (AP)")
    ar: float = Field(..., description="Общая сумма возвратов (AR)")
    pa: float = Field(..., description="Период активности клиента в месяцах (PA)")
    pl: float = Field(..., description="Период жизни клиента в месяцах (PL)")

# Обработчик корневого адреса (устраняет ошибку 404 и приветствует пользователя)
@app.get("/")
def read_root():
    return {
        "сообщение": "Добро пожаловать в ACAS Scoring API. Добавьте '/docs' в конец URL-адреса, чтобы открыть интерактивный интерфейс тестирования."
    }

# Основной метод для расчета рейтинга ACAS
@app.post("/calculate-acas/")
def calculate_acas(metrics: ClientMetrics):
    # Константы модели
    R1, PM, K = 0.5, 3.0, 2.0
    
    # 1. Защита от деления на ноль и расчет Взвешенной эффективности (WE)
    if metrics.vi == 0 or metrics.ai == 0:
        we = 0.0
    else:
        we = max(0.0, min(1.0, 0.5 * (((metrics.vp - metrics.vr) / metrics.vi) + ((metrics.ap - metrics.ar) / metrics.ai))))
        
    # 2. Расчет Коэффициента потери активности (AG) и Нулевого давления (ZP)
    ag = max(0.0, 1.0 - (metrics.pa / metrics.pl))
    zp = max(0.0, (metrics.vi - metrics.vp + metrics.vr) / metrics.pa)
    
    # 3. Индекс потерь (WI) и Жесткий рейтинг (R2)
    wi = 0.5 * (ag + zp)
    r2 = we * max(0.0, 1.0 - wi)
    
    # 4. Динамическое сглаживание (w_pl) и итоговый балл ACAS
    w_pl = 1.0 / (1.0 + (metrics.pl / PM) ** K)
    acas_score = (w_pl * R1 + (1.0 - w_pl) * r2) * 100
    
    # 5. Присвоение статуса на основе матрицы бизнес-правил
    if acas_score < 0.0:
        status = "Критический"
    elif acas_score <= 0.99:
        status = "Нулевой"
    elif acas_score <= 5.0:
        status = "Очень низкий"
    elif acas_score <= 25.0:
        status = "Низкий"
    elif acas_score <= 65.0:
        status = "Средний"
    elif acas_score <= 95.0:
        status = "Высокий"
    else:
        status = "Очень высокий"

    # Ответ микросервиса (на русском языке)
    return {
        "Взвешенная_эффективность_WE": round(we, 2),
        "Индекс_потерь_WI": round(wi, 2),
        "Рейтинг_ACAS_Процент": round(acas_score, 2),
        "Статус": status
    }
