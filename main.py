import utils
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def root():
    return RedirectResponse(url="/docs/")


@app.get("/allBerryStats")
def get_berries_stats():
    names_list = utils.get_berries_names()
    growth_time_list = utils.get_growth_times(names_list)

    return {
        "berries_names": names_list,
        "min_growth_time": utils.get_min_growth_time(growth_time_list),
        "median_growth_time": utils.get_median_growth_time(growth_time_list),
        "max_growth_time": utils.get_max_growth_time(growth_time_list),
        "variance_growth_time": utils.get_variance_growth_time(growth_time_list),
        "mean_growth_time": utils.get_mean_growth_time(growth_time_list),
        "frequency_growth_time": utils.get_growth_time_frequencies(growth_time_list)
    }


@app.get("/histogram", response_class=HTMLResponse)
def get_frequency_histogram():
    return utils.generate_histogram()


