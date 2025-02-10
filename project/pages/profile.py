import streamlit as st
import pandas as pd
from utils.visualization import create_progress_chart
from utils.helpers import calculate_bmi, get_bmi_category, calculate_daily_calories

st.title("👤 User Profile")

# Profile Information
st.header("Personal Information")

col1, col2 = st.columns(2)

with col1:
    st.session_state.user_profile['name'] = st.text_input("Name", st.session_state.user_profile.get('name', ''))
    st.session_state.user_profile['age'] = st.number_input("Age", 18, 120, st.session_state.user_profile.get('age', 30))
    st.session_state.user_profile['weight'] = st.number_input("Weight (kg)", 30.0, 300.0, st.session_state.user_profile.get('weight', 70.0))
    st.session_state.user_profile['height'] = st.number_input("Height (cm)", 100, 250, st.session_state.user_profile.get('height', 170))
    st.session_state.user_profile['gender'] = st.selectbox("Gender", ["Male", "Female"], 
        index=0 if st.session_state.user_profile.get('gender', 'Male') == 'Male' else 1)
    st.session_state.user_profile['activity_level'] = st.select_slider(
        "Activity Level",
        options=['sedentary', 'light', 'moderate', 'very_active'],
        value=st.session_state.user_profile.get('activity_level', 'moderate'),
        help="Sedentary (office job), Light (1-2x/week), Moderate (3-5x/week), Very Active (6-7x/week)"
    )
    st.session_state.user_profile['goal'] = st.selectbox(
        "Fitness Goal", 
        ["weight_loss", "maintenance", "muscle_gain"],
        index=0 if not st.session_state.user_profile.get('goal') else ["weight_loss", "maintenance", "muscle_gain"].index(st.session_state.user_profile['goal'])
    )

with col2:
    # Calculate and display BMI
    if st.session_state.user_profile['weight'] > 0 and st.session_state.user_profile['height'] > 0:
        bmi = calculate_bmi(st.session_state.user_profile['weight'], st.session_state.user_profile['height'])
        bmi_category = get_bmi_category(bmi)

        st.markdown("""
        ### Your Body Metrics
        """)

        st.markdown(f"""
        <div class="metric-card">
            <h3>BMI: {bmi}</h3>
            <p>Category: {bmi_category}</p>
        </div>
        """, unsafe_allow_html=True)

        # Calculate and display recommended calories
        recommended_calories = calculate_daily_calories(
            st.session_state.user_profile['weight'],
            st.session_state.user_profile['height'],
            st.session_state.user_profile['age'],
            st.session_state.user_profile['gender'],
            st.session_state.user_profile['activity_level'],
            st.session_state.user_profile['goal']
        )

        st.markdown(f"""
        <div class="metric-card">
            <h3>Daily Calorie Target</h3>
            <p>{recommended_calories} kcal</p>
            <small>Based on your profile and goals</small>
        </div>
        """, unsafe_allow_html=True)

        # Macro breakdown
        protein_target = st.session_state.user_profile['weight'] * 2  # 2g per kg bodyweight
        fat_target = (recommended_calories * 0.25) / 9  # 25% of calories from fat
        carbs_target = (recommended_calories - (protein_target * 4) - (fat_target * 9)) / 4

        st.markdown(f"""
        <div class="metric-card">
            <h3>Recommended Macros</h3>
            <p>Protein: {int(protein_target)}g</p>
            <p>Carbs: {int(carbs_target)}g</p>
            <p>Fat: {int(fat_target)}g</p>
        </div>
        """, unsafe_allow_html=True)

    st.image("https://images.unsplash.com/photo-1518459031867-a89b944bffe4", caption="Your Fitness Journey")


# Progress Tracking
st.header("Progress Tracking")

# Mock progress data
progress_data = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=10),
    'weight': [80, 79.5, 79.2, 78.8, 78.5, 78.2, 77.9, 77.7, 77.5, 77.3]
})

st.plotly_chart(create_progress_chart(progress_data))

# Save Changes
if st.button("Save Changes"):
    st.success("Profile updated successfully!")

# Achievement Badges
st.header("Achievements")
achievements = st.columns(4)

with achievements[0]:
    st.markdown("""
    <div class="metric-card">
        <h4>🏃‍♂️ Getting Started</h4>
        <p>Completed first workout</p>
    </div>
    """, unsafe_allow_html=True)

with achievements[1]:
    st.markdown("""
    <div class="metric-card">
        <h4>🥗 Nutrition Pro</h4>
        <p>Logged meals for 7 days</p>
    </div>
    """, unsafe_allow_html=True)

with achievements[2]:
    st.markdown("""
    <div class="metric-card">
        <h4>💪 Workout Warrior</h4>
        <p>10 workouts completed</p>
    </div>
    """, unsafe_allow_html=True)

with achievements[3]:
    st.markdown("""
    <div class="metric-card">
        <h4>⭐ Goal Crusher</h4>
        <p>Reached first target</p>
    </div>
    """, unsafe_allow_html=True)