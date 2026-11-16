"""Construye tablas/G14_espana_alquiler_y_colchon_ahorro_por_edad_2004_2025.csv
y tablas/G14b_espana_emancipacion_e_hipoteca_por_edad_simple.csv.

Contraste de la hipótesis «alquilar ya no permite ahorrar para la entrada», ECV
2004-2025 (microdatos INE). Reutiliza la lectura y la clasificación de tenencia de
g13_tenencia_hipoteca_por_edad.py.

G14, por edad de la persona responsable (HB080) y régimen de tenencia:
- pct_sin_colchon: hogares que no pueden afrontar un gasto imprevisto (HS060 = 2).
  Es la única pregunta de la ECV que mide directamente la existencia de ahorro
  disponible; el importe de referencia lo fija cada año el INE (en torno a una
  doceava parte del umbral de riesgo de pobreza anual).
- Solo inquilinos de mercado: esfuerzo en alquiler = 12 × HH060 (alquiler mensual
  vigente) / HY020 (renta disponible del año anterior); mediana y proporción por
  encima del 30 % y del 40 %; renta residual tras el alquiler por unidad de consumo
  (HX240), en euros de 2024 con el IPC de España (BIS, media anual del año de renta).
- La renta de 2004-2007 (base 2004, declarada) se multiplica por k_hogar = 1,146 para hacerla
  homogénea con la de base 2013 (registros fiscales); sin esa corrección el esfuerzo de 2004-2007
  queda sobrestimado en torno a un 15 %.

G14b, por edad simple (18-40), media de las olas 2005-2008 y 2022-2025:
- proporción de personas que son responsables de su vivienda (HB080) y proporción
  que es responsable de una vivienda en propiedad con hipoteca. Sirve para fijar a
  qué edad empieza a ser habitual el acceso a la propiedad con crédito.
"""
import csv, json, os
from collections import defaultdict
import g13_tenencia_hipoteca_por_edad as g13

# Cambio de base de la renta en 2008: la renta del hogar de base 2004 (2004-2007, declarada) es un 14,6 %
# inferior a la de base 2013 (registros fiscales) en el solape 2008-2012. Se corrige con k_hogar.
K_HOGAR = json.load(open(os.path.join(g13.BASE, 'datos', 'procesados', 'g1c_enlace_ecv_bases.json')))['k_hogar']

T = g13.T
TRAMOS = {'18-24': (18, 24), '25-34': (25, 34), '18-35': (18, 35), '35-44': (35, 44), 'todos': (16, 120)}


def ipc_anual():
    acc = defaultdict(list)
    with open(os.path.join(g13.BASE, 'datos', 'procesados', 'bis_ipc_mensual.csv')) as f:
        for r in csv.DictReader(f):
            if r['area'] == 'ES':
                acc[int(r['mes'][:4])].append(float(r['indice_2010_100']))
    return {y: sum(v) / len(v) for y, v in acc.items()}


def tenencia(r):
    if 'HH021' in r:
        return {'1': 'prop_sin', '2': 'prop_hip', '3': 'alq_mercado', '4': 'otros', '5': 'otros'}.get(r['HH021'].strip())
    hs = 'HS010_F' if 'HS010_F' in r else 'HS011_F'
    c = r['HH020'].strip()
    if c == '1':
        return 'prop_sin' if r[hs].strip() == '-2' else 'prop_hip'
    return {'2': 'alq_mercado', '3': 'otros', '4': 'otros'}.get(c)


def wmediana(pares):
    pares = sorted(pares); tot = sum(w for _, w in pares); acum = 0
    for v, w in pares:
        acum += w
        if acum >= tot / 2:
            return v


def ola(anio):
    peso = {r['DB030']: g13.fl(r['DB090']) or 0 for r in g13.leer(anio, 'd')}
    edad, wper = {}, {}
    for r in g13.leer(anio, 'p'):
        nac = g13.fl(r['PB140'])
        if nac is not None:
            edad[r['PB030'].strip()] = anio - int(nac)
            wper[r['PB030'].strip()] = g13.fl(r['PB040']) or 0
    hogares = []
    for r in g13.leer(anio, 'h'):
        w = peso.get(r['HB030'].strip(), 0); jefe = r['HB080'].strip()
        if not w or jefe not in edad:
            continue
        hogares.append(dict(edad=edad[jefe], jefe=jefe, w=w, ten=tenencia(r),
                            colchon=r['HS060'].strip(), alq=g13.fl(r['HH060']),
                            renta=(g13.fl(r['HY020']) or 0) * (K_HOGAR if anio < 2008 else 1) if r['HY020'].strip() else None,
                            uc=g13.fl(r['HX240'])))
    return hogares, edad, wper


def main():
    ipc = ipc_anual()
    filas = []
    simple = defaultdict(lambda: [0.0, 0.0, 0.0])   # (periodo, edad) -> [personas, jefes, jefes_hip]
    for anio in range(2004, 2026):
        hog, edad, wper = ola(anio)
        defl = ipc[2024] / ipc[anio - 1]   # renta del año anterior, en euros de 2024
        for nombre, (a, b) in TRAMOS.items():
            for ten in ('todos', 'alq_mercado', 'prop_hip'):
                sel = [h for h in hog if a <= h['edad'] <= b and (ten == 'todos' or h['ten'] == ten)
                       and h['colchon'] in ('1', '2')]
                tot = sum(h['w'] for h in sel)
                if not tot:
                    continue
                fila = dict(anio_encuesta=anio, tramo=nombre, tenencia=ten, n_muestra=len(sel),
                            pct_sin_colchon=round(100 * sum(h['w'] for h in sel if h['colchon'] == '2') / tot, 2))
                if ten == 'alq_mercado':
                    v = [h for h in sel if h['alq'] and h['renta'] and h['renta'] > 0 and h['uc']]
                    esf = [(12 * h['alq'] / h['renta'], h['w']) for h in v]
                    tv = sum(h['w'] for h in v)
                    fila.update(
                        esfuerzo_alquiler_mediana_pct=round(100 * wmediana(esf), 1),
                        pct_esfuerzo_sup_30=round(100 * sum(w for e, w in esf if e > 0.30) / tv, 1),
                        pct_esfuerzo_sup_40=round(100 * sum(w for e, w in esf if e > 0.40) / tv, 1),
                        renta_residual_uc_eur2024=round(wmediana(
                            [((h['renta'] - 12 * h['alq']) / h['uc'] * defl, h['w']) for h in v])))
                filas.append(fila)
        periodo = '2005-2008' if 2005 <= anio <= 2008 else ('2022-2025' if anio >= 2022 else None)
        if periodo:
            jefes = {h['jefe']: h['ten'] for h in hog}
            for pid, e in edad.items():
                if 18 <= e <= 40:
                    s = simple[(periodo, e)]; w = wper[pid]
                    s[0] += w
                    if pid in jefes:
                        s[1] += w
                        s[2] += w if jefes[pid] == 'prop_hip' else 0
        print(anio, 'ok')
    campos = list(dict.fromkeys(k for f in filas for k in f))
    with open(os.path.join(T, 'G14_espana_alquiler_y_colchon_ahorro_por_edad_2004_2025.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(filas)
    with open(os.path.join(T, 'G14b_espana_emancipacion_e_hipoteca_por_edad_simple.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['periodo', 'edad', 'pct_responsable_vivienda', 'pct_responsable_vivienda_con_hipoteca'])
        for (p, e), (n, j, hp) in sorted(simple.items()):
            w.writerow([p, e, round(100 * j / n, 2), round(100 * hp / n, 2)])


if __name__ == '__main__':
    main()
