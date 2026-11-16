"""Construye tablas/G13_espana_tenencia_hipoteca_por_edad_2004_2025.csv y
tablas/G13b_espana_hipoteca_jovenes_por_renta_y_contrato_2004_2025.csv.

Régimen de tenencia de la vivienda principal por edad de la persona responsable,
ECV 2004-2025 (microdatos INE), con especial atención a la propiedad con hipoteca
como resultado observable del acceso al crédito.

- Edad: la de la persona responsable de la vivienda (HB080), año de encuesta menos
  año de nacimiento (PB140). HB080 existe en todas las olas; HB090 (segundo
  responsable) desaparece en 2021, por lo que no se usa.
- Tenencia: HH021 desde 2011 (1 propiedad sin hipoteca, 2 con hipoteca, 3 alquiler
  de mercado, 4 alquiler reducido, 5 cesión). En 2004-2010 solo existe HH020
  (1 propiedad, 2 alquiler de mercado, 3 reducido, 4 cesión); la hipoteca se
  identifica porque la pregunta de retrasos en el pago de hipoteca o alquiler
  (HS010 hasta 2007, HS011 desde 2008) solo es aplicable (flag distinto de -2) a
  quien tiene hipoteca o paga alquiler. Validación en 2013 y 2019, con ambas
  variables: el 99 % de los propietarios HH021=2 tiene la pregunta aplicable y el
  99 % de los HH021=1 no la tiene.
- Indicador de acceso compuesto: hogares con responsable de 25-34 años en
  propiedad con hipoteca por cada 100 personas de 25-34 años. Recoge a la vez la
  emancipación y el acceso al crédito y no sufre el sesgo de selección de la
  distribución por régimen de tenencia (que solo mira a quienes ya se han
  emancipado).
- G13b: proporción de hogares con hipoteca entre los de responsable de 25-39 años,
  (a) por quintil de renta disponible equivalente del hogar (HY020/HX240) (quintiles calculados
  cada año sobre todos los hogares, de modo que mide la posición relativa) y
  (b) por tipo de contrato del responsable asalariado (PL140 hasta 2020; PL141
  desde 2021: 1x temporal, 2x indefinido).
"""
import csv, glob, os
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BR = os.path.join(BASE, 'datos', 'brutos')
T = os.path.join(BASE, 'tablas')
TRAMOS = [(16, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 120)]


def fichero(anio, t):
    yy = str(anio)[2:]
    if anio == 2025:
        return os.path.join(BR, 'ecv_2025', 'CSV', f'esudb25{t}.csv')
    return sorted(glob.glob(os.path.join(BR, 'ecv_hist', f'ext_{anio}', '**', f'esudb{yy}{t}.csv'),
                            recursive=True), key=len)[0]


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def leer(anio, t):
    return csv.DictReader(open(fichero(anio, t), encoding='latin1'))


def wquintiles(vals, ws):
    pares = sorted(zip(vals, ws))
    tot = sum(ws); cortes, acum, k = [], 0, 1
    for v, w in pares:
        acum += w
        while k < 5 and acum >= tot * k / 5:
            cortes.append(v); k += 1
    return cortes


def ola(anio):
    peso = {r['DB030']: fl(r['DB090']) or 0 for r in leer(anio, 'd')}
    personas, pob = {}, defaultdict(float)
    for r in leer(anio, 'p'):
        nac = fl(r['PB140'])
        if nac is None:
            continue
        edad = anio - int(nac)
        contrato = None
        if r.get('PL140', '').strip() in ('1', '2'):
            contrato = 'indefinido' if r['PL140'].strip() == '1' else 'temporal'
        elif r.get('PL141', '').strip()[:1] in ('1', '2'):
            contrato = 'temporal' if r['PL141'].strip()[:1] == '1' else 'indefinido'
        personas[r['PB030'].strip()] = (edad, contrato)
        if 25 <= edad <= 34:
            pob['25-34'] += fl(r['PB040']) or 0
    hogares = []
    for r in leer(anio, 'h'):
        hid = r['HB030'].strip(); w = peso.get(hid, 0)
        jefe = personas.get(r['HB080'].strip())
        if not jefe or not w:
            continue
        if 'HH021' in r:
            ten = {'1': 'prop_sin', '2': 'prop_hip', '3': 'alq_mercado', '4': 'alq_reducido',
                   '5': 'cesion'}.get(r['HH021'].strip())
        else:
            hs = 'HS010_F' if 'HS010_F' in r else 'HS011_F'
            c = r['HH020'].strip()
            ten = {'2': 'alq_mercado', '3': 'alq_reducido', '4': 'cesion'}.get(c)
            if c == '1':
                ten = 'prop_sin' if r[hs].strip() == '-2' else 'prop_hip'
        if not ten:
            continue
        # renta disponible equivalente: HY020 / HX240 (unidades de consumo, escala OCDE modificada)
        uc = fl(r.get('HX240'))
        hx = fl(r['HY020']) / uc if uc and fl(r['HY020']) is not None else None
        hogares.append(dict(edad=jefe[0], contrato=jefe[1], ten=ten, w=w,
                            renta=fl(r['HY020']), hx=hx))
    return hogares, pob


def main():
    filas, filas_b = [], []
    for anio in range(2004, 2026):
        hog, pob = ola(anio)
        for a, b in TRAMOS:
            sel = [h for h in hog if a <= h['edad'] <= b]
            tot = sum(h['w'] for h in sel)
            fila = dict(anio_encuesta=anio, tramo=f'{a}-{b}' if b < 120 else f'{a}+',
                        n_muestra=len(sel), hogares_miles=round(tot / 1000, 1))
            for k in ('prop_sin', 'prop_hip', 'alq_mercado', 'alq_reducido', 'cesion'):
                fila[f'pct_{k}'] = round(100 * sum(h['w'] for h in sel if h['ten'] == k) / tot, 2)
            if (a, b) == (25, 34):
                hip = sum(h['w'] for h in sel if h['ten'] == 'prop_hip')
                fila['hogares_por_100_personas_25_34'] = round(100 * tot / pob['25-34'], 2)
                fila['hogares_hipoteca_por_100_personas_25_34'] = round(100 * hip / pob['25-34'], 2)
            filas.append(fila)
        # G13b: renta y contrato, responsable de 25-39
        validos = [h for h in hog if h['hx'] is not None]
        clave = 'hx'
        cortes = wquintiles([h[clave] for h in validos], [h['w'] for h in validos])
        jov = [h for h in validos if 25 <= h['edad'] <= 39]
        for q in range(5):
            lo = cortes[q - 1] if q else float('-inf'); hi = cortes[q] if q < 4 else float('inf')
            sel = [h for h in jov if lo < h[clave] <= hi]
            tot = sum(h['w'] for h in sel)
            filas_b.append(dict(anio_encuesta=anio, grupo=f'quintil_{q + 1}', medida_renta=clave,
                                n_muestra=len(sel),
                                pct_prop_hip=round(100 * sum(h['w'] for h in sel if h['ten'] == 'prop_hip') / tot, 2) if tot else ''))
        for c in ('indefinido', 'temporal'):
            sel = [h for h in jov if h['contrato'] == c]
            tot = sum(h['w'] for h in sel)
            filas_b.append(dict(anio_encuesta=anio, grupo=f'contrato_{c}', medida_renta='',
                                n_muestra=len(sel),
                                pct_prop_hip=round(100 * sum(h['w'] for h in sel if h['ten'] == 'prop_hip') / tot, 2) if tot else ''))
        print(anio, 'ok', len(hog))
    for nombre, fs in (('G13_espana_tenencia_hipoteca_por_edad_2004_2025.csv', filas),
                       ('G13b_espana_hipoteca_jovenes_por_renta_y_contrato_2004_2025.csv', filas_b)):
        campos = list(dict.fromkeys(k for f in fs for k in f))
        with open(os.path.join(T, nombre), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(fs)


if __name__ == '__main__':
    main()
