import streamlit as st
from utils.helpers import load_exercise_library, recommend_workout
from utils.visualization import create_workout_summary
import pandas as pd

st.title("💪 Workout Tracker")

# Load exercise library
exercise_lib = load_exercise_library()

# Sidebar Settings for Workout Plan
st.sidebar.header("Workout Preferences")
fitness_goal = st.sidebar.selectbox("🎯 Fitness Goal", ["Weight Loss", "Muscle Gain", "General Fitness"], key="workout_goal")
fitness_level = st.sidebar.selectbox("📈 Fitness Level", ["Beginner", "Intermediate", "Advanced"], key="workout_level")
workout_location = st.sidebar.selectbox("📍 Workout Location", ["Gym", "Home"], key="workout_location")

# Workout Planner Section
st.header("📌 Workout Planner")

# Generate workout recommendation
if st.button("🏋️‍♂️ Get Workout Plan"):
    workout = recommend_workout(fitness_goal, fitness_level, exercise_lib)
    
    if workout:
        with st.expander("📋 **Your Workout Plan**", expanded=True):
            st.markdown(f"### **{workout['name']}**")
            st.write(f"**Duration:** {workout['duration']} minutes")
            st.write(f"**Difficulty:** {workout['difficulty']}")

        for exercise_id in workout['exercises']:
            exercise = next(e for e in exercise_lib['exercises'] if e['id'] == exercise_id)
            with st.expander(f"🏋️ {exercise['name']} - {exercise['muscle_group']}"):
                st.write(f"**Category:** {exercise['category']}")
                st.write(f"**Difficulty:** {exercise['difficulty']}")
                st.write(f"**Instructions:** {exercise['instructions']}")

# Exercise Library
st.header("📖 Exercise Library")
exercise_names = [exercise['name'] for exercise in exercise_lib['exercises']]
search_exercise = st.selectbox("🔍 Search Exercises", ["All"] + exercise_names, key="search_exercise")

filtered_exercises = exercise_lib['exercises'] if search_exercise == "All" else [e for e in exercise_lib['exercises'] if e['name'] == search_exercise]

if filtered_exercises:
    for exercise in filtered_exercises:
        with st.expander(f"🏋️ {exercise['name']} - {exercise['muscle_group']}"):
            st.write(f"**Category:** {exercise['category']}")
            st.write(f"**Difficulty:** {exercise['difficulty']}")
            st.write(f"**Instructions:** {exercise['instructions']}")
else:
    st.warning("⚠️ No exercises found. Try a different search term.")

# Workout Tracking
st.header("📊 Track Your Workout")

if st.button("▶ Start Tracking"):
    st.session_state['tracking'] = True
    st.session_state['exercises_done'] = []

if 'tracking' in st.session_state and st.session_state['tracking']:
    selected_exercise = st.selectbox("🏋️ Select Exercise", [e['name'] for e in exercise_lib['exercises']], key="log_exercise")
    sets = st.number_input("🔄 Number of Sets", 1, 10, 3, key="log_sets")
    reps = st.number_input("🔢 Number of Reps", 1, 50, 12, key="log_reps")

    if st.button("📌 Log Exercise"):
        st.session_state['exercises_done'].append({
            'exercise': selected_exercise,
            'sets': sets,
            'reps': reps
        })
        st.success(f"✅ Logged {sets} sets of {reps} reps for {selected_exercise}")

    if st.session_state['exercises_done']:
        workout_df = pd.DataFrame(st.session_state['exercises_done'])
        st.subheader("📋 Logged Exercises")
        st.dataframe(workout_df)
        st.plotly_chart(create_workout_summary(workout_df))
