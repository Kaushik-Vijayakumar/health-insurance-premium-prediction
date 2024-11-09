import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os
import sklearn
import sys

model_path = os.path.join(os.path.dirname(__file__), "default_RandomForest_model.pkl")
# Load the model from the pickle file
with open(model_path, "rb") as file:
    model = pickle.load(file)

st.title("Health Insurance Premium Price Prediction")

st.subheader("Do you have any of the following conditions?")
col1, col2 = st.columns(2)
with col1:
    diabetes = int(st.toggle("Diabetes", value=0))
    blood_pressure_problems = int(st.toggle("Blood Pressure Problems", value=False))
    any_transplants = int(st.toggle("Any Transplants", value=False))
    any_chronic_diseases = int(st.toggle("Any Chronic Diseases", value=False))
    known_allergies = int(st.toggle("Known Allergies", value=False))
    history_of_cancer_in_family = int(st.toggle("History of Cancer in Family", value=False))
    options = [0, 1, 2, 3]
    number_of_major_surgeries = int(st.segmented_control(
        "No. of Major Surgeries", options, selection_mode="single", default=0
    ))
with col2:
    age = int(st.slider("How old are you?", 18, 66, 25))
    height = int(st.number_input(
        "How tall are you? (in cm)", value=145, min_value=145, max_value=188
    ))
    weight = int(st.number_input(
        "What's your weight? (in kg)", value=51, min_value=51, max_value=132
    ))

BMI = weight / ((height / 100) ** 2)

data = {
    "Age": [age],
    "Diabetes": [diabetes],
    "BloodPressureProblems": [blood_pressure_problems],
    "AnyTransplants": [any_transplants],
    "AnyChronicDiseases": [any_chronic_diseases],
    "Height": [height],
    "Weight": [weight],
    "KnownAllergies": [known_allergies],
    "HistoryOfCancerInFamily": [history_of_cancer_in_family],
    "NumberOfMajorSurgeries": [number_of_major_surgeries],
}

df = pd.DataFrame(data)

predicted_premium = model.predict(df)[0]

st.markdown("""
    <style>
    .bmi-card {
        background: linear-gradient(135deg, #2f3040 0%, #262730 100%);
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        color: white;
        margin: auto;
        max-width: 500px;
    }

    .bmi-title {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .bmi-value {
        font-size: 48px;
        font-weight: 700;
        margin: 0;
        text-align: right;
        background: #fd4b4a;
        padding: 10px 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"""
    <div class="bmi-card">
        <div class="bmi-title">Premium Price</div>
        <div class="bmi-value">${predicted_premium:.1f}</div>
    </div>
    """, unsafe_allow_html=True)
