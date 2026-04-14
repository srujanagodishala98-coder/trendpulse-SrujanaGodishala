import pandas as pd

# 1 — Load the JSON File

# Load the JSON file into a DataFrame
df = pd.read_json("data/trends_20260414.json")

# Print no.of rows got loaded
print(f"\nLoaded {len(df)} stories from data/trends_20260414.json")


# 2 — Cleaning the Data

# Removing duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"\nAfter removing duplicates: {len(df)}")

# Drop rows where post_id, title, or score is missing
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Ensure score and num_comments are integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Strip extra whitespace from titles
df["title"] = df["title"].str.strip()

print("\nData cleaning completed.")

# 3 — Save as CSV

# Save the cleaned DataFrame to CSV
df.to_csv("data/trends_clean.csv", index=False)

# Print confirmation message
print("----------------------------------------------------------------")
print(f"\nSaved {len(df)} rows to data/trends_clean.csv\n")
print("Data saved to CSV file successfully.")
print("----------------------------------------------------------------")

# Print summary: number of stories per category
print("Stories per category:")
print(df["category"].value_counts())
