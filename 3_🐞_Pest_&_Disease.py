import streamlit as st
import os
from PIL import Image
import io
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- PAGE CONFIGURATION (must be the FIRST Streamlit command) ---
st.set_page_config(
    page_title="Pest & Disease Detection",
    page_icon="🐞",
    layout="wide"
)

# --- SECURITY CHECK ---
if not st.session_state.get("authenticated", False):
    st.error("🔒 Please log in to access this page.")
    st.stop()

st.title("🐞 Pest & Disease Detection")

# --- API & MODEL INITIALIZATION ---
try:
    groq_api_key = 'YOUR_API_KEY'
    llm = ChatGroq(
        temperature=0.5,
        model_name="llama-3.3-70b-versatile",
        api_key=groq_api_key
    )
except KeyError:
    st.error("Groq API key not found. Please set it in your .env file.")
    st.stop()

# --- HELPER & AI FUNCTIONS ---
def analyze_image_with_cnn(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    return "The image appears to show a leaf with characteristics of **Powdery Mildew** (white, dusty spots)."

def get_treatment_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """You are a plant pathologist and pest control expert.
         Your task is to provide a diagnosis and a comprehensive treatment plan based on the user's input (either a text description or a preliminary image analysis).
         
         Your response should include:
         1.  **Potential Diagnosis:** State the likely pest or disease.
         2.  **Immediate Actions:** Steps the user should take right away to contain the issue.
         3.  **Organic Treatment Methods:** Recommend safe, organic, and sustainable solutions (e.g., neem oil, horticultural soaps, biological controls). Provide application instructions.
         4.  **Chemical Treatment Methods:** If necessary, recommend appropriate chemical treatments (fungicides, pesticides). Mention active ingredients and safety precautions (e.g., PPE, application timing).
         5.  **Prevention Tips:** Advise on long-term strategies to prevent recurrence (e.g., proper spacing, watering techniques, sanitation).
         
         Format the response clearly using markdown. If the input is from an image analysis, acknowledge it."""),
        ("human", "{context}")
    ])
    return prompt | llm | StrOutputParser()

# --- SESSION STATE INITIALIZATION ---
if "pest_history" not in st.session_state:
    st.session_state.pest_history = []

# --- UI LAYOUT ---
st.markdown("Identify and get treatment plans for crop pests and diseases. You can either upload an image or describe the symptoms.")

tab1, tab2 = st.tabs(["🖼️ Upload Image", "📝 Describe Symptoms"])

with tab1:
    st.subheader("Upload an Image of the Affected Plant/Leaf")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_container_width=True, width=300)

        if st.button("Analyze Image"):
            with st.spinner("Analyzing image and generating diagnosis..."):
                image_bytes = uploaded_file.getvalue()
                cnn_analysis = analyze_image_with_cnn(image_bytes)
                st.info(f"**Preliminary Image Analysis:** {cnn_analysis}")
                context = f"An image was uploaded. The initial analysis suggests: '{cnn_analysis}'. Please provide a full diagnosis and treatment plan based on this."
                chain = get_treatment_chain()
                try:
                    ai_response = chain.invoke({"context": context})
                    st.subheader("🧠 AI Diagnosis and Treatment Plan")
                    st.markdown(ai_response)
                    st.session_state.pest_history.append({"query": f"Image Analysis: {cnn_analysis}", "response": ai_response})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

with tab2:
    st.subheader("Describe the Symptoms You Are Observing")
    with st.form("description_form"):
        symptom_description = st.text_area(
            "Provide as much detail as possible (e.g., color of spots, location on plant, texture, presence of insects).",
            "I see yellow spots with a powdery, white texture on the upper side of the cucumber leaves."
        )
        submit_button = st.form_submit_button("Get Diagnosis from Description")

        if submit_button and symptom_description:
            with st.spinner("Analyzing description and generating diagnosis..."):
                context = f"A farmer has described the following symptoms: '{symptom_description}'. Please provide a full diagnosis and treatment plan."
                chain = get_treatment_chain()
                try:
                    ai_response = chain.invoke({"context": context})
                    st.subheader("🧠 AI Diagnosis and Treatment Plan")
                    st.markdown(ai_response)
                    st.session_state.pest_history.append({"query": f"Text Description: {symptom_description}", "response": ai_response})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# --- DISPLAY SESSION HISTORY ---
if st.session_state.pest_history:
    st.write("---")
    st.subheader("📜 Session History")
    for i, entry in enumerate(reversed(st.session_state.pest_history)):
        with st.expander(f"Diagnosis #{len(st.session_state.pest_history) - i}: {entry['query'][:50]}..."):
            st.info(f"**Query:** {entry['query']}")
            st.markdown(entry['response'])
