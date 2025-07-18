import streamlit as st
import json

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



