import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Nafta Súper CABA — Evolución Histórica",
    page_icon="⛽",
    layout="wide",
)

# ── Traducción de meses ───────────────────────────────────────────────────────
MESES_ES = {
    "Jan": "Ene", "Feb": "Feb", "Mar": "Mar", "Apr": "Abr",
    "May": "May", "Jun": "Jun", "Jul": "Jul", "Aug": "Ago",
    "Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dec": "Dic",
}

def mes_es(fecha):
    s = fecha.strftime("%b %Y")
    for en, es in MESES_ES.items():
        s = s.replace(en, es)
    return s

# ── Datos históricos ──────────────────────────────────────────────────────────
raw = {
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
    "ars": [
         62.0,  62.0,  62.0,  65.5,  65.5,  65.5,
         68.0,  68.0,  72.0,  78.0,  78.0,  82.0,
         99.0,  99.0, 103.0, 115.0, 118.0, 122.0,
        128.0, 130.0, 135.0, 142.0, 146.5, 150.9,
        150.9, 155.0, 162.0, 175.0, 183.0, 197.0,
        215.0, 230.0, 248.0, 260.0, 311.0, 380.0,
        699.0, 734.0, 762.0, 800.0, 836.0, 878.0,
        941.0, 974.0,1005.0,1040.0,1068.0,1096.0,
       1128.0,1145.0,1173.0,1194.0,1214.0,1240.0,
       1265.0,1300.0,1340.0,1380.0,1430.0,1520.0,
       1680.0,1800.0,1920.0,
    ],
    "tc_oficial": [
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
    "tc_blue": [
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

df = pd.DataFrame(raw)
df["fecha"]       = pd.to_datetime(df["fecha"], format="%Y-%m")
df["usd_oficial"] = df["ars"] / df["tc_oficial"]
df["usd_blue"]    = df["ars"] / df["tc_blue"]
df["fecha_es"]    = df["fecha"].apply(mes_es)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.kpi-card {
    background: linear-gradient(135deg,#1a1f2e 0%,#242938 100%);
    border: 1px solid #2a3050;
    border-radius: 14px;
    padding: 20px 18px 16px;
    text-align: center;
    min-height: 108px;
}
.kpi-label   { color:#7a839a; font-size:11px; letter-spacing:.6px; text-transform:uppercase; margin-bottom:8px; }
.kpi-value   { color:#eef0f5; font-size:26px; font-weight:700; letter-spacing:-0.5px; }
.kpi-up      { color:#ff6b6b; font-size:12px; margin-top:6px; }
.kpi-down    { color:#6bcb77; font-size:12px; margin-top:6px; }
.kpi-neutral { color:#7a839a; font-size:12px; margin-top:6px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# ⛽ Nafta Súper — Evolución Histórica en CABA")
st.caption("Precio por litro · Nafta súper YPF · Ciudad de Buenos Aires · Ene 2021 – Mar 2026")
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Opciones")

    modo = st.radio(
        "Moneda",
        ["🇺🇸 USD — Dólar oficial", "💵 USD — Dólar blue", "🇦🇷 ARS — Pesos"],
        index=0,
    )

    fechas_labels = df["fecha_es"].tolist()
    idx_ini, idx_fin = st.select_slider(
        "Rango de fechas",
        options=list(range(len(fechas_labels))),
        value=(0, len(fechas_labels) - 1),
        format_func=lambda i: fechas_labels[i],
    )

    st.markdown("---")
    mostrar_eventos  = st.checkbox("Eventos históricos", value=True)
    mostrar_mm       = st.checkbox("Media móvil 3 meses", value=False)
    mostrar_comparar = st.checkbox("Comparar oficial vs blue", value=False)

    st.markdown("---")
    st.markdown("""
**Fuentes**  
Surtidores.com.ar · Infobae  
La Nación · Ámbito · BCRA
""")
    st.caption("Precios de referencia YPF CABA.\nPueden variar por estación y fecha exacta.")

# ── Filtrar datos ─────────────────────────────────────────────────────────────
dff = df.iloc[idx_ini : idx_fin + 1].copy().reset_index(drop=True)

# ── Config según modo ─────────────────────────────────────────────────────────
if "oficial" in modo:
    col_y  = "usd_oficial"
    simbolo = "USD"
    label_y = "USD / litro (dólar oficial)"
    color1  = "#4fc3f7"
    fill1   = "rgba(79,195,247,0.10)"
elif "blue" in modo:
    col_y  = "usd_blue"
    simbolo = "USD"
    label_y = "USD / litro (dólar blue)"
    color1  = "#ffb347"
    fill1   = "rgba(255,179,71,0.10)"
else:
    col_y  = "ars"
    simbolo = "ARS"
    label_y = "ARS / litro"
    color1  = "#69f0ae"
    fill1   = "rgba(105,240,174,0.10)"

def fmt_val(v):
    if simbolo == "USD":
        return "USD {:,.2f}".format(v)
    return "$ {:,.0f}".format(v)

# ── KPIs ──────────────────────────────────────────────────────────────────────
val_actual  = dff[col_y].iloc[-1]
val_inicial = dff[col_y].iloc[0]
val_min     = dff[col_y].min()
val_max     = dff[col_y].max()
variacion   = (val_actual / val_inicial - 1) * 100

fecha_ini_label = dff["fecha_es"].iloc[0]
fecha_fin_label = dff["fecha_es"].iloc[-1]

sign = "▲" if variacion > 0 else "▼"
cls  = "kpi-up" if variacion > 0 else "kpi-down"
badge = '<div class="{}">{} {:.1f}% vs {}</div>'.format(cls, sign, abs(variacion), fecha_ini_label)

def kpi_html(label, value_str, extra=""):
    return (
        '<div class="kpi-card">'
        '<div class="kpi-label">{}</div>'
        '<div class="kpi-value">{}</div>'
        '{}'
        '</div>'
    ).format(label, value_str, extra)

c1, c2, c3, c4 = st.columns(4)
c1.markdown(kpi_html("Precio actual · " + fecha_fin_label, fmt_val(val_actual), badge),
            unsafe_allow_html=True)
c2.markdown(kpi_html("Precio inicial · " + fecha_ini_label, fmt_val(val_inicial)),
            unsafe_allow_html=True)
c3.markdown(kpi_html("Mínimo del período", fmt_val(val_min)),
            unsafe_allow_html=True)
c4.markdown(kpi_html("Máximo del período", fmt_val(val_max)),
            unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Eventos clave ─────────────────────────────────────────────────────────────
EVENTOS = [
    ("2022-03", "Acuerdo FMI",            "#aaaaff",  35, -50),
    ("2022-07", "Crisis gasoil",           "#ffdd57",  35, -50),
    ("2023-08", "Devaluación Massa",       "#ff9944",  35, -50),
    ("2023-12", "Asunción Milei",          "#ff4444", -80, -50),
    ("2025-04", "Flotación del peso",      "#44ff99",  35, -50),
    ("2026-02", "Conflicto Medio Oriente", "#ff6688", -110, -50),
]

# ── Gráfico principal ─────────────────────────────────────────────────────────
fig = go.Figure()

if mostrar_comparar and simbolo == "USD":
    series = [
        ("usd_oficial", "#4fc3f7", "rgba(79,195,247,0.08)",  "Dólar oficial"),
        ("usd_blue",    "#ffb347", "rgba(255,179,71,0.08)",  "Dólar blue"),
    ]
    for col, color, fill, name in series:
        fig.add_trace(go.Scatter(
            x=dff["fecha"], y=dff[col],
            fill="tozeroy", fillcolor=fill,
            line=dict(color=color, width=0),
            showlegend=False, hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=dff["fecha"], y=dff[col],
            mode="lines+markers", name=name,
            line=dict(color=color, width=2.5),
            marker=dict(size=4, color=color),
            hovertemplate="<b>%{x|%b %Y}</b><br>" + name + ": <b>USD %{y:.3f}</b><extra></extra>",
        ))
else:
    fig.add_trace(go.Scatter(
        x=dff["fecha"], y=dff[col_y],
        fill="tozeroy", fillcolor=fill1,
        line=dict(color=color1, width=0),
        showlegend=False, hoverinfo="skip",
    ))
    if simbolo == "USD":
        hover_fmt = "<b>%{x|%b %Y}</b><br>" + label_y + ": <b>USD %{y:.3f}</b><extra></extra>"
    else:
        hover_fmt = "<b>%{x|%b %Y}</b><br>" + label_y + ": <b>$ %{y:,.0f}</b><extra></extra>"
    fig.add_trace(go.Scatter(
        x=dff["fecha"], y=dff[col_y],
        mode="lines+markers", name=label_y,
        line=dict(color=color1, width=2.5),
        marker=dict(size=5, color=color1),
        hovertemplate=hover_fmt,
    ))

# Media móvil
if mostrar_mm and len(dff) >= 3:
    dff["mm3"] = dff[col_y].rolling(3, center=True).mean()
    fig.add_trace(go.Scatter(
        x=dff["fecha"], y=dff["mm3"],
        mode="lines", name="Media móvil 3m",
        line=dict(color="#ffffff", width=1.5, dash="dot"),
        opacity=0.55,
        hovertemplate="MM3: <b>%{y:.3f}</b><extra></extra>",
    ))

# Eventos
if mostrar_eventos:
    for fecha_str, label, color, ax, ay in EVENTOS:
        ev_fecha = pd.to_datetime(fecha_str)
        if not (dff["fecha"].min() <= ev_fecha <= dff["fecha"].max()):
            continue
        mask = dff["fecha"] == ev_fecha
        if mask.any():
            y_ev = float(dff.loc[mask, col_y].values[0])
        else:
            idx_c = (dff["fecha"] - ev_fecha).abs().idxmin()
            ev_fecha = dff.loc[idx_c, "fecha"]
            y_ev = float(dff.loc[idx_c, col_y])

        fig.add_vline(
            x=ev_fecha.timestamp() * 1000,
            line=dict(color=color, width=1.2, dash="dash"),
            opacity=0.55,
        )
        fig.add_annotation(
            x=ev_fecha, y=y_ev,
            text=label,
            showarrow=True, arrowhead=2, arrowsize=0.8,
            arrowcolor=color,
            font=dict(size=10, color=color),
            bgcolor="#1a1f2e", bordercolor=color,
            borderwidth=1, borderpad=5,
            ax=ax, ay=ay,
        )

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    height=460,
    margin=dict(l=10, r=10, t=45, b=10),
    title=dict(
        text="Nafta súper YPF · CABA  |  " + label_y,
        font=dict(size=14, color="#c0c8d8"),
        x=0.01,
    ),
    xaxis=dict(
        showgrid=True, gridcolor="#1a2030", gridwidth=1,
        tickfont=dict(color="#6b7590", size=11),
        tickformat="%b %Y",
    ),
    yaxis=dict(
        showgrid=True, gridcolor="#1a2030", gridwidth=1,
        tickfont=dict(color="#6b7590", size=11),
        title=dict(text=label_y, font=dict(color="#6b7590", size=11)),
        tickprefix=simbolo + " ",
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0.3)", bordercolor="#2a3050", borderwidth=1,
        font=dict(color="#8b92a5", size=11),
    ),
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

# ── Variación interanual ──────────────────────────────────────────────────────
st.markdown("### 📊 Variación interanual (%)")

dff2 = dff.copy()
dff2["var_anual"] = dff2[col_y].pct_change(12) * 100
dff2 = dff2.dropna(subset=["var_anual"])

if not dff2.empty:
    colors_bar = ["#ff6b6b" if v > 0 else "#6bcb77" for v in dff2["var_anual"]]
    fig2 = go.Figure(go.Bar(
        x=dff2["fecha"],
        y=dff2["var_anual"],
        marker_color=colors_bar,
        hovertemplate="<b>%{x|%b %Y}</b><br>Variación anual: <b>%{y:.1f}%</b><extra></extra>",
    ))
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        height=240,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, tickfont=dict(color="#6b7590", size=11),
                   tickformat="%b %Y"),
        yaxis=dict(showgrid=True, gridcolor="#1a2030",
                   tickfont=dict(color="#6b7590", size=11), ticksuffix="%"),
        hovermode="x unified",
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Se necesitan al menos 13 meses de datos para mostrar variación anual.")

# ── Tabla ─────────────────────────────────────────────────────────────────────
with st.expander("📋 Ver tabla de datos completa"):
    tabla = dff[["fecha_es", "ars", "tc_oficial", "usd_oficial", "tc_blue", "usd_blue"]].copy()
    tabla.columns = ["Mes", "ARS / litro", "TC Oficial", "USD / litro (oficial)", "TC Blue", "USD / litro (blue)"]
    tabla["ARS / litro"]           = tabla["ARS / litro"].map("$ {:,.1f}".format)
    tabla["TC Oficial"]            = tabla["TC Oficial"].map("$ {:,.0f}".format)
    tabla["USD / litro (oficial)"] = tabla["USD / litro (oficial)"].map("USD {:.3f}".format)
    tabla["TC Blue"]               = tabla["TC Blue"].map("$ {:,.0f}".format)
    tabla["USD / litro (blue)"]    = tabla["USD / litro (blue)"].map("USD {:.3f}".format)
    st.dataframe(tabla, use_container_width=True, hide_index=True)

# ── Nota ──────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "📌 Datos de referencia basados en precios de nafta súper YPF en CABA. "
    "Tipo de cambio oficial: Banco Nación (BCRA). Dólar blue: mercado informal. "
    "Fuentes: Surtidores.com.ar · Infobae · La Nación · Ámbito · El Economista · BCRA."
)
