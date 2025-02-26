import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

# Unit Categories 
unit_categories = {
    "Area": ["square meters", "square kilometers", "square miles", "square feet", "hectares", "acres"],
    "Data Transfer Rate": ["bits per second", "kilobits per second", "megabits per second", "gigabits per second"],
    "Digital Storage": ["bytes", "kilobytes", "megabytes", "gigabytes", "terabytes"],
    "Energy": ["joules", "kilojoules", "calories", "kilocalories", "watt-hours", "kilowatt-hours"],
    "Frequency": ["hertz", "kilohertz", "megahertz", "gigahertz"],
    "Fuel Economy": ["miles per gallon", "kilometers per liter", "liters per 100 km"],
    "Length": ["meters", "kilometers", "miles", "feet", "centimeters", "inches"],
    "Mass": ["grams", "kilograms", "pounds", "ounces"],
    "Plane Angle": ["degrees", "radians", "gradians"],
    "Pressure": ["pascals", "kilopascals", "bars", "atmospheres", "pounds per square inch"],
    "Speed": ["meters per second", "kilometers per hour", "miles per hour", "knots"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Time": ["seconds", "minutes", "hours", "days", "weeks", "years"],
    "Volume": ["liters", "milliliters", "cubic meters", "cubic feet", "gallons"],
}

# Custom Styling
st.markdown("""
     <style>
        /* Dark Gradient Background */
        .stApp {
            background: linear-gradient(135deg, #000000, #4B0082);
            font-family: 'Arial', sans-serif;
            color: white;
        }
        /* Title and Subtitle Styling */
        h1 {
            text-align: center;
            color: #ffffff;
        }
        p {
            text-align: center;
            color: #d3d3d3;
        }
        /* Input Fields Styling */
        .stNumberInput, .stSelectbox {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 15px;
            border-radius: 10px;
            # border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stNumberInput input, .stSelectbox select {
            color: black !important;
        }
        /* Button Styling */
        .stButton button {
            background-color: #8A2BE2 !important;
            color: white !important;
            border-radius: 5px !important;
            padding: 10px 20px !important;
            font-size: 16px;
            transition: background-color 0.3s ease;
            border: none;
        }
            
        .stSidebar {
            background-color: rgba(255, 255, 255, 0.1);}
        .stButton button:hover {
            background-color: #7B1FA2 !important;
        }
        /* Result Box Styling */
        .result-box {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            text-align: center;
            color: white;
        }
        /* Footer Styling */
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #d3d3d3;
        }
        /* Spinner Styling */
        .stSpinner > div {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for history
if "conversion_history" not in st.session_state:
    st.session_state.conversion_history = []

# Main title
st.markdown("<h1>🔄 Unit Converter App</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 16px; margin-bottom: 20px;'>Convert between different units easily using AI!</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    category = st.selectbox("Select Category:", list(unit_categories.keys()), index=0)
    available_units = unit_categories[category]

    value = st.number_input("Enter Value:", min_value=0.0, format="%.2f")
    from_unit = st.selectbox("From Unit:", available_units)
    to_unit = st.selectbox("To Unit:", available_units)

# Real-Time Conversion 
result_text = None  # Initialize result_text
if value and from_unit and to_unit:
    if from_unit == to_unit:
        st.warning("Please select different units!")
    else:
        query = f"Convert {value} {from_unit} to {to_unit}"
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

        with st.spinner("🔄 AI is thinking..."):
            response = model.generate_content(query)

        # Result
        result_text = response.text
        st.markdown("<h3>Conversion Result:</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-box'>{result_text}</div>", unsafe_allow_html=True)

        # Save to history
        if result_text:
            history_entry = f"{value} {from_unit} ➡ {result_text}"
            if history_entry not in st.session_state.conversion_history:
                st.session_state.conversion_history.insert(0, history_entry)

# Sidebar Conversion History
with st.sidebar:
    st.subheader("📜 Conversion History")
    
    if st.session_state.conversion_history:
        for history in st.session_state.conversion_history[:10]:  # Show last 10
            st.write(f"🔹 {history}")
    else:
        st.write("No history yet!")
# Footer
st.markdown("<div class='footer'>Made with ❤️ by Alishba Naveed</div>", unsafe_allow_html=True)