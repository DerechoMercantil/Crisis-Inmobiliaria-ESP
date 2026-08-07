#!/usr/bin/env python3
"""Versiones interactivas (HTML + Plotly) de las gráficas N1-N6 y
regeneración del índice de la galería con todas las páginas presentes."""
import csv, os, re
import plotly.graph_objects as go
import plotly.io as pio

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
T = os.path.join(BASE, 'tablas')
OUT = os.path.join(BASE, 'graficas', 'interactivas')

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


def leer(nombre):
    with open(os.path.join(T, nombre)) as f:
        return list(csv.DictReader(f))


def guardar(fig, nombre, titulo, subtitulo, fuente):
    fig.update_layout(
        template=PLANTILLA, separators=',.',
        title=dict(text=f'<b>{titulo}</b><br><sup style="color:{TINTA2}">{subtitulo}</sup>',
                   font=dict(size=17, color=TINTA), x=0, xanchor='left'),
        annotations=list(fig.layout.annotations) + [dict(
            text=fuente, xref='paper', yref='paper', x=0, y=-0.16, xanchor='left',
            showarrow=False, font=dict(size=10, color=MUTED))],
    )
    pio.write_html(fig, os.path.join(OUT, f'{nombre}.html'),
                   include_plotlyjs='plotly.min.js', full_html=True,
                   config={'displaylogo': False, 'locale': 'es',
                           'modeBarButtonsToRemove': ['lasso2d', 'select2d']})


# ---------- N1 ----------
rows = leer('N1_espana_vpo_franquismo_anual.csv')
fig = go.Figure(go.Bar(
    x=[int(r['anio']) for r in rows], y=[float(r['vpo_terminadas']) for r in rows],
    marker_color=COLOR[0], name='VPO terminadas',
    hovertemplate='%{y:,.0f} viviendas<extra>%{x}</extra>'))
fig.update_layout(yaxis_title='Viviendas protegidas terminadas al año', showlegend=False)
guardar(fig, 'N01_vpo_franquismo',
        'La vivienda protegida del franquismo: hasta 241.000 terminadas en un año',
        'Viviendas acogidas a la protección del Estado terminadas (calificación definitiva), 1958-1975. Serie validada entre anuarios.',
        'Fuente: Anuarios Estadísticos de España (INE, fondo documental): anuarios 1965, 1971 y 1976. Elaboración propia.')

# ---------- N2 ----------
rows = [r for r in leer('N2_espana_vpo_por_promotor_anual.csv') if not r['nota']]
x = [int(r['anio']) for r in rows]
fig = go.Figure()
fig.add_trace(go.Bar(x=x, y=[float(r['definitivas_promotor_privado']) for r in rows],
                     name='Promotor privado', marker_color=COLOR[0],
                     hovertemplate='%{y:,.0f}<extra>Privado</extra>'))
fig.add_trace(go.Bar(x=x, y=[float(r['definitivas_promotor_publico']) for r in rows],
                     name='Promotor público', marker_color=COLOR[2],
                     hovertemplate='%{y:,.0f}<extra>Público</extra>'))
fig.update_layout(barmode='stack', yaxis_title='Calificaciones definitivas al año')
guardar(fig, 'N02_vpo_por_promotor',
        'Quién construye la VPO: el promotor público gana peso, pero sobre cifras mínimas',
        'Calificaciones definitivas de vivienda protegida por tipo de promotor (planes estatales y autonómicos), 2014-2025.',
        'Fuente: Mº de Vivienda y Agenda Urbana / MITMS, Boletín estadístico (cuadros 1.6.2.1-1.6.2.2). Elaboración propia.')

# ---------- N3 ----------
rows = leer('N3_espana_destinos_pms_2004.csv')
cortas = {'Construcción de viviendas con protección pública': 'Vivienda protegida',
          'Otros fines de interés social — urbanización y dotaciones': 'Interés social: urbanización y dotaciones',
          'Otros fines de interés social — otros usos': 'Interés social: otros usos',
          'Conservación y gestión del propio PMS': 'Conservación del propio PMS',
          'Construcción de vivienda libre y otros usos autonómicos': 'Vivienda libre y otros usos autonómicos',
          'Usos no previstos en las normativas autonómicas': 'Usos no previstos legalmente'}
datos = sorted(((cortas[r['destino']], float(r['pct_sobre_valor_total'])) for r in rows),
               key=lambda t: t[1])
colores = ['#d03b3b' if 'no previstos' in e else (COLOR[0] if e == 'Vivienda protegida' else '#9ec5f4')
           for e, _ in datos]
fig = go.Figure(go.Bar(
    y=[e for e, _ in datos], x=[v for _, v in datos], orientation='h',
    marker_color=colores, hovertemplate='%{x:.1f} %<extra>%{y}</extra>'))
fig.update_layout(xaxis_title='% del valor total de los recursos empleados en 2004',
                  hovermode='closest', showlegend=False)
guardar(fig, 'N03_destinos_pms',
        'El suelo cedido para vivienda pública: solo el 16% acabó en vivienda protegida',
        'Destino de los recursos de los Patrimonios Municipales de Suelo, ejercicio 2004. Un 18,4% fue a usos no previstos en la legislación.',
        'Fuente: Tribunal de Cuentas, Informe de fiscalización de los PMS, ejercicio 2004 (BOE-A-2009-2122). Elaboración propia.')

# ---------- N4 ----------
rows = leer('N4_espana_coste_construccion_vs_precio.csv')
x = [int(r['anio']) for r in rows]
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=[float(r['precio_venta_eur_m2']) for r in rows],
                         name='Precio de venta de la vivienda libre', mode='lines',
                         line=dict(color=COLOR[0], width=2.4),
                         hovertemplate='%{y:,.0f} €/m²<extra>Precio venta</extra>'))
fig.add_trace(go.Scatter(x=x, y=[float(r['pem_residencial_eur_m2']) for r in rows],
                         name='Coste de construcción (PEM de los visados)', mode='lines',
                         line=dict(color=COLOR[1], width=2.4), fill='tonexty',
                         fillcolor='rgba(42,120,214,0.07)',
                         hovertemplate='%{y:,.0f} €/m²<extra>Coste PEM</extra>'))
fig.add_trace(go.Scatter(x=x, y=[float(r['pem_sobre_precio_pct']) for r in rows],
                         name='Coste sobre precio (%)', mode='none', hoverinfo='skip',
                         showlegend=False, visible=False))
fig.update_layout(yaxis_title='Euros por m²')
guardar(fig, 'N04_coste_vs_precio',
        'La burbuja no fue de costes: construir costaba el 18% de lo que se cobraba (2006)',
        'PEM por m² de la edificación residencial visada frente a precio de venta del m² de vivienda libre, 1992-2025. '
        'El PEM excluye IVA, honorarios, suelo y márgenes.',
        'Fuente: MITMS, visados de dirección de obra (cuadros 9.2-9.3); Mº Fomento/MIVAU y BdE. Elaboración propia.')

# ---------- N5 ----------
rows = leer('N5_espana_precio_suelo_anual.csv')
x = [int(r['anio']) for r in rows]
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=[float(r['precio_suelo_eur_m2_mun_mas_50k']) for r in rows],
                         name='Municipios de más de 50.000 habitantes', mode='lines+markers',
                         line=dict(color=COLOR[0], width=2.4), marker=dict(size=6),
                         hovertemplate='%{y:,.1f} €/m²<extra>>50.000 hab.</extra>'))
fig.add_trace(go.Scatter(x=x, y=[float(r['precio_suelo_eur_m2_nacional']) for r in rows],
                         name='Total nacional', mode='lines+markers',
                         line=dict(color=COLOR[1], width=2.4), marker=dict(size=6),
                         hovertemplate='%{y:,.1f} €/m²<extra>Nacional</extra>'))
fig.update_layout(yaxis_title='Euros por m² de suelo urbano transaccionado')
guardar(fig, 'N05_precio_suelo',
        'El precio del suelo urbano transaccionado: del pico de 2007 a la mitad',
        'Precio medio del m² de suelo urbano en transacciones, medias anuales, 2004-2025. La composición de lo transaccionado varía con el ciclo.',
        'Fuente: MITMS/MIVAU, Estadística de Precios de Suelo Urbano (cuadros 4 y 4.5). Elaboración propia.')

# ---------- N6 ----------
rows = leer('N6_espana_iniciadas_por_decadas.csv')
per = [r['periodo'] for r in rows]
fig = go.Figure()
fig.add_trace(go.Bar(x=per, y=[float(r['iniciadas_libres']) for r in rows], name='Libres',
                     marker_color=COLOR[0], hovertemplate='%{y:,.0f}<extra>Libres</extra>'))
fig.add_trace(go.Bar(x=per, y=[float(r['iniciadas_protegidas']) for r in rows], name='Protegidas',
                     marker_color=COLOR[2], hovertemplate='%{y:,.0f}<extra>Protegidas</extra>'))
fig.update_layout(barmode='stack', yaxis_title='Viviendas iniciadas en la década')
guardar(fig, 'N06_decadas_libres_protegidas',
        'Cinco décadas de construcción: de 7 de cada 10 protegidas a 1 de cada 8',
        'Viviendas iniciadas por décadas, libres y protegidas, 1976-2025. En 1976-1985 las libres solo constan desde 1980.',
        'Fuente: Mº de Vivienda y Agenda Urbana, vía Banco de España (Síntesis de Indicadores, cuadro 1.5). Elaboración propia.')

# ---------- índice completo ----------
paginas = sorted(f for f in os.listdir(OUT) if f.endswith('.html') and f != 'index.html')
titulos = {}
for p in paginas:
    h = open(os.path.join(OUT, p), encoding='utf-8').read()
    m = re.search(r'<b>(.*?)</b>', h)
    titulos[p] = m.group(1) if m else p
grupo_g = [p for p in paginas if p.startswith('G')]
grupo_n = [p for p in paginas if p.startswith('N')]
li_g = '\n'.join(f'<li><a href="{p}">{titulos[p]}</a></li>' for p in grupo_g)
li_n = '\n'.join(f'<li><a href="{p}">{titulos[p]}</a></li>' for p in grupo_n)
html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gráficas interactivas — monografía burbuja inmobiliaria</title>
<style>
 body {{ font-family: system-ui, -apple-system, 'Segoe UI', sans-serif; color: #0b0b0b;
        max-width: 46rem; margin: 3rem auto; padding: 0 1rem; line-height: 1.5; }}
 h1 {{ font-size: 1.5rem; }} h2 {{ font-size: 1.1rem; margin-top: 2rem; }} p {{ color: #52514e; }}
 li {{ margin: .45rem 0; }} a {{ color: #2a78d6; }}
 footer {{ margin-top: 2.5rem; font-size: .85rem; color: #898781; }}
</style></head><body>
<h1>Gráficas interactivas de la monografía</h1>
<p>Cada gráfica muestra el valor exacto al pasar el cursor. Las versiones para imprenta (B/N)
y en color, las tablas de datos y la memoria de fuentes están en el repositorio.</p>
<h2>Gráficas principales (G1-G10)</h2>
<ol>
{li_g}
</ol>
<h2>Series complementarias (N1-N6)</h2>
<ol>
{li_n}
</ol>
<footer>Fuentes: Banco de España, INE, MIVAU/MITMS, BOE, Tribunal de Cuentas, Eurostat, OCDE,
BIS, Reserva Federal, Prados de la Escosura. Detalle serie a serie en <code>tablas/FUENTES.md</code>.</footer>
</body></html>"""
open(os.path.join(OUT, 'index.html'), 'w').write(html)
print(f'{len(grupo_n)} interactivas N + índice regenerado ({len(paginas)} páginas en total)')
