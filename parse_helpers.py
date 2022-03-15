## CLI PARSING HELEPRS ## 

### Takes in a list of arguments and joins entries with flags into tuple pairs
def parse_cli_entries(input):
    cleaned_args = []

    i = 0
    while i < len(input):
        # get current entry
        arg = input[i]

        # process flag/no-flag arguments
        if arg[0] == "-":
            # catch possible errors with flag handling
            assert i + 1 < len(input), "Flag at end of argument chain"
            assert input[i + 1][0] != "-", "Two flags in succession"

            cleaned_args.append((arg, input[i + 1]))
            i += 1
        else:
            cleaned_args.append(arg)
        
        i += 1

    return cleaned_args
        

## CSV PARSING HELPERS ##

### Cleans and separates a .csv row into its individual entry components ###
def split_csv_row(input):
    cleaned_str = input.strip()

    # Only return split row if input is valid
    if cleaned_str:
        return cleaned_str.split(",")

### Splits datetime entry into individual date, time, UTC components ###
def parse_time(input):
    date_time = input.split("T")
    time_utc = date_time[1].split("+")
    return [date_time[0]] + time_utc

### Generates an entry_map containing mappings between a column name and its list of entries ###
def parse_csv(file_name):
    try:
        f = open(file_name)
    except FileNotFoundError:
        assert False, "Invalid file name"

    # get topics from first line of csv, generate initial entry_map
    topics = split_csv_row(f.readline())
    entry_map = {t : [] for t in topics}

    # add all entries of csv file to the entry_map
    curr_line = split_csv_row(f.readline())
    while curr_line:
        for topic, entry in zip(topics, curr_line):
            entry_map[topic].append(entry)
        curr_line = split_csv_row(f.readline())

    f.close()
    return entry_map