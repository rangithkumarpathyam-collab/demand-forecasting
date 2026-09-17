import matplotlib.pyplot as plt


def plot_forecast(historical, forecast):
    """
    Plot historical demand and future forecast.
    """

    plt.figure(figsize=(12, 6))

    # Historical demand
    plt.plot(
        historical.index,
        historical.values,
        marker="o",
        label="Historical Sales"
    )

    # Forecast
    plt.plot(
        forecast.index,
        forecast["forecast_sales"],
        marker="o",
        linestyle="--",
        label="Forecast"
    )

    plt.title("Demand Forecast")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()