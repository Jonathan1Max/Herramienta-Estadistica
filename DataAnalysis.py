import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalysis:
    def __init__(self, file_path):
        """Inicializa la clase con los datos del archivo CSV"""
        self.data = pd.read_csv(file_path, delimiter=';')  # Se específico el delimitador como punto y coma
        self.clean_data()

    def clean_data(self):
        """Limpia los datos convirtiendo las columnas relevantes a tipo numérico"""
        columns_to_convert = ['Poblacion_1994', 'Poblacion_2002', 'Poblacion_2018', 
                              'Distribucion_1994', 'Distribucion_2002', 
                              'Distribucion_2018', 'Tasa_de_Crecimiento']
        for column in columns_to_convert:
            self.data[column] = pd.to_numeric(self.data[column], errors='coerce')

    def group_data(self, column):
        """Agrupa datos según una columna específica"""
        return self.data[column].value_counts()

    def calculate_statistics(self, column):
        """Calcula media, mediana, moda y desviación estándar para una columna"""
        data_col = self.data[column]
        mean = np.mean(data_col)
        median = np.median(data_col)
        mode = data_col.mode().iloc[0] if not data_col.mode().empty else None
        std_dev = np.std(data_col, ddof=0)  # Se define ddof=0 para la desviación estándar de la población
        return {
            'Media': mean, 
            'Mediana': median, 
            'Moda': mode, 
            'Desviación Estándar': std_dev
        }

    def plot_histogram(self, column):
        """Genera un histograma para una columna específica"""
        plt.figure(figsize=(10, 6))
        sns.histplot(self.data[column], kde=True, bins=10)
        plt.title(f'Histograma de {column}')
        plt.xlabel(column)
        plt.ylabel('Frecuencia')
        plt.grid()
        plt.show()

    def plot_statistics_bars(self, years):
        """Genera un gráfico de barras para la media y mediana de los años especificados"""
        means = [self.calculate_statistics(year)['Media'] for year in years]
        medians = [self.calculate_statistics(year)['Mediana'] for year in years]
        
        x_labels = years
        width = 0.35  # ancho de las barras

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(x_labels, means, width, label='Media', alpha=0.7)
        ax.bar([x + width for x in range(len(medians))], medians, width, label='Mediana', alpha=0.7)

        ax.set_xlabel('Año')
        ax.set_ylabel('Población')
        ax.set_title('Media y Mediana de la Población por Año')
        ax.set_xticks([x + width / 2 for x in range(len(x_labels))])
        ax.set_xticklabels(x_labels)
        ax.legend()
        plt.show()

if __name__ == "__main__":
    # Datos del archivo CSV
    analysis = DataAnalysis('censo_datos.csv')
    
    # Agrupación de datos (ejemplo usando la columna 'Departamento')
    print("Agrupación por Departamento:")
    print(analysis.group_data('Departamento'))
    
    # Cálculos estadísticos para los años de población
    years = ['Poblacion_1994', 'Poblacion_2002', 'Poblacion_2018']
    for year in years:
        print(f"\nEstadísticas para {year}:")
        estadisticas = analysis.calculate_statistics(year)
        for key, value in estadisticas.items():
            print(f"{key}: {value}")
        
        # Graficos del histograma
        analysis.plot_histogram(year)

    # Graficos de media y mediana
    analysis.plot_statistics_bars(years)
