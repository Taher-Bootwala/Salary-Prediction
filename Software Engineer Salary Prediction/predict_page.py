import streamlit as st
import pandas as pd
import pickle

# Load CSV file
@st.cache
def load_salary_data():
    df = pd.read_csv("survey_results_public_new.csv")
    
    # Debugging: Print column names
    st.write("Columns in the dataset:", df.columns)
    return df

# Function to load the model and encoders
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

# Load data
data = load_model()
df = load_salary_data()

regressor = data["model"]
le_education = data["Degree"]
le_languages = data["Languages"] 

def show_predict_page():
    st.title("Software Developer Salary Prediction (India)")

    st.write("### Provide your details to estimate the salary")

    # Fixed list of education levels
    education = (
    "Less than a Bachelors",
    "Bachelors",
    "Masters",
    "Post grad"
)


    # Sample programming languages
    languages = [
        "JavaScript", "Python", "Java", "C++", "PHP", "Ruby", "Swift"
    ]

    # User inputs
    education_level = st.selectbox("Degree Level", education)
    selected_languages = st.multiselect("Programming Languages Known", languages)
    experience = st.slider("Years of Experience", 0, 50, 3)

    # Predict button
    ok = st.button("Calculate Salary")
    if ok:
        if not selected_languages:
            st.error("Please select at least one programming language.")
            return

        # Filter data based on user input
        filtered_df = df[
            (df['Degree'] == education_level) &
            (df['Experience_Years'] == experience)
        ]

        # Display predicted salary
        language_encoded = le_languages.transform([selected_languages[0]])[0] if selected_languages else 0
        education_encoded = le_education.transform([education_level])[0]
        X = pd.DataFrame([[education_encoded, experience, language_encoded]], 
                         columns=["Degree", "Experience_Years", "Languages"])
        predicted_salary = regressor.predict(X)[0]
        st.subheader(f"The estimated salary is ₹{predicted_salary:.2f} INR")

# Uncomment this to run the app locally
if __name__ == "__main__":
    show_predict_page()
