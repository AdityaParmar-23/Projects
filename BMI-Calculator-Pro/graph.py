import matplotlib.pyplot as plt


def show_graph(data, username):
    """
    Display BMI history as a line chart.
    """

    if not data:
        return False

    bmi_values = [row[0] for row in data]
    dates = [row[1] for row in data]

    plt.style.use("dark_background")

    figure, axis = plt.subplots(figsize=(10, 5.5))

    figure.patch.set_facecolor("#111827")
    axis.set_facecolor("#111827")

    axis.plot(
        dates,
        bmi_values,
        marker="o",
        markersize=7,
        linewidth=2.5,
        label="BMI"
    )

    # BMI reference levels
    axis.axhline(
        y=18.5,
        linestyle="--",
        linewidth=1.2,
        alpha=0.7
    )

    axis.axhline(
        y=25,
        linestyle="--",
        linewidth=1.2,
        alpha=0.7
    )

    axis.axhline(
        y=30,
        linestyle="--",
        linewidth=1.2,
        alpha=0.7
    )

    axis.set_title(
        f"{username} — BMI Trend",
        fontsize=17,
        fontweight="bold",
        pad=15
    )

    axis.set_xlabel(
        "Recorded Date",
        fontsize=11
    )

    axis.set_ylabel(
        "BMI",
        fontsize=11
    )

    axis.grid(
        True,
        alpha=0.2
    )

    axis.legend()

    figure.autofmt_xdate()

    figure.tight_layout()

    plt.show()

    return True