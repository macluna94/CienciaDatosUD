import pandas as pd
import numpy as np

def toNum(valor):
    try:
        # Eliminar el símbolo de dólar y las comas
        if isinstance(valor, str):
            valor = valor.replace('$', '').replace(',', '')
        return round(float(valor), 2)
    except:
        return 0

try:
    # Leer el archivo CSV
    df = pd.read_csv("C:/Users/manuell/Videos/CienciaDatos_AN/peliculas.csv")
    
    # Convertir datos
    try:
        # String a Fecha
        df['Estreno'] = pd.to_datetime(df['Estreno'])
        print("Conversión de fechas exitosa")
    except Exception as e:
        print(f"Error al convertir fechas: {str(e)}")
    
    try:
        # String a entero
        df['Presupuesto'] = df['Presupuesto'].apply(toNum)
        df['TaquillaInternacional'] = df['TaquillaInternacional'].apply(toNum)
        df['TaquillaEEUU'] = df['TaquillaEEUU'].apply(toNum)
        print("Conversión de valores numéricos exitosa")
    except Exception as e:
        print(f"Error al convertir valores numéricos: {str(e)}")
    
    # Mostrar las primeras filas del DataFrame
    print("\nPrimeras filas del DataFrame:")
    print(df.head())

except FileNotFoundError:
    print("Error: No se encontró el archivo CSV")
except pd.errors.EmptyDataError:
    print("Error: El archivo CSV está vacío")
except Exception as e:
    print(f"Error inesperado: {str(e)}")

# Convertir los valores de NumPy a enteros usando item()
intercept = int(modelo.intercept_[0].item())
coef = int(modelo.coef_[0].item())

# Imprimir los resultados
print(f" Interceptor: {intercept} \n Coeficiente: {coef}") 