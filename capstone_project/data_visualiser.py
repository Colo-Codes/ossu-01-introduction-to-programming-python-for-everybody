import sqlite3
import json

# Database
sqlite_connection = sqlite3.connect("capstone_normalised.sqlite")
cursor = sqlite_connection.cursor()

# 2d Chart Colours:
# - Migrations: navy
# - Employment ratios: chocolate
# - Dwelling quantities: green
# - Dwelling prices: limegreen

# Migrations
cursor.execute(
    """SELECT time_period, value, regions.name AS region_name FROM migrations
               JOIN regions ON migrations.region_id = regions.id"""
)
migration_rows = cursor.fetchall()

trace1 = dict()
trace1["x"] = []
trace1["y"] = []
trace_3d_migrations = dict()
trace_3d_migrations["data"] = []
states = []

print("Processing Migration data")

for migration in migration_rows:
    trace_3d_migrations["data"].append({"x": [], "y": [], "z": []})
    iteration_state = migration[2]

    if iteration_state not in states:
        states.append(iteration_state)

    index = states.index(iteration_state)

    if migration[2] == "Australia":
        trace1["x"].append(int(migration[0]))
        trace1["y"].append(migration[1])
        trace1["name"] = "Migrations in " + migration[2]
        trace1["type"] = "scatter"
        trace1["line"] = {"color": "navy"}
    else:
        trace_3d_migrations["data"][index]["x"].append(
            [migration[2], migration[2] + " "]
        )
        trace_3d_migrations["data"][index]["y"].append(
            [int(migration[0]), int(migration[0])]
        )
        trace_3d_migrations["data"][index]["z"].append([migration[1], migration[1]])

# Employment Ratios
cursor.execute(
    """SELECT time_period, ratio, regions.name AS region_name FROM employment_ratios
               JOIN regions ON employment_ratios.region_id = regions.id"""
)
employment_rows = cursor.fetchall()

trace2 = dict()
trace2["x"] = []
trace2["y"] = []
trace_3d_employment = dict()
trace_3d_employment["data"] = []

print("Processing Employment Ratio data")

for ratio in employment_rows:
    trace_3d_employment["data"].append({"x": [], "y": [], "z": []})
    iteration_state = ratio[2]

    if iteration_state not in states:
        states.append(iteration_state)

    index = states.index(iteration_state)

    if ratio[2] == "Australia":
        trace2["x"].append(int(ratio[0]))
        trace2["y"].append(ratio[1])
        trace2["name"] = "Employment Ratio in " + ratio[2]
        trace2["type"] = "scatter"
        trace2["yaxis"] = "y2"
        trace2["line"] = {"color": "chocolate"}
    else:
        trace_3d_employment["data"][index]["x"].append([ratio[2], ratio[2] + " "])
        trace_3d_employment["data"][index]["y"].append([int(ratio[0]), int(ratio[0])])
        trace_3d_employment["data"][index]["z"].append([ratio[1], ratio[1]])

# Dwelling Numbers
cursor.execute(
    """SELECT time_period, number_of_dwellings, regions.name AS region_name FROM dwelling_numbers
               JOIN regions ON dwelling_numbers.region_id = regions.id"""
)
dwelling_numbers_rows = cursor.fetchall()

trace3 = dict()
trace3["x"] = []
trace3["y"] = []
trace_3d_dwelling_numbers = dict()
trace_3d_dwelling_numbers["data"] = []

print("Processing Dwelling Quantity data")

for number_of_dwellings in dwelling_numbers_rows:
    trace_3d_dwelling_numbers["data"].append({"x": [], "y": [], "z": []})
    iteration_state = number_of_dwellings[2]

    if iteration_state not in states:
        states.append(iteration_state)

    index = states.index(iteration_state)

    if number_of_dwellings[2] == "Australia":
        trace3["x"].append(int(number_of_dwellings[0]))
        trace3["y"].append(number_of_dwellings[1])
        trace3["name"] = "Dwelling Quantity in " + number_of_dwellings[2]
        trace3["type"] = "scatter"
        trace3["yaxis"] = "y3"
        trace3["line"] = {"color": "green"}
    else:
        trace_3d_dwelling_numbers["data"][index]["x"].append(
            [number_of_dwellings[2], number_of_dwellings[2] + " "]
        )
        trace_3d_dwelling_numbers["data"][index]["y"].append(
            [int(number_of_dwellings[0]), int(number_of_dwellings[0])]
        )
        trace_3d_dwelling_numbers["data"][index]["z"].append(
            [number_of_dwellings[1], number_of_dwellings[1]]
        )

# Dwelling Prices
cursor.execute(
    """SELECT time_period, mean_price, regions.name AS region_name FROM dwelling_prices
               JOIN regions ON dwelling_prices.region_id = regions.id"""
)
dwelling_prices_rows = cursor.fetchall()

trace4 = dict()
trace4["x"] = []
trace4["y"] = []
trace_3d_dwelling_prices = dict()
trace_3d_dwelling_prices["data"] = []

print("Processing Dwelling Mean Price data")

for mean_price in dwelling_prices_rows:
    trace_3d_dwelling_prices["data"].append({"x": [], "y": [], "z": []})
    iteration_state = mean_price[2]

    if iteration_state not in states:
        states.append(iteration_state)

    index = states.index(iteration_state)

    if mean_price[2] == "Australia":
        trace4["x"].append(int(mean_price[0]))
        trace4["y"].append(mean_price[1])
        trace4["name"] = "Dwelling Mean Price in " + mean_price[2]
        trace4["type"] = "scatter"
        trace4["yaxis"] = "y4"
        trace4["line"] = {"color": "limegreen"}
    else:
        trace_3d_dwelling_prices["data"][index]["x"].append(
            [mean_price[2], mean_price[2] + " "]
        )
        trace_3d_dwelling_prices["data"][index]["y"].append(
            [int(mean_price[0]), int(mean_price[0])]
        )
        trace_3d_dwelling_prices["data"][index]["z"].append(
            [mean_price[1], mean_price[1]]
        )

print("Storing processed data in charts.js file")

file_handle = open("charts.js", "w")
file_handle.write("trace1 = ")
file_handle.write(json.dumps(trace1))
file_handle.write("\n")
file_handle.write("trace2 = ")
file_handle.write(json.dumps(trace2))
file_handle.write("\n")
file_handle.write("trace3 = ")
file_handle.write(json.dumps(trace3))
file_handle.write("\n")
file_handle.write("trace4 = ")
file_handle.write(json.dumps(trace4))
file_handle.write("\n")

file_handle.write("trace_3d_migrations = ")
file_handle.write(json.dumps(trace_3d_migrations))
file_handle.write("\n")
file_handle.write("trace_3d_employment = ")
file_handle.write(json.dumps(trace_3d_employment))
file_handle.write("\n")
file_handle.write("trace_3d_dwelling_numbers = ")
file_handle.write(json.dumps(trace_3d_dwelling_numbers))
file_handle.write("\n")
file_handle.write("trace_3d_dwelling_prices = ")
file_handle.write(json.dumps(trace_3d_dwelling_prices))
file_handle.write("\n")

print("Charts ready to be visualised. \n\tOpen charts.htm file in your browser.")

cursor.close()
file_handle.close()
