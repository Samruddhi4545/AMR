import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
model = joblib.load("amr_prediction_model.pkl")
st.title("Antimicrobial Resistance Prediction Dashboard")
st.write("Interactive tool to explore resistance trends and predict patient outcomes.")
st.sidebar.header("Patient Information")

age = st.sidebar.slider("Age", 0, 100, 30)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Unknown"])
specimen = st.sidebar.selectbox("Specimen Type", ["Blood", "Urine", "Sputum", "Unknown"])
test_method = st.sidebar.selectbox("Test Method", ["Disk Diffusion", "MIC", "Unknown"])
res_genes = st.sidebar.selectbox("Resistance Genes", ["NDM-1", "OXA-48", "Unknown"])
antibiotic = st.sidebar.selectbox("Antibiotic", ["Amoxicillin", "Ciprofloxacin", "Meropenem", "Vancomycin", "Colistin"])
result = st.sidebar.selectbox("Result", ["Sensitive", "Intermediate", "Resistant"])
# Simple encoding for demo (must match training pipeline)
result_map = {"Sensitive":0, "Intermediate":1, "Resistant":2}
outcome_map = {0:"ICU", 1:"Recovered", 2:"Deceased"}

input_data = pd.DataFrame({
    "Age":[age],
    "Gender":[0 if gender=="Male" else 1 if gender=="Female" else 2],
    "Specimen_Type":[0 if specimen=="Blood" else 1 if specimen=="Urine" else 2 if specimen=="Sputum" else 3],
    "Test_Method":[0 if test_method=="Disk Diffusion" else 1 if test_method=="MIC" else 2],
    "Resistance_Genes":[0 if res_genes=="NDM-1" else 1 if res_genes=="OXA-48" else 2],
    "Antibiotic":[0 if antibiotic=="Amoxicillin" else 1 if antibiotic=="Ciprofloxacin" else 2 if antibiotic=="Meropenem" else 3 if antibiotic=="Vancomycin" else 4],
    "Result":[result_map[result]]
})
if st.sidebar.button("Predict Outcome"):
    prediction = model.predict(input_data)[0]
    st.subheader("Predicted Patient Outcome")
    st.write(f"➡️ {outcome_map[prediction]}")
st.subheader("Resistance Trends (Demo Visualization)")

# Example: antibiotic resistance distribution
demo_data = pd.DataFrame({
    "Antibiotic":["Amoxicillin","Ciprofloxacin","Meropenem","Vancomycin","Colistin"],
    "Resistance":[40, 55, 20, 30, 10]
})

fig, ax = plt.subplots()
sns.barplot(x="Antibiotic", y="Resistance", data=demo_data, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)
