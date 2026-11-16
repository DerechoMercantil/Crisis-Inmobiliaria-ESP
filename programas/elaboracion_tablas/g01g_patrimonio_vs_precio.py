#!/usr/bin/env python3
"""Construye tablas/G01g_espana_patrimonio_vs_precio_vivienda_por_edad_2002_2024.csv: patrimonio
neto mediano de los hogares, por edad del cabeza de familia, en % del precio de la vivienda
tipo (93,75 m², misma serie de precio que G1c-G1f). Mide la barrera de entrada: una compra
exige aportar en torno al 30 % del precio (20 % de entrada no financiada y ~10 % de impuestos
y gastos).

- Patrimonio: Banco de España, Encuesta Financiera de las Familias (olas 2002-2024), mediana
  de la riqueza neta en euros constantes de 2024 (ficheros eff_*.xlsx).
- Precio: precio_vivienda_tipo() de g01c_renta_joven.py (tasación hasta 2007; IPV del INE
  desde 2008), llevado a euros de 2024 con el IPC (BIS, long CPI España, media anual).
"""
import csv, os
from collections import defaultdict
import openpyxl
from g01c_renta_joven import BASE, BR, T, precio_vivienda_tipo

COHORTES = [('menor_35', 'Menor de 35'), ('35_44', 'Entre 35 y 44'), ('55_64', 'Entre 55 y 64'),
            ('65_74', 'Entre 65 y 74'), ('todos', 'TODOS LOS HOGARES')]


def eff(fichero):
    filas = [r for r in openpyxl.load_workbook(os.path.join(BR, fichero), read_only=True).worksheets[0]
             .iter_rows(values_only=True)]
    cab = next(r for r in filas if r and any(isinstance(x, str) and ('Entre' in x or 'TODOS' in x) for x in r))
    cab = [c for c in cab if c is not None]
    datos = {}
    for r in filas:
        r = [x for x in r if x is not None]
        if r and str(r[0]).isdigit():
            datos[int(r[0])] = dict(zip(cab, [float(x) * 1000 for x in r[1:]]))
    return datos


def ipc_anual():
    d = defaultdict(list)
    with open(os.path.join(BASE, 'datos', 'procesados', 'bis_ipc_mensual.csv')) as f:
        for r in csv.DictReader(f):
            if r['area'] == 'ES':
                d[int(r['mes'][:4])].append(float(r['indice_2010_100']))
    return {a: sum(v) / len(v) for a, v in d.items() if len(v) == 12}


def main():
    riqueza = eff('eff_riqueza_neta_mediana_por_edad.xlsx')
    todos = eff('eff_riqueza_neta_mediana_todos.xlsx')
    ipc = ipc_anual()
    precio, precio_tas = precio_vivienda_tipo(), precio_vivienda_tipo('tasacion')
    salida = os.path.join(T, 'G01g_espana_patrimonio_vs_precio_vivienda_por_edad_2002_2024.csv')
    with open(salida, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['anio_ola_eff', 'precio_vivienda_tipo_eur_2024']
                   + [f'patrimonio_mediano_{c}_eur_2024' for c, _ in COHORTES]
                   + [f'patrimonio_{c}_pct_precio' for c, _ in COHORTES]
                   + [f'patrimonio_{c}_pct_precio_tasacion' for c, _ in COHORTES])
        for a in sorted(riqueza):
            fila = dict(riqueza[a], **todos[a])
            p = precio[a] * ipc[2024] / ipc[a]
            pt = precio_tas[a] * ipc[2024] / ipc[a]
            pat = [fila[col] for _, col in COHORTES]
            w.writerow([a, round(p)] + [round(x) for x in pat] + [round(100 * x / p, 1) for x in pat]
                       + [round(100 * x / pt, 1) for x in pat])
    print('Escrito', salida)


if __name__ == '__main__':
    main()
