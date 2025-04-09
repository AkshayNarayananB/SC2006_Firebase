import ollama
import datetime
import re

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
        f"{user_data_str}. Generate workout for today. Include 3 variations of the plans: Home, Outdoor, and Gym workouts. "
        f"Separate out the home,outdoor,gym workout by using identical '######' tag.'Make sure plan suits the duration and goal requirements. Only give proper exercise name and set/duration info no objective stuff. DO NOT SUMMARIZE PROMPT IN RESPONSE. Every variation i.e., Home, Gym , Outdoor should start with the word 'Variation.'")
    
    # Query deepseek model
    print(datetime.datetime.now())
    response = extract_text_after_think_tag(query_deepseek(prompt)).split("Variation")
    try:
        home = response[1]
        outdoor = response[2]
        gym = response[3]
    except:
        print("Entering except")
        if(abc==5):
            print("Plan Generation Timed Out")
        else:
            abc+=1
            generate_workout_plan(user_data_str)
    print("DeepSeek Response:\n")
    print("home", home)
    print("outdoor",outdoor)
    print("gym",gym)
    print(datetime.datetime.now())
    print()
    return(home,outdoor,gym)
