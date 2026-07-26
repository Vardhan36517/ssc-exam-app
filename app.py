import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(
    page_title="ExamSaathi - Your Personal Mentor",
    page_icon="🎓",
    layout="centered"
)

# Custom Styling (CSS)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    .main-header h1 {
        color: white !important;
        margin: 0;
        font-weight: 700;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Get API Key
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "").strip()

# Custom Header
st.markdown("""
<div class="main-header">
    <h1>🎓 ExamSaathi</h1>
    <p style="margin-top: 5px; opacity: 0.9;">Your Personal SSC & Govt Exam Mentor (Bilingual English + Telugu)</p>
</div>
""", unsafe_allow_html=True)

if not GEMINI_API_KEY:
    st.error("⚠️ GEMINI_API_KEY Secrets mein missing hai! Streamlit Settings -> Secrets mein key check karein.")
    st.stop()

# Configure GenAI
genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
You are 'ExamSaathi', an expert AI mentor and tutor created specifically to help the user prepare for Indian Competitive Exams (SSC CGL, CHSL, Banking, Railway, APPSC/TSPSC).

Key Rules:
1. Language: Explain every concept using a simple, clear combination of English and Telugu script (Bilingual). Technical terms should be in English with clear Telugu explanations.
2. Subject Knowledge: You are an expert across Quantitative Aptitude, Logical Reasoning, General Awareness (GK/Current Affairs), and English Language.
3. Structure: Use bold headers, examples, step-by-step logic, and clean bullet points for easy reading.
"""

def generate_response(prompt_text):
    # Valid model names for google-generativeai SDK
    models_to_try = [
        'gemini-1.5-flash-latest', 
        'gemini-1.5-pro-latest', 
        'gemini-pro'
    ]
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=SYSTEM_INSTRUCTION
            )
            response = model.generate_content(prompt_text)
            return response.text
        except Exception:
            continue
            
    st.error("Unable to generate response. Please check API Key status in Google AI Studio.")
    return None

tab_learn, tab_practice = st.tabs(["📖 Learning & Guidance", "📝 Practice & Mock Test"])

with tab_learn:
    st.subheader("💡 Ask Anything or Get Strategy")
    learn_option = st.radio(
        "Select Mode:",
        ["Ask a Doubt / Learn Concept", "Daily Study Routine"],
        horizontal=True
    )

    if learn_option == "Ask a Doubt / Learn Concept":
        user_query = st.text_area(
            "What topic do you want to learn today?",
            placeholder="e.g., Explain Profit and Loss shortcuts or Static GK..."
        )
        if st.button("🚀 Explain Step-by-Step"):
            if user_query:
                with st.spinner("Preparing detailed guidance in English + Telugu..."):
                    res = generate_response(f"Explain clearly from basics to advanced: {user_query}")
                    if res:
                        st.success("Here is your explanation:")
                        st.markdown(res)
            else:
                st.warning("Please type a topic or question first!")

    elif learn_option == "Daily Study Routine":
        exam_name = st.text_input("Target Exam", "SSC CGL")
        study_hours = st.slider("Daily Available Study Hours", 2, 12, 6)
        if st.button("🎯 Generate Time Table"):
            with st.spinner("Designing schedule..."):
                res = generate_response(f"Create a practical daily study time table for {exam_name} with {study_hours} study hours per day. Explain in English + Telugu.")
                if res:
                    st.markdown(res)

with tab_practice:
    st.subheader("📝 Practice Mock Test")
    subject_choice = st.selectbox(
        "Choose Subject:",
        ["Mixed SSC Mock Test", "Quantitative Aptitude", "Logical Reasoning", "General Awareness (GK)", "English Language"]
    )
    st.info("💡 Practice tests help build speed & accuracy!")

    if st.button("⚡ Generate Test"):
        with st.spinner("Generating 5 fresh questions..."):
            prompt = (
                f"Generate a 5-question MCQ test for {subject_choice}. "
                "Provide Questions 1-5 with options first. "
                "Then provide Answer Key with step-by-step explanations in English + Telugu."
            )
            res = generate_response(prompt)
            if res:
                st.markdown(res)
