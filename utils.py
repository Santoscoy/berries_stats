import json
import statistics
import requests
import io
import base64
import matplotlib.pyplot as plot
from collections import Counter


def get_content(url):
    response = requests.get(url)
    return json.loads(response.content.decode('utf-8'))


def get_berrie_url(name):
    return f"https://pokeapi.co/api/v2/berry/{name}"


def get_berries_names():
    url = "https://pokeapi.co/api/v2/berry"
    content = get_content(url)
    return [item["name"] for item in content["results"]]


def get_growth_times(names_list):
    growth_time_list = []
    for name in names_list:
        url = get_berrie_url(name)
        content = get_content(url)
        growth_time_list.append(content["growth_time"])

    return growth_time_list


def get_max_growth_time(growth_time_list):
    return max(growth_time_list)


def get_median_growth_time(growth_time_list):
    return float(statistics.median(growth_time_list))


def get_min_growth_time(growth_time_list):
    return min(growth_time_list)


def get_variance_growth_time(growth_time_list):
    return statistics.variance(growth_time_list)


def get_mean_growth_time(growth_time_list):
    return statistics.mean(growth_time_list)


def get_growth_time_frequencies(growth_time_list):
    return Counter(growth_time_list)


def generate_histogram():
    n_list = get_growth_times(get_berries_names())

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


def generate_html(fig_base64):
    return f"""
    <html>
        <head>
            <title>Histogram</title>
        </head>
        <body>
            <img src="data:image/png;base64,{fig_base64}">
        </body>
    </html>
    """
