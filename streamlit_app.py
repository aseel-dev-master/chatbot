import streamlit as st
import google.generativeai as genai
import re
import io
import xmind_sdk as xmind   # install with: pip install xmind-sdk

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- AI Functions ----------
def get_explanation(topic, subject):
    prompt = f"""
    Give a short explanation about {topic} in {subject} with simple language.
    Include 2-3 examples in bullet points.
    """
    response = model.generate_content(prompt)
    return response.text

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

def check_answer(user_ans, correct_ans):
    user_ans = user_ans.lower()
    correct_ans = correct_ans.lower()
    return all(word in user_ans for word in correct_ans.split()[:2])  # simple keyword check

def generate_mindmap_outline(topic, subject):
    prompt = f"""
    Create a structured mind map for the topic: {topic} in {subject}.
    Use bullet points, short labels:
    - Main topic
      - Subtopic
        - Point A
        - Point B
    Make at least two levels deep.
    """
    return model.generate_content(prompt).text

def outline_to_xmind(outline_text, root_title):
    doc = xmind.XMindDocument.create("Sheet 1", root_title)
    sheet = doc.get_first_sheet()
    root = sheet.get_root_topic()

    # Parse bullet format and build tree
    stack = [(0, root)]
    for line in outline_text.splitlines():
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if not stripped.startswith("-"):
            continue
        title = stripped[1:].strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        node = parent.add_subtopic(title)
        stack.append((indent, node))
    return doc

# ---------- Streamlit UI ----------
st.title("📚 AI Learning Assistant")
st.write("Learn English, Math, and Science interactively!")

# Tabs
tabs = st.tabs(["📖 English", "➗ Math", "🔬 Science"])

for i, subject in enumerate(["English", "Math", "Science"]):
    with tabs[i]:
        st.header(f"{subject} Learning")
        topic = st.text_input(f"Enter a {subject} topic:", key=f"topic_{subject}")

        if st.button(f"Generate {subject} Content", key=f"gen_{subject}"):
            if topic.strip():
                with st.spinner("Generating content..."):
                    explanation = get_explanation(topic, subject)
                    qa_pairs = get_questions(topic, subject)
                    outline = generate_mindmap_outline(topic, subject)

                # Explanation
                st.subheader("📘 Explanation with Examples")
                st.markdown(explanation)

                # Questions
                st.subheader("📝 Practice Questions")
                answers = {}
                for idx, (q, a) in enumerate(qa_pairs):
                    st.write(f"**Q{idx+1}: {q}**")
                    answers[idx] = {
                        "user": st.text_input(f"Your answer for Q{idx+1}", key=f"{subject}_{idx}"),
                        "correct": a
                    }

                if st.button(f"Check {subject} Answers", key=f"check_{subject}"):
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

                # Mind map
                st.subheader("🧠 Mind Map")
                st.text(outline)

                # Convert to XMind and enable download
                doc = outline_to_xmind(outline, topic)
                buf = io.BytesIO()
                doc.save(buf)
                buf.seek(0)

                st.download_button(
                    label="⬇️ Download Mind Map (.xmind)",
                    data=buf,
                    file_name=f"{topic}_mindmap.xmind",
                    mime="application/octet-stream"
                )
            else:
                st.warning("Please enter a topic!")
