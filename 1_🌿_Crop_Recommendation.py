from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import streamlit as st
import os
import requests
 
# --- PAGE CONFIGURATION (must be the FIRST Streamlit command) ---
st.set_page_config(
    page_title="Crop Recommendation",
    page_icon="🌿",
    layout="wide"
)
 
# --- SECURITY CHECK ---
# Ensure user is authenticated before showing the page
if not st.session_state.get("authenticated", False):
    st.error("🔒 Please log in to access this page.")
    st.stop()
 
st.title("🌿 Crop Recommendation (Weather & Season)")
 
# --- API & MODEL INITIALIZATION ---
try:
    groq_api_key = "YOUR API KEYS"
    openweathermap_api_key = "YOUR API KEY"
 
    # Initialize the Groq Chat model
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile"  # ✅ Updated: llama3-8b-8192 was decommissioned
    )
except KeyError as e:
    st.error(f"API key not found: {e}. Please set it in your Streamlit secrets.")
    st.stop()
 
# --- HELPER FUNCTIONS ---
def get_weather_data(location, api_key):
    """Fetches current weather data from OpenWeatherMap API."""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    params = {"q": location, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"cod": "404", "message": f"Error fetching weather data: {str(e)}"}
 
def get_crop_recommendation_chain():
    """Creates a LangChain chain for crop recommendation."""
    prompt = ChatPromptTemplate.from_messages([
        ("system",
          """You are an expert agronomist. Your task is to recommend suitable crops based on location, season, and real-time weather data.
          Provide a detailed recommendation including:
          1.  A list of 3-5 suitable crops, ranked by suitability.
          2.  For each crop, provide a brief reason why it's suitable for the given conditions.
          3.  Provide actionable planting tips (e.g., soil preparation, sowing depth, initial watering).
          4.  Mention any potential challenges or risks for the top recommended crop in that climate.
          Format your response clearly using markdown for readability."""),
        ("human",
          """Please provide crop recommendations for the following conditions:
          - Location: {location}
          - Month/Season: {season}
          - Weather Data: {weather}""")
    ])
    return prompt | llm | StrOutputParser()
 
# --- SESSION STATE INITIALIZATION ---
if "crop_rec_history" not in st.session_state:
    st.session_state.crop_rec_history = []
 
# --- UI LAYOUT ---
st.markdown("Enter your location and the current month/season to get AI-powered crop recommendations.")
 
with st.form("recommendation_form"):
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Enter your Location (e.g., 'Vijayawada, India')", "Vijayawada, India")
    with col2:
        season = st.selectbox(
            "Select Month/Season",
            ("January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December")
        )
 
    submit_button = st.form_submit_button("Get Recommendation")
 
# --- FORM SUBMISSION LOGIC ---
if submit_button and location and season:
    with st.spinner(f"Fetching weather for {location} and generating recommendations..."):
        weather_data = get_weather_data(location, openweathermap_api_key)
 
        if weather_data.get("cod") == 200:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
 
            weather_summary = f"Temperature: {temp}°C, Humidity: {humidity}%, Conditions: {description.title()}"
            st.info(f"**Current Weather in {location}:** {weather_summary}")
 
            chain = get_crop_recommendation_chain()
            try:
                ai_response = chain.invoke({
                    "location": location,
                    "season": season,
                    "weather": weather_summary
                })
 
                st.subheader("🧠 AI Recommendation")
                st.markdown(ai_response)
 
                st.session_state.crop_rec_history.append({
                    "query": f"Location: {location}, Season: {season}, Weather: {weather_summary}",
                    "response": ai_response
                })
 
            except Exception as e:
                st.error(f"An error occurred while communicating with the AI model: {e}")
        else:
            st.error(f"Could not fetch weather data. Please check the location or API key. Error: {weather_data.get('message', 'Unknown error')}")
 
# --- DISPLAY SESSION HISTORY ---
if st.session_state.crop_rec_history:
    st.write("---")
    st.subheader("📜 Session History")
    for i, entry in enumerate(reversed(st.session_state.crop_rec_history)):
        with st.expander(f"Recommendation #{len(st.session_state.crop_rec_history) - i}: {entry['query'][:50]}..."):
            st.info(f"**Query:** {entry['query']}")
            st.markdown(entry['response'])
