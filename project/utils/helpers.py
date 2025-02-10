import json
import pandas as pd
from pathlib import Path

def load_food_database():
    with open('data/food_database.json', 'r') as f:
        return json.load(f)

def load_exercise_library():
    with open('data/exercise_library.json', 'r') as f:
        return json.load(f)

def calculate_bmi(weight, height):
    """Calculate BMI given weight in kg and height in cm."""
    if height <= 0 or weight <= 0:
        return 0
    height_m = height / 100  # Convert cm to m
    bmi = weight / (height_m * height_m)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Return BMI category based on value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_daily_calories(weight, height, age, gender, activity_level, goal):
    """
    Calculate recommended daily calories based on user data and goals.
    Activity levels: sedentary, light, moderate, very_active
    Goals: weight_loss, maintenance, muscle_gain
    """
    # Calculate BMR using Mifflin-St Jeor Equation
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Activity multiplier
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'very_active': 1.725
    }

    tdee = bmr * activity_multipliers.get(activity_level, 1.2)

    # Adjust based on goal
    if goal == 'weight_loss':
        return int(tdee - 500)  # 500 calorie deficit
    elif goal == 'muscle_gain':
        return int(tdee + 300)  # 300 calorie surplus
    else:
        return int(tdee)  # Maintenance

def calculate_macros(foods, portions):
    total_calories = sum(food['calories'] * portion for food, portion in zip(foods, portions))
    total_protein = sum(food['protein'] * portion for food, portion in zip(foods, portions))
    total_carbs = sum(food['carbs'] * portion for food, portion in zip(foods, portions))
    total_fat = sum(food['fat'] * portion for food, portion in zip(foods, portions))

    return {
        'calories': total_calories,
        'protein': total_protein,
        'carbs': total_carbs,
        'fat': total_fat
    }

def generate_meal_plan(target_calories, food_database):
    # Simple meal plan generation based on target calories
    foods = food_database['foods']
    meals = []

    # Basic algorithm to select foods that match target calories
    remaining_calories = target_calories
    while remaining_calories > 0 and len(meals) < 3:
        for food in foods:
            if food['calories'] <= remaining_calories:
                meals.append(food)
                remaining_calories -= food['calories']
                break

    return meals

def recommend_workout(goal, fitness_level, exercise_library):
    exercises = exercise_library['exercises']
    workouts = exercise_library['workouts']

    # Filter workouts based on difficulty and goal
    suitable_workouts = [
        workout for workout in workouts 
        if workout['difficulty'] == fitness_level
    ]

    return suitable_workouts[0] if suitable_workouts else None