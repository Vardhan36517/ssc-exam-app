import streamlit as st
from google import genai
from google.genai import types

# Page Config
st.set_page_config(page_title="ExamSaathi - SSC & Govt Exams", page_icon="📚", layout="centered")

# Get API Key securely
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

SYSTEM_INSTRUCTION = """
You are 'ExamSaathi', an expert AI mentor and tutor created specifically to help the user prepare for Indian Competitive Exams (SSC CGL, CHSL, Banking, Railway, APPSC/TSPSC).

Key Rules:
1. Language: Explain every concept using a simple, clear combination of English and Telugu script (Bilingual). Technical terms should be in English with clear Telugu explanations.
2. Subject Knowledge: You are an expert across Quantitative Aptitude, Logical Reasoning, General Awareness (GK/Current Affairs), and English Language.
3. Structure: Use bold headers and clean bullet points for easy reading.
"""

@st.cache_resource
def get_client(api_key):
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

client = get_client(GEMINI_API_KEY)

# Header
st.title("📚 ExamSaathi")
st.caption("Your Personal SSC & Government Exam Mentor (English + Telugu)")

if not GEMINI_API_KEY:
    st.error("Please add your GEMINI_API_KEY in Streamlit Secrets!")
    st.stop()

# 2 Main Sections (Tabs)
tab_learn, tab_practice = st.tabs(["📖 1. Learning & Guidance", "📝 2. Practice & Mock Test"])

# ---------------------------------------------------------
# SECTION 1: LEARNING & GUIDANCE
# ---------------------------------------------------------
with tab_learn:
    st.header("Learning & Study Guidance")
    st.write("Learn any topic in English + Telugu or get customized study routines!")

    learn_option = st.radio(
        "Choose an option:",
        ["Ask a Doubt / Learn a Topic", "Get Daily Study Schedule & Strategy"],
        horizontal=True
    )

    if learn_option == "Ask a Doubt / Learn a Topic":
        st.subheader("💡 Ask Anything (Maths, Reasoning, English, GK)")
        user_query = st.text_area(
            "Type your topic or question below:",
            placeholder="e.g., Explain Time and Work shortcuts or Current Affairs..."
        )
        if st.button("Explain Concept 🚀"):
            if user_query:
                with st.spinner("Preparing explanation in English + Telugu..."):
                    prompt = f"Thoroughly explain the topic with clear step-by-step guidance: {user_query}"
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
                    )
                    st.markdown(response.text)
            else:
                st.warning("Please enter a question or topic name!")

    elif learn_option == "Get Daily Study Schedule & Strategy":
        st.subheader("📅 Personalized Time Management Plan")
        exam_name = st.text_input("Target Exam", "SSC CGL")
        study_hours = st.slider("How many hours can you study daily?", 2, 12, 6)
        if st.button("Generate Time Table 🎯"):
            with st.spinner("Designing study schedule..."):
                prompt = f"Create a daily time management routine for {exam_name} for someone with {study_hours} hours available per day. Divide slots for Quant, Reasoning, English, GK, and daily revision. Explain in English + Telugu."
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
                )
                st.markdown(response.text)

# ---------------------------------------------------------
# SECTION 2: PRACTICE & MOCK TEST
# ---------------------------------------------------------
with tab_practice:
    st.header("Practice Test Section")
    st.write("Take practice tests twice a week (or anytime) to test your speed and concepts!")

    subject_choice = st.selectbox(
        "Select Test Topic:",
        ["All Subjects (Mixed SSC Mock)", "Quantitative Aptitude (Maths)", "Logical Reasoning", "General Awareness (GK)", "English Language"]
    )
    st.info("💡 **Recommended Schedule:** Practice on Wednesdays and Sundays!")

    if st.button("🎯 Generate Practice Test"):
        with st.spinner("Generating 5 fresh questions with answers..."):
            prompt = (
                f"Generate a 5-question multiple choice practice test for {subject_choice} based on official exam patterns. "
                "List Questions 1 to 5 with options A, B, C, D first. "
                "Below all questions, provide the Answer Key with detailed solutions explained in English + Telugu."
            )
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
            )
            st.markdown(response.text)
