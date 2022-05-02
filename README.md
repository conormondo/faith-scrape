# Faith Scraper

This is a project that was developed to use Google's Place API to find establishements and their details in a specific area. Specifically every single church in Webb County.

NOTE: This is currently a relatively slow report as I needed to stay under the GCP usage free tier.

## Usage
Download Python 3.0+ if not already downloaded. I might go back and make 2.7 formattable.
If pip is installed and you're using a virtual environment, activate that then run the following. 
```
pip install -r requirements.txt
```
Then
```
python main.py
```

## Settings
- **API_KEY**: Your Google Places API key.
- **GOOGLE_URL**: The base google URL for the places API.
- **SEARCH_LOCATIONS**: JSON array of lattitude, longitude pairs
- **ZIP_CODES_TO_CHECK**: Zip codes to filter the end results to once all the details are grabbed from the place details API
- **PHRASES**: All of the different phrases that you would like to to use for each location. Basically the equivalent of using the text search on the google maps website.
- **FILTER_TYPE**: Only return places with this "type" included. List of supported types [here](https://developers.google.com/maps/documentation/places/web-service/supported_types).
- **FIELDS_TO_USE**: The fields you would like the places api to return
- **UNUSED_FIELDS**: The fields returnable by the API that are not being used. To have then returned, move to the "FIELDS_TO_USE" array. However please note that none of these are currently supported with regards to import cleaning / transforming.

## TODO
- This should have been more obejct-oriented. Should rework that before anything else
- Async functionality so that people with their GCP billing down can go wild.