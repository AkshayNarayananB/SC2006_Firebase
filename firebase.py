# pip  install firebase-admin
import firebase_admin
from firebase_admin import credentials, firestore
import ollama_text

def  writeBack(uid, home_desc, outdoor_desc, gym_desc):
    
    workout_ref = db.collection('workoutPlan').document(uid)
    doc = workout_ref.get()
    if doc.exists:
        workout_ref.update({
            'gymDesc': gym_desc,
            'homeDesc': home_desc,
            'outdoorDesc': outdoor_desc,
            'completed': False,
            'selectedWorkout': None
        })
        print(f"Document for UID {uid} updated successfully.")
    else:
        # Document doesn't exist, create new document
        workout_ref.set({
            'gymDesc': gym_desc,
            'homeDesc': home_desc,
            'outdoorDesc': outdoor_desc,
            'completed': False,
            'selectedWorkout': None
        })
        print(f"Document for UID {uid} created successfully.")



cred = credentials.Certificate('C:\\Users\\Narayanakshay\\FBCred.json')
firebase_admin.initialize_app(cred)

#client
db = firestore.client()

uid_data = {}
#uid = []

#Get all userProfile documents to get the direct information of all users for prompt - duration/goals/healthconditions
userprofile_docs = db.collection('userProfile').stream()

for userprofile_doc in userprofile_docs:
    user_data = userprofile_doc.to_dict()
    uid = user_data.get('uid') # Get UID from document

    if(uid):
      # Concatenate fitness goals, fitness level, health conditions, and workout duration
      fitness_goals_str = ', '.join(user_data.get('fitnessGoals', []))  # Concatenate all fitness goals
      fitness_level = user_data.get('fitnessLevel', '')
      health_conditions = ', '.join(user_data.get('healthConditions', [])) if user_data.get('healthConditions') else ''
      workout_duration = user_data.get('workoutDuration', '')
      workout_frequency = user_data.get('workoutFrequency', '')
      workout_types = user_data.get('workoutTypes', [])

        # Handle case where workoutTypes is a single value or null
      if isinstance(workout_types, list) and workout_types:
      	workout_types_str = ', '.join(workout_types)  # Concatenate list of workout types
      elif isinstance(workout_types, str):  # Single value case
        workout_types_str = workout_types
      else:  # Case where workoutTypes is null or empty
        workout_types_str = 'None'
     
      # Concatenated string to send directly to deepseek
      concatenated_str = f"Fitness goals: {fitness_goals_str}, Fitness level: {fitness_level}, Health Issues: {health_conditions}, Workout Duration: {workout_duration}, {workout_frequency} times a week, mostly {workout_types_str}"

      # Store in dictionary
      uid_data[uid] = concatenated_str
    else:
      continue

#Get the previous workout for all the users whose uid has been recorded in uid_data
completed_workout_docs = db.collection('completedWorkout').stream()

for workout_doc in completed_workout_docs:
    workout_data = workout_doc.to_dict()
    workout_uid = workout_data.get('userId')
    if workout_uid in uid_data:
        workout_details_str = ""
        for exercise in workout_data.get('exercises', []):
            exercise_name = exercise.get('name', '')
            exercise_duration = exercise.get('duration', '')
            workout_details_str += f"{exercise_name} ({exercise_duration}), "
        # Trailing comma and space if any
        workout_details_str = workout_details_str.rstrip(', ')
        uid_data[workout_uid] += f", Previous Workout: {workout_details_str}"

# Sample printing function to check data fetching before sending to deepseek
for uid, concatenated_str in uid_data.items():
    response = ollama_text.generate_workout_plan(concatenated_str)
    home = response[0]
    outdoor = response[1]
    gym = response[2]
    writeBack(uid,home,outdoor,gym)
    #print(f"UID: {uid}, Data: {concatenated_str}")




