"""
Create Final Comprehensive Dataset
Combines real API data with generated data to create an impressive, large-scale dataset
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path
from config import DATA_DIR

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def load_real_api_data():
    """Load the real data we fetched from APIs"""
    print("Loading real API data...")
    
    exercises_api = pd.read_csv(DATA_DIR / "exercises_comprehensive_api.csv")
    nutrition_api = pd.read_csv(DATA_DIR / "nutrition_comprehensive_api.csv")
    
    print(f"  Loaded {len(exercises_api)} real exercises")
    print(f"  Loaded {len(nutrition_api)} real nutrition items")
    
    return exercises_api, nutrition_api

def generate_members(count=2500):
    """Generate realistic member profiles"""
    print(f"\nGenerating {count} member profiles...")
    
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
                   'William', 'Barbara', 'David', 'Elizabeth', 'Richard', 'Susan', 'Joseph', 'Jessica',
                   'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
                   'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
                   'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                  'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
                  'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
                  'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson']
    
    membership_types = ['Basic', 'Premium', 'Elite', 'Student', 'Senior']
    goals = ['Weight Loss', 'Muscle Gain', 'General Fitness', 'Athletic Performance', 'Health Maintenance']
    
    members = []
    base_date = datetime(2020, 1, 1)
    
    for i in range(count):
        join_date = base_date + timedelta(days=random.randint(0, 1800))
        age = random.randint(18, 75)
        
        member = {
            'member_id': f'MEM{str(i+1).zfill(6)}',
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f'member{i+1}@email.com',
            'phone': f'+1-555-{random.randint(100,999)}-{random.randint(1000,9999)}',
            'date_of_birth': (datetime.now() - timedelta(days=age*365)).strftime('%Y-%m-%d'),
            'gender': random.choice(['Male', 'Female', 'Other']),
            'join_date': join_date.strftime('%Y-%m-%d'),
            'membership_type': random.choice(membership_types),
            'membership_status': random.choice(['Active', 'Active', 'Active', 'Inactive']),  # 75% active
            'fitness_goal': random.choice(goals),
            'height_cm': round(random.uniform(150, 200), 1),
            'weight_kg': round(random.uniform(50, 120), 1),
            'emergency_contact': f'+1-555-{random.randint(100,999)}-{random.randint(1000,9999)}'
        }
        members.append(member)
    
    df = pd.DataFrame(members)
    print(f"  Generated {len(df)} members")
    return df

def generate_workout_logs(members_df, exercises_df, count=15000):
    """Generate workout activity logs using real exercises"""
    print(f"\nGenerating {count} workout logs...")
    
    logs = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(count):
        member = members_df.sample(1).iloc[0]
        exercise = exercises_df.sample(1).iloc[0]
        workout_date = base_date + timedelta(days=random.randint(0, 350))
        
        sets = random.randint(2, 5)
        reps = random.randint(6, 20)
        weight = round(random.uniform(5, 150), 1) if exercise['type'] == 'strength' else 0
        duration = random.randint(15, 90)
        calories = round(duration * random.uniform(3, 8), 1)
        
        log = {
            'workout_log_id': f'WL{str(i+1).zfill(8)}',
            'member_id': member['member_id'],
            'workout_date': workout_date.strftime('%Y-%m-%d'),
            'workout_time': f'{random.randint(5,22):02d}:{random.randint(0,59):02d}:00',
            'exercise_name': exercise['name'],
            'exercise_type': exercise['type'],
            'muscle_group': exercise['muscle'],
            'sets_completed': sets,
            'reps_per_set': reps,
            'weight_kg': weight,
            'duration_minutes': duration,
            'calories_burned': calories,
            'intensity_level': random.choice(['Low', 'Moderate', 'High', 'Very High']),
            'notes': random.choice(['Great workout!', 'Felt strong', 'Good progress', 'Challenging', ''])
        }
        logs.append(log)
    
    df = pd.DataFrame(logs)
    print(f"  Generated {len(df)} workout logs")
    return df

def generate_nutrition_logs(members_df, nutrition_df, count=10000):
    """Generate nutrition tracking logs using real food data"""
    print(f"\nGenerating {count} nutrition logs...")
    
    logs = []
    base_date = datetime(2024, 1, 1)
    meal_types = ['Breakfast', 'Lunch', 'Dinner', 'Snack', 'Post-Workout']
    
    for i in range(count):
        member = members_df.sample(1).iloc[0]
        food = nutrition_df.sample(1).iloc[0]
        log_date = base_date + timedelta(days=random.randint(0, 350))
        
        serving_multiplier = round(random.uniform(0.5, 3.0), 1)
        
        log = {
            'nutrition_log_id': f'NL{str(i+1).zfill(8)}',
            'member_id': member['member_id'],
            'log_date': log_date.strftime('%Y-%m-%d'),
            'meal_type': random.choice(meal_types),
            'food_name': food['name'],
            'serving_size': f"{serving_multiplier * food.get('serving_size_g', 100)}g",
            'calories': round(food['calories'] * serving_multiplier, 1),
            'protein_g': round(food['protein_g'] * serving_multiplier, 1),
            'carbs_g': round(food['carbohydrates_total_g'] * serving_multiplier, 1),
            'fat_g': round(food['fat_total_g'] * serving_multiplier, 1),
            'fiber_g': round(food.get('fiber_g', 0) * serving_multiplier, 1),
            'sugar_g': round(food.get('sugar_g', 0) * serving_multiplier, 1)
        }
        logs.append(log)
    
    df = pd.DataFrame(logs)
    print(f"  Generated {len(df)} nutrition logs")
    return df

def generate_engagement_data(members_df, count=8000):
    """Generate member engagement and activity metrics"""
    print(f"\nGenerating {count} engagement records...")
    
    records = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(count):
        member = members_df.sample(1).iloc[0]
        record_date = base_date + timedelta(days=random.randint(0, 350))
        
        check_ins = random.randint(0, 30)
        app_logins = random.randint(0, 50)
        classes_attended = random.randint(0, 15)
        trainer_sessions = random.randint(0, 8)
        
        engagement_score = min(100, (check_ins * 2) + (app_logins * 0.5) + (classes_attended * 5) + (trainer_sessions * 10))
        
        record = {
            'engagement_id': f'ENG{str(i+1).zfill(8)}',
            'member_id': member['member_id'],
            'record_date': record_date.strftime('%Y-%m-%d'),
            'check_ins_count': check_ins,
            'app_logins_count': app_logins,
            'classes_attended': classes_attended,
            'trainer_sessions': trainer_sessions,
            'engagement_score': round(engagement_score, 1),
            'last_visit_date': (record_date - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
            'at_risk_flag': 'Yes' if engagement_score < 20 else 'No'
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    print(f"  Generated {len(df)} engagement records")
    return df

def main():
    print("\nCREATING FINAL COMPREHENSIVE DATASET")
    print("Combining real API data with scaled generated data")
    print("-" * 60)
    
    # Load real API data
    exercises_api, nutrition_api = load_real_api_data()
    
    # Generate scaled datasets
    members_df = generate_members(2500)
    workout_logs_df = generate_workout_logs(members_df, exercises_api, 15000)
    nutrition_logs_df = generate_nutrition_logs(members_df, nutrition_api, 10000)
    engagement_df = generate_engagement_data(members_df, 8000)
    
    # Save all datasets
    print("\nSaving final datasets...")
    members_df.to_csv(DATA_DIR / "members_final.csv", index=False)
    exercises_api.to_csv(DATA_DIR / "exercises_final.csv", index=False)
    nutrition_api.to_csv(DATA_DIR / "nutrition_final.csv", index=False)
    workout_logs_df.to_csv(DATA_DIR / "workout_logs_final.csv", index=False)
    nutrition_logs_df.to_csv(DATA_DIR / "nutrition_logs_final.csv", index=False)
    engagement_df.to_csv(DATA_DIR / "member_engagement_final.csv", index=False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("FINAL DATASET SUMMARY")
    print("=" * 60)
    print(f"\nReal API Data:")
    print(f"  Exercises: {len(exercises_api)} (100% from API Ninjas)")
    print(f"  Nutrition Items: {len(nutrition_api)} (100% from API Ninjas)")
    print(f"\nGenerated Data (using real API data):")
    print(f"  Members: {len(members_df)}")
    print(f"  Workout Logs: {len(workout_logs_df)}")
    print(f"  Nutrition Logs: {len(nutrition_logs_df)}")
    print(f"  Engagement Records: {len(engagement_df)}")
    print(f"\nTotal Records: {len(members_df) + len(exercises_api) + len(nutrition_api) + len(workout_logs_df) + len(nutrition_logs_df) + len(engagement_df)}")
    print("\nThis is a production-scale dataset perfect for showcasing to recruiters!")
    print("=" * 60)

if __name__ == "__main__":
    main()
