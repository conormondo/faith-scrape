from config import CONFIG
import pandas as pd
import json
import requests
import time

# Constants
GOOGLE_URL = CONFIG.GOOGLE_URL
FILTER_TYPE = CONFIG.FILTER_TYPE
API_KEY = CONFIG.API_KEY
LOCATIONS = CONFIG.LOCATIONS


def call_api(location, phrase):
    # TODO: Handle pagination or separate into larger function
    '''
    Calls api for basic response for places
    returns flattened list of 60 place responses
    '''
    url = GOOGLE_URL + '/textsearch/json'
    params = {
    'query': phrase.lower(),
    'location': ','.join([str(l) for l in location]),
    'radius': 50000,
    'type': FILTER_TYPE,
    'key': str(API_KEY)
    }
    headers = {}
    responses = []
    # initial api call
    r = requests.get(url, headers=headers, params=params)
    next_page = r.json().get('next_page_token', None)
    responses.append(r.json().get('results'))
    while next_page:
        params = {}
        params['pagetoken'] = next_page
        params['key'] = str(API_KEY)
        time.sleep(2)
        r2 = requests.get(url, headers=headers, params=params)
        next_page = r2.json().get('next_page_token', None)
        results = r2.json().get('results', None)
        status = r2.json().get('status')
        if status != 'OK':
            print('Irregular Status {status}: {phrase}/{location}')
        responses.append(results)

    print(f'Responses from {len(responses)} pages.')
    flat_list = [place for page in responses for place in page]
    return flat_list

def get_place_details(p_id):
    '''
    Returns dict with fields_to_return as keys
    Currently meant to be called for every church result found
    '''
    fields_to_return = [
    'place_id',
    'formatted_phone_number',
    'website'
    ]
    url = GOOGLE_URL + '/details/json'
    params = {
    'place_id': str(p_id),
    'fields': ','.join(fields_to_return),
    'key': str(API_KEY)
    }
    headers = {}
    r = requests.get(url, headers=headers, params=params)
    response_json = r.json()
    if response_json.get('status') == 'OK':
        return r.json().get('result', None)
    else:
        return None

def get_all_details(*p_ids):
    '''Takes list of place ids and returns list of detail results'''
    arr = [get_place_details(i) for i in p_ids]
    return arr

def load_data():
    with open('response.json', 'r') as file:
        data = json.load(file)
    return data

def collect_fields(*responses):
    '''Takes unpacked list of json objects'''
    fields_to_collect = [
        'place_id',
        'name',
        'business_status',
        'formatted_address',
        # 'geometry',
        # 'icon',
        # 'icon_background_color',
        # 'icon_mask_base_uri',
        # 'opening_hours',
        # 'photos',
        # 'plus_code',
        # 'rating',
        # 'reference',
        'types',
        'user_ratings_total'
        ]
        # Empty dict for api fields
    fields = {key:list() for key in fields_to_collect}
    # Populates dict with data from response
    for response in responses:
        for key in fields.keys():
            fields[key].append(response.get(key, None))

    return fields

def do_locational_search(location, *phrases):
    ''' Calls api for a location with list of phrases'''
    search_list = []
    for phrase in phrases:
        print(f'Searching for {phrase} places at {location}...')
        # Gets places
        responses = call_api(location, phrase)
        dict = collect_fields(*responses)
        search_list.append(dict)
        print(f'{phrase} search finished...')
    return search_list

def lookup_details(main_frame):
    '''
    Takes main frame, calls the api for every unique place ID.
    Returns frame with details.'''

    main_frame.drop_duplicates(subset='place_id', inplace=True)
    id_list = main_frame['place_id'].to_list()
    print(f'Looking up details for {len(id_list)} places.')
    details = get_all_details(*id_list)
    details_frame = pd.DataFrame(details)
    merged = pd.merge(
                    left=main_frame,
                    right=details_frame,
                    on='place_id',
                    how='left')
    return merged


def main():
    # TODO: Setup phrases, locations in setting
    # TODO: Bring back in webb zip codes
    # TODO: have main file be reread to filter out ZIPCODES
    phrases = ['Catholic', 'Baptist']
    locations = [(31.143277, -97.41826)]
    search_list = [] # list of dicts

    # Process
    for location in locations:
        search = do_locational_search(location, *phrases)
        for place in search:
            search_list.append(place)

    # Makes a list of dataframes from list of dicts
    df_list = [pd.DataFrame(s) for s in search_list]
    df_all = pd.concat(df_list)
    with_details = lookup_details(df_all)
    if not with_details.empty:
        with_details.to_csv('main_data.csv', index=False)

if __name__ == '__main__':
    main()
