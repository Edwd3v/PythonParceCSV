from datetime import datetime
import csv
import pandas as pd
import random
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import platform

class DataProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesador de Datos")

        self.selected_file_path = None  # Almacena la ruta del archivo seleccionado
    
        # Etiqueta e instrucciones
        self.label = tk.Label(root, text="Seleccione un archivo Excel:")
        self.label.pack(pady=10)

        # Botón para seleccionar el archivo
        self.button = tk.Button(root, text="Seleccionar Archivo", command=self.process_data)
        self.button.pack(pady=10)

        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=20)

        # Texto informativo
        self.info_text = tk.Text(root, height=10, width=50)
        self.info_text.pack(pady=10)

        # Botón de finalizar (inicialmente deshabilitado)
        self.finish_button = tk.Button(root, text="Finalizar", command=self.finish, state=tk.DISABLED)
        self.finish_button.pack(pady=10)

    def process_data(self):
        if not self.selected_file_path:
            # Abre el cuadro de diálogo para seleccionar un archivo
            file_types = [("Excel files", "*.xls"), ("Excel files", "*.xlsx")]
            self.selected_file_path = filedialog.askopenfilename(filetypes=file_types)

            if not self.selected_file_path:
                self.write_to_info_text("No se seleccionó ningún archivo.")
                return

            self.write_to_info_text(f'Se seleccionó el archivo: {os.path.basename(self.selected_file_path)}')

        # Puedes agregar más mensajes informativos a medida que avanzas en el procesamiento
        self.write_to_info_text("Iniciando procesamiento de datos...")

        try:
            csv_path = self.transform_excel_to_csv()

            if csv_path:
                data = self.read_csv_module(csv_path)

                # Estructurar datos
                id_proveedor = []

                for i, dato in enumerate(data):
                    fecha_str = dato.get('Fecha')

                    if fecha_str is not None and fecha_str != '':
                        try:
                            fecha = datetime.strptime(fecha_str, '%Y/%m/%d').strftime('%Y-%m-%d')
                        except ValueError:
                            fecha = None
                    else:
                        fecha = None

                    precio_str = dato.get('Vr. Unitario', '')
                    cantidad_str = dato.get('Cantidad', '')

                    # Asegurar que las cadenas vacías sean manejadas correctamente
                    precio = float(precio_str) if precio_str != '' else 0
                    cantidad = float(cantidad_str) if cantidad_str != '' else 0

                    id_proveedor.append({
                        "concepto": dato.get('Texto Captura Concepto'),
                        "referencia": dato.get('Referencia'),
                        "fecha": fecha,
                        "precio": precio,
                        "Documento Fuente": dato.get('Documento Fuente'),
                        "Beneficiario Nombre": dato.get('Beneficiario Nombre'),
                        "Cantidad": cantidad
                    })

                    # Actualizar la barra de progreso
                    progress_value = int((i + 1) / len(data) * 100)
                    self.update_progress(progress_value)

                # Crear un diccionario para realizar un seguimiento de la referencia más reciente
                referencias_mas_recientes = {}

                for proveedor in id_proveedor:
                    referencia = proveedor.get('referencia')
                    fecha_proveedor = datetime.strptime(proveedor.get('fecha', ''), '%Y-%m-%d') if proveedor.get('fecha') else None

                    if referencia is not None:
                        if referencia in referencias_mas_recientes:
                            fecha_existente = datetime.strptime(referencias_mas_recientes[referencia].get('fecha', ''), '%Y-%m-%d') if referencias_mas_recientes[referencia].get('fecha') else None
                            if fecha_proveedor and (not fecha_existente or fecha_proveedor > fecha_existente):
                                referencias_mas_recientes[referencia] = proveedor
                        else:
                            referencias_mas_recientes[referencia] = proveedor

                self.write_to_info_text("Datos estructurados. Procesando referencias...")
                # Imprimir el progreso para depuración
                self.write_to_info_text("Referencias procesadas. Escribiendo resultados...")

                # Obtener el nombre del archivo original sin extensión
                file_name = os.path.splitext(os.path.basename(csv_path))[0]

                # Construir el nombre del archivo de resultados
                output_path = os.path.join('.', f'resultados_{file_name}.csv')
                self.write_csv(list(referencias_mas_recientes.values()), output_path)

                self.write_to_info_text(f'Data written to {output_path}')
                # Habilitar el botón de finalizar
                self.finish_button.config(state=tk.NORMAL)

        except Exception as e:
            self.write_to_info_text(f"Error inesperado: {e}")

    def transform_excel_to_csv(self):
        # Carga el archivo de Excel
        df = pd.read_excel(self.selected_file_path)

        # Guarda el DataFrame en un archivo CSV
        number_document = random.randint(1, 100)
        output_path = f'data{number_document}.csv'
        df.to_csv(output_path, index=False)

        self.write_to_info_text(f'Documento transformado y guardado como {output_path}')
        return output_path

    def read_csv_module(self, path):
        with open(path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = next(reader)
            data = []

            for row in reader:
                iterable = zip(header, row)
                country_dict = {key: value for key, value in iterable}
                data.append(country_dict)
            return data

    def write_csv(self, data, output_path):
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ["concepto", "referencia", "fecha", "precio", "Documento Fuente", "Beneficiario Nombre", "Cantidad"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in data:
                writer.writerow(row)

    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()

    def write_to_info_text(self, message):
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)

    def finish(self):
        # Agrega cualquier limpieza o cierre necesario aquí
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = DataProcessorApp(root)
    app.root.mainloop()

    
import tkinter as tk
from ToolsByteScultor.ui_module import DataProcessorUI
from ToolsByteScultor.data_processor_module import DataProcessor

if __name__ == '__main__':
    root = tk.Tk()

    data_processor = DataProcessor()
    ui = DataProcessorUI(root, data_processor)

    root.mainloop()
