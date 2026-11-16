"""Construye tablas/G18_espana_umbral_renta_acceso_compra_2004_2024.csv.

Responde a la pregunta «¿qué salario neto mensual tiene, de forma mayoritaria, quien
hoy no puede comprar vivienda?» con un umbral de acceso explícito y la ECV.

Umbral de acceso (condición de flujo):
- Cuota anual de una hipoteca por el 80 % de la vivienda tipo de la monografía
  (93,75 m²; precio de compraventa del INE desde 2008, tabla G1c) con las condiciones
  de préstamo del Banco de España de cada año: cuota = 0,8 × precio × F, donde F es la
  cuota anual por euro prestado implícita en SI_1_5.43-44 (tabla G1f).
- Renta neta anual mínima = cuota / 0,30 (umbral de esfuerzo del 30 %, el de las
  recomendaciones internacionales y del Consejo de la Juventud); variante al 35 %.
- No incluye la condición de patrimonio (entrada del 20 % más un 10 % de impuestos y
  gastos), que se da aparte: la mayoría de quienes superan el umbral de renta tampoco
  tendría la entrada (iteraciones 2-5).

Población (ECV, microdatos INE; renta del año anterior a la encuesta):
- Asalariados de 18 a 64 años con salario neto (PY010N) > 0 y, aparte, los de 25 a 34. Variante
  «a tiempo completo todo el año» (12 meses a tiempo completo: PL070 hasta 2008, PL073 desde
  2009), más cercana a la idea de nómina mensual; sin ella, el salario anual incluye a quien
  trabajó solo parte del año o a tiempo parcial.
  Salario mensual = anual / 12 (equivale a una nómina en 12 pagas; en 14 pagas, × 12/14).
- Hogares (renta disponible del hogar HY020), por si la compra se plantea en pareja.
- Cambio de base de 2008: rentas de 2004-2007 enlazadas con k_mediana = 1,024 (personas,
  g1e_enlace_ecv_bases.json) y k_hogar = 1,146 (hogares, g1c_enlace_ecv_bases.json).
- Euros corrientes del año de renta y euros constantes de 2024 (IPC de España, BIS).
"""
import csv, json, os
import g13_tenencia_hipoteca_por_edad as g13
from g14_alquiler_ahorro_por_edad import ipc_anual, wmediana

B = g13.BASE
K_PER = json.load(open(os.path.join(B, 'datos', 'procesados', 'g1e_enlace_ecv_bases.json')))['k_mediana']
K_HOG = json.load(open(os.path.join(B, 'datos', 'procesados', 'g1c_enlace_ecv_bases.json')))['k_hogar']


def series():
    precio = {int(r['anio']): float(r['precio_vivienda_tipo_eur'])
              for r in csv.DictReader(open(os.path.join(g13.T, 'G01c_espana_ratio_precio_renta_joven_1980_2024.csv')))}
    f = {int(r['anio']): float(r['cuota_anual_por_euro_prestado'])
         for r in csv.DictReader(open(os.path.join(g13.T, 'G01f_espana_esfuerzo_teorico_por_edad_1987_2024.csv')))}
    return precio, f


def main():
    precio, f = series(); ipc = ipc_anual(); filas = []
    for enc in range(2005, 2026):
        y = enc - 1
        cuota = 0.8 * precio[y] * f[y]
        u30, u35 = cuota / 0.30, cuota / 0.35
        kp, kh = (K_PER, K_HOG) if enc < 2008 else (1.0, 1.0)
        defl = ipc[2024] / ipc[y]
        asal = []
        for r in g13.leer(enc, 'p'):
            nac, s = g13.fl(r['PB140']), g13.fl(r['PY010N'])
            if nac is None or not s or s <= 0:
                continue
            e = enc - int(nac)
            if 18 <= e <= 64:
                meses = g13.fl(r.get('PL073') if 'PL073' in r else r.get('PL070'))
                asal.append((s * kp, g13.fl(r['PB040']) or 0, e, meses == 12))
        peso = {r['DB030']: g13.fl(r['DB090']) or 0 for r in g13.leer(enc, 'd')}
        hog = [(g13.fl(r['HY020']) * kh, peso.get(r['HB030'].strip(), 0)) for r in g13.leer(enc, 'h')
               if g13.fl(r['HY020']) is not None and peso.get(r['HB030'].strip())]
        fila = dict(anio_renta=y, encuesta=f'ECV {enc}', precio_vivienda_tipo_eur=round(precio[y]),
                    cuota_mensual_hipoteca_80pct_eur=round(cuota / 12),
                    entrada_y_gastos_30pct_eur=round(0.3 * precio[y]),
                    umbral_renta_neta_mensual_30pct_eur=round(u30 / 12),
                    umbral_renta_neta_mensual_35pct_eur=round(u35 / 12))
        grupos = (('asalariados_18_64', asal), ('asalariados_25_34', [a for a in asal if 25 <= a[2] <= 34]),
                  ('asalariados_tc_todo_el_anio_18_64', [a for a in asal if a[3]]),
                  ('asalariados_tc_todo_el_anio_25_34', [a for a in asal if a[3] and 25 <= a[2] <= 34]))
        for nombre, sel in grupos:
            sel = [a[:3] for a in sel]
            tot = sum(w for _, w, _ in sel)
            bajo = [(s, w) for s, w, _ in sel if s < u30]
            fila[f'{nombre}_pct_bajo_umbral30'] = round(100 * sum(w for _, w in bajo) / tot, 1)
            fila[f'{nombre}_pct_bajo_umbral35'] = round(100 * sum(w for s, w, _ in sel if s < u35) / tot, 1)
            fila[f'{nombre}_salario_mensual_mediano_bajo_umbral30_eur'] = round(wmediana(bajo) / 12)
            fila[f'{nombre}_salario_mensual_mediano_bajo_umbral30_eur2024'] = round(wmediana(bajo) / 12 * defl)
            fila[f'{nombre}_salario_mensual_mediano_todos_eur'] = round(wmediana([(s, w) for s, w, _ in sel]) / 12)
        tot = sum(w for _, w in hog); bajo = [(v, w) for v, w in hog if v < u30]
        fila['hogares_pct_bajo_umbral30'] = round(100 * sum(w for _, w in bajo) / tot, 1)
        fila['hogares_renta_mensual_mediana_bajo_umbral30_eur'] = round(wmediana(bajo) / 12)
        fila['umbral_renta_neta_mensual_30pct_eur2024'] = round(u30 / 12 * defl)
        filas.append(fila)
        print(y, fila['umbral_renta_neta_mensual_30pct_eur'],
              *[(fila[f'{g}_pct_bajo_umbral30'], fila[f'{g}_salario_mensual_mediano_bajo_umbral30_eur'],
                 fila[f'{g}_salario_mensual_mediano_todos_eur']) for g, _ in grupos],
              fila['hogares_pct_bajo_umbral30'], fila['hogares_renta_mensual_mediana_bajo_umbral30_eur'])
    with open(os.path.join(g13.T, 'G18_espana_umbral_renta_acceso_compra_2004_2024.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0])); w.writeheader(); w.writerows(filas)


if __name__ == '__main__':
    main()
