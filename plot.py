import pandas as pd
import matplotlib.pyplot as plt

algo, date = "ppo", "20230530-232400"
results = pd.read_csv(f"./solutions/{algo}/{date}/logs/results.csv")
print(results.head())

results.plot(y=["total_fitness", "height_diff", "distance"], kind='line')
plt.show()