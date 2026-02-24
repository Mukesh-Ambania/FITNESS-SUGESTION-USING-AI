import streamlit as st
import random
import pandas as pd
import time
from ai_engine import get_full_health_plan, generate_ai_response


st.set_page_config(
    page_title="AI Fitness Coach",
    layout="wide",
    page_icon="🏋️"
)


st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: white;
}
.main {
    background: radial-gradient(circle at top, #0b0f1a, #06080f);
}
.hero {
    padding: 60px;
    border-radius: 20px;
    margin-bottom: 25px;
    background: linear-gradient(135deg, #ff4d4d, #ff884d);
}
.glass {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 25px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}
.metric {
    font-size: 34px;
    font-weight: bold;
    color: #ff4d4d;
}
.section-title {
    font-size: 26px;
    font-weight: 800;
    color: #ff884d;
}
.plan-text {
    font-size: 18px;
    line-height: 1.8;
}
.footer {
    margin-top: 30px;
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(135deg, #203a43, #2c5364);
    text-align: center;
    font-size: 16px;
}
.stButton button {
    background: linear-gradient(135deg, #ff4d4d, #ff884d);
    color: white;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "dashboard"


st.markdown("""
<div class="hero">
<h1>Train Smarter. Live Stronger.</h1>
<p>AI-powered fitness intelligence for performance and health optimization</p>
</div>
""", unsafe_allow_html=True)


c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🏠 Dashboard"):
        st.session_state.page = "dashboard"

with c2:
    if st.button("📋 Generate Plan"):
        st.session_state.page = "plan"

with c3:
    if st.button("💬 AI Coach"):
        st.session_state.page = "chat"


if st.session_state.page == "dashboard":

    st.markdown('<div class="section-title">Performance Overview</div>', unsafe_allow_html=True)


    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.image(
        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=1400&q=80",
        width="stretch"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    
    col1, col2, col3 = st.columns(3)
    h = col1.empty()
    o = col2.empty()
    c = col3.empty()

    for _ in range(6):
        h.markdown(f'<div class="glass"><div class="metric">❤️ {random.randint(65,90)}</div>Heart Rate BPM</div>', unsafe_allow_html=True)
        o.markdown(f'<div class="glass"><div class="metric">🫁 {random.randint(95,100)}%</div>Oxygen Level</div>', unsafe_allow_html=True)
        c.markdown(f'<div class="glass"><div class="metric">🔥 {random.randint(1800,2600)}</div>Calories Burned</div>', unsafe_allow_html=True)
        time.sleep(0.4)

    
    st.markdown('<div class="section-title">Weekly Training Load</div>', unsafe_allow_html=True)

    data = pd.DataFrame({
        "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        "Intensity": [3,4,2,5,4,6,5]
    })

    st.bar_chart(data.set_index("Day"))

elif st.session_state.page == "plan":

    st.sidebar.header("User Profile")

    name = st.sidebar.text_input("Name", "John")
    age = st.sidebar.number_input("Age", 10, 100, 25)
    weight = st.sidebar.number_input("Weight (kg)", 30, 200, 70)
    height = st.sidebar.number_input("Height (cm)", 100, 250, 170)

    activity = st.sidebar.selectbox("Activity Level", ["Low","Moderate","High"])
    diet = st.sidebar.selectbox("Diet", ["Keto","Vegetarian","Balanced","Low Carb"])
    goal = st.sidebar.selectbox("Goal", ["Weight Loss","Muscle Gain","Endurance","Flexibility"])

    def format_plan(text):
        text = text.replace("Breakfast","<span style='color:#ff884d;font-weight:bold;font-size:22px'>🍳 BREAKFAST</span>")
        text = text.replace("Lunch","<span style='color:#ff884d;font-weight:bold;font-size:22px'>🍛 LUNCH</span>")
        text = text.replace("Dinner","<span style='color:#ff884d;font-weight:bold;font-size:22px'>🍲 DINNER</span>")
        text = text.replace("Snacks","<span style='color:#ff884d;font-weight:bold;font-size:22px'>🥗 SNACKS</span>")
        text = text.replace("Workout","<span style='color:#ff4d4d;font-weight:bold;font-size:22px'>🏋️ WORKOUT</span>")
        text = text.replace("Warm-up","<span style='color:#ffb347;font-weight:bold'>🔥 Warm-up</span>")
        text = text.replace("Cool-down","<span style='color:#ffb347;font-weight:bold'>🧘 Cool-down</span>")
        return text

    if st.sidebar.button("Generate Plan"):

        with st.spinner("Building your AI fitness strategy..."):

            result = get_full_health_plan(name, age, weight, height, activity, diet, goal)
            styled = f"<div class='plan-text'>{format_plan(result)}</div>"

            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown(styled, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


elif st.session_state.page == "chat":

    st.markdown('<div class="section-title">AI Fitness Coach</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask about fitness, diet, workouts...")

    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        response = generate_ai_response(user_input)

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role":"assistant","content":response})


st.markdown("""
<div class="footer">
AI Fitness Intelligence • Smart Training • Smart Nutrition • Better Health
</div>
""", unsafe_allow_html=True)