from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from .db import Base


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    medicine_name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    time = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)


class FitnessRecord(Base):
    __tablename__ = "fitness_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    steps = Column(Integer, default=0)
    calories = Column(Float, default=0.0)
    water_intake = Column(Float, default=0.0)
    sleep_hours = Column(Float, default=0.0)
    heart_rate = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class NutritionRecord(Base):
    __tablename__ = "nutrition_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    meal_type = Column(String, nullable=False)
    food_item = Column(String, nullable=False)
    calories = Column(Float, default=0.0)
    protein = Column(Float, default=0.0)
    carbs = Column(Float, default=0.0)
    fats = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SymptomRecord(Base):
    __tablename__ = "symptom_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    symptom = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    notes = Column(Text, default="")
    advice = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)