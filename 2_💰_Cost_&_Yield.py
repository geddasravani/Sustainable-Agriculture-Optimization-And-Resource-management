import streamlit as st

import os

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate          # ✅ Fixed import

from langchain_core.output_parsers import StrOutputParser      # ✅ Fixed import
 
# --- PAGE CONFIGURATION (must be the FIRST Streamlit command) ---

st.set_page_config(

    page_title="Cost & Yield Optimization",

    page_icon="💰",

    layout="wide"

)
 
# --- SECURITY CHECK ---

if not st.session_state.get("authenticated", False):

    st.error("🔒 Please log in to access this page.")

    st.stop()
 
st.title("💰 Cost Reduction & Yield Optimization")
 
# --- API & MODEL INITIALIZATION ---

try:

    groq_api_key = "YOUR_API_KEY"

    llm = ChatGroq(

        temperature=0.7,

        model_name="llama-3.3-70b-versatile",                 # ✅ Updated model

        api_key=groq_api_key

    )

except KeyError:

    st.error("Groq API key not found. Please set it in your .env file.")

    st.stop()
 
# --- LANGCHAIN CHAIN DEFINITION ---

def get_optimization_chain():

    """Creates a LangChain chain for optimization plans."""

    prompt = ChatPromptTemplate.from_messages([

        ("system",

         """You are an expert in agricultural economics and modern farming techniques.

         Your goal is to provide a comprehensive optimization plan for a farmer.

         Based on the user's inputs, generate a detailed report with two main sections:

         1.  **Short-Term Plan (Next 3-6 Months):**

             - Immediate, low-cost actions to reduce operational expenses.

             - Techniques to improve yield for the current or upcoming harvest.

             - Specific advice on resource management (water, fertilizer).

         2.  **Long-Term Plan (Next 1-3 Years):**

             - Strategic investments (e.g., machinery, irrigation systems).

             - Suggestions for crop rotation, soil health improvement, and sustainable practices.

             - Market diversification and risk management strategies.
 
         Provide actionable, clear, and realistic advice. Format the response using markdown."""),

        ("human",

         """Please generate an optimization plan for my farm with the following details:

         - Crop Type: {crop}

         - Farm Size: {size}

         - Available Resources: {resources}""")

    ])

    return prompt | llm | StrOutputParser()
 
# --- SESSION STATE INITIALIZATION ---

if "cost_yield_history" not in st.session_state:

    st.session_state.cost_yield_history = []
 
# --- UI LAYOUT ---

st.markdown("Provide details about your farm to receive a customized plan for reducing costs and maximizing yield.")
 
with st.form("optimization_form"):

    crop_type = st.text_input("Primary Crop Type", "Rice")

    farm_size = st.text_input("Farm Size (e.g., '10 acres', '5 hectares')", "10 acres")

    available_resources = st.text_area(

        "Describe your Available Resources",

        "Canal irrigation, one tractor, access to standard NPK fertilizers, manual labor available."

    )

    submit_button = st.form_submit_button("Get Optimization Plan")
 
# --- FORM SUBMISSION LOGIC ---

if submit_button and crop_type and farm_size and available_resources:

    with st.spinner("Generating a customized optimization plan..."):

        chain = get_optimization_chain()

        try:

            ai_response = chain.invoke({

                "crop": crop_type,

                "size": farm_size,

                "resources": available_resources

            })

            st.subheader("🧠 AI-Generated Optimization Plan")

            st.markdown(ai_response)

            st.session_state.cost_yield_history.append({

                "query": f"Crop: {crop_type}, Size: {farm_size}, Resources: {available_resources}",

                "response": ai_response

            })
 
        except Exception as e:

            st.error(f"An error occurred while communicating with the AI model: {e}")
 
# --- DISPLAY SESSION HISTORY ---

if st.session_state.cost_yield_history:

    st.write("---")

    st.subheader("📜 Session History")

    for i, entry in enumerate(reversed(st.session_state.cost_yield_history)):

        with st.expander(f"Plan #{len(st.session_state.cost_yield_history) - i}: {entry['query'][:50]}..."):

            st.info(f"**Query:** {entry['query']}")

            st.markdown(entry['response'])
