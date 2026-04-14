import requests
import json
import time
import os
from datetime import datetime

# Define categories and their keywords
CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# Base URLs for the Hacker News API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_DETAILS_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# User-Agent header
HEADERS = {"User-Agent": "TrendPulse/1.0"}

def fetch_story_details(story_id):
    """Fetches details for a single Hacker News story."""
    try:
        response = requests.get(ITEM_DETAILS_URL.format(story_id), headers=HEADERS)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for story ID {story_id}: {e}")
        return None

def assign_category(title):
    """Assigns a category to a story based on its title and predefined keywords."""
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return "uncategorized" # Default category if no keywords match

def collect_stories():
    """Collects trending Hacker News stories, categorizes them, and extracts relevant fields."""
    collected_stories = []
    category_counts = {cat: 0 for cat in CATEGORIES.keys()} # Initialize counts for each category

    print("Fetching top story IDs...")
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS)
        response.raise_for_status()
        top_story_ids = response.json()[:500] # Fetch the first 500 story IDs
        print(f"Successfully fetched {len(top_story_ids)} top story IDs.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching top story IDs: {e}")
        return []

    processed_stories_count = 0
    # Process stories in batches, waiting between categories
    for category in CATEGORIES.keys():
        print(f"\nCollecting stories for category: {category}...")
        stories_for_category = []
        for story_id in top_story_ids:
            if category_counts[category] >= 25: # Limit to 25 stories per category
                break # Move to the next category once limit is reached

            details = fetch_story_details(story_id)
            if details and details.get('title'): # Ensure story has a title
                # Assign category and check if it matches the current category being processed
                assigned_cat = assign_category(details['title'])
                if assigned_cat == category:
                    if category_counts[category] < 25:
                        story_data = {
                            "post_id": details.get("id"),
                            "title": details.get("title"),
                            "category": assigned_cat,
                            "score": details.get("score", 0),
                            "num_comments": details.get("descendants", 0),
                            "author": details.get("by_Srujana", "N/A"),
                            "collected_at": datetime.now().isoformat()
                        }
                        stories_for_category.append(story_data)
                        category_counts[category] += 1
            processed_stories_count += 1
            # Simple progress update (too frequent for every story due to sleep per category)
            # You might want to adjust this for very large number of stories

        collected_stories.extend(stories_for_category)
        print(f"Collected {len(stories_for_category)} stories for '{category}'. \nTotal collected: {len(collected_stories)}")
        time.sleep(2) # Wait 2 seconds between processing each category

    return collected_stories

def save_stories_to_json(stories, output_dir="data"):
    """Saves the collected stories to a JSON file."""
    os.makedirs(output_dir, exist_ok=True) # Create data directory if it doesn't exist

    today_date = datetime.now().strftime("%Y%m%d")
    filename = os.path.join(output_dir, f"trends_{today_date}.json")

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stories, f, ensure_ascii=False, indent=4)
        print(f"\nCollected {len(stories)} stories. Saved to {filename}")
    except IOError as e:
        print(f"Error saving stories to file {filename}: {e}")

if __name__ == "__main__":
    collected_data = collect_stories()
    if collected_data:
        save_stories_to_json(collected_data)

print("\nData collection completed successfully.")