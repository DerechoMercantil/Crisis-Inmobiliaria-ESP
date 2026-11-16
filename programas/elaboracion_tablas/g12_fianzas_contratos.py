#!/usr/bin/env python3
"""Construye las tablas G12 de contratos de alquiler registrados en los depósitos autonómicos de fianzas:

- tablas/G12_contratos_alquiler_fianzas_trimestral.csv (2016 T1 - 2026 T1)
- tablas/G12b_contratos_alquiler_fianzas_anual.csv (2005-2025)

Fuentes (descarga del 7-10-2026, ficheros en datos/brutos/fianzas/):
- Cataluña: Incasòl, Registre de fiances, vía Dades Obertes de la Generalitat, conjunto qww9-bvhh
  («Preu mitjà del lloguer d'habitatges per municipi»). Contratos dados de alta en el registro de
  fianzas en el periodo (fecha de alta de la fianza). Los totales de Cataluña y de Barcelona ciudad se
  obtienen sumando municipios: el total «Catalunya» del conjunto supramunicipal hepw-33ik da 80.309
  contratos en 2025, cifra incompatible con sus propios trimestres (suma 108.057) y con la suma
  municipal (108.057). Las rentas medias trimestrales de Cataluña sí se toman de hepw-33ik.
  Trimestres disponibles desde 2019; antes, solo años (2005-2006 de hepw-33ik; 2007- de qww9-bvhh).
- Euskadi: Gobierno Vasco, Estadística del Mercado de Alquiler (EMAL), tablas T1.1/T1.2 (trimestral)
  y T2.1/T2.2 (anual): fianzas de contratos de alquiler libre de vivienda habitual en vivienda
  colectiva, según trimestre o año de INICIO del contrato.
"""
import csv, os
import openpyxl
import pandas as pd

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
BR = os.path.join(BASE, 'datos', 'brutos', 'fianzas')
TRIM = {'gener-març': 1, 'abril-juny': 2, 'juliol-setembre': 3, 'octubre-desembre': 4}


def cataluna():
    m = pd.read_csv(os.path.join(BR, 'incasol_qww9-bvhh_municipis.csv'), dtype={'Codi territorial': str})
    s = pd.read_csv(os.path.join(BR, 'incasol_hepw-33ik_supramunicipal.csv'), dtype={'Codi territorial': str})
    trim = {}
    for (a, p), g in m[m['Període'].isin(TRIM)].groupby(['Any', 'Període']):
        bcn = g.loc[g['Codi territorial'] == '08019', 'Habitatges'].sum()
        trim[(int(a), TRIM[p])] = {'cataluna_contratos': int(g['Habitatges'].sum()),
                                   'barcelona_contratos': int(bcn)}
    cat = s[s['Àmbit territorial'] == 'Catalunya']
    for _, r in cat[cat['Període'].isin(TRIM)].iterrows():
        k = (int(r['Any']), TRIM[r['Període']])
        if k in trim and pd.notna(r['Renda']):
            trim[k]['cataluna_renta_media'] = round(float(r['Renda']), 2)
    anual = {}
    for a, g in m[m['Període'] == 'gener-desembre'].groupby('Any'):
        anual[int(a)] = {'cataluna_contratos': int(g['Habitatges'].sum()),
                         'barcelona_contratos': int(g.loc[g['Codi territorial'] == '08019', 'Habitatges'].sum())}
    for _, r in cat[cat['Període'] == 'gener-desembre'].iterrows():
        a = int(r['Any'])
        if a not in anual:  # 2005-2006: solo en el conjunto supramunicipal
            anual[a] = {'cataluna_contratos': int(r['Habitatges'])}
    return trim, anual


def fila_euskadi(ws):
    filas = list(ws.iter_rows(values_only=True))
    datos = next(f for f in filas if f and f[0] == 'Euskadi')
    return list(datos[2:])  # columnas A-B: rótulos


def euskadi():
    wb = openpyxl.load_workbook(os.path.join(BR, 'emal_2016_2025_vivienda.xlsx'), read_only=True, data_only=True)
    n_t, r_t = fila_euskadi(wb['T1.1']), fila_euskadi(wb['T1.2'])
    n_a, r_a = fila_euskadi(wb['T2.1']), fila_euskadi(wb['T2.2'])
    trim, anual = {}, {}
    for i in range(40):  # 2016 T1 - 2025 T4; las columnas siguientes son contratos vigentes
        trim[(2016 + i // 4, i % 4 + 1)] = {'euskadi_contratos': int(n_t[i]), 'euskadi_renta_media': round(float(r_t[i]), 2)}
    for i in range(10):  # 2016-2025
        anual[2016 + i] = {'euskadi_contratos': int(n_a[i]), 'euskadi_renta_media': round(float(r_a[i]), 2)}
    return trim, anual


def escribir(nombre, claves, filas, cols, clave_cols):
    with open(os.path.join(BASE, 'tablas', nombre), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(clave_cols + cols)
        for k in claves:
            d = filas.get(k, {})
            w.writerow(list(k if isinstance(k, tuple) else (k,)) + [d.get(c, '') for c in cols])
    print('Escrito', nombre)


def main():
    ct, ca = cataluna()
    et, ea = euskadi()
    trim = {}
    for src in (ct, et):
        for k, v in src.items():
            if k[0] >= 2016:
                trim.setdefault(k, {}).update(v)
    for k, v in trim.items():
        v['trimestre'] = f'{k[0]}-T{k[1]}'
    cols_t = ['cataluna_contratos', 'barcelona_contratos', 'euskadi_contratos', 'cataluna_renta_media', 'euskadi_renta_media']
    claves = sorted(trim)
    with open(os.path.join(BASE, 'tablas', 'G12_contratos_alquiler_fianzas_trimestral.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['trimestre', 'anio', 'trim'] + cols_t)
        for k in claves:
            w.writerow([trim[k]['trimestre'], k[0], k[1]] + [trim[k].get(c, '') for c in cols_t])
    print('Escrito G12_contratos_alquiler_fianzas_trimestral.csv')
    anual = {}
    for src in (ca, ea):
        for k, v in src.items():
            anual.setdefault(k, {}).update(v)
    escribir('G12b_contratos_alquiler_fianzas_anual.csv', sorted(anual), anual,
             ['cataluna_contratos', 'barcelona_contratos', 'euskadi_contratos', 'euskadi_renta_media'], ['anio'])


if __name__ == '__main__':
    main()
