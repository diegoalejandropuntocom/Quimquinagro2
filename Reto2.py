#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard financiero interactivo — QuimQuinAgro 2025
Autor: Diego Alejandro Ramírez Benítez
Versión adaptada y mejorada por GPT-5
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ==============================================================
# CONFIGURACIÓN INICIAL
# ==============================================================

DB_PATH = "contabilidad.db"

st.set_page_config(
    page_title="Diego Alejandro Ramírez",
    layout="wide",
    page_icon="💰"
)

st.markdown("<h1 style='color: green'>Información financiera QuimQuinAgro 👨🏻‍🌾🐟🎣</h1>", unsafe_allow_html=True)

st.write("""
Este tablero interactivo permite visualizar el comportamiento financiero de la asociación **QuimQuinAgro** durante el año 2025.  
A través de las secciones disponibles puedes analizar la **evolución de ingresos y egresos mensuales**, identificar los **principales gastos**,  
y observar la **participación de cada socio en los ingresos registrados**.  
Utiliza el menú lateral para explorar cada consulta de forma independiente.
""")

# ==============================================================
# FUNCIÓN DE CONEXIÓN
# ==============================================================

@st.cache_data
def ejecutar_consulta(query: str) -> pd.DataFrame:
    """Ejecuta una consulta SQL en la base de datos y devuelve un DataFrame."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Error ejecutando consulta: {e}")
        return pd.DataFrame()

# ==============================================================
# MENÚ LATERAL
# ==============================================================

opcion = st.sidebar.radio(
    "Selecciona la consulta que deseas visualizar:",
    [
        "📦 Caja mensual",
        "💸 Top 10 egresos",
        "💰 Ingresos por socio (CXC) — 2025",
        "💰 Ingresos por socio (CXC) — 2024",
        "💰 Ingresos por socio (CXC) — 2023"
    ]
)


# ==============================================================
# SECCIÓN 1: CAJA MENSUAL
# ==============================================================

if opcion == "📦 Caja mensual":
    st.subheader("📦 Caja mensual (básico)")
    st.write("""
    Durante 2025 se observó un comportamiento financiero irregular: los ingresos alcanzan su punto más alto en enero y febrero, 
    superando ampliamente a los egresos y reflejando un inicio de año favorable. 
    A partir de marzo comienza una fuerte disminución que se acentúa hacia el segundo semestre, 
    donde incluso no se registran ingresos en varios meses. Los egresos, aunque más estables, 
    presentan picos en febrero y abril. Esto sugiere gastos operativos concentrados en ciertas fechas. 
    El gráfico evidencia una buena gestión inicial, pero una pérdida progresiva de flujo de caja, 
    indicando la necesidad de estrategias para mantener ingresos constantes y equilibrar los gastos.
    """)

    with st.expander("📊 Mostrar gráficos de caja mensual"):
        consulta_caja = """
            SELECT 
                substr(fecha,1,7) AS mes,
                ROUND(SUM(COALESCE(abono,0)),2) AS total_ingresos,
                ROUND(SUM(COALESCE(prestamo,0)),2) AS total_egresos
            FROM caja2025
            GROUP BY mes
            ORDER BY mes;
        """
        df_caja = ejecutar_consulta(consulta_caja)

        if df_caja.empty:
            st.warning("No se encontraron datos en la tabla `caja2025`.")
        else:
            st.dataframe(df_caja, use_container_width=True)

            fig = px.bar(
                df_caja,
                x="mes",
                y=["total_ingresos", "total_egresos"],
                barmode="group",
                title="Totales mensuales de ingresos y egresos — 2025",
                color_discrete_sequence=["#1f77b4", "#FFC107"]
            )
            st.plotly_chart(fig, use_container_width=True)

# ==============================================================
# SECCIÓN 2: TOP 10 EGRESOS
# ==============================================================

elif opcion == "💸 Top 10 egresos":
    st.subheader("💸 Top 10 egresos más altos")
    st.write("""
    Durante el año 2025, los ingresos se concentran en pocos socios, lo que refleja una alta dependencia financiera de un número reducido de aportantes. 
    Entre ellos, destacan aquellos con mayores registros de “salida” asociados a cuentas por cobrar, mientras que otros socios presentan actividad mínima o nula. 
    Esta desigualdad sugiere la necesidad de diversificar las fuentes de ingreso y fortalecer la participación de los socios con menor aporte. 
    El gráfico evidencia una concentración marcada que, si bien facilita la gestión administrativa, representa un riesgo financiero ante posibles incumplimientos 
    o falta de continuidad de los socios más activos.
    """)

    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha inicial", pd.to_datetime("2025-01-01"))
    with col2:
        fecha_fin = st.date_input("Fecha final", pd.to_datetime("2025-12-31"))

    with st.expander("📊 Mostrar datos de egresos"):
        query_top = f"""
            SELECT detalle AS concepto,
                   ROUND(SUM(COALESCE(prestamo,0)),2) AS total_egreso
            FROM caja2025
            WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
            GROUP BY detalle
            ORDER BY total_egreso DESC
            LIMIT 10;
        """
        df_top10 = ejecutar_consulta(query_top)

        if df_top10.empty:
            st.warning("No se encontraron egresos en el rango seleccionado.")
        else:
            st.dataframe(df_top10, use_container_width=True)

            fig = px.bar(
                df_top10,
                x="total_egreso",
                y="concepto",
                orientation="h",
                title="Top 10 conceptos con mayores egresos",
                text="total_egreso",
                color="total_egreso",
                color_continuous_scale="Reds"
            )
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

# ==============================================================
# SECCIÓN 3: INGRESOS POR SOCIO (CXC) — AÑO 2025
# ==============================================================

elif opcion == "💰 Ingresos por socio (CXC) — 2025":
    st.subheader("💰 Ingresos por socio (CXC) — Año 2025")
    st.write("""
    El análisis de los egresos durante 2025 muestra una concentración en determinados registros, 
    reflejando que las salidas de dinero se relacionan principalmente con pocas operaciones o beneficiarios. 
    En general, los egresos representan los compromisos financieros y pagos realizados por la asociación, 
    evidenciando una dinámica moderada y focalizada. Aunque el comportamiento global sugiere control en los desembolsos, 
    la baja dispersión de datos limita una lectura completa del flujo de pagos entre socios o proveedores, 
    lo que resalta la importancia de mantener actualizada la información para una interpretación más precisa del movimiento financiero.
    """)

    socios_query = """
        SELECT DISTINCT TRIM(nombre) AS nombre, TRIM(codigo) AS codigo
        FROM socios2024
        WHERE nombre IS NOT NULL AND nombre <> '';
    """
    df_socios = ejecutar_consulta(socios_query)

    lista_socios = ['Todos los socios'] + sorted(df_socios['nombre'].tolist()) if not df_socios.empty else ['Todos los socios']
    socio_sel = st.selectbox("Selecciona un socio:", lista_socios)

    with st.expander("📈 Mostrar resultados CXC 2025"):
        if socio_sel == "Todos los socios":
            query_all = """
                SELECT 
                    COALESCE(s.nombre, 'Socio no identificado') AS socio,
                    ROUND(SUM(CAST(c.salida AS FLOAT)), 2) AS total_ingreso
                FROM socios2024 s
                LEFT JOIN cxc2025 c 
                    ON TRIM(s.codigo) = TRIM(c.codigo_cliente)
                WHERE CAST(c.salida AS FLOAT) > 0
                GROUP BY s.nombre
                ORDER BY total_ingreso DESC;
            """
            df_all = ejecutar_consulta(query_all)

            if df_all.empty:
                st.warning("No se encontraron ingresos registrados en la base de datos.")
            else:
                st.dataframe(df_all, use_container_width=True)
                fig = px.bar(
                    df_all,
                    x="socio",
                    y="total_ingreso",
                    text="total_ingreso",
                    title="Concentración de ingresos por socio — CXC 2025",
                    color="total_ingreso",
                    color_continuous_scale="Blues"
                )
                fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
                fig.update_layout(xaxis_title="Socio", yaxis_title="Total ingreso")
                st.plotly_chart(fig, use_container_width=True)

        else:
            codigo_row = df_socios.loc[df_socios['nombre'] == socio_sel]
            if codigo_row.empty:
                st.warning("No se encontró el código del socio seleccionado.")
            else:
                codigo = codigo_row['codigo'].iloc[0]
                query_socio = f"""
                    SELECT 
                        fecha,
                        ROUND(CAST(salida AS FLOAT), 2) AS ingreso
                    FROM cxc2025
                    WHERE TRIM(codigo_cliente) = '{codigo}'
                      AND CAST(salida AS FLOAT) > 0
                    ORDER BY fecha;
                """
                df_socio = ejecutar_consulta(query_socio)

                if df_socio.empty:
                    st.warning(f"No se encontraron ingresos registrados para {socio_sel}.")
                else:
                    df_socio['fecha'] = pd.to_datetime(df_socio['fecha'])
                    st.dataframe(df_socio, use_container_width=True)
                    fig = px.line(
                        df_socio,
                        x="fecha",
                        y="ingreso",
                        markers=True,
                        title=f"Evolución de ingresos de {socio_sel} — CXC 2025",
                        color_discrete_sequence=["#2ca02c"]
                    )
                    st.plotly_chart(fig, use_container_width=True)

    st.write("En este caso, solo aparece información correspondiente a **Yamile Vera**, porque los demás socios no registran egresos en la base de datos CXP 2025 o sus datos no están correctamente asociados por nombre o código.")

# ==============================================================
# SECCIÓN 4: INGRESOS POR SOCIO (CXC) — AÑO 2024
# ==============================================================

elif opcion == "💰 Ingresos por socio (CXC) — 2024":
    st.subheader("💰 Ingresos por socio (CXC) — Año 2024")
    st.write("""
    El análisis de los ingresos por socio durante 2024 muestra una distribución más limitada en comparación con 2025. 
    En este año, algunos socios registraron actividad financiera moderada, mientras que otros no presentan movimientos en la base de datos. 
    El comportamiento evidencia posibles diferencias en la participación o registro contable entre ejercicios, 
    lo que puede deberse a cambios en la gestión, actualización de datos o la incorporación de nuevos socios.
    """)

    socios_query_2024 = """
        SELECT DISTINCT TRIM(nombre) AS nombre, TRIM(codigo) AS codigo
        FROM socios2024
        WHERE nombre IS NOT NULL AND nombre <> '';
    """
    df_socios_2024 = ejecutar_consulta(socios_query_2024)

    lista_socios_2024 = ['Todos los socios'] + sorted(df_socios_2024['nombre'].tolist()) if not df_socios_2024.empty else ['Todos los socios']
    socio_sel_2024 = st.selectbox("Selecciona un socio (2024):", lista_socios_2024)

    with st.expander("📈 Mostrar resultados CXC 2024"):
        if socio_sel_2024 == "Todos los socios":
            query_all_2024 = """
                SELECT 
                    COALESCE(s.nombre, 'Socio no identificado') AS socio,
                    ROUND(SUM(CAST(c.salida AS FLOAT)), 2) AS total_ingreso
                FROM socios2024 s
                LEFT JOIN cxc2024 c 
                    ON TRIM(s.codigo) = TRIM(c.socio)
                WHERE CAST(c.salida AS FLOAT) > 0
                GROUP BY s.nombre
                ORDER BY total_ingreso DESC;
            """
            df_all_2024 = ejecutar_consulta(query_all_2024)

            if df_all_2024.empty:
                st.warning("No se encontraron ingresos registrados en la base de datos 2024.")
            else:
                st.dataframe(df_all_2024, use_container_width=True)
                fig = px.bar(
                    df_all_2024,
                    x="socio",
                    y="total_ingreso",
                    text="total_ingreso",
                    title="Concentración de ingresos por socio — CXC 2024",
                    color="total_ingreso",
                    color_continuous_scale="Blues"
                )
                fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
                fig.update_layout(xaxis_title="Socio", yaxis_title="Total ingreso")
                st.plotly_chart(fig, use_container_width=True)

        else:
            codigo_row_2024 = df_socios_2024.loc[df_socios_2024['nombre'] == socio_sel_2024]
            if codigo_row_2024.empty:
                st.warning("No se encontró el código del socio seleccionado.")
            else:
                codigo_2024 = codigo_row_2024['codigo'].iloc[0]
                query_socio_2024 = f"""
                    SELECT 
                        fecha,
                        ROUND(CAST(salida AS FLOAT), 2) AS ingreso
                    FROM cxc2024
                    WHERE TRIM(socio) = '{codigo_2024}'
                      AND CAST(salida AS FLOAT) > 0
                    ORDER BY fecha;
                """
                df_socio_2024 = ejecutar_consulta(query_socio_2024)

                if df_socio_2024.empty:
                    st.warning(f"No se encontraron ingresos registrados para {socio_sel_2024} en 2024.")
                else:
                    df_socio_2024['fecha'] = pd.to_datetime(df_socio_2024['fecha'])
                    st.dataframe(df_socio_2024, use_container_width=True)
                    fig = px.line(
                        df_socio_2024,
                        x="fecha",
                        y="ingreso",
                        markers=True,
                        title=f"Evolución de ingresos de {socio_sel_2024} — CXC 2024",
                        color_discrete_sequence=["#2ca02c"]
                    )
                    st.plotly_chart(fig, use_container_width=True)

    st.write("""
    En este año, solo **Yamile Vera** registró ingresos por un total de **$3.500.000**, 
    lo que evidencia una concentración de los movimientos financieros en una sola socia. 
    Esto puede deberse a que los demás socios no realizaron operaciones durante 2024 o 
    a que sus datos no están correctamente asociados por nombre o código dentro del sistema contable.
    """)

# ==============================================================
# SECCIÓN 5: INGRESOS POR SOCIO (CXC) — AÑO 2023
# ==============================================================

elif opcion == "💰 Ingresos por socio (CXC) — 2023":
    st.subheader("💰 Ingresos por socio (CXC) — Año 2023")
    st.write("""
    En 2023 no se dispone de una tabla específica de cuentas por cobrar (`cxc2023`) en la base de datos, 
    por lo tanto, no es posible mostrar los ingresos por socio de ese año. 
    Es posible que la información esté en la tabla `cxp2023` (cuentas por pagar) o que no se haya registrado.
    """)

    # Comprobamos si la tabla cxc2023 existe en la base de datos
    check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='cxc2023';"
    df_check = ejecutar_consulta(check_query)

    if df_check.empty:
        st.warning("⚠️ No se encontró la tabla `cxc2023` en la base de datos. No hay registros de ingresos disponibles para 2023.")
    else:
        socios_query_2023 = """
            SELECT DISTINCT TRIM(nombre) AS nombre, TRIM(codigo) AS codigo
            FROM socios2023
            WHERE nombre IS NOT NULL AND nombre <> '';
        """
        df_socios_2023 = ejecutar_consulta(socios_query_2023)

        lista_socios_2023 = ['Todos los socios'] + sorted(df_socios_2023['nombre'].tolist()) if not df_socios_2023.empty else ['Todos los socios']
        socio_sel_2023 = st.selectbox("Selecciona un socio (2023):", lista_socios_2023)

        with st.expander("📈 Mostrar resultados CXC 2023"):
            if socio_sel_2023 == "Todos los socios":
                query_all_2023 = """
                    SELECT 
                        COALESCE(s.nombre, 'Socio no identificado') AS socio,
                        ROUND(SUM(CAST(c.salida AS FLOAT)), 2) AS total_ingreso
                    FROM socios2023 s
                    LEFT JOIN cxc2023 c 
                        ON TRIM(s.codigo) = TRIM(c.codigo_cliente)
                    WHERE CAST(c.salida AS FLOAT) > 0
                    GROUP BY s.nombre
                    ORDER BY total_ingreso DESC;
                """
                df_all_2023 = ejecutar_consulta(query_all_2023)

                if df_all_2023.empty:
                    st.warning("No se encontraron ingresos registrados en la base de datos 2023.")
                else:
                    st.dataframe(df_all_2023, use_container_width=True)
                    fig = px.bar(
                        df_all_2023,
                        x="socio",
                        y="total_ingreso",
                        text="total_ingreso",
                        title="Concentración de ingresos por socio — CXC 2023",
                        color="total_ingreso",
                        color_continuous_scale="Blues"
                    )
                    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
                    fig.update_layout(xaxis_title="Socio", yaxis_title="Total ingreso")
                    st.plotly_chart(fig, use_container_width=True)

            else:
                codigo_row_2023 = df_socios_2023.loc[df_socios_2023['nombre'] == socio_sel_2023]
                if codigo_row_2023.empty:
                    st.warning("No se encontró el código del socio seleccionado.")
                else:
                    codigo_2023 = codigo_row_2023['codigo'].iloc[0]
                    query_socio_2023 = f"""
                        SELECT 
                            fecha,
                            ROUND(CAST(salida AS FLOAT), 2) AS ingreso
                        FROM cxc2023
                        WHERE TRIM(codigo_cliente) = '{codigo_2023}'
                          AND CAST(salida AS FLOAT) > 0
                        ORDER BY fecha;
                    """
                    df_socio_2023 = ejecutar_consulta(query_socio_2023)

                    if df_socio_2023.empty:
                        st.warning(f"No se encontraron ingresos registrados para {socio_sel_2023} en 2023.")
                    else:
                        df_socio_2023['fecha'] = pd.to_datetime(df_socio_2023['fecha'])
                        st.dataframe(df_socio_2023, use_container_width=True)
                        fig = px.line(
                            df_socio_2023,
                            x="fecha",
                            y="ingreso",
                            markers=True,
                            title=f"Evolución de ingresos de {socio_sel_2023} — CXC 2023",
                            color_discrete_sequence=["#2ca02c"]
                        )
                        st.plotly_chart(fig, use_container_width=True)

    st.write("""
    En este año no se registran datos de ingresos por socio, 
    posiblemente porque el sistema contable aún no tenía implementada la categoría de cuentas por cobrar (CXC).
    """)

# ==============================================================
# PIE DE PÁGINA
# ==============================================================

st.caption("Profe pongame 5.0 😄")
