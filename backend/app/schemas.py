from pydantic import BaseModel
from typing import Optional


class MedicationCreate(BaseModel):
    patient_name: str
    medicine_name: str
    dosage: str
    time: str


class MedicationStatusUpdate(BaseModel):
    status: str


class MedicationOut(MedicationCreate):
    id: int
    status: str

    class Config:
        from_attributes = True


class FitnessCreate(BaseModel):
    patient_name: str
    steps: int
    calories: float
    water_intake: float
    sleep_hours: float
    heart_rate: int


class FitnessOut(FitnessCreate):
    id: int

    class Config:
        from_attributes = True


class NutritionCreate(BaseModel):
    patient_name: str
    meal_type: str
    food_item: str
    calories: float
    protein: float
    carbs: float
    fats: float


class NutritionOut(NutritionCreate):
    id: int

    class Config:
        from_attributes = True


class SymptomCreate(BaseModel):
    patient_name: str
    symptom: str
    severity: str
    notes: Optional[str] = ""


class SymptomOut(SymptomCreate):
    id: int
    advice: str

    class Config:
        from_attributes = True