import streamlit as st
import requests
from datetime import datetime
from lxml import html

# Función para obtener los precios del dólar y las fechas de actualización desde la API
def obtener_precios():
    url_emp = "https://pydolarve.org/api/v1/dollar?page=enparalelovzla"
    url = "https://www.bcv.org.ve/"

    try:
        response_emp = requests.get(url_emp)
        response_emp.raise_for_status()
        datos_emp = response_emp.json()
        precio_promedio = datos_emp["monitors"]["enparalelovzla"]["price"]
        actualizacion_promedio = datos_emp["monitors"]["enparalelovzla"]["last_update"]

        page = requests.get(url)
        tree = html.fromstring(page.content)
        dato = tree.xpath('//*[@id="dolar"]/div/div/div[2]/strong/text()')
        precio_bcv = float(("".join(dato[0].split())).replace(",", "."))
        actualizacion_bcv = datetime.now().strftime("%d/%m/%Y %H:%M")

        return precio_promedio, actualizacion_promedio, precio_bcv, actualizacion_bcv

    except requests.RequestException as e:
        st.error("Error al obtener los precios.")
        return None, None, None, None

# Estilo para ocultar el encabezado de Streamlit
st.markdown(
    """
    <style>
    .css-1d391kg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Título de la aplicación 
st.title("Calculadora de Dólares")

# Inicializar variables de sesión
if 'precio_promedio' not in st.session_state:
    st.session_state.precio_promedio = 0
    st.session_state.precio_bcv = 0
    st.session_state.actualizacion_promedio = ""
    st.session_state.actualizacion_bcv = ""

    # Obtener precios al iniciar la aplicación
    st.session_state.precio_promedio, st.session_state.actualizacion_promedio, st.session_state.precio_bcv, st.session_state.actualizacion_bcv = obtener_precios()

# Botón para actualizar precios
if st.button("Actualizar Precios"):
    st.session_state.precio_promedio, st.session_state.actualizacion_promedio, st.session_state.precio_bcv, st.session_state.actualizacion_bcv = obtener_precios()
    st.success("Precios actualizados.")

# Mostrar precios actuales
st.subheader("Precios actuales")
st.write(f"Precio promedio: {st.session_state.precio_promedio}")
st.write(f"Última actualización promedio: {st.session_state.actualizacion_promedio}")
st.write(f"Precio BCV: {st.session_state.precio_bcv}")
st.write(f"Última actualización BCV: {st.session_state.actualizacion_bcv}")

# Entrada de monto
monto = st.number_input("Ingrese el monto en dólares:", min_value=0.0, step=0.1)

# Calcular valores
if st.button("Calcular"):
    if st.session_state.precio_promedio > 0 and st.session_state.precio_bcv > 0:  # Verificar que los precios sean válidos
        valor_promedio = monto * st.session_state.precio_promedio
        valor_bcv = monto * st.session_state.precio_bcv
        
        # Mostrar resultados con estilo
        st.markdown(f"<h2 style='color: #4CAF50;'>Valor en precio promedio: {valor_promedio:.2f}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color: #2196F3;'>Valor en precio BCV: {valor_bcv:.2f}</h2>", unsafe_allow_html=True)
    else:
        st.error("Los precios no están disponibles. Asegúrese de actualizar primero.")
