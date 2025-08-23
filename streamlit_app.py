import streamlit as st
import google.generativeai as genai
import re

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get explanation + examples
def get_explanation(topic, subject):
    prompt = f"""
    Give a short explanation about {topic} in {subject} with simple language.
    Include 2-3 examples in bullet points.
    """
    response = model.generate_content(prompt)
    return response.text

# Function to generate 5 questions with answers
def get_questions(topic, subject):
    prompt = f"""
    Generate 5 questions with correct answers about {topic} in {subject}.
    Format as:
    Q: question text
    A: answer text
    """
    response = model.generate_content(prompt)
    qa_pairs = []
    for match in re.findall(r"Q:\s*(.*?)\s*A:\s*(.*?)(?=Q:|$)", response.text, re.S):
        qa_pairs.append((match[0].strip(), match[1].strip()))
    return qa_pairs

# Function to check answers (loose matching)
def check_answer(user_ans, correct_ans):
    user_ans = user_ans.lower()
    correct_ans = correct_ans.lower()
    return all(word in user_ans for word in correct_ans.split()[:2])  # simple keyword check

st.title("📚 AI Learning Assistant")
st.write("Learn English, Math, and Science interactively!")

# Tabs
tabs = st.tabs(["📖 English", "➗ Math", "🔬 Science"])

for i, subject in enumerate(["English", "Math", "Science"]):
    with tabs[i]:
        st.header(f"{subject} Learning")
        topic = st.text_input(f"Enter a {subject} topic:")
        
        if st.button(f"Generate {subject} Content"):
            if topic.strip():
                with st.spinner("Generating content..."):
                    explanation = get_explanation(topic, subject)
                    qa_pairs = get_questions(topic, subject)

                st.subheader("📘 Explanation with Examples")
                st.markdown(explanation)

                st.subheader("📝 Practice Questions")
                answers = {}
                for idx, (q, a) in enumerate(qa_pairs):
                    st.write(f"**Q{idx+1}: {q}**")
                    answers[idx] = {
                        "user": st.text_input(f"Your answer for Q{idx+1}", key=f"{subject}_{idx}"),
                        "correct": a
                    }

                if st.button(f"Check {subject} Answers"):
                    st.subheader("✅ Results")
                    score = 0
                    for idx, ans in answers.items():
                        st.write(f"**Q{idx+1}:** {qa_pairs[idx][0]}")
                        st.write(f"**Your Answer:** {ans['user']}")
                        st.write(f"**Correct Answer:** {ans['correct']}")
                        if check_answer(ans['user'], ans['correct']):
                            st.success("✅ Correct!")
                            score += 1
                        else:
                            st.error("❌ Incorrect")
                    st.write(f"**Your Score: {score}/5**")
            else:
                st.warning("Please enter a topic!")
