#!/usr/bin/env python3
"""G1bis: extiende la ratio precio/renta de G1 hasta 1971 mediante retropolación
académica del tramo 1971-1986 (la serie oficial del BdE arranca en 1987).

Numerador: precio del m² de 1987 (tabla G1b) retropolado con el índice nominal
del BIS (Selected residential property prices, España) x 93,75 m².
Denominador: renta del hogar mediano de 1987 (tabla G1b) retropolada con la
NNDI nominal por hogar de Prados de la Escosura / hogares censales INE —
mismo método ya aprobado y usado para el denominador 1979-1986 de G10.

Añade una columna de contraste con el price-to-income de la OCDE (por
persona, no por hogar), encadenada en 1987, para mostrar hasta qué punto
difieren ambos conceptos de renta.
"""
import csv, collections, statistics, os
import openpyxl

BASE = os.path.join(os.path.dirname(__file__), '..', '..')
BRUTOS = os.path.join(BASE, 'datos', 'brutos')
TABLAS = os.path.join(BASE, 'tablas')

# --- valores base de 1987, tomados de la tabla G1b (ya validada) ---
g1b_1987 = next(r for r in csv.DictReader(open(os.path.join(TABLAS, 'G1b_espana_precio_vs_renta_indexado.csv')))
                if r['anio'] == '1987')
PRECIO_87 = float(g1b_1987['precio_m2_eur'])       # 327 €/m²
RBD_87 = float(g1b_1987['rbd_hogar_mediano_eur'])  # 9.913 €
SUPERFICIE = 93.75

# --- BIS, Selected residential property prices, España, índice nominal ---
rows = list(csv.DictReader(open(os.path.join(BRUTOS, 'bis_spp.csv'))))
byy = collections.defaultdict(list)
for r in rows:
    if r['REF_AREA'] == 'ES' and r['VALUE'] == 'N' and r['OBS_VALUE']:
        byy[int(r['TIME_PERIOD'][:4])].append(float(r['OBS_VALUE']))
bis = {y: statistics.mean(v) for y, v in byy.items()}

# --- Prados de la Escosura, NNDI nominal (Tabla 2, col. 7) ---
wb = openpyxl.load_workbook(os.path.join(BRUTOS, 'prados_chn_1850_2024.xlsx'), read_only=True)
ws = wb['Table 2']
nndi = {}
for row in ws.iter_rows(min_row=7, values_only=True):
    if row[0] is None:
        continue
    try:
        y = int(row[0])
    except (TypeError, ValueError):
        continue
    if row[7] is not None:
        nndi[y] = float(row[7])

# --- hogares censales INE (viviendas principales), interpolación log-lineal ---
CENSOS = {1970: 8505251, 1981: 10431327, 1991: 11736376}


def hogares(y):
    if y <= 1981:
        a, b, ya, yb = CENSOS[1970], CENSOS[1981], 1970, 1981
    else:
        a, b, ya, yb = CENSOS[1981], CENSOS[1991], 1981, 1991
    return a * (b / a) ** ((y - ya) / (yb - ya))


bis_87 = bis[1987]
nndi_hogar_87 = nndi[1987] / hogares(1987)

# --- OCDE price-to-income (por persona), para la columna de contraste ---
oecd_rows = list(csv.DictReader(open(os.path.join(BRUTOS, 'oecd_price_income_all.csv'))))
oecd_byy = collections.defaultdict(list)
for r in oecd_rows:
    if r['REF_AREA'] == 'ESP' and r['OBS_VALUE']:
        oecd_byy[int(r['TIME_PERIOD'][:4])].append(float(r['OBS_VALUE']))
oecd = {y: statistics.mean(v) for y, v in oecd_byy.items()}
oecd_87 = oecd[1987]
ratio_87 = 3.09  # ratio oficial BdE de 1987 (tabla G1), ancla de la cadena OCDE

retro = {}
contraste_ocde = {}
for y in range(1971, 1987):
    precio = PRECIO_87 * bis[y] / bis_87
    nndi_hogar_y = nndi[y] / hogares(y)
    rbd = RBD_87 * nndi_hogar_y / nndi_hogar_87
    retro[y] = round(precio * SUPERFICIE / rbd, 2)
    contraste_ocde[y] = round(oecd[y] / oecd_87 * ratio_87, 2)

oficial = {int(r['anio']): float(r['precio_vivienda_en_anios_de_rbd_hogar_mediano'])
           for r in csv.DictReader(open(os.path.join(TABLAS, 'G1_espana_ratio_precio_rbd_anual.csv')))}

out = os.path.join(TABLAS, 'G1bis_espana_ratio_precio_rbd_anual_1971.csv')
with open(out, 'w') as f:
    w = csv.writer(f)
    w.writerow(['anio', 'precio_vivienda_en_anios_de_rbd_hogar_mediano', 'metodo', 'ratio_contraste_ocde'])
    for y in range(1971, 1987):
        w.writerow([y, retro[y], 'retropolación académica (BIS + Prados NNDI/hogar)', contraste_ocde[y]])
    for y in sorted(oficial):
        w.writerow([y, oficial[y], 'serie oficial BdE', ''])
print(f'escrito {out}')
