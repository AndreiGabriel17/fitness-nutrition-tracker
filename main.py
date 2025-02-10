import streamlit as st
import pandas as pd
import os
import importlib.util
from utils.helpers import load_food_database, load_exercise_library
from utils.visualization import create_macro_pie_chart

st.set_page_config(
    page_title="Fitness & Nutrition Tracker",
    page_icon="🏋️‍♂️",
    layout="wide"
)

# Initialize session state for page if not set
if 'page' not in st.session_state:
    st.session_state['page'] = "Home"

def set_page(page_name):
    st.session_state['page'] = page_name

# Sidebar Navigation
st.sidebar.markdown("<div class='sidebar-buttons'>", unsafe_allow_html=True)
st.sidebar.button("Home", on_click=set_page, args=("Home",))
st.sidebar.button("Meal Planner", on_click=set_page, args=("Meal Planner",))
st.sidebar.button("Workout Tracker", on_click=set_page, args=("Workout Tracker",))
st.sidebar.button("Profile", on_click=set_page, args=("Profile",))
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Load custom CSS from style.css
with open('styles/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state for user profile
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
page = st.session_state['page']

# Function to dynamically load pages from ./pages/ directory
def load_page(page_name):
    page_path = f"pages/{page_name.lower().replace(' ', '_')}.py"
    if os.path.exists(page_path):
        spec = importlib.util.spec_from_file_location("page_module", page_path)
        page_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(page_module)
        return page_module
    return None

if page == "Home":
    st.title("🏋️‍♂️ Fitness & Nutrition Tracker")
    st.header("Dashboard Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔥 Daily Calories", "2000 kcal")
        st.progress(0.7)
    with col2:
        st.metric("💪 Protein Goal", "150g")
        st.progress(0.6)
    with col3:
        st.metric("🏋️ Workouts This Week", "3/5")
        st.progress(0.8)

    st.header("Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        st.button("🍽️ Log Meal", key="log_meal", help="Track your daily meals")
    with col2:
        st.button("🏃‍♂️ Start Workout", key="start_workout", help="Start a new workout session")

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
    date_range = st.slider("Select Date Range", 1, 10, (1, 10))
    progress_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'weight': [80, 79.5, 79.2, 78.8, 78.5, 78.2, 77.9, 77.7, 77.5, 77.3]
    })
    st.line_chart(progress_data.set_index('date').iloc[date_range[0]-1:date_range[1]])
    
else:
    page_module = load_page(page)
    if page_module:
        page_module.run()
    else:
        st.error("Page not found.")

st.markdown("---\nCreated with ❤️ for your fitness journey")
