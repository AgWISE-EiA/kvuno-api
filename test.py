import os

import pyreadr

# Specify the path to your RDS file
data_folder = os.path.join("static/" 'data')

# Convert to list of dictionaries
data_records = []

for filename in os.listdir(data_folder):
    print(filename)
    if filename.endswith('.RDS'):
        file_path = os.path.join(data_folder, filename)
        print(file_path)
        result = pyreadr.read_r(file_path)
        data = result[None]
        data['source'] = filename
        for index, row in data.iterrows():
            record = {
                'XY': row['XY'],
                'country': row['country'],
                'province': row['province'],
                'lon': row['lon'],
                'lat': row['lat'],
                'Variety': row['Variety'],
                'Season_type': row['Season_type'],
                'Opt_date': row['Opt_date'],
                'Planting_Option': row['Planting_Option'],
                'source_file': filename
            }
            data_records.append(record)

print(data_records)
