"""Construye tablas/G19_espana_emancipacion_y_alquiler_de_entrada_2005_2025.csv.

Coste efectivo de emanciparse, medido con los ficheros LONGITUDINALES de la ECV (INE):
la ECV sigue a las mismas personas durante cuatro años, de modo que se puede observar a
quien vivía con sus padres en un año y vive en su propio hogar al año siguiente.

Paneles (sin solapamiento de transiciones): 2005-2008 (base 2004), 2009-2012,
2015-2018 y 2022-2025 (base 2013). Descarga: INE, ecv_b2004/ y ecv_b2013/periodo_*.zip.

Definiciones, para cada par de años consecutivos (t-1, t) dentro de un panel:
- Persona de 18 a 34 años en t, presente en ambos años.
- «Vivía con sus padres» en t-1: en su hogar figuraba su padre o su madre (RB220 o RB230)
  y no era responsable de la vivienda (HB080/HB090).
- «Se emancipa» en t: su hogar es otro (RB040 distinto), sin padre ni madre, y es
  responsable de la vivienda o cónyuge del responsable (RB240).
- Destino: régimen de tenencia del nuevo hogar (HH021; en 2005-2008, HH020 y la pregunta
  de retrasos HS010/HS011 para distinguir la hipoteca, como en g13).
- Alquiler de entrada: HH060 del nuevo hogar en alquiler de mercado, en euros de 2024
  (IPC de España del año t). Comparación: hogares con responsable de 25-34 años en
  alquiler de mercado que NO cambian de hogar entre t-1 y t (alquiler del incumbente).
- Renta: HY020 del nuevo hogar (renta del año anterior de sus miembros); en el panel de
  base 2004 se enlaza con k_hogar = 1,146.
- Pesos: longitudinales de dos años de la persona (RB062), y RB060 si falta.
"""
import csv, json, os
from collections import defaultdict
import g13_tenencia_hipoteca_por_edad as g13
from g14_alquiler_ahorro_por_edad import ipc_anual, wmediana

BR = os.path.join(g13.BR, 'ecv_long')
K_HOG = json.load(open(os.path.join(g13.BASE, 'datos', 'procesados', 'g1c_enlace_ecv_bases.json')))['k_hogar']
PANELES = [('2005-2008', 'p0508/es08r.csv', 'p0508/es08h.csv', ',', True),
           ('2009-2012', 'p0912/es12r.csv', 'p0912/es12h.csv', ',', False),
           ('2015-2018', 'p1518/es18r.csv', 'p1518/es18h.csv', ',', False),
           ('2022-2025', 'p2225/CSV/ECV_Lr_22a25.tab', 'p2225/CSV/ECV_Lh_22a25.tab', '\t', False)]


def filas(ruta, sep):
    with open(os.path.join(BR, ruta), encoding='latin1') as f:
        for r in csv.DictReader(f, delimiter=sep):
            yield {k.strip('" '): (v or '').strip('" ') for k, v in r.items() if k}


def tenencia(r):
    t = r.get('HH021', '')
    if t:
        return {'1': 'prop_sin', '2': 'prop_hip', '3': 'alq_mercado', '4': 'otros', '5': 'otros'}.get(t)
    c = r.get('HH020', '')
    if c == '1':
        hs = r.get('HS011_F', '') if r.get('HS011_F', '') not in ('', '-5') else r.get('HS010_F', '')
        return 'prop_sin' if hs == '-2' else 'prop_hip'
    return {'2': 'alq_mercado', '3': 'otros', '4': 'otros'}.get(c)


def panel(nombre, fr, fh, sep, base2004, ipc):
    per = {}
    for r in filas(fr, sep):
        try:
            per[(int(r['RB010']), r['RB030'])] = dict(
                hid=r['RB040'], nac=int(r['RB080']) if r['RB080'] else None,
                padre=r.get('RB220', ''), madre=r.get('RB230', ''), conyuge=r.get('RB240', ''),
                w=g13.fl(r.get('RB062')) or g13.fl(r.get('RB060')) or 0)
        except ValueError:
            continue
    hog = {}
    for r in filas(fh, sep):
        hog[(int(r['HB010']), r['HB030'])] = dict(resp={r.get('HB080', ''), r.get('HB090', '')} - {''},
                                                  ten=tenencia(r), alq=g13.fl(r.get('HH060')),
                                                  y=g13.fl(r.get('HY020')))
    k = K_HOG if base2004 else 1.0
    n_pob = n_em = 0
    pob = em = 0.0; destino = defaultdict(float); alq_ent, esf_ent, ren_ent = [], [], []; alq_inc = []
    anios = sorted({a for a, _ in per})
    for t in anios[1:]:
        defl = ipc[2024] / ipc[t]
        for (a, pid), p in per.items():
            if a != t or p['nac'] is None or not 18 <= t - p['nac'] <= 34:
                continue
            q = per.get((t - 1, pid))
            if not q:
                continue
            h0 = hog.get((t - 1, q['hid'])); h1 = hog.get((t, p['hid']))
            if not h0 or not h1:
                continue
            if (q['padre'] or q['madre']) and pid not in h0['resp']:
                pob += p['w']; n_pob += 1
                es_resp = pid in h1['resp'] or (p['conyuge'] and p['conyuge'] in h1['resp'])
                if p['hid'] != q['hid'] and not (p['padre'] or p['madre']) and es_resp:
                    em += p['w']; n_em += 1; destino[h1['ten'] or 'n/d'] += p['w']
                    if h1['ten'] == 'alq_mercado' and h1['alq'] and h1['y'] and h1['y'] > 0:
                        alq_ent.append((h1['alq'] * defl, p['w']))
                        esf_ent.append((12 * h1['alq'] / (h1['y'] * k), p['w']))
                        ren_ent.append((h1['y'] * k / 12 * (ipc[2024] / ipc[t - 1]), p['w']))
        # incumbentes: hogares con responsable de 25-34 años en alquiler de mercado que no cambian
        for (a, hid), h in hog.items():
            if a != t or h['ten'] != 'alq_mercado' or not h['alq']:
                continue
            h0 = hog.get((t - 1, hid))
            if not h0 or h0['ten'] != 'alq_mercado':
                continue
            resp = [per.get((t, x)) for x in h['resp']]
            resp = [x for x in resp if x and x['nac'] and 25 <= t - x['nac'] <= 34 and x['hid'] == hid]
            if resp:
                alq_inc.append((h['alq'] * defl, resp[0]['w']))
    tot = sum(destino.values()) or 1
    return dict(panel=nombre, transiciones=f'{anios[0]}-{anios[-1]}',
                n_jovenes_con_padres=n_pob, n_emancipaciones=n_em,
                tasa_emancipacion_anual_pct=round(100 * em / pob, 1) if pob else '',
                destino_alquiler_mercado_pct=round(100 * destino['alq_mercado'] / tot, 1),
                destino_propiedad_hipoteca_pct=round(100 * destino['prop_hip'] / tot, 1),
                destino_propiedad_sin_hipoteca_pct=round(100 * destino['prop_sin'] / tot, 1),
                destino_otros_pct=round(100 * (destino['otros'] + destino['n/d']) / tot, 1),
                n_entrantes_alquiler=len(alq_ent),
                alquiler_entrada_mediano_eur2024=round(wmediana(alq_ent)) if alq_ent else '',
                esfuerzo_entrada_mediano_pct=round(100 * wmediana(esf_ent), 1) if esf_ent else '',
                renta_hogar_entrante_mensual_mediana_eur2024=round(wmediana(ren_ent)) if ren_ent else '',
                n_incumbentes=len(alq_inc),
                alquiler_incumbente_mediano_eur2024=round(wmediana(alq_inc)) if alq_inc else '',
                ratio_entrada_incumbente=round(wmediana(alq_ent) / wmediana(alq_inc), 2) if alq_ent and alq_inc else '',
                ), destino


def main():
    ipc = ipc_anual(); out = []
    for args in PANELES:
        fila, _ = panel(*args, ipc)
        out.append(fila); print(fila)
    campos = list(out[0])
    with open(os.path.join(g13.T, 'G19_espana_emancipacion_y_alquiler_de_entrada_2005_2025.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction='ignore'); w.writeheader(); w.writerows(out)


if __name__ == '__main__':
    main()
