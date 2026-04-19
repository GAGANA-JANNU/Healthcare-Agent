def get_medical_research(topic: str):
    topic = topic.lower()

    research_db = {
        "diabetes": "Diabetes management includes balanced diet, exercise, glucose monitoring, and regular doctor consultation.",
        "hypertension": "Hypertension can be managed through reduced salt intake, exercise, stress management, and medications.",
        "anemia": "Anemia may improve with iron-rich foods, supplements, and treatment of underlying causes.",
        "fever": "Fever is often a sign of infection. Hydration, rest, and monitoring are important.",
        "headache": "Headache may be due to stress, dehydration, lack of sleep, or other causes. Rest and hydration can help in mild cases.",
        "nutrition": "Balanced nutrition includes proteins, carbohydrates, healthy fats, vitamins, minerals, and proper hydration."
    }

    return research_db.get(
        topic,
        f"No detailed medical research found for '{topic}', but regular professional consultation is recommended."
    )