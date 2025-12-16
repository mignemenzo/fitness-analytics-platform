"""
Health & Fitness Analytics Platform - API Testing Script
Author: Data Engineering Team
Date: December 2025

This script tests the API Ninjas Exercises and Nutrition APIs to validate
connectivity, understand data structures, and ensure data quality for the
ETL pipeline.
"""

import requests
import json
import pandas as pd
from datetime import datetime
import time

# API Configuration
API_BASE_URL = "https://api.api-ninjas.com/v1"
API_KEY = "YOUR_API_KEY_HERE"  # Replace with actual API key from api-ninjas.com

HEADERS = {
    "X-Api-Key": API_KEY
}


class FitnessAPITester:
    """Test and validate fitness-related APIs"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"X-Api-Key": api_key}
        self.base_url = API_BASE_URL
        self.results = {
            "exercises": [],
            "nutrition": [],
            "errors": []
        }
    
    def test_exercises_api(self):
        """Test Exercises API with various muscle groups"""
        print("\n" + "="*70)
        print("TESTING EXERCISES API")
        print("="*70)
        
        # Test different muscle groups
        muscle_groups = ["biceps", "chest", "back", "legs", "shoulders", "abs"]
        
        for muscle in muscle_groups:
            try:
                print(f"\n📊 Fetching exercises for: {muscle.upper()}")
                
                endpoint = f"{self.base_url}/exercises"
                params = {"muscle": muscle}
                
                response = requests.get(endpoint, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    exercises = response.json()
                    print(f"✅ Success! Retrieved {len(exercises)} exercises")
                    
                    # Store results
                    for exercise in exercises:
                        exercise['query_muscle'] = muscle
                        exercise['fetch_timestamp'] = datetime.now().isoformat()
                        self.results['exercises'].append(exercise)
                    
                    # Display sample exercise
                    if exercises:
                        sample = exercises[0]
                        print(f"\n   Sample Exercise: {sample.get('name')}")
                        print(f"   Type: {sample.get('type')}")
                        print(f"   Difficulty: {sample.get('difficulty')}")
                        print(f"   Equipment: {', '.join(sample.get('equipments', []))}")
                        print(f"   Instructions: {sample.get('instructions', '')[:100]}...")
                
                elif response.status_code == 401:
                    print(f"❌ Authentication Error: Invalid API Key")
                    self.results['errors'].append({
                        "api": "exercises",
                        "muscle": muscle,
                        "error": "Invalid API Key",
                        "status_code": 401
                    })
                    return False
                
                else:
                    print(f"❌ Error: Status Code {response.status_code}")
                    self.results['errors'].append({
                        "api": "exercises",
                        "muscle": muscle,
                        "error": response.text,
                        "status_code": response.status_code
                    })
                
                # Rate limiting - be respectful to API
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Exception occurred: {str(e)}")
                self.results['errors'].append({
                    "api": "exercises",
                    "muscle": muscle,
                    "error": str(e)
                })
        
        return True
    
    def test_nutrition_api(self):
        """Test Nutrition API with various food queries"""
        print("\n" + "="*70)
        print("TESTING NUTRITION API")
        print("="*70)
        
        # Test different food queries
        food_queries = [
            "grilled chicken breast",
            "1 cup brown rice",
            "2 eggs and avocado",
            "protein shake with banana",
            "salmon with vegetables"
        ]
        
        for query in food_queries:
            try:
                print(f"\n🍽️  Analyzing nutrition for: '{query}'")
                
                endpoint = f"{self.base_url}/nutrition"
                params = {"query": query}
                
                response = requests.get(endpoint, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    nutrition_data = response.json()
                    print(f"✅ Success! Retrieved nutrition data for {len(nutrition_data)} items")
                    
                    # Store results
                    for item in nutrition_data:
                        item['original_query'] = query
                        item['fetch_timestamp'] = datetime.now().isoformat()
                        self.results['nutrition'].append(item)
                    
                    # Display nutrition summary
                    if nutrition_data:
                        for item in nutrition_data:
                            print(f"\n   Food: {item.get('name')}")
                            print(f"   Calories: {item.get('calories', 0):.1f} kcal")
                            print(f"   Protein: {item.get('protein_g', 0):.1f}g")
                            print(f"   Carbs: {item.get('carbohydrates_total_g', 0):.1f}g")
                            print(f"   Fat: {item.get('fat_total_g', 0):.1f}g")
                            print(f"   Serving Size: {item.get('serving_size_g', 0):.1f}g")
                
                elif response.status_code == 401:
                    print(f"❌ Authentication Error: Invalid API Key")
                    self.results['errors'].append({
                        "api": "nutrition",
                        "query": query,
                        "error": "Invalid API Key",
                        "status_code": 401
                    })
                    return False
                
                else:
                    print(f"❌ Error: Status Code {response.status_code}")
                    self.results['errors'].append({
                        "api": "nutrition",
                        "query": query,
                        "error": response.text,
                        "status_code": response.status_code
                    })
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Exception occurred: {str(e)}")
                self.results['errors'].append({
                    "api": "nutrition",
                    "query": query,
                    "error": str(e)
                })
        
        return True
    
    def test_specific_exercise_queries(self):
        """Test specific exercise queries with different parameters"""
        print("\n" + "="*70)
        print("TESTING SPECIFIC EXERCISE QUERIES")
        print("="*70)
        
        test_cases = [
            {"name": "press", "description": "Exercises with 'press' in name"},
            {"type": "strength", "description": "Strength exercises"},
            {"difficulty": "beginner", "description": "Beginner exercises"},
            {"muscle": "chest", "type": "strength", "description": "Chest strength exercises"}
        ]
        
        for test_case in test_cases:
            try:
                description = test_case.pop('description')
                print(f"\n🔍 Testing: {description}")
                print(f"   Parameters: {test_case}")
                
                endpoint = f"{self.base_url}/exercises"
                response = requests.get(endpoint, headers=self.headers, params=test_case)
                
                if response.status_code == 200:
                    exercises = response.json()
                    print(f"✅ Found {len(exercises)} exercises")
                    
                    if exercises:
                        print(f"   Examples: {', '.join([ex['name'] for ex in exercises[:3]])}")
                
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Exception: {str(e)}")
    
    def save_results(self, output_dir="../data"):
        """Save API test results to JSON and CSV files"""
        print("\n" + "="*70)
        print("SAVING RESULTS")
        print("="*70)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save exercises data
        if self.results['exercises']:
            exercises_df = pd.DataFrame(self.results['exercises'])
            
            # Flatten equipment lists for CSV
            exercises_df['equipments'] = exercises_df['equipments'].apply(
                lambda x: ', '.join(x) if isinstance(x, list) else x
            )
            
            exercises_csv = f"{output_dir}/exercises_sample_{timestamp}.csv"
            exercises_df.to_csv(exercises_csv, index=False)
            print(f"✅ Saved exercises data: {exercises_csv}")
            print(f"   Total exercises: {len(exercises_df)}")
            
            # Save JSON for reference
            exercises_json = f"{output_dir}/exercises_sample_{timestamp}.json"
            with open(exercises_json, 'w') as f:
                json.dump(self.results['exercises'], f, indent=2)
            print(f"✅ Saved exercises JSON: {exercises_json}")
        
        # Save nutrition data
        if self.results['nutrition']:
            nutrition_df = pd.DataFrame(self.results['nutrition'])
            
            nutrition_csv = f"{output_dir}/nutrition_sample_{timestamp}.csv"
            nutrition_df.to_csv(nutrition_csv, index=False)
            print(f"✅ Saved nutrition data: {nutrition_csv}")
            print(f"   Total nutrition items: {len(nutrition_df)}")
            
            # Save JSON
            nutrition_json = f"{output_dir}/nutrition_sample_{timestamp}.json"
            with open(nutrition_json, 'w') as f:
                json.dump(self.results['nutrition'], f, indent=2)
            print(f"✅ Saved nutrition JSON: {nutrition_json}")
        
        # Save errors if any
        if self.results['errors']:
            errors_json = f"{output_dir}/api_errors_{timestamp}.json"
            with open(errors_json, 'w') as f:
                json.dump(self.results['errors'], f, indent=2)
            print(f"⚠️  Saved errors log: {errors_json}")
    
    def generate_summary_report(self):
        """Generate a summary report of API testing"""
        print("\n" + "="*70)
        print("API TESTING SUMMARY REPORT")
        print("="*70)
        
        print(f"\n📊 Exercises API:")
        print(f"   Total exercises retrieved: {len(self.results['exercises'])}")
        
        if self.results['exercises']:
            exercises_df = pd.DataFrame(self.results['exercises'])
            print(f"   Unique muscle groups: {exercises_df['muscle'].nunique()}")
            print(f"   Exercise types: {', '.join(exercises_df['type'].unique())}")
            print(f"   Difficulty levels: {', '.join(exercises_df['difficulty'].unique())}")
        
        print(f"\n🍽️  Nutrition API:")
        print(f"   Total nutrition items retrieved: {len(self.results['nutrition'])}")
        
        if self.results['nutrition']:
            nutrition_df = pd.DataFrame(self.results['nutrition'])
            total_calories = nutrition_df['calories'].sum()
            avg_protein = nutrition_df['protein_g'].mean()
            print(f"   Total calories (all samples): {total_calories:.1f} kcal")
            print(f"   Average protein per item: {avg_protein:.1f}g")
        
        print(f"\n❌ Errors encountered: {len(self.results['errors'])}")
        
        if self.results['errors']:
            print("\n   Error details:")
            for error in self.results['errors']:
                print(f"   - {error.get('api')}: {error.get('error')}")
        
        print("\n" + "="*70)
        print("✅ API TESTING COMPLETE")
        print("="*70)


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("HEALTH & FITNESS ANALYTICS PLATFORM")
    print("API Testing & Validation Script")
    print("="*70)
    
    # Check if API key is set
    if API_KEY == "YOUR_API_KEY_HERE":
        print("\n⚠️  WARNING: API Key not configured!")
        print("Please sign up at https://api-ninjas.com and replace API_KEY in the script")
        print("\nFor testing purposes, you can:")
        print("1. Visit https://api-ninjas.com")
        print("2. Sign up for a free account")
        print("3. Get your API key from the dashboard")
        print("4. Replace 'YOUR_API_KEY_HERE' in this script with your actual key")
        return
    
    # Initialize tester
    tester = FitnessAPITester(API_KEY)
    
    # Run tests
    exercises_success = tester.test_exercises_api()
    
    if exercises_success:
        nutrition_success = tester.test_nutrition_api()
        
        if nutrition_success:
            tester.test_specific_exercise_queries()
    
    # Save results
    tester.save_results()
    
    # Generate summary
    tester.generate_summary_report()
    
    print("\n💡 Next Steps:")
    print("1. Review the saved CSV and JSON files in the data directory")
    print("2. Verify data quality and structure")
    print("3. Proceed to Snowflake setup and ETL pipeline development")
    print("4. Use these sample files as reference for schema design\n")


if __name__ == "__main__":
    main()
