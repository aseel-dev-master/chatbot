import streamlit as st
import google.generativeai as genai

# App title
st.title("📚 AI Learning App 🤖✨")
st.write("Learn **English words** or practice **Math** . 🎉")

# 🔑 Gemini API Key
gemini_api_key = st.text_input("🔑 Gemini API Key", type="password")

if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # -------------------------
    # 📘 English Teacher Quiz
    # -------------------------
    st.header("✨ English Teacher Quiz")

    if st.button("Get 10 Words + Examples"):
        with st.spinner("Asking Gemini for words..."):
            response = model.generate_content("""
            You are an English teacher.
            1. Give me 10 useful English words for learning.
            2. For each word, write one simple example sentence.
            Format your answer as:
            word - example
            """)
            st.session_state.words_examples = response.text

    if "words_examples" in st.session_state:
        st.subheader("10 Words and Examples")
        st.write(st.session_state.words_examples)

        if st.button("Create Quiz"):
            with st.spinner("Generating quiz..."):
                quiz = model.generate_content(f"""
                You are an English teacher.
                I have these words with examples:
                {st.session_state.words_examples}

                Make a 10-question quiz for me.
                Use multiple choice (A/B/C/D).
                At the end, write the correct answers as:
                Answers: 1-A, 2-C, 3-B ...
                """)
                st.session_state.quiz_text = quiz.text

    if "quiz_text" in st.session_state:
        st.subheader("📝 Quiz Time!")
        st.text_area("📖 Quiz Questions + Answers", st.session_state.quiz_text, height=300)

    # -------------------------
    # ➗ Math Practice Section
    # -------------------------
    st.header("➗ Math Practice with Explanations")

    math_topic = st.text_input("Enter a math topic (e.g., fractions, algebra, geometry):")

    if st.button("Generate Math Practice"):
        if not math_topic.strip():
            st.warning("Please enter a math topic first.")
        else:
            with st.spinner(f"Asking Gemini for {math_topic}..."):
                # Short explanation
                explanation = model.generate_content(f"""
                You are a math teacher.
                Explain the topic "{math_topic}" in a short and simple way for a student.
                Keep it under 8 sentences.
                """)
                st.session_state.math_expl = explanation.text

                # Practice problems
                problems = model.generate_content(f"""
                You are a math teacher.
                Create 5 practice problems about {math_topic}.
                Only show the questions first (Q1, Q2, etc.) WITHOUT answers.
                Format clearly.
                """)
                st.session_state.math_problems = problems.text

                # Correct answers (to check later)
                answers = model.generate_content(f"""
                You are a math teacher.
                Create the correct answers for 5 practice problems about {math_topic}.
                Format as:
                A1: answer
                A2: answer
                A3: answer
                A4: answer
                A5: answer
                """)
                st.session_state.math_answers = answers.text

    if "math_expl" in st.session_state:
        st.subheader("📖 Short Explanation")
        st.write(st.session_state.math_expl)

    if "math_problems" in st.session_state:
        st.subheader("🧮 Solve These Problems")
        st.write(st.session_state.math_problems)

        # Input fields for answers
        user_answers = []
        for i in range(1, 6):
            ans = st.text_input(f"Your Answer for Q{i}:")
            user_answers.append(ans)

        if st.button("Check Answers"):
            st.subheader("✅ Results")
            correct_list = st.session_state.math_answers.split("\n")
            score = 0

            for i in range(5):
                if i < len(correct_list):
                    correct = correct_list[i].strip()
                    user = user_answers[i].strip()
                    if user and user in correct:
                        st.write(f"Q{i+1}: 🌟 ✅ Correct! 🎉")
                        score += 1
                    else:
                        st.write(f"Q{i+1}: ❌ Wrong 😢 | {correct}")

            st.write(f"Final Score: {score}/5")

