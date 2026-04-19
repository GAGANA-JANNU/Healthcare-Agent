def generate_health_report(patient_name, fitness_records, medications, nutrition_records, symptoms):
    report = f"Health Report for {patient_name}\n"
    report += "=" * 50 + "\n\n"

    report += f"Total Fitness Records: {len(fitness_records)}\n"
    report += f"Total Medications: {len(medications)}\n"
    report += f"Total Nutrition Records: {len(nutrition_records)}\n"
    report += f"Total Symptom Records: {len(symptoms)}\n\n"

    if fitness_records:
        latest = fitness_records[-1]
        report += "Latest Fitness Summary:\n"
        report += f"- Steps: {latest.steps}\n"
        report += f"- Calories: {latest.calories}\n"
        report += f"- Water Intake: {latest.water_intake} L\n"
        report += f"- Sleep: {latest.sleep_hours} hrs\n"
        report += f"- Heart Rate: {latest.heart_rate} bpm\n\n"

    if medications:
        report += "Medication List:\n"
        for med in medications:
            report += f"- {med.medicine_name} ({med.dosage}) at {med.time} | Status: {med.status}\n"
        report += "\n"

    if nutrition_records:
        report += "Nutrition Summary:\n"
        for n in nutrition_records:
            report += f"- {n.meal_type}: {n.food_item} ({n.calories} kcal)\n"
        report += "\n"

    if symptoms:
        report += "Symptoms:\n"
        for s in symptoms:
            report += f"- {s.symptom} [{s.severity}] -> {s.advice}\n"

    return report