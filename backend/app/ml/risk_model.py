from .features import build_health_features


def predict_health_risk(steps, calories, water_intake, sleep_hours, heart_rate):
    features = build_health_features(
        steps, calories, water_intake, sleep_hours, heart_rate
    )

    score = 0
    for _, value in features.items():
        if value:
            score += 1

    if steps < 2000 and sleep_hours < 5:
        return "High Risk"
    if score >= 4:
        return "High Risk"
    elif score >= 2:
        return "Moderate Risk"
    return "Low Risk"