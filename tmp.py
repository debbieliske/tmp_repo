df = pd.DataFrame(data)

# Clean and convert utilization to numeric
df['Utilization'] = df['Utilization'].str.rstrip('%').astype(float)

# Calculate average utilization per position
avg_utilization = df.groupby("Position")["Utilization"].mean().sort_values(ascending=False)

# Plot
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")
ax = sns.barplot(
    x=avg_utilization.values, 
    y=avg_utilization.index, 
    palette="viridis"
)
