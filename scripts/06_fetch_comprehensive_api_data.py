"""
Comprehensive API Data Fetch
Pulls as much real data as possible from API Ninjas to build a substantial dataset
"""

import requests
import pandas as pd
import time
from pathlib import Path
from config import API_CONFIG, DATA_DIR

def fetch_all_exercises_for_muscle(muscle_group, max_results=100):
    """
    Fetch all available exercises for a muscle group
    API Ninjas returns up to 10 per call, so we'll use offset to get more
    """
    url = f"{API_CONFIG['api_ninjas_base_url']}/exercises"
    headers = {'X-Api-Key': API_CONFIG['api_key']}
    
    all_exercises = []
    offset = 0
    
    print(f"Fetching all {muscle_group} exercises...")
    
    while len(all_exercises) < max_results:
        params = {
            'muscle': muscle_group,
            'offset': offset
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break  # No more results
                
                all_exercises.extend(data)
                print(f"  Got {len(data)} more (total: {len(all_exercises)})")
                offset += 10
                time.sleep(0.3)  # Small delay between requests
            else:
                print(f"  API error: {response.status_code}")
                break
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            break
    
    return all_exercises

def fetch_nutrition_batch(food_items):
    """
    Fetch nutrition data for a list of food items
    """
    url = f"{API_CONFIG['api_ninjas_base_url']}/nutrition"
    headers = {'X-Api-Key': API_CONFIG['api_key']}
    
    all_nutrition = []
    
    for food in food_items:
        params = {'query': food}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    # Add the search term for reference
                    for item in data:
                        item['search_term'] = food
                    all_nutrition.extend(data)
                    print(f"  {food}: {len(data)} items")
                else:
                    print(f"  {food}: no data")
            else:
                print(f"  {food}: API error {response.status_code}")
            
            time.sleep(0.3)  # Delay between requests
            
        except Exception as e:
            print(f"  {food}: Error - {str(e)}")
    
    return all_nutrition

def main():
    print("\nComprehensive API Data Fetch")
    print("This will fetch as much real data as possible from API Ninjas")
    print("Estimated API calls: 200-300 out of your 3,000 limit\n")
    
    # Part 1: Fetch exercises for ALL major muscle groups
    muscle_groups = [
        'abdominals', 'abductors', 'adductors', 'biceps', 'calves', 
        'chest', 'forearms', 'glutes', 'hamstrings', 'lats', 
        'lower_back', 'middle_back', 'neck', 'quadriceps', 'traps', 
        'triceps', 'shoulders'
    ]
    
    print("PART 1: Fetching Exercises")
    print("-" * 50)
    
    all_exercises = []
    for muscle in muscle_groups:
        exercises = fetch_all_exercises_for_muscle(muscle, max_results=50)
        all_exercises.extend(exercises)
        print(f"  Total exercises so far: {len(all_exercises)}\n")
    
    # Remove duplicates (some exercises work multiple muscles)
    df_exercises = pd.DataFrame(all_exercises)
    df_exercises = df_exercises.drop_duplicates(subset=['name'])
    
    output_file = DATA_DIR / "exercises_comprehensive_api.csv"
    df_exercises.to_csv(output_file, index=False)
    print(f"\nSaved {len(df_exercises)} unique exercises to exercises_comprehensive_api.csv")
    
    # Part 2: Fetch nutrition for a comprehensive list of foods
    # Include proteins, carbs, fats, vegetables, fruits, snacks
    food_categories = {
        'Proteins': [
            'chicken breast', 'chicken thigh', 'ground beef', 'steak', 'pork chop',
            'salmon', 'tuna', 'tilapia', 'shrimp', 'cod',
            'eggs', 'egg whites', 'turkey breast', 'ground turkey',
            'tofu', 'tempeh', 'protein powder', 'cottage cheese'
        ],
        'Carbs': [
            'white rice', 'brown rice', 'jasmine rice', 'quinoa', 'oatmeal',
            'whole wheat bread', 'white bread', 'pasta', 'sweet potato',
            'regular potato', 'couscous', 'bagel', 'tortilla'
        ],
        'Vegetables': [
            'broccoli', 'spinach', 'kale', 'carrots', 'bell pepper',
            'tomato', 'cucumber', 'lettuce', 'asparagus', 'green beans',
            'cauliflower', 'brussels sprouts', 'zucchini', 'mushrooms'
        ],
        'Fruits': [
            'banana', 'apple', 'orange', 'strawberry', 'blueberry',
            'mango', 'pineapple', 'grapes', 'watermelon', 'peach',
            'pear', 'kiwi', 'grapefruit'
        ],
        'Healthy Fats': [
            'avocado', 'almonds', 'walnuts', 'peanut butter', 'almond butter',
            'olive oil', 'coconut oil', 'chia seeds', 'flax seeds',
            'cashews', 'pecans', 'sunflower seeds'
        ],
        'Dairy': [
            'greek yogurt', 'milk', 'cheese', 'mozzarella', 'cheddar cheese',
            'yogurt', 'whey protein', 'butter'
        ],
        'Snacks': [
            'granola bar', 'protein bar', 'rice cakes', 'popcorn',
            'dark chocolate', 'honey', 'maple syrup'
        ]
    }
    
    print("\n\nPART 2: Fetching Nutrition Data")
    print("-" * 50)
    
    all_nutrition = []
    for category, foods in food_categories.items():
        print(f"\n{category}:")
        nutrition_data = fetch_nutrition_batch(foods)
        all_nutrition.extend(nutrition_data)
        print(f"  Category total: {len(nutrition_data)} items")
    
    # Save nutrition data
    df_nutrition = pd.DataFrame(all_nutrition)
    output_file = DATA_DIR / "nutrition_comprehensive_api.csv"
    df_nutrition.to_csv(output_file, index=False)
    print(f"\n\nSaved {len(df_nutrition)} nutrition items to nutrition_comprehensive_api.csv")
    
    # Final summary
    print("\n" + "=" * 50)
    print("COMPREHENSIVE DATA FETCH COMPLETE!")
    print("=" * 50)
    print(f"\nExercises: {len(df_exercises)} unique exercises")
    print(f"Nutrition: {len(df_nutrition)} food items")
    print(f"\nEstimated API calls used: ~{len(muscle_groups) * 5 + len(sum(food_categories.values(), []))}")
    print(f"This is still well within your 3,000 monthly limit!")
    print("\nYou now have a SUBSTANTIAL real-world dataset from actual APIs.")

if __name__ == "__main__":
    main()
