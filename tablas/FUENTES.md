# Fuentes de las tablas de datos

Fecha de descarga de todos los datos: 16 de julio de 2026.
Los ficheros brutos originales están en `datos/brutos/`; las series limpias en `datos/procesados/`.

## G1_espana_ratio_precio_rbd_anual.csv (Gráfica 1, versión ratio)

- **Serie**: Precio de la vivienda / Renta bruta disponible por hogar (años de renta).
- **Fuente**: Banco de España, *Síntesis de Indicadores*, cuadro 1.5 «Mercado de la vivienda», serie SI_1_5.43 (código DHIVTNOAPLPMMUVT_RLI derivado). Trimestral, 1987 T1 – 2026 T1; aquí anualizada (media de trimestres).
- **Definición BdE**: «Precio medio de una vivienda libre de 93,75 m² construidos dividido por la renta bruta estimada del hogar mediano».
- **URL**: https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/si_1_5.csv
- Complemento disponible: serie SI_1_5.44 «esfuerzo teórico anual» (% de renta destinado a cuotas el primer año), misma fuente y periodo (`datos/procesados/bde_esfuerzo_teorico.csv`).

### G01 — Revisiones de la serie del BdE y diferencia con Funcas (2019)

- **Origen del gráfico de Funcas** (`FUNCAS/image.png`): Gráfico 5 de C. Ocaña P. de Tudela y R. Torres, «El mercado de la vivienda: situación y perspectivas a corto plazo», *Cuadernos de Información Económica*, n.º 273, noviembre-diciembre de 2019, p. 5 (PDF en `FUNCAS/funcas_CIE_273art02.pdf`). `FUNCAS/image 2.png` contiene los mismos datos (2000-2019, mismos rótulos y medias) redibujados sin identificación de autor ni fuente.
- **Por qué difiere de nuestra G01**: Funcas usó la edición del cuadro 1.5 del BdE vigente en 2019. La versión de julio de 2019 (recuperada del Internet Archive, `datos/brutos/bde_si_1_5_vintages/`) reproduce sus valores con medias anuales: 2000 = 4,02 (Funcas 4,0; esfuerzo 27,3); 2007 = 8,94 (8,9); 2008, esfuerzo 51,1 (51,2); I-2019 = 7,52 (7,5; esfuerzo 33,5 frente a 33,4). Desde entonces el BdE ha revisado la serie: hoy 2007 = 9,36 y 2019 = 6,86.
- **Qué se revisó**: el numerador no cambia (precio del m² tasado idéntico en ambas versiones); cambia el **denominador**, la renta bruta estimada del hogar mediano. Comparación en `datos/procesados/bde_ratio_precio_renta_versiones_2019_vs_actual.csv`: la renta implícita se revisa entre −1,6 % y −7,0 % en 1995-2015 y entre +0,5 % y +6,3 % en 2016-2018. La versión de 2019 hacía caer esa renta de 22.042 € (2013) a 20.290 € (2018), por debajo de la de 2000; la actual la hace crecer hasta 21.574 €.
- **Por qué revisa el BdE**: según el artículo metodológico (Boletín Económico, mayo de 2005, «Indicadores de accesibilidad y esfuerzo en el mercado de la vivienda»; copia en `datos/brutos/bde_si_1_5_vintages/`), la renta del hogar mediano no se observa cada año: se ancla en la mediana de la Encuesta Financiera de las Familias (22.000 € brutos en 2001) y se extrapola con el perfil de la renta bruta disponible del sector hogares de la Contabilidad Nacional, por hogar. Las revisiones de la Contabilidad Nacional y del número de hogares (EPA y censos) se trasladan a toda la serie, y los últimos años de cada edición son provisionales: la edición de abril de 2022 daba 8,1 años para 2021 y la actual da 7,15. Qué revisión concreta explica cada tramo no puede determinarse con la información publicada.
- **Consecuencias para la monografía**: (1) citar siempre la edición del BdE utilizada (la nuestra: descarga de 16-7-2026) y tratar los dos o tres últimos años como provisionales; (2) las series por edad (G01c, G01d, G01e) no dependen de esta estimación, porque usan rentas de encuesta, y G01f solo toma del BdE el factor de financiación (cociente esfuerzo/ratio), que apenas cambia entre ediciones (2018: 4,39 frente a 4,44); (3) la serie del BdE empieza en 1987 en todas sus ediciones; antes de esa fecha solo existe nuestra retropolación académica de G01bis (1971-1986), y el esfuerzo no puede extenderse antes de 1987.

## G1bis_espana_ratio_precio_rbd_anual_1971.csv (Gráfica 1bis, serie extendida 1971-2025)

- **Serie**: la misma ratio de G01 (precio de la vivienda en años de renta bruta del hogar mediano), con el tramo 1971-1986 retropolado. La columna `metodo` identifica el origen de cada año.
- **Tramo 1987-2026**: serie oficial BdE, idéntica a G01.
- **Tramo 1971-1986 (retropolación, script `graficas/scripts/g1bis_retropolacion_1971.py`)**:
  - *Numerador*: precio del m² de 1987 (327 €/m², Fomento, tabla G01b) retropolado con el índice nominal del BIS, *Selected residential property prices* (WS_SPP, serie de España, media anual de trimestres), × 93,75 m².
  - *Denominador*: renta bruta del hogar mediano de 1987 (9.913 €, implícita en la serie BdE, tabla G01b) retropolada con la NNDI nominal por hogar — mismo método aprobado para el denominador 1979-1986 de G10 (Prados de la Escosura, Tabla 2; hogares = viviendas principales censales INE 1970/1981/1991, interpolación log-lineal). La reproducción de la renta 1979-1986 coincide exactamente con la de G10.
- **Columna `ratio_contraste_ocde`** (solo 1971-1986): la misma ratio retropolada con el índice *price-to-income* de la OCDE (HPI_YDH, España) encadenado en 1987. Diferencia máxima con la serie principal: 0,25 años (1981). Se descartó como método principal porque la OCDE usa renta disponible **por persona**, no por hogar: en el solapamiento 1987-2025 esa diferencia de concepto acumula desviaciones grandes (2007: 6,1 frente al 9,4 oficial), al crecer el número de hogares más deprisa que la población.
- **Advertencia para la nota al pie**: el tramo retropolado combina un índice de precios de cobertura limitada en los setenta con una renta media por hogar (no mediana); es una aproximación académica, no estadística oficial, y así se distingue (trazo discontinuo) en la gráfica G01bis.

## Numerador de las series por edad G01c-G01g: precio de compraventa desde 2008 (decisión de 15-10-2026)

- **Cambio**: el precio de la vivienda tipo (93,75 m²) es el valor de tasación (Fomento/MIVAU; BIS antes de 1987) hasta 2007 y, desde 2008, el nivel de 2007 evoluciona con el **Índice de Precios de Vivienda del INE** (general nacional, media anual; tabla 80271, `datos/brutos/ine_ipv_80271_medias_anuales.json`). Implementado en `precio_vivienda_tipo()` de `g01c_renta_joven.py`; la tabla G01c conserva la versión con tasación en columnas aparte.
- **Motivo (criterio metodológico, no de resultado)**: el valor de tasación mide la valoración para garantía hipotecaria, no el precio pagado; el IPV se basa en compraventas ante notario y mantiene constante la calidad de la vivienda, de modo que no le afectan los cambios de composición de lo tasado. Ambas series se separan desde 2015: IPV +60 % (2015-2024) y +81 % (2015-2025) frente a +30 % y +44 % de la tasación; en 2025 el IPV supera en un 21 % su nivel de 2007 y la tasación en un 3 %. Se enlaza en 2007 porque es el primer año del IPV.
- **Efecto**: nada cambia hasta 2007. En 2024 el joven necesita 15,2 años de renta (13,2 con tasación) y el perceptor adulto mediano 11,8 (10,3). Las posiciones relativas entre edades no cambian, porque el precio es común.
- **Sin IPV antes de 2007**: no hay índice nacional de compraventas anterior; antes de 2007 se mantiene la tasación.
- **Límite temporal**: las rentas por edad llegan a 2024 (ECV 2025). La ECV 2026, con rentas de 2025, no estaba publicada a 15-10-2026; 2025, con una subida del IPV del 12,7 %, deberá añadirse cuando se publique.
- **Prueba descartada 1, ponderación geográfica por cohorte**: precio de tasación por comunidad autónoma (1995-2025) ponderado por la población de cada cohorte (INE, Estadística Continua de Población, tabla 56940, `datos/brutos/ine_ecp_56940_poblacion_ccaa_edad.csv`). Los jóvenes afrontan un precio un 0 % (1995) a 1,9 % (2024) superior al del conjunto de adultos; 55-64 y 65-74, entre un 1,3 % y un 1,8 % inferior en 2024. El efecto es pequeño (unos 2,5 puntos de ensanchamiento de la brecha) y solo calculable desde 1995, por lo que no se adopta; queda como prueba de robustez que refuerza, sin alterar, la conclusión.
- **Prueba descartada 2, EPF 1973-74**: según su documentación (Alonso-Colmenares, Lara y Ruiz-Castillo, Documento de Trabajo UC3M 91-10, 1991, `datos/brutos/epf7374/`), los ficheros solo contienen ingresos agregados del hogar, «sin información sobre la contribución por parte de cada perceptor individual», y no recogen la edad de los miembros. No permite calcular la renta del tramo 18-35; las series por edad empiezan en 1980.

## G1c_espana_ratio_precio_renta_joven_1980_2024.csv (Gráfica 1c, la vivienda en años de renta de un joven)

- **Serie**: precio de la vivienda tipo de G01/G01bis (vivienda libre de 93,75 m² construidos, en euros) dividido por (a) la renta disponible anual **mediana del perceptor de 18 a 35 años** y (b) la renta disponible mediana del hogar, calculadas con las mismas encuestas y el mismo concepto. 1980-2024. Script reproducible: `graficas/scripts/g01c_renta_joven.py`.
- **Concepto de renta**: renta *disponible* (neta de IRPF y cotizaciones), que es el único concepto medido en todas las encuestas y corresponde a la «renta disponible» de la contabilidad nacional. Joven: trabajo por cuenta ajena y propia más prestaciones sociales, sin rentas del capital (despreciables a esa edad). Hogar: ingresos monetarios ordinarios netos totales. Solo perceptores (jóvenes con ingresos > 0); su proporción se recoge en la tabla (53 % en 1980, 83 % en 2024). Edad al final del periodo de referencia de la renta.
- **Fuentes (microdatos del INE, descarga libre, en `datos/brutos/`)**:
  - EPF 1980-81 (`ebpf/datos_ebpf8081.zip`): ingresos netos de los 12 últimos meses por perceptor (hasta 4 por hogar), enlazados con la edad del miembro; peso FACELE1 × MULT1 × MULT2 (nota del INE de 16-9-2015). 10.777 jóvenes perceptores en la muestra.
  - EBPF 1990-91 (`ebpf/datos_ebpf9091.zip`): registro de miembros (tipo 3), ingresos por fuente. 11.490 jóvenes perceptores.
  - PHOGUE 1994-2001 (`phogue/`): fichero de adultos, PI110 + PI130 (trabajo + prestaciones, netos); hogar HI100; renta del año anterior.
  - ECV 2005-2025 (`ecv_hist/`, `ecv_2025/`): PY010N, PY050N, PY080N, PY090N-PY140N; hogar HY020; pesos PB040 y DB090; renta del año anterior.
- **Enlace metodológico 2008**: desde 2008 la ECV (base 2013) toma la renta de registros fiscales; las encuestas anteriores son de renta declarada. El INE publica 2008-2012 en ambas bases: en ese solape la mediana del joven apenas cambia (factor 0,968) y la del hogar sube un 14,6 % (factor 1,146). Ambos factores se aplican a todas las medianas declaradas (EPF, PHOGUE, ECV 2005-2007). Detalle en `datos/procesados/g1c_enlace_ecv_bases.json`.
- **Exclusión**: ECV 2004 (renta 2003) — la primera ola tiene 807 hogares con renta cero (≈ 120 en las siguientes) y una renta media del hogar un 17 % inferior a la de 2005.
- **Interpolación**: los años sin encuesta (1981-1989, 1991-1992, 2001-2003) se interpolan log-linealmente en la renta, no en la ratio; el precio es siempre el dato anual observado. En la gráfica se distinguen con trazo punteado; los años medidos llevan marcador.
- **Contraste de robustez (método alternativo)**: aplicar la renta relativa del joven al denominador del Banco de España (G01bis / (renta joven / renta hogar)) da el mismo perfil de largo plazo (4,7 años en 1980; 20,2 en 2007), pero se descartó como principal porque mezcla la renta bruta estimada del BdE con medidas de encuesta y depende mucho del enlace de 2008 (factor 0,845). Con él, 2024 quedaba en 17,6 años en lugar de 13,2 (ambos con tasación).
- **Advertencias para la nota al pie**: (1) la serie arranca en 1980, primera encuesta con ingresos individuales por persona (la EPF 1973-74 no los tiene; véase arriba); (2) la infradeclaración de ingresos en las encuestas antiguas, si existiera, haría que el dato de 1980 *sobrestime* los años necesarios, de modo que el aumento real sería todavía mayor; (3) la unidad es la persona joven perceptora, no la pareja: en 1980 predominaba el hogar de un solo perceptor y hoy el de dos, cuestión que debe tratarse en el texto.
- **Lectura clave** (precio de compraventa desde 2008): 5,5 años en 1980 → 10,7 en 1990 → 17,4 en 2007 → 13,3 en 2013 → 17,0 en 2018 → 15,2 en 2024 (con tasación: 16,6 en 2018 y 13,2 en 2024). El joven necesitaba 1,7 veces los años del hogar mediano en 1980 y 2,5 veces en 2024. La moderación desde 2018 coincide con las subidas del SMI (la renta mediana del joven perceptor pasa de 8.969 € a 13.535 €), pero con el precio de compraventa es mucho menor que con la tasación.

## G1d_espana_ratio_precio_renta_por_edad_1980_2024.csv (Gráfica 1d, espejo generacional de la 1c)

- **Serie**: precio de la vivienda tipo (93,75 m²) en años de renta disponible del perceptor mediano de 55-64 y de 65-74 años, junto a la serie de 18-35 años de G01c. 1980-2024. Script: `graficas/scripts/g01d_renta_mayores.py` (reutiliza los lectores de `g01c_renta_joven.py`, parametrizados por edad; G01c se reproduce idéntica).
- **Método**: idéntico a G01c, con la persona perceptora como unidad (decisión de equipo de 5-10-2026, frente a la alternativa de usar el hogar). Renta personal = trabajo + prestaciones sociales, pensiones incluidas, neta. Factor de enlace base 2004 / base 2013 propio de cada cohorte: 1,056 (55-64) y 1,046 (65-74), frente a 0,968 de los jóvenes (en `datos/procesados/g1d_enlace_ecv_bases.json`): el paso a registros fiscales capta algo más renta de los mayores, sobre todo pensiones.
- **Tramos**: 55-64 y 65-74, los de la EFF (Gráfica 6). Se descartó 55-70 porque mezcla dos poblaciones cuyo peso relativo cambia mucho. Diagnóstico (proporción de perceptores cuyo ingreso principal es una pensión):

| Encuesta | 55-64 | 65-74 |
|---|---|---|
| EPF 1980-81 | 35 % | 90 % |
| EBPF 1990-91 | 40 % | 95 % |
| PHOGUE 2001 | 24 % | 93 % |
| ECV 2008 | 20 % | 93 % |
| ECV 2025 | 8 % | 86 % |

  65-74 es una cohorte homogénea de pensionistas en todo el periodo. En 55-64 predominan siempre los trabajadores, pero la caída de pensionistas (prejubilaciones de la reconversión en los ochenta y noventa) es un efecto de composición que debe mencionarse.
- **Advertencias para la nota al pie**: (1) más del 80 % de estas cohortes vive en vivienda en propiedad (ECV 2025: 82,3 % en 55-64; 87,1 % en 65-74), de modo que para ellas la cifra no mide esfuerzo de compra sino el valor de la vivienda en relación con su renta; la gráfica es un término de comparación con los jóvenes. (2) La renta personal excluye las rentas del capital e inmobiliarias, como en G01c; en las encuestas antiguas suponen entre el 2 % y el 7 % de la renta de los mayores perceptores, y la ECV no las asigna a personas, por lo que su renta está algo infravalorada en todo el periodo. (3) La proporción de perceptores sube de 63 % a 88 % (55-64) y de 73 % a 86 % (65-74), sobre todo por la incorporación de mujeres con pensión o salario propios.
- **Lectura clave**: en 1980 el perceptor mediano joven tenía más renta que el de 55-64 (1,11 veces) y que el de 65-74 (1,68 veces); en 2024 tiene 0,69 veces la de ambos (13.535 € frente a 19.601 € y 19.642 €). En años de renta: 5,5 / 6,1 / 9,2 en 1980; 15,2 / 10,5 / 10,5 en 2024. La cohorte de 65-74 alcanza 20,9 años en 2007 y cae a 10,5 por la mejora de las pensiones; la de los jóvenes no ha bajado de 13,3 desde 2006.

## G1e_espana_ratio_precio_renta_todas_edades_1980_2024.csv (tabla de referencia para G01c y G01d)

- **Serie**: precio de la vivienda tipo (93,75 m²) en años de renta disponible del conjunto de perceptores de 18 años o más, con la **mediana** (estadístico de G01c/G01d, directamente comparable) y la **media**; junto a las cohortes de 18-35, 55-64 y 65-74 años y su **renta relativa** (mediana de la cohorte / mediana de 18 y más). 1980-2024. Script: `graficas/scripts/g01e_renta_todas_edades.py` (mismos lectores; G01c y G01d se reproducen idénticas tras la reestructuración).
- **Método**: idéntico a G01c/G01d (persona perceptora, renta neta de trabajo y prestaciones, mismas encuestas, interpolación log-lineal). La mediana y la media se enlazan cada una con su propio factor base 2004 / base 2013: 1,024 y 1,065 (`datos/procesados/g1e_enlace_ecv_bases.json`). Que el factor de la media sea mayor es coherente con que los registros fiscales captan mejor las rentas altas.
- **Interpretación**: «todas las edades» es la población perceptora adulta completa (incluye 36-54 y mayores de 74), no el promedio aritmético de las tres cohortes, que excluiría esas edades y no ponderaría por población. La media supera a la mediana en un 26 % en 1980 y un 16 % en 2024; por eso, en años de renta, la media da siempre cifras menores.
- **Advertencia**: en la EPF 1980-81 solo constan hasta cuatro perceptores por hogar; en los hogares con más perceptores (minoritarios) falta alguno, lo que afecta más a esta serie que a las de cohorte.
- **Lectura clave**: con la mediana, 5,9 años en 1980, 10,4 en 1990, 16,3 en 2007 y 11,8 en 2024 (con la media: 4,7; 8,3; 13,6; 10,1). Renta relativa: el joven pasa de 1,08 veces la mediana de los adultos (1980) a 0,77 (2024), con un mínimo de 0,68 en 2016 y 2018; la cohorte de 55-64, de 0,97 a 1,12; la de 65-74, de 0,64 a 1,12. En 2024 el joven necesita 15,2 años frente a 11,8 del perceptor adulto mediano; en 1980 necesitaba menos que él (5,5 frente a 5,9).

## G1f_espana_esfuerzo_teorico_por_edad_1987_2024.csv (Gráfica 1f, esfuerzo por edad; equivalente al gráfico de Funcas)

- **Referencia**: gráfico de Funcas en `FUNCAS/image.png` («Indicadores de esfuerzo para la compra de vivienda»), construido con el cuadro 1.5 de la *Síntesis de Indicadores* del **Banco de España** (no del Ministerio de Hacienda): ratio precio/renta (SI_1_5.43) y esfuerzo teórico anual sin deducciones (SI_1_5.44). Control: la media 2000-2024 del esfuerzo del hogar mediano según el BdE es 35,5 %, la misma que señala Funcas (35 %, 2000-2019).
- **Definición BdE del esfuerzo**: importe bruto de las cuotas del primer año de una vivienda tipo financiada con un préstamo estándar por el 80 % de su valor, en % de la renta anual del hogar mediano.
- **Método por edad** (script `graficas/scripts/g01f_esfuerzo_por_edad.py`): como SI_1_5.43 y SI_1_5.44 comparten vivienda y renta, su cociente F = esfuerzo / ratio = 80 × cuota anual por euro prestado contiene solo los supuestos de financiación del BdE de cada año. Esfuerzo de la cohorte = F × años de renta de la cohorte (tabla G01e). Es la misma cuota que el BdE, dividida por la renta disponible del perceptor mediano de cada edad. Los supuestos implícitos son verosímiles: plazo de unos 10 años en 1989-1990 (tipo del 15-16,5 %), 14 en 1995, 18 en 1999, 22-26 desde 2004 (los registradores dan 22,8 años en 2015; el cálculo, 22,4).
- **Dificultades metodológicas (para el texto y la nota al pie)**:
  1. *Cobertura*: el BdE publica el esfuerzo desde 1987 y no hay serie oficial de tipos hipotecarios anterior a 1989 (los índices oficiales empiezan en 1989-1990). Extenderlo a 1980-1986 exigiría suponer tipo y plazo; no se hace.
  2. *El tipo de interés cambia el relato temporal, no el generacional*: con tipos del 15-17 % y plazos de unos 10 años, el esfuerzo del joven fue máximo a comienzos de los noventa (176,3 % de su renta en 1990, último año con encuesta antes del PHOGUE; 185,5 % en 1991 con renta interpolada), no en 2007 (98,6 %); en 2024 es 74,5 % (64,9 % con tasación). Pero como el factor de financiación es común a todas las edades, la posición relativa es idéntica en ambos indicadores: el joven pasa de 1,00 veces el esfuerzo del adulto mediano (1987) a 1,29 (2024).
  3. *Sesgo de la cuota del primer año con inflación alta*: en 1987-1995 la inflación y el crecimiento nominal de las rentas eran altos, de modo que la carga de una cuota fija caía deprisa en los años siguientes; el indicador de primer año sobrestima la carga de aquellos años frente a hoy. Una medida más homogénea sería el esfuerzo medio durante la vida del préstamo (pendiente de decisión).
  4. *Unidad*: el BdE divide por la renta del hogar mediano; aquí se divide por la de una sola persona perceptora, por coherencia con G01c-G01e. Los niveles no son comparables con la línea del BdE (que se incluye como referencia) y un esfuerzo superior a 100 % significa que la cuota no es pagable con una sola renta, no que se pagara.
  5. *Convenciones del BdE que se conservan por comparabilidad*: préstamo del 80 % (la relación préstamo/valor efectiva, SI_1_5.38, ha sido menor), cuota bruta y sin deducciones fiscales (la deducción por vivienda habitual, vigente hasta 2012, reducía la carga efectiva antes de 2013).
- **Medias 2000-2024 del esfuerzo** (equivalentes a las de Funcas; precio de compraventa desde 2008): hogar mediano BdE 35,5 %; todas las edades 61,5 %; 18-35, 73,3 %; 55-64, 53,9 %; 65-74, 69,4 %. Años de renta: hogar BdE 7,1; todas las edades 12,2; 18-35, 14,7; 55-64, 10,7; 65-74, 13,6. El factor de financiación del BdE no depende del precio, por lo que el esfuerzo por edad hereda directamente el cambio de numerador.

## G1g_espana_patrimonio_vs_precio_vivienda_por_edad_2002_2024.csv (Gráfica 1g, la barrera de entrada)

- **Serie**: patrimonio neto mediano de los hogares por edad del cabeza de familia (menos de 35, 35-44, 55-64, 65-74 y todos), en % del precio de la vivienda tipo de 93,75 m², ambos en euros de 2024. Olas 2002-2024. Script: `graficas/scripts/g01g_patrimonio_vs_precio.py`.
- **Fuentes**: Banco de España, Encuesta Financiera de las Familias, mediana de la riqueza neta en euros de 2024 (`eff_riqueza_neta_mediana_por_edad.xlsx`, ya usado en G06; y `eff_riqueza_neta_mediana_todos.xlsx`, descarga de 15-10-2026: concept=0, variable=0, statistic=9, population=0). Precio: el de G01c-G01f, llevado a euros de 2024 con el IPC de España (BIS, media anual).
- **Por qué este indicador**: la ratio precio/renta mide un flujo y no puede reflejar lo que muestra G06, la pérdida de patrimonio de los jóvenes frente a la revalorización de los propietarios. El patrimonio sí determina la barrera de entrada: una compra exige aportar en torno al 30 % del precio (20 % de entrada no financiada e impuestos y gastos de alrededor del 10 %). Se expresa en % del precio, y no como múltiplo, porque con patrimonios cercanos a cero (5.900 € en 2014) el múltiplo se dispara sin significado.
- **Advertencias**: (1) la unidad es el hogar por edad del cabeza de familia (la de la EFF), no la persona perceptora de G01c-G01f; (2) «menos de 35» de la EFF no coincide exactamente con 18-35; (3) el umbral del 30 % es una referencia estándar, no un dato estadístico; (4) el precio de 2002-2007 es de tasación y el de 2008-2024, de compraventa (con tasación, los porcentajes serían algo menores en 2008-2014, cuando el precio de compraventa cayó más que la tasación, y mayores desde 2020: el de los menores de 35 sería del 12,8 % en 2024 en lugar del 11,1 %; columnas `_tasacion` de la tabla).
- **Lectura clave**: el patrimonio mediano de los hogares de menos de 35 años equivalía al 46 % del precio de la vivienda tipo en 2002 y al 40-43 % en 2005-2011, por encima de lo que exige una compra; desde 2014 está entre el 4 % y el 15 % (11 % en 2024). El de 35-44 cae del 95 % (2005) al 39 %; el de 65-74 sube del 93 % (2002) al 121 %.

## G11_espana_hogares_vs_viviendas_terminadas_1971_2025.csv (Gráfica 11, viviendas terminadas y hogares nuevos)

- **Series**: viviendas terminadas al año (libres + protegidas) y hogares nuevos (variación anual del número de hogares), con su saldo. 1971-2025. Script reproducible: `graficas/scripts/g11_hogares_viviendas.py`. Complementa la gráfica de referencia de Jon González (`Jon-Gonzalez/`, precio de la vivienda frente a salario real desde 2018).
- **Viviendas terminadas**:
  - 1970-1990: OCDE, *Main Economic Indicators*, «Total dwellings and residential buildings constructed for Spain» (FRED, serie PRCNDW01ESA470N, media mensual × 12; `datos/brutos/oecd_fred_viviendas_terminadas_esp_PRCNDW01ESA470N.csv`). Es la estadística de la D. G. para la Vivienda: reproduce sus cifras publicadas (1976: 319.850 frente a 319.825; 1990: 281.120 frente a 281.119) y coincide con la serie actual del Ministerio en el solape (1991: +0,3 %; 2000-2012: diferencias ≤ 0,1 %; ±5 % en 1992-1998 por revisiones posteriores).
  - 1991-2025: Mº de Vivienda y Agenda Urbana, boletín estadístico en línea: viviendas libres terminadas (tabla 32201000) + calificaciones definitivas de vivienda protegida, planes estatales y autonómicos (tabla 31306000). Ficheros en `datos/brutos/mivau_boletin/`. Control: 2024 = 86.609 + 14.371 = 100.980, la cifra publicada por el Ministerio.
- **Hogares nuevos**:
  - 1971-2001: promedio intercensal (viviendas principales de los censos del INE: 8.505.251 a 31-12-1970; 10.431.327 a 1-3-1981; 11.736.376 a 1-3-1991; 14.187.169 a 1-11-2001), interpolado linealmente por fechas censales. No hay estimación anual oficial anterior a 2002: el ciclo intra-decenal no es observable y la línea va en trazo discontinuo.
  - 2002: Mº de Vivienda, estimación del parque de viviendas principales (tabla 33102000), anclada al censo de 2001. No se usa la EPA para ese año porque su nivel de 2002 supera en unos 160.000 hogares al censo de 2001 y crearía un salto artificial.
  - 2003-2025: INE, EPA, número de hogares (media anual de los cuatro trimestres, base 2021), vía Banco de España SI_1_5.36.
- **Advertencias para la nota al pie**: (1) la EPA da −47.725 hogares en 2021 y +332.125 en 2022, en coincidencia con la pandemia y el nuevo cuestionario de la EPA de 2021; la cifra significativa es la suma de ambos años (+284.400). (2) Las viviendas terminadas incluyen segundas residencias y viviendas que quedan vacías o se destinan a no residentes; el saldo no mide «viviendas sobrantes» sino la producción frente a la formación de hogares. (3) No se descuentan demoliciones ni cambios de uso. (4) La serie empieza en 1971 porque no hay serie anual de viviendas terminadas publicada antes de 1970 (para 1960-1979 solo se conocen totales: unos 5,4 millones, según CCOO, *Cuatro décadas fallidas de política de vivienda*).
- **Lectura clave (sumas del periodo)**:

| Periodo | Viviendas terminadas | Hogares nuevos | Viviendas por hogar nuevo |
|---|---|---|---|
| 1971-1980 | 3.201.250 | 1.894.954 | 1,69 |
| 1981-1990 | 2.218.370 | 1.314.730 | 1,69 |
| 1991-2000 | 2.822.836 | 2.280.474 | 1,24 |
| 1997-2007 (burbuja) | 5.366.946 | 3.694.865 | 1,45 |
| 2009-2013 | 1.074.397 | 1.144.725 | 0,94 |
| 2014-2019 | 341.658 | 484.075 | 0,71 |
| 2020-2025 | 555.727 | 1.062.950 | 0,52 |
| 2022-2025 | 373.495 | 1.013.350 | 0,37 |
| 2021-2025, con hogares de la ECP (columna `hogares_nuevos_ecp`) | 468.223 | 1.222.836 | 0,38 |

- **Actualización de 5-11-2026**: la columna `hogares_nuevos_ecp` añade, para 2021-2025, la variación de hogares de la Estadística Continua de Población (INE, tabla 60131, del 1 de enero de cada año al del siguiente; `datos/brutos/ine_ecp/`). Las columnas anteriores no cambian. El capítulo sobre crédito usa esta serie porque evita la ruptura de la EPA de 2021, y su cifra coincide con la de las tablas L del capítulo sobre la oferta.

## G2_ratio_precio_renta_anual.csv (Gráfica 2, comparativa)

- **Serie**: *Price-to-income ratio* (índice 2015 = 100). España, Italia, Reino Unido, Hungría y zona euro (EA).
- **Fuente**: OCDE, *Analytical House Prices Indicators* (OECD.ECO.MPD / DSD_AN_HOUSE_PRICES), medida HPI_YDH. Trimestral, anualizada (media).
- **Cobertura**: España 1971–, Italia 1970–, Reino Unido 1987–, Hungría 2007–, zona euro 1980–.
- **URL**: https://sdmx.oecd.org/public/rest/data/OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,1.0/
- **Advertencia**: es un índice de evolución, no el nivel en «años de renta». Existe variante «standardised price-income ratio» (% sobre la media de largo plazo) en la misma fuente.

## G3_espana_ipc_vs_vivienda_anual.csv (Gráfica 3, España)

- **Series**: precio nominal de la vivienda, IPC y precio real de la vivienda, todo rebasado a 1971 = 100, anual (media de trimestres/meses).
- **Fuente precios vivienda**: BIS, *Selected residential property prices* (WS_SPP), serie Q:ES:N:628 (nominal) y Q:ES:R:628 (real, deflactada por IPC). España desde 1971 T1. El propio BdE es el proveedor nacional de la serie.
- **Fuente IPC**: BIS, *Long consumer prices* (WS_LONG_CPI), serie M:ES:628. España desde 1954.
- **URL**: https://stats.bis.org/api/v1/data/BIS,WS_SPP,1.0/ y .../BIS,WS_LONG_CPI,1.0/
- Contraste nacional disponible: IPC INE (variación anual desde 1962; índice enlazado desde 2002), API Tempus serie IPC251856 / IPC251852.

## G4_comparativa_precios_reales_anual.csv (Gráfica 4, comparativa)

- **Serie**: precio real de la vivienda (deflactado por IPC nacional), índice 2015 = 100, anual.
- **Fuente**: BIS, *Selected residential property prices* (WS_SPP), series R:628.
- **Cobertura**: España 1971–, Italia 1947– (nominal desde 1927), Reino Unido 1968–, **Hungría 1992–** (nominal desde 1990), zona euro (XM) 1975–.

## Series ya descargadas para las Gráficas 8 y 10 (pendientes de elaborar)

De BdE *Síntesis de Indicadores* cuadro 1.5 (`datos/procesados/`):

| Fichero | Serie | Cobertura | Fuente primaria |
|---|---|---|---|
| mivau_viv_iniciadas_total.csv | Viviendas iniciadas, total | 1970– | Mº de Vivienda y Agenda Urbana |
| mivau_viv_iniciadas_libres.csv | Viviendas iniciadas, libres | 1980– | Mº de Vivienda y Agenda Urbana |
| mivau_viv_iniciadas_protegidas.csv | Viviendas iniciadas, protegidas | 1970– | Mº de Vivienda y Agenda Urbana |
| mitms_visados_obra_nueva.csv | Visados de obra nueva | 1991– | Mº de Transportes y Movilidad Sostenible |
| mivau_compraventas_total/nueva/usada.csv | Compraventas ante notario | 2004– | Mº de Vivienda y Agenda Urbana |
| mivau_precio_m2_tasada.csv | Precio m² vivienda libre tasada | 1995– | Mº de Vivienda y Agenda Urbana |
| st_precio_m2_capitales.csv | Precio m² (capitales) | 1985– (semestral) | Sociedad de Tasación |
| eurostat_rbd_hogares_es.csv | RBD hogares e ISFLSH (B6G), mill. € | 1995–2024 | Eurostat, nasa_10_nf_tr (ESA 2010) |

## G2b_ratio_precio_renta_estandarizado_anual.csv (Gráfica 2, variante estandarizada)

- **Serie**: *Standardised price-income ratio* (% sobre la media de largo plazo de cada país; 100 = valoración en línea con su media histórica).
- **Fuente**: OCDE, *Analytical House Prices Indicators*, medida HPI_YDH_AVG. Anualizada (media de trimestres).
- Misma cobertura que G02. Lectura directa de «sobrevaloración» respecto a renta; útil para la hipótesis de convergencia.

## G8a_espana_viviendas_iniciadas_anual.csv (Gráfica 8, producción)

- **Series**: viviendas iniciadas (total, libres, protegidas) y visados de obra nueva. Sumas anuales de datos mensuales.
- **Fuente**: Mº de Vivienda y Agenda Urbana (iniciadas) y Mº de Transportes y Movilidad Sostenible (visados), vía Banco de España, Síntesis de Indicadores cuadro 1.5 (series SI_1_5.16-19).
- **Advertencias del BdE**: (1) hasta diciembre de 1979 la serie «total» incluye únicamente viviendas protegidas — no existe dato mensual de libres antes de 1980 (solo semestral/anual en publicaciones históricas); (2) «protegida» incluye promoción privada y pública.

## G8b_espana_compraventas_anual.csv (Gráfica 8, compraventas)

- **Series**: compraventas de vivienda ante notario: total, nueva, usada. Sumas anuales de datos trimestrales, 2004–.
- **Fuente**: Mº de Vivienda y Agenda Urbana (con Consejo General del Notariado), vía Banco de España, Síntesis de Indicadores cuadro 1.5 (SI_1_5.25-27).

## G9_ue_permisos_viviendas_anual.csv (Gráfica 9, oferta UE)

- **Serie**: permisos de construcción — número de viviendas (miles), edificios residenciales excepto residencias colectivas. UE-27, zona euro (EA20), España, Italia, Hungría y Reino Unido (hasta 2019, Brexit).
- **Fuente**: Eurostat, *Building permits — annual data* (sts_cobp_a), indicador BPRM_DW, unidad THS, sin ajustar.
- **Cobertura**: 2005–2025 para el agregado UE (no existe agregado anterior). Si se necesita un tramo más largo por país, existe el índice trimestral (base 2015/2021) y, como fuente complementaria no oficial-UE, las *completions* de EMF-Hypostat desde los años 90 — pendiente de decisión.

## G7_eeuu_riqueza_por_edad_anual.csv y G7b_..._por_generacion (Gráfica 7)

- **Series**: participación (%) en la riqueza neta total de los hogares de EE.UU. por grupo de edad (<40, 40-54, 55-69, 70+) y por generación (Silent, Baby Boom, Gen X, Millennial); también participación en la riqueza inmobiliaria. Medias anuales de datos trimestrales.
- **Fuente**: Reserva Federal, *Distributional Financial Accounts* (DFA), 1989 T3 – 2026 T1.
- **URL**: https://www.federalreserve.gov/releases/z1/dataviz/download/zips/dfa.zip (ficheros dfa-age-shares.csv y dfa-generation-shares.csv). Descargado 2026-07-16.
- Dato ilustrativo: los menores de 40 años pasan del 11,6 % de la riqueza (1990) al 6,7 % (2025); los mayores de 70, del 19,3 % al 31,9 %.

## G6_espana_riqueza_neta_mediana_por_edad.csv y G06b (media) (Gráfica 6)

- **Series**: riqueza neta mediana (y media) de los hogares por edad del cabeza de familia (<35, 35-44, 45-54, 55-64, 65-74, ≥75). Miles de euros **en términos reales, base 2024**. Olas EFF 2002-2024 (9 olas).
- **Fuente**: Banco de España, Encuesta Financiera de las Familias (EFF), herramienta oficial de resultados.
- **URL**: https://app.bde.es/efs_www/quick-download?concept=0&variable=0&statistic=9&population=7&lang=ES (mediana; statistic=0 para la media). Ficheros xlsx originales en datos/brutos/. Descargado 2026-07-16.
- **Nota**: la EFF arranca en 2002; no existe fuente española comparable anterior (decisión de equipo: aceptar horizonte 2002-2024). La ola 2024 se publicó en abril de 2026 (Documento Ocasional BdE 2610).
- Dato ilustrativo: mediana real de los <35 años: 104.200 € (2005) → 5.900 € (2014) → 22.900 € (2024); los ≥75: 118.200 € (2002) → 214.500 € (2024).

## G1b_espana_precio_vs_renta_indexado.csv (Gráfica 1, versión indexada, 1987-2025)

- **Series**: precio del m² de vivienda libre tasada (serie enlazada) e ingreso bruto del hogar mediano, ambos indexados 1987=100, más la ratio oficial en años de renta.
- **Precio 1987-1994**: Ministerio de Fomento, *Precio medio del m² de las viviendas. Datos de tasaciones hipotecarias* (serie antigua, base 1987), reproducida en R. Vergés, «Estadísticas de vivienda libre en España. 1987-2011», *Estadística Española* (INE), vol. 54, n.º 179 (2012), Tabla 5.
- **Precio 1995-2025**: Mº de Vivienda y Agenda Urbana, valor tasado de vivienda libre (vía BdE, SI_1_5.4). Enlace 1994→1995 sin discontinuidad apreciable (660 → 683 €/m²).
- **Renta del hogar mediano**: derivada aritméticamente de las series del Banco de España como precio_m² × 93,75 / ratio(SI_1_5.43); es la renta bruta del hogar mediano implícita en la metodología del BdE. Valores de control: ~9.900 € (1987), ~20.600 € (2007), ~25.400 € (2024).
- **Nota metodológica**: el tramo 1987-1994 procede de la serie antigua de Fomento con base muestral más reducida (las tasadoras se agruparon en ATASA a partir de 1995); el propio BdE enlaza internamente ambas series en su ratio. Documentar en nota al pie de la gráfica.

## G5_espana_transferencia_alquiler_por_edad.csv (Gráfica 5, sincrónica)

- **Series**: alquiler anual pagado y cobrado por los hogares españoles, por tramo de edad de la persona responsable de la vivienda. Año 2025 (alquileres pagados: mensualidad vigente ×12; alquileres cobrados: renta bruta del ejercicio fiscal 2024).
- **Fuente**: elaboración propia sobre **microdatos de la Encuesta de Condiciones de Vida 2025 (INE)**, descarga libre (ecv_b2013/datos_2025.zip). Variables: HH060 (alquiler mensual), HH021 (régimen de tenencia, códigos 3-4), HY040G (renta bruta por alquiler de propiedades), RB080 (año de nacimiento del responsable), DB090 (factor de elevación). Script reproducible: `graficas/scripts/g5_ecv_transferencia_alquiler.py`.
- **Validación**: el total estimado de alquiler pagado (27.870 M€) coincide con el publicado por eldiario.es con la misma fuente (~28.000 M€ en 2025).
- **Nota**: la diferencia entre lo pagado por los hogares y lo declarado como cobrado por hogares (7.582 M€) corresponde a alquileres pagados a personas jurídicas, alquiler no declarado y otros — misma categoría residual que emplea eldiario.es. Los dos lados proceden de la misma encuesta pero de periodos de referencia distintos (renta corriente vs. ejercicio fiscal previo); documentar en nota al pie.
- Lectura clave: los hogares con responsable menor de 45 años pagan el 47 % del alquiler total y perciben menos del 10 %; los mayores de 65 perciben 9.635 M€ y pagan 3.176 M€.

## G10_espana_vpo_precio_maximo_1979_2025.csv (Gráfica 10, VPO)

- **Serie**: precio máximo legal de venta de una vivienda de protección oficial de régimen general de **90 m² útiles** (tope del RD-L 31/1978), en el **área geográfica media nacional**, año a año 1979-2025; y su expresión en años de renta bruta del hogar mediano (1987-2025, denominador derivado de las series del Banco de España, mismo que G01b).
- **Fuente**: elaboración propia a partir del **BOE** (todas las normas verificadas en el texto original; columna `norma` de la tabla). Cadena normativa:
  - **Regla de precio**: art. 11 del RD 3148/1978 (BOE-A-1979-1217): precio venta ≤ 1,2 × módulo (M) por m² útil. El factor 1,2 sobre el módulo (ponderado desde 1984) se mantiene en el RD 3280/1983 (BOE-A-1984-252), RD 1494/1987 (BOE-A-1987-27603, DA 2.ª), RD 224/1989 y RD 1932/1991 (BOE-A-1992-604) hasta 1997.
  - **Módulos**: O. 19-1-1979 (BOE-A-1979-3278, área B1: 26.500 pts/m²); revisiones: O. 25-1-1980 (BOE-A-1980-2906, +10,48%), O. 27-1-1981 (BOE-A-1981-2371, +14,23%), O. 23-3-1982 (BOE-A-1982-8401, +14,13%), O. 11-3-1983 (BOE-A-1983-7974, +7,78%). Nuevo sistema de áreas y ponderación: O. 7-3-1984 (BOE-A-1984-5919, A1 47.614 pts, pond. 11%), O. 13-12-1984 (BOE-A-1984-27970, 50.947, 10%), O. 6-2-1986 (BOE-A-1986-3583, 53.622, 8,75%), O. 23-12-1986 (BOE-A-1986-33760, 55.901, 6%), O. 15-1-1988 (BOE-A-1988-2612, 57.578, 4,3%), O. 4-3-1989 (BOE-A-1989-5407, 59.536, 4,3%), O. 12-2-1990 (BOE-A-1990-4100, 63.287, 6,75%), O. 18-1-1991 (BOE-A-1991-2152, 67.559, 7,1%). Plan 92-95 (áreas 1.ª-4.ª por población; usamos área 3.ª, 100.000-500.000 hab.): O. 18-3-1992 (BOE-A-1992-6452, 67.131 pts, pond. 6,57%; sin revisión en 1993), O. 22-12-1993 (BOE-A-1993-30993, pond. 72.639), O. 31-1-1995 (BOE-A-1995-2886, 72.639), O. 15-2-1996 (BOE-A-1996-3831, 72.639; prorrogados para 1997 y 1998 por BOE-A-1996-29122 y BOE-A-1998-2983).
  - **Precio básico nacional**: RD 1186/1998 (BOE-A-1998-15136, DA 2.ª: 98.500 pts/m² útil; banda CCAA +15%/−20%); RD 115/2001 (100.500 pts = 604,02 €, BOE-A-2001-23913); RD 1/2002 (BOE-A-2002-689: PBN 623,77 €; techo general nueva construcción 1,56×PBN); Acuerdos CM 27-12-2002 (636,25 €, BOE-A-2003-987) y 26-12-2003 (648,98 €, BOE-A-2004-316); RD 801/2005 (BOE-A-2005-12049, DA 1.ª: PBN 695,19 €; vivienda de precio general 1,60×); **RD 2066/2008 (BOE-A-2008-20751, DA 2.ª: Módulo Básico Estatal 758 €/m² útil, precio general 1,60× = 1.212,80 €/m² útil, SIN ACTUALIZAR desde diciembre de 2008)**.
- **Advertencias metodológicas** (para la nota al pie): (1) "área media" = B1 (1979-83) → A1 (1984-91) → área 3.ª (1992-98), grupos que contienen la mayoría de capitales de provincia salvo Madrid/Barcelona; el empalme 1991→1992 es prácticamente continuo (72.356 → 71.541 pts). (2) Desde 1998 el Estado fija una referencia nacional y las CCAA concretan el precio dentro de bandas/techos: usamos el techo aplicable típico de capital (1,15×PBN en 1998-2001; 1,56×PBN en 2002-04; 1,60×PBN/MBE desde 2005), lo que introduce un salto real (+30% en 1998) que refleja el cambio de régimen, no un error de serie. (3) Sin ATPMS (Madrid/Barcelona tendrían incrementos adicionales).
- **Pendiente** (siguiente fase): tramo 1954-1978 (viviendas de renta limitada de la Ley de 15-7-1954 y VPO grupos I/II del D. 2131/1963 y Reglamento D. 2114/1968), cuya regla de precio se basa en el coste de ejecución material y exige supuestos adicionales; y denominador de renta para 1979-1986 (series históricas académicas).

### G10 — Denominador de renta 1979-1986 (añadido)

- **Método**: la renta bruta del hogar mediano (serie BdE, disponible desde 1987) se retropola a 1979-1986 con el índice de **renta nacional neta disponible (NNDI) nominal por hogar**: NNDI de L. Prados de la Escosura, *Spain's Historical National Accounts: Expenditure and Output, 1850-2024* (actualización 20-10-2025, Tabla 2; citar como Prados de la Escosura, *Spanish Economic Growth, 1850-2015*, Palgrave, 2017), dividida por el número de hogares (= viviendas principales censales INE: 8.505.251 en 1970; 10.431.327 en 1981; 11.736.376 en 1991, tomadas del cuadro SI_1_5 del BdE, series 84; interpolación log-lineal intercensal).
- **URL dataset**: https://frdelpino.es/investigacion/wp-content/uploads/2025/10/Spains_Historical_National_Accounts_1850-2024_frdp_20.10.2025.xlsx (en datos/brutos/). Descargado 2026-07-17.
- **Control de empalme**: la ratio VPO/renta pasa de 4,28 (1986, método académico) a 3,88 (1987, método BdE) — discontinuidad moderada y en el sentido esperado (la renta mediana crece algo menos que la renta media nacional por hogar); documentar en nota al pie. La columna `metodo_denominador` de la tabla identifica el método de cada año.
- **Decisión de equipo (17-7-2026)**: el tramo 1954-1978 no se incluye en la serie numérica; el régimen de renta limitada/grupos I-II se tratará en el texto con hitos documentados.

### Nota G02b
La OCDE no publica el ratio estandarizado (HPI_YDH_AVG) para Hungría (serie demasiado corta): la gráfica G02b compara España, Italia, Reino Unido y zona euro. Hungría sí aparece en G02 (índice, desde 2007) y en G04 (precios reales, desde 1992).

## G12_contratos_alquiler_fianzas_trimestral.csv y G12b_contratos_alquiler_fianzas_anual.csv (Gráfica 12, contratos de alquiler registrados)

- **Series**: nuevos contratos de alquiler de vivienda con fianza depositada en los registros autonómicos, y su renta media mensual. Trimestral: 2016 T1 - 2026 T1 (Cataluña desde 2019 T1; Euskadi hasta 2025 T4). Anual: 2005-2025 (Cataluña), 2007-2025 (Barcelona ciudad), 2016-2025 (Euskadi). Script reproducible: `graficas/scripts/g12_fianzas_contratos.py`; gráfica: función `g12` de `generar_graficas.py`. Descarga: 7-10-2026, en `datos/brutos/fianzas/`.
- **Cataluña y Barcelona**: Incasòl, Registre de fiances, vía Dades Obertes de la Generalitat:
  - conjunto `qww9-bvhh` («Preu mitjà del lloguer d'habitatges per municipi»): contratos (`Habitatges`) por municipio y periodo;
  - conjunto `hepw-33ik` (ámbitos supramunicipales): renta media trimestral de Cataluña y años 2005-2006.
  - Fecha de referencia: **alta de la fianza en el registro**, no inicio del contrato.
- **Euskadi**: Gobierno Vasco, Estadística del Mercado de Alquiler (EMAL), fichero `EMAL-2016-2025_es.xlsx`, tablas T1.1/T1.2 (trimestral) y T2.1/T2.2 (anual): solo **alquiler libre de vivienda habitual en vivienda colectiva**. Fecha de referencia: **trimestre de inicio del contrato**. Existencias a 31-12-2025: 86.522 contratos vigentes de vivienda habitual colectiva y 3.144 de temporada (tabla A1).
- **Errata detectada en la fuente**: el total «Catalunya» de 2025 en `hepw-33ik` (enero-diciembre) es 80.309 contratos, incompatible con su propio acumulado enero-septiembre (81.126) y con la suma de sus trimestres (108.057). La suma de municipios de `qww9-bvhh` da 108.057, que es la cifra que se usa. Conviene comunicarlo a la Generalitat.
- **Advertencias para la nota al pie**:
  1. Mide **contratos firmados y registrados** (flujo), no la oferta disponible ni el parque alquilado. Una caída es compatible con menos viviendas en el mercado, pero también con contratos más largos (menos rotación: las duraciones mínimas de 5/7 años del RDL 7/2019 y las prórrogas de la Ley 12/2023 reducen las firmas nuevas sin reducir el número de hogares en alquiler), con desplazamiento a modalidades sin fianza depositada (temporada, habitaciones, contratos no registrados) o con menor cumplimiento del depósito.
  2. Las dos fuentes no son homogéneas (fecha de alta frente a inicio del contrato; universo completo frente a vivienda habitual colectiva): se comparan en índice 2019 = 100, no en niveles.
  3. El último trimestre de cada fuente es provisional (fianzas depositadas tarde).
  4. El crecimiento de 2005-2013 en Cataluña refleja en parte la extensión del cumplimiento de la obligación de depósito, no solo el mercado.
  5. Ninguna serie cubre todavía los RDL 26-29/2026: Cataluña llega a 2026 T1 (publicado el 30-7-2026) y la EMAL a 2025 T4.
- **Lectura clave**: 2025 frente a 2019: Cataluña −33,5 % (162.520 → 108.057); Barcelona −40,0 % (51.294 → 30.789); Euskadi −24,8 % (20.959 → 15.758). El descenso empieza en 2022-2023, antes de los topes catalanes de marzo de 2024, y es común a dos comunidades con regulaciones distintas: no puede atribuirse a una norma concreta sin un diseño causal.

## G13_espana_tenencia_hipoteca_por_edad_2004_2025.csv y G13b_espana_hipoteca_jovenes_por_renta_y_contrato_2004_2025.csv

- **Series**: régimen de tenencia de la vivienda principal por edad de la persona responsable; proporción con hipoteca entre los hogares con responsable de 25 a 39 años, por quintil de renta, tipo de contrato y perfil.
- **Fuente**: INE, ECV 2004-2025, microdatos. Script: `graficas/scripts/g13_tenencia_hipoteca_por_edad.py`.
- **Advertencias**: la tenencia procede de HH021 desde 2011. En 2004-2010 solo existe HH020, y la hipoteca se identifica por la pregunta de retrasos en el pago de hipoteca o alquiler (HS010/HS011).

## G14_espana_alquiler_y_colchon_ahorro_por_edad_2004_2025.csv y G14b_espana_emancipacion_e_hipoteca_por_edad_simple.csv

- **Series**: capacidad de afrontar un gasto imprevisto (HS060) y esfuerzo en alquiler de los inquilinos de mercado (12 × HH060 / HY020), por edad; emancipación e hipoteca por tramos de edad simple.
- **Fuente**: INE, ECV 2004-2025, microdatos. Script: `graficas/scripts/g14_alquiler_ahorro_por_edad.py`.
- **Advertencia**: la renta de 2005-2007 se corrige por el cambio de base de 2008 (k_hogar = 1,146; `datos/procesados/g1c_enlace_ecv_bases.json`).

## G15_espana_propiedad_por_edad_1980_2025.csv

- **Series**: hogares encabezados, propietarios y propietarios con pagos pendientes por cada cien personas de cada tramo de edad.
- **Fuente**: INE, microdatos de EPF 1980-81, EBPF 1990-91 y ECV. Script: `graficas/scripts/g15_propiedad_jovenes_1980_2025.py`.
- **Advertencias**: el diseño de registro de 1980-81 no recoge la lista de códigos de tenencia, que se infiere de la estructura del fichero y se contrasta con la publicada para 1990-91. En 1980-1991, «pagos pendientes» incluye pagos aplazados al promotor o a la cooperativa.

## G16_espana_alquiler_jovenes_por_territorio_2005_2025.csv

- **Series**: alquiler mediano en euros de 2024 y esfuerzo de los hogares con responsable de 25 a 34 años en alquiler de mercado, por grado de urbanización, comunidad autónoma y tipo de hogar; 2005-2008 frente a 2022-2025.
- **Fuente**: INE, ECV, microdatos; IPC de España vía BIS. Script: `graficas/scripts/g16_alquiler_jovenes_segmentado.py`.

## G17_espana_pobreza_tras_vivienda_inquilinos_jovenes_2005_2025.csv

- **Series**: riesgo de pobreza antes y después de pagar la vivienda en los hogares con responsable de 25 a 34 años, por régimen de tenencia, con la convención estadística y con la cuota hipotecaria completa.
- **Fuente**: INE, ECV, microdatos. Script: `graficas/scripts/g17_pobreza_tras_vivienda_jovenes.py`.
- **Advertencia**: la cuota completa solo está disponible desde 2008 (variable nacional).

## G18_espana_umbral_renta_acceso_compra_2004_2024.csv

- **Series**: renta neta mínima para atender la cuota de una hipoteca por el 80 % de la vivienda tipo, con un esfuerzo del 30 % (variante del 35 %), y proporción de la población por debajo de ese umbral.
- **Fuente**: precios de la tabla G01c, condiciones de préstamo del Banco de España (tabla G01f) y ECV. Scripts: `graficas/scripts/g18_umbral_renta_acceso_compra.py` y `g18_grafica.py`.

## G19_espana_emancipacion_y_alquiler_de_entrada_2005_2025.csv

- **Series**: tasa anual de emancipación de los jóvenes de 18 a 34 años que viven con sus padres, destino por régimen de tenencia y alquiler de entrada.
- **Fuente**: INE, ECV, ficheros longitudinales 2005-2008 (base 2004), 2009-2012, 2015-2018 y 2022-2025 (base 2013). Script: `graficas/scripts/g19_emancipacion_longitudinal.py`.
- **Advertencias**: la encuesta pierde a parte de quienes cambian de domicilio, por lo que el nivel de la tasa está infravalorado. La muestra de quienes se emancipan al alquiler es de 40 a 71 personas por panel, insuficiente para estimar con precisión el alquiler de entrada.

## G20_bancos_espanoles_densidad_apr_por_exposicion_2025.csv

- **Series**: densidad de activos ponderados por riesgo (APR / valor de exposición) por clase de exposición de los bancos españoles.
- **Fuente**: EBA, *2025 EU-wide Transparency Exercise*, `tr_cre.csv`, fecha de referencia 30-6-2025. Script: `graficas/scripts/g20_densidad_capital_eba.py`.
- **Advertencias**: datos consolidados de grupo, incluida la actividad en el extranjero. La financiación especializada comprende también la de proyectos, activos y materias primas.

## G21, G22 y G23 (gráficas del capítulo sobre crédito)

- **G21**: crédito con garantía inmobiliaria a la construcción y las actividades inmobiliarias y crédito a los hogares para vivienda, % del PIB (Banco de España, SI_1_5.54 y SI_1_5.56, dato de diciembre). **G22**: propietarios de 25 a 34 años (tabla G15). **G23**: destino de quienes se emancipan (tabla G19).
- **Scripts**: `graficas/scripts/g21_graficas_capitulo_credito.py` (imágenes en color y en blanco y negro) y `g21_g23_excel_editables.py` (`graficas/editables/`: libros Excel con datos y gráficos editables de G21 y G23, en color y en blanco y negro, que pide el anexo técnico de la editorial).

## Detalle de los datos del capítulo sobre crédito sin tabla propia

**Condiciones del crédito hipotecario (tabla 3 del capítulo).** Banco de España, *Síntesis de indicadores*, cuadro 1.5, series SI_1_5.25 (compraventas ante notario) y SI_1_5.37 a SI_1_5.39 (relación préstamo-valor y plazo); INE, *Estadística de hipotecas*, tabla 3223. Brutos en `datos/brutos/bde_si_1_5.csv` y `datos/brutos/ine_hipotecas/`.

**Encuesta sobre Préstamos Bancarios (BCE).** `datos/brutos/bce_bls/bls_es_hogares_vivienda.csv`, España, préstamos a hogares para vivienda, porcentajes netos, sumas por periodo:

| Serie | 2007-2009 | 2015-2018 |
|---|---|---|
| Criterios de aprobación (`Z…ST`) | +650 | −89 |
| Condiciones de relación préstamo-valor (`LVR…TC`) | +690 | +133 |

Factores del endurecimiento de los criterios de aprobación, sumas de 2007 a 2014: perspectivas del mercado de la vivienda (`HMP`) +787; actividad económica general (`GEA`) +683; coste de los recursos y restricciones de balance (`BSC`) +329, de los que +110 en 2008 y +167 en 2011-2012.

**Compras sin hipoteca.** Colegio de Registradores, *Estadística Registral Inmobiliaria*, cuarto trimestre de 2025 (`datos/brutos/registradores/eri_4t_2025.pdf`): compraventas con hipoteca, 74,3 % en el cuarto trimestre y 70,8 % en el tercero. INE, hipotecas sobre vivienda, frente a compraventas ante notario: 34 % sin hipoteca en 2025. Banco de España, *Informe de Estabilidad Financiera. Primavera 2026*, recuadro 4.1, nota 1: 67 % de las primeras viviendas con hipoteca en 2017-2023.

**Vivienda en la riqueza de los hogares.** Banco de España, EFF 2024 (`datos/brutos/eff_series/eff_todas_las_series.csv`). Percentiles 25-50 y 50-75 de riqueza neta: activos reales, 84,5 % de la riqueza bruta en ambos; vivienda principal, 80,5 % y 74,5 % de los activos reales, es decir, en torno al 68 % y al 63 % de la riqueza bruta.

**Cálculo ilustrativo de capital.** Exposición × ponderación × 8 % (art. 92.1.c CRR), sin colchones ni Pilar 2. Hipoteca con relación préstamo-valor del 80 %: (55/80 × 20 % + 25/80 × 75 %) = 37,2 %. Con garantía del Estado sobre el 50 % de un préstamo AUE: 500.000 × 150 % × 8 % = 60.000 euros (art. 235.1 CRR, con ponderación del 0 % en la parte cubierta).
