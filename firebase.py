# pip  install firebase-admin
import firebase_admin
from firebase_admin import credentials, firestore

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
      workout_types = ', '.join(user_data.get('workoutTypes', []))
     
      # Concatenated string to send directly to deepseek
      concatenated_str = f"Fitness goals: {fitness_goals_str}, Fitness level: {fitness_level}, Health Issues: {health_conditions}, Workout Duration: {workout_duration}, {workout_frequency} times a week, mostly {workout_types}"

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
    print(f"UID: {uid}, Data: {concatenated_str}")




