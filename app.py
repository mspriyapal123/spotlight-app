import streamlit as st
import json

# Load events
with open("events.json", "r") as f:
    events = json.load(f)

st.title("🎓 UniHub - Student Event Aggregator")

# Get unique types from events
event_types = list(set([e["type"] for e in events]))
event_types.sort()
event_types.insert(0, "All")

# Sidebar filters
st.sidebar.header("🎯 Filter Events")
selected_type = st.sidebar.selectbox("Choose Type", event_types)

# Search bar
search = st.text_input("🔍 Search events")

# Filter by type and search
filtered = []
for e in events:
    if (selected_type == "All" or e["type"] == selected_type) and search.lower() in e["title"].lower():
        filtered.append(e)

# Display
for event in filtered:
    st.subheader(event["title"])
    st.write(f"Type: {event['type']}")
    st.markdown(f"[Apply Now]({event['apply_link']})", unsafe_allow_html=True)
    st.markdown("---")
