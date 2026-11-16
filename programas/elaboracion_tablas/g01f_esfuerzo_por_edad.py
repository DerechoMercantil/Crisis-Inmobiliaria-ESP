#!/usr/bin/env python3
"""Construye tablas/G01f_espana_esfuerzo_teorico_por_edad_1987_2024.csv: equivalente por edad
del gráfico de Funcas sobre el cuadro 1.5 de la Síntesis de Indicadores del Banco de España
(años de renta y esfuerzo teórico anual sin deducciones).

El esfuerzo teórico del BdE (SI_1_5.44) es la cuota bruta del primer año de un préstamo
estándar por el 80 % del precio de la vivienda tipo, en % de la renta del hogar mediano; la
ratio precio/renta (SI_1_5.43) usa la misma vivienda y la misma renta. Su cociente
F = esfuerzo / ratio = 80 × cuota anual por euro prestado recoge solo los supuestos de
financiación del BdE (tipo y plazo de cada año). El esfuerzo de cada cohorte es
F × años de renta de la cohorte (tabla G1e), es decir, la misma cuota sobre su renta.
El BdE publica el esfuerzo desde 1987; no hay serie oficial de tipos hipotecarios anterior
a 1989, por lo que la tabla empieza en 1987.
"""
import csv, os

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
COLS = [('18_mas', 'anios_renta_mediana_18_mas'), ('18_35', 'anios_renta_18_35'),
        ('55_64', 'anios_renta_55_64'), ('65_74', 'anios_renta_65_74')]


def anual_bde(codigo, n_periodos):
    filas = list(csv.reader(open(os.path.join(BASE, 'datos', 'brutos', 'bde_si_1_5.csv'), encoding='latin1')))
    j = filas[2].index(codigo)
    d = {}
    for f in filas[6:]:
        if f and f[0][-4:].isdigit() and j < len(f) and f[j] not in ('_', ''):
            d.setdefault(int(f[0][-4:]), []).append(float(f[j]))
    return {a: sum(v) / len(v) for a, v in d.items() if len(v) == n_periodos}


def main():
    ratio, esfuerzo = anual_bde('SI_1_5.43', 4), anual_bde('SI_1_5.44', 4)
    tipo = anual_bde('SI_1_5.40', 12)
    with open(os.path.join(BASE, 'tablas', 'G01e_espana_ratio_precio_renta_todas_edades_1980_2024.csv')) as f:
        g1e = [r for r in csv.DictReader(f) if int(r['anio']) >= 1987]

    salida = os.path.join(BASE, 'tablas', 'G01f_espana_esfuerzo_teorico_por_edad_1987_2024.csv')
    with open(salida, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['anio', 'tipo_interes_bde_pct', 'cuota_anual_por_euro_prestado', 'anios_renta_hogar_bde',
                    'esfuerzo_hogar_bde_pct']
                   + [f'anios_renta_{c}' for c, _ in COLS] + [f'esfuerzo_{c}_pct' for c, _ in COLS]
                   + ['tipo', 'fuente'])
        for r in g1e:
            a = int(r['anio'])
            factor = esfuerzo[a] / ratio[a]
            anios = [float(r[col]) for _, col in COLS]
            w.writerow([a, round(tipo[a], 2) if a in tipo else '', round(factor / 80, 4), round(ratio[a], 2),
                        round(esfuerzo[a], 1)] + [round(x, 2) for x in anios] + [round(factor * x, 1) for x in anios]
                       + [r['tipo'], r['fuente']])
    print('Escrito', salida)


if __name__ == '__main__':
    main()
