import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Nafta Super CABA - Evolución Histórica",
    page_icon="⛽",
    layout="wide"
)

# ── Datos históricos ─────────────────────────────────────────────────────────
# Precios nafta súper YPF en CABA (ARS/litro) — fuentes: Surtidores, Infobae,
# La Nación, El Economista, Ambito, El Cronista.
raw_data = {
    "fecha": [
        "2021-01","2021-02","2021-03","2021-04","2021-05","2021-06",
        "2021-07","2021-08","2021-09","2021-10","2021-11","2021-12",
        "2022-01","2022-02","2022-03","2022-04","2022-05","2022-06",
        "2022-07","2022-08","2022-09","2022-10","2022-11","2022-12",
        "2023-01","2023-02","2023-03","2023-04","2023-05","2023-06",
        "2023-07","2023-08","2023-09","2023-10","2023-11","2023-12",
        "2024-01","2024-02","2024-03","2024-04","2024-05","2024-06",
        "2024-07","2024-08","2024-09","2024-10","2024-11","2024-12",
        "2025-01","2025-02","2025-03","2025-04","2025-05","2025-06",
        "2025-07","2025-08","2025-09","2025-10","2025-11","2025-12",
        "2026-01","2026-02","2026-03",
    ],
    # ARS por litro (nafta súper YPF en CABA)
    "ars": [
        62.0,  62.0,  62.0,  65.5,  65.5,  65.5,
        68.0,  68.0,  72.0,  78.0,  78.0,  82.0,
        99.0,  99.0, 103.0, 115.0, 118.0, 122.0,
       128.0, 130.0, 135.0, 142.0, 146.5, 150.9,
       150.9, 155.0, 162.0, 175.0, 183.0, 197.0,
       215.0, 230.0, 248.0, 260.0, 311.0, 380.0,
       699.0, 734.0, 762.0, 800.0, 836.0, 878.0,
       941.0, 974.0, 1005.0,1040.0,1068.0,1096.0,
      1128.0,1145.0,1173.0,1194.0,1214.0,1240.0,
      1265.0,1300.0,1340.0,1380.0,1430.0,1520.0,
      1680.0,1800.0,1920.0,
    ],
    # Dólar oficial (ARS/USD) — BCRA / Banco Nación
    "usd_oficial": [
        84,  85,  87,  92,  93,  95,
        97,  98, 100, 102, 103, 104,
       104, 105, 107, 113, 117, 124,
       131, 138, 141, 157, 163, 168,
       177, 188, 193, 216, 231, 258,
       265, 285, 341, 350, 365, 400,
       820, 825, 835, 870, 905, 920,
       940, 952, 960, 985, 997,1010,
      1025,1040,1070,1100,1110,1125,
      1145,1165,1195,1218,1240,1270,
      1300,1340,1378,
    ],
    # Dólar blue (mercado informal) — referencia alternativa
    "usd_blue": [
        165, 148, 145, 155, 165, 175,
        185, 186, 188, 196, 193, 207,
        210, 210, 205, 208, 208, 230,
        280, 285, 290, 285, 303, 330,
        375, 368, 380, 413, 484, 500,
        520, 590, 724, 815, 950,1000,
       1045,1045,1055,1080,1230,1480,
       1425,1335,1275,1220,1095,1050,
       1270,1255,1275,1250,1220,1225,
       1250,1260,1280,1300,1310,1320,
       1360,1390,1400,
    ],
}

df = pd.DataFrame(raw_data)
df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m")
df["usd_litro_oficial"] = df["ars"] / df["usd_oficial"]
df["usd_litro_blue"]    = df["ars"] / df["usd_blue"]

# ── Estilos CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130 0%, #262b3d 100%);
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 18px 22px;
        text-align: center;
    }
    .metric-label { color: #8b92a5; font-size: 13px; margin-bottom: 4px; }
    .metric-value { color: #f0f2f5; font-size: 26px; font-weight: 700; }
    .metric-delta-up   { color: #ff6b6b; font-size: 13px; margin-top: 4px; }
    .metric-delta-down { color: #6bcb77; font-size: 13px; margin-top: 4px; }
    .source-note { color: #555e7a; font-size: 11px; margin-top: 6px; }
    h1 { color: #f0f2f5 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("# ⛽ Nafta Súper — Evolución Histórica en CABA")
st.markdown(
    "Precio por litro de **nafta súper YPF** en la Ciudad de Buenos Aires "
    "| Enero 2021 – Marzo 2026"
)
st.divider()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuración")

    modo = st.radio(
        "Moneda",
        ["USD — Dólar oficial", "USD — Dólar blue / informal", "ARS — Pesos"],
        index=0,
    )

    rango = st.select_slider(
        "Rango de fechas",
        options=df["fecha"].dt.strftime("%b %Y").tolist(),
        value=(
            df["fecha"].dt.strftime("%b %Y").tolist()[0],
            df["fecha"].dt.strftime("%b %Y").tolist()[-1],
        ),
    )

    mostrar_eventos = st.checkbox("Mostrar eventos clave", value=True)
    mostrar_promedio = st.checkbox("Mostrar media móvil 3 meses", value=False)

    st.divider()
    st.markdown("""
    **Fuentes:**  
    Surtidores.com.ar · Infobae · La Nación  
    El Economista · Ámbito · BCRA  
    """)
    st.markdown('<p class="source-note">Datos aproximados. Precio YPF CABA.</p>', unsafe_allow_html=True)

# Filtrar por rango
fechas_str = df["fecha"].dt.strftime("%b %Y").tolist()
idx_ini = fechas_str.index(rango[0])
idx_fin = fechas_str.index(rango[1])
dff = df.iloc[idx_ini : idx_fin + 1].copy()

# Columna activa según modo
if "oficial" in modo:
    col_y    = "usd_litro_oficial"
    simbolo  = "USD"
    label_y  = "USD / litro (dólar oficial)"
    color_ln = "#4fc3f7"
elif "blue" in modo:
    col_y    = "usd_litro_blue"
    simbolo  = "USD"
    label_y  = "USD / litro (dólar blue)"
    color_ln = "#ffb347"
else:
    col_y    = "ars"
    simbolo  = "ARS"
    label_y  = "ARS / litro"
    color_ln = "#69f0ae"

fmt = ".2f" if simbolo == "USD" else ",.0f"

# ── KPIs ─────────────────────────────────────────────────────────────────────
val_actual  = dff[col_y].iloc[-1]
val_inicial = dff[col_y].iloc[0]
val_min     = dff[col_y].min()
val_max     = dff[col_y].max()
variacion   = (val_actual / val_inicial - 1) * 100

c1, c2, c3, c4 = st.columns(4)

def kpi(col, label, value, delta=None, delta_label=""):
    delta_html = ""
    if delta is not None:
        sign = "▲" if delta > 0 else "▼"
        cls  = "delta-up" if delta > 0 else "delta-down"
        delta_html = f'<div class="metric-{cls}">{sign} {abs(delta):.1f}% {delta_label}</div>'
    col.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{simbolo} {value:{fmt.replace(',','').replace('.2f',',.2f')}}</div>
            {delta_html}
        </div>""",
        unsafe_allow_html=True,
    )

with c1: kpi(c1, "Precio actual (Mar 2026)", val_actual, variacion, "vs inicio período")
with c2: kpi(c2, f"Precio inicio ({dff['fecha'].iloc[0].strftime('%b %Y')})", val_inicial)
with c3: kpi(c3, "Mínimo del período", val_min)
with c4: kpi(c4, "Máximo del período", val_max)

st.markdown("<br>", unsafe_allow_html=True)

# ── Eventos clave ────────────────────────────────────────────────────────────
eventos = [
    {"fecha": "2022-03", "label": "Acuerdo FMI",        "color": "#aaaaff"},
    {"fecha": "2022-07", "label": "Crisis gasoil",       "color": "#ffdd57"},
    {"fecha": "2023-08", "label": "Devaluación Massa",   "color": "#ff9944"},
    {"fecha": "2023-12", "label": "Asunción Milei\n+devaluación", "color": "#ff4444"},
    {"fecha": "2025-04", "label": "Flotación del peso",  "color": "#44ff99"},
    {"fecha": "2026-02", "label": "Conflicto Medio Oriente\n→ suba combustibles", "color": "#ff6688"},
]

# ── Gráfico principal ────────────────────────────────────────────────────────
fig = go.Figure()

# Área rellena
fig.add_trace(go.Scatter(
    x=dff["fecha"], y=dff[col_y],
    fill="tozeroy",
    fillcolor=color_ln.replace(")", ", 0.12)").replace("rgb", "rgba").replace("#", "rgba(")
              if "#" in color_ln else color_ln,
    line=dict(color=color_ln, width=0),
    showlegend=False, hoverinfo="skip",
    name="área",
))
# Overwrite with simple fillcolor
fig.update_traces(
    selector=dict(name="área"),
    fillcolor=f"rgba(79,195,247,0.10)" if "oficial" in modo
              else ("rgba(255,179,71,0.10)" if "blue" in modo else "rgba(105,240,174,0.10)"),
)

# Línea principal
fig.add_trace(go.Scatter(
    x=dff["fecha"], y=dff[col_y],
    mode="lines+markers",
    name=label_y,
    line=dict(color=color_ln, width=2.5),
    marker=dict(size=5, color=color_ln),
    hovertemplate=(
        "<b>%{x|%B %Y}</b><br>"
        f"{label_y}: <b>%{{y:{fmt}}}</b><extra></extra>"
    ),
))

# Media móvil
if mostrar_promedio and len(dff) >= 3:
    dff["mm3"] = dff[col_y].rolling(3, center=True).mean()
    fig.add_trace(go.Scatter(
        x=dff["fecha"], y=dff["mm3"],
        mode="lines", name="Media móvil 3m",
        line=dict(color="#ffffff", width=1.5, dash="dot"),
        opacity=0.6,
        hovertemplate="MM3: <b>%{y:.2f}</b><extra></extra>",
    ))

# Eventos clave
if mostrar_eventos:
    for ev in eventos:
        ev_fecha = pd.to_datetime(ev["fecha"])
        if dff["fecha"].min() <= ev_fecha <= dff["fecha"].max():
            y_val = dff.loc[dff["fecha"] == ev_fecha, col_y]
            if y_val.empty:
                # buscar más cercana
                idx_cerca = (dff["fecha"] - ev_fecha).abs().idxmin()
                ev_fecha  = dff.loc[idx_cerca, "fecha"]
                y_val     = dff.loc[idx_cerca, col_y]
            else:
                y_val = y_val.values[0]

            fig.add_vline(
                x=ev_fecha.timestamp() * 1000,
                line=dict(color=ev["color"], width=1.2, dash="dash"),
                opacity=0.6,
            )
            fig.add_annotation(
                x=ev_fecha, y=y_val,
                text=ev["label"].replace("\n", "<br>"),
                showarrow=True, arrowhead=2, arrowsize=1,
                arrowcolor=ev["color"],
                font=dict(size=10, color=ev["color"]),
                bgcolor="#1e2130", bordercolor=ev["color"],
                borderwidth=1, borderpad=4,
                ax=30, ay=-40,
            )

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0f1117",
    plot_bgcolor="#0f1117",
    height=460,
    margin=dict(l=10, r=10, t=40, b=10),
    title=dict(
        text=f"Precio nafta súper YPF — CABA | {label_y}",
        font=dict(size=15, color="#c9d1e0"),
    ),
    xaxis=dict(
        showgrid=True, gridcolor="#1e2130",
        title="", tickfont=dict(color="#8b92a5"),
        tickangle=-30,
    ),
    yaxis=dict(
        showgrid=True, gridcolor="#1e2130",
        title=label_y, tickfont=dict(color="#8b92a5"),
        tickprefix=f"{simbolo} ",
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)",
        font=dict(color="#8b92a5"),
    ),
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

# ── Gráfico de variación interanual ─────────────────────────────────────────
st.markdown("### 📊 Variación interanual (%)")

dff_var = dff.copy()
dff_var["var_anual"] = dff_var[col_y].pct_change(12) * 100
dff_var = dff_var.dropna(subset=["var_anual"])

if not dff_var.empty:
    colors_bar = ["#ff6b6b" if v > 0 else "#6bcb77" for v in dff_var["var_anual"]]
    fig2 = go.Figure(go.Bar(
        x=dff_var["fecha"],
        y=dff_var["var_anual"],
        marker_color=colors_bar,
        hovertemplate="<b>%{x|%B %Y}</b><br>Var. anual: <b>%{y:.1f}%</b><extra></extra>",
    ))
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, tickfont=dict(color="#8b92a5"), tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor="#1e2130", tickfont=dict(color="#8b92a5"),
                   ticksuffix="%"),
        hovermode="x unified",
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Se necesitan al menos 13 meses de datos para calcular variación anual.")

# ── Tabla de datos ───────────────────────────────────────────────────────────
with st.expander("📋 Ver tabla de datos completa"):
    tabla = dff[["fecha","ars","usd_litro_oficial","usd_litro_blue"]].copy()
    tabla["fecha"] = tabla["fecha"].dt.strftime("%b %Y")
    tabla.columns = ["Mes", "ARS/litro", "USD/litro (oficial)", "USD/litro (blue)"]
    tabla["ARS/litro"] = tabla["ARS/litro"].map("{:,.1f}".format)
    tabla["USD/litro (oficial)"] = tabla["USD/litro (oficial)"].map("{:.3f}".format)
    tabla["USD/litro (blue)"]    = tabla["USD/litro (blue)"].map("{:.3f}".format)
    st.dataframe(tabla, use_container_width=True, hide_index=True)

# ── Nota metodológica ────────────────────────────────────────────────────────
st.markdown("""
---
<small style='color:#555e7a'>
📌 <b>Metodología:</b> Precios de nafta súper YPF en estaciones de servicio de CABA.  
El tipo de cambio oficial corresponde al valor de venta del Banco Nación (BCRA).  
El dólar blue es el tipo de cambio del mercado informal. Datos de referencia — pueden diferir levemente según fecha y estación.  
Fuentes: Surtidores.com.ar, Infobae, La Nación, El Economista, Ámbito, BCRA.
</small>
""", unsafe_allow_html=True)
