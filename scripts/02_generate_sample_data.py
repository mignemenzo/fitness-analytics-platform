"""
Health & Fitness Analytics Platform - Sample Data Generator
Author: Data Engineering Team
Date: December 2025

This script generates realistic sample data that mimics API responses
and creates simulated member activity data for the analytics platform.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


class SampleDataGenerator:
    """Generate realistic sample data for fitness analytics platform"""
    
    def __init__(self):
        self.output_dir = "/home/ubuntu/fitness_analytics_platform/data"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_exercises_data(self, n_exercises=100):
        """Generate sample exercises data matching API Ninjas structure"""
        print("\n📊 Generating sample exercises data...")
        
        muscle_groups = ["biceps", "triceps", "chest", "back", "legs", "shoulders", 
                        "abs", "glutes", "calves", "forearms", "quadriceps", "hamstrings"]
        
        exercise_types = ["strength", "cardio", "olympic_weightlifting", "plyometrics", 
                         "powerlifting", "stretching", "strongman"]
        
        difficulties = ["beginner", "intermediate", "expert"]
        
        equipment_options = [
            ["barbell"], ["dumbbell"], ["kettlebell"], ["bodyweight"], 
            ["cable"], ["machine"], ["resistance band"], ["medicine ball"],
            ["barbell", "bench"], ["dumbbell", "bench"], ["pull-up bar"],
            ["treadmill"], ["rowing machine"], ["stationary bike"]
        ]
        
        exercise_names = [
            "Barbell Bench Press", "Dumbbell Curl", "Squat", "Deadlift", "Pull-up",
            "Push-up", "Plank", "Lunges", "Leg Press", "Shoulder Press",
            "Lat Pulldown", "Tricep Dips", "Leg Curl", "Calf Raise", "Russian Twist",
            "Burpees", "Mountain Climbers", "Box Jumps", "Kettlebell Swing", "Rowing",
            "Bicycle Crunches", "Side Plank", "Hip Thrust", "Face Pull", "Arnold Press",
            "Hammer Curl", "Concentration Curl", "Preacher Curl", "Cable Fly", "Incline Press",
            "Decline Press", "Front Squat", "Bulgarian Split Squat", "Romanian Deadlift",
            "Sumo Deadlift", "Overhead Press", "Lateral Raise", "Front Raise", "Shrugs",
            "Upright Row", "Bent Over Row", "T-Bar Row", "Seated Row", "Chin-up",
            "Dumbbell Pullover", "Tricep Extension", "Skull Crushers", "Close-Grip Bench",
            "Diamond Push-ups", "Leg Extension", "Hack Squat", "Goblet Squat", "Wall Sit"
        ]
        
        # Extend exercise names to reach desired count
        while len(exercise_names) < n_exercises:
            base_name = random.choice(exercise_names[:20])
            modifier = random.choice(["Incline", "Decline", "Seated", "Standing", 
                                     "Single-Arm", "Alternating", "Wide-Grip", "Close-Grip"])
            exercise_names.append(f"{modifier} {base_name}")
        
        exercises = []
        for i in range(n_exercises):
            exercise = {
                "name": exercise_names[i] if i < len(exercise_names) else f"Exercise {i+1}",
                "type": random.choice(exercise_types),
                "muscle": random.choice(muscle_groups),
                "difficulty": random.choice(difficulties),
                "equipments": random.choice(equipment_options),
                "instructions": f"Detailed step-by-step instructions for performing {exercise_names[i] if i < len(exercise_names) else f'Exercise {i+1}'} safely and effectively. Focus on proper form, breathing technique, and controlled movements throughout the exercise.",
                "safety_info": "Maintain proper form throughout the movement. Start with lighter weights to master technique. Avoid locking joints at full extension. Keep core engaged for stability."
            }
            exercises.append(exercise)
        
        df = pd.DataFrame(exercises)
        
        # Save to CSV
        csv_path = f"{self.output_dir}/exercises_sample.csv"
        df_csv = df.copy()
        df_csv['equipments'] = df_csv['equipments'].apply(lambda x: ', '.join(x))
        df_csv.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(df)} exercises to {csv_path}")
        
        # Save to JSON
        json_path = f"{self.output_dir}/exercises_sample.json"
        with open(json_path, 'w') as f:
            json.dump(exercises, f, indent=2)
        print(f"✅ Saved exercises JSON to {json_path}")
        
        return df
    
    def generate_nutrition_data(self, n_items=50):
        """Generate sample nutrition data matching API Ninjas structure"""
        print("\n🍽️  Generating sample nutrition data...")
        
        food_items = [
            "Grilled Chicken Breast", "Brown Rice", "Salmon", "Broccoli", "Sweet Potato",
            "Eggs", "Avocado", "Quinoa", "Greek Yogurt", "Almonds",
            "Banana", "Oatmeal", "Protein Shake", "Tuna", "Spinach",
            "Whole Wheat Bread", "Peanut Butter", "Cottage Cheese", "Blueberries", "Turkey Breast",
            "Black Beans", "Olive Oil", "Chicken Thigh", "Asparagus", "Strawberries",
            "Whey Protein", "Cashews", "Tilapia", "Kale", "Beef Steak",
            "Lentils", "Coconut Oil", "Shrimp", "Brussels Sprouts", "Apple",
            "Whole Milk", "Cheddar Cheese", "Pasta", "Orange", "Walnuts",
            "Tofu", "Edamame", "Chickpeas", "Green Beans", "Mango",
            "Pork Chop", "Zucchini", "Watermelon", "Feta Cheese", "Hummus"
        ]
        
        nutrition_items = []
        for food in food_items[:n_items]:
            # Generate realistic nutrition values based on food type
            is_protein = any(x in food.lower() for x in ['chicken', 'salmon', 'tuna', 'beef', 'protein', 'egg', 'turkey', 'shrimp'])
            is_carb = any(x in food.lower() for x in ['rice', 'potato', 'bread', 'oatmeal', 'quinoa', 'pasta', 'beans'])
            is_fat = any(x in food.lower() for x in ['avocado', 'oil', 'nuts', 'cheese', 'butter'])
            
            if is_protein:
                calories = np.random.uniform(150, 300)
                protein = np.random.uniform(25, 40)
                carbs = np.random.uniform(0, 5)
                fat = np.random.uniform(3, 15)
            elif is_carb:
                calories = np.random.uniform(100, 250)
                protein = np.random.uniform(3, 10)
                carbs = np.random.uniform(20, 50)
                fat = np.random.uniform(0.5, 5)
            elif is_fat:
                calories = np.random.uniform(150, 300)
                protein = np.random.uniform(2, 10)
                carbs = np.random.uniform(2, 15)
                fat = np.random.uniform(10, 30)
            else:  # Vegetables/fruits
                calories = np.random.uniform(20, 100)
                protein = np.random.uniform(1, 5)
                carbs = np.random.uniform(5, 25)
                fat = np.random.uniform(0, 2)
            
            item = {
                "name": food,
                "calories": round(calories, 1),
                "serving_size_g": round(np.random.uniform(80, 200), 1),
                "fat_total_g": round(fat, 1),
                "fat_saturated_g": round(fat * 0.3, 1),
                "protein_g": round(protein, 1),
                "sodium_mg": round(np.random.uniform(50, 500), 0),
                "potassium_mg": round(np.random.uniform(100, 800), 0),
                "cholesterol_mg": round(np.random.uniform(0, 100) if is_protein else 0, 0),
                "carbohydrates_total_g": round(carbs, 1),
                "fiber_g": round(np.random.uniform(0, 8), 1),
                "sugar_g": round(np.random.uniform(0, 15), 1)
            }
            nutrition_items.append(item)
        
        df = pd.DataFrame(nutrition_items)
        
        # Save to CSV
        csv_path = f"{self.output_dir}/nutrition_sample.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(df)} nutrition items to {csv_path}")
        
        # Save to JSON
        json_path = f"{self.output_dir}/nutrition_sample.json"
        with open(json_path, 'w') as f:
            json.dump(nutrition_items, f, indent=2)
        print(f"✅ Saved nutrition JSON to {json_path}")
        
        return df
    
    def generate_member_profiles(self, n_members=1000):
        """Generate simulated member profiles"""
        print("\n👥 Generating member profiles...")
        
        # Generate member data
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2025, 12, 15)
        
        members = []
        for i in range(n_members):
            join_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            
            member = {
                "member_id": f"MEM{str(i+1).zfill(6)}",
                "first_name": f"Member{i+1}",
                "last_name": f"LastName{i+1}",
                "email": f"member{i+1}@fitness.com",
                "age": random.randint(18, 65),
                "gender": random.choice(["Male", "Female", "Other"]),
                "membership_type": random.choice(["Basic", "Premium", "VIP"]),
                "membership_status": random.choice(["Active", "Active", "Active", "Inactive"]),  # 75% active
                "join_date": join_date.strftime("%Y-%m-%d"),
                "fitness_goal": random.choice([
                    "Weight Loss", "Muscle Gain", "General Fitness", 
                    "Athletic Performance", "Flexibility", "Endurance"
                ]),
                "height_cm": round(random.uniform(150, 200), 1),
                "initial_weight_kg": round(random.uniform(50, 120), 1)
            }
            members.append(member)
        
        df = pd.DataFrame(members)
        
        # Save to CSV
        csv_path = f"{self.output_dir}/members_sample.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(df)} member profiles to {csv_path}")
        
        return df
    
    def generate_workout_logs(self, members_df, exercises_df, n_logs=5000):
        """Generate simulated workout logs"""
        print("\n🏋️  Generating workout logs...")
        
        # Filter active members
        active_members = members_df[members_df['membership_status'] == 'Active']['member_id'].tolist()
        
        workout_logs = []
        for i in range(n_logs):
            member_id = random.choice(active_members)
            member_join_date = members_df[members_df['member_id'] == member_id]['join_date'].values[0]
            
            # Workout date between join date and now
            join_dt = datetime.strptime(member_join_date, "%Y-%m-%d")
            days_since_join = (datetime.now() - join_dt).days
            workout_date = join_dt + timedelta(days=random.randint(0, days_since_join))
            
            # Select random exercise
            exercise = exercises_df.sample(1).iloc[0]
            
            log = {
                "workout_log_id": f"WL{str(i+1).zfill(8)}",
                "member_id": member_id,
                "workout_date": workout_date.strftime("%Y-%m-%d"),
                "workout_time": f"{random.randint(6, 21):02d}:{random.choice(['00', '15', '30', '45'])}:00",
                "exercise_name": exercise['name'],
                "exercise_type": exercise['type'],
                "muscle_group": exercise['muscle'],
                "sets": random.randint(1, 5) if exercise['type'] == 'strength' else 1,
                "reps": random.randint(6, 15) if exercise['type'] == 'strength' else 0,
                "weight_kg": round(random.uniform(5, 100), 1) if exercise['type'] == 'strength' else 0,
                "duration_minutes": random.randint(5, 60),
                "calories_burned": round(random.uniform(50, 500), 1),
                "difficulty_rating": random.randint(1, 10),
                "notes": random.choice(["Great workout!", "Felt strong today", "Need to increase weight", 
                                       "Good form", "Challenging but rewarding", ""])
            }
            workout_logs.append(log)
        
        df = pd.DataFrame(workout_logs)
        
        # Save to CSV
        csv_path = f"{self.output_dir}/workout_logs_sample.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(df)} workout logs to {csv_path}")
        
        return df
    
    def generate_nutrition_logs(self, members_df, nutrition_df, n_logs=3000):
        """Generate simulated nutrition logs"""
        print("\n🥗 Generating nutrition logs...")
        
        active_members = members_df[members_df['membership_status'] == 'Active']['member_id'].tolist()
        
        meal_types = ["Breakfast", "Lunch", "Dinner", "Snack", "Pre-Workout", "Post-Workout"]
        
        nutrition_logs = []
        for i in range(n_logs):
            member_id = random.choice(active_members)
            member_join_date = members_df[members_df['member_id'] == member_id]['join_date'].values[0]
            
            join_dt = datetime.strptime(member_join_date, "%Y-%m-%d")
            days_since_join = (datetime.now() - join_dt).days
            log_date = join_dt + timedelta(days=random.randint(0, days_since_join))
            
            # Select random food item
            food = nutrition_df.sample(1).iloc[0]
            
            # Adjust serving size
            serving_multiplier = round(random.uniform(0.5, 2.0), 1)
            
            log = {
                "nutrition_log_id": f"NL{str(i+1).zfill(8)}",
                "member_id": member_id,
                "log_date": log_date.strftime("%Y-%m-%d"),
                "meal_type": random.choice(meal_types),
                "food_item": food['name'],
                "serving_size_g": round(food['serving_size_g'] * serving_multiplier, 1),
                "servings": serving_multiplier,
                "calories": round(food['calories'] * serving_multiplier, 1),
                "protein_g": round(food['protein_g'] * serving_multiplier, 1),
                "carbs_g": round(food['carbohydrates_total_g'] * serving_multiplier, 1),
                "fat_g": round(food['fat_total_g'] * serving_multiplier, 1),
                "fiber_g": round(food['fiber_g'] * serving_multiplier, 1),
                "sugar_g": round(food['sugar_g'] * serving_multiplier, 1)
            }
            nutrition_logs.append(log)
        
        df = pd.DataFrame(nutrition_logs)
        
        # Save to CSV
        csv_path = f"{self.output_dir}/nutrition_logs_sample.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(df)} nutrition logs to {csv_path}")
        
        return df
    
    def generate_member_engagement(self, members_df, n_records=2000):
        """Generate member engagement metrics"""
        print("\n📈 Generating member engagement data...")
        
        engagement_records = []
        for _, member in members_df.iterrows():
            join_dt = datetime.strptime(member['join_date'], "%Y-%m-%d")
            days_since_join = (datetime.now() - join_dt).days
            
            # Generate monthly engagement records
            for month_offset in range(0, min(days_since_join // 30, 12)):
                record_date = join_dt + timedelta(days=month_offset * 30)
                
                # Simulate engagement decline over time for some members
                engagement_factor = 1.0 if member['membership_status'] == 'Active' else random.uniform(0.3, 0.7)
                
                record = {
                    "engagement_id": f"ENG{len(engagement_records)+1:08d}",
                    "member_id": member['member_id'],
                    "record_date": record_date.strftime("%Y-%m-%d"),
                    "check_ins": int(random.randint(0, 20) * engagement_factor),
                    "app_logins": int(random.randint(0, 30) * engagement_factor),
                    "classes_attended": int(random.randint(0, 12) * engagement_factor),
                    "trainer_sessions": int(random.randint(0, 4) * engagement_factor),
                    "engagement_score": round(random.uniform(0, 100) * engagement_factor, 1)
                }
                engagement_records.append(record)
                
                if len(engagement_records) >= n_records:
                    break
            
            if len(engagement_records) >= n_records:
                break
        
        df = pd.DataFrame(engagement_records)
        
        # Save to CSV
        csv_path = f"{self.output_dir}/member_engagement_sample.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(df)} engagement records to {csv_path}")
        
        return df
    
    def generate_summary_statistics(self, members_df, exercises_df, nutrition_df, 
                                   workout_logs_df, nutrition_logs_df, engagement_df):
        """Generate summary statistics of the dataset"""
        print("\n" + "="*70)
        print("SAMPLE DATA GENERATION SUMMARY")
        print("="*70)
        
        print(f"\n📊 Dataset Statistics:")
        print(f"   Members: {len(members_df):,}")
        print(f"   - Active: {len(members_df[members_df['membership_status'] == 'Active']):,}")
        print(f"   - Inactive: {len(members_df[members_df['membership_status'] == 'Inactive']):,}")
        
        print(f"\n   Exercises: {len(exercises_df):,}")
        print(f"   - Muscle Groups: {exercises_df['muscle'].nunique()}")
        print(f"   - Exercise Types: {exercises_df['type'].nunique()}")
        
        print(f"\n   Nutrition Items: {len(nutrition_df):,}")
        print(f"   - Avg Calories: {nutrition_df['calories'].mean():.1f} kcal")
        print(f"   - Avg Protein: {nutrition_df['protein_g'].mean():.1f}g")
        
        print(f"\n   Workout Logs: {len(workout_logs_df):,}")
        print(f"   - Avg Duration: {workout_logs_df['duration_minutes'].mean():.1f} minutes")
        print(f"   - Avg Calories Burned: {workout_logs_df['calories_burned'].mean():.1f} kcal")
        
        print(f"\n   Nutrition Logs: {len(nutrition_logs_df):,}")
        print(f"   - Total Calories Logged: {nutrition_logs_df['calories'].sum():,.0f} kcal")
        
        print(f"\n   Engagement Records: {len(engagement_df):,}")
        print(f"   - Avg Engagement Score: {engagement_df['engagement_score'].mean():.1f}")
        
        print("\n" + "="*70)
        print("✅ SAMPLE DATA GENERATION COMPLETE")
        print("="*70)


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("HEALTH & FITNESS ANALYTICS PLATFORM")
    print("Sample Data Generation Script")
    print("="*70)
    
    generator = SampleDataGenerator()
    
    # Generate all datasets
    exercises_df = generator.generate_exercises_data(n_exercises=100)
    nutrition_df = generator.generate_nutrition_data(n_items=50)
    members_df = generator.generate_member_profiles(n_members=1000)
    workout_logs_df = generator.generate_workout_logs(members_df, exercises_df, n_logs=5000)
    nutrition_logs_df = generator.generate_nutrition_logs(members_df, nutrition_df, n_logs=3000)
    engagement_df = generator.generate_member_engagement(members_df, n_records=2000)
    
    # Generate summary
    generator.generate_summary_statistics(
        members_df, exercises_df, nutrition_df, 
        workout_logs_df, nutrition_logs_df, engagement_df
    )
    
    print("\n💡 Next Steps:")
    print("1. Review the generated CSV files in the data directory")
    print("2. Use these files as input for Snowflake data warehouse")
    print("3. Proceed with ETL pipeline development")
    print("4. Build Power BI dashboards using this data\n")


if __name__ == "__main__":
    main()
