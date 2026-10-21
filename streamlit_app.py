
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
# ==========================================
# MODULO ESTRUCTURAL BASICO
# ==========================================

st.divider()
st.header("Analisis estructural preliminar")

st.write(
    "Estudio academico de una columna de concreto "
    "con seccion circular variable sometida a carga axial."
)

st.warning(
    "Este modulo es educativo. No determina la capacidad "
    "resistente ni certifica la seguridad estructural "
    "de una columna real."
)

# Datos introducidos por el usuario
st.subheader("1. Parametros de analisis")

carga_axial = st.number_input(
    "Carga axial externa aplicada (kN)",
    min_value=0.0,
    max_value=10000.0,
    value=500.0,
    step=25.0
)

peso_unitario = st.number_input(
    "Peso unitario del concreto (kN/m3)",
    min_value=0.0,
    max_value=30.0,
    value=24.0,
    step=0.5
)

fc = st.number_input(
    "Resistencia especificada del concreto f'c (MPa)",
    min_value=1.0,
    max_value=100.0,
    value=28.0,
    step=1.0
)

# Geometria de las secciones
area_base = np.pi * rb**2
area_superior = np.pi * rt**2

# Peso propio de la columna
peso_propio = peso_unitario * V

# Fuerza axial estimada en cada extremo.
# Se supone una carga externa aplicada en la parte superior
# y se considera el peso propio distribuido de la columna.
fuerza_superior = carga_axial
fuerza_base = carga_axial + peso_propio

# Esfuerzo promedio: kN/m2 convertido a MPa.
# 1 MPa = 1000 kN/m2.
if area_base > 0 and area_superior > 0:
    esfuerzo_base = fuerza_base / area_base / 1000
    esfuerzo_superior = fuerza_superior / area_superior / 1000
else:
    esfuerzo_base = 0.0
    esfuerzo_superior = 0.0

# Resultados
st.subheader("2. Resultados")

m1, m2, m3 = st.columns(3)

m1.metric(
    "Peso propio",
    f"{peso_propio:.2f} kN"
)

m2.metric(
    "Fuerza axial en la base",
    f"{fuerza_base:.2f} kN"
)

m3.metric(
    "Fuerza axial en la parte superior",
    f"{fuerza_superior:.2f} kN"
)

st.subheader("3. Esfuerzos promedio")

r1, r2 = st.columns(2)

r1.metric(
    "Esfuerzo promedio en la base",
    f"{esfuerzo_base:.3f} MPa"
)

r2.metric(
    "Esfuerzo promedio superior",
    f"{esfuerzo_superior:.3f} MPa"
)

st.write(
    "El esfuerzo promedio se calcula como la fuerza axial "
    "dividida entre el area de la seccion transversal."
)

st.latex(r"\sigma = \frac{N}{A}")

# Tabla comparativa
import pandas as pd

tabla_estructural = pd.DataFrame({
    "Seccion": ["Base", "Superior"],
    "Radio (m)": [rb, rt],
    "Area (m2)": [area_base, area_superior],
    "Fuerza axial (kN)": [fuerza_base, fuerza_superior],
    "Esfuerzo promedio (MPa)": [
        esfuerzo_base, esfuerzo_superior
    ]
})

st.dataframe(
    tabla_estructural,
    use_container_width=True,
    hide_index=True
)

# Interpretacion
st.subheader("4. Interpretacion de resultados")

if area_superior < area_base:
    st.write(
        "La seccion superior tiene menor area que la base. "
        "Bajo la misma fuerza axial, una menor area produce "
        "un mayor esfuerzo promedio."
    )
elif area_superior > area_base:
    st.write(
        "La seccion superior tiene mayor area que la base. "
        "Para una misma fuerza axial, su esfuerzo promedio "
        "seria menor."
    )
else:
    st.write(
        "Las dos secciones tienen la misma area. "
        "La variacion del esfuerzo depende de la fuerza axial "
        "que actua en cada seccion."
    )

st.subheader("5. Alcance y limitaciones")

st.write(
    f"La resistencia especificada del concreto introducida "
    f"es f'c = {fc:.1f} MPa. Este dato caracteriza el material, "
    "pero no basta para calcular la capacidad resistente "
    "de la columna."
)

st.write(
    "El analisis no incluye acero de refuerzo, excentricidad, "
    "momentos flectores, esbeltez, efectos de segundo orden, "
    "combinaciones de carga ni verificaciones normativas. "
    "Por tanto, los resultados son estimaciones academicas "
    "de esfuerzos promedio y no constituyen un diseno estructural."
)

