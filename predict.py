import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('EarnEstimator.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
le_age = data["le_age"]
le_dev = data["le_dev"]
le_ind = data["le_ind"]

def show_predict_page():
    st.title("EarnEstimator")

    st.write("""### We need some information to predict the salary""")

    country = (
        "United States of America",
        "Canada" 
    )

    age = (
        '35-44 years old', '25-34 years old', '55-64 years old',
       '18-24 years old', '45-54 years old', '65 years or older',
       'Under 18 years old', 'Prefer not to say'
    )
    
    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )
    
    devtype = (
        'Full-Stack/Backend/Frontend Dev',
        'Data Specialist(AI/ML/DBMS)',
        'Managers/Team leads',
        'Other professionals',
    )
    
    industry = (
        'IT industry professional',
        'Financial professional',
        'Different Type of Sector Professional',
        'Other',
        
    )

    country = st.selectbox("Country", country)
    education = st.selectbox("Education Level", education)
    devtype = st.selectbox("Developer Type", devtype)
    industry = st.selectbox("Industry you are working in", industry)
    age = st.selectbox("Age group", age)
    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[age, education,devtype, country, experience, industry]])
        X[:, 0] = le_age.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X[:, 2] = le_dev.transform(X[:,2])
        X[:, 3] = le_country.transform(X[:,3])
        X[:, 5] = le_ind.transform(X[:,5])

        X = X.astype(float)
        
        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")