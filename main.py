import streamlit as st
import pandas as pd
from utils.helpers import load_food_database, load_exercise_library
from utils.visualization import create_macro_pie_chart

st.set_page_config(
    page_title="Fitness & Nutrition Tracker",
    page_icon="🏋️‍♂️",
    layout="wide"
)

# Hide Streamlit's default navigation
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.session_state['page'] = "Home"
elif st.sidebar.button("Meal Planner"):
    st.session_state['page'] = "Meal Planner"
elif st.sidebar.button("Workout Tracker"):
    st.session_state['page'] = "Workout Tracker"
elif st.sidebar.button("Profile"):
    st.session_state['page'] = "Profile"

# Load custom CSS
with open('styles/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': '',
        'age': 30,
        'weight': 70.0,
        'height': 170,
        'gender': 'Male',
        'activity_level': 'moderate',
        'goal': 'weight_loss'
    }

# Handle Navigation
page = st.session_state.get('page', "Home")

if page == "Home":
    st.title("🏋️‍♂️ Fitness & Nutrition Tracker")
    st.header("Dashboard Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Daily Calories", "2000 kcal")
    with col2:
        st.metric("Protein Goal", "150g")
    with col3:
        st.metric("Workouts This Week", "3/5")

    st.header("Quick Actions")
    if st.button("Log Meal"): st.session_state['current_page'] = 'meal_logger'
    if st.button("Start Workout"): st.session_state['current_page'] = 'workout_tracker'

    st.header("Featured Content")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Today's Recommended Meal")
        st.image("https://images.unsplash.com/photo-1598002041532-459c3549b714", caption="Healthy Chicken Bowl")
        st.markdown("* Grilled Chicken Breast\n* Brown Rice\n* Steamed Broccoli")
    with col2:
        st.subheader("Workout of the Day")
        st.image("https://images.unsplash.com/photo-1518611012118-696072aa579a", caption="Full Body Workout")
        st.markdown("* 3x10 Push-ups\n* 3x12 Squats\n* 3x10 Dumbbell Rows")

    st.header("Your Progress")
    progress_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'weight': [80, 79.5, 79.2, 78.8, 78.5, 78.2, 77.9, 77.7, 77.5, 77.3]
    })
    st.line_chart(progress_data.set_index('date'))
    
elif page == "Meal Planner":
    st.title("🍽️ Meal Planner")
    st.write("Plan your meals based on your goals and available ingredients.")
    # Add meal planning functionalities here

elif page == "Workout Tracker":
    st.title("💪 Workout Tracker")
    st.write("Track your workouts and monitor progress.")
    # Add workout tracking functionalities here

elif page == "Profile":
    st.title("👤 Profile Settings")
    st.write("Manage your personal information and fitness goals.")
    # Add profile management functionalities here

st.markdown("---\nCreated with ❤️ for your fitness journey")
