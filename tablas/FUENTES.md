# Fuentes de las tablas de datos

Fecha de descarga de todos los datos: 16 de julio de 2026.
Los ficheros brutos originales están en `datos/brutos/`; las series limpias en `datos/procesados/`.

## G1_espana_ratio_precio_rbd_anual.csv (Gráfica 1, versión ratio)

- **Serie**: Precio de la vivienda / Renta bruta disponible por hogar (años de renta).
- **Fuente**: Banco de España, *Síntesis de Indicadores*, cuadro 1.5 «Mercado de la vivienda», serie SI_1_5.43 (código DHIVTNOAPLPMMUVT_RLI derivado). Trimestral, 1987 T1 – 2026 T1; aquí anualizada (media de trimestres).
- **Definición BdE**: «Precio medio de una vivienda libre de 93,75 m² construidos dividido por la renta bruta estimada del hogar mediano».
- **URL**: https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/si_1_5.csv
- Complemento disponible: serie SI_1_5.44 «esfuerzo teórico anual» (% de renta destinado a cuotas el primer año), misma fuente y periodo (`datos/procesados/bde_esfuerzo_teorico.csv`).

## G1bis_espana_ratio_precio_rbd_anual_1971.csv (Gráfica 1bis, serie extendida 1971-2025)

- **Serie**: la misma ratio de G1 (precio de la vivienda en años de renta bruta del hogar mediano), con el tramo 1971-1986 retropolado. La columna `metodo` identifica el origen de cada año.
- **Tramo 1987-2026**: serie oficial BdE, idéntica a G1.
- **Tramo 1971-1986 (retropolación, script `graficas/scripts/g1bis_retropolacion_1971.py`)**:
  - *Numerador*: precio del m² de 1987 (327 €/m², Fomento, tabla G1b) retropolado con el índice nominal del BIS, *Selected residential property prices* (WS_SPP, serie de España, media anual de trimestres), × 93,75 m².
  - *Denominador*: renta bruta del hogar mediano de 1987 (9.913 €, implícita en la serie BdE, tabla G1b) retropolada con la NNDI nominal por hogar — mismo método aprobado para el denominador 1979-1986 de G10 (Prados de la Escosura, Tabla 2; hogares = viviendas principales censales INE 1970/1981/1991, interpolación log-lineal). La reproducción de la renta 1979-1986 coincide exactamente con la de G10.
- **Columna `ratio_contraste_ocde`** (solo 1971-1986): la misma ratio retropolada con el índice *price-to-income* de la OCDE (HPI_YDH, España) encadenado en 1987. Diferencia máxima con la serie principal: 0,25 años (1981). Se descartó como método principal porque la OCDE usa renta disponible **por persona**, no por hogar: en el solapamiento 1987-2025 esa diferencia de concepto acumula desviaciones grandes (2007: 6,1 frente al 9,4 oficial), al crecer el número de hogares más deprisa que la población.
- **Advertencia para la nota al pie**: el tramo retropolado combina un índice de precios de cobertura limitada en los setenta con una renta media por hogar (no mediana); es una aproximación académica, no estadística oficial, y así se distingue (trazo discontinuo) en la gráfica G01bis.

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
- Misma cobertura que G2. Lectura directa de «sobrevaloración» respecto a renta; útil para la hipótesis de convergencia.

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

## G6_espana_riqueza_neta_mediana_por_edad.csv y G6b (media) (Gráfica 6)

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

- **Serie**: precio máximo legal de venta de una vivienda de protección oficial de régimen general de **90 m² útiles** (tope del RD-L 31/1978), en el **área geográfica media nacional**, año a año 1979-2025; y su expresión en años de renta bruta del hogar mediano (1987-2025, denominador derivado de las series del Banco de España, mismo que G1b).
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

### Nota G2b
La OCDE no publica el ratio estandarizado (HPI_YDH_AVG) para Hungría (serie demasiado corta): la gráfica G2b compara España, Italia, Reino Unido y zona euro. Hungría sí aparece en G2 (índice, desde 2007) y en G4 (precios reales, desde 1992).

---

# Segunda entrega: nuevos grupos de datos (N1-N6), agosto de 2026

## N1_espana_vpo_franquismo_anual.csv y N1_plazos_regimen_proteccion.csv (VPO del franquismo)

- **Serie**: viviendas acogidas a la protección del Estado, terminadas (calificación definitiva), 1958-1975, total nacional.
- **Fuente**: Anuarios Estadísticos de España (INE, fondo documental digitalizado, inebaseweb), cuadros «Edificación y vivienda — Viviendas acogidas a la protección del Estado»: Anuario 1965 (datos 1958-1964), Anuario 1971 (1963-1970) y Anuario 1976 (1967-1975). PDFs originales en `datos/brutos/ine_anuario*_viv*.pdf`. Descargado 2026-08-07.
- **Validación cruzada**: los años de solapamiento coinciden entre anuarios (1963-64, 1967-69 exactos; 1970: 185.290 vs 185.294, discrepancia de 4 viviendas que se documenta; se toma el dato del anuario más reciente).
- **Límites**: (1) el tramo 1950-1957 no se incluye: corresponde a regímenes anteriores no homologables (viviendas protegidas de la Ley de 19-4-1939 y bonificables del D.-L. de 19-11-1948) cuyos cuadros no están expuestos con título identificable en los anuarios digitalizados 1955-1961; se tratará con hitos en el texto. (2) El desglose territorial histórico es provincial y no se ha extraído (decisión de equipo: serie nacional). Contexto adicional disponible: cuadro provincial de la Fiscalía Superior de la Vivienda con promedios 1941-55 (`ine_anuario1958_viv0.pdf`).
- **Plazos del régimen de protección** (N1_plazos_regimen_proteccion.csv): no existe estadística de descalificaciones efectivas; la tabla recoge la duración LEGAL del régimen por periodo de calificación. Verificado sobre texto BOE: Reglamento D. 2114/1968, arts. 100 y 146 (50 años desde la calificación definitiva, extinción automática por transcurso; BOE-A-1968-1060) y RD-L 31/1978, art. 1 (30 años; BOE-A-1978-27765). Los regímenes de 1939 y 1954 quedaron verificados el 7-8-2026 sobre los facsímiles del BOE: Ley de 19-4-1939 (BOE-A-1939-6523; BOE núm. 110 de 20-4-1939, `boe_ley1939_viviendas_protegidas.pdf`), art. 5.b) — exención del 90% de «toda contribución, impuesto o arbitrio... durante los veinte años siguientes» — y art. 6 (reintegro de anticipos a partir de los veinte años); y Ley de 15-7-1954 (BOE núm. 197 de 16-7-1954, pp. 4834-4841, `boe_ley1954_renta_limitada.pdf`), art. 13 — bonificación del 90% «durante un plazo de veinte años» — y art. 10.Octavo (exención de la primera transmisión «dentro de los veinte años siguientes a la fecha de su calificación»). Se archiva además la edición compilada del Ministerio (`mitms_ley1954_renta_limitada.pdf`, incluye texto con anotaciones de órdenes posteriores). Conclusión reforzada: en toda la cadena 1939→1954→1968→1978, el plazo más largo de protección (50 años) es el del Reglamento de 1968, y el más corto (30 años) el del régimen democrático de 1978.

## N2_espana_vpo_por_promotor_anual.csv (VPO por tipo de promotor)

- **Series**: calificaciones definitivas y provisionales de vivienda protegida por tipo de promotor (privado/público), planes estatales y autonómicos. Sumas anuales de series mensuales, 2014-2026.
- **Fuente**: Boletín estadístico online MITMS/MIVAU (apps.fomento.gob.es/boletinonline2), cuadros 1.6.2.1/1.6.2.2 (definitivas) y 1.3.2.1/1.3.2.2 (provisionales); ficheros sedal 31206010/20 y 31203010/20. Descargado 2026-08-07. Script: `graficas/scripts/n_series_boletin_mitms.py`.
- **Límites y descartes documentados**: (1) el desglose mensual por promotor solo se publica desde 2014; la ampliación 1991-2013 exigiría el Boletín anual del Observatorio de Vivienda y Suelo (pendiente). (2) Se DESCARTÓ el cuadro 7 de visados de aparejadores («viviendas según clase de promotor», 1991-) porque su nota metodológica advierte que las obras promovidas por el Estado, las CCAA y las corporaciones locales no se visan en dichos colegios: la serie no capta a la Administración y no sirve para este desglose.

## N3_espana_destinos_pms_2004.csv (patrimonios municipales de suelo)

- **Serie**: distribución porcentual de los destinos de los bienes y recursos de los Patrimonios Municipales de Suelo, ejercicio 2004 (muestra: capitales de provincia, municipios >100.000 hab. y los cinco mayores >20.000 de cada CCAA).
- **Fuente**: Tribunal de Cuentas, *Informe de fiscalización de la gestión y control de los recursos integrantes del Patrimonio Municipal del Suelo, ejercicio 2004* (aprobado por el Pleno el 26-6-2008; Resolución de la Comisión Mixta de 8-10-2008), publicado en BOE núm. 33, de 7-2-2009, BOE-A-2009-2122 (PDF en `datos/brutos/tcu_pms_2004_boe.pdf`).
- **Contexto**: no existe estadística nacional continua de los PMS ni del suelo de cesión obligatoria (10 % del aprovechamiento) pendiente de desarrollo — verificado y documentado; esta foto fija oficial es el mejor dato disponible (decisión de equipo, 2026-08-07). Datos complementarios del mismo informe: solo 21 ayuntamientos (14,6 % de los fiscalizados) tenían el PMS formalmente constituido a 31-12-2004.

## N4_espana_coste_construccion_vs_precio.csv (costes de construcción vs precio de venta)

- **Series**: presupuesto de ejecución material (PEM) por m² de la edificación residencial visada (obra nueva) frente al precio de venta del m² de vivienda libre; y residual = precio − PEM. Anual 1992-2025.
- **Fuentes**: visados de dirección de obra de los Colegios de Aparejadores (Boletín estadístico MITMS, cuadros 9.2 superficie y 9.3 presupuesto, ficheros sedal 09010200/09010300; reconstrucción anual por suma de los 12 meses, validada contra el bloque anual del fichero donde existe y por identidad contable residencial = suma de componentes en todos los años); precio de venta: serie enlazada de G1b (Fomento base 1987/MIVAU). Script: `graficas/scripts/n4_n5_costes_visados.py`.
- **Definición y advertencia**: el PEM excluye IVA, honorarios facultativos, gastos generales, beneficio del contratista, costes financieros y suelo (definición oficial de la nota metodológica MITMS). El residual precio−PEM comprende suelo + márgenes + costes no-PEM: es una COTA SUPERIOR de la repercusión del suelo, no el suelo aislado (método aprobado por el equipo como complemento).
- Lectura clave: el PEM era el 36 % del precio de venta a mediados de los noventa, cayó al 18,5 % en 2006 (residual suelo+márgenes: 81,5 %) y ronda el 31-33 % desde 2014.
- Complemento incorporado el 7-8-2026: véase N4b.

## N4b_espana_indices_costes_materiales.csv (índice de costes por componentes: complemento de N4)

- **Series**: Índice de Costes del Sector de la Construcción (ICSC, MITMS), base 2015, medias anuales 2005-2023 reindexadas a 2005 = 100: coste total de la edificación residencial (mano de obra + materiales), mano de obra, consumo de materiales de la edificación residencial, cemento, cerámica, acero y madera.
- **Fuentes**: Boletín estadístico online MITMS, sección 57 (base 2015): cuadro 1 (índice general, `mitms_57010000.xls`) y cuadros 2.1-2.2 de precios de materiales (`mitms_57020000.xls`, `mitms_57030000.xls`). Script: `graficas/scripts/n4b_indices_materiales.py`. Descarga: 2026-08-07.
- **Identificación de columnas** (los XLS de la base 2015 vienen sin rótulos): doble evidencia convergente. (1) El anexo oficial de productos de la base 2015 (`mitms_icsc_anexo_productos.pdf`, transportes.gob.es) enumera los 43 productos en orden fijo, que se reparte entre las tablas con exactamente las anchuras observadas (tabla 2.1 = productos 1-9; tabla 2.2 = productos 10-19; tabla 2.3 = productos 20-26). (2) Los cuadros homólogos de la base enero 2005 (`mitms_38010000/38020000/38030000.xls`) sí llevan rótulos y muestran el mismo orden. Validación interna: la media del año base es 100 (comprobado programáticamente, 2015 = 100 ± 0,002).
- **Advertencia metodológica**: la base 2015 (CNAE 2009) estima los precios de materiales a partir del IPRI del INE (`mitms_metodologia_icsc_base2015.pdf`); su tramo retropolado 2005-2012 NO coincide con las series de la base 2005 (divergencias de hasta ±20% en acero), por tratarse de una revisión metodológica y no de un mero cambio de base. Se usa exclusivamente la base 2015, que es la serie oficial vigente y es internamente homogénea. La serie termina en 2023 (último año publicado del ICSC en el boletín).
- Lectura clave: entre 2005 y 2023 la mano de obra subió un 39% y el coste total residencial un 51%, mientras el acero llegó a +176% en 2022 y el cemento a +66% en 2023 (crisis energética). El encarecimiento reciente de construir es de materiales, no salarial; y en todo caso queda a un orden de magnitud de la revalorización del activo documentada en G1/G3.

## N5_espana_precio_suelo_anual.csv (precio del suelo urbano)

- **Series**: precio medio del m² de suelo urbano en transacciones, total nacional y municipios de más de 50.000 habitantes. Medias anuales de datos trimestrales (solo años completos), 2004-2025.
- **Fuente**: Estadística de Precios de Suelo Urbano (MITMS/MIVAU), Boletín estadístico online, cuadros 4 y 4.5 (sedal 36400500 y 36403000). Descargado 2026-08-07. Script: `graficas/scripts/n_series_boletin_mitms.py`.
- **Advertencia de composición**: es precio medio de lo TRANSACCIONADO cada año (la mezcla de ubicaciones y calidades varía con el ciclo); la caída posterior a 2007 en municipios grandes refleja también el desplazamiento de las transacciones hacia suelos peores. No existe estadística oficial anterior a 2004.

## N6_espana_iniciadas_por_decadas.csv y N6_espana_terminadas_anual.csv (viviendas construidas por décadas)

- **Series**: (a) viviendas iniciadas libres y protegidas agregadas por décadas 1976-2025 (de las series mensuales BdE/MIVAU ya documentadas en G8a; solo años con 12 meses); (b) viviendas terminadas anuales 1991-2025: libres (cuadro 3.2 del Boletín, sedal 32201000) y VPO (calificaciones definitivas, cuadro 1.6, sedal 31306000 — la nota oficial de la tabla indica que es la serie antes titulada «viviendas protegidas terminadas»).
- **Fuente**: Mº de Vivienda y Agenda Urbana / MITMS, Boletín estadístico online. Script: `graficas/scripts/n_series_boletin_mitms.py`.
- Lectura clave: la VPO fue el 71,8 % de lo iniciado en 1976-1985 (1,44 millones de viviendas) y es el 12,2 % en 2016-2025 (129.000).
