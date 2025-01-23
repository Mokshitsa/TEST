import streamlit as st
import requests

# Backend URL
BASE_URL = "http://127.0.0.1:5000"  # Replace with your hosted backend URL

st.title("SurgiSim XR Prototype")

# Upload Section
st.header("Upload Patient Imaging")
uploaded_file = st.file_uploader("Upload CT/MRI Image", type=["png", "jpg", "jpeg", "dcm"])

if uploaded_file:
    if st.button("Upload"):
        files = {'file': uploaded_file.getvalue()}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        if response.status_code == 200:
            file_id = response.json().get('file_id')
            st.success(f"File uploaded successfully! File ID: {file_id}")
        else:
            st.error(f"Error: {response.json().get('error')}")

# Check Status Section
st.header("Check Model Status")
file_id = st.text_input("Enter File ID to Check Status")

if file_id and st.button("Check Status"):
    response = requests.get(f"{BASE_URL}/model_status/{file_id}")
    if response.status_code == 200:
        status = response.json().get('status')
        st.info(f"Status: {status}")
    else:
        st.error(f"Error: {response.json().get('error')}")

# AI Feedback Section
st.header("Get AI Feedback")
surgical_steps = st.text_area("Enter Surgical Steps (One per Line)", height=200)

if st.button("Get Feedback"):
    steps = surgical_steps.splitlines()
    response = requests.post(f"{BASE_URL}/ai_feedback", json={'surgical_steps': steps})
    if response.status_code == 200:
        feedback = response.json().get('feedback')
        for i, fb in enumerate(feedback):
            st.write(f"Step {i+1}: {fb}")
    else:
        st.error(f"Error: {response.json().get('error')}")
