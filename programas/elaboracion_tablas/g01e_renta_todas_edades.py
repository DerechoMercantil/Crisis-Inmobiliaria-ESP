#!/usr/bin/env python3
"""Construye tablas/G01e_espana_ratio_precio_renta_todas_edades_1980_2024.csv: serie de
referencia para contrastar G1c y G1d. El precio de la vivienda tipo (93,75 m²) en años
de renta disponible del conjunto de perceptores de 18 años o más, con la mediana (el
estadístico de G1c/G1d) y la media, junto a las cohortes de 18-35, 55-64 y 65-74 años y
su renta relativa respecto a la mediana de todas las edades.

Método idéntico a G1c/G1d; la media y la mediana se enlazan cada una con su propio
factor base 2004 / base 2013 (solape 2008-2012).
"""
import csv, json, os
from g01c_renta_joven import BASE, T, precio_vivienda_tipo
from g01d_renta_mayores import lecturas, enlazar

TODAS = (18, 120)


def main():
    declaradas, solape, registros = lecturas(TODAS)
    mediana, k_med = enlazar(declaradas, solape, registros, 'med_joven')
    media, k_media = enlazar(declaradas, solape, registros, 'media_joven')
    print(f'k mediana = {k_med:.4f}, k media = {k_media:.4f}')
    precio = precio_vivienda_tipo()
    with open(os.path.join(T, 'G01d_espana_ratio_precio_renta_por_edad_1980_2024.csv')) as f:
        coh = {int(r['anio']): r for r in csv.DictReader(f)}

    salida = os.path.join(T, 'G01e_espana_ratio_precio_renta_todas_edades_1980_2024.csv')
    with open(salida, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['anio', 'precio_vivienda_tipo_eur',
                    'renta_disp_mediana_18_mas_eur', 'renta_disp_media_18_mas_eur',
                    'anios_renta_mediana_18_mas', 'anios_renta_media_18_mas',
                    'anios_renta_18_35', 'anios_renta_55_64', 'anios_renta_65_74',
                    'renta_relativa_18_35', 'renta_relativa_55_64', 'renta_relativa_65_74',
                    'tipo', 'fuente', 'pct_perceptores_18_mas', 'n_muestral_18_mas'])
        for y in sorted(coh):
            c, md, mn = coh[y], mediana[y]['renta'], media[y]['renta']
            rel = lambda col: round(float(c[col]) / md, 3)
            w.writerow([y, round(precio[y]), round(md), round(mn), round(precio[y] / md, 2), round(precio[y] / mn, 2),
                        c['anios_renta_18_35'], c['anios_renta_55_64'], c['anios_renta_65_74'],
                        rel('renta_disp_18_35_eur'), rel('renta_disp_55_64_eur'), rel('renta_disp_65_74_eur'),
                        c['tipo'], c['fuente'],
                        round(mediana[y]['pct'], 3) if mediana[y]['pct'] != '' else '', mediana[y]['n']])
    with open(os.path.join(BASE, 'datos', 'procesados', 'g1e_enlace_ecv_bases.json'), 'w') as f:
        json.dump(dict(k_mediana=k_med, k_media=k_media,
                       solape=[dict(encuesta=a['anio_renta'] + 1, mediana_b2004=a['med_joven'], mediana_b2013=b['med_joven'],
                                    media_b2004=a['media_joven'], media_b2013=b['media_joven']) for a, b in solape]),
                  f, indent=1)
    print('Escrito', salida)


if __name__ == '__main__':
    main()
