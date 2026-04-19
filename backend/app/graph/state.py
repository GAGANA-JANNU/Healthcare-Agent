from typing import TypedDict, List


class HealthState(TypedDict):
    patient_name: str
    steps: int
    calories: float
    water_intake: float
    sleep_hours: float
    heart_rate: int
    risk_level: str
    alerts: List[str]
    recommendation: str