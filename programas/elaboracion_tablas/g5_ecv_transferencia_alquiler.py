#!/usr/bin/env python3
"""G5: Transferencia intergeneracional del alquiler (sincrónica, España).
Fuente: microdatos ECV 2025 (INE), ecv_b2013/datos_2025.zip.
- Lado pagador: HH060 (alquiler mensual actual) x12, hogares con HH021 en (3,4).
- Lado perceptor: HY040G (renta bruta anual por alquiler de propiedades, año fiscal 2024).
- Edad: del responsable 1 de la vivienda (HB080 -> RB080 fichero R). Pesos: DB090.
- El residuo pagado-cobrado = alquiler a personas jurídicas, no declarado y otros.
"""
import csv, collections, os
BASE = os.path.join(os.path.dirname(__file__), '../../datos/brutos/ecv_2025/CSV')

pesos = {r['DB030']: float(r['DB090'] or 0) for r in csv.DictReader(open(f'{BASE}/esudb25d.csv'))}
nacim = {r['RB030']: r.get('RB080','') for r in csv.DictReader(open(f'{BASE}/esudb25r.csv'))}
def bracket(e): return '16-29' if e<30 else '30-44' if e<45 else '45-64' if e<65 else '65+'

paga, cobra = collections.Counter(), collections.Counter()
n_paga, n_cobra = collections.Counter(), collections.Counter()
for row in csv.DictReader(open(f'{BASE}/esudb25h.csv')):
    w = pesos.get(row['HB030'], 0)
    anio = (nacim.get((row.get('HB080') or '').strip()) or '').strip()
    if not anio: continue
    br = bracket(2025 - int(float(anio)))
    if (row.get('HH021') or '').strip() in ('3','4'):
        try: rm = float(row.get('HH060') or 0)
        except ValueError: rm = 0
        if rm > 0: paga[br] += rm*12*w; n_paga[br] += w
    try: ra = float(row.get('HY040G') or 0)
    except ValueError: ra = 0
    if ra > 0: cobra[br] += ra*w; n_cobra[br] += w

out = os.path.join(os.path.dirname(__file__), '../../tablas/G05_espana_transferencia_alquiler_por_edad.csv')
with open(out, 'w') as f:
    w = csv.writer(f)
    w.writerow(['tramo_edad','alquiler_pagado_mill_eur','hogares_pagadores','alquiler_cobrado_mill_eur','hogares_perceptores'])
    for br in ['16-29','30-44','45-64','65+']:
        w.writerow([br, round(paga[br]/1e6), round(n_paga[br]), round(cobra[br]/1e6), round(n_cobra[br])])
    resid = (sum(paga.values())-sum(cobra.values()))/1e6
    w.writerow(['empresas_no_declarado_otros','', '', round(resid), ''])
    w.writerow(['TOTAL', round(sum(paga.values())/1e6), round(sum(n_paga.values())), round(sum(paga.values())/1e6), ''])
print('escrito', out)
