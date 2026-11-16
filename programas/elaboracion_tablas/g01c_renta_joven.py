#!/usr/bin/env python3
"""Construye tablas/G01c_espana_ratio_precio_renta_joven_1980_2024.csv: el precio de la
vivienda tipo de G01/G01bis (vivienda libre de 93,75 m²) expresado en años de renta
disponible del joven perceptor mediano (18 a 35 años) y, como referencia, del hogar
mediano, con las mismas encuestas y el mismo concepto de renta, 1980-2024.

- Renta del joven: mediana de la renta personal disponible (neta de impuestos y
  cotizaciones) de los perceptores de 18-35 años: trabajo por cuenta ajena y propia
  más prestaciones sociales. Edad al final del periodo de referencia de la renta.
- Renta del hogar: mediana del total de ingresos monetarios ordinarios netos.
- Precio: vivienda tipo de 93,75 m²; tasación (Fomento/MIVAU, BIS antes de 1987) hasta 2007 y,
  desde 2008, evolución del Índice de Precios de Vivienda del INE (compraventas ante notario,
  calidad constante). Se conserva la versión con tasación en columnas aparte.
- Fuentes (microdatos INE): EPF 1980-81, EBPF 1990-91, PHOGUE 1994-2001 y ECV 2005-2025
  (estas dos con renta del año anterior). ECV 2004 se excluye (anomalía de la renta
  del hogar en la primera ola).
- Enlace: la ECV base 2013 (2008-) toma la renta de registros fiscales; las encuestas
  anteriores son de renta declarada. Las medianas declaradas se multiplican por la
  razón media base 2013 / base 2004 del solape 2008-2012 (una para el joven y otra
  para el hogar). Los años sin encuesta se interpolan log-linealmente.
"""
import csv, glob, json, math, os, zipfile
from collections import defaultdict

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
BR = os.path.join(BASE, 'datos', 'brutos')
T = os.path.join(BASE, 'tablas')
EDAD_MIN, EDAD_MAX = 18, 35


def wmedian(vals, ws):
    pares = sorted((v, w) for v, w in zip(vals, ws) if w > 0)
    tot = sum(w for _, w in pares)
    acc = 0
    for v, w in pares:
        acc += w
        if acc >= tot / 2:
            return v


def resultado(anio_renta, fuente, hv, hw, yv, yw, n_jov_pob):
    mh, my = wmedian(hv, hw), wmedian(yv, yw)
    return dict(anio_renta=anio_renta, fuente=fuente, med_hogar=mh, med_joven=my,
                media_joven=sum(v * w for v, w in zip(yv, yw)) / sum(yw),
                rel=my / mh, pct_jov_perceptores=sum(yw) / n_jov_pob, n_muestra=len(yv))


# ---------- EPF 1980-81 (un registro por hogar, ancho fijo) ----------
def epf8081(edades=(EDAD_MIN, EDAD_MAX)):
    raw = zipfile.ZipFile(os.path.join(BR, 'ebpf', 'datos_ebpf8081.zip')).read('EPF80-81')
    f = lambda l, a, n: l[a - 1:a - 1 + n].decode('latin1').strip()
    num = lambda s: int(s) if s.strip().isdigit() else 0
    hv, hw, yv, yw, pob = [], [], [], [], 0
    for l in (x for x in raw.split(b'\r\n') if x.strip()):
        w = num(f(l, 7691, 8)) / 1e4 * num(f(l, 7645, 2)) * num(f(l, 7647, 2))
        edad = {num(f(l, 66 + 14 * k, 2)): num(f(l, 70 + 14 * k, 2)) for k in range(num(f(l, 64, 2)))}
        pers, hogar = {}, 0
        for k in range(4):
            o = 1569 + 66 * k
            orden = num(f(l, o, 2))
            if not orden:
                continue
            x = [num(f(l, o + 2 + 8 * j, 8)) for j in range(8)]   # X2..X9
            pers[orden] = pers.get(orden, 0) + x[0] + x[1] + x[3] + x[6]
            hogar += x[7] - x[4] - x[5]
        hv.append(hogar); hw.append(w)
        for orden, e in edad.items():
            if edades[0] <= e <= edades[1]:
                pob += w
                if pers.get(orden, 0) > 0:
                    yv.append(pers[orden]); yw.append(w)
    return resultado(1980, 'EPF 1980-81', hv, hw, yv, yw, pob)


# ---------- EBPF 1990-91 (registro 1 hogares, registro 3 miembros) ----------
def epf9091(edades=(EDAD_MIN, EDAD_MAX)):
    z = zipfile.ZipFile(os.path.join(BR, 'ebpf', 'datos_ebpf9091.zip'))
    rd = lambda n: [l for l in z.read(n).split(b'\r\n') if l.strip()]
    g = lambda l, a, b: int(l[a - 1:b]) if l[a - 1:b].strip().isdigit() else 0
    peso = {l[:5]: g(l, 737, 746) / 1e5 * g(l, 747, 754) / 1e5 for l in rd('TIPREG1.TXT')}
    hogar, yv, yw, pob = defaultdict(float), [], [], 0
    for l in rd('TIPREG3.TXT'):
        trabajo_prest = (g(l, 61, 68) + g(l, 69, 76) - g(l, 77, 84)
                         + sum(g(l, a, a + 7) for a in range(141, 204, 8)))
        capital_transf = (g(l, 85, 92) - g(l, 93, 100) + g(l, 101, 108) - g(l, 109, 116)
                          + g(l, 117, 124) + g(l, 125, 132) - g(l, 133, 140) + g(l, 213, 220))
        hogar[l[:5]] += trabajo_prest + capital_transf
        if edades[0] <= g(l, 13, 14) <= edades[1]:
            w = g(l, 261, 270) / 1e5 * g(l, 271, 278) / 1e5
            pob += w
            if trabajo_prest > 0:
                yv.append(trabajo_prest); yw.append(w)
    hv = [hogar.get(h, 0) for h in peso]
    return resultado(1990, 'EBPF 1990-91', hv, list(peso.values()), yv, yw, pob)


# ---------- PHOGUE 1994-2001 (renta del año anterior) ----------
def phogue(ola, edades=(EDAD_MIN, EDAD_MAX)):
    d = os.path.join(BR, 'phogue', 'ext')
    g = lambda l, a, b: float(l[a - 1:b]) if l[a - 1:b].strip() not in (b'', b'-8', b'-9') else 0.0
    hv, hw = [], []
    for l in open(os.path.join(d, f'w{ola}hhs.asc'), 'rb'):
        hv.append(g(l, 134, 143)); hw.append(g(l, 51, 58))
    yv, yw, pob = [], [], 0
    for l in open(os.path.join(d, f'w{ola}pers.asc'), 'rb'):
        if not l[70:72].strip().isdigit():
            continue
        if edades[0] <= int(l[70:72]) - 1 <= edades[1]:
            w = g(l, 36, 43); pob += w
            v = max(g(l, 330, 339), 0) + max(g(l, 420, 429), 0)
            if v > 0:
                yv.append(v); yw.append(w)
    return resultado(1992 + ola, f'PHOGUE {1993 + ola}', hv, hw, yv, yw, pob)


# ---------- ECV (renta del año anterior) ----------
PY_NETAS = ['PY010N', 'PY050N', 'PY080N', 'PY090N', 'PY100N', 'PY110N', 'PY120N', 'PY130N', 'PY140N']


def ecv(encuesta, base='b2013', edades=(EDAD_MIN, EDAD_MAX)):
    yy = str(encuesta)[2:]
    if encuesta == 2025:
        fich = lambda t: os.path.join(BR, 'ecv_2025', 'CSV', f'esudb25{t}.csv')
    else:
        carpeta = f'ext_b04_{encuesta}' if base == 'b2004' and encuesta >= 2008 else f'ext_{encuesta}'
        fich = lambda t: sorted(glob.glob(os.path.join(BR, 'ecv_hist', carpeta, '**', f'esudb{yy}{t}.csv'),
                                          recursive=True), key=len)[0]
    def fl(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return 0.0
    leer = lambda t: csv.DictReader(open(fich(t), encoding='latin1'))
    peso = {r['DB030']: fl(r['DB090']) for r in leer('d')}
    renta = {r['HB030']: fl(r['HY020']) for r in leer('h')}
    hogares = [h for h in peso if h in renta]
    yv, yw, pob = [], [], 0
    for r in leer('p'):
        try:
            edad = int(r['PB010']) - 1 - int(r['PB140'])
        except ValueError:
            continue
        if edades[0] <= edad <= edades[1]:
            w = fl(r['PB040']); pob += w
            v = sum(fl(r.get(c)) for c in PY_NETAS)
            if v > 0:
                yv.append(v); yw.append(w)
    return resultado(encuesta - 1, f'ECV {encuesta}' + (' (base 2004)' if base == 'b2004' else ''),
                     [renta[h] for h in hogares], [peso[h] for h in hogares], yv, yw, pob)


PESETAS_EURO = 166.386


def ipv_ine():
    """INE, Índice de Precios de Vivienda, general nacional, media anual (tabla 80271)."""
    with open(os.path.join(BR, 'ine_ipv_80271_medias_anuales.json')) as f:
        serie = next(s for s in json.load(f) if s['Nombre'].startswith('Nacional. Media anual. General'))
    return {d['Anyo']: d['Valor'] for d in serie['Data']}


def precio_vivienda_tipo(numerador='ipv'):
    """Precio de la vivienda libre de 93,75 m² en euros. Hasta 2007, valor de tasación
    (G1b; BIS antes de 1987). Desde 2008, con numerador='ipv', el nivel de 2007 evoluciona
    con el Índice de Precios de Vivienda del INE (compraventas, calidad constante)."""
    pm2 = {}
    with open(os.path.join(T, 'G01b_espana_precio_vs_renta_indexado.csv')) as f:
        for r in csv.DictReader(f):
            pm2[int(r['anio'])] = float(r['precio_m2_eur'])
    bis = defaultdict(list)
    with open(os.path.join(BASE, 'datos', 'procesados', 'bis_precios_vivienda_trimestral.csv')) as f:
        for r in csv.DictReader(f):
            if r['area'] == 'ES' and r['nominal_real'] == 'N':
                bis[int(r['trimestre'][:4])].append(float(r['indice_2010_100']))
    bis = {y: sum(v) / len(v) for y, v in bis.items()}
    for y in range(1971, 1987):
        pm2[y] = pm2[1987] * bis[y] / bis[1987]
    if numerador == 'ipv':
        ipv = ipv_ine()
        for y in ipv:
            if y > 2007:
                pm2[y] = pm2[2007] * ipv[y] / ipv[2007]
    return {y: v * 93.75 for y, v in pm2.items()}


def main():
    declaradas = [epf8081(), epf9091()] + [phogue(o) for o in range(1, 9)] \
        + [ecv(y, 'b2004') for y in (2005, 2006, 2007)]
    solape = [(ecv(y, 'b2004'), ecv(y)) for y in range(2008, 2013)]
    k_joven = sum(b['med_joven'] / a['med_joven'] for a, b in solape) / len(solape)
    k_hogar = sum(b['med_hogar'] / a['med_hogar'] for a, b in solape) / len(solape)
    registros = [ecv(y) for y in range(2008, 2026)]

    medidos = {}
    for r in declaradas + registros:
        declarada = r in declaradas
        a_euros = 1 / PESETAS_EURO if r['anio_renta'] < 2002 else 1
        medidos[r['anio_renta']] = dict(
            r, joven=r['med_joven'] * a_euros * (k_joven if declarada else 1),
            hogar=r['med_hogar'] * a_euros * (k_hogar if declarada else 1),
            tipo='medido; renta declarada enlazada' if declarada else 'medido; ECV base 2013')

    precio = precio_vivienda_tipo()
    precio_tas = precio_vivienda_tipo('tasacion')
    anios = sorted(medidos)
    salida = os.path.join(T, 'G01c_espana_ratio_precio_renta_joven_1980_2024.csv')
    with open(salida, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['anio', 'precio_vivienda_tipo_eur', 'renta_disp_joven_mediano_eur', 'renta_disp_hogar_mediano_eur',
                    'anios_renta_joven_18_35', 'anios_renta_hogar_mediano', 'tipo', 'fuente',
                    'pct_jovenes_18_35_perceptores', 'n_muestral_jovenes',
                    'precio_vivienda_tipo_tasacion_eur', 'anios_renta_joven_18_35_tasacion'])
        for y in range(anios[0], anios[-1] + 1):
            if y in medidos:
                m = medidos[y]
                joven, hogar, tipo, fuente = m['joven'], m['hogar'], m['tipo'], m['fuente']
                extra = [round(m['pct_jov_perceptores'], 3), m['n_muestra']]
            else:
                a = max(x for x in anios if x < y); b = min(x for x in anios if x > y)
                t = (y - a) / (b - a)
                interp = lambda c: math.exp(math.log(medidos[a][c]) * (1 - t) + math.log(medidos[b][c]) * t)
                joven, hogar, tipo, fuente, extra = interp('joven'), interp('hogar'), 'interpolado', '', ['', '']
            w.writerow([y, round(precio[y]), round(joven), round(hogar), round(precio[y] / joven, 2),
                        round(precio[y] / hogar, 2), tipo, fuente] + extra
                       + [round(precio_tas[y]), round(precio_tas[y] / joven, 2)])

    with open(os.path.join(BASE, 'datos', 'procesados', 'g1c_enlace_ecv_bases.json'), 'w') as f:
        json.dump(dict(k_joven=k_joven, k_hogar=k_hogar,
                       solape=[dict(encuesta=a['anio_renta'] + 1, joven_b2004=a['med_joven'], joven_b2013=b['med_joven'],
                                    hogar_b2004=a['med_hogar'], hogar_b2013=b['med_hogar']) for a, b in solape]),
                  f, indent=1)
    print(f'k_joven = {k_joven:.4f}, k_hogar = {k_hogar:.4f}. Escrito', salida)


if __name__ == '__main__':
    main()
