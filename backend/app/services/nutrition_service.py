from sqlalchemy.orm import Session
from ..models import NutritionRecord


def add_nutrition_record(db: Session, data):
    record = NutritionRecord(
        patient_name=data.patient_name,
        meal_type=data.meal_type,
        food_item=data.food_item,
        calories=data.calories,
        protein=data.protein,
        carbs=data.carbs,
        fats=data.fats
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_nutrition_records(db: Session):
    return db.query(NutritionRecord).all()