import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=API_KEY)


MODEL_NAME = "llama-3.1-8b-instant"



def generate_ai_response(prompt: str):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional fitness and nutrition expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"



def get_meal_plan(age, weight, height, activity_level, dietary_preference, fitness_goal):
    prompt = f"""
Create a personalized meal plan.

User:
Age: {age}
Weight: {weight} kg
Height: {height} cm
Activity Level: {activity_level}
Diet Type: {dietary_preference}
Goal: {fitness_goal}

Include:
- Breakfast, Lunch, Dinner, Snacks
- Nutrition breakdown
- Hydration advice
- Meal prep tips
"""
    return generate_ai_response(prompt)



def get_fitness_plan(age, weight, height, activity_level, fitness_goal):
    prompt = f"""
Create a workout plan.

User:
Age: {age}
Weight: {weight} kg
Height: {height} cm
Activity Level: {activity_level}
Goal: {fitness_goal}

Include:
- Warm-up
- Main workout
- Cool-down
- Safety tips
"""
    return generate_ai_response(prompt)



def get_full_health_plan(name, age, weight, height, activity_level, dietary_preference, fitness_goal):
    meal = get_meal_plan(age, weight, height, activity_level, dietary_preference, fitness_goal)
    workout = get_fitness_plan(age, weight, height, activity_level, fitness_goal)

    final_prompt = f"""
Create a holistic health strategy.

User Name: {name}

MEAL PLAN:
{meal}

WORKOUT PLAN:
{workout}

Combine both into one structured plan with lifestyle advice.
"""

    return generate_ai_response(final_prompt)