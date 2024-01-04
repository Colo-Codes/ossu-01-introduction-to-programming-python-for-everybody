# Statistics to get out of this script:
#
# - Migration
#   - Year with highest migration
#   - Year with lowest migration
#   - Average Migration per year
#   - Average Migration per state
# - Employment ratio
#   - Year with highest employment ratio
#   - Year with lowest employment ratio
#   - Average employment ratio per year
#   - Average employment ratio per state
# - Dwellings (quantity)
#   - Year with highest dwellings number
#   - Year with lowest dwellings number
#   - Average dwellings number per year
# - Dwellings (price)
#   - Year with highest dwelling price
#   - Year with lowest dwelling price
#   - Average dwelling price per year

import sqlite3

# Database
sqlite_connection = sqlite3.connect("capstone_normalised.sqlite")
cursor = sqlite_connection.cursor()


def process_data(rows):
    processed_data = dict()
    highest_year_data = None
    lowest_year_data = None
    year_data = None
    state_data = None

    for row_data in rows:
        year, value, state = row_data
        value = int(value)

        if (
            highest_year_data == None
            and lowest_year_data == None
            and year_data == None
            and state_data == None
        ):
            highest_year_data = (year, value)
            lowest_year_data = (year, value)
            year_data = [value]
            state_data = [(state, value)]
        else:
            if value > highest_year_data[1]:
                highest_year_data = (year, value)
            elif value < lowest_year_data[1]:
                lowest_year_data = (year, value)
            year_data.append(value)
            state_data.append((state, value))

    average_year_data = int(sum(year_data) / len(year_data))

    average_state_data = dict()
    for state_data in state_data:
        state_name = state_data[0]
        state_value = state_data[1]
        if state_name in average_state_data:
            average_state_data[state_name].append(state_value)
        else:
            average_state_data[state_name] = []
            average_state_data[state_name].append(state_value)

    for state_data in average_state_data:
        value_list = average_state_data[state_data]
        average_state_data[state_data] = int(sum(value_list) / len(value_list))

    processed_data["highest_year"] = highest_year_data
    processed_data["lowest_year"] = lowest_year_data
    processed_data["average_year"] = average_year_data
    processed_data["average_state"] = average_state_data

    return processed_data


def print_data(processed_data, data_type, units):
    highest_year_year = processed_data["highest_year"][0]
    highest_year_value = processed_data["highest_year"][1]
    lowest_year_year = processed_data["lowest_year"][0]
    lowest_year_value = processed_data["lowest_year"][1]
    average_migration_year_value = processed_data["average_year"]
    average_state_data = processed_data["average_state"]

    print("\n    == ---------------------------------------- ==")
    print(f"       {data_type} statistics")
    print("    == ---------------------------------------- ==")
    print(
        f"    Highest {data_type} year was {highest_year_year} with {'{:,}'.format(highest_year_value)} {units}."
    )
    print(
        f"    Lowest {data_type} year was {lowest_year_year} with {'{:,}'.format(lowest_year_value)} {units}."
    )
    print(
        f"        The {data_type} variation between the highest and lowest year is about {'%.2f' % abs(round((highest_year_value / lowest_year_value), 2))} times the lowest year."
    )
    print(
        f"    Average {data_type} per year is {'{:,}'.format(average_migration_year_value)} {units}."
    )
    print(f"    Average {data_type} per state is:")
    for state_data in average_state_data:
        print(
            f"        {state_data}: {'{:,}'.format(average_state_data[state_data])} {units}"
        )


# Migration Statistics
print("Getting migration data from database...")

cursor.execute(
    """SELECT time_period, value, regions.name AS region_name FROM migrations
               JOIN regions ON migrations.region_id = regions.id"""
)
migration_rows = cursor.fetchall()
processed_data = process_data(migration_rows)

data_type = "Migration"
units = "migrations"
print_data(processed_data, data_type, units)


# Employment Statistics
print("\nGetting employment ratios data from database...")

cursor.execute(
    """SELECT time_period, ratio, regions.name AS region_name FROM employment_ratios
               JOIN regions ON employment_ratios.region_id = regions.id"""
)
employment_rows = cursor.fetchall()

processed_data = process_data(employment_rows)

data_type = "Employment Ratio"
units = "%"
print_data(processed_data, data_type, units)

# Dwelling Numbers Statistics
print("\nGetting dwelling numbers data from database...")

cursor.execute(
    """SELECT time_period, number_of_dwellings, regions.name AS region_name FROM dwelling_numbers
               JOIN regions ON dwelling_numbers.region_id = regions.id"""
)
dwelling_rows = cursor.fetchall()
processed_data = process_data(dwelling_rows)

data_type = "Dwelling Number"
units = "(x1000) dwellings"
print_data(processed_data, data_type, units)

# Dwelling Prices Statistics
print("\nGetting dwelling prices data from database...")

cursor.execute(
    """SELECT time_period, mean_price, regions.name AS region_name FROM dwelling_prices
               JOIN regions ON dwelling_prices.region_id = regions.id"""
)
dwelling_rows = cursor.fetchall()
processed_data = process_data(dwelling_rows)

data_type = "Dwelling Mean Prices"
units = "(x1000) AUD"
print_data(processed_data, data_type, units)
