import streamlit as st
import pickle
import base64

# Set Page Configuration
st.set_page_config(page_title="Disease Prediction", page_icon="🩺", layout="wide")

# Hiding Streamlit UI Elements
hide_st_style = """
    <style>
    /* Remove Streamlit menu, footer, and header */
    #MainMenu {display: none !important;}
    footer {display: none !important;}
    header {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Function to Encode Background Image
def get_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Apply Background Image
background_image = "back.jpg"
base64_image = get_base64(background_image)

st.markdown(
    f"""
    <style>
    /* Background Styling */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                    url("data:image/png;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        transition: margin-left 0.3s ease-in-out;
    }}

    # /* Dark overlay for better readability */
    # [data-testid="stAppViewContainer"]::before {{
    #     content: "";
    #     position: fixed;
    #     top: 0;
    #     left: 0;
    #     width: 100%;
    #     height: 100%;
    #     background: rgba(0, 0, 0, 0.3);
    #     z-index: -1;
    #     padding-top: 0;
    # }}

    # /* Adjust when sidebar is expanded */
    # [data-testid="stSidebar"] + [data-testid="stAppViewContainer"] {{
    #     background-position: left 250px center;
    # }}

    # /* When sidebar is collapsed */
    # [data-testid="collapsedControl"] + [data-testid="stAppViewContainer"] {{
    #     background-position: left 0px center;
    # }}

    html, body, [data-testid="stAppViewContainer"] * {{
        font-family: 'Arial', sans-serif;
        color: white;
    }}

    /* Input field styling */
    [data-baseweb="input"] {{
        padding: 10px !important;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.3);
        color: black;
        font-weight: bold;
    }}

    /* Improve Button Styling */
    .stButton>button {{
        background-color: #008CBA;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        transition: 0.3s;
    }}

    .stButton>button:hover {{
        background-color: #005F73;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
    }}

    /* Selectbox Styling */
    .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        border: 2px solid #008CBA !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 8px !important;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2) !important;
    }}

    /* Dropdown Menu */
    .stSelectbox div[role="listbox"] {{
        border-radius: 8px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    }}

    .stSelectbox div[role="listbox"] div[role="option"]:hover {{
        background-color: #e0f7ff;
    }}

    /* Heading and Text Styling */
    h1 {{
        font-size: 36px !important;
        color: #FF5733 !important;
    }}

    h2 {{
        font-size: 28px !important;
    }}

    h3 {{
        font-size: 24px !important;
    }}

    p {{
        font-size: 20px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# Load Disease Prediction Models
models = {
    'diabetes': pickle.load(open('models/diabetes.pkl', 'rb')),
    'heart_disease': pickle.load(open('models/heart.pkl', 'rb')),
    'parkinsons': pickle.load(open('models/parkinsons_model.pkl', 'rb')),
    'lung_cancer': pickle.load(open('models/lungs_disease.pkl', 'rb')),
    'thyroid': pickle.load(open('models/Thyroid_model.pkl', 'rb')),
    'kidney': pickle.load(open('models/kidney.pkl','rb')),
    'liver': pickle.load(open('models/liver.pkl','rb')),
    'breast_cancer': pickle.load(open('models/breast_cancer.pkl','rb'))
}

# Sidebar Navigation
with st.sidebar:
    st.image("icon.png", width=100)
    st.markdown("## 🔍 Select a Disease to Predict:")
    selected = st.selectbox("", [
        "Diabetes Prediction",
        "Heart Disease Prediction",
        "Parkinsons Prediction",
        "Lung Cancer Prediction",
        "Hypo-Thyroid Prediction",
        "Kidney Disease Prediction",
        "Liver Disease Prediction",
        "Breast Cancer Prediction"
    ])


# Function for Input Fields
def display_input(label, tooltip, key, input_type="text", min_value=None, max_value=None, step=1, value=None):
    """Creates a Streamlit input field with proper handling for text and number inputs."""
    if input_type == "text":
        return st.text_input(label, value=value or "", key=key, help=tooltip)
    elif input_type == "number":
        return st.number_input(label, value=value if value is not None else min_value, key=key, 
                               help=tooltip, min_value=min_value, max_value=max_value, step=step, format="%f" if isinstance(step, float) else "%d")
    else:
        raise ValueError("Invalid input_type. Use 'text' or 'number'.")



# # Display Prediction Form Based on Selection
st.markdown("<br>", unsafe_allow_html=True)

# Diabetes Prediction
if selected == "Diabetes Prediction":
    st.markdown("# **Diabetes Prediction**")
    st.write("### Enter the following details to check for diabetes:")

    col1, col2 = st.columns(2)

    with col1:
        Pregnancies = display_input("Number of Pregnancies", "Enter number of times pregnant", "Pregnancies", input_type="number", min_value=0, max_value=20, step=1, value=1)
        Glucose = display_input("Glucose Level", "Enter glucose level", "Glucose", input_type="number", min_value=50, max_value=300, step=1, value=100)
        BloodPressure = display_input("Blood Pressure value", "Enter blood pressure value", "BloodPressure", input_type="number", min_value=50, max_value=200, step=1, value=80)
        SkinThickness = display_input("Skin Thickness value", "Enter skin thickness value", "SkinThickness", input_type="number", min_value=0, max_value=99, step=1, value=20)

    with col2:
        Insulin = display_input("Insulin Level", "Enter insulin level", "Insulin", input_type="number", min_value=0, max_value=900, step=1, value=30)
        BMI = display_input("BMI value", "Enter Body Mass Index value", "BMI", input_type="number", min_value=10.0, max_value=60.0, step=0.1, value=25.0)
        DiabetesPedigreeFunction = display_input("Diabetes Pedigree Function", "Enter diabetes pedigree function value", "DiabetesPedigreeFunction", input_type="number", min_value=0.0, max_value=2.5, step=0.01, value=0.5)
        Age = display_input("Age", "Enter age of the person", "Age", input_type="number", min_value=10, max_value=100, step=1, value=30)

    if st.button("🔎 **Get Diabetes Test Result**"):
        diab_prediction = models["diabetes"].predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        st.success("🛑 The person is diabetic" if diab_prediction[0] == 1 else "✅ The person is not diabetic")


# Heart Disease Prediction
if selected == "Heart Disease Prediction":
    st.markdown("# **Heart Disease Prediction**")
    st.write("### Enter the following details to check for heart disease:")

    col1, col2 = st.columns(2)

    with col1:
        age = display_input("Age", "Enter age of the person", "age", input_type="number", min_value=18, max_value=100, step=1, value=25)
        sex = display_input("Sex (1 = Male; 0 = Female)", "Enter sex of the person", "sex", input_type="number", min_value=0, max_value=1, step=1, value=1)
        cp = display_input("Chest Pain Type (0-3)", "Enter chest pain type", "cp", input_type="number", min_value=0, max_value=3, step=1, value=1)
        oldpeak = display_input("ST Depression Induced by Exercise", "Enter oldpeak value", "oldpeak", input_type="number", min_value=0.0, max_value=6.2, step=0.1, value=1.0)
        ca = display_input("Number of Major Vessels (0-3)", "Enter the number of major vessels", "ca", input_type="number", min_value=0, max_value=3, step=1, value=0)

    with col2:
        thal = display_input("Thalassemia (0-3)", "Enter thalassemia value", "thal", input_type="number", min_value=0, max_value=3, step=1, value=2)
        thalach = display_input("Max Heart Rate Achieved", "Enter maximum heart rate", "thalach", input_type="number", min_value=60, max_value=220, step=1, value=150)
        chol = display_input("Serum Cholesterol", "Enter serum cholesterol in mg/dl", "chol", input_type="number", min_value=100, max_value=600, step=1, value=200)
        trestbps = display_input("Resting Blood Pressure", "Enter resting blood pressure", "trestbps", input_type="number", min_value=80, max_value=200, step=1, value=120)
        restecg = display_input('Resting Electrocardiographic results (0, 1, 2)', 'Enter resting ECG results', 'restecg', 'number',0,2,1,1)

    if st.button("🔎 **Get Heart Disease Test Result**"):
        heart_prediction = models["heart_disease"].predict([[cp, thal, oldpeak, ca, thalach, age, chol, trestbps]])
        st.success("🛑 The person has heart disease" if heart_prediction[0] == 1 else "✅ The person does not have heart disease")
    

# Lung Cancer Prediction
if selected == "Lung Cancer Prediction":
    st.markdown("# **Lung Cancer Prediction**")
    st.write("### Enter the following details to predict lung cancer:")

    col1, col2 = st.columns(2)

    with col1:
        #GENDER = display_input("Gender (1 = Male; 0 = Female)", "Enter gender of the person", "GENDER", input_type="number", min_value=0, max_value=1, step=1, value=1)
        AGE = display_input("Age", "Enter age of the person", "AGE", input_type="number", min_value=10, max_value=100, step=1, value=50)
        SMOKING = display_input("Smoking (1 = Yes; 0 = No)", "Enter if the person smokes", "SMOKING", input_type="number", min_value=0, max_value=1, step=1, value=0)
        #YELLOW_FINGERS = display_input("Yellow Fingers (1 = Yes; 0 = No)", "Enter if the person has yellow fingers", "YELLOW_FINGERS", input_type="number", min_value=0, max_value=1, step=1, value=0)
        ANXIETY = display_input("Anxiety (1 = Yes; 0 = No)", "Enter if the person has anxiety", "ANXIETY", input_type="number", min_value=0, max_value=1, step=1, value=0)
        PEER_PRESSURE = display_input("Peer Pressure (1 = Yes; 0 = No)", "Enter if the person is under peer pressure", "PEER_PRESSURE", input_type="number", min_value=0, max_value=1, step=1, value=0)
        CHRONIC_DISEASE = display_input("Chronic Disease (1 = Yes; 0 = No)", "Enter if the person has a chronic disease", "CHRONIC_DISEASE", input_type="number", min_value=0, max_value=1, step=1, value=0)
        FATIGUE = display_input("Fatigue (1 = Yes; 0 = No)", "Enter if the person experiences fatigue", "FATIGUE", input_type="number", min_value=0, max_value=1, step=1, value=0)

    with col2:
        ALLERGY = display_input("Allergy (1 = Yes; 0 = No)", "Enter if the person has allergies", "ALLERGY", input_type="number", min_value=0, max_value=1, step=1, value=0)
        WHEEZING = display_input("Wheezing (1 = Yes; 0 = No)", "Enter if the person experiences wheezing", "WHEEZING", input_type="number", min_value=0, max_value=1, step=1, value=0)
        ALCOHOL_CONSUMING = display_input("Alcohol Consuming (1 = Yes; 0 = No)", "Enter if the person consumes alcohol", "ALCOHOL_CONSUMING", input_type="number", min_value=0, max_value=1, step=1, value=0)
        COUGHING = display_input("Coughing (1 = Yes; 0 = No)", "Enter if the person experiences coughing", "COUGHING", input_type="number", min_value=0, max_value=1, step=1, value=0)
        #SHORTNESS_OF_BREATH = display_input("Shortness Of Breath (1 = Yes; 0 = No)", "Enter if the person has breathing issues", "SHORTNESS_OF_BREATH", input_type="number", min_value=0, max_value=1, step=1, value=0)
        SWALLOWING_DIFFICULTY = display_input("Swallowing Difficulty (1 = Yes; 0 = No)", "Enter if the person has difficulty swallowing", "SWALLOWING_DIFFICULTY", input_type="number", min_value=0, max_value=1, step=1, value=0)
        CHEST_PAIN = display_input("Chest Pain (1 = Yes; 0 = No)", "Enter if the person experiences chest pain", "CHEST_PAIN", input_type="number", min_value=0, max_value=1, step=1, value=0)

    if st.button("🔎 **Get Lung Cancer Test Result**"):
        lungs_prediction = models["lung_cancer"].predict([[AGE, SMOKING+1, ANXIETY+1, PEER_PRESSURE+1, CHRONIC_DISEASE+1, FATIGUE+1, ALLERGY+1, WHEEZING+1, ALCOHOL_CONSUMING+1, COUGHING+1, SWALLOWING_DIFFICULTY+1, CHEST_PAIN+1]])
        if lungs_prediction[0] == 1:
            st.error("🛑 **The person has lung cancer disease**")
        else:
            st.success("✅ **The person does not have lung cancer disease**")


# Hypo-Thyroid Prediction
if selected == "Hypo-Thyroid Prediction":
    st.markdown("# **Hypo-Thyroid Prediction**")
    st.write("### Enter the following details to predict hypo-thyroid disease:")

    col1, col2 = st.columns(2)

    with col1:
        age = display_input("Age", "Enter age of the person", "age", input_type="number", min_value=10, max_value=100, step=1, value=30)
        sex = display_input("Sex (1 = Male; 0 = Female)", "Enter sex of the person", "sex", input_type="number", min_value=0, max_value=1, step=1, value=1)
        on_thyroxine = display_input("On Thyroxine (1 = Yes; 0 = No)", "Enter if the person is on thyroxine", "on_thyroxine", input_type="number", min_value=0, max_value=1, step=1, value=0)
        tsh = display_input("TSH Level", "Enter TSH level", "tsh", input_type="number", min_value=0.1, max_value=10.0, step=0.1, value=1.5)

    with col2:
        t3_measured = display_input("T3 Measured (1 = Yes; 0 = No)", "Enter if T3 was measured", "t3_measured", input_type="number", min_value=0, max_value=1, step=1, value=1)
        t3 = display_input("T3 Level", "Enter T3 level", "t3", input_type="number", min_value=0.1, max_value=5.0, step=0.1, value=2.0)
        tt4 = display_input("TT4 Level", "Enter TT4 level", "tt4", input_type="number", min_value=1.0, max_value=20.0, step=0.1, value=8.0)

    if st.button("🔎 **Get Thyroid Test Result**"):
        thyroid_prediction = models["thyroid"].predict([[age, sex, on_thyroxine, tsh, t3_measured, t3, tt4]])
        if thyroid_prediction[0] == 1:
            st.error("🛑 **The person has Hypo-Thyroid disease**")
        else:
            st.success("✅ **The person does not have Hypo-Thyroid disease**")

# Parkinson's Prediction
if selected == "Parkinsons Prediction":
    st.markdown("# **Parkinson's Disease Prediction**")
    st.write("### Enter the following details to check for Parkinson's disease:")

    col1, col2 = st.columns(2)

    with col1:
        fo = display_input("MDVP:Fo(Hz)", "Enter MDVP:Fo(Hz) value", "fo", input_type="number", min_value=50, max_value=300, step=1, value=150)
        fhi = display_input("MDVP:Fhi(Hz)", "Enter MDVP:Fhi(Hz) value", "fhi", input_type="number", min_value=50, max_value=400, step=1, value=200)
        flo = display_input("MDVP:Flo(Hz)", "Enter MDVP:Flo(Hz) value", "flo", input_type="number", min_value=50, max_value=300, step=1, value=100)
        Jitter_percent = display_input("MDVP:Jitter(%)", "Enter MDVP:Jitter(%) value", "Jitter_percent", input_type="number", min_value=0.0, max_value=1.0, step=0.01, value=0.01)
        Jitter_Abs = display_input("MDVP:Jitter(Abs)", "Enter MDVP:Jitter(Abs) value", "Jitter_Abs", input_type="number", min_value=0.00001, max_value=0.1, step=0.00001, value=0.0005)
        # RAP = display_input("MDVP:RAP", "Enter MDVP:RAP value", "RAP", input_type="number", min_value=0.0, max_value=0.5, step=0.01, value=0.02)
        # PPQ = display_input("MDVP:PPQ", "Enter MDVP:PPQ value", "PPQ", input_type="number", min_value=0.0, max_value=0.5, step=0.01, value=0.02)
        # DDP = display_input("Jitter:DDP", "Enter Jitter:DDP value", "DDP", input_type="number", min_value=0.0, max_value=0.5, step=0.01, value=0.02)
        Shimmer = display_input("MDVP:Shimmer", "Enter MDVP:Shimmer value", "Shimmer", input_type="number", min_value=0.0, max_value=1.0, step=0.01, value=0.02)
        # Shimmer_dB = display_input("MDVP:Shimmer(dB)", "Enter MDVP:Shimmer(dB) value", "Shimmer_dB", input_type="number", min_value=0.0, max_value=5.0, step=0.1, value=1.0)
        # APQ3 = display_input("Shimmer:APQ3", "Enter Shimmer:APQ3 value", "APQ3", input_type="number", min_value=0.0, max_value=0.5, step=0.01, value=0.02)

    with col2:
        # APQ5 = display_input("Shimmer:APQ5", "Enter Shimmer:APQ5 value", "APQ5", input_type="number", min_value=0.0, max_value=0.5, step=0.01, value=0.02)
        # APQ = display_input("MDVP:APQ", "Enter MDVP:APQ value", "APQ", input_type="number", min_value=0.0, max_value=0.5, step=0.01, value=0.02)
        # DDA = display_input("Shimmer:DDA", "Enter Shimmer:DDA value", "DDA", input_type="number", min_value=0.0, max_value=0.5, step=0.01, value=0.02)
        # NHR = display_input("NHR", "Enter NHR value", "NHR", input_type="number", min_value=0.0, max_value=1.0, step=0.01, value=0.05)
        HNR = display_input("HNR", "Enter HNR value", "HNR", input_type="number", min_value=0.0, max_value=50.0, step=1.0, value=20.0)
        RPDE = display_input("RPDE", "Enter RPDE value", "RPDE", input_type="number", min_value=0.0, max_value=1.0, step=0.01, value=0.5)
        DFA = display_input("DFA", "Enter DFA value", "DFA", input_type="number", min_value=0.0, max_value=1.0, step=0.01, value=0.7)
        spread1 = display_input("Spread1", "Enter spread1 value", "spread1", input_type="number", min_value=-10.0, max_value=0.0, step=0.1, value=-4.0)
        spread2 = display_input("Spread2", "Enter spread2 value", "spread2", input_type="number", min_value=0.0, max_value=1.0, step=0.01, value=0.2)
        D2 = display_input("D2", "Enter D2 value", "D2", input_type="number", min_value=0.0, max_value=4.0, step=0.1, value=2.0)
        # PPE = display_input("PPE", "Enter PPE value", "PPE", input_type="number", min_value=0.0, max_value=1.0, step=0.01, value=0.3)

    if st.button("🔎 **Get Parkinson's Test Result**"):
        parkinsons_prediction = models["parkinsons"].predict([[fo, fhi, flo, Jitter_percent, Shimmer, HNR, RPDE, DFA, spread1, spread2, D2]])
        if parkinsons_prediction[0] == 1:
            st.error("🛑 **The person has Parkinson's disease**")
        else:
            st.success("✅ **The person does not have Parkinson's disease**")


# Liver Disease Prediction
if selected == "Liver Disease Prediction":
    st.markdown("# **Liver Disease Prediction**")
    st.write("### Enter the following details to check for liver disease:")

    col1, col2 = st.columns(2)

    with col1:
        Age = display_input("Age", "Enter Age", "Age", input_type="number", min_value=10, max_value=100, step=1, value=30)
        Gender = display_input("Gender (1 = Male; 0 = Female)", "Enter Gender", "Gender", input_type="number", min_value=0, max_value=1, step=1, value=1)
        Total_Bilirubin = display_input("Total Bilirubin", "Enter Total Bilirubin", "Total_Bilirubin", input_type="number", min_value=0.1, max_value=50.0, step=0.1, value=1.0)
        Direct_Bilirubin = display_input("Direct Bilirubin", "Enter Direct Bilirubin", "Direct_Bilirubin", input_type="number", min_value=0.1, max_value=20.0, step=0.1, value=0.5)
        Alkaline_Phosphotase = display_input("Alkaline Phosphotase", "Enter Alkaline Phosphotase", "Alkaline_Phosphotase", input_type="number", min_value=50, max_value=1000, step=1, value=300)

    with col2:
        Alamine_Aminotransferase = display_input("Alamine Aminotransferase", "Enter Alamine Aminotransferase", "Alamine_Aminotransferase", input_type="number", min_value=10, max_value=500, step=1, value=50)
        Aspartate_Aminotransferase = display_input("Aspartate Aminotransferase", "Enter Aspartate Aminotransferase", "Aspartate_Aminotransferase", input_type="number", min_value=10, max_value=500, step=1, value=50)
        Total_Proteins = display_input("Total Proteins", "Enter Total Proteins", "Total_Proteins", input_type="number", min_value=3.0, max_value=10.0, step=0.1, value=6.5)
        Albumin = display_input("Albumin", "Enter Albumin", "Albumin", input_type="number", min_value=2.0, max_value=6.0, step=0.1, value=4.0)
        Albumin_and_Globulin_Ratio = display_input("Albumin & Globulin Ratio", "Enter Albumin & Globulin Ratio", "Albumin_and_Globulin_Ratio", input_type="number", min_value=0.1, max_value=3.0, step=0.1, value=1.2)

    if st.button("🔎 **Get Liver Disease Test Result**"):
        liver_prediction = models["liver"].predict([[Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Proteins, Albumin, Albumin_and_Globulin_Ratio]])
        if liver_prediction[0] == 1:
            st.error("🛑 **The person has liver disease**")
        else:
            st.success("✅ **The person does not have liver disease**")

# Kidney Disease Prediction
if selected == "Kidney Disease Prediction":
    st.markdown("# **Kidney Disease Prediction**")
    st.write("### Enter the following details to check for kidney disease:")

    col1, col2 = st.columns(2)

    with col1:
        age = display_input("Age", "Enter Age", "age", input_type="number", min_value=10, max_value=100, step=1, value=30)
        rbc = display_input("Red Blood Cells", "Enter RBC Count", "rbc", input_type="number", min_value=3.0, max_value=6.5, step=0.1, value=4.5)
        pc = display_input("Pus Cells", "Enter Pus Cells", "pc", input_type="number", min_value=0, max_value=1, step=1, value=0)
        bgr = display_input("Blood Glucose Random", "Enter Blood Glucose Random", "bgr", input_type="number", min_value=50, max_value=400, step=1, value=120)

    with col2:
        Gender = display_input("Gender (1 = Male; 0 = Female)", "Enter Gender", "Gender", input_type="number", min_value=0, max_value=1, step=1, value=1)
        al = display_input("Albumin", "Enter Albumin", "al", input_type="number", min_value=0, max_value=5, step=1, value=1)
        sc = display_input("Serum Creatinine", "Enter Serum Creatinine", "sc", input_type="number", min_value=0.5, max_value=15.0, step=0.1, value=1.2)
        wc = display_input("White Blood Cells", "Enter WBC Count", "wc", input_type="number", min_value=2000, max_value=15000, step=100, value=8000)

    if st.button("🔎 **Get Kidney Disease Test Result**"):
        kidney_prediction = models["kidney"].predict([[al, rbc, pc, bgr, sc,wc]])
        if kidney_prediction[0] == 1:
            st.error("🛑 **The person has kidney disease**")
        else:
            st.success("✅ **The person does not have kidney disease**")



# Breast Cancer Prediction
if selected == "Breast Cancer Prediction":
    st.markdown("# **Breast Cancer Prediction**")
    st.write("### Enter the following details to check for breast cancer:")

    col1, col2, col3 = st.columns(3)

    with col3:
        texture_mean = display_input("Texture Mean", "Enter Texture Mean", "texture_mean", input_type="number", min_value=0.0, max_value=50.0, step=0.1)
        texture_worst = display_input("Texture Worst", "Enter Texture Worst", "texture_worst", input_type="number", min_value=0.0, max_value=50.0, step=0.1)
        smoothness_worst = display_input("Smoothness Worst", "Enter Smoothness Worst", "smoothness_worst", input_type="number", min_value=0.0, max_value=1.0, step=0.01)
        perimeter_worst = display_input("Perimeter Worst", "Enter Perimeter Worst", "perimeter_worst", input_type="number", min_value=0.0, max_value=300.0, step=0.1)
        perimeter_mean = display_input("Perimeter Mean", "Enter Perimeter Mean", "perimeter_mean", input_type="number", min_value=0.0, max_value=200.0, step=0.1)
        perimeter_se = display_input("Perimeter SE", "Enter Perimeter SE", "perimeter_se", input_type="number", min_value=0.0, max_value=20.0, step=0.1)

    with col2:
        compactness_worst = display_input("Compactness Worst", "Enter Compactness Worst", "compactness_worst", input_type="number", min_value=0.0, max_value=1.0, step=0.01)
        concavity_worst = display_input("Concavity Worst", "Enter Concavity Worst", "concavity_worst", input_type="number", min_value=0.0, max_value=1.0, step=0.01)
        concave_points_worst = display_input("Concave Points Worst", "Enter Concave Points Worst", "concave_points_worst", input_type="number", min_value=0.0, max_value=1.0, step=0.01)
        concave_points_mean = display_input("Concave Points Mean", "Enter Concave Points Mean", "concave_points_mean", input_type="number", min_value=0.0, max_value=1.0, step=0.01)
        concavity_mean = display_input("Concavity Mean", "Enter Concavity Mean", "concavity_mean", input_type="number", min_value=0.0, max_value=1.0, step=0.01)
        symmetry_worst = display_input("Symmetry Worst", "Enter Symmetry Worst", "symmetry_worst", input_type="number", min_value=0.0, max_value=1.0, step=0.01)
        
    with col1:
        radius_worst = display_input("Radius Worst", "Enter Radius Worst", "radius_worst", input_type="number", min_value=0.0, max_value=50.0, step=0.1)
        radius_mean = display_input("Radius Mean", "Enter Radius Mean", "radius_mean", input_type="number", min_value=0.0, max_value=50.0, step=0.1)
        radius_se = display_input("Radius SE", "Enter Radius SE", "radius_se", input_type="number", min_value=0.0, max_value=5.0, step=0.1)
        area_mean = display_input("Area Mean", "Enter Area Mean", "area_mean", input_type="number", min_value=0.0, max_value=3000.0, step=1.0)
        area_se = display_input("Area SE", "Enter Area SE", "area_se", input_type="number", min_value=0.0, max_value=500.0, step=1.0)
        area_worst = display_input("Area Worst", "Enter Area Worst", "area_worst", input_type="number", min_value=0.0, max_value=4000.0, step=1.0)

    if st.button("🔎 **Get Breast Cancer Test Result**"):
        breast_cancer_prediction = models["breast_cancer"].predict([[
            radius_mean, texture_mean, perimeter_mean, area_mean, concavity_mean,
            concave_points_mean, radius_se, perimeter_se, area_se, radius_worst,
            texture_worst, perimeter_worst, area_worst, smoothness_worst,
            compactness_worst, concavity_worst, concave_points_worst, symmetry_worst
        ]])


        if breast_cancer_prediction[0] == 1:
            st.error("🛑 **The person has breast cancer**")
        else:
            st.success("✅ **The person does not have breast cancer**")
