import json
import statistics
import requests
import io
import base64
import matplotlib.pyplot as plot
from collections import Counter


def get_content(url: str) -> dict:
    """Get the content on given URl"""
    response = requests.get(url)
    return json.loads(response.content.decode("utf-8"))


def get_berries_data() -> dict:
    """
    This function process the content and return a dictionary with the
    following structure:
    {"cheri": "https://pokeapi.co/api/v2/berry/1/", ...}
    """
    count = get_berries_count()
    url = f"https://pokeapi.co/api/v2/berry?offset=0&limit={count}"
    content = get_content(url)
    return {item["name"]: item["url"] for item in content["results"]}


def get_berries_count() -> int:
    """Request to pokeapi to get the count of all berrie objects"""
    url = "https://pokeapi.co/api/v2/berry"
    content = get_content(url)
    return content["count"]


def get_growth_times(urls: list) -> list:
    """
    Request the expanded content on every url received and return
    a list with integers representing the growth time of the berries
    """
    growth_time_list = []
    for url in urls:
        content = get_content(url)
        growth_time_list.append(content["growth_time"])

    return growth_time_list


def get_max_growth_time(growth_time_list: list) -> int:
    """
    Receives a list with the following structure: [1, 2, 3, 4, 5]
    and return the max number of the list: 5
    """
    return max(growth_time_list)


def get_median_growth_time(growth_time_list: list) -> float:
    """
    Receives a list with the following structure: [1, 2, 3, 4, 5]
    and return the median number of the list: 3.0
    """
    return float(statistics.median(growth_time_list))


def get_min_growth_time(growth_time_list: list) -> int:
    """
    Receives a list with the following structure: [1, 2, 3, 4, 5]
    and return the median number of the list: 1
    """
    return min(growth_time_list)


def get_variance_growth_time(growth_time_list: list) -> float:
    """
    Receives a list with the following structure: [1, 2, 3, 4, 5]
    and return the variance of the list: 2.5
    """
    return statistics.variance(growth_time_list)


def get_mean_growth_time(growth_time_list: list) -> float:
    """
    Receives a list with the following structure: [1, 2, 3, 4, 5]
    and return the mean of the list: 3.0
    """
    return statistics.mean(growth_time_list)


def get_growth_time_frequencies(growth_time_list: list) -> Counter:
    """
    Receives a list with the following structure: [1, 2, 3, 4, 5]
    and return the appearances of every value: Counter({1: 1, 2: 1, 3: 1, 4: 1, 5: 1})
    """
    return Counter(growth_time_list)


def generate_histogram() -> str:
    """
    Generates a histogram with data based on the PokeAPI,
    returns a plain html file with the image of the histogram.
    """
    n_list = get_growth_times(
        list(get_berries_data().values())
    )

    intervals = range(min(n_list), max(n_list) + 2)
    plot.hist(x=n_list, bins=intervals, color="#F2AB6D", rwidth=0.85)
    plot.title("Histogram of frequencies")
    plot.xlabel("Growth times")
    plot.ylabel("Frequency")
    plot.xticks(intervals)

    buffer = io.BytesIO()
    plot.savefig(buffer, format="png")
    buffer.seek(0)

    fig_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return generate_html(fig_base64)


def generate_html(fig_base64: str) -> str:
    """A string that represents a html is formatted, adding the argument in the img tag"""
    return (
        f"<html><head><title>Histogram</title></head><body>"
        f'<img src="data:image/png;base64,{fig_base64}"></body></html>'
    )
