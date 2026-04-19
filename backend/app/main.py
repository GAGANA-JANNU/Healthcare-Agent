from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import schemas
from .services import (
    medication_service,
    fitness_service,
    nutrition_service,
    symptom_service,
    research_service,
    report_service
)
from .models import FitnessRecord, Medication, NutritionRecord, SymptomRecord
from .graph.workflow import build_health_workflow

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthcare Track B API")

workflow = build_health_workflow()


@app.get("/")
def root():
    return {"message": "Healthcare Track B Backend Running"}


@app.post("/medications")
def create_medication(data: schemas.MedicationCreate, db: Session = Depends(get_db)):
    return medication_service.add_medication(db, data)


@app.get("/medications")
def read_medications(db: Session = Depends(get_db)):
    return medication_service.get_medications(db)


@app.put("/medications/{med_id}")
def change_medication_status(med_id: int, data: schemas.MedicationStatusUpdate, db: Session = Depends(get_db)):
    updated = medication_service.update_medication_status(db, med_id, data.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Medication not found")
    return updated


@app.delete("/medications/{med_id}")
def remove_medication(med_id: int, db: Session = Depends(get_db)):
    deleted = medication_service.delete_medication(db, med_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Medication not found")
    return {"message": "Medication deleted successfully"}


@app.post("/fitness")
def create_fitness(data: schemas.FitnessCreate, db: Session = Depends(get_db)):
    record = fitness_service.add_fitness_record(db, data)
    analysis = fitness_service.analyze_fitness(data)

    state = {
        "patient_name": data.patient_name,
        "steps": data.steps,
        "calories": data.calories,
        "water_intake": data.water_intake,
        "sleep_hours": data.sleep_hours,
        "heart_rate": data.heart_rate,
        "risk_level": "",
        "alerts": [],
        "recommendation": ""
    }

    result = workflow.invoke(state)

    return {
        "record": {
            "id": record.id,
            "patient_name": record.patient_name,
            "steps": record.steps,
            "calories": record.calories,
            "water_intake": record.water_intake,
            "sleep_hours": record.sleep_hours,
            "heart_rate": record.heart_rate
        },
        "analysis": analysis,
        "workflow_result": result
    }


@app.get("/fitness")
def read_fitness(db: Session = Depends(get_db)):
    return fitness_service.get_fitness_records(db)


@app.post("/nutrition")
def create_nutrition(data: schemas.NutritionCreate, db: Session = Depends(get_db)):
    return nutrition_service.add_nutrition_record(db, data)


@app.get("/nutrition")
def read_nutrition(db: Session = Depends(get_db)):
    return nutrition_service.get_nutrition_records(db)


@app.post("/symptoms")
def create_symptom(data: schemas.SymptomCreate, db: Session = Depends(get_db)):
    return symptom_service.add_symptom_record(db, data)


@app.get("/symptoms")
def read_symptoms(db: Session = Depends(get_db)):
    return symptom_service.get_symptom_records(db)


@app.get("/research/{topic}")
def research(topic: str):
    return {"topic": topic, "summary": research_service.get_medical_research(topic)}


@app.get("/report/{patient_name}")
def generate_report(patient_name: str, db: Session = Depends(get_db)):
    fitness_records = db.query(FitnessRecord).filter(FitnessRecord.patient_name == patient_name).all()
    medications = db.query(Medication).filter(Medication.patient_name == patient_name).all()
    nutrition_records = db.query(NutritionRecord).filter(NutritionRecord.patient_name == patient_name).all()
    symptoms = db.query(SymptomRecord).filter(SymptomRecord.patient_name == patient_name).all()

    report = report_service.generate_health_report(
        patient_name, fitness_records, medications, nutrition_records, symptoms
    )

    return {"patient_name": patient_name, "report": report}