"""Construye tablas/G17_espana_pobreza_tras_vivienda_inquilinos_jovenes_2005_2025.csv.

Hogares con responsable de 25-34 años en alquiler de mercado (ECV, microdatos INE):
esfuerzo en alquiler y riesgo de pobreza antes y después de pagar la vivienda, con la
corrección del cambio de base de la renta en 2008.

- Cambio de base: en 2005-2007 (base 2004) la renta del hogar procede de la
  declaración del entrevistado; desde 2008 (base 2013), de registros fiscales. En el
  solape 2008-2012 la mediana de la renta del hogar es un 14,6 % mayor en base 2013
  (k_hogar = 1,146, datos/procesados/g1c_enlace_ecv_bases.json). Sin corregir, el
  esfuerzo de 2005-2007 está sobrestimado en esa proporción. Aquí se multiplica HY020
  de 2005-2007 por k_hogar para el esfuerzo; las tasas de pobreza, que son relativas a
  la mediana del propio año, no necesitan corrección.
- Riesgo de pobreza: renta disponible equivalente (HY020 / HX240) inferior al 60 % de
  la mediana nacional del año, calculada sobre personas (peso DB090 × HX040). «Tras
  la vivienda»: misma comparación con (HY020 − 12 × HH070) / HX240, siendo HH070 el
  coste total mensual de la vivienda (alquiler, suministros y demás gastos), frente al
  mismo umbral. Es el indicador del informe de Oxfam Intermón de octubre de 2026,
  aunque ese informe se limita a personas ocupadas.
"""
import csv, json, os
from collections import defaultdict
import g13_tenencia_hipoteca_por_edad as g13
from g14_alquiler_ahorro_por_edad import ipc_anual, tenencia, wmediana

K_HOGAR = json.load(open(os.path.join(g13.BASE, 'datos', 'procesados', 'g1c_enlace_ecv_bases.json')))['k_hogar']
PERIODOS = {'2005-2007 (base 2004, corregida)': range(2005, 2008), '2008-2010': range(2008, 2011),
            '2014-2016': range(2014, 2017), '2022-2025': range(2022, 2026)}


def ola(anio, ipc):
    d = {r['DB030']: (g13.fl(r['DB090']) or 0, r['DB100'].strip()) for r in g13.leer(anio, 'd')}
    edad = {}
    for r in g13.leer(anio, 'p'):
        n = g13.fl(r['PB140'])
        if n is not None:
            edad[r['PB030'].strip()] = anio - int(n)
    hog = []
    for r in g13.leer(anio, 'h'):
        x = d.get(r['HB030'].strip()); y = g13.fl(r['HY020']); uc = g13.fl(r['HX240'])
        if not x or not x[0] or y is None or not uc:
            continue
        hog.append(dict(w=x[0], urb=x[1], y=y, uc=uc, n=g13.fl(r['HX040']) or 1,
                        ten=tenencia(r), alq=g13.fl(r['HH060']), coste=g13.fl(r['HH070']) or 0,
                        edad=edad.get(r['HB080'].strip())))
    umbral = 0.6 * wmediana([(h['y'] / h['uc'], h['w'] * h['n']) for h in hog])
    k = K_HOGAR if anio < 2008 else 1.0
    defl = ipc[2024] / ipc[anio - 1]
    out = []
    for h in hog:
        if h['edad'] is None or not 25 <= h['edad'] <= 34 or h['ten'] != 'alq_mercado' or not h['alq'] or h['y'] <= 0:
            continue
        out.append(dict(w=h['w'], urb=h['urb'], uni=h['n'] == 1,
                        esf=12 * h['alq'] / (h['y'] * k),
                        pobre_antes=h['y'] / h['uc'] < umbral,
                        pobre_despues=(h['y'] - 12 * h['coste']) / h['uc'] < umbral,
                        renta_eq_real=h['y'] * k / h['uc'] * defl))
    return out


def medidas(sel):
    t = sum(h['w'] for h in sel)
    return dict(n_muestra=len(sel),
                esfuerzo_alquiler_mediano_pct=round(100 * wmediana([(h['esf'], h['w']) for h in sel]), 1),
                pct_esfuerzo_sup_40=round(100 * sum(h['w'] for h in sel if h['esf'] > 0.4) / t, 1),
                pct_pobreza_antes_vivienda=round(100 * sum(h['w'] for h in sel if h['pobre_antes']) / t, 1),
                pct_pobreza_tras_vivienda=round(100 * sum(h['w'] for h in sel if h['pobre_despues']) / t, 1),
                renta_equivalente_mediana_eur2024=round(wmediana([(h['renta_eq_real'], h['w']) for h in sel])))


def main():
    ipc = ipc_anual()
    filas = []
    for p, anios in PERIODOS.items():
        hs = [h for a in anios for h in ola(a, ipc)]
        for grupo, f in (('Todos', lambda h: True), ('Zona densamente poblada', lambda h: h['urb'] == '1'),
                         ('Hogar unipersonal', lambda h: h['uni'])):
            filas.append(dict(periodo=p, grupo=grupo, **medidas([h for h in hs if f(h)])))
    with open(os.path.join(g13.T, 'G17_espana_pobreza_tras_vivienda_inquilinos_jovenes_2005_2025.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0])); w.writeheader(); w.writerows(filas)
    for r in filas:
        print(r)


if __name__ == '__main__':
    main()
