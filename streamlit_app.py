import streamlit as st
import google.generativeai as genai

# App Title
st.title("📚 AI Learning App")
st.write("Learn **English**, **Math**, and **Science** with Gemini AI. 🎓")

# Gemini API Key
gemini_api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")

if not gemini_api_key:
    st.info("Please enter your Gemini API key to continue.", icon="🗝️")
else:
    # Configure Gemini
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Tabs for each subject
    tab1, tab2, tab3 = st.tabs(["📝 English", "➗ Math", "🔬 Science"])

    # --- English Section ---
    with tab1:
        st.header("📝 English Learning")
        eng_topic = st.text_input("Enter an English topic (e.g., Adjectives, Verbs):", key="eng_topic")

        if st.button("Generate English Content"):
            if not eng_topic.strip():
                st.warning("Please enter an English topic.")
            else:
                with st.spinner("Generating English lesson..."):
                    explanation = model.generate_content(f"""
                    Explain the English topic "{eng_topic}" in a short and simple way for students.
                    Keep it under 8 sentences.
                    Include at least 2 simple examples in bullet points and bold important words.
                    """)
                    st.session_state.eng_expl = explanation.text

                    questions = model.generate_content(f"""
                    Create 5 questions about "{eng_topic}" with correct answers.
                    Format like:
                    Q1: ...
                    A1: ...
                    """)
                    st.session_state.eng_ques = questions.text

        if "eng_expl" in st.session_state:
            st.subheader("📖 English Explanation with Examples")
            st.markdown(st.session_state.eng_expl)

        if "eng_ques" in st.session_state:
            st.subheader("📝 English Practice")
            st.text_area("Questions + Answers", st.session_state.eng_ques, height=300)

    # --- Math Section ---
    with tab2:
        st.header("➗ Math Learning")
        math_topic = st.text_input("Enter a Math topic (e.g., Fractions, Algebra):", key="math_topic")

        if st.button("Generate Math Content"):
            if not math_topic.strip():
                st.warning("Please enter a Math topic.")
            else:
                with st.spinner("Generating Math lesson..."):
                    explanation = model.generate_content(f"""
                    Explain the math topic "{math_topic}" in a short and simple way for students.
                    Keep it under 8 sentences.
                    Include at least 2 solved examples formatted in code blocks.
                    """)
                    st.session_state.math_expl = explanation.text

                    questions = model.generate_content(f"""
                    Create 5 math problems about "{math_topic}" with answers.
                    Format like:
                    Q1: ...
                    A1: ...
                    """)
                    st.session_state.math_ques = questions.text

        if "math_expl" in st.session_state:
            st.subheader("📖 Math Explanation with Examples")
            st.markdown(st.session_state.math_expl)

        if "math_ques" in st.session_state:
            st.subheader("🧮 Math Practice")
            st.text_area("Questions + Answers", st.session_state.math_ques, height=300)

    # --- Science Section ---
    with tab3:
        st.header("🔬 Science Learning")
        sci_topic = st.text_input("Enter a Science topic (e.g., Photosynthesis, Gravity):", key="sci_topic")

        if st.button("Generate Science Content"):
            if not sci_topic.strip():
                st.warning("Please enter a Science topic.")
            else:
                with st.spinner("Generating Science lesson..."):
                    explanation = model.generate_content(f"""
                    Explain the science topic "{sci_topic}" in a short and simple way for students.
                    Keep it under 8 sentences.
                    Include at least 2 real-life examples as bullet points.
                    """)
                    st.session_state.sci_expl = explanation.text

                    questions = model.generate_content(f"""
                    Create 5 science questions about "{sci_topic}" with answers.
                    Format like:
                    Q1: ...
                    A1: ...
                    """)
                    st.session_state.sci_ques = questions.text

        if "sci_expl" in st.session_state:
            st.subheader("📖 Science Explanation with Examples")
            st.markdown(st.session_state.sci_expl)

        if "sci_ques" in st.session_state:
            st.subheader("🔍 Science Practice")
            st.text_area("Questions + Answers", st.session_state.sci_ques, height=300)

