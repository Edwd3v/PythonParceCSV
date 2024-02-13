from datetime import datetime
import csv
import pandas as pd
import random
import os

class DataProcessor:
    def transform_excel_to_csv(self, selected_file_path):
        # Logica de transformacion de Excel a CSV
        df = pd.read_excel(selected_file_path)
        number_document = random.randint(1, 100)
        output_path = f'data{number_document}.csv'
        df.to_csv(output_path, index=False)
        return output_path

    def read_csv_module(self, path):
        # Logica de lectura de CSV
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = next(reader)
            data = []

            for row in reader:
                iterable = zip(header, row)
                country_dict = {key: value for key, value in iterable}
                data.append(country_dict)
            return data

    def write_csv(self, data, output_path):
        # Logica de escritura de CSV
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ["concepto", "referencia", "fecha", "precio", "Documento Fuente", "Beneficiario Nombre", "Cantidad"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in data:
                writer.writerow(row)
