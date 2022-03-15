# Custom parsing functions (by Bryce Wong)
from parse_helpers import parse_time, parse_csv

class CookieLog:    

    ### Initialize parameters for CookieLog instance ###
    def __init__(self):
        # cookie_map stores a mapping between timestamps and a {cookie: count_ref} map for each day
        self.cookie_map = {}

        # checks if CookieLog has loaded in some information
        self.initialized = False
    
    ### Adds 1 to the cookie's count_ref in the corresponding timestamp entry ###
    def add_to_map(self, cookie, timestamp):
        # initialize new timestamp in cookie_map if it does not exist
        if timestamp not in self.cookie_map:
            self.cookie_map[timestamp] = {}

        # get corresponding timestamp entry in cookie_map
        time_entry = self.cookie_map[timestamp]
        
        # add 1 to specified cookie's ref count under corresponding time_entry, init if needed
        if cookie not in time_entry:
            time_entry[cookie] = 0
        time_entry[cookie] += 1

    ### Takes in a cookie log file, parses it, and updates cookie_map with new ref counts for each timestamp ###
    def add_cookies_from_file(self, file_name):
        # extract cookie, timestamp information from csv input file
        entries = parse_csv(file_name)

        # separate into cookie/timestamp components
        cookies = entries["cookie"]
        timestamps = [parse_time(e)[0] for e in entries["timestamp"]]
        
        # add each (cookie, timestamp) pair to the cookie_map
        for c, t in zip(cookies, timestamps):
            self.add_to_map(c, t)

        # CookieLog is now initialized with some data
        self.initialized = True

    ### Takes in a date and returns the most active cookie(s) on that timestamp ###
    def most_active_cookie(self, date):
        # Check if data exists in the CookieLog instance
        assert self.initialized, "CookieLog contains no data"

        time_entry = self.cookie_map.get(date, None)

        # Only outputs values if there are cookies for that timestamp
        if time_entry:
            highest_count = max(time_entry.values())
            matching_cookies = [c for c in time_entry if time_entry[c] == highest_count]
            
            # Return output string with all cookies a on new line
            return "\n".join(matching_cookies)

        # Timestamp does not exist in CookieLog instance
        assert False, "Date not present in CookieLog"