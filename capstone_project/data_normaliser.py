import sqlite3

# Database
raw_sqlite_connection = sqlite3.connect("capstone.sqlite")
raw_cursor = raw_sqlite_connection.cursor()
normalised_sqlite_connection = sqlite3.connect("capstone_normalised.sqlite")
normalised_cursor = normalised_sqlite_connection.cursor()

# Make some fresh tables using executescript()
normalised_cursor.executescript(
    """
    DROP TABLE IF EXISTS migrations;
    DROP TABLE IF EXISTS employment_ratios;
    DROP TABLE IF EXISTS dwelling_numbers;
    DROP TABLE IF EXISTS dwelling_prices;
    DROP TABLE IF EXISTS regions;

    CREATE TABLE migrations (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        time_period INTEGER,
        value INTEGER,
        region_id INTEGER
    );

    CREATE TABLE employment_ratios (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        time_period CHAR(255),
        ratio DECIMAL(10,2),
        region_id INTEGER
    );

    CREATE TABLE dwelling_numbers (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        time_period INTEGER,
        number_of_dwellings INTEGER,
        region_id INTEGER
    );

    CREATE TABLE dwelling_prices (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        time_period INTEGER,
        mean_price DECIMAL(10,1),
        region_id INTEGER
    );
                     
    CREATE TABLE regions (
        id CHAR(255),
        name CHAR(255)
    );
"""
)


def group_data(data_rows, data_type):
    # Dwellings:            data_dictionary: {year: {region: [(value1, value2), ...]}
    # Employment Ratios:    data_dictionary: {year: {region: [value, ...]}
    data_dictionary = dict()

    for row in data_rows:
        row_value = None
        if data_type == "employment_ratios":
            _, time_period, ratio, region_id = row
            row_value = ratio
        elif data_type == "dwellings":
            _, time_period, number_of_dwellings, mean_price, region_id = row
            row_value = (number_of_dwellings, mean_price)
        else:
            return

        year = time_period.split("-")[0]

        if year in data_dictionary:
            if region_id in data_dictionary[year]:
                data_dictionary[year][region_id].append(row_value)
            else:
                data_dictionary[year][region_id] = []
                data_dictionary[year][region_id].append(row_value)
        else:
            data_dictionary[year] = dict()
            data_dictionary[year][region_id] = []
            data_dictionary[year][region_id].append(row_value)

    return data_dictionary


def average_data(data_dictionary, data_type):
    averaged_data_dictionary = {}
    for year in data_dictionary:
        regions = data_dictionary[year]
        for region in regions:
            if data_type == "dwellings":
                values_list = data_dictionary[year][region]
                number_of_dwellings = []
                mean_prices = []
                for values_tuple in values_list:
                    number_of_dwellings.append(values_tuple[0])
                    mean_prices.append(values_tuple[1])
                averaged_number_of_dwellings = sum(number_of_dwellings) / len(
                    number_of_dwellings
                )
                averaged_mean_price = sum(mean_prices) / len(mean_prices)
                averaged_values = (averaged_number_of_dwellings, averaged_mean_price)

                print(
                    f"    Averaging {year}, region {region} -> dwellings: {averaged_number_of_dwellings}, price: {averaged_mean_price}"
                )

            elif data_type == "employment_ratios":
                values_list = data_dictionary[year][region]
                averaged_values = sum(values_list) / len(values_list)

                print(
                    f"    Averaging {year}, region {region} -> ratio: {averaged_values}"
                )

            if year in averaged_data_dictionary:
                averaged_data_dictionary[year][region] = averaged_values
            else:
                averaged_data_dictionary[year] = dict()
                averaged_data_dictionary[year][region] = averaged_values

    return averaged_data_dictionary


# Normalise dwellings
#   time_period: quarter -> year
print("Normalising dwellings...")

raw_cursor.execute(
    "SELECT id, time_period, number_of_dwellings, mean_price, region_id FROM dwellings ORDER BY region_id, time_period"
)
dwellings_rows = raw_cursor.fetchall()
data_dictionary = group_data(dwellings_rows, "dwellings")
averaged_data_dictionary = average_data(data_dictionary, "dwellings")

for year in averaged_data_dictionary:
    regions = averaged_data_dictionary[year]
    for region in regions:
        number_of_dwellings = regions[region][0]
        mean_price = regions[region][1]
        print(
            f"    Inserting number of dwellings ({number_of_dwellings}) and mean price ({mean_price}) into databases... YEAR: {year}, REGION: {region}"
        )

        normalised_cursor.execute(
            """INSERT OR IGNORE INTO dwelling_numbers (time_period, number_of_dwellings, region_id)
                        VALUES (?, ?, ?)""",
            (year, number_of_dwellings, region),
        )
        normalised_cursor.execute(
            """INSERT OR IGNORE INTO dwelling_prices (time_period, mean_price, region_id)
                        VALUES (?, ?, ?)""",
            (year, mean_price, region),
        )

        normalised_sqlite_connection.commit()

# Normalise employment ratios
#   time_period: month -> year
print("Normalising employment ratios...")

raw_cursor.execute(
    "SELECT id, time_period, ratio, region_id FROM employment_ratios ORDER BY region_id, time_period"
)
employment_ratios_rows = raw_cursor.fetchall()
data_dictionary = group_data(employment_ratios_rows, "employment_ratios")
averaged_data_dictionary = average_data(data_dictionary, "employment_ratios")

for year in averaged_data_dictionary:
    regions = averaged_data_dictionary[year]
    for region in regions:
        ratio = regions[region]
        print(
            f"    Inserting ratio ({ratio}) into database... YEAR: {year}, REGION: {region}"
        )
        normalised_cursor.execute(
            """INSERT OR IGNORE INTO employment_ratios (time_period, ratio, region_id)
                        VALUES (?, ?, ?)""",
            (year, ratio, region),
        )

        normalised_sqlite_connection.commit()

# Normalise migrations
print("Normalising migrations...")

raw_cursor.execute(
    "SELECT id, time_period, value, region_id FROM migrations ORDER BY time_period, region_id"
)
migrations_ratios_rows = raw_cursor.fetchall()

for row_data in migrations_ratios_rows:
    year = row_data[1]
    value = row_data[2]
    region = row_data[3]
    print(
        f"    Inserting value ({value}) into database... YEAR: {year}, REGION: {region}"
    )
    normalised_cursor.execute(
        """INSERT OR IGNORE INTO migrations (time_period, value, region_id)
                        VALUES (?, ?, ?)""",
        (year, value, region),
    )

    normalised_sqlite_connection.commit()

# Normalise regions
print("Normalising regions...")

raw_cursor.execute("SELECT id, name FROM regions ORDER BY id")
regions_rows = raw_cursor.fetchall()

for row_data in regions_rows:
    id = row_data[0]
    name = row_data[1]
    print(f"    Inserting name ({name}) into database... ID: {id}")
    normalised_cursor.execute(
        """INSERT OR IGNORE INTO regions (id, name)
                        VALUES (?, ?)""",
        (id, name),
    )

    normalised_sqlite_connection.commit()

raw_sqlite_connection.close()
normalised_sqlite_connection.close()
