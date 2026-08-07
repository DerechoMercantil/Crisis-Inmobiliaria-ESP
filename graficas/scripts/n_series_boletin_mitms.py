#!/usr/bin/env python3
"""Procesa los XLS del Boletín estadístico online del MITMS/MIVAU
(apps.fomento.gob.es/boletinonline2) para los nuevos grupos de datos N2, N5 y N6.

Ficheros esperados en datos/brutos/ (descarga documentada en tablas/FUENTES.md):
- mitms_32201000.xls  viviendas libres terminadas, anual 1991-, CCAA/prov
- mitms_31306000.xls  VPO: calificaciones definitivas (= terminadas), anual 1991-, CCAA/prov
- mitms_31206010.xls  VPO: calif. definitivas promotor PRIVADO, mensual 2014-
- mitms_31206020.xls  VPO: calif. definitivas promotor PÚBLICO, mensual 2014-
- mitms_31203010.xls  VPO: calif. provisionales promotor PRIVADO, mensual 2014-
- mitms_31203020.xls  VPO: calif. provisionales promotor PÚBLICO, mensual 2014-
- mitms_36400500.xls  precio medio m² suelo urbano, trimestral 2004-, total nacional
- mitms_36403000.xls  ídem, municipios de más de 50.000 habitantes
"""
import csv, os, re
import xlrd

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
BRUTOS = os.path.join(BASE, 'datos', 'brutos')
TABLAS = os.path.join(BASE, 'tablas')
PROC = os.path.join(BASE, 'datos', 'procesados')


def abrir(nombre):
    return xlrd.open_workbook(os.path.join(BRUTOS, f'mitms_{nombre}.xls')).sheet_by_index(0)


def fila_total(sh):
    """Localiza la fila del total nacional (TOTAL NACIONAL / España)."""
    for r in range(sh.nrows):
        for c in range(min(3, sh.ncols)):
            v = str(sh.cell_value(r, c)).strip().upper()
            if v in ('TOTAL NACIONAL', 'ESPAÑA'):
                return r
    raise ValueError('sin fila de total nacional')


def serie_anual(nombre):
    """Tabla anual: fila de años (floats) + fila total nacional."""
    sh = abrir(nombre)
    rt = fila_total(sh)
    # fila de años: la última fila por encima del total cuyo contenido son años
    for r in range(rt - 1, -1, -1):
        anios = {c: int(sh.cell_value(r, c)) for c in range(sh.ncols)
                 if isinstance(sh.cell_value(r, c), float) and 1950 < sh.cell_value(r, c) < 2030}
        if len(anios) >= 5:
            out = {}
            for c, a in anios.items():
                v = sh.cell_value(rt, c)
                if isinstance(v, float):
                    out[a] = v
            return out
    raise ValueError('sin fila de años')


def serie_mensual_por_anio(nombre):
    """Tabla mensual: cabecera 'AAAA por meses' agrupando 12 columnas."""
    sh = abrir(nombre)
    rt = fila_total(sh)
    # localizar la fila con 'por meses'
    ranios = None
    for r in range(rt):
        if any('por meses' in str(sh.cell_value(r, c)) for c in range(sh.ncols)):
            ranios = r
            break
    grupos = {}   # col inicial -> año
    for c in range(sh.ncols):
        m = re.match(r'(\d{4}) por meses', str(sh.cell_value(ranios, c)))
        if m:
            grupos[c] = int(m.group(1))
    out = {}
    cols = sorted(grupos)
    for i, c0 in enumerate(cols):
        c1 = cols[i + 1] if i + 1 < len(cols) else sh.ncols
        vals = [sh.cell_value(rt, c) for c in range(c0, c1)]
        vals = [v for v in vals if isinstance(v, float)]
        if vals:
            out[grupos[c0]] = (sum(vals), len(vals))
    return out


def serie_trimestral(nombre):
    """Tabla trimestral tipo suelo: cabecera 'Año AAAA' cada 4 columnas."""
    sh = abrir(nombre)
    rt = fila_total(sh)
    ranios = None
    grupos = {}
    for r in range(rt):
        for c in range(sh.ncols):
            m = re.match(r'Año (\d{4})', str(sh.cell_value(r, c)))
            if m:
                grupos[c] = int(m.group(1))
                ranios = r
        if grupos:
            break
    out = {}
    cols = sorted(grupos)
    for i, c0 in enumerate(cols):
        c1 = cols[i + 1] if i + 1 < len(cols) else sh.ncols
        vals = [sh.cell_value(rt, c) for c in range(c0, c1)]
        vals = [v for v in vals if isinstance(v, float) and v > 0]
        if len(vals) == 4:                            # solo años completos
            out[grupos[c0]] = sum(vals) / len(vals)   # media anual de trimestres
    return out


def leer_bde(nombre):
    """Series mensuales ya procesadas del BdE (datos/procesados)."""
    out = {}
    with open(os.path.join(PROC, f'{nombre}.csv')) as f:
        for r in csv.DictReader(f):
            y = int(r['anio'])
            out.setdefault(y, []).append(float(r['valor']))
    return {y: (sum(v), len(v)) for y, v in out.items()}


# ---------- N6: terminadas anual 1991- ----------
libres_term = serie_anual('32201000')
vpo_def = serie_anual('31306000')
with open(os.path.join(TABLAS, 'N6_espana_terminadas_anual.csv'), 'w') as f:
    w = csv.writer(f)
    w.writerow(['anio', 'libres_terminadas', 'vpo_calificaciones_definitivas', 'total'])
    for y in sorted(set(libres_term) | set(vpo_def)):
        lt, vd = libres_term.get(y), vpo_def.get(y)
        w.writerow([y, round(lt) if lt else '', round(vd) if vd else '',
                    round((lt or 0) + (vd or 0)) if lt and vd else ''])

# ---------- N6: décadas desde iniciadas (BdE 1970-) ----------
ini_prot = leer_bde('mivau_viv_iniciadas_protegidas')
ini_lib = leer_bde('mivau_viv_iniciadas_libres')
decadas = [(1976, 1985), (1986, 1995), (1996, 2005), (2006, 2015), (2016, 2025)]
with open(os.path.join(TABLAS, 'N6_espana_iniciadas_por_decadas.csv'), 'w') as f:
    w = csv.writer(f)
    w.writerow(['periodo', 'iniciadas_libres', 'iniciadas_protegidas', 'total',
                'pct_protegidas', 'nota'])
    for a0, a1 in decadas:
        lib = sum(ini_lib[y][0] for y in range(a0, a1 + 1) if y in ini_lib and ini_lib[y][1] == 12)
        pro = sum(ini_prot[y][0] for y in range(a0, a1 + 1) if y in ini_prot and ini_prot[y][1] == 12)
        nota = 'libres solo desde 1980' if a0 < 1980 else ''
        tot = lib + pro
        w.writerow([f'{a0}-{a1}', round(lib), round(pro), round(tot),
                    round(100 * pro / tot, 1) if tot else '', nota])

# ---------- N2: VPO por promotor (mensual 2014- -> anual) ----------
priv_def = serie_mensual_por_anio('31206010')
pub_def = serie_mensual_por_anio('31206020')
priv_prov = serie_mensual_por_anio('31203010')
pub_prov = serie_mensual_por_anio('31203020')
with open(os.path.join(TABLAS, 'N2_espana_vpo_por_promotor_anual.csv'), 'w') as f:
    w = csv.writer(f)
    w.writerow(['anio', 'definitivas_promotor_privado', 'definitivas_promotor_publico',
                'pct_publico_definitivas', 'provisionales_promotor_privado',
                'provisionales_promotor_publico', 'nota'])
    for y in sorted(set(priv_def) | set(pub_def)):
        pd_, pb = priv_def.get(y, (None, 0)), pub_def.get(y, (None, 0))
        pv, pb2 = priv_prov.get(y, (None, 0)), pub_prov.get(y, (None, 0))
        nota = '' if pd_[1] == 12 else f'año incompleto ({pd_[1]} meses)'
        tot = (pd_[0] or 0) + (pb[0] or 0)
        w.writerow([y, round(pd_[0]) if pd_[0] is not None else '',
                    round(pb[0]) if pb[0] is not None else '',
                    round(100 * pb[0] / tot, 1) if tot else '',
                    round(pv[0]) if pv[0] is not None else '',
                    round(pb2[0]) if pb2[0] is not None else '', nota])

# ---------- N5: precio del suelo urbano 2004- ----------
suelo_nac = serie_trimestral('36400500')
suelo_50k = serie_trimestral('36403000')
with open(os.path.join(TABLAS, 'N5_espana_precio_suelo_anual.csv'), 'w') as f:
    w = csv.writer(f)
    w.writerow(['anio', 'precio_suelo_eur_m2_nacional', 'precio_suelo_eur_m2_mun_mas_50k'])
    for y in sorted(set(suelo_nac) | set(suelo_50k)):
        w.writerow([y, round(suelo_nac.get(y, 0), 1) or '', round(suelo_50k.get(y, 0), 1) or ''])

print('Tablas N2, N5 y N6 generadas.')
