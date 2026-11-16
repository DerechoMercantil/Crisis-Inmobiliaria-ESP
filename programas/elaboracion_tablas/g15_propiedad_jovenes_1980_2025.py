"""Construye tablas/G15_espana_propiedad_por_edad_1980_2025.csv.

Serie larga de acceso a la propiedad por edad del sustentador principal o persona
responsable: EPF 1980-81, EBPF 1990-91 y ECV 2004-2025 (microdatos INE). Responde a
la comparación «los jóvenes de hace 40 años».

- EPF 1980-81: régimen de tenencia P61 (posición 361). El diseño de registro no
  recoge la lista de códigos; se infiere de los bloques que cumplimenta cada código
  (1-5 rellenan el coste y el año de adquisición, «solo viviendas en propiedad o
  acceso»; 6-7 rellenan el año de alquiler; 8-11, ninguno) y de su coincidencia con
  la lista publicada de la EBPF 1990-91: 1 herencia, 2-3 compra pagada (nueva/usada),
  4-5 acceso a la propiedad (nueva/usada), 6 alquiler, 7 realquiler, 8-11 cedida.
  La distribución ponderada (alquiler 22,8 %) es coherente con el censo de 1981.
- EBPF 1990-91: tenencia en posiciones 71-72 del registro 1 (lista publicada);
  edad exacta del sustentador principal en el registro 3 (relación = 1).
- ECV: tenencia como en g13 (propiedad = HH021 1-2 o HH020 1; con pagos pendientes
  = con hipoteca).
- «Con pagos pendientes» equivale a «acceso a la propiedad» en las EPF y a
  «propiedad con hipoteca» en la ECV. En 1980-91 incluye pagos aplazados al promotor
  o a la cooperativa, no solo préstamo bancario: es una medida de acceso con
  financiación, no estrictamente de hipoteca.
- Indicadores por cada 100 personas de 25-34 años: combinan emancipación y acceso.
"""
import csv, os, zipfile
from collections import defaultdict
import g13_tenencia_hipoteca_por_edad as g13

BR, T = g13.BR, g13.T
TRAMOS = [(18, 24), (25, 34), (18, 35), (35, 44), (45, 54)]


def epf8081():
    raw = zipfile.ZipFile(os.path.join(BR, 'ebpf', 'datos_ebpf8081.zip')).read('EPF80-81')
    f = lambda l, a, n: l[a - 1:a - 1 + n].decode('latin1').strip()
    num = lambda s: int(s) if s.strip().isdigit() else 0
    hog, pob = [], defaultdict(float)
    for l in (x for x in raw.split(b'\r\n') if x.strip()):
        w = num(f(l, 7691, 8)) / 1e4 * num(f(l, 7645, 2)) * num(f(l, 7647, 2))
        t = num(f(l, 361, 2))
        ten = 'prop_pend' if t in (4, 5) else 'prop_pagada' if t in (1, 2, 3) else \
              'alquiler' if t in (6, 7) else 'cedida' if t else None
        jefe = None
        for k in range(num(f(l, 64, 2))):
            e = num(f(l, 70 + 14 * k, 2))
            if num(f(l, 68 + 14 * k, 1)) == 1:
                jefe = e
            pob[e] += w
        if ten and jefe is not None:
            hog.append(dict(edad=jefe, ten=ten, w=w))
    return hog, pob


def epf9091():
    z = zipfile.ZipFile(os.path.join(BR, 'ebpf', 'datos_ebpf9091.zip'))
    rd = lambda n: [l for l in z.read(n).split(b'\r\n') if l.strip()]
    g = lambda l, a, b: int(l[a - 1:b]) if l[a - 1:b].strip().isdigit() else 0
    ten_h = {}
    for l in rd('TIPREG1.TXT'):
        t = g(l, 71, 72)
        ten_h[l[:5]] = ('prop_pend' if t in (4, 5) else 'prop_pagada' if t in (1, 2, 3) else
                        'alquiler' if t in (12, 13) else 'cedida' if t else None,
                        g(l, 737, 746) / 1e5 * g(l, 747, 754) / 1e5)
    hog, pob = [], defaultdict(float)
    for l in rd('TIPREG3.TXT'):
        e = g(l, 13, 14); w = g(l, 261, 270) / 1e5 * g(l, 271, 278) / 1e5
        pob[e] += w
        if g(l, 11, 11) == 1 and l[:5] in ten_h and ten_h[l[:5]][0]:
            hog.append(dict(edad=e, ten=ten_h[l[:5]][0], w=ten_h[l[:5]][1]))
    return hog, pob


def ecv(anio):
    peso = {r['DB030']: g13.fl(r['DB090']) or 0 for r in g13.leer(anio, 'd')}
    edad, pob = {}, defaultdict(float)
    for r in g13.leer(anio, 'p'):
        nac = g13.fl(r['PB140'])
        if nac is not None:
            e = anio - int(nac); edad[r['PB030'].strip()] = e
            pob[e] += g13.fl(r['PB040']) or 0
    hog = []
    for r in g13.leer(anio, 'h'):
        w = peso.get(r['HB030'].strip(), 0); j = r['HB080'].strip()
        if not w or j not in edad:
            continue
        if 'HH021' in r:
            ten = {'1': 'prop_pagada', '2': 'prop_pend', '3': 'alquiler', '4': 'alquiler',
                   '5': 'cedida'}.get(r['HH021'].strip())
        else:
            hs = 'HS010_F' if 'HS010_F' in r else 'HS011_F'; c = r['HH020'].strip()
            ten = ('prop_pagada' if r[hs].strip() == '-2' else 'prop_pend') if c == '1' else \
                  {'2': 'alquiler', '3': 'alquiler', '4': 'cedida'}.get(c)
        if ten:
            hog.append(dict(edad=edad[j], ten=ten, w=w))
    return hog, pob


def resumen(etiqueta, hog, pob):
    filas = []
    for a, b in TRAMOS:
        sel = [h for h in hog if a <= h['edad'] <= b]
        tot = sum(h['w'] for h in sel)
        prop = sum(h['w'] for h in sel if h['ten'] in ('prop_pagada', 'prop_pend'))
        pend = sum(h['w'] for h in sel if h['ten'] == 'prop_pend')
        alq = sum(h['w'] for h in sel if h['ten'] == 'alquiler')
        p = sum(v for e, v in pob.items() if a <= e <= b)
        filas.append(dict(fuente=etiqueta, tramo=f'{a}-{b}', n_muestra=len(sel),
                          pct_propiedad=round(100 * prop / tot, 1), pct_prop_pagos_pendientes=round(100 * pend / tot, 1),
                          pct_alquiler=round(100 * alq / tot, 1),
                          hogares_por_100_personas=round(100 * tot / p, 1),
                          propietarios_por_100_personas=round(100 * prop / p, 1),
                          prop_pendientes_por_100_personas=round(100 * pend / p, 1)))
    return filas


def main():
    filas = resumen('EPF 1980-81', *epf8081()) + resumen('EBPF 1990-91', *epf9091())
    for anio in range(2004, 2026):
        filas += resumen(f'ECV {anio}', *ecv(anio))
    with open(os.path.join(T, 'G15_espana_propiedad_por_edad_1980_2025.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0])); w.writeheader(); w.writerows(filas)
    for r in filas:
        if r['tramo'] == '25-34':
            print(r)


if __name__ == '__main__':
    main()
