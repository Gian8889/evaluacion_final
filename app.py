import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def info_general(self):
        return pd.DataFrame({
            'Tipo de dato': self.df.dtypes,
            'No nulos': self.df.count(),
            'Nulos': self.df.isnull().sum()
        })

    def clasificar_variables(self):
        num = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        return num, cat

    def estadisticas(self):
        return self.df.describe()

    def plot_histograma(self, col):
        fig, ax = plt.subplots()
        sns.histplot(self.df[col].dropna(), kde=True, ax=ax)
        return fig
        
    def filtrar_por_rango(self, col, min_val, max_val):
        # Filtra el df basado en un rango (para cumplir con el widget slider)
        return self.df[(self.df[col] >= min_val) & (self.df[col] <= max_val)]

    def plot_crosstab(self, col1, col2):
        # Creamos una tabla cruzada
        ct = pd.crosstab(self.df[col1], self.df[col2])
        # Graficamos
        fig, ax = plt.subplots(figsize=(10, 6))
        ct.plot(kind='bar', stacked=True, ax=ax)
        plt.xticks(rotation=45, ha='right')
        plt.title(f'Relación entre {col1} y {col2}')
        return fig

# --- INTERFAZ PRINCIPAL ---
st.set_page_config(page_title="App Bancaria", layout="wide")

# Sidebar con widgets
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox("Selecciona un módulo:", ["Modulo 1: Home", "Modulo 2: Carga de Datos", "Modulo 3: Análisis EDA"])

# --- MÓDULO 1: HOME ---
if opcion == "Modulo 1: Home":
    st.title("📊 Proyecto: Análisis de Campaña BankMarketing")
    
    st.write("### 🎯 Objetivo del Análisis")
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
        st.write("**Nombre completo:** Jorge Huaman Calderon")
        st.write("**Curso / Especialización:** Especialización en Python for Analytics")
    with col_b:
        st.write("**Año:** 2026")
        st.write("**Edicion:** 58")
    
    st.divider()
    
    st.write("### ℹ️ Breve explicación del dataset")
    st.write("""
    El dataset contiene información sobre clientes de una institución financiera. 
    Incluye variables demográficas (edad, educación, estado civil) y datos 
    relacionados con gestiones de marketing previas y actuales (duración del contacto, 
    número de llamadas, resultados de campañas anteriores).
    """)

    st.divider() # Línea divisoria estética
    
    st.write("### 🛠️ Tecnologías utilizadas")
    st.markdown("""
    * **Lenguaje:** Python
    * **Manipulación de datos:** Pandas, NumPy
    * **Visualización:** Matplotlib, Seaborn
    * **Interfaz interactiva:** Streamlit
    """)

# --- MÓDULO 2: CARGA ---
elif opcion == "Modulo 2: Carga de Datos":
    st.header("📤 Carga tu archivo")
    archivo = st.file_uploader("Sube BankMarketing.csv", type=['csv'])
    
    if archivo:
        df = pd.read_csv(archivo, sep=';')
        st.session_state['df'] = df # Guardamos el df para toda la sesión
        st.success("Dataset cargado correctamente")
        st.write(f"### Dimensiones del dataset")
        st.write(f"El dataset tiene **{df.shape[0]} filas** y **{df.shape[1]} columnas**.")

        st.write("### Vista previa (primeras 5 filas)")
        st.dataframe(df.head())

# --- MÓDULO 3: EDA ---
# --- MÓDULO 3: EDA ---
elif opcion == "Modulo 3: Análisis EDA":
    if 'df' in st.session_state:
        df = st.session_state['df']
        analyzer = DataAnalyzer(df) 
        
        # Corrección: Asegúrate de que esta línea tenga exactamente 8 espacios
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Info/Variables", "Estadística/Nulos", "Distribución", "Bivariado", "Insights"])
        
        with tab1:
            st.header("Ítem 1: Información General")
            st.dataframe(analyzer.info_general())
            st.header("Ítem 2: Clasificación")
            num, cat = analyzer.clasificar_variables()
            c1, c2 = st.columns(2)
            c1.write(f"**Numéricas ({len(num)}):**")
            c1.write(num)
            c2.write(f"**Categóricas ({len(cat)}):**")
            c2.write(cat)

        with tab2:
            st.header("Ítem 3: Estadísticas Descriptivas")
            st.write(analyzer.estadisticas())
            st.header("Ítem 4: Valores Faltantes")
            st.bar_chart(df.isnull().sum())
            st.write("Discusión: Los valores faltantes se analizan para determinar si es necesario imputar datos o eliminar registros.")

        with tab3:
    # --- Ítem 5: Distribución Numérica ---
            st.header("Ítem 5: Distribución Numérica")
            var_num = st.selectbox("Selecciona variable:", df.select_dtypes('number').columns)
            if st.checkbox("Ver Histograma"):
                st.pyplot(analyzer.plot_histograma(var_num))
    
    # --- Ítem 6: Análisis Categórico ---
            st.header("Ítem 6: Análisis de variables categóricas")
            var_cat = st.selectbox("Selecciona categórica:", df.select_dtypes('object').columns)
    
    # Mostrar conteos y proporciones
            c1, c2 = st.columns(2)
    
    # Cálculo de proporciones
            conteo = df[var_cat].value_counts()
            proporcion = df[var_cat].value_counts(normalize=True)
            resumen = pd.DataFrame({'Conteo': conteo, 'Proporción': proporcion})
    
            with c1:
                st.write("**Resumen estadístico:**")
                st.dataframe(resumen.style.format({'Proporción': '{:.2%}'}))
        
            with c2:
                st.write("**Gráfico de barras:**")
                st.bar_chart(conteo)

        with tab4:
            st.header("Ítems 7 y 8: Análisis Bivariado")
            tipo_analisis = st.radio("¿Qué tipo de análisis deseas hacer?", ["Numérico (Boxplot)", "Categórico (Barras Apiladas)"])
            
            if tipo_analisis == "Numérico (Boxplot)":
                col_x = st.selectbox("Eje X (Categoría):", df.select_dtypes('object').columns)
                col_y = st.selectbox("Eje Y (Numérica):", df.select_dtypes('number').columns)
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.boxplot(data=df, x=col_x, y=col_y, ax=ax)
                plt.xticks(rotation=45, ha='right')
                st.pyplot(fig)
            else:
                col1 = st.selectbox("Variable 1:", df.select_dtypes('object').columns)
                col2 = st.selectbox("Variable 2:", df.select_dtypes('object').columns)
                # Usamos el nuevo método
                st.pyplot(analyzer.plot_crosstab(col1, col2))

        with tab5:
            st.header("Ítem 9: Análisis Dinámico")
            
            # Usamos el slider para filtrar datos por una variable numérica
            var_slider = st.selectbox("Variable para filtrar con slider:", df.select_dtypes('number').columns)
            min_v = int(df[var_slider].min())
            max_v = int(df[var_slider].max())
            rango = st.slider("Selecciona rango:", min_v, max_v, (min_v, max_v))
            
            # Aplicamos el filtro usando la POO
            df_filtrado = analyzer.filtrar_por_rango(var_slider, rango[0], rango[1])
            st.write(f"Filas encontradas: {len(df_filtrado)}")
            st.dataframe(df_filtrado.head())
            
            # Correlación
            cols_sel = st.multiselect("Columnas para correlación:", df.select_dtypes('number').columns)
            if cols_sel:
                st.write(df_filtrado[cols_sel].corr())
            
            st.header("Ítem 10: Hallazgos clave")
            st.markdown("""
            * **Insight 1:** La edad de los clientes influye en...
            * **Insight 2:** La duración de la llamada tiene una correlación de...
            * **Insight 3:** Los clientes con educación universitaria tienden a...
            * **Insight 4:** La variable 'contact' muestra una preferencia por...
            * **Insight 5:** Recomendación estratégica para el negocio.
            """)
    else:
        st.warning("Primero carga el archivo en el Módulo 2.")
