from sqlalchemy.orm import Session
from ..models import FitnessRecord
from ..ml.risk_model import predict_health_risk
from ..ml.anomaly import detect_anomaly


def add_fitness_record(db: Session, data):
    record = FitnessRecord(
        patient_name=data.patient_name,
        steps=data.steps,
        calories=data.calories,
        water_intake=data.water_intake,
        sleep_hours=data.sleep_hours,
        heart_rate=data.heart_rate
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_fitness_records(db: Session):
    return db.query(FitnessRecord).all()


def analyze_fitness(data):
    risk = predict_health_risk(
        data.steps, data.calories, data.water_intake, data.sleep_hours, data.heart_rate
    )
    alerts = detect_anomaly(data.heart_rate, data.sleep_hours, data.water_intake)

    return {
        "risk_level": risk,
        "alerts": alerts
    }