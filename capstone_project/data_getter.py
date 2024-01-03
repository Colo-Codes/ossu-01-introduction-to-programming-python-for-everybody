import urllib.request, urllib.parse, urllib.error
import ssl
import xml.etree.ElementTree as ET
import sqlite3

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

service_url = 'https://api.data.abs.gov.au/data/'

# Database
sqlite_connection = sqlite3.connect('capstone.sqlite')
cursor = sqlite_connection.cursor()
# Make some fresh tables using executescript()
cursor.executescript('''
    DROP TABLE IF EXISTS migrations;
    DROP TABLE IF EXISTS employment_ratios;
    DROP TABLE IF EXISTS dwellings;
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

    CREATE TABLE dwellings (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        time_period INTEGER,
        number_of_dwellings INTEGER,
        mean_price DECIMAL(10,1),
        region_id INTEGER
    );
                     
    CREATE TABLE regions (
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        name CHAR(255)
    );
''')

def get_data(query_setup, start_period = True, end_period = False, include_months = False, include_quarters = False):
    START_YEAR = '2011'
    START_MONTH = '01'
    START_QUARTER = 'Q1'
    END_YEAR = '2022'
    END_MONTH = '12'
    END_QUARTER = 'Q4'

    params = dict()
    
    if start_period:
        if include_months:
            params['startPeriod'] = START_YEAR + '-' + START_MONTH
        elif include_quarters:
            params['startPeriod'] = START_YEAR + '-' + START_QUARTER
        else:
            params['startPeriod'] = START_YEAR
    
    if end_period:
        if include_months:
            params['endPeriod'] = END_YEAR + '-' + END_MONTH
        elif include_quarters:
            params['endPeriod'] = END_YEAR + '-' + END_QUARTER
        else:
            params['endPeriod'] = END_YEAR
    
    url = service_url  + query_setup + urllib.parse.urlencode(params)
    print('\nRetrieving...', url)

    url_handle = urllib.request.urlopen(url, context=ctx)
    data = url_handle.read().decode()
    print('Retrieved', len(data), 'characters')

    return data

def parse_data(data, compound_data = False):
    xml_root = ET.fromstring(data)
    # Find all Obs elements under Series
    series_elements = xml_root.findall(".//{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Series")

    output = []

    for series in series_elements:
        series_key = series.findall("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}SeriesKey/{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Value")
        region_value = None
        measure_type = None

        for key in series_key:
            if key.attrib['id'] == 'REGION':
                region_value = key.attrib['value']
            elif compound_data and key.attrib['id'] == 'MEASURE':
                measure_type = key.attrib['value']
        
        obs = series.findall("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Obs")
        for obs_element in obs:
            time_periods_and_values = (obs_element.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsDimension").attrib["value"],
                                        obs_element.find("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsValue").attrib["value"])

            # Insert into database
            if (region_value == None): continue

            time_period, value = time_periods_and_values
            if compound_data:
                output.append((measure_type, region_value, time_period, value))
            else:
                output.append((region_value, time_period, value))
    
    return output

# Net Overseas Migration (per state)
try:
    query_setup = 'ABS,NOM_CY,1.0.0/3.TOT.3..A?'
    start_period = True
    data = get_data(query_setup, start_period)

    parsed_data = parse_data(data)

    for region_id, time_period, value in parsed_data:
        if (region_id == None): continue

        print(f"Inserting into database... REGION: {region_id}, TIME_PERIOD: {time_period}, VALUE: {value}")

        cursor.execute('''INSERT OR IGNORE INTO migrations (time_period, value, region_id) 
        VALUES (?, ?, ?)''', (time_period, value, region_id) )

        sqlite_connection.commit()
except:
    print('ERROR processing: Net Overseas Migration (per state)')

# Employment to population ratio (per state)
try:
    query_setup = 'ABS,LF,1.0.0/M16.3.1599.20..M?'
    start_period = True
    end_period = True
    include_months = True
    data = get_data(query_setup, start_period, end_period, include_months)

    parsed_data = parse_data(data)

    for region_id, time_period, value in parsed_data:
        if (region_id == None): continue

        print(f"Inserting into database... REGION: {region_id}, TIME_PERIOD: {time_period}, VALUE: {value}")

        cursor.execute('''INSERT OR IGNORE INTO employment_ratios (time_period, ratio, region_id) 
        VALUES (?, ?, ?)''', (time_period, value, region_id) )

        sqlite_connection.commit()
except:
    print('ERROR processing: Employment to population ratio (per state)')

# Number of residential dwellings and Mean price of residential dwellings (per state)
try:
    query_setup = 'ABS,RES_DWELL_ST,1.0.0/5+4..Q?'
    start_period = True
    end_period = True
    include_months = False
    include_quarters = True
    data = get_data(query_setup, start_period, end_period, include_months, include_quarters)

    compound_data = True
    parsed_data = parse_data(data, compound_data)
    
    for measure_type, region_id, time_period, value in parsed_data:
        if (region_id == None): continue
        # '4' => number_of_dwellings
        if measure_type != '4': continue

        print(f"Inserting into database... MEASURE TYPE: {measure_type} REGION: {region_id}, TIME_PERIOD: {time_period}, VALUE: {value}")

        cursor.execute('''INSERT OR IGNORE INTO dwellings (time_period, number_of_dwellings, region_id)
                       VALUES (?, ?, ?)''', (time_period, value, region_id) )
        
        sqlite_connection.commit()

    for measure_type, region_id, time_period, value in parsed_data:
        if (region_id == None): continue
        # '5' => mean_price
        if measure_type != '5': continue
        
        print(f"Updating database... MEASURE TYPE: {measure_type} REGION: {region_id}, TIME_PERIOD: {time_period}, VALUE: {value}")

        cursor.execute('''UPDATE dwellings SET mean_price = ? WHERE time_period = ? AND region_id = ?''', 
                        (value, time_period, region_id) )

        sqlite_connection.commit()
except:
    print('ERROR processing: Number of residential dwellings and Mean price of residential dwellings (per state)')