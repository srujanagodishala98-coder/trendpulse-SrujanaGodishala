import pandas as pd
import numpy as np

# 1 — Load and Explore

# Load the cleaned CSV into a DataFrame
df = pd.read_csv("data/trends_clean.csv")

# Print the shape of the DataFrame
print(f"\nLoaded data: {df.shape}\n")

# Print the first 5 rows
print("First 5 rows:")
print(df.head(), "\n")

# Compute average score and average num_comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()
print(f"Average score   : {int(avg_score)}")
print(f"Average comments: {int(avg_comments)}\n")


# 2 — Basic Analysis with NumPy

scores = df["score"].values
comments = df["num_comments"].values

print("--- NumPy Stats ---")
print(f"Mean score   : {int(np.mean(scores))}")
print(f"Median score : {int(np.median(scores))}")
print(f"Std deviation: {int(np.std(scores))}")
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}\n")

# Category with most stories
category_counts = df["category"].value_counts()
most_category = category_counts.idxmax()
print(f"Most stories in: {most_category} ({category_counts.max()} stories)\n")

# Story with most comments
max_comments_idx = np.argmax(comments)
most_commented_story = df.iloc[max_comments_idx]
print(f'Most commented story: "{most_commented_story["title"]}"  — {most_commented_story["num_comments"]} comments\n')



# 3 — Add New Columns

# Engagement = num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if score > average score
df["is_popular"] = df["score"] > avg_score



# 4 — Save the Result

df.to_csv("data/trends_analysed.csv", index=False)
print("Saved to data/trends_analysed.csv\n")
print("Analysis completed successfully.\n")