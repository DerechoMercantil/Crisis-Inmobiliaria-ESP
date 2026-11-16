#!/usr/bin/env python3
"""Construye tablas/G11_espana_hogares_vs_viviendas_terminadas_1971_2025.csv: viviendas
terminadas y hogares nuevos (variación anual del número de hogares) en España.

- Viviendas terminadas (libres + protegidas):
  1970-1990: OCDE, Main Economic Indicators, «Total dwellings and residential buildings
  constructed for Spain» (vía FRED, PRCNDW01ESA470N; media mensual × 12), que reproduce
  la estadística del Ministerio (D. G. para la Vivienda).
  1991-2025: Mº de Vivienda y Agenda Urbana, boletín estadístico: viviendas libres
  terminadas (tabla 32201000) + calificaciones definitivas de vivienda protegida,
  planes estatales y autonómicos (tabla 31306000).
- Hogares nuevos:
  1971-2001: promedio intercensal (censos INE de 1970, 1981, 1991 y 2001, viviendas
  principales; interpolación lineal por fechas censales).
  2002: Mº de Vivienda, estimación del parque de viviendas principales (tabla 33102000),
  anclada al censo de 2001.
  2003-2025: INE, EPA, número de hogares (media anual de los cuatro trimestres; base 2021),
  vía Banco de España SI_1_5.36.
  2021-2025, columna aparte (hogares_nuevos_ecp): INE, Estadística Continua de Población,
  tabla 60131, variación entre el 1 de enero de cada año y el del siguiente. Evita la
  ruptura de la EPA de 2021 (-47.725 / +332.125).
"""
import csv, datetime as dt, os
import openpyxl, xlrd

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
BR = os.path.join(BASE, 'datos', 'brutos')
CENSOS = {dt.date(1970, 12, 31): 8505251, dt.date(1981, 3, 1): 10431327,
          dt.date(1991, 3, 1): 11736376, dt.date(2001, 11, 1): 14187169}


def total_nacional_xls(codigo):
    sh = xlrd.open_workbook(os.path.join(BR, 'mivau_boletin', f'mivau_{codigo}.xls')).sheets()[0]
    anios = None
    for i in range(sh.nrows):
        fila = sh.row_values(i)
        vals = [x for x in fila if x != '']
        if vals and all(isinstance(x, float) and 1900 < x < 2100 for x in vals):
            anios = fila
        if any(str(x).strip().upper().startswith('TOTAL NAC') for x in fila[:3]):
            return {int(a): v for a, v in zip(anios, fila) if isinstance(a, float) and a > 1900 and v != ''}


def principales_mivau():
    filas = list(openpyxl.load_workbook(os.path.join(BR, 'mivau_boletin', 'mivau_33102000.xlsx'),
                                        read_only=True)['Tabla 2'].iter_rows(values_only=True))
    anios = next(f for f in filas if f and any(str(x) == '2001' for x in f))
    sub = next(f for f in filas if f and any(str(x).startswith('Principales') for x in f if x))
    tot = next(f for f in filas if f and any(str(x).strip().upper().startswith('TOTAL NAC') for x in f if x))
    out, actual = {}, None
    for a, s, v in zip(anios, sub, tot):
        if a is not None and str(a).isdigit():
            actual = int(a)
        if actual and s and str(s).startswith('Principal') and v:
            out[actual] = int(v)
    return out


def hogares_censo(d):
    fechas = sorted(CENSOS)
    tramos = list(zip(fechas, fechas[1:]))
    a, b = next(((a, b) for a, b in tramos if a <= d <= b), tramos[-1])
    t = (d - a).days / (b - a).days
    return CENSOS[a] + (CENSOS[b] - CENSOS[a]) * t


def hogares_epa():
    filas = list(csv.reader(open(os.path.join(BR, 'bde_si_1_5.csv'), encoding='latin1')))
    j = filas[2].index('SI_1_5.36')
    trim = {}
    for f in filas[6:]:
        if f and f[0][-4:].isdigit() and j < len(f) and f[j] not in ('_', ''):
            trim.setdefault(int(f[0][-4:]), []).append(float(f[j]) * 1000)
    return {a: sum(v) / 4 for a, v in trim.items() if len(v) == 4}


def hogares_ecp():
    with open(os.path.join(BR, 'ine_ecp', 'ine_60131_hogares_total_nacional.csv')) as f:
        ene = {int(r['fecha'][:4]): int(r['hogares']) for r in csv.DictReader(f) if r['fecha'].endswith('-01-01')}
    return {a: ene[a + 1] - ene[a] for a in ene if a + 1 in ene}


def main():
    terminadas = {}
    with open(os.path.join(BR, 'oecd_fred_viviendas_terminadas_esp_PRCNDW01ESA470N.csv')) as f:
        for r in csv.DictReader(f):
            a = int(r['observation_date'][:4])
            if a <= 1990:
                terminadas[a] = (round(float(r['PRCNDW01ESA470N']) * 12), 'OCDE MEI (estadística del Ministerio)')
    libres, protegidas = total_nacional_xls('32201000'), total_nacional_xls('31306000')
    for a in libres:
        terminadas[a] = (round(libres[a] + protegidas[a]), 'MIVAU: libres terminadas + calificaciones definitivas')

    epa, princ = hogares_epa(), principales_mivau()
    hogares = {}
    for a in range(1971, 2002):
        hogares[a] = (round(hogares_censo(dt.date(a, 12, 31)) - hogares_censo(dt.date(a - 1, 12, 31))),
                      'promedio intercensal (censos INE)')
    hogares[2002] = (princ[2002] - princ[2001], 'MIVAU: parque de viviendas principales')
    for a in range(2003, max(epa) + 1):
        hogares[a] = (round(epa[a] - epa[a - 1]), 'INE EPA: hogares, media anual')

    ecp = hogares_ecp()
    salida = os.path.join(BASE, 'tablas', 'G11_espana_hogares_vs_viviendas_terminadas_1971_2025.csv')
    with open(salida, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['anio', 'viviendas_terminadas', 'hogares_nuevos', 'saldo_viviendas_menos_hogares',
                    'fuente_viviendas', 'fuente_hogares', 'hogares_nuevos_ecp'])
        for a in range(1971, max(hogares) + 1):
            v, fv = terminadas[a]
            h, fh = hogares[a]
            w.writerow([a, v, h, v - h, fv, fh, ecp.get(a, '')])
    print('Escrito', salida)


if __name__ == '__main__':
    main()
