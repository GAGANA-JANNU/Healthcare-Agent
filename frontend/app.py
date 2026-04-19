import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Healthcare Track B", layout="wide")

st.markdown("""
<style>
.main {
    background-color: #f8fbff;
}
h1, h2, h3 {
    color: #1f3b73;
}
.stButton>button {
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = ""
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:
    st.title("🔐 Healthcare Monitoring AI Agent - Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", ["Patient", "Doctor", "Caregiver"])

    if st.button("Login"):
        # Simple demo login
        if username and password:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.username = username
            st.success(f"Welcome {username} ({role})")
            st.rerun()
        else:
            st.error("Please enter username and password")

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("Choose Module")
st.sidebar.write(f"👤 User: {st.session_state.username}")
st.sidebar.write(f"🩺 Role: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.username = ""
    st.rerun()

menu = st.sidebar.radio(
    "",
    [
        "Home",
        "Medication Tracker",
        "Fitness Tracker",
        "Nutrition Tracker",
        "Symptom Checker",
        "Medical Research",
        "Health Report",
        "AI Chatbot",
        "Dashboard"
    ]
)

# ---------------- HOME ----------------
if menu == "Home":
    st.title("🏥 Healthcare Monitoring AI Agent - Track B")
    st.markdown("This is not a diagnosis tool. It helps track health data and basic suggestions.")
    st.subheader("Welcome")
    st.write("Track medication, fitness, nutrition, symptoms, research, and reports.")

    col1, col2, col3 = st.columns(3)
    col1.info("💊 Medication Management")
    col2.info("🏃 Fitness Analysis")
    col3.info("🤖 AI Health Assistance")

# ---------------- MEDICATION ----------------
elif menu == "Medication Tracker":
    st.title("💊 Medication Tracker")

    with st.form("med_form"):
        patient_name = st.text_input("Patient Name")
        medicine_name = st.text_input("Medicine Name")
        dosage = st.text_input("Dosage")
        time = st.text_input("Time")
        submitted = st.form_submit_button("Add Medication")

        if submitted:
            payload = {
                "patient_name": patient_name,
                "medicine_name": medicine_name,
                "dosage": dosage,
                "time": time
            }
            res = requests.post(f"{API}/medications", json=payload)
            if res.status_code == 200:
                st.success("Medication added successfully")
            else:
                st.error("Failed to add medication")

    if st.button("Show Medications"):
        res = requests.get(f"{API}/medications")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)

                st.subheader("Update Medication Status")
                med_id = st.number_input("Enter Medication ID", min_value=1, step=1)
                status = st.selectbox("Select Status", ["taken", "missed", "pending"])

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Update Status"):
                        res2 = requests.put(
                            f"{API}/medications/{int(med_id)}",
                            json={"status": status}
                        )
                        if res2.status_code == 200:
                            st.success("Medication status updated")
                        else:
                            st.error("Could not update status")

                with col2:
                    if st.button("Delete Medication"):
                        res3 = requests.delete(f"{API}/medications/{int(med_id)}")
                        if res3.status_code == 200:
                            st.success("Medication deleted")
                        else:
                            st.error("Could not delete medication")
            else:
                st.info("No medications found")

# ---------------- FITNESS ----------------
elif menu == "Fitness Tracker":
    st.title("🏃 Fitness Tracker")

    with st.form("fitness_form"):
        patient_name = st.text_input("Patient Name", key="fit_name")
        steps = st.number_input("Steps", min_value=0, step=100)
        calories = st.number_input("Calories", min_value=0.0, step=10.0)
        water_intake = st.number_input("Water Intake (Liters)", min_value=0.0, step=0.5)
        sleep_hours = st.number_input("Sleep Hours", min_value=0.0, step=0.5)
        heart_rate = st.number_input("Heart Rate", min_value=0, step=1)
        submitted = st.form_submit_button("Add Fitness Record")

        if submitted:
            payload = {
                "patient_name": patient_name,
                "steps": steps,
                "calories": calories,
                "water_intake": water_intake,
                "sleep_hours": sleep_hours,
                "heart_rate": heart_rate
            }
            res = requests.post(f"{API}/fitness", json=payload)
            if res.status_code == 200:
                result = res.json()
                st.success("Fitness record added")
                st.write("### Analysis")
                st.json(result["analysis"])
                st.write("### Workflow Result")
                st.json(result["workflow_result"])
            else:
                st.error("Failed to add fitness record")

    if st.button("Show Fitness Records"):
        res = requests.get(f"{API}/fitness")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)

                st.subheader("Fitness Charts")

                if "steps" in df.columns:
                    fig, ax = plt.subplots()
                    ax.plot(df["steps"])
                    ax.set_title("Steps Trend")
                    ax.set_xlabel("Record Index")
                    ax.set_ylabel("Steps")
                    st.pyplot(fig)

                if "heart_rate" in df.columns:
                    fig2, ax2 = plt.subplots()
                    ax2.plot(df["heart_rate"])
                    ax2.set_title("Heart Rate Trend")
                    ax2.set_xlabel("Record Index")
                    ax2.set_ylabel("Heart Rate")
                    st.pyplot(fig2)
            else:
                st.info("No fitness records found")

# ---------------- NUTRITION ----------------
elif menu == "Nutrition Tracker":
    st.title("🍎 Nutrition Tracker")

    with st.form("nutrition_form"):
        patient_name = st.text_input("Patient Name", key="nut_name")
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
        food_item = st.text_input("Food Item")
        calories = st.number_input("Calories", min_value=0.0, step=10.0, key="nut_cal")
        protein = st.number_input("Protein", min_value=0.0, step=1.0)
        carbs = st.number_input("Carbs", min_value=0.0, step=1.0)
        fats = st.number_input("Fats", min_value=0.0, step=1.0)
        submitted = st.form_submit_button("Add Nutrition Record")

        if submitted:
            payload = {
                "patient_name": patient_name,
                "meal_type": meal_type,
                "food_item": food_item,
                "calories": calories,
                "protein": protein,
                "carbs": carbs,
                "fats": fats
            }
            res = requests.post(f"{API}/nutrition", json=payload)
            if res.status_code == 200:
                st.success("Nutrition record added")
            else:
                st.error("Failed to add nutrition record")

    if st.button("Show Nutrition Records"):
        res = requests.get(f"{API}/nutrition")
        if res.status_code == 200:
            data = res.json()
            if data:
                st.dataframe(pd.DataFrame(data))
            else:
                st.info("No nutrition records found")

# ---------------- SYMPTOM CHECKER ----------------
elif menu == "Symptom Checker":
    st.title("🤒 Symptom Checker")

    with st.form("symptom_form"):
        patient_name = st.text_input("Patient Name", key="sym_name")
        symptom = st.text_input("Symptom")
        severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe"])
        notes = st.text_area("Additional Notes")
        submitted = st.form_submit_button("Check Symptom")

        if submitted:
            payload = {
                "patient_name": patient_name,
                "symptom": symptom,
                "severity": severity,
                "notes": notes
            }
            res = requests.post(f"{API}/symptoms", json=payload)
            if res.status_code == 200:
                result = res.json()
                st.success("Symptom saved")
                st.write("### Advice")
                st.write(result["advice"])
            else:
                st.error("Failed to save symptom")

    if st.button("Show Symptom Records"):
        res = requests.get(f"{API}/symptoms")
        if res.status_code == 200:
            data = res.json()
            if data:
                st.dataframe(pd.DataFrame(data))
            else:
                st.info("No symptom records found")

# ---------------- MEDICAL RESEARCH ----------------
elif menu == "Medical Research":
    st.title("🔍 Medical Research Lookup")

    topic = st.text_input("Enter topic (example: diabetes, fever, anemia)")
    if st.button("Search Research"):
        res = requests.get(f"{API}/research/{topic}")
        if res.status_code == 200:
            st.success("Research found")
            st.write(res.json()["summary"])
        else:
            st.error("Unable to fetch research")

# ---------------- HEALTH REPORT ----------------
elif menu == "Health Report":
    st.title("📋 Health Report")

    patient_name = st.text_input("Enter patient name")
    if st.button("Generate Report"):
        res = requests.get(f"{API}/report/{patient_name}")
        if res.status_code == 200:
            st.text_area("Health Report", res.json()["report"], height=400)
        else:
            st.error("Unable to generate report")

# ---------------- AI CHATBOT ----------------
elif menu == "AI Chatbot":
    st.title("🤖 AI Health Chatbot")
    st.write("Ask a basic health-related question.")

    user_input = st.text_input("Ask your question")

    if st.button("Get Advice"):
        text = user_input.lower()

        if "fever" in text:
            st.write("Advice: Drink fluids, take proper rest, and monitor body temperature.")
        elif "headache" in text:
            st.write("Advice: Stay hydrated, reduce screen time, and rest.")
        elif "cough" in text:
            st.write("Advice: Drink warm fluids and monitor breathing. Seek help if severe.")
        elif "diet" in text or "nutrition" in text:
            st.write("Advice: Follow a balanced diet with protein, carbohydrates, vitamins, and enough water.")
        elif "diabetes" in text:
            st.write("Advice: Maintain diet control, regular exercise, and blood sugar monitoring.")
        else:
            st.write("Advice: This system gives basic suggestions only. Please consult a doctor for proper diagnosis.")

# ---------------- DASHBOARD ----------------
elif menu == "Dashboard":
    st.title("📊 Health Dashboard")

    try:
        fit_res = requests.get(f"{API}/fitness")
        med_res = requests.get(f"{API}/medications")
        nut_res = requests.get(f"{API}/nutrition")
        sym_res = requests.get(f"{API}/symptoms")

        fitness_count = len(fit_res.json()) if fit_res.status_code == 200 else 0
        medication_count = len(med_res.json()) if med_res.status_code == 200 else 0
        nutrition_count = len(nut_res.json()) if nut_res.status_code == 200 else 0
        symptom_count = len(sym_res.json()) if sym_res.status_code == 200 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Fitness Records", fitness_count)
        col2.metric("Medications", medication_count)
        col3.metric("Nutrition Records", nutrition_count)
        col4.metric("Symptoms", symptom_count)

        if fit_res.status_code == 200:
            fit_data = fit_res.json()
            if fit_data:
                df = pd.DataFrame(fit_data)

                if "steps" in df.columns:
                    st.subheader("Steps Overview")
                    fig, ax = plt.subplots()
                    ax.plot(df["steps"])
                    ax.set_title("Steps Trend")
                    ax.set_xlabel("Record Index")
                    ax.set_ylabel("Steps")
                    st.pyplot(fig)

                if "calories" in df.columns:
                    st.subheader("Calories Overview")
                    fig2, ax2 = plt.subplots()
                    ax2.plot(df["calories"])
                    ax2.set_title("Calories Trend")
                    ax2.set_xlabel("Record Index")
                    ax2.set_ylabel("Calories")
                    st.pyplot(fig2)
            else:
                st.info("No fitness data available for dashboard")
        else:
            st.error("Unable to fetch dashboard data")

    except Exception as e:
        st.error(f"Dashboard error: {e}")