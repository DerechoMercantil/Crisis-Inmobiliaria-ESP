#!/usr/bin/env python3
"""Construye tablas/G01bis_espana_ratio_precio_rbd_anual_1971.csv: la ratio oficial
del BdE (1987-) retropolada a 1971-1986.

Método del tramo 1971-1986 (coherente con el denominador académico de G10):
- Numerador: precio del m² de vivienda (327 €/m², Fomento 1987, tabla G1b)
  retropolado con el índice nominal del BIS (WS_SPP, serie de España) × 93,75 m².
- Denominador: renta bruta del hogar mediano (9.913 €, 1987, implícita en la serie
  BdE) retropolada con la NNDI nominal por hogar: NNDI de Prados de la Escosura
  (Tabla 2) / hogares (viviendas principales censales INE 1970-1981-1991,
  interpolación log-lineal). Reproduce exactamente la renta 1979-86 de G10.
- Columna de contraste: la misma ratio retropolada con el price-to-income de la
  OCDE (renta por persona, no por hogar); diferencia máxima 0,25 años.
"""
import csv, math, os
from collections import defaultdict
import openpyxl

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = os.path.join(BASE, 'datos', 'procesados')
B = os.path.join(BASE, 'datos', 'brutos')
T = os.path.join(BASE, 'tablas')

PRECIO_M2_1987 = 327      # €/m², Fomento base 1987 (tabla G1b)
RENTA_1987 = 9913         # €, renta bruta hogar mediano implícita BdE (tabla G1b)
RATIO_1987 = 3.09         # años de renta (tabla G1)
CENSOS = {1970: 8505251, 1981: 10431327, 1991: 11736376}  # viviendas principales INE


def media_anual(fichero, filtro):
    d = defaultdict(list)
    with open(os.path.join(P, fichero)) as f:
        for r in csv.DictReader(f):
            if filtro(r):
                d[int(r['trimestre'][:4])].append(float(r[list(r)[-1]]))
    return {y: sum(v) / len(v) for y, v in d.items()}


bis = media_anual('bis_precios_vivienda_trimestral.csv',
                  lambda r: r['area'] == 'ES' and r['nominal_real'] == 'N')
oecd = media_anual('oecd_price_income_trimestral.csv', lambda r: r['area'] == 'ESP')

wb = openpyxl.load_workbook(os.path.join(B, 'prados_chn_1850_2024.xlsx'), read_only=True)
nndi = {}
for r in wb['Table 2'].iter_rows(min_row=7, max_col=8, values_only=True):
    try:
        nndi[int(r[0])] = float(r[7])
    except (TypeError, ValueError):
        continue


def hogares(y):
    c0, c1 = (1970, 1981) if y <= 1981 else (1981, 1991)
    t = (y - c0) / (c1 - c0)
    return math.exp(math.log(CENSOS[c0]) * (1 - t) + math.log(CENSOS[c1]) * t)


nndi_ph = {y: nndi[y] * 1e6 / hogares(y) for y in range(1970, 1992)}

bde = {}
with open(os.path.join(T, 'G01_espana_ratio_precio_rbd_anual.csv')) as f:
    for r in csv.DictReader(f):
        if r['precio_vivienda_en_anios_de_rbd_hogar_mediano']:
            bde[int(r['anio'])] = float(r['precio_vivienda_en_anios_de_rbd_hogar_mediano'])

salida = os.path.join(T, 'G01bis_espana_ratio_precio_rbd_anual_1971.csv')
with open(salida, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['anio', 'precio_vivienda_en_anios_de_rbd_hogar_mediano', 'metodo',
                'ratio_contraste_ocde'])
    for y in range(1971, 1987):
        precio = PRECIO_M2_1987 * bis[y] / bis[1987] * 93.75
        renta = RENTA_1987 * nndi_ph[y] / nndi_ph[1987]
        contraste = RATIO_1987 * oecd[y] / oecd[1987]
        w.writerow([y, round(precio / renta, 2),
                    'retropolación académica (BIS + Prados NNDI/hogar)',
                    round(contraste, 2)])
    for y in sorted(bde):
        w.writerow([y, bde[y], 'serie oficial BdE', ''])
print('Escrito', salida)
