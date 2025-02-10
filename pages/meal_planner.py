import streamlit as st
from utils.helpers import load_food_database, calculate_macros, generate_meal_plan
from utils.visualization import create_macro_pie_chart

st.title("🥗 Meal Planner")

# Load food database
food_db = load_food_database()

# Meal Planning Section
st.header("Create Your Meal Plan")

col1, col2 = st.columns(2)

with col1:
    target_calories = st.number_input("Target Daily Calories", min_value=1200, max_value=5000, value=2000)
    dietary_preference = st.selectbox("Dietary Preference", ["None", "Vegetarian", "Vegan", "Keto"])

with col2:
    st.image("https://images.unsplash.com/photo-1551584277-a31a25e08fc8", caption="Healthy Meal Planning")

# Generate meal plan
if st.button("Generate Meal Plan"):
    meal_plan = generate_meal_plan(target_calories, food_db)
    
    st.subheader("Your Meal Plan")
    for i, meal in enumerate(meal_plan, 1):
        st.markdown(f"""
        <div class="meal-card">
            <h4>Meal {i}</h4>
            <p>{meal['name']}</p>
            <p>Calories: {meal['calories']} kcal</p>
            <p>Protein: {meal['protein']}g | Carbs: {meal['carbs']}g | Fat: {meal['fat']}g</p>
        </div>
        """, unsafe_allow_html=True)

# Food Database Browser
st.header("Food Database")
search_term = st.text_input("Search Foods")

filtered_foods = [
    food for food in food_db['foods']
    if search_term.lower() in food['name'].lower()
] if search_term else food_db['foods']

for food in filtered_foods:
    st.markdown(f"""
    <div class="meal-card">
        <h4>{food['name']}</h4>
        <p>Per {food['serving_size']}{food['unit']}:</p>
        <p>Calories: {food['calories']} kcal</p>
        <p>Protein: {food['protein']}g | Carbs: {food['carbs']}g | Fat: {food['fat']}g</p>
    </div>
    """, unsafe_allow_html=True)

# Recipe Suggestions
st.header("Recipe Suggestions")
for recipe in food_db['recipes']:
    st.markdown(f"""
    <div class="meal-card">
        <h4>{recipe['name']}</h4>
        <p>{recipe['instructions']}</p>
        <p>Calories: {recipe['calories']} kcal</p>
        <p>Protein: {recipe['protein']}g | Carbs: {recipe['carbs']}g | Fat: {recipe['fat']}g</p>
    </div>
    """, unsafe_allow_html=True)
