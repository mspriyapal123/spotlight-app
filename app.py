import streamlit as st
import json
import os

# Load events
if os.path.exists("events.json"):
    with open("events.json", "r") as f:
        events = json.load(f)
else:
    events = []

st.set_page_config(page_title="Spotlight - Event Aggregator", layout="centered")

st.title("🎯 Spotlight - Event Aggregator for Students")

# Add a new event
st.sidebar.header("➕ Add a New Event")

with st.sidebar.form("event_form"):
    title = st.text_input("Event Title")
    event_type = st.selectbox("Event Type", ["Internship", "Hackathon", "Workshop", "Seminar", "Conference", "Contest", "Other"])
    deadline = st.date_input("Registration Deadline")
    link = st.text_input("Apply Link")
    submitted = st.form_submit_button("Submit")

    if submitted and title and event_type and link:
        new_event = {
            "title": title,
            "type": event_type,
            "deadline": deadline.strftime("%Y/%m/%d"),
            "link": link
        }
        events.append(new_event)
        with open("events.json", "w") as f:
            json.dump(events, f, indent=2)
        st.success("✅ Event added successfully! Please refresh the app.")

# Filter and search
st.header("📚 All Student Events")

search = st.text_input("🔍 Search events by title:")

filtered = [e for e in events if search.lower() in e['title'].lower()]
for event in filtered:
    st.markdown(f"### {event['title']}")
    st.markdown(f"**Type:** {event['type']}")
    st.markdown(f"**Deadline:** {event.get('deadline', 'N/A')}")
    st.markdown(f"[Apply Now]({event['link']})")
    st.markdown("---")

# 📄 Resume Match Analyzer

st.header("📄 Resume Match Analyzer")

# Input resume
resume_text = st.text_area("✍️ Paste your resume text here")

# Input job description
jd_text = st.text_area("📋 Paste the job description here")

# Compare button
if st.button("🔍 Analyze Match"):
    if resume_text and jd_text:
        # Convert both texts to lowercase
        resume_words = set(resume_text.lower().split())
        jd_words = set(jd_text.lower().split())

        # Matching keywords
        common = resume_words.intersection(jd_words)
        missing = jd_words - resume_words

        match_percent = round(len(common) / len(jd_words) * 100, 2)

        st.success(f"✅ Match Score: {match_percent}%")
        st.markdown("### ✅ Common Keywords Found:")
        st.write(", ".join(common))

        st.markdown("### ❌ Missing Important Keywords:")
        st.write(", ".join(missing))
    else:
        st.warning("Please paste both resume and job description text.")


import PyPDF2

st.markdown("---")
st.header("📄 Resume Match Analyzer")

# Step 1: Upload resume PDF
st.subheader("📤 Upload Your Resume (PDF)")
uploaded_file = st.file_uploader("Choose your resume file", type="pdf")

resume_text = ""  # Empty string to hold resume text

if uploaded_file is not None:
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        resume_text += page.extract_text()
    st.text_area("📄 Extracted Resume Text", resume_text, height=200)

# Step 2: Paste job description
jd_text = st.text_area("📋 Paste the job description here")

# Step 3: Match Resume and JD
if st.button("🔍 Analyze Match"):
    if resume_text and jd_text:
        resume_words = set(resume_text.lower().split())
        jd_words = set(jd_text.lower().split())

        common = resume_words.intersection(jd_words)
        missing = jd_words - resume_words

        match_percent = round(len(common) / len(jd_words) * 100, 2)

        st.success(f"✅ Match Score: {match_percent}%")
        st.markdown("### ✅ Common Keywords Found:")
        st.write(", ".join(common))

        st.markdown("### ❌ Missing Important Keywords:")
        st.write(", ".join(missing))

        if missing:
            st.markdown("### 💡 Suggestions to Improve Your Resume:")
            for keyword in list(missing)[:5]:
                st.write(f"- Add the keyword: **{keyword}**")
    else:
        st.warning("Please upload a resume and paste job description.")


