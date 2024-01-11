# app.py
import streamlit as st
import requests
from database import fetch_distinct_values, fetch_distinct_brand_models
import config

st.title("Cars Price Prediction App")

# Form to collect input features
usage = st.number_input("Usage", min_value=0, max_value=1000000, step=1)
third_party_insurance_deadline = st.number_input("Third Party Insurance Deadline", min_value=0, max_value=12, step=1)
production_year = st.number_input("Production Year", min_value=1380, max_value=1402, value=1402, step=1)

# Load possible values 
motor_statuses = fetch_distinct_values("motor_status")
colors = fetch_distinct_values("color")
body_statuses = fetch_distinct_values("body_status")
chassis_statuses = fetch_distinct_values("chassis_status")
fuel_types = fetch_distinct_values("fuel_type")

motor_status = st.selectbox("Motor Status", motor_statuses)
color = st.selectbox("Color", colors)
body_status = st.selectbox("Body Status", body_statuses)
chassis_status = st.selectbox("Chassis Status", chassis_statuses)
fuel_type = st.selectbox("Fuel Type", fuel_types)

brand_model_level1_options = fetch_distinct_brand_models()
brand_model_level1 = st.selectbox("Brand Model Level 1", brand_model_level1_options)

if brand_model_level1:
    brand_model_level2_options = fetch_distinct_brand_models(brand_model_level1=brand_model_level1)
    brand_model_level2_options = [item for item in brand_model_level2_options if item != '']
    brand_model_level2 = st.selectbox("Brand Model Level 2", brand_model_level2_options) if len(brand_model_level2_options) > 0 else None

    if brand_model_level2:
        brand_model_level3_options = fetch_distinct_brand_models(brand_model_level2=brand_model_level2, 
                                                                 brand_model_level1=brand_model_level1)
        brand_model_level3_options = [item for item in brand_model_level3_options if item != '']
        brand_model_level3 = st.selectbox("Brand Model Level 3", brand_model_level3_options) if len(brand_model_level3_options) > 0 else None

submit_button = st.button("Submit")

# Function to make API request
@st.cache_data
def make_prediction(data_point):
    response = requests.get(url=config.URL, json=data_point).json()
    return response

# Handle form submission
if submit_button:
    user_data_point = {
        "usage": usage,
        "third_party_insurance_deadline": int(third_party_insurance_deadline),
        "production_year": production_year,
        "motor_status": motor_status,
        "color": color,
        "body_status": body_status,
        "chassis_status": chassis_status,
        "fuel_type": fuel_type,
        "brand_model_level1": brand_model_level1,
        "brand_model_level2": brand_model_level2,
        "brand_model_level3": brand_model_level3
    }

    
    result = make_prediction(user_data_point)
    
    # Display the predicted price in a better format
    formatted_price = "{:,.0f} Toomans".format(result["predicted_price"])
    dl_formatted_price = "{:,.0f} Toomans".format(result["dl_predicted_price"])

    # Display result in a card
    st.markdown("## Prediction Result")
    st.success(f"Predicted Price: {formatted_price}")
    st.success(f"Deep Learning Predicted Price: {dl_formatted_price}")
