import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from features import create_features

df = pd.read_csv("sales.csv")

df = create_features(df)

features = ["day", "month", "day_of_week", "lag_1", "lag_7"]

X = df[features]
y = df["sales"]

split = int(len(df) * 0.8)

X_train = X[:split]
X_test = X[split:]

y_train = y[:split]
y_test = y[split:]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(mean_squared_error(y_test, predictions))

mape = np.mean(
    np.abs((y_test - predictions) / y_test)
) * 100

print("Model Evaluation")
print("----------------")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("MAPE:", round(mape, 2), "%")


# Actual vs Predicted graph

test_dates = df["date"].iloc[split:]

plt.figure(figsize=(10, 5))

plt.plot(
    test_dates,
    y_test,
    marker="o",
    label="Actual"
)

plt.plot(
    test_dates,
    predictions,
    marker="o",
    label="Predicted"
)

plt.title("Actual vs Predicted Sales")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()

plt.savefig("actual_vs_predicted.png")

plt.show()

print("\nActual vs Predicted graph saved as actual_vs_predicted.png")