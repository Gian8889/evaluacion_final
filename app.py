import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- DEFINICIÓN DE LA CLASE POO ---
class DataAnalyzer:
    def __init__(self, df):
        self.df = df
    
    def estadisticas(self):
        return self.df.describe()
    
    def obtener_columnas(self):
        nums = self.df.select_dtypes(include=['number']).columns.tolist()
        cats = self.df.select_dtypes(include=['object']).columns.tolist()
        return nums, cats

# --- INTERFAZ PRINCIPAL ---
st.set_page_config(page_title="App Bancaria", layout="wide")

# Sidebar con widgets
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox("Selecciona un módulo:", ["Home", "Carga de Datos", "Análisis EDA"])

# --- MÓDULO 1: HOME ---
if opcion == "Home":
    st.title("Proyecto: BankMarketing")
    st.write("Bienvenido. Este es el proyecto de Especialización.")
    
    # Widget adicional en Home como pediste
    seleccion_rapida = st.selectbox("Ir a:", ["Home", "Carga de Datos", "Análisis EDA"])
    if seleccion_rapida != "Home":
        st.info(f"Selecciona '{seleccion_rapida}' en la barra lateral izquierda.")

# --- MÓDULO 2: CARGA ---
elif opcion == "Carga de Datos":
    st.header("Carga tu archivo")
    archivo = st.file_uploader("Sube BankMarketing.csv", type=['csv'])
    
    if archivo:
        df = pd.read_csv(archivo, sep=';')
        st.session_state['df'] = df # Guardamos el df para toda la sesión
        st.success("Dataset cargado")

# --- MÓDULO 3: EDA ---
elif opcion == "Análisis EDA":
    if 'df' in st.session_state:
        df = st.session_state['df']
        analyzer = DataAnalyzer(df) # Instanciamos la clase POO
        
        # Uso de TABS y COLUMNS
        tab1, tab2 = st.tabs(["Estadísticas", "Visualización"])
        
        with tab1:
            st.write(analyzer.estadisticas())
            
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                # Widgets: selectbox y slider
                var = st.selectbox("Elige variable:", df.columns)
                rango = st.slider("Ajuste", 0, 100)
            with col2:
                # Widget: checkbox
                if st.checkbox("Mostrar gráfico"):
                    st.line_chart(df[var] if var in df.select_dtypes('number') else None)
    else:
        st.warning("Primero carga el archivo.")
