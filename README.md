# BerriesStatsAPI

This API generates berry growing time statistics with data based on the PokeAPI url:
https://pokeapi.co/docs/v2#berries

## API on heroku

You can visit the deployed BerriesStatsAPI on http://berries-stats.herokuapp.com/docs to test it online, or test it locally by following the next steps

### Requirements
- Python (v3.8 or higher)
- pip

### Installation to run locally

1. Clone this repository.
2. Install the dependendices with the following command:

`pip install -r requirements.txt`

### Usage
1. Run the server with the following command:

`uvicorn app.main:app --host 0.0.0.0 --port 8000`

2. Acces the API in your web browser at the http://localhost:8000 URL.
3. You will be redirected to the `/docs` path where you can test the available API endpoints
4. To view the generated histogram, enter the url: http://localhost:8000/histogram in your browser
5. To stop the server, press CTRL + C in the terminal.

### Endpoints

- **GET** "/": Redirect to `/docs` enpoint
- **GET** "/allBerriesStats": Returns a JSON with the following structure:
```
{

    "berries_names": [...],

    "min_growth_time": "" // time, int

    "median_growth_time": "", // time, float

    "max_growth_time": "" // time, int

    "variance_growth_time": "" // time, float

    "mean_growth_time": "", // time, float

    "frequency_growth_time": "", // time, {growth_time: frequency, ...}

}
```
- **GET** "/histogram": returns a plain html with a PokeAPI data histogram of berry growth times

### TESTING

1. To test the project just run the following command on the root directory: `pytest`


