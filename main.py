from _config import CONFIG
import pandas as pd
from _helpers import do_locational_search, lookup_details, check_zip_codes

# Constants
LOCATIONS = CONFIG.SEARCH_LOCATIONS
PHRASES = CONFIG.PHRASES

def main():
    ''' Goes through each location, calls each place search phrase.'''
    
    search_list = [] # list of dicts

    # Process
    for location in LOCATIONS:
        search = do_locational_search(location, *PHRASES)
        for place in search:
            search_list.append(place)

    # Makes a list of dataframes from list of dicts
    df_list = [pd.DataFrame(s) for s in search_list]
    df_all = pd.concat(df_list)
    df_all.to_csv('without_duplicates_removed.csv', index=False) # Writes
    with_details = lookup_details(df_all)
    if not with_details.empty:
        with_details.to_csv('without_zip_code_verification.csv', index=False) # Writes
        in_area = check_zip_codes(with_details)
        in_area.to_csv('main_report.csv', index=False)
    

if __name__ == '__main__':
    main()
