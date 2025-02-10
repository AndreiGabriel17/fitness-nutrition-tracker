import streamlit as st
from utils.helpers import load_food_database, calculate_macros, generate_meal_plan
from utils.visualization import create_macro_pie_chart

st.title("🥗 Meal Planner")

# Load food database
food_db = load_food_database()

# Sidebar for settings
st.sidebar.header("Meal Plan Settings")
target_calories = st.sidebar.number_input("🎯 Target Calories", min_value=1200, max_value=5000, value=2000, key="target_cal")
dietary_preference = st.sidebar.selectbox("🥦 Dietary Preference", ["None", "Vegetarian", "Vegan", "Keto"], key="diet_pref")

# Meal Plan Section
st.header("📌 Create Your Meal Plan")

# Generate meal plan
if st.button("Generate Meal Plan"):
    meal_plan = generate_meal_plan(target_calories, food_db)

    st.subheader("🍽️ Your Meal Plan")
    for i, meal in enumerate(meal_plan, 1):
        with st.expander(f"Meal {i}: {meal['name']}"):
            st.write(f"**Calories:** {meal['calories']} kcal")
            st.write(f"**Protein:** {meal['protein']}g | **Carbs:** {meal['carbs']}g | **Fat:** {meal['fat']}g")

# Food Database Browser
st.header("📜 Food Database")
search_term = st.text_input("🔎 Search Foods", key="food_search")

filtered_foods = [
    food for food in food_db['foods']
    if search_term.lower() in food['name'].lower()
] if search_term else food_db['foods']

# Display food database as a table
if filtered_foods:
    st.dataframe(filtered_foods)
else:
    st.write("⚠️ No foods found. Try a different search term.")

# Recipe Suggestions
st.header("📌 Recipe Suggestions")
for recipe in food_db['recipes']:
    with st.expander(f"🍳 {recipe['name']}"):
        st.write(f"**Calories:** {recipe['calories']} kcal")
        st.write(f"**Protein:** {recipe['protein']}g | **Carbs:** {recipe['carbs']}g | **Fat:** {recipe['fat']}g")
        st.write(f"**Instructions:** {recipe['instructions']}")
