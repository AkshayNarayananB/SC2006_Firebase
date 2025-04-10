import ollama
import datetime
import re

format = """
Warm Up
Warmup Exercise Name
Warmup Exercise Name
Warmup Exercise Name

Workout
Exercise Name | Reps OR Duration | Targeted Muscle
Exercise Name | Reps OR Duration | Targeted Muscle
Exercise Name | Reps OR Duration | Targeted Muscle
Exercise Name | Reps OR Duration | Targeted Muscle
Exercise Name | Reps OR Duration | Targeted Muscle
[Include more workouts here depending on entire workout duration]
"""
# Define the model
MODEL_NAME = "deepseek-r1:1.5b"
abc = 0
def extract_text_after_think_tag(response):
    # Find the position of the </think> tag
    think_end_index = response.find('</think>')
    
    if think_end_index != -1:
        # Extract everything after the </think> tag
        return response[think_end_index + len('</think>'):].strip()
    else:
        return "No </think> tag found in the response."


# Function to send a query to DeepSeek
def query_deepseek(prompt):
    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']


# Function to send a query to DeepSeek
def generate_workout_plan(user_data_str):
    # Construct the prompt dynamically
    prompt = (
    f"{user_data_str}. Generate today's workout plan. "
    f"Create 3 variations: Home, Outdoor, and Gym workouts. "
    f"STRICT FORMAT:\n"
    f"Only use these exact headings: '#### Home', '#### Outdoor', '#### Gym'. "
    f"Under each heading, ONLY list exercises in this style:\n"
    f"Exercise Name - sets x reps OR duration\n\n"
    f"NO extra headings, NO extra descriptions, NO comments, NO explanations."
    f"NO summaries, NO motivational text. "
    f"ABSOLUTELY NO TEXT OUTSIDE THE FORMAT. Can include more exercises depending on duration\n\n"
    f"EXAMPLE FORMAT:\n"
    f"#### Home\n"
    f"Push-Ups - 3 sets x 15 reps\n"
    f"Squats - 3 sets x 20 reps\n"
    f"#### Outdoor\n"
    f"Jogging - 20 minutes\n"
    f"Pull-ups - 3 sets x 8 reps\n"
    f"#### Gym\n"
    f"Bench Press - 4 sets x 10 reps\n"
    f"Deadlifts - 4 sets x 6 reps"
    )
    
    # Query deepseek model
    print(datetime.datetime.now())
    response = extract_text_after_think_tag(query_deepseek(prompt))
    rep = response.split("####")
    print(response)
    try:
        home = rep[1]
        outdoor = rep[2]
        gym = rep[3]
    except:
        print("Entering except")
        if(abc==5):
            print("Plan Generation Timed Out")
        else:
            print("Going into loop")
            generate_workout_plan(user_data_str)
    print("DeepSeek Response:\n")
    print("home", home)
    print("outdoor",outdoor)
    print("gym",gym)
    print(datetime.datetime.now())
    print()
    return(home,outdoor,gym)
