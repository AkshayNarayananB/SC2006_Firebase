import ollama
import datetime
import re

format = """
Home Workout Variation
Warm-Up Section (Duration: [warm_up_duration_home] minutes)


[exercise_name_1] – Duration: [duration_1] minutes – Target Muscle Group: [target_muscle_group_1]
[exercise_name_2] – Duration: [duration_2] minutes – Target Muscle Group: [target_muscle_group_2]
[exercise_name_3] – Duration: [duration_3] minutes – Target Muscle Group: [target_muscle_group_3]
[exercise_name_4] – Duration: [duration_4] minutes – Target Muscle Group: [target_muscle_group_4]
[exercise_name_5] – Duration: [duration_5] minutes – Target Muscle Group: [target_muscle_group_5]
Main Workout Section (Duration: [main_workout_duration_home] minutes)


[exercise_name_1] – Sets: [sets_1], Reps: [reps_1], Rest: [rest_time_1] seconds – Target Muscle Group: [target_muscle_group_1]
[exercise_name_2] – Sets: [sets_2], Reps: [reps_2], Rest: [rest_time_2] seconds – Target Muscle Group: [target_muscle_group_2]
[exercise_name_3] – Sets: [sets_3], Reps: [reps_3], Rest: [rest_time_3] seconds – Target Muscle Group: [target_muscle_group_3]
[exercise_name_4] – Sets: [sets_4], Reps: [reps_4], Rest: [rest_time_4] seconds – Target Muscle Group: [target_muscle_group_4]
[exercise_name_5] – Sets: [sets_5], Reps: [reps_5], Rest: [rest_time_5] seconds – Target Muscle Group: [target_muscle_group_5]
Cool-Down Section (Duration: [cool_down_duration_home] minutes)


[exercise_name_1] – Duration: [duration_1] minutes – Target Muscle Group: [target_muscle_group_1]
[exercise_name_2] – Duration: [duration_2] minutes – Target Muscle Group: [target_muscle_group_2]
[exercise_name_3] – Duration: [duration_3] minutes – Target Muscle Group: [target_muscle_group_3]
[exercise_name_4] – Duration: [duration_4] minutes – Target Muscle Group: [target_muscle_group_4]
[exercise_name_5] – Duration: [duration_5] minutes – Target Muscle Group: [target_muscle_group_5]
Total Duration: [total_duration_home] minutes


Equipment Needed: [equipment_needed_home] (e.g., Dumbbells, Resistance Bands, None)



Outdoor Workout Variation
Warm-Up Section (Duration: [warm_up_duration_outdoor] minutes)


[exercise_name_1] – Duration: [duration_1] minutes – Target Muscle Group: [target_muscle_group_1]
[exercise_name_2] – Duration: [duration_2] minutes – Target Muscle Group: [target_muscle_group_2]
[exercise_name_3] – Duration: [duration_3] minutes – Target Muscle Group: [target_muscle_group_3]
[exercise_name_4] – Duration: [duration_4] minutes – Target Muscle Group: [target_muscle_group_4]
[exercise_name_5] – Duration: [duration_5] minutes – Target Muscle Group: [target_muscle_group_5]
Main Workout Section (Duration: [main_workout_duration_outdoor] minutes)


[exercise_name_1] – Sets: [sets_1], Reps: [reps_1], Rest: [rest_time_1] seconds – Target Muscle Group: [target_muscle_group_1]
[exercise_name_2] – Sets: [sets_2], Reps: [reps_2], Rest: [rest_time_2] seconds – Target Muscle Group: [target_muscle_group_2]
[exercise_name_3] – Sets: [sets_3], Reps: [reps_3], Rest: [rest_time_3] seconds – Target Muscle Group: [target_muscle_group_3]
[exercise_name_4] – Sets: [sets_4], Reps: [reps_4], Rest: [rest_time_4] seconds – Target Muscle Group: [target_muscle_group_4]
[exercise_name_5] – Sets: [sets_5], Reps: [reps_5], Rest: [rest_time_5] seconds – Target Muscle Group: [target_muscle_group_5]
Cool-Down Section (Duration: [cool_down_duration_outdoor] minutes)


[exercise_name_1] – Duration: [duration_1] minutes – Target Muscle Group: [target_muscle_group_1]
[exercise_name_2] – Duration: [duration_2] minutes – Target Muscle Group: [target_muscle_group_2]
[exercise_name_3] – Duration: [duration_3] minutes – Target Muscle Group: [target_muscle_group_3]
[exercise_name_4] – Duration: [duration_4] minutes – Target Muscle Group: [target_muscle_group_4]
[exercise_name_5] – Duration: [duration_5] minutes – Target Muscle Group: [target_muscle_group_5]
Total Duration: [total_duration_outdoor] minutes


Equipment Needed: [equipment_needed_outdoor] (e.g., None, Resistance Bands)



Gym Workout Variation
Warm-Up Section (Duration: [warm_up_duration_gym] minutes)


[exercise_name_1] – Duration: [duration_1] minutes – Target Muscle Group: [target_muscle_group_1]
[exercise_name_2] – Duration: [duration_2] minutes – Target Muscle Group: [target_muscle_group_2]
[exercise_name_3] – Duration: [duration_3] minutes – Target Muscle Group: [target_muscle_group_3]
[exercise_name_4] – Duration: [duration_4] minutes – Target Muscle Group: [target_muscle_group_4]
[exercise_name_5] – Duration: [duration_5] minutes – Target Muscle Group: [target_muscle_group_5]
Main Workout Section (Duration: [main_workout_duration_gym] minutes)


[exercise_name_1] – Sets: [sets_1], Reps: [reps_1], Rest: [rest_time_1] seconds – Target Muscle Group: [target_muscle_group_1]
[exercise_name_2] – Sets: [sets_2], Reps: [reps_2], Rest: [rest_time_2] seconds – Target Muscle Group: [target_muscle_group_2]
[exercise_name_3] – Sets: [sets_3], Reps: [reps_3], Rest: [rest_time_3] seconds – Target Muscle Group: [target_muscle_group_3]
[exercise_name_4] – Sets: [sets_4], Reps: [reps_4], Rest: [rest_time_4] seconds – Target Muscle Group: [target_muscle_group_4]
[exercise_name_5] – Sets: [sets_5], Reps: [reps_5], Rest: [rest_time_5] seconds – Target Muscle Group: [target_muscle_group_5]
Cool-Down Section (Duration: [cool_down_duration_gym] minutes)


[exercise_name_1] – Duration: [duration_1] minutes – Target Muscle Group: [target_muscle_group_1]
[exercise_name_2] – Duration: [duration_2] minutes – Target Muscle Group: [target_muscle_group_2]
[exercise_name_3] – Duration: [duration_3] minutes – Target Muscle Group: [target_muscle_group_3]
[exercise_name_4] – Duration: [duration_4] minutes – Target Muscle Group: [target_muscle_group_4]
[exercise_name_5] – Duration: [duration_5] minutes – Target Muscle Group: [target_muscle_group_5]
Total Duration: [total_duration_gym] minutes


Equipment Needed: [equipment_needed_gym] (e.g., Dumbbells, Machines, Kettlebells)
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
        f"{user_data_str}. Generate workout for today. Include 3 variations of the plans: Home, Outdoor, and Gym workouts. "
        f"Separate out the home,outdoor,gym workout by using identical '######' tag. Make sure plan suits the duration and goal requirements. Only give proper exercise name and set/duration info no objective stuff. DO NOT SUMMARIZE PROMPT IN RESPONSE. Every variation i.e., Home, Gym , Outdoor should start with the word 'Variation.' Use this format {format}")
    
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
