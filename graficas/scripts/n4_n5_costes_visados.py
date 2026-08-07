#!/usr/bin/env python3
"""N4/N5: coste de construcción residencial (PEM de visados) frente a precio
de venta, y residual suelo+márgenes, 1992-2025.

Fuentes:
- mitms_09010200.xls: visados de obra nueva, superficie a construir (m²),
  columna 'residencial' verificada por identidad contable (residencial =
  suma de sus 4 componentes). Boletín estadístico MITMS, cuadro 9.2. 1991-.
- mitms_09010300.xls: ídem, presupuesto de ejecución material (miles de
  euros), cuadro 9.3. El PEM excluye IVA, honorarios, gastos generales,
  beneficio del contratista y costes financieros y de suelo (definición de
  la nota metodológica oficial).
- Precio de venta €/m²: serie enlazada de G1b (Fomento base 1987 reproducida
  en Vergés 2012 + MIVAU 1995-), tabla G1b_espana_precio_vs_renta_indexado.csv.

Advertencia metodológica (consultada y aprobada por el equipo): el residual
precio de venta − PEM incluye suelo, márgenes y costes no-PEM; es una cota
superior de la repercusión del suelo, no el suelo aislado.

Se usa 1992 como primer año completo de visados (1991 es año de arranque
parcial de la estadística).
"""
import csv, os
import xlrd

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
BRUTOS = os.path.join(BASE, 'datos', 'brutos')
TABLAS = os.path.join(BASE, 'tablas')


def serie_anual_visados(nombre, col_anio):
    """Devuelve {año: (total, residencial)} sumando columna a columna.

    Estructura del XLS 'sedal': un bloque anual con los últimos 5 años y,
    debajo, un bloque por año (fila del año = diciembre + 11 filas con los
    meses restantes). Los años completos anteriores a ese bloque anual se
    reconstruyen sumando sus 12 meses; el bloque anual sirve de validación.
    """
    sh = xlrd.open_workbook(os.path.join(BRUTOS, f'mitms_{nombre}.xls')).sheet_by_index(0)
    MESES = {'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'}
    anual, mensual = {}, {}
    r = 0
    while r < sh.nrows:
        y = sh.cell_value(r, col_anio)
        if isinstance(y, float) and 1990 < y < 2027:
            y = int(y)
            etiqueta_mes = str(sh.cell_value(r, col_anio + 1)).strip()
            fila = [sh.cell_value(r, c) if isinstance(sh.cell_value(r, c), float) else 0.0
                    for c in range(col_anio + 2, sh.ncols)]
            if etiqueta_mes in MESES:
                # bloque mensual: esta fila y las siguientes con etiqueta de mes
                acum, n = fila[:], 1
                rr = r + 1
                def _mes(fila_idx):
                    a = str(sh.cell_value(fila_idx, col_anio)).strip().rstrip('.')
                    b = str(sh.cell_value(fila_idx, col_anio + 1)).strip().rstrip('.')
                    return (a in MESES) or (b in MESES and not a)
                while rr < sh.nrows and _mes(rr):
                    f2 = [sh.cell_value(rr, c) if isinstance(sh.cell_value(rr, c), float) else 0.0
                          for c in range(col_anio + 2, sh.ncols)]
                    acum = [a + b for a, b in zip(acum, f2)]
                    n += 1
                    rr += 1
                if n == 12:
                    mensual[y] = acum
                r = rr
                continue
            else:
                anual[y] = fila
        r += 1

    out = {}
    for y, fila in sorted({**mensual, **anual}.items()):
        vals = [v for v in fila if v]
        total, resid = vals[0], vals[1]
        if not (abs(sum(vals[2:5]) - resid) <= max(2.0, resid * 0.002)
                or abs(sum(vals[2:6]) - resid) <= max(2.0, resid * 0.002)):
            raise ValueError(f'{nombre}: identidad residencial no se cumple en {y}')
        if y in anual and y in mensual:
            suma_m = [v for v in mensual[y] if v]
            if abs(suma_m[0] - total) > total * 0.005:
                raise ValueError(f'{nombre}: suma de meses != anual en {y}')
        out[y] = (total, resid)
    return out


sup = serie_anual_visados('09010200', 0)   # m²
pem = serie_anual_visados('09010300', 1)   # miles de euros

precio_venta = {}
with open(os.path.join(TABLAS, 'G1b_espana_precio_vs_renta_indexado.csv')) as f:
    for r in csv.DictReader(f):
        precio_venta[int(r['anio'])] = float(r['precio_m2_eur'])

with open(os.path.join(TABLAS, 'N4_espana_coste_construccion_vs_precio.csv'), 'w') as f:
    w = csv.writer(f)
    w.writerow(['anio', 'pem_residencial_eur_m2', 'precio_venta_eur_m2',
                'pem_sobre_precio_pct', 'residual_suelo_margenes_eur_m2',
                'residual_sobre_precio_pct'])
    for y in sorted(set(sup) & set(pem)):
        if y < 1992:
            continue
        pem_m2 = pem[y][1] * 1000 / sup[y][1]
        pv = precio_venta.get(y)
        if pv:
            resid = pv - pem_m2
            w.writerow([y, round(pem_m2, 1), round(pv, 1),
                        round(100 * pem_m2 / pv, 1), round(resid, 1),
                        round(100 * resid / pv, 1)])
        else:
            w.writerow([y, round(pem_m2, 1), '', '', '', ''])

print('Tabla N4 generada.')
