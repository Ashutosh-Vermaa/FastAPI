import streamlit as st
import requests
from config import API_URL
st.set_page_config(page_title="User Details Form", page_icon="📝")

st.title("📝 User Details Form")
st.write("Please fill in the details below.")

with st.form("user_details_form"):
    age = st.number_input(
        "Age",
        min_value=2,
        max_value=89,
        step=1,
        help="Age of the person (must be between 1 and 90)"
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=0.1,
        step=0.1,
        format="%.2f",
        help="Weight of the person in kg"
    )

    height = st.number_input(
        "Height (m)",
        min_value=0.1,
        step=0.1,
        format="%.2f",
        help="Height of the person"
    )

    income_lpa = st.number_input(
        "Income (LPA)",
        min_value=0.1,
        step=0.1,
        format="%.2f",
        help="Income of the person in Lakhs Per Annum"
    )

    smoker = st.selectbox(
        "Does the person smoke?",
        options=["yes", "no"],
        help="Smoking status of the person"
    )

    city = st.text_input(
        "City",
        help="City of the person"
    )

    occupation = st.selectbox(
        "Occupation",
        options=['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],
        help="Occupation of the person"
    )

    submitted = st.form_submit_button("Submit")

if submitted:
    if not city.strip() or not occupation.strip():
        st.error("City and Occupation cannot be empty.")
    else:
        user_data = {
            "age": int(age),
            "weight": float(weight),
            "height": float(height),
            "income_lpa": float(income_lpa),
            "smoker": smoker,
            "city": city.strip(),
            "occupation": occupation.strip(),
        }

        st.success("Details submitted successfully!")
        # st.subheader("Submitted Data")
        # st.json(user_data)

        # Example: send this to an API/backend
        try:
            response = requests.post(API_URL, json=user_data)
            if response.status_code==200:
                result=response.json()
                st.success(f"Predicted insurance premium category: {result['predicted category is']}")
            else:
                st.error(f"API error: {response.status_code}- {response.text}")
        except requests.exceptions.ConnectionError:
            st.error('Could not connect to the fastAPI server. Make sure it is running')
