import streamlit as st
import google.generativeai as genai
import re

# App title & description
st.title("📚 English Teacher Quiz 🤖✨")
st.write(
    "This app teaches you **10 English words with examples** and then gives you a fun **quiz** "
    "with stickers 🎉. It uses Google's **Gemini AI**. "
    "Enter your API key below to start learning."
)

# Ask user for their Gemini API key
gemini_api_key = st.text_input("🔑 Gemini API Key", type="password")

if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:
    # Configure Gemini client
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Step 1: Get words and examples
    if st.button("✨ Get 10 Words + Examples"):
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
        st.subheader("✨ 10 Words and Examples")
        st.write(st.session_state.words_examples)

        # Step 2: Create quiz
        if st.button("📝 Create Quiz"):
            with st.spinner("Generating quiz..."):
                quiz = model.generate_content(f"""
                You are an English teacher.
                I have these words with examples:
                {st.session_state.words_examples}

                Make a 10-question quiz for me.
                Use multiple choice (A/B/C/D).
                After listing the questions, write the correct answers as:
                Answers: 1-A, 2-C, 3-B ...
                """)
                st.session_state.quiz_text = quiz.text

    # Step 3: Run quiz
    if "quiz_text" in st.session_state:
        st.subheader("📝 Quiz Time!")

        parts = st.session_state.quiz_text.split("Answers:")
        questions = parts[0].strip()
        answers_text = parts[1].strip() if len(parts) > 1 else ""

        st.text_area("📖 Quiz Questions", questions, height=300)

        # Extract answers
        answer_key = {}
        matches = re.findall(r"(\d+)\s*[-:]?\s*([A-D])", answers_text)
        for num, ans in matches:
            answer_key[int(num)] = ans.upper()

        score = 0
        for i in range(1, len(answer_key) + 1):
            user_ans = st.radio(f"Q{i}: Your Answer", ["A", "B", "C", "D"], key=f"q{i}")
            if st.button(f"Check Q{i}", key=f"check{i}"):
                correct = answer_key[i]
                if user_ans == correct:
                    st.success("🌟 ✅ Correct! 🎉😃")
                    score += 1
                else:
                    st.error(f"❌ Wrong 😢👎 Correct answer: {correct}")

        st.write(f"🎯 Final Score: {score}/{len(answer_key)}")
        if score == len(answer_key):
            st.success("🏆🌟 PERFECT SCORE! 🎉🥳")
        elif score >= len(answer_key) // 2:
            st.info("👏 Good job! Keep practicing 💪")
        else:
            st.warning("📘 Don’t give up, study again and retry! 🚀")
