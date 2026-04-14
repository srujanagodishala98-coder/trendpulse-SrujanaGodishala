import pandas as pd
import matplotlib.pyplot as plt
import os

# 1 — Setup

# Load the analysed CSV
df = pd.read_csv("data/trends_analysed.csv")

# Create outputs/ folder if it doesn't exist
os.makedirs("outputs", exist_ok=True)




# 2 — Chart 1: Top 10 Stories by Score

top10 = df.nlargest(10, "score").copy()
# Shorten titles longer than 50 characters
top10["short_title"] = top10["title"].apply(lambda x: x[:47] + "..." if len(x) > 50 else x)

plt.figure(figsize=(8,6))
plt.barh(top10["short_title"], top10["score"], color="skyblue")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()




# 3 — Chart 2: Stories per Category

category_counts = df["category"].value_counts()

plt.figure(figsize=(8,6))
category_counts.plot(kind="bar", color=plt.cm.tab10.colors)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()





plt.figure(figsize=(8,6))
colors = df["is_popular"].map({True: "green", False: "red"})
plt.scatter(df["score"], df["num_comments"], c=colors, alpha=0.6)
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend(handles=[
    plt.Line2D([0],[0], marker='o', color='w', label='Popular', markerfacecolor='green', markersize=8),
    plt.Line2D([0],[0], marker='o', color='w', label='Not Popular', markerfacecolor='red', markersize=8)
])
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()



# Bonus — Dashboard

fig, axes = plt.subplots(1, 3, figsize=(18,6))

# Chart 1 in dashboard
axes[0].barh(top10["short_title"], top10["score"], color="skyblue")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")
axes[0].set_title("Top 10 Stories by Score")

# Chart 2 in dashboard
axes[1].bar(category_counts.index, category_counts.values, color=plt.cm.tab10.colors)
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].set_title("Stories per Category")

# Chart 3 in dashboard
axes[2].scatter(df["score"], df["num_comments"], c=colors, alpha=0.6)
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].set_title("Score vs Comments")

fig.suptitle("TrendPulse Dashboard", fontsize=16)
plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("\nCharts saved to outputs folder:\n")
print(" |-- chart1_top_stories.png")
print(" |-- chart2_categories.png")
print(" |-- chart3_scatter.png")
print(" |__ dashboard.png (bonus)\n")
