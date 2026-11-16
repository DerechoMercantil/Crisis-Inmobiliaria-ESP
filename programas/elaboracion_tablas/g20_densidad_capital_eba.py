"""Construye tablas/G20_bancos_espanoles_densidad_apr_por_exposicion_2025.csv.

Densidad de activos ponderados por riesgo (APR / valor de exposición) por clase de
exposición en los bancos españoles del ejercicio de transparencia de la EBA de 2025
(fecha de referencia 30-6-2025; datos consolidados de grupo, incluida la actividad en
el extranjero). Fuente: EBA, 2025 EU-wide Transparency Exercise, tr_cre.csv
(datos/brutos/eba_transparencia_2025/). Último ejercicio publicado: la EBA lo ha
discontinuado y remite al Pillar 3 Data Hub.

Partidas: valor de exposición 2520522/2520524/2520525 y APR 2520532/2520534/2520535.
Clases: 406 minoristas garantizadas con bienes inmuebles (IRB; aproxima la hipoteca
residencial), 304 financiación especializada (IRB; incluye promoción inmobiliaria, pero
también financiación de proyectos, de activos y de materias primas), 303 empresas (IRB),
501 garantizadas con inmuebles y exposiciones AUE (método estándar; mezcla vivienda,
comercial y promoción, no separables en esta fuente).
"""
import csv, os
from collections import defaultdict

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
F = os.path.join(BASE, 'datos', 'brutos', 'eba_transparencia_2025', 'tr_cre.csv')
BANCOS = {'5493006QMFDDMYWIAM13': 'Santander', 'K8MS7FD7N5Z2WQ51AZ71': 'BBVA', '7CUNS533WID6K7DGFI87': 'CaixaBank',
          'SI5RG2M0WQQLZCXKRM20': 'Sabadell', 'VWMYAEQSTOPNV0SUGU82': 'Bankinter', '5493007SJLLCTM6J6M37': 'Unicaja',
          '549300U4LIZV0REEQQ46': 'Kutxabank', '549300OLBL49CW8CT155': 'Ibercaja', '54930056IRBXK0Q1FP96': 'Abanca',
          '95980020140005881190': 'Cajamar (BCC)'}
CLASES = [('IRB', '2', '2520525', '2520535', '406', 'Hipotecas (minoristas garantizadas con inmuebles)'),
          ('IRB', '2', '2520524', '2520534', '304', 'Financiación especializada'),
          ('IRB', '2', '2520522', '2520532', '303', 'Empresas'),
          ('Estándar', '1', '2520522', '2520532', '501', 'Garantizadas con inmuebles y AUE')]


def main():
    acc = defaultdict(float)
    items = {c[2] for c in CLASES} | {c[3] for c in CLASES}
    with open(F, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['NSA'] != 'ES' or r['Period'] != '202506' or r['Item'] not in items or r['Country'] != '0':
                continue
            try:
                acc[(r['LEI_Code'], r['Portfolio'], r['Item'], r['Exposure'])] += float(r['Amount'])
            except ValueError:
                pass
    filas = []
    for metodo, port, ev, rw, exp, nombre in CLASES:
        for lei, banco in list(BANCOS.items()) + [('TOTAL', 'Total bancos españoles')]:
            if lei == 'TOTAL':
                x = sum(v for (l, p, i, e), v in acc.items() if p == port and i == ev and e == exp)
                y = sum(v for (l, p, i, e), v in acc.items() if p == port and i == rw and e == exp)
            else:
                x, y = acc.get((lei, port, ev, exp), 0), acc.get((lei, port, rw, exp), 0)
            if x:
                filas.append(dict(metodo=metodo, clase=nombre, banco=banco, exposicion_mill_eur=round(x),
                                  apr_mill_eur=round(y), densidad_apr_pct=round(100 * y / x, 1)))
    out = os.path.join(BASE, 'tablas', 'G20_bancos_espanoles_densidad_apr_por_exposicion_2025.csv')
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0])); w.writeheader(); w.writerows(filas)
    for r in filas:
        if r['banco'] == 'Total bancos españoles':
            print(r)


if __name__ == '__main__':
    main()
