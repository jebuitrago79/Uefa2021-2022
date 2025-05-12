import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

df = pd.read_csv("Player_Equipos_Europeos2021_22.csv")

metricas = ["overall", "pace", "shooting", "defending", "physic", "power_shot_power"]
df_metricas = df[metricas].dropna()

correlation_matrix = df_metricas.corr()
plt.figure(figsize=(10, 7))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Matriz de Correlación de Métricas FIFA 2021-2022")
plt.tight_layout()
plt.show()

X = df_metricas.drop(columns=["overall"])
y = df_metricas["overall"]

X_const = sm.add_constant(X)
model = sm.OLS(y, X_const).fit()

print(model.summary())
