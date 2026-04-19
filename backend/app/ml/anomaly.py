def detect_anomaly(heart_rate, sleep_hours, water_intake):
    alerts = []

    if heart_rate > 110:
        alerts.append("Abnormally high heart rate detected")
    if sleep_hours < 4:
        alerts.append("Very low sleep duration detected")
    if water_intake < 1:
        alerts.append("Very low water intake detected")

    return alerts