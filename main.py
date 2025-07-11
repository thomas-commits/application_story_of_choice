import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

import os
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase only once
if not firebase_admin._apps:
    firebase_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if not firebase_json:
        st.error("❌ Firebase credentials not found. Check your Render environment variables.")
    else:
        cred_dict = json.loads(firebase_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)


# Connect to Firestore
db = firestore.client()

# Streamlit UI
st.set_page_config(page_title="Story of Choice", layout="centered")
st.title("📚 Add Your Story")

name = st.text_input("👤 Your Name (used as ID)")
title = st.text_input("📝 Story Title")
text = st.text_area("✍️ Write Your Story (max 100 characters)", max_chars=100)

if st.button("Submit Story"):
    if not name or not title or not text:
        st.warning("Please fill in all fields.")
    else:
        doc_ref = db.collection("user_stories").document(name)
        doc_ref.set({
            "title": title,
            "text": text
        })
        st.success(f"Story for '{name}' saved successfully!")

# Optional: View all stories
if st.checkbox("📖 Show All Stories"):
    stories = db.collection("user_stories").stream()
    for story in stories:
        data = story.to_dict()
        st.subheader(data['title'])
        st.caption(f"By {story.id}")
        st.write(data['text'])
