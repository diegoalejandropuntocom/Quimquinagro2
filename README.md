# Quimquinagro2
Diseño de un tablero interactivo en Streamlit que permite a la asociación consultar y visualizar su información financiera de manera sencilla.
*Manual de usuario*


Nota: En el archivo "Retos 2" se encuentran los pantallazos del uso de la palicación.
````markdown
# 💰Diego Alejandro Ramirez

Este proyecto es un **tablero financiero interactivo** desarrollado en **Python con Streamlit**, diseñado para visualizar y analizar la información contable de la Asociación **QuimQuinAgro** correspondiente al año 2025.  

Permite consultar datos sobre **caja mensual**, **egresos más altos** e **ingresos por socio (CXC)** de forma dinámica y visual, facilitando la interpretación de los resultados financieros y apoyando la toma de decisiones de la asociación.

---

## 🧭 1. Requisitos del sistema

Antes de usar la aplicación, asegúrate de tener instalado:

- **Python 3.9 o superior**
- **pip** (gestor de paquetes de Python)
- Las siguientes librerías:

```bash
pip install streamlit pandas plotly
````

También debes contar con el archivo de base de datos `contabilidad.db` en la misma carpeta del proyecto.

---

## ⚙️ 2. Instrucciones de instalación y ejecución

1. **Descarga o clona** este proyecto en tu equipo.

2. Verifica que el archivo **`contabilidad.db`** se encuentre en la misma carpeta que **`app.py`**.

3. Abre una terminal (o el Anaconda Prompt) y navega hasta la carpeta del proyecto.
   Ejemplo:

   ```bash
   cd ruta/del/proyecto
   ```

4. Ejecuta la aplicación con el siguiente comando:

   ```bash
   streamlit run app.py
   ```

5. Se abrirá automáticamente en tu navegador la interfaz del **Dashboard Financiero Interactivo**.

---

## 🧩 3. Estructura del proyecto

```
📂 QuimQuinAgro_Dashboard/
├── app.py                 → Código principal del tablero
├── contabilidad.db        → Base de datos con los registros contables
└── README.md              → Manual de usuario e instrucciones
```

---

## 📊 4. Descripción de las secciones del dashboard

El tablero está dividido en tres secciones principales, accesibles desde el menú lateral (sidebar):

### 1️⃣ Caja mensual (básico)

Muestra los **totales de ingresos y egresos mensuales** durante 2025.
Incluye una tabla interactiva y un gráfico de barras agrupadas.

> 💬 *Conclusión:* Los ingresos alcanzan su punto más alto a inicios del año, pero disminuyen hacia el segundo semestre, evidenciando la necesidad de estrategias para mantener la estabilidad financiera.

---

### 2️⃣ Top 10 egresos

Permite identificar los **conceptos en los que más se gasta** dentro del año 2025.
Incluye un selector de rango de fechas y visualiza los 10 principales egresos mediante un gráfico de barras horizontales.

> 💬 *Conclusión:* Los egresos se concentran en pocos conceptos, lo que refleja una gestión focalizada pero que puede implicar riesgos si ciertos gastos se vuelven recurrentes.

---

### 3️⃣ Ingresos por socio (CXC)

Visualiza los **ingresos totales asociados a cada socio**, o la evolución temporal de uno específico.
Incluye una lista desplegable con todos los socios registrados en la base de datos.

> 💬 *Conclusión general:* La concentración de ingresos en pocos socios refleja dependencia financiera, resaltando la importancia de diversificar las fuentes de ingreso.
> 📌 *Nota:* En la base actual, solo aparece información para **Yamile Vera**, ya que los demás socios no presentan registros en la tabla `cxc2025` o no están correctamente asociados por código o nombre.

---

## 💡 5. Consejos de uso

* Asegúrate de que el archivo `contabilidad.db` esté actualizado y contenga datos del año 2025.
* Si la aplicación no muestra información, verifica la correspondencia entre los **códigos de socios** y los registros en `cxc2025`.
* Usa el **expander (“📊 Mostrar datos...”)** en cada sección para visualizar las tablas detalladas.

---

## 🧰 6. Problemas comunes y soluciones

| Problema              | Posible causa                                               | Solución                                                                 |
| --------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------ |
| No se muestran datos  | La base de datos está vacía o no se encuentra en la carpeta | Verifica que `contabilidad.db` esté junto a `app.py`                     |
| Solo aparece un socio | Los códigos de los demás no coinciden entre tablas          | Revisa la tabla `socios2024` y `cxc2025` para corregir nombres o códigos |
| Error de conexión     | SQLite no puede abrir la base                               | Cierra otros programas que usen la base o revisa permisos                |
| Streamlit no abre     | Falta de instalación                                        | Ejecuta `pip install streamlit`                                          |

---

## 👨🏻‍💻 7. Autor

**Diego Alejandro Ramírez Benítez**  
Estudiante — *Introducción al Business Intelligence 2025-II*  
Proyecto desarrollado con el apoyo de **GPT-5**  

**Docente:** Lina María Sepúlveda Cano

---

📅 **Asociación QuimQuinAgro — Tablero financiero interactivo 2025-II**

```
