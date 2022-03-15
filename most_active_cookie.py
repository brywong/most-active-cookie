# Permitted additional libraries
import sys # for cli-parsing

# Custom parsing functions + CookieLog class (by Bryce Wong)
from parse_helpers import parse_cli_entries
from CookieLog import CookieLog

def main(args):
    # parse arguments
    args = parse_cli_entries(args)

    # confirm that arguments are valid
    assert len(args) == 2, "Invalid number of arguments"
    assert type(args[0]) != tuple, "First argument has a flag"
    assert type(args[1]) == tuple and args[1][0] == "-d", "Second argument must have -d flag"

    # parse arguments (get file_name, date)
    file_name = args[0]
    date = args[1][1] # (-d, date) tuple pair, get date entry

    # create new CookieLog instance + initialize log information
    cl = CookieLog()
    cl.add_cookies_from_file(file_name)

    # get most active cookie from CookieLog, output to console
    print(cl.most_active_cookie(date))

if __name__ == "__main__":
    main(sys.argv[1:])