def build_health_features(steps, calories, water_intake, sleep_hours, heart_rate):
    return {
        "low_steps": steps < 3000,
        "high_calories": calories > 2500,
        "low_water": water_intake < 2,
        "low_sleep": sleep_hours < 6,
        "high_heart_rate": heart_rate > 100
    }