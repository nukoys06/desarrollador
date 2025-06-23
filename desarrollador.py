import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
import time

# Configuración de la página
st.set_page_config(
    page_title="Bootstrap Analytics",
    page_icon="📊",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #3B82F6, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .exercise-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #e5e7eb;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .exercise-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .selected-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: 2px solid #667eea;
    }
    .metric-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(90deg, #3B82F6, #8B5CF6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        width: 100%;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Clase para análisis bootstrap
class BootstrapAnalyzer:
    def __init__(self):
        self.n_bootstrap = 1000
    
    @staticmethod
    def parse_data(data_string):
        try:
            return [float(x.strip()) for x in data_string.split(',') if x.strip()]
        except:
            return []
    
    def random_sample(self, arr, size=None):
        if size is None:
            size = len(arr)
        return [random.choice(arr) for _ in range(size)]
    
    def block_bootstrap(self, data, block_size=3):
        blocks = []
        for i in range(len(data) - block_size + 1):
            blocks.append(data[i:i + block_size])
        
        num_blocks = int(np.ceil(len(data) / block_size))
        sample = []
        for _ in range(num_blocks):
            sample.extend(random.choice(blocks))
        
        return sample[:len(data)]
    
    def calculate_correlation(self, x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
        
        return numerator / denominator if denominator != 0 else 0
    
    def run_analysis(self, exercise_id, data1, data2=None):
        results = {}
        bootstrap_stats = []
        
        if exercise_id == '1':  # Estimación de la Media
            original_mean = np.mean(data1)
            for _ in range(self.n_bootstrap):
                sample = self.random_sample(data1)
                bootstrap_stats.append(np.mean(sample))
            
            bootstrap_stats.sort()
            results = {
                'original_mean': round(original_mean, 4),
                'bootstrap_mean': round(np.mean(bootstrap_stats), 4),
                'ci_95': [round(np.percentile(bootstrap_stats, 2.5), 4), 
                         round(np.percentile(bootstrap_stats, 97.5), 4)],
                'std_error': round(np.std(bootstrap_stats), 4)
            }
        
        elif exercise_id == '2':  # Comparación de Dos Medias
            if not data2:
                st.error("Necesitas datos para ambos sistemas")
                return None
            
            original_diff = np.mean(data1) - np.mean(data2)
            for _ in range(self.n_bootstrap):
                sample1 = self.random_sample(data1)
                sample2 = self.random_sample(data2)
                bootstrap_stats.append(np.mean(sample1) - np.mean(sample2))
            
            bootstrap_stats.sort()
            ci_95 = [np.percentile(bootstrap_stats, 2.5), np.percentile(bootstrap_stats, 97.5)]
            
            results = {
                'original_diff': round(original_diff, 4),
                'bootstrap_diff': round(np.mean(bootstrap_stats), 4),
                'ci_95': [round(ci_95[0], 4), round(ci_95[1], 4)],
                'significant': ci_95[0] > 0 or ci_95[1] < 0
            }
        
        elif exercise_id == '3':  # Estimación de Proporciones
            original_prop = sum(1 for x in data1 if x == 1) / len(data1)
            for _ in range(self.n_bootstrap):
                sample = self.random_sample(data1)
                bootstrap_stats.append(sum(1 for x in sample if x == 1) / len(sample))
            
            bootstrap_stats.sort()
            results = {
                'original_prop': round(original_prop, 4),
                'bootstrap_prop': round(np.mean(bootstrap_stats), 4),
                'ci_90': [round(np.percentile(bootstrap_stats, 5), 4),
                         round(np.percentile(bootstrap_stats, 95), 4)]
            }
        
        elif exercise_id == '4':  # Correlación Bootstrap
            if not data2 or len(data1) != len(data2):
                st.error("Necesitas dos variables con el mismo número de observaciones")
                return None
            
            original_corr = self.calculate_correlation(data1, data2)
            for _ in range(self.n_bootstrap):
                indices = [random.randint(0, len(data1)-1) for _ in range(len(data1))]
                sample1 = [data1[i] for i in indices]
                sample2 = [data2[i] for i in indices]
                bootstrap_stats.append(self.calculate_correlation(sample1, sample2))
            
            bootstrap_stats.sort()
            results = {
                'original_corr': round(original_corr, 4),
                'bootstrap_corr': round(np.mean(bootstrap_stats), 4),
                'ci_95': [round(np.percentile(bootstrap_stats, 2.5), 4),
                         round(np.percentile(bootstrap_stats, 97.5), 4)]
            }
        
        elif exercise_id == '5':  # Mediana y Percentiles
            original_median = np.median(data1)
            for _ in range(self.n_bootstrap):
                sample = self.random_sample(data1)
                bootstrap_stats.append(np.median(sample))
            
            bootstrap_stats.sort()
            results = {
                'original_median': round(original_median, 4),
                'bootstrap_median': round(np.mean(bootstrap_stats), 4),
                'ci_95': [round(np.percentile(bootstrap_stats, 2.5), 4),
                         round(np.percentile(bootstrap_stats, 97.5), 4)]
            }
        
        elif exercise_id == '6':  # Razón de Varianzas
            if not data2:
                st.error("Necesitas datos para ambos procesos")
                return None
            
            original_ratio = np.var(data1, ddof=1) / np.var(data2, ddof=1)
            for _ in range(self.n_bootstrap):
                sample1 = self.random_sample(data1)
                sample2 = self.random_sample(data2)
                var1 = np.var(sample1, ddof=1)
                var2 = np.var(sample2, ddof=1)
                if var2 != 0:
                    bootstrap_stats.append(var1 / var2)
            
            bootstrap_stats.sort()
            results = {
                'original_ratio': round(original_ratio, 4),
                'bootstrap_ratio': round(np.mean(bootstrap_stats), 4),
                'ci_95': [round(np.percentile(bootstrap_stats, 2.5), 4),
                         round(np.percentile(bootstrap_stats, 97.5), 4)]
            }
        
        elif exercise_id == '10':  # Bootstrap con Datos Dependientes
            original_volatility = np.std(data1, ddof=1)
            for _ in range(self.n_bootstrap):
                sample = self.block_bootstrap(data1, 3)
                bootstrap_stats.append(np.std(sample, ddof=1))
            
            bootstrap_stats.sort()
            results = {
                'original_volatility': round(original_volatility, 4),
                'bootstrap_volatility': round(np.mean(bootstrap_stats), 4),
                'ci_95': [round(np.percentile(bootstrap_stats, 2.5), 4),
                         round(np.percentile(bootstrap_stats, 97.5), 4)]
            }
        
        # Añadir distribución para gráfico
        results['bootstrap_distribution'] = bootstrap_stats[:100]  # Solo los primeros 100 para el gráfico
        
        return results

# Función principal
def main():
    # Header
    st.markdown('<h1 class="main-header">Bootstrap Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Análisis estadístico avanzado con técnicas de remuestreo</p>', unsafe_allow_html=True)
    
    # Definir ejercicios
    exercises = [
        {'id': '1', 'name': 'Estimación de la Media', 'desc': 'Intervalo de confianza para la media poblacional', 'icon': '📊'},
        {'id': '2', 'name': 'Comparación de Dos Medias', 'desc': 'Diferencia significativa entre dos sistemas', 'icon': '⚖️'},
        {'id': '3', 'name': 'Estimación de Proporciones', 'desc': 'Proporción de éxito en tratamiento médico', 'icon': '📈'},
        {'id': '4', 'name': 'Correlación Bootstrap', 'desc': 'Coeficiente de correlación entre variables', 'icon': '🔗'},
        {'id': '5', 'name': 'Mediana y Percentiles', 'desc': 'Estadísticas robustas con bootstrap', 'icon': '📏'},
        {'id': '6', 'name': 'Razón de Varianzas', 'desc': 'Comparación de variabilidad entre procesos', 'icon': '📐'},
        {'id': '7', 'name': 'Bootstrap en Regresión', 'desc': 'Coeficientes de regresión lineal', 'icon': '📉'},
        {'id': '8', 'name': 'Diferencia de Proporciones', 'desc': 'Comparación de efectividad de tratamientos', 'icon': '🧪'},
        {'id': '9', 'name': 'Bootstrap Paramétrico', 'desc': 'Estimación con distribución exponencial', 'icon': '⚡'},
        {'id': '10', 'name': 'Bootstrap con Datos Dependientes', 'desc': 'Bootstrap por bloques para series temporales', 'icon': '🔄'}
    ]
    
    # Selección de ejercicio
    st.subheader("🎯 Selecciona tu Análisis")
    
    # Crear grid de ejercicios
    cols = st.columns(3)
    selected_exercise = None
    
    for i, ex in enumerate(exercises):
        with cols[i % 3]:
            if st.button(f"{ex['icon']} {ex['name']}", key=f"ex_{ex['id']}", help=ex['desc']):
                st.session_state.selected_exercise = ex['id']
    
    # Mostrar ejercicio seleccionado
    if 'selected_exercise' in st.session_state:
        selected_ex = next(ex for ex in exercises if ex['id'] == st.session_state.selected_exercise)
        
        st.markdown("---")
        st.subheader(f"{selected_ex['icon']} {selected_ex['name']}")
        st.write(selected_ex['desc'])
        
        # Determinar etiquetas de datos
        data_labels = {
            '2': {'label1': 'Sistema A:', 'label2': 'Sistema B:'},
            '4': {'label1': 'Horas de estudio:', 'label2': 'Calificaciones:'},
            '6': {'label1': 'Proceso 1:', 'label2': 'Proceso 2:'},
            '7': {'label1': 'Publicidad (x):', 'label2': 'Ventas (y):'},
            '8': {'label1': 'Tratamiento A:', 'label2': 'Tratamiento B:'}
        }
        
        labels = data_labels.get(st.session_state.selected_exercise, {'label1': 'Datos:', 'label2': None})
        
        # Entrada de datos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Entrada de Datos")
            data1_input = st.text_area(
                labels['label1'],
                placeholder="1.2, 3.4, 5.6, 7.8, 9.0...",
                height=100
            )
            
            if labels['label2']:
                data2_input = st.text_area(
                    labels['label2'],
                    placeholder="2.1, 4.3, 6.5, 8.7, 10.9...",
                    height=100
                )
            else:
                data2_input = ""
        
        with col2:
            st.subheader("🚀 Ejecutar Análisis")
            
            if st.button("Ejecutar Análisis Bootstrap", type="primary"):
                if data1_input:
                    analyzer = BootstrapAnalyzer()
                    data1 = analyzer.parse_data(data1_input)
                    data2 = analyzer.parse_data(data2_input) if data2_input else None
                    
                    if data1:
                        with st.spinner("Ejecutando análisis bootstrap..."):
                            results = analyzer.run_analysis(st.session_state.selected_exercise, data1, data2)
                        
                        if results:
                            st.session_state.results = results
                            st.success("¡Análisis completado exitosamente!")
                    else:
                        st.error("Por favor ingresa datos válidos")
                else:
                    st.error("Por favor ingresa algunos datos")
        
        # Mostrar resultados
        if 'results' in st.session_state and st.session_state.results:
            st.markdown("---")
            st.subheader("📈 Resultados del Análisis")
            
            results = st.session_state.results
            
            # Métricas principales
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Estadísticas Principales")
                
                for key, value in results.items():
                    if key != 'bootstrap_distribution':
                        if isinstance(value, list):
                            st.metric(
                                label=key.replace('_', ' ').title(),
                                value=f"[{', '.join(map(str, value))}]"
                            )
                        elif isinstance(value, bool):
                            st.metric(
                                label=key.replace('_', ' ').title(),
                                value="Sí" if value else "No"
                            )
                        else:
                            st.metric(
                                label=key.replace('_', ' ').title(),
                                value=str(value)
                            )
            
            with col2:
                st.subheader("📊 Distribución Bootstrap")
                
                if 'bootstrap_distribution' in results:
                    # Crear histograma
                    fig = go.Figure(data=[
                        go.Histogram(
                            x=results['bootstrap_distribution'],
                            nbinsx=20,
                            marker_color='rgba(59, 130, 246, 0.7)',
                            marker_line_color='rgba(59, 130, 246, 1)',
                            marker_line_width=1.5
                        )
                    ])
                    
                    fig.update_layout(
                        title="Distribución de Estadísticas Bootstrap",
                        xaxis_title="Valor",
                        yaxis_title="Frecuencia",
                        template="plotly_white",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    
    # Instrucciones
    st.markdown("---")
    st.subheader("💡 Instrucciones Rápidas")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("• Selecciona el tipo de análisis que necesitas")
        st.write("• Ingresa tus datos separados por comas")
    with col2:
        st.write("• Para comparaciones, llena ambos campos")
        st.write("• Se generan 1000 muestras bootstrap automáticamente")

if __name__ == "__main__":
    main()
