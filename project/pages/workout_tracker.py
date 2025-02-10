import streamlit as st
from utils.helpers import load_exercise_library, recommend_workout
from utils.visualization import create_workout_summary
import pandas as pd

st.title("💪 Workout Tracker")

# Load exercise library
exercise_lib = load_exercise_library()

# Workout Planner Section
st.header("Workout Planner")

col1, col2 = st.columns(2)

with col1:
    fitness_goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "General Fitness"])
    fitness_level = st.selectbox("Fitness Level", ["beginner", "intermediate", "advanced"])
    workout_location = st.selectbox("Location", ["Gym", "Home"])

with col2:
    st.image("https://images.unsplash.com/photo-1517130038641-a774d04afb3c", caption="Workout Planning")

# Generate workout recommendation
if st.button("Get Workout Plan"):
    workout = recommend_workout(fitness_goal, fitness_level, exercise_lib)
    
    if workout:
        st.subheader("Your Workout Plan")
        st.markdown(f"""
        <div class="workout-card">
            <h4>{workout['name']}</h4>
            <p>Duration: {workout['duration']} minutes</p>
            <p>Difficulty: {workout['difficulty']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        for exercise_id in workout['exercises']:
            exercise = next(e for e in exercise_lib['exercises'] if e['id'] == exercise_id)
            st.markdown(f"""
            <div class="workout-card">
                <h4>{exercise['name']}</h4>
                <p>Muscle Group: {exercise['muscle_group']}</p>
                <p>Instructions:</p>
                <p>{exercise['instructions']}</p>
            </div>
            """, unsafe_allow_html=True)

# Exercise Library
st.header("Exercise Library")
search_term = st.text_input("Search Exercises")

filtered_exercises = [
    exercise for exercise in exercise_lib['exercises']
    if search_term.lower() in exercise['name'].lower()
] if search_term else exercise_lib['exercises']

for exercise in filtered_exercises:
    st.markdown(f"""
    <div class="workout-card">
        <h4>{exercise['name']}</h4>
        <p>Category: {exercise['category']}</p>
        <p>Muscle Group: {exercise['muscle_group']}</p>
        <p>Difficulty: {exercise['difficulty']}</p>
        <p>Instructions:</p>
        <p>{exercise['instructions']}</p>
    </div>
    """, unsafe_allow_html=True)

# Workout Tracking
st.header("Track Your Workout")
if st.button("Start Tracking"):
    st.session_state['tracking'] = True
    st.session_state['exercises_done'] = []

if 'tracking' in st.session_state and st.session_state['tracking']:
    exercise = st.selectbox("Select Exercise", [e['name'] for e in exercise_lib['exercises']])
    sets = st.number_input("Number of Sets", 1, 10, 3)
    reps = st.number_input("Number of Reps", 1, 50, 12)
    
    if st.button("Log Exercise"):
        st.session_state['exercises_done'].append({
            'exercise': exercise,
            'sets': sets,
            'reps': reps
        })
        
    if st.session_state['exercises_done']:
        workout_df = pd.DataFrame(st.session_state['exercises_done'])
        st.plotly_chart(create_workout_summary(workout_df))
