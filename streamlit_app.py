
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Columna de concreto 3D",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Modelado 3D de una columna de concreto")
st.write(
    "Aplicación académica para estudiar el volumen de una columna "
    "circular con radio variable mediante cálculo integral."
)

st.sidebar.header("Dimensiones de la columna")

H = st.sidebar.number_input(
    "Altura H (m)", min_value=0.5, max_value=10.0,
    value=4.0, step=0.1
)

rb = st.sidebar.number_input(
    "Radio inferior (m)", min_value=0.05, max_value=1.0,
    value=0.30, step=0.01, format="%.2f"
)

rt = st.sidebar.number_input(
    "Radio superior (m)", min_value=0.05, max_value=1.0,
    value=0.20, step=0.01, format="%.2f"
)

st.sidebar.header("Estimación de costos")

precio = st.sidebar.number_input(
    "Precio del concreto (COP/m³)",
    min_value=0, value=450000, step=10000
)

# Radio variable linealmente con la altura
def radio(y):
    return rb + (rt - rb) * y / H

# Volumen mediante integración por discos
V = np.pi * H / 3 * (rb**2 + rb * rt + rt**2)

# Áreas de las secciones extremas
A_inferior = np.pi * rb**2
A_superior = np.pi * rt**2

# Costo estimado del concreto
costo = V * precio

# Construcción de la superficie 3D
z = np.linspace(0, H, 70)
theta = np.linspace(0, 2 * np.pi, 80)
Z, T = np.meshgrid(z, theta)

R = rb + (rt - rb) * Z / H
X = R * np.cos(T)
Y = R * np.sin(T)

fig = go.Figure()

fig.add_trace(go.Surface(
    x=X,
    y=Y,
    z=Z,
    colorscale="Blues",
    showscale=False,
    name="Columna"
))

fig.update_layout(
    title="Modelo tridimensional de la columna",
    scene=dict(
        xaxis_title="X (m)",
        yaxis_title="Y (m)",
        zaxis_title="Altura (m)",
        aspectmode="data"
    ),
    margin=dict(l=0, r=0, t=45, b=0)
)

columna, resultados = st.columns([1.6, 1])

with columna:
    st.plotly_chart(fig, use_container_width=True)

with resultados:
    st.subheader("Resultados geométricos")

    st.metric("Volumen", f"{V:.4f} m³")
    st.metric("Área inferior", f"{A_inferior:.4f} m²")
    st.metric("Área superior", f"{A_superior:.4f} m²")
    st.metric("Costo estimado", f"${costo:,.0f} COP")

    st.write("### Función del radio")
    st.latex(
        rf"r(y)={rb:.3f}"
        rf"+\frac{{{rt-rb:.3f}}}{{{H:.3f}}}y"
    )

    st.write("### Integral del volumen")
    st.latex(
        r"V=\pi\int_0^H [r(y)]^2\,dy"
    )

    st.write("### Volumen calculado")
    st.latex(
        r"V=\frac{\pi H}{3}"
        r"(r_b^2+r_b r_t+r_t^2)"
    )
    st.write(f"Resultado: **{V:.6f} m³**")

st.divider()

st.subheader("Interpretación de ingeniería")

st.write(
    "Al modificar la altura y los radios, cambian la geometría, "
    "las áreas de las secciones y el volumen de concreto. "
    "Esto permite estudiar cómo las dimensiones influyen en "
    "la cantidad de material utilizada."
)

st.info(
    "Este modelo es geométrico y académico. El costo depende "
    "del precio supuesto por el usuario. La aplicación no "
    "verifica la capacidad resistente ni la seguridad estructural "
    "de la columna."
)

