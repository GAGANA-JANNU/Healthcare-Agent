from ..ml.risk_model import predict_health_risk
from ..ml.anomaly import detect_anomaly


def analyze_node(state):
    risk = predict_health_risk(
        state["steps"],
        state["calories"],
        state["water_intake"],
        state["sleep_hours"],
        state["heart_rate"]
    )
    alerts = detect_anomaly(
        state["heart_rate"],
        state["sleep_hours"],
        state["water_intake"]
    )

    state["risk_level"] = risk
    state["alerts"] = alerts
    return state


def recommendation_node(state):
    if state["risk_level"] == "High Risk":
        state["recommendation"] = "Immediate lifestyle correction and doctor consultation recommended."
    elif state["risk_level"] == "Moderate Risk":
        state["recommendation"] = "Improve hydration, sleep, and activity levels."
    else:
        state["recommendation"] = "Current health pattern looks stable. Maintain healthy habits."

    return state