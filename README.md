# Most Active Cookie

## Running the Code
Given a cookie log file, the most active cookie for a specified day can be retrieved by executing the most_active_cooke program. An example is shown below: <br>

`python3 most_active_cookie.py cookie_log.csv -d 2018-12-09`

To run the unit tests associated with the program, run the following command: <br>
`python3 testing.py`

## File Contents
* `most_active_cookie.py` - reads in arguments and outputs the most active cookie(s) to the console
* `parse_helpers.py` - file containing custom-made helper functions used to parse csv and cli inputs
* `CookieLog.py` - contains the CookieLog class which stores information about the number of cookies referenced in the cookie log per day
* `testing.py` - contains unit tests used to verify code functionality and error edge cases
*` test_data` - a folder with sample inputs used in `testing.py`