# REST API Integration - Real Data

This project now includes actual data from API Ninjas! Here's what we fetched:

## What We Got

**Exercises**: 20 real exercises from API Ninjas
- Biceps, chest, shoulders, and triceps exercises
- Includes equipment requirements, difficulty levels, and detailed instructions
- Saved in `data/exercises_real_api.csv`

**Nutrition Data**: 14 real food items
- Common fitness foods like chicken breast, salmon, oatmeal, etc.
- Complete macro breakdown (protein, carbs, fats, calories)
- Saved in `data/nutrition_real_api.csv`

## API Usage Stats

- **API Calls Used**: 21 out of 3,000 monthly limit
- **Remaining**: 2,979 calls
- **Cost**: $0 (using free tier)

## How It Works

The script `05_fetch_real_api_data.py` connects to API Ninjas using your API key and pulls real data. It's set up to:

1. Fetch exercises for different muscle groups
2. Get nutrition info for common fitness foods
3. Save everything to CSV files
4. Handle errors gracefully if the API is down

## Running It Yourself

If you want to fetch more data:

```bash
cd scripts
python 05_fetch_real_api_data.py
```

The script is smart about rate limiting and won't hammer the API. It waits half a second between requests to be respectful.

## Why This Matters

Having real API data shows you can:
- Work with REST APIs and handle authentication
- Parse JSON responses and convert to DataFrames
- Handle API errors and rate limits
- Integrate external data sources into your pipeline

This is exactly what data engineers do in real jobs - pulling data from various APIs and loading it into data warehouses.

## Next Steps

You could easily extend this to:
- Fetch more muscle groups (we only did 7)
- Get more nutrition items (thousands available)
- Set up a scheduled job to refresh data daily
- Add more APIs (weather, location, etc.)

The infrastructure is all there, you just need to call the functions!
