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
    st.title("📊 Proyecto: Análisis de Campaña BankMarketing")
    
    st.write("### Objetivo del Análisis")
    st.write("""
    Este proyecto tiene como finalidad realizar un Análisis Exploratorio de Datos (EDA) 
    sobre el dataset BankMarketing, con el objetivo de identificar los factores 
    clave que influyen en la aceptación de las campañas de marketing financiero.
    """)
    
    st.divider() # Línea divisoria estética
    
    st.write("### 👤 Datos del Autor")
    # Usamos columnas para presentar los datos de forma ordenada
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Nombre completo:** [Tu Nombre Aquí]")
        st.write("**Curso / Especialización:** Especialización en Python for Analytics")
    with col_b:
        st.write("**Año:** 2026")
    
    st.divider()
    
    st.write("### ℹ️ Breve explicación del dataset")
    st.write("""
    El dataset contiene información sobre clientes de una institución financiera. 
    Incluye variables demográficas (edad, educación, estado civil) y datos 
    relacionados con gestiones de marketing previas y actuales (duración del contacto, 
    número de llamadas, resultados de campañas anteriores).
    """)
    
    st.write("### 🛠️ Tecnologías utilizadas")
    st.markdown("""
    * **Lenguaje:** Python
    * **Manipulación de datos:** Pandas, NumPy
    * **Visualización:** Matplotlib, Seaborn
    * **Interfaz interactiva:** Streamlit
    """)

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
