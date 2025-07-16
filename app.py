import streamlit as st
import json
import os

st.set_page_config(page_title="Spotlight - Event Aggregator", layout="wide")
st.title("🎯 Spotlight - Event Aggregator for Students")

# Load existing events

if os.path.exists("events.json"):
    with open("events.json", "r") as f:
        events = json.load(f)
else:
    events = []

# Sidebar: Add New Event Form

st.sidebar.header("➕ Add a New Event")

with st.sidebar.form("event_form"):
    title = st.text_input("📌 Event Title")
    etype = st.selectbox("📂 Event Type", ["Internship", "Hackathon", "Seminar", "Workshop"])
    deadline = st.date_input("📅 Registration Deadline")
    link = st.text_input("🔗 Apply Link")
    submit = st.form_submit_button("Submit")

    if submit:
        if title and link:
            new_event = {
                "title": title,
                "type": etype,
                "deadline": str(deadline),  # Convert date to string
                "apply_link": link
            }
            events.append(new_event)

            with open("events.json", "w") as f:
                json.dump(events, f, indent=2)

            st.success("✅ Event added successfully!")
            st.experimental_rerun()
        else:
            st.warning("⚠️ Please fill all fields.")


# Main: Show Events

st.subheader("📅 All Student Events")

search = st.text_input("🔍 Search events by title:")

filtered = [e for e in events if search.lower() in e['title'].lower()]

if filtered:
    for event in filtered:
        st.markdown(f"""
        ### 🔹 {event['title']}
        **Type:** {event['type']}  
        **Deadline:** {event['deadline']}  
        [🔗 Apply Now]({event['apply_link']})
        """)
        st.markdown("---")
else:
    st.info("No events found. Try a different search.")
