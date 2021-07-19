# Read every line of the file.
# Split each line into a list of values.
# Extract the column names.
# Use the column names and lists to create a dictionary.
# Filter out the rounds you aren’t interested in.
# Calculate the total and average values for the rounds you are interested in.

file_name = "techcrunch.csv"
lines = (line for line in open(file_name))
list_line = (line.rstrip().split(",") for line in lines)
cols = next(list_line)
company_dicts = (dict(zip(cols, data)) for data in list_line)
funding = (
    int(company_dict["raisedAmt"])
    for company_dict in company_dicts
    if company_dict["round"] == "a"
)
total_series_a = sum(funding)
