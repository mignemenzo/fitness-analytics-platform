"""
Fetch Real Data from API Ninjas
This script pulls actual exercise and nutrition data from the API
"""

import requests
import pandas as pd
import time
from pathlib import Path
from config import API_CONFIG, DATA_DIR

def fetch_exercises_by_muscle(muscle_group, limit=10):
    """
    Get exercise data from API Ninjas for a specific muscle group
    Returns a list of exercise dictionaries
    """
    url = f"{API_CONFIG['api_ninjas_base_url']}/exercises"
    headers = {'X-Api-Key': API_CONFIG['api_key']}
    params = {'muscle': muscle_group}
    
    print(f"Fetching {muscle_group} exercises...")
    
    try:
        response = requests.get(
            url, 
            headers=headers, 
            params=params, 
            timeout=API_CONFIG['timeout_seconds']
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Got {len(data)} exercises")
            return data[:limit]  # Only take what we need
        else:
            print(f"  API returned status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"  Error: {str(e)}")
        return []

def fetch_nutrition_info(food_name):
    """
    Get nutrition data for a specific food item
    Returns a dictionary with macros and calories
    """
    url = f"{API_CONFIG['api_ninjas_base_url']}/nutrition"
    headers = {'X-Api-Key': API_CONFIG['api_key']}
    params = {'query': food_name}
    
    print(f"Fetching nutrition for {food_name}...")
    
    try:
        response = requests.get(
            url, 
            headers=headers, 
            params=params, 
            timeout=API_CONFIG['timeout_seconds']
        )
        
        if response.status_code == 200:
            data = response.json()
            if data:
                print(f"  Found it!")
                return data[0]  # API returns a list, we want the first item
            else:
                print(f"  No data found")
                return None
        else:
            print(f"  API returned status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  Error: {str(e)}")
        return None

def main():
    print("\nStarting API data fetch...")
    print("This will use about 35 API calls out of your 3,000 monthly limit\n")
    
    # Fetch exercises for major muscle groups
    # We'll get 5 exercises per group to keep it reasonable
    muscle_groups = ['biceps', 'chest', 'legs', 'abs', 'back', 'shoulders', 'triceps']
    all_exercises = []
    
    print("Part 1: Fetching exercises")
    print("-" * 40)
    
    for muscle in muscle_groups:
        exercises = fetch_exercises_by_muscle(muscle, limit=5)
        all_exercises.extend(exercises)
        time.sleep(0.5)  # Small delay to be nice to the API
    
    # Save exercises to CSV
    if all_exercises:
        df_exercises = pd.DataFrame(all_exercises)
        output_file = DATA_DIR / "exercises_real_api.csv"
        df_exercises.to_csv(output_file, index=False)
        print(f"\nSaved {len(all_exercises)} real exercises to exercises_real_api.csv")
    else:
        print("\nNo exercises were fetched. Check your API key.")
    
    # Fetch nutrition for common fitness foods
    # These are typical foods people track when working out
    foods = [
        'chicken breast', 'brown rice', 'broccoli', 'salmon', 
        'banana', 'oatmeal', 'eggs', 'almonds', 'greek yogurt', 
        'sweet potato', 'spinach', 'avocado', 'quinoa', 'tuna'
    ]
    
    print(f"\nPart 2: Fetching nutrition data")
    print("-" * 40)
    
    nutrition_data = []
    for food in foods:
        data = fetch_nutrition_info(food)
        if data:
            nutrition_data.append(data)
        time.sleep(0.5)  # Small delay between requests
    
    # Save nutrition to CSV
    if nutrition_data:
        df_nutrition = pd.DataFrame(nutrition_data)
        output_file = DATA_DIR / "nutrition_real_api.csv"
        df_nutrition.to_csv(output_file, index=False)
        print(f"\nSaved {len(nutrition_data)} real nutrition items to nutrition_real_api.csv")
    else:
        print("\nNo nutrition data was fetched. Check your API key.")
    
    # Summary
    print("\n" + "-" * 40)
    print("Done!")
    print(f"Total API calls used: ~{len(muscle_groups) + len(foods)}")
    print(f"Remaining this month: ~{3000 - len(muscle_groups) - len(foods)}")
    print("\nYou now have real API data mixed with your generated data.")
    print("This shows recruiters you can work with actual REST APIs!")

if __name__ == "__main__":
    main()
