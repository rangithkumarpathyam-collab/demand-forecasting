import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from features import create_features

df = pd.read_csv("sales.csv")

df = create_features(df)

features = ["day", "month", "day_of_week", "lag_1", "lag_7"]

X = df[features]
y = df["sales"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model trained and saved successfully!")

last_row = df.iloc[-1]

predictions = []

lag_1 = last_row["sales"]
lag_7 = df.iloc[-7]["sales"]

last_date = last_row["date"]

for i in range(1, 8):
    future_date = last_date + pd.Timedelta(days=i)

    new_data = pd.DataFrame([{
        "day": future_date.day,
        "month": future_date.month,
        "day_of_week": future_date.dayofweek,
        "lag_1": lag_1,
        "lag_7": lag_7
    }])

    prediction = model.predict(new_data)[0]

    predictions.append(prediction)

    lag_7 = lag_1
    lag_1 = prediction

print("\nNext 7 Days Prediction:")

for i, prediction in enumerate(predictions, 1):
    print("Day", i, ":", round(prediction, 2))


# Create forecast graph

future_dates = [
    last_date + pd.Timedelta(days=i)
    for i in range(1, 8)
]

plt.figure(figsize=(10, 5))

plt.plot(
    future_dates,
    predictions,
    marker="o"
)

plt.title("Next 7 Days Demand Forecast")
plt.xlabel("Date")
plt.ylabel("Predicted Sales")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()

plt.savefig("forecast.png")

plt.show()

print("\nForecast graph saved as forecast.png")