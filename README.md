# Datos, gráficos y programas de *La crisis inmobiliaria española*

**Repositorio de la obra** *La Crisis Inmobiliaria Española: Un Estudio Interdisciplinario desde el Análisis Económico del Derecho* (dir. Manuel Castilla Cubillas; coord. Daniel Raya Quero), Aranzadi, en prensa.

**Versión de trabajo.** La versión citable y permanente es la 1.0 de Zenodo, correspondiente a la edición impresa: DOI [10.5281/zenodo.24287542](https://doi.org/10.5281/zenodo.24287542). Este repositorio contiene los mismos ficheros, sin comprimir, más la transcripción de la entrevista que cita el capítulo de D. Raya Quero (`anexos/`).

Los gráficos interactivos y las figuras pueden consultarse en la página del repositorio: https://derechomercantil.github.io/Crisis-Inmobiliaria-ESP/

Contiene los gráficos y las figuras que se imprimen en la obra, los gráficos complementarios que la obra cita sin imprimirlos, las tablas de datos a las que remite el texto y los programas que las elaboran y dibujan. Las cifras de la obra proceden de estas tablas.

## Contenido

| Carpeta | Contenido |
| --- | --- |
| `graficos_impresos/` | Los seis gráficos impresos (gráficos 1 a 6) y, en `figuras/`, las dos figuras (figuras 1 y 2) |
| `graficos_complementarios/` | Los doce gráficos complementarios (1 a 12) |
| `tablas/` y `datos_fuente/` | Tablas de datos (`tablas/`), su documentación (`tablas/FUENTES.md`) y los datos de origen de pequeño tamaño que emplean los programas (`datos_fuente/`) |
| `programas/` | Programas en Python: elaboración de las tablas (`programas/elaboracion_tablas/`) y generación de los gráficos (`programas/graficos/`) |
| `anexos/` | Transcripción editada de la entrevista de 23 de septiembre de 2026 que cita el capítulo de D. Raya Quero |

Cada gráfico, impreso o complementario, se ofrece en cinco formatos:

- `bn/`: TIFF a 600 ppp en escala de grises y PDF vectorial (edición impresa).
- `color/`: TIFF a 600 ppp, PDF vectorial y PNG (edición electrónica).
- `editables/`: libro Excel con los datos y el gráfico editable, en color y en blanco y negro.
- `interactivas/`: página HTML con el gráfico interactivo y su tabla de datos; requiere el fichero `plotly.min.js` de la misma carpeta.
- `datos/`: CSV con la serie exacta representada.

Las imágenes de los gráficos impresos no llevan título, porque figura en el pie del libro; las de los complementarios lo incorporan.

## Gráficos impresos

| N.º | Título | Lugar de la obra | Tabla de origen |
| --- | --- | --- | --- |
| 1 | Precio de la vivienda tipo en años de renta disponible del perceptor mediano de 18 a 35 años y del hogar mediano (España, 1980-2024) | Introducción general | G01c |
| 2 | Precio de la vivienda tipo en años de renta disponible del perceptor mediano, por grupo de edad (España, 1980-2024) | Introducción general | G01d |
| 3 | Crédito con garantía inmobiliaria a la construcción y las actividades inmobiliarias y crédito a los hogares para vivienda, en porcentaje del PIB (España, 1999-2025) | D. Raya Quero, epígrafe IV.3 | `datos_fuente/bde_si_1_5.csv` (series SI_1_5.54 y SI_1_5.56) |
| 4 | Régimen de tenencia de los jóvenes de 18 a 34 años que se emancipan y tasa anual de emancipación (España, 2005-2025) | D. Raya Quero, epígrafe VI.2 | G19 |
| 5 | Precios reales de la vivienda en España, Hungría, Italia, el Reino Unido y la zona del euro (índice 2015 = 100, 1971-2025) | V. Blazsek, epígrafe IV | G04 |
| 6 | Viviendas terminadas y variación anual del número de hogares (España, 1971-2025) | C. J. Rusillo Ramiro, epígrafe VI | G11 |

## Figuras

Diagramas conceptuales del capítulo de M. Castilla Cubillas, elaborados con Microsoft Visio. Se numeran aparte de los gráficos porque no representan series de datos. Cada una se ofrece en `figuras/color/` (PDF vectorial exportado desde Visio y PNG a 300 ppp), `figuras/bn/` (el mismo PDF en escala de grises, para la edición impresa) y `figuras/editables/` (fichero original `.vsdx`). A diferencia de los gráficos, llevan el título en la imagen. En la figura 2 se han corregido tres erratas de texto del original, sin modificar el dibujo: «patrimonio», las unidades («mm€», miles de millones de euros, como en el texto) y «Generaciones X, Y, Z». La página del `.vsdx` de la figura 1 está configurada en A3; el dibujo es el mismo que el del PDF, exportado en A4.

| N.º | Título | Lugar de la obra | Datos |
| --- | --- | --- | --- |
| 1 | Sistema del derecho a la vivienda (SDV) en España: áreas jurídicas por niveles normativos y subsistemas | M. Castilla Cubillas, epígrafe III.4 | — |
| 2 | Grafo del rescate bancario y de su interferencia con la asequibilidad de la vivienda (millardos de euros) | M. Castilla Cubillas, epígrafe IV.3 | Las cifras del texto, epígrafe IV.3, y sus notas |

## Gráficos complementarios

Se numeran por el orden en que la obra los cita por primera vez.

| N.º | Título | Citado en | Tabla de origen |
| --- | --- | --- | --- |
| 1 | Precio de la vivienda en años de renta bruta disponible del hogar mediano (España, 1971-2026) | Introducción general | G01bis |
| 2 | Precio real de la vivienda, deflactado por el índice de precios de consumo (España, 1971 = 100, 1971-2025) | Introducción general | G03 |
| 3 | Ratio entre el precio de la vivienda y la renta disponible respecto de su media de largo plazo en España, Italia, el Reino Unido y la zona del euro (media = 100, 1970-2025) | Introducción general | G02b |
| 4 | Participación en la riqueza neta de los hogares por edad del cabeza de familia (Estados Unidos, 1989-2025) | Introducción general | G07 |
| 5 | Asalariados y hogares cuya renta no alcanza el umbral necesario para pagar la hipoteca de la vivienda tipo sin destinarle más del 30 % de sus ingresos (España, 2004-2024) | Introducción general | G18 |
| 6 | Patrimonio neto mediano de los hogares en porcentaje del precio de la vivienda tipo, por edad del cabeza de familia (España, 2002-2024) | Introducción general; M. Janssens, ayudas de Estado | G01g |
| 7 | Riqueza neta mediana de los hogares por edad del cabeza de familia (España, 2002-2024) | Introducción general | G06 |
| 8 | Alquileres pagados y percibidos por los hogares, por edad de la persona responsable de la vivienda (España, 2025) | Introducción general | G05 |
| 9 | Cuota hipotecaria del primer año en porcentaje de la renta disponible del perceptor mediano, por grupo de edad (España, 1987-2024) | Introducción general | G01f |
| 10 | Viviendas iniciadas, libres y protegidas (España, 1970-2025) | C. J. Rusillo Ramiro; D. Raya Quero | G08a |
| 11 | Precio del metro cuadrado de vivienda y renta bruta disponible del hogar mediano (España, 1987 = 100, 1987-2025) | C. J. Rusillo Ramiro | G01b |
| 12 | Precio máximo legal de una vivienda protegida de 90 m² útiles en años de renta del hogar mediano (España, 1979-2025) | C. J. Rusillo Ramiro | G10 |

## Tablas

Cada tabla se identifica por el código con el que la cita la obra («tabla G13»), que encabeza el nombre de su fichero (`tablas/G13_…csv`). La obra cita expresamente las tablas G01c, G01e, G01f, G01g, G08a, G11, G12, G12b, G13, G13b, G14b, G15, G17, G19 y G20; las demás son las de origen de los gráficos.

`tablas/FUENTES.md` documenta la fuente, el método y las advertencias de cada tabla. Su apartado «Detalle de los datos del capítulo sobre crédito sin tabla propia» recoge el detalle al que remiten las notas del capítulo de D. Raya Quero que no citan una tabla concreta. Es el cuaderno de fuentes del trabajo, por lo que describe también algunas series que no forman parte de la obra, y emplea las rutas de la estructura de trabajo: `graficas/scripts/` corresponde aquí a `programas/elaboracion_tablas/`, y `datos/brutos/` y `datos/procesados/`, a `datos_fuente/`.

**Tabla G11.** La columna `hogares_nuevos` procede, para 2003-2025, de la Encuesta de Población Activa, cuyo cambio de cuestionario en 2021 produce una ruptura de la serie. La columna `hogares_nuevos_ecp` ofrece para 2021-2025 la variación anual del número de hogares según la Estadística Continua de Población del INE, que es la que emplean el gráfico 6 y el texto de la obra.

## Reproducción

Los gráficos se reproducen íntegramente con los ficheros de este depósito (Python 3 con matplotlib, Pillow, openpyxl y plotly):

```
python3 programas/graficos/generar_graficos_definitivos.py
python3 programas/graficos/generar_graficos_complementarios.py
```

Los programas de `programas/elaboracion_tablas/` documentan cómo se han elaborado las tablas a partir de los microdatos y series oficiales. Los microdatos (Encuesta de Condiciones de Vida, Encuesta de Presupuestos Familiares, Encuesta Básica de Presupuestos Familiares y Panel de Hogares de la Unión Europea, del INE) no se incluyen por su volumen y porque pueden descargarse de las direcciones que indica `tablas/FUENTES.md`. Para ejecutar esos programas se ha de reproducir la estructura de trabajo que esperan: `tablas/`, `datos/brutos/` y `datos/procesados/` en la carpeta superior a la de los programas.

## Lo que no incluye este repositorio

- Los microdatos en bruto, por las razones indicadas.
- El texto de la obra y el anexo que comenta los gráficos.
- Programas para las figuras 1 y 2, que se dibujan a mano en Visio; su fichero `.vsdx` permite editarlas.

## Licencias

- Datos, tablas, gráficos y documentación de elaboración propia: Creative Commons Atribución 4.0 Internacional (`LICENCIA-DATOS.txt`).
- Programas: licencia MIT (`LICENCIA-CODIGO.txt`).
- Los ficheros de terceros de `datos_fuente/` (Banco de España, INE, Banco Central Europeo, Banco de Pagos Internacionales, OCDE) siguen sujetos a las condiciones de sus proveedores. `plotly.min.js` es una biblioteca de Plotly Technologies con su propia licencia MIT.

## Cómo citar

Raya-Quero, Daniel y Castilla Cubillas, Manuel, *Datos, gráficos y programas de «La Crisis Inmobiliaria Española: Un Estudio Interdisciplinario desde el Análisis Económico del Derecho»*, versión 1.0, Zenodo, 2026, https://doi.org/10.5281/zenodo.24287542.

## Versión citable

Zenodo, versión 1.0: https://doi.org/10.5281/zenodo.24287542. La entrevista de `anexos/` solo se publica en este repositorio.
