#!/usr/bin/env python3
"""N4b: Índice de Costes del Sector de la Construcción (ICSC, MITMS) por componentes.

Los cuadros de la base 2015 (57xxxxxx, serie anual 2005-2023) llegan sin rótulos de
columna. La identificación de columnas se apoya en dos evidencias convergentes:
  1. El anexo oficial de productos de la base 2015 (`mitms_icsc_anexo_productos.pdf`)
     enumera los 43 productos en un orden fijo que se reparte entre las tablas de
     «precios y materiales diversos» exactamente con las anchuras observadas:
     tabla 2.1 = ids 1-9 (9 columnas: áridos, cemento, cal, hormigón, mortero,
     cerámica, prefabricados, yeso, derivados del yeso); tabla 2.2 = ids 10-19
     (10 columnas: acero, madera, sintéticos, asfálticos, caucho, vidrio plano,
     vidrio hueco, carpintería de madera, carpintería metálica, herrajes);
     tabla 2.3 = ids 20-26 (7 columnas).
  2. Los cuadros homólogos de la base enero 2005 (38xxxxxx) SÍ llevan rótulos y
     presentan el mismo orden de columnas.
Nota: las series 2005-2012 de la base 2015 NO coinciden con las de la base 2005
(la base 2015 retropola desde el IPRI del INE; es una revisión metodológica, no un
mero cambio de base), por lo que aquí se usa exclusivamente la base 2015.
Validación interna: la media del año base debe ser 100 (2015 = 100 ± 0,1).
Salida: tablas/N4b_espana_indices_costes_materiales.csv, reindexado a 2005 = 100.
"""
import csv, os
import xlrd

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
BRUTOS = os.path.join(BASE, 'datos', 'brutos')

ANCHURAS_ESPERADAS = {  # PERIODO + columnas de producto según el anexo de la base 2015
    'mitms_57020000.xls': 10,
    'mitms_57030000.xls': 11,
    'mitms_57010000.xls': 14,  # índice general: 6 tipos de obra x 2 ponderaciones + mano de obra
}


def serie_anual(fichero, col):
    """Filas anuales: col 0 es el año en float (los bloques mensuales usan texto)."""
    sh = xlrd.open_workbook(os.path.join(BRUTOS, fichero)).sheet_by_index(0)
    if sh.ncols != ANCHURAS_ESPERADAS[fichero]:
        raise ValueError(f'{fichero}: {sh.ncols} columnas, se esperaban '
                         f'{ANCHURAS_ESPERADAS[fichero]} — revisar mapeo')
    out = {}
    for r in range(sh.nrows):
        a = sh.cell_value(r, 0)
        if isinstance(a, float) and 1980 <= a <= 2030:
            v = sh.cell_value(r, col)
            if isinstance(v, float):
                if int(a) in out:
                    raise ValueError(f'{fichero}: año {int(a)} duplicado')
                out[int(a)] = v
    return out


SERIES = [
    # nombre, fichero base 2015, columna
    ('coste_total_residencial', 'mitms_57010000.xls', 2),
    ('mano_de_obra',            'mitms_57010000.xls', 7),
    ('materiales_residencial',  'mitms_57010000.xls', 9),
    ('cemento',                 'mitms_57020000.xls', 2),
    ('ceramica',                'mitms_57020000.xls', 6),
    ('acero',                   'mitms_57030000.xls', 1),
    ('madera',                  'mitms_57030000.xls', 2),
]

datos = {}
for nombre, f15, col in SERIES:
    s15 = serie_anual(f15, col)
    if abs(s15[2015] - 100) > 0.1:
        raise ValueError(f'{nombre}: el año base 2015 vale {s15[2015]:.3f}, no 100')
    print(f'  {nombre}: 2005-2023 leída, base 2015 = {s15[2015]:.3f}')
    datos[nombre] = s15

anios = sorted(set.intersection(*(set(v) for v in datos.values())))
assert anios[0] == 2005, anios
salida = os.path.join(BASE, 'tablas', 'N4b_espana_indices_costes_materiales.csv')
with open(salida, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['anio'] + [n for n, *_ in SERIES])
    for a in anios:
        w.writerow([a] + [round(datos[n][a] / datos[n][2005] * 100, 2)
                          for n, *_ in SERIES])
print(f'{salida}: {anios[0]}-{anios[-1]} ({len(anios)} años), índices 2005=100')
