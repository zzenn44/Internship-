import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data.csv")

num_df = df.drop(columns=["date"])

corr = num_df.corr(method="pearson")

mask = np.triu(np.ones_like(corr, dtype=bool))

plt.figure(figsize=(12, 8))
sns.heatmap(corr, mask=mask, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("heatmap_masked.png")
plt.close()

sns.pairplot(num_df[["close", "volume", "rsi_14", "macd", "atr_14", "next_day_close"]])
plt.savefig("pairplot.png")
plt.close()

corr_unstack = corr.unstack().sort_values()

print("Top positive correlations:")
print(corr_unstack.tail(10))

print("\nTop negative correlations:")
print(corr_unstack.head(10))



