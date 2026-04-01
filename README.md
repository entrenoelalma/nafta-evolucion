# ⛽ Nafta Súper — Evolución Histórica en CABA

Aplicación interactiva que muestra la evolución del precio de la **nafta súper YPF** en la Ciudad de Buenos Aires entre **enero 2021 y marzo 2026**, con conversión a dólares (oficial y blue).

🔗 **[Ver app en vivo](https://musitani-nafta-evolucion-nafta-historico.streamlit.app)**

---

## 📸 Capturas

> _Agregá una captura de pantalla de la app aquí._

---

## 📊 Qué muestra la app

- Precio mensual en **ARS**, **USD oficial** y **USD blue/informal**
- Gráfico interactivo con zoom, tooltips y eventos históricos clave:
  - Acuerdo FMI (mar 2022)
  - Crisis del gasoil (jul 2022)
  - Devaluación Massa (ago 2023)
  - Asunción Milei + devaluación (dic 2023)
  - Flotación del peso (abr 2025)
  - Conflicto Medio Oriente → suba combustibles (feb 2026)
- Variación interanual en barras
- Media móvil de 3 meses (opcional)
- Tabla de datos completa

---

## 🚀 Correr localmente

```bash
git clone https://github.com/musitani/nafta-evolucion.git
cd nafta-evolucion
pip install -r requirements.txt
streamlit run nafta_historico.py
```

La app abre automáticamente en `http://localhost:8501`.

---

## 🗂️ Estructura del proyecto

```
nafta-evolucion/
├── nafta_historico.py   # App principal (Streamlit + Plotly)
├── requirements.txt     # Dependencias
└── README.md
```

---

## 📦 Dependencias

| Paquete | Versión mínima |
|---|---|
| streamlit | 1.32.0 |
| plotly | 5.20.0 |
| pandas | 2.0.0 |
| numpy | 1.26.0 |

---

## 📰 Fuentes de datos

Los precios corresponden a la nafta súper YPF en estaciones de servicio de CABA. Los tipos de cambio son valores de venta del Banco Nación (oficial) y del mercado informal (blue).

- [Surtidores.com.ar](https://surtidores.com.ar)
- [Infobae — Economía](https://www.infobae.com/economia/)
- [La Nación — Economía](https://www.lanacion.com.ar/economia/)
- [Ámbito Financiero](https://www.ambito.com)
- [El Economista](https://eleconomista.com.ar)
- [BCRA — Banco Central de la República Argentina](https://www.bcra.gob.ar)

> Los datos son de referencia y pueden diferir levemente según la fecha exacta y la estación de servicio.

---

## 📝 Licencia

MIT — libre para usar, modificar y compartir.
