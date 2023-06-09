from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

from app import utils


app = FastAPI(
    title="Berries Stats API",
)


@app.get("/")
async def root():
    """Endpoint to redirecting main root to docs"""
    return RedirectResponse(url="/docs/")


@app.get("/allBerryStats")
async def get_berries_stats():
    """Endpoint to get berries statistics"""
    berries_dict = utils.get_berries_data()
    growth_time_list = utils.get_growth_times(list(berries_dict.values()))

    return {
        "berries_names": list(berries_dict.keys()),
        "min_growth_time": utils.get_min_growth_time(growth_time_list),
        "median_growth_time": utils.get_median_growth_time(growth_time_list),
        "max_growth_time": utils.get_max_growth_time(growth_time_list),
        "variance_growth_time": utils.get_variance_growth_time(growth_time_list),
        "mean_growth_time": utils.get_mean_growth_time(growth_time_list),
        "frequency_growth_time": utils.get_growth_time_frequencies(growth_time_list),
    }


@app.get("/histogram", response_class=HTMLResponse)
async def get_frequency_histogram():
    """Endpoint to generate histogram of frequency growth times"""
    return utils.generate_histogram()
