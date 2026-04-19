from sqlalchemy.orm import Session
from ..models import Medication


def add_medication(db: Session, data):
    medication = Medication(
        patient_name=data.patient_name,
        medicine_name=data.medicine_name,
        dosage=data.dosage,
        time=data.time,
        status="pending"
    )
    db.add(medication)
    db.commit()
    db.refresh(medication)
    return medication


def get_medications(db: Session):
    return db.query(Medication).all()


def delete_medication(db: Session, med_id: int):
    med = db.query(Medication).filter(Medication.id == med_id).first()
    if med:
        db.delete(med)
        db.commit()
        return True
    return False


def update_medication_status(db: Session, med_id: int, status: str):
    med = db.query(Medication).filter(Medication.id == med_id).first()
    if not med:
        return None
    med.status = status
    db.commit()
    db.refresh(med)
    return med