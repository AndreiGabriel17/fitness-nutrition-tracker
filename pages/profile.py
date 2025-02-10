import streamlit as st
import pandas as pd
from utils.visualization import create_progress_chart
from utils.helpers import calculate_bmi, get_bmi_category, calculate_daily_calories

st.title("👤 User Profile")

# Load Profile Data
profile = st.session_state.user_profile

# Sidebar for quick navigation
st.sidebar.header("Profile Settings")
profile["name"] = st.sidebar.text_input("👤 Name", profile.get("name", ""), key="profile_name")
profile["age"] = st.sidebar.number_input("🎂 Age", 18, 120, profile.get("age", 30), key="profile_age")
profile["weight"] = st.sidebar.number_input("⚖️ Weight (kg)", 30.0, 300.0, profile.get("weight", 70.0), key="profile_weight")
profile["height"] = st.sidebar.number_input("📏 Height (cm)", 100, 250, profile.get("height", 170), key="profile_height")
profile["gender"] = st.sidebar.selectbox("⚧ Gender", ["Male", "Female"], index=0 if profile.get("gender", "Male") == "Male" else 1, key="profile_gender")

profile["activity_level"] = st.sidebar.select_slider(
    "🏃‍♂️ Activity Level",
    options=['sedentary', 'light', 'moderate', 'very_active'],
    value=profile.get("activity_level", "moderate"),
    key="profile_activity"
)

profile["goal"] = st.sidebar.selectbox(
    "🎯 Fitness Goal",
    ["weight_loss", "maintenance", "muscle_gain"],
    index=["weight_loss", "maintenance", "muscle_gain"].index(profile.get("goal", "weight_loss")),
    key="profile_goal"
)

# Display BMI and Calories
with st.expander("📊 **Your Body Metrics**", expanded=True):
    if profile["weight"] > 0 and profile["height"] > 0:
        bmi = calculate_bmi(profile["weight"], profile["height"])
        bmi_category = get_bmi_category(bmi)

        st.metric("📏 BMI", f"{bmi:.1f}", help=f"Category: {bmi_category}")

        recommended_calories = calculate_daily_calories(
            profile["weight"], profile["height"], profile["age"],
            profile["gender"], profile["activity_level"], profile["goal"]
        )

        st.metric("🔥 Daily Calorie Target", f"{recommended_calories} kcal")

        # Macro breakdown
        protein_target = profile["weight"] * 2  # 2g per kg bodyweight
        fat_target = (recommended_calories * 0.25) / 9  # 25% of calories from fat
        carbs_target = (recommended_calories - (protein_target * 4) - (fat_target * 9)) / 4

        st.progress(protein_target / (recommended_calories / 4))
        st.write(f"**Protein:** {int(protein_target)}g")
        
        st.progress(carbs_target / (recommended_calories / 4))
        st.write(f"**Carbs:** {int(carbs_target)}g")
        
        st.progress(fat_target / (recommended_calories / 9))
        st.write(f"**Fat:** {int(fat_target)}g")

st.image("https://images.unsplash.com/photo-1518459031867-a89b944bffe4", caption="Your Fitness Journey")

# Progress Tracking
st.header("📈 Progress Tracking")

# Allow users to manually input their weight history
st.subheader("📊 Log Your Weight")
weight_date = st.date_input("📅 Select Date")
weight_value = st.number_input("⚖️ Enter Your Weight (kg)", 30.0, 300.0, profile["weight"], key="log_weight")

if st.button("Log Weight"):
    st.success(f"✅ Logged {weight_value} kg on {weight_date}!")

# Mock progress data
progress_data = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=10),
    'weight': [80, 79.5, 79.2, 78.8, 78.5, 78.2, 77.9, 77.7, 77.5, 77.3]
})

st.plotly_chart(create_progress_chart(progress_data))

# Save Changes
if st.button("💾 Save Profile Changes"):
    st.success("✅ Profile updated successfully!")

# Achievements Section
st.header("🏆 Achievements")
achievements = st.columns(4)

with achievements[0]:
    st.success("🏃‍♂️ Getting Started\n\nCompleted first workout!")

with achievements[1]:
    st.info("🥗 Nutrition Pro\n\nLogged meals for 7 days!")

with achievements[2]:
    st.warning("💪 Workout Warrior\n\n10 workouts completed!")

with achievements[3]:
    st.error("⭐ Goal Crusher\n\nReached first target!")
