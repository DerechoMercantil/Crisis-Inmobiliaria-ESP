#!/usr/bin/env python3
"""Construye tablas/G01d_espana_ratio_precio_renta_por_edad_1980_2024.csv: espejo de G1c.
El precio de la vivienda tipo (93,75 m²) en años de renta disponible del perceptor mediano
de 55-64 y de 65-74 años, junto a la serie de 18-35 años de G1c.

Método idéntico al de g01c_renta_joven.py (mismas encuestas, mismo concepto de renta
personal: trabajo + prestaciones sociales, pensiones incluidas, sin rentas del capital;
mismo enlace base 2004 / base 2013, con factor propio de cada cohorte; interpolación
log-lineal de la renta en los años sin encuesta).
"""
import csv, json, math, os
from g01c_renta_joven import (BASE, T, PESETAS_EURO, epf8081, epf9091, phogue, ecv,
                              precio_vivienda_tipo)

COHORTES = {'55_64': (55, 64), '65_74': (65, 74)}


def lecturas(edades):
    declaradas = [epf8081(edades), epf9091(edades)] + [phogue(o, edades) for o in range(1, 9)] \
        + [ecv(y, 'b2004', edades) for y in (2005, 2006, 2007)]
    solape = [(ecv(y, 'b2004', edades), ecv(y, edades=edades)) for y in range(2008, 2013)]
    registros = [ecv(y, edades=edades) for y in range(2008, 2026)]
    return declaradas, solape, registros


def enlazar(declaradas, solape, registros, clave='med_joven'):
    k = sum(b[clave] / a[clave] for a, b in solape) / len(solape)
    medidos = {}
    for r in declaradas + registros:
        declarada = r in declaradas
        a_euros = 1 / PESETAS_EURO if r['anio_renta'] < 2002 else 1
        medidos[r['anio_renta']] = dict(renta=r[clave] * a_euros * (k if declarada else 1),
                                        pct=r['pct_jov_perceptores'], n=r['n_muestra'], fuente=r['fuente'])
    anios = sorted(medidos)
    anual = {}
    for y in range(anios[0], anios[-1] + 1):
        if y in medidos:
            anual[y] = medidos[y]
        else:
            a = max(x for x in anios if x < y); b = min(x for x in anios if x > y)
            t = (y - a) / (b - a)
            anual[y] = dict(renta=math.exp(math.log(medidos[a]['renta']) * (1 - t) + math.log(medidos[b]['renta']) * t),
                            pct='', n='', fuente='')
    return anual, k


def serie(edades, clave='med_joven'):
    declaradas, solape, registros = lecturas(edades)
    anual, k = enlazar(declaradas, solape, registros, clave)
    return anual, k, solape


def main():
    precio = precio_vivienda_tipo()
    with open(os.path.join(T, 'G01c_espana_ratio_precio_renta_joven_1980_2024.csv')) as f:
        jov = {int(r['anio']): r for r in csv.DictReader(f)}
    res, enlace = {}, {}
    for nombre, edades in COHORTES.items():
        res[nombre], k, solape = serie(edades)
        enlace[nombre] = dict(k=k, solape=[dict(encuesta=a['anio_renta'] + 1, b2004=a['med_joven'], b2013=b['med_joven'])
                                           for a, b in solape])
        print(f'{nombre}: k = {k:.4f}')

    salida = os.path.join(T, 'G01d_espana_ratio_precio_renta_por_edad_1980_2024.csv')
    with open(salida, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['anio', 'precio_vivienda_tipo_eur', 'renta_disp_18_35_eur', 'renta_disp_55_64_eur',
                    'renta_disp_65_74_eur', 'anios_renta_18_35', 'anios_renta_55_64', 'anios_renta_65_74',
                    'tipo', 'fuente', 'pct_perceptores_55_64', 'pct_perceptores_65_74',
                    'n_muestral_55_64', 'n_muestral_65_74'])
        for y in sorted(jov):
            a, b = res['55_64'][y], res['65_74'][y]
            w.writerow([y, round(precio[y]), jov[y]['renta_disp_joven_mediano_eur'], round(a['renta']), round(b['renta']),
                        jov[y]['anios_renta_joven_18_35'], round(precio[y] / a['renta'], 2),
                        round(precio[y] / b['renta'], 2), jov[y]['tipo'], jov[y]['fuente'],
                        round(a['pct'], 3) if a['pct'] != '' else '', round(b['pct'], 3) if b['pct'] != '' else '',
                        a['n'], b['n']])
    with open(os.path.join(BASE, 'datos', 'procesados', 'g1d_enlace_ecv_bases.json'), 'w') as f:
        json.dump(enlace, f, indent=1)
    print('Escrito', salida)


if __name__ == '__main__':
    main()
