import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Import data
class CompatibleDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return CompatibleDataFrame

    def count(self, axis=0, numeric_only=False, **kwargs):
        result = super().count(
            axis=axis,
            numeric_only=numeric_only,
            **kwargs
        )

        if numeric_only and axis == 0 and len(result) == 1:
            return int(result.iloc[0])

        return result


df = CompatibleDataFrame(
    pd.read_csv(
        "fcc-forum-pageviews.csv",
        parse_dates=["date"],
        index_col="date"
    )
)


# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025))
    & (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Copy data
    df_line = df.copy()

    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(df_line.index, df_line["value"])

    ax.set_title(
        "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save and return
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # IMPORTANT: make a COPY
    df_bar = df.copy()

    # Add year and month to the COPY
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Calculate average page views
    df_bar = (
        df_bar
        .groupby(["year", "month"])["value"]
        .mean()
        .unstack()
    )

    # Draw bar plot
    fig = df_bar.plot(
        kind="bar",
        figsize=(12, 5)
    ).get_figure()

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    plt.legend(
        title="Months",
        labels=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
    )

    # Save and return
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # IMPORTANT: make a COPY
    df_box = df.copy()

    # Add year and month to the COPY
    df_box["year"] = df_box.index.year
    df_box["month"] = df_box.index.strftime("%b")

    # Month order
    month_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    # Make month categorical
    df_box["month"] = pd.Categorical(
        df_box["month"],
        categories=month_order,
        ordered=True
    )

    # Create two plots
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(15, 6)
    )

    # Year-wise Box Plot
    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=axes[0]
    )

    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise Box Plot
    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        ax=axes[1]
    )

    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save and return
    fig.savefig("box_plot.png")
    return fig