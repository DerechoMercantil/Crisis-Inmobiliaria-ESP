#!/usr/bin/env python3
"""Versiones interactivas (HTML) de las gráficas de la monografía.

- Tooltip con el valor exacto al pasar el cursor (hover unificado por año).
- Misma paleta categórica validada, mismos títulos y fuentes que las versiones estáticas.
- Salida: graficas/interactivas/*.html + index.html (galería).
- Autocontenidas frente a GitHub Pages: un único plotly.min.js compartido en el directorio.
"""
import csv, os, sys
import plotly.graph_objects as go
import plotly.io as pio

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
T = os.path.join(BASE, 'tablas')
OUT = os.path.join(BASE, 'graficas', 'interactivas')
os.makedirs(OUT, exist_ok=True)

COLOR = ['#2a78d6', '#1baf7a', '#eda100', '#008300', '#4a3aa7', '#e34948', '#e87ba4', '#eb6834']
TINTA, TINTA2, MUTED, REJILLA = '#0b0b0b', '#52514e', '#898781', '#e1e0d9'

PLANTILLA = go.layout.Template()
PLANTILLA.layout = dict(
    font=dict(family='system-ui, -apple-system, Segoe UI, sans-serif', color=TINTA2, size=13),
    paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
    xaxis=dict(gridcolor=REJILLA, linecolor='#c3c2b7', ticks='outside', tickcolor='#c3c2b7', zeroline=False),
    yaxis=dict(gridcolor=REJILLA, linecolor='#c3c2b7', ticks='outside', tickcolor='#c3c2b7', zeroline=False),
    hovermode='x unified', hoverlabel=dict(bgcolor='white', font=dict(color=TINTA, size=12)),
    legend=dict(orientation='h', yanchor='bottom', y=1.0, x=0),
    margin=dict(l=70, r=30, t=110, b=90),
)

FICHAS = []  # (archivo, titulo) para el índice


def leer(nombre):
    with open(os.path.join(T, nombre)) as f:
        return list(csv.DictReader(f))


def col(rows, campo, anio='anio', fin=2025):
    xs, ys = [], []
    for r in rows:
        y = int(r[anio])
        if y > fin or not r[campo]:
            continue
        xs.append(y); ys.append(float(r[campo]))
    return xs, ys


def guardar(fig, nombre, titulo, subtitulo, fuente):
    fig.update_layout(
        template=PLANTILLA,
        title=dict(text=f'<b>{titulo}</b><br><sup style="color:{TINTA2}">{subtitulo}</sup>',
                   font=dict(size=17, color=TINTA), x=0, xanchor='left'),
        annotations=list(fig.layout.annotations) + [dict(
            text=fuente, xref='paper', yref='paper', x=0, y=-0.16, xanchor='left',
            showarrow=False, font=dict(size=10, color=MUTED))],
    )
    ruta = os.path.join(OUT, f'{nombre}.html')
    pio.write_html(fig, ruta, include_plotlyjs='plotly.min.js', full_html=True,
                   config={'displaylogo': False, 'locale': 'es',
                           'modeBarButtonsToRemove': ['lasso2d', 'select2d']})
    FICHAS.append((f'{nombre}.html', titulo))


def linea(fig, x, y, i, nombre, unidad='', dec=1):
    fig.add_trace(go.Scatter(
        x=x, y=y, name=nombre, mode='lines',
        line=dict(color=COLOR[i % len(COLOR)], width=2.4),
        hovertemplate=f'%{{y:,.{dec}f}}{unidad}<extra>{nombre}</extra>'))


ES = dict(separators=',.')  # decimal coma, millar punto


def fig_base(ytitulo=''):
    fig = go.Figure()
    fig.update_layout(yaxis_title=ytitulo, separators=',.')
    return fig


# ---------- G1 ----------
rows = leer('G1_espana_ratio_precio_rbd_anual.csv')
x, y = col(rows, 'precio_vivienda_en_anios_de_rbd_hogar_mediano')
fig = fig_base('Años de renta bruta del hogar mediano')
linea(fig, x, y, 0, 'España', ' años')
fig.update_yaxes(range=[0, 10])
guardar(fig, 'G01_ratio_precio_renta_espana',
        'El precio de la vivienda, en años de renta de un hogar mediano (España)',
        'Precio medio de una vivienda libre de 93,75 m² construidos / renta bruta anual del hogar mediano. 1987-2025.',
        'Fuente: Banco de España, Síntesis de Indicadores, cuadro 1.5 (serie SI_1_5.43). Elaboración propia.')

# ---------- G1b ----------
rows = leer('G1b_espana_precio_vs_renta_indexado.csv')
x, p = col(rows, 'indice_precio_1987_100')
_, r = col(rows, 'indice_rbd_1987_100')
fig = fig_base('Índice, 1987 = 100')
linea(fig, x, p, 0, 'Precio del m² de vivienda libre')
linea(fig, x, r, 1, 'Renta bruta del hogar mediano')
guardar(fig, 'G01b_precio_vs_renta_indexado',
        'El precio de la vivienda se multiplica por 8; la renta por hogar, por 2,6 (1987-2025)',
        'Índices nominales, base 1987 = 100. Serie de precio enlazada (Mº Fomento base 1987 / MIVAU 1995-).',
        'Fuente: Mº de Fomento (1987-94, en Vergés, Estadística Española 179/2012); MIVAU y Banco de España (1995-2025). Elaboración propia.')

# ---------- G1bis ----------
rows = leer('G1bis_espana_ratio_precio_rbd_anual_1971.csv')
retro = [(int(r['anio']), float(r['precio_vivienda_en_anios_de_rbd_hogar_mediano']))
         for r in rows if r['metodo'].startswith('retropolación')]
oficial = [(int(r['anio']), float(r['precio_vivienda_en_anios_de_rbd_hogar_mediano']))
           for r in rows if r['metodo'] == 'serie oficial BdE' and int(r['anio']) <= 2025]
xr, yr = zip(*retro)
xo, yo = zip(*oficial)
xr, yr = list(xr) + [xo[0]], list(yr) + [yo[0]]
fig = fig_base('Años de renta bruta del hogar mediano')
fig.add_trace(go.Scatter(x=xr, y=yr, name='Retropolación 1971-1986 (BIS y Prados de la Escosura)',
                         mode='lines', line=dict(color=COLOR[0], width=2.2, dash='dash'),
                         hovertemplate='%{y:,.2f} años<extra>Retropolación</extra>'))
fig.add_trace(go.Scatter(x=xo, y=yo, name='Serie oficial del Banco de España (1987-2025)',
                         mode='lines', line=dict(color=COLOR[0], width=2.4),
                         hovertemplate='%{y:,.2f} años<extra>Serie oficial BdE</extra>'))
fig.update_yaxes(range=[0, 10])
guardar(fig, 'G01bis_ratio_precio_renta_espana_1971',
        'Medio siglo de precio de la vivienda, en años de renta del hogar mediano (España)',
        'Precio medio de una vivienda libre de 93,75 m² construidos / renta bruta anual del hogar mediano. 1971-2025. '
        'Tramo 1971-1986 retropolado: precios BIS enlazados a la serie de Fomento; renta según Prados de la Escosura y hogares censales (método de G10).',
        'Fuente: Banco de España (SI_1_5.43, 1987-); BIS, Selected residential property prices; Prados de la Escosura (2017, act. 2025); censos INE. Elaboración propia.')

# ---------- G2 / G2b ----------
PAISES = [('Espana', 'España', 0), ('Italia', 'Italia', 1), ('ReinoUnido', 'Reino Unido', 2),
          ('Hungria', 'Hungría', 3), ('ZonaEuro', 'Zona euro', 4)]
for tabla, nombre, titulo, sub, fuente in [
    ('G2_ratio_precio_renta_anual.csv', 'G02_ratio_precio_renta_comparativa',
     'Precio de la vivienda sobre renta por hogar: cinco mercados, un mismo destino',
     'Ratio precio/renta por hogar, índice 2015 = 100. 1970-2025 (Hungría desde 2007; Reino Unido desde 1987).',
     'Fuente: OCDE, Analytical House Prices Indicators (price-to-income ratio). Elaboración propia.'),
    ('G2b_ratio_precio_renta_estandarizado_anual.csv', 'G02b_ratio_estandarizado_comparativa',
     'Sobrevaloración de la vivienda respecto a la renta: desviación sobre la media histórica',
     'Ratio precio/renta estandarizado: 100 = media de largo plazo de cada país. La OCDE no calcula esta serie para Hungría.',
     'Fuente: OCDE, Analytical House Prices Indicators (standardised price-to-income ratio). Elaboración propia.')]:
    rows = leer(tabla)
    fig = fig_base('Índice')
    for campo, etiqueta, i in PAISES:
        x, y = col(rows, campo)
        if x:
            linea(fig, x, y, i, etiqueta)
    if 'estandarizado' in tabla:
        fig.add_hline(y=100, line_color='#c3c2b7', line_width=1)
    guardar(fig, nombre, titulo, sub, fuente)

# ---------- G3 ----------
rows = leer('G3_espana_ipc_vs_vivienda_anual.csv')
x, pv = col(rows, 'precio_vivienda_nominal_1971_100')
_, ipc = col(rows, 'ipc_1971_100')
_, real = col(rows, 'precio_vivienda_real_1971_100')
fig = fig_base('Índice, 1971 = 100 (escala logarítmica)')
linea(fig, x, pv, 0, 'Precio de la vivienda (nominal)', dec=0)
linea(fig, x, ipc, 1, 'IPC (inflación acumulada)', dec=0)
linea(fig, x, real, 2, 'Precio de la vivienda real (deflactado)', dec=0)
fig.update_yaxes(type='log')
guardar(fig, 'G03_espana_inflacion_vs_vivienda',
        'Vivienda e inflación en España desde 1971: ×84 nominal, ×24 el IPC, ×3,4 real',
        'Índices base 1971 = 100, escala logarítmica. Medias anuales.',
        'Fuente: BIS, Selected residential property prices (España; proveedor: Banco de España) y BIS Long consumer prices. Elaboración propia.')

# ---------- G4 ----------
rows = leer('G4_comparativa_precios_reales_anual.csv')
fig = fig_base('Índice real, 2015 = 100')
for campo, etiqueta, i in PAISES:
    xs, ys = [], []
    for rr in rows:
        yy = int(rr['anio'])
        if 1971 <= yy <= 2025 and rr[campo]:
            xs.append(yy); ys.append(float(rr[campo]))
    if xs:
        linea(fig, xs, ys, i, etiqueta)
guardar(fig, 'G04_comparativa_precios_reales',
        'Precios reales de la vivienda: Hungría, el país más "burbujeado" del panel',
        'Índice de precios de la vivienda deflactado por el IPC nacional, base 2015 = 100. 1971-2025 (Hungría desde 1992).',
        'Fuente: BIS, Selected residential property prices (series reales). Elaboración propia.')

# ---------- G5 ----------
rows = leer('G5_espana_transferencia_alquiler_por_edad.csv')
tramos = ['16-29', '30-44', '45-64', '65+']
etiq = ['16-29 años', '30-44 años', '45-64 años', '65 y más']
paga = [float(r['alquiler_pagado_mill_eur'])/1000 for r in rows if r['tramo_edad'] in tramos]
cobra = [float(r['alquiler_cobrado_mill_eur'])/1000 for r in rows if r['tramo_edad'] in tramos]
resid = next(float(r['alquiler_cobrado_mill_eur'])/1000 for r in rows if r['tramo_edad'].startswith('empresas'))
fig = fig_base('')
fig.add_trace(go.Bar(y=etiq, x=paga, name='Alquiler pagado', orientation='h',
                     marker_color=COLOR[0],
                     hovertemplate='%{x:,.1f} miles de millones €<extra>Pagado, %{y}</extra>'))
fig.add_trace(go.Bar(y=etiq, x=cobra, name='Alquiler cobrado', orientation='h',
                     marker_color=COLOR[5],
                     hovertemplate='%{x:,.1f} miles de millones €<extra>Cobrado, %{y}</extra>'))
fig.update_layout(barmode='group', xaxis_title='Miles de millones de euros al año',
                  yaxis=dict(autorange='reversed'), hovermode='closest')
guardar(fig, 'G05_transferencia_alquiler_edad',
        'Quién paga y quién cobra el alquiler en España, por edad',
        f'Alquiler anual pagado y cobrado por los hogares, según edad de la persona de referencia (ECV 2025). '
        f'Además, {resid:.1f} miles de millones € van a empresas, alquiler no declarado y otros.'.replace('.', ','),
        'Fuente: elaboración propia sobre microdatos de la Encuesta de Condiciones de Vida 2025 (INE).')

# ---------- G6 ----------
rows = leer('G6_espana_riqueza_neta_mediana_por_edad.csv')
grupos6 = [('mediana_miles_eur_2024_menor_de_35', 'Menos de 35', 0),
           ('mediana_miles_eur_2024_entre_35_y_44', '35-44', 1),
           ('mediana_miles_eur_2024_entre_45_y_54', '45-54', 2),
           ('mediana_miles_eur_2024_entre_55_y_64', '55-64', 3),
           ('mediana_miles_eur_2024_entre_65_y_74', '65-74', 4),
           ('mediana_miles_eur_2024_mayor_de_75', '75 y más', 5)]
fig = fig_base('Miles de euros de 2024')
for campo, etiqueta, i in grupos6:
    x, y = col(rows, campo, fin=2024)
    fig.add_trace(go.Scatter(x=x, y=y, name=etiqueta, mode='lines+markers',
                             line=dict(color=COLOR[i], width=2.4), marker=dict(size=6),
                             hovertemplate='%{y:,.1f} mil €<extra>' + etiqueta + '</extra>'))
guardar(fig, 'G06_riqueza_por_edad_espana',
        'La riqueza de los jóvenes se hunde: de 104.000 € (2005) a 23.000 € (2024)',
        'Riqueza neta mediana de los hogares por edad del cabeza de familia. Miles de euros constantes de 2024. Olas EFF 2002-2024.',
        'Fuente: Banco de España, Encuesta Financiera de las Familias (EFF), resultados oficiales. Elaboración propia.')

# ---------- G7 ----------
rows = leer('G7_eeuu_riqueza_por_edad_anual.csv')
grupos7 = [('pct_riqueza_neta_menores_40', 'Menores de 40', 0), ('pct_riqueza_neta_40_54', '40-54', 1),
           ('pct_riqueza_neta_55_69', '55-69', 2), ('pct_riqueza_neta_70_o_mas', '70 y más', 3)]
fig = fig_base('% de la riqueza neta total de los hogares')
for campo, etiqueta, i in grupos7:
    x, y = col(rows, campo)
    linea(fig, x, y, i, etiqueta, unidad=' %')
guardar(fig, 'G07_eeuu_riqueza_por_edad',
        'EE.UU.: los menores de 40 años pasan del 12% al 7% de la riqueza (1989-2025)',
        'Participación de cada grupo de edad en la riqueza neta total de los hogares. Medias anuales.',
        'Fuente: Reserva Federal, Distributional Financial Accounts. Elaboración propia.')

# ---------- G8a ----------
rows = leer('G8a_espana_viviendas_iniciadas_anual.csv')
x, tot = col(rows, 'iniciadas_total')
_, prot = col(rows, 'iniciadas_protegidas')
xl, lib = col(rows, 'iniciadas_libres')
fig = fig_base('Miles de viviendas iniciadas al año')
linea(fig, x, [v/1000 for v in tot], 0, 'Total iniciadas', dec=1)
linea(fig, xl, [v/1000 for v in lib], 1, 'Libres', dec=1)
linea(fig, x, [v/1000 for v in prot], 2, 'Protegidas', dec=1)
fig.add_vrect(x0=1970, x1=1980, fillcolor=REJILLA, opacity=0.35, line_width=0,
              annotation_text='Hasta 1979 el total solo recoge protegidas',
              annotation_position='top left', annotation_font=dict(size=10, color=MUTED))
guardar(fig, 'G08a_viviendas_iniciadas',
        'La vivienda protegida se desploma: de 250.000 iniciadas al año a menos de 20.000',
        'Viviendas iniciadas en España por régimen, 1970-2025.',
        'Fuente: Mº de Vivienda y Agenda Urbana, vía Banco de España (Síntesis de Indicadores, cuadro 1.5). Elaboración propia.')

# ---------- G8b ----------
rows = leer('G8b_espana_compraventas_anual.csv')
x, tot = col(rows, 'compraventas_total')
_, nue = col(rows, 'vivienda_nueva')
_, usa = col(rows, 'vivienda_usada')
fig = fig_base('Miles de compraventas al año')
linea(fig, x, [v/1000 for v in tot], 0, 'Total', dec=1)
linea(fig, x, [v/1000 for v in nue], 1, 'Vivienda nueva', dec=1)
linea(fig, x, [v/1000 for v in usa], 2, 'Vivienda usada', dec=1)
guardar(fig, 'G08b_compraventas',
        'El mercado pos-burbuja es de segunda mano: la vivienda nueva no se recupera',
        'Compraventas de vivienda ante notario en España, 2004-2025.',
        'Fuente: Mº de Vivienda y Agenda Urbana (Consejo General del Notariado), vía Banco de España. Elaboración propia.')

# ---------- G9 ----------
rows = leer('G9_ue_permisos_viviendas_anual.csv')
for campo, etiqueta, i in [('EU27_2020', 'UE-27', 0), ('ES', 'España', 1), ('IT', 'Italia', 2), ('HU', 'Hungría', 3)]:
    pass
fig = fig_base('Miles de viviendas autorizadas (escala logarítmica)')
for campo, etiqueta, i in [('EU27_2020', 'UE-27', 0), ('ES', 'España', 1), ('IT', 'Italia', 2), ('HU', 'Hungría', 3)]:
    x, y = col(rows, campo)
    linea(fig, x, y, i, etiqueta, dec=1)
fig.update_yaxes(type='log')
guardar(fig, 'G09_permisos_ue',
        'Permisos de construcción de vivienda: la UE construye la mitad que en 2006',
        'Viviendas en permisos de construcción (edificios residenciales, miles). 2005-2025. Escala logarítmica.',
        'Fuente: Eurostat, Building permits (sts_cobp_a). Elaboración propia.')

# ---------- G10 ----------
rows = leer('G10_espana_vpo_precio_maximo_1979_2025.csv')
x, vpo = col(rows, 'vpo_en_anios_de_renta')
r1 = leer('G1_espana_ratio_precio_rbd_anual.csv')
xl, libre = col(r1, 'precio_vivienda_en_anios_de_rbd_hogar_mediano')
fig = fig_base('Años de renta bruta del hogar mediano')
linea(fig, xl, libre, 0, 'Vivienda libre (93,75 m² construidos)', ' años')
linea(fig, x, vpo, 1, 'VPO régimen general (90 m² útiles)', ' años')
fig.update_yaxes(range=[0, 10])
guardar(fig, 'G10_vpo_en_anios_de_renta',
        'La vivienda protegida también se encarece: de 2,5 años de renta (1997) a 4,2 (2025)',
        'Precio máximo legal de una VPO de 90 m² útiles (área media nacional) y precio de la vivienda libre, en años de renta del hogar mediano.',
        'Fuente: elaboración propia a partir del BOE, Banco de España y Prados de la Escosura (renta 1979-86). Detalle en tablas/FUENTES.md.')

# ---------- índice ----------
tarjetas = '\n'.join(
    f'<li><a href="{a}">{t}</a></li>' for a, t in FICHAS)
html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gráficas interactivas — monografía burbuja inmobiliaria</title>
<style>
 body {{ font-family: system-ui, -apple-system, 'Segoe UI', sans-serif; color: #0b0b0b;
        max-width: 46rem; margin: 3rem auto; padding: 0 1rem; line-height: 1.5; }}
 h1 {{ font-size: 1.5rem; }} p {{ color: #52514e; }}
 li {{ margin: .45rem 0; }} a {{ color: #2a78d6; }}
 footer {{ margin-top: 2.5rem; font-size: .85rem; color: #898781; }}
</style></head><body>
<h1>Gráficas interactivas de la monografía</h1>
<p>Cada gráfica muestra el valor exacto al pasar el cursor. Las versiones para imprenta (B/N)
y en color, las tablas de datos y la memoria de fuentes están en el repositorio.</p>
<ol>
{tarjetas}
</ol>
<footer>Fuentes: Banco de España, INE, MIVAU, BOE, Eurostat, OCDE, BIS, Reserva Federal,
Prados de la Escosura. Detalle serie a serie en <code>tablas/FUENTES.md</code>.</footer>
</body></html>"""
open(os.path.join(OUT, 'index.html'), 'w').write(html)
print(f'{len(FICHAS)} gráficas interactivas + index.html en {OUT}')
