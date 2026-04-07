import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ======================
# 1. Load and Clean Data
# ======================
df = pd.read_csv("fraud_sample.csv")

# Drop unnecessary column
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Convert datetime
df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])

# Create new feature: hour
df["hour"] = df["trans_date_trans_time"].dt.hour

print("Data Loaded Successfully")
print(df.head())

# ======================
# 2. SQL Analysis
# ======================
conn = sqlite3.connect(":memory:")
df.to_sql("transactions", conn, index=False, if_exists="replace")

query = """
SELECT category, COUNT(*) as fraud_count
FROM transactions
WHERE is_fraud = 1
GROUP BY category
ORDER BY fraud_count DESC
"""

fraud_by_category = pd.read_sql(query, conn)
print("\nFraud by Category:")
print(fraud_by_category)

# ======================
# 3. Fraud by Hour Analysis
# ======================
fraud_by_hour = (
    df[df["is_fraud"] == 1]
    .groupby("hour")
    .size()
)

print("\nFraud by Hour:")
print(fraud_by_hour)

# ======================
# 4. Visualisation
# ======================
plt.figure(figsize=(10, 5))
fraud_by_hour.plot(kind="bar")

plt.title("Fraud Transactions by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Fraud Transactions")

plt.tight_layout()

# Save figure (IMPORTANT for GitHub)
plt.savefig("outputs/fraud_by_hour.png")

plt.show()
