import streamlit as st
import google.generativeai as genai
import sqlite3
import pandas as pd
import plotly.express as px

# ---------------- GEMINI ----------------

genai.configure(
    api_key="YOUR API KEY"
)

model = genai.GenerativeModel(
    "gemini-2.5-flash-lite"
)

# ---------------- DATABASE ----------------

conn = sqlite3.connect(
    "database.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS moods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS journal(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

def save_mood(mood):
    cursor.execute(
        "INSERT INTO moods(mood) VALUES(?)",
        (mood,)
    )
    conn.commit()

def save_journal(text):
    cursor.execute(
        "INSERT INTO journal(content) VALUES(?)",
        (text,)
    )
    conn.commit()

def get_moods():
    cursor.execute(
        "SELECT mood FROM moods"
    )
    return cursor.fetchall()

# ---------------- PAGE ----------------

st.set_page_config(
    page_title="SafeSpace AI",
    page_icon="💙",
    layout="wide"
)

st.title("💙 SafeSpace AI")
st.caption("Talk. Reflect. Grow.")

# ---------------- SIDEBAR ----------------

menu = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "AI Companion",
        "Mood Tracker",
        "Journal",
        "Letter Never Sent",
        "Relaxation",
        "Motivation",
        "Insights"
    ]
)

# ---------------- HOME ----------------

if menu == "Home":

    st.header("Welcome to SafeSpace AI")

    st.write("""
    A private place to:

    • Talk freely

    • Track your moods

    • Journal your thoughts

    • Reflect on emotions

    • Practice relaxation

    • Get motivation
    """)

# ---------------- AI COMPANION ----------------

elif menu == "AI Companion":

    st.header("🤖 AI Companion")

    question = st.text_area(
        "What's on your mind?"
    )

    if st.button("Talk"):

        prompt = f"""
        You are SafeSpace AI.

        Be supportive and empathetic.

        Help users reflect on emotions.

        Never diagnose illnesses.

        User:
        {question}
        """

        response = model.generate_content(
            prompt
        )

        st.success(
            response.text
        )

# ---------------- MOOD TRACKER ----------------

elif menu == "Mood Tracker":

    st.header("😊 Mood Tracker")

    mood = st.selectbox(
        "How do you feel today?",
        [
            "😊 Happy",
            "😔 Sad",
            "😟 Anxious",
            "😴 Tired",
            "😐 Neutral",
            "🤩 Excited"
        ]
    )

    if st.button("Save Mood"):

        save_mood(mood)

        st.success(
            "Mood saved successfully!"
        )

# ---------------- JOURNAL ----------------

elif menu == "Journal":

    st.header("📔 Private Journal")

    journal = st.text_area(
        "Write your thoughts"
    )

    if st.button("Save Journal"):

        save_journal(journal)

        prompt = f"""
        Analyze this journal.

        Give:

        1. Main emotion
        2. Positive observation
        3. Reflection question

        Journal:
        {journal}
        """

        response = model.generate_content(
            prompt
        )

        st.write(
            response.text
        )

# ---------------- LETTER NEVER SENT ----------------

elif menu == "Letter Never Sent":

    st.header("💌 Letter Never Sent")

    letter = st.text_area(
        "Write anything you wish you could say"
    )

    if st.button(
        "Reflect on Letter"
    ):

        prompt = f"""
        Analyze this private letter.

        Mention:

        - emotions
        - concerns
        - healthy reflection

        Letter:
        {letter}
        """

        response = model.generate_content(
            prompt
        )

        st.write(
            response.text
        )

# ---------------- RELAXATION ----------------

elif menu == "Relaxation":

    st.header("🌿 Relaxation Corner")

    option = st.selectbox(
        "Choose",
        [
            "Breathing",
            "Exam Stress",
            "Sleep",
            "Overthinking"
        ]
    )

    if st.button("Start"):

        prompt = f"""
        Give a detailed relaxation guide for:

        {option}
        """

        response = model.generate_content(
            prompt
        )

        st.write(
            response.text
        )

# ---------------- MOTIVATION ----------------

elif menu == "Motivation":

    st.header("✨ Daily Motivation")

    if st.button("Generate Motivation"):

        response = model.generate_content(
            """
            Give an inspiring motivational
            message for a student.
            """
        )

        st.success(
            response.text
        )

# ---------------- INSIGHTS ----------------

elif menu == "Insights":

    st.header("📊 Mood Insights")

    moods = get_moods()

    if moods:

        df = pd.DataFrame(
            moods,
            columns=["Mood"]
        )

        fig = px.pie(
            df,
            names="Mood",
            title="Mood Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No mood data available yet."
        )
