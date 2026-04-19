from sqlalchemy.orm import Session
from ..models import SymptomRecord


def symptom_advice(symptom: str, severity: str):
    symptom = symptom.lower()
    severity = severity.lower()

    if "fever" in symptom:
        return "Drink plenty of fluids, take rest, and monitor temperature. Visit a doctor if fever continues."
    if "headache" in symptom:
        return "Stay hydrated, take rest, and avoid screen strain. Seek medical help if severe."
    if "cough" in symptom:
        return "Use warm fluids and rest. If breathing issues occur, consult a doctor."
    if "stomach" in symptom:
        return "Eat light food, stay hydrated, and monitor symptoms."
    if "throat" in symptom:
        return "Use warm water, avoid cold items, and take rest. Consult a doctor if pain worsens."
    return f"For {severity} {symptom}, basic rest and hydration are advised. If symptoms worsen, contact a doctor."


def add_symptom_record(db: Session, data):
    advice = symptom_advice(data.symptom, data.severity)
    record = SymptomRecord(
        patient_name=data.patient_name,
        symptom=data.symptom,
        severity=data.severity,
        notes=data.notes,
        advice=advice
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_symptom_records(db: Session):
    return db.query(SymptomRecord).all()