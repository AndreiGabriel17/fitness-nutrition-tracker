import streamlit as st
import pandas as pd
from utils.helpers import load_food_database, load_exercise_library
from utils.visualization import create_macro_pie_chart

st.set_page_config(
    page_title="Fitness & Nutrition Tracker",
    page_icon="🏋️‍♂️",
    layout="wide"
)

# Load custom CSS
with open('styles/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state with valid default values
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': '',
        'age': 30,  # Default age set to 30
        'weight': 70.0,  # Default weight in kg
        'height': 170,  # Default height in cm
        'gender': 'Male',
        'activity_level': 'moderate',
        'goal': 'weight_loss'
    }

# Main page header
st.title("🏋️‍♂️ Fitness & Nutrition Tracker")

# Dashboard layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>Daily Calories</h3>
        <p>2000 kcal</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>Protein Goal</h3>
        <p>150g</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>Workouts This Week</h3>
        <p>3/5</p>
    </div>
    """, unsafe_allow_html=True)

# Quick Actions
st.header("Quick Actions")
quick_actions = st.columns(2)

with quick_actions[0]:
    if st.button("Log Meal"):
        st.session_state['current_page'] = 'meal_logger'

with quick_actions[1]:
    if st.button("Start Workout"):
        st.session_state['current_page'] = 'workout_tracker'

# Featured Content
st.header("Featured Content")
featured_cols = st.columns(2)

with featured_cols[0]:
    st.subheader("Today's Recommended Meal")
    st.image("https://images.unsplash.com/photo-1598002041532-459c3549b714", 
             caption="Healthy Chicken Bowl")
    st.markdown("""
    * Grilled Chicken Breast
    * Brown Rice
    * Steamed Broccoli
    """)

with featured_cols[1]:
    st.subheader("Workout of the Day")
    st.image("https://images.unsplash.com/photo-1518611012118-696072aa579a",
             caption="Full Body Workout")
    st.markdown("""
    * 3x10 Push-ups
    * 3x12 Squats
    * 3x10 Dumbbell Rows
    """)

# Progress Section
st.header("Your Progress")
progress_data = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=10),
    'weight': [80, 79.5, 79.2, 78.8, 78.5, 78.2, 77.9, 77.7, 77.5, 77.3]
})

st.line_chart(progress_data.set_index('date'))

# Footer
st.markdown("""
---
Created with ❤️ for your fitness journey
""")