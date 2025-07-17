import streamlit as st
import json
import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load existing events
st.set_page_config(page_title="Spotlight - Event Aggregator", layout="wide")
st.title("🎯 Spotlight - Event Aggregator for Students")

if os.path.exists("events.json"):
    with open("events.json", "r") as f:
        events = json.load(f)
else:
    events = []

# Sidebar form to add new event
st.sidebar.header("➕ Add New Event")
with st.sidebar.form("event_form"):
    title = st.text_input("Event Title")
    etype = st.selectbox("Event Type", ["Internship","Hackathon","Workshop","Seminar","Conference","Contest","Other"])
    deadline = st.date_input("Registration Deadline")
    link = st.text_input("Apply Link")
    if st.form_submit_button("Submit"):
        if title and link:
            new_event = {"title":title, "type":etype, "deadline":deadline.strftime("%Y/%m/%d"), "link":link}
            events.append(new_event)
            with open("events.json","w") as f:
                json.dump(events, f, indent=2)
            st.success("✅ Event added successfully!")
            st.experimental_rerun()
        else:
            st.warning("⚠️ Please fill all fields.")

# Display events
st.subheader("📅 All Student Events")
search = st.text_input("🔍 Search events by title:")
filtered = [e for e in events if search.lower() in e.get("title","").lower()]

if filtered:
    for event in filtered:
        st.markdown(f"### {event.get('title','Untitled')}")
        st.markdown(f"**Type:** {event.get('type','N/A')}")
        st.markdown(f"**Deadline:** {event.get('deadline','N/A')}")
        st.markdown(f"[🔗 Apply Now]({event.get('link','#')})")
        st.markdown("---")
else:
    st.info("No events found. Try a different search!")

# ----------------------------
# 📄 Resume Match Analyzer
# ----------------------------
st.markdown("---")
st.markdown("## 📝 Resume Match Analyzer")

# PDF Upload
uploaded_file = st.file_uploader("📤 Upload your resume (PDF format)", type=["pdf"])
resume_text = ""
if uploaded_file is not None:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text() or ""
        st.success("✅ Resume text extracted successfully!")
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")

# Show extracted + allow edit
resume_input = st.text_area("📝 Resume Text", value=resume_text, height=200)
jd_text = st.text_area("📄 Job Description", height=200)

# Matching logic
if st.button("🔍 Analyze Match"):
    if resume_input.strip()=="" or jd_text.strip()=="":
        st.warning("⚠️ Please provide both resume and job description text.")
    else:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_input, jd_text])
        sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        score = round(sim*100, 2)
        st.markdown(f"### ✅ Match Score: **{score}%**")
        
        if score > 70:
            st.success("🎯 Great match! Your resume aligns well.")
        elif score > 40:
            st.info("👍 Decent match, can be improved.")
        else:
            st.warning("⚠️ Low match. Consider updating your resume.")

        # Keywords info
        resume_words = set(resume_input.lower().split())
        jd_words = set(jd_text.lower().split())
        common = resume_words.intersection(jd_words)
        missing = jd_words - resume_words

        st.markdown("### ✅ Common Keywords Found")
        st.write(", ".join(common) or "None")

        st.markdown("### ❌ Missing Keywords")
        st.write(", ".join(missing) or "None")

        if missing:
            st.markdown("### 💡 Suggestions")
            st.info("Try including these: " + ", ".join(list(missing)[:5]))
