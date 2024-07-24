import os

import pandas as pd
import pyreadr


class DataPreprocessor:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.data = pd.DataFrame()

    def load_rds_files(self):
        all_data = pd.DataFrame
        for filename in os.listdir(self.data_folder):
            print(filename)
            if filename.endswith('.RDS'):
                file_path = os.path.join(self.data_folder, filename)
                print(file_path)
                result = pyreadr.read_r(file_path)
                data = result[None]
                data['source'] = filename
                all_data = pd.concat([all_data, data], ignore_index=True)

        self.data = all_data

    def get_data(self):
        return self.data.to_dict(orient='records')
