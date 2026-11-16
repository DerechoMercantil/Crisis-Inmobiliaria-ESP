"""Gráficos complementarios: los que la obra cita como referencia al repositorio y no imprime.

Numerados por orden de aparición de la cita en la obra. Misma salida que los gráficos
definitivos (B/N, color, Excel editable, HTML interactivo y CSV), en ../complementarios/.
Uso:  python3 generar_graficos_complementarios.py
"""
import os
import generar_graficos_definitivos as B
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

B.SALIDA = os.path.join(B.RAIZ, 'graficos_complementarios')
num, leer, es = B.num, B.leer, B.es
PREF = dict(prefijo='Complementario', rotulo='Gráfico complementario', con_titulo=True)
EDAD = 'Elaboración propia con microdatos del INE (EPF, EBPF, PHOGUE y ECV). '


def col(filas, c, escala=1.0):
    return [None if a[c] in ('', None) else float(a[c]) / escala for a in filas]


def anios(tabla, desde=None, hasta=None, x='anio'):
    r = leer(tabla)
    return [a for a in r if (desde is None or int(a[x]) >= desde) and (hasta is None or int(a[x]) <= hasta)]


def specs():
    S = []
    r = anios('G01bis_espana_ratio_precio_rbd_anual_1971.csv')
    x = [int(a['anio']) for a in r]; v = col(r, 'precio_vivienda_en_anios_de_rbd_hogar_mediano')
    retro = [b if a <= 1987 else None for a, b in zip(x, v)]; ofi = [b if a >= 1987 else None for a, b in zip(x, v)]
    S.append(dict(n=1, slug='precio_vivienda_renta_hogar_1971_2026', origen='G01bis', capitulo='Introducción general, notas 1 y 30',
        titulo='Precio de la vivienda en años de renta bruta disponible del hogar mediano (España, 1971-2026)',
        sub='Vivienda libre de 93,75 m² construidos. Desde 1987, serie del Banco de España; 1971-1986, retropolación propia con el índice de precios del BIS y la renta nacional neta por hogar de Prados de la Escosura. El dato de 2026 corresponde al primer trimestre.',
        fuente='Banco de España, Síntesis de indicadores, cuadro 1.5; Banco de Pagos Internacionales; Prados de la Escosura, cuentas nacionales históricas. Elaboración propia.',
        x=x, series=[('Banco de España (desde 1987)', ofi, 0, '-'), ('Retropolación propia (1971-1986)', retro, 0, 'guion')], ylab='Años de renta', ylim=(0, 10), dec=1,
        rotulos=[(1971, 0), (2007, 0), (2026, 0)]))
    r = anios('G03_espana_ipc_vs_vivienda_anual.csv'); x = [int(a['anio']) for a in r]
    S.append(dict(n=2, slug='precio_real_vivienda_1971_2025', origen='G03', capitulo='Introducción general, nota 1',
        titulo='Precio real de la vivienda, deflactado por el índice de precios de consumo (España, 1971 = 100, 1971-2025)',
        sub='Índice de precios de la vivienda dividido por el índice de precios de consumo, medias anuales.',
        fuente='Banco de Pagos Internacionales, Selected residential property prices, e INE, índice de precios de consumo. Elaboración propia.',
        x=x, series=[('Precio real de la vivienda', col(r, 'precio_vivienda_real_1971_100'), 0, '-')], ylab='Índice (1971 = 100)', ylim=(0, 450), dec=0,
        extra=[('Precio nominal (1971 = 100)', col(r, 'precio_vivienda_nominal_1971_100')), ('IPC (1971 = 100)', col(r, 'ipc_1971_100'))],
        rotulos=[(1986, 0), (2007, 0), (2025, 0)]))
    r = anios('G02b_ratio_precio_renta_estandarizado_anual.csv', 1970, 2025); x = [int(a['anio']) for a in r]
    S.append(dict(n=3, slug='ratio_precio_renta_respecto_media_historica', origen='G02b', capitulo='Introducción general, nota 6',
        titulo='Ratio entre el precio de la vivienda y la renta disponible respecto de su media de largo plazo en España, Italia, el Reino Unido y la zona del euro (media = 100, 1970-2025)',
        sub='Cada serie se expresa en porcentaje de su propia media histórica: un valor de 120 indica una ratio un 20 % superior a la media.',
        fuente='OCDE, Analytical House Prices Indicators. Elaboración propia.',
        x=x, series=[('España', col(r, 'Espana'), 1, '-'), ('Zona del euro', col(r, 'ZonaEuro'), 2, '-'), ('Italia', col(r, 'Italia'), 3, '-'), ('Reino Unido', col(r, 'ReinoUnido'), 4, '-')],
        ylab='Media histórica = 100', ylim=(50, 160), dec=0, final=True))
    r = anios('G07_eeuu_riqueza_por_edad_anual.csv', 1989, 2025); x = [int(a['anio']) for a in r]
    S.append(dict(n=4, slug='riqueza_neta_por_edad_estados_unidos', origen='G07', capitulo='Introducción general, nota 7',
        titulo='Participación en la riqueza neta de los hogares por edad del cabeza de familia (Estados Unidos, 1989-2025)',
        sub='Porcentaje de la riqueza neta total de los hogares, medias anuales.',
        fuente='Reserva Federal, Distributional Financial Accounts. Elaboración propia.',
        x=x, series=[('Menores de 40 años', col(r, 'pct_riqueza_neta_menores_40'), 0, '-'), ('De 40 a 54 años', col(r, 'pct_riqueza_neta_40_54'), 3, '-'), ('De 55 a 69 años', col(r, 'pct_riqueza_neta_55_69'), 1, '-'), ('70 años o más', col(r, 'pct_riqueza_neta_70_o_mas'), 2, '-')],
        ylab='% de la riqueza neta', ylim=(0, 50), dec=1, final=True, sufijo=' %'))
    r = anios('G18_espana_umbral_renta_acceso_compra_2004_2024.csv', x='anio_renta'); x = [int(a['anio_renta']) for a in r]
    S.append(dict(n=5, slug='asalariados_bajo_umbral_acceso_compra', origen='G18', capitulo='Introducción general, nota 19',
        titulo='Asalariados y hogares cuya renta no alcanza el umbral necesario para pagar la hipoteca de la vivienda tipo sin destinarle más del 30 % de sus ingresos (España, 2004-2024)',
        sub='Préstamo del 80 % del precio de la vivienda tipo, a los tipos y plazos medios de cada año. No incluye la entrada.',
        fuente='Elaboración propia con microdatos de la Encuesta de Condiciones de Vida del INE y Banco de España, Síntesis de indicadores.',
        x=x, series=[('Asalariados de 25 a 34 años', col(r, 'asalariados_25_34_pct_bajo_umbral30'), 0, '-'), ('Asalariados de 18 a 64 años', col(r, 'asalariados_18_64_pct_bajo_umbral30'), 3, '-'), ('Hogares', col(r, 'hogares_pct_bajo_umbral30'), 4, '-')],
        ylab='% por debajo del umbral', ylim=(0, 100), dec=1, final=True, sufijo=' %'))
    r = anios('G01g_espana_patrimonio_vs_precio_vivienda_por_edad_2002_2024.csv', x='anio_ola_eff'); x = [int(a['anio_ola_eff']) for a in r]
    S.append(dict(n=6, slug='patrimonio_neto_frente_a_precio_vivienda_por_edad', origen='G01g', capitulo='Introducción general, nota 23',
        titulo='Patrimonio neto mediano de los hogares en porcentaje del precio de la vivienda tipo, por edad del cabeza de familia (España, 2002-2024)',
        sub='Riqueza neta mediana de cada grupo dividida por el precio de la vivienda tipo, ambos en euros de 2024. Una compra exige aportar en torno al 30 % del precio.',
        fuente='Banco de España, Encuesta Financiera de las Familias, olas de 2002 a 2024. Elaboración propia.',
        x=x, series=[('Menores de 35 años', col(r, 'patrimonio_menor_35_pct_precio'), 0, '-'), ('De 35 a 44 años', col(r, 'patrimonio_35_44_pct_precio'), 3, '-'), ('De 55 a 64 años', col(r, 'patrimonio_55_64_pct_precio'), 1, '-'), ('De 65 a 74 años', col(r, 'patrimonio_65_74_pct_precio'), 2, '-')],
        ylab='% del precio de la vivienda tipo', ylim=(0, 200), dec=0, final=True, sufijo=' %', marcas=True))
    r = anios('G06_espana_riqueza_neta_mediana_por_edad.csv'); x = [int(a['anio']) for a in r]
    S.append(dict(n=7, slug='riqueza_neta_mediana_por_edad', origen='G06', capitulo='Introducción general, nota 23',
        titulo='Riqueza neta mediana de los hogares por edad del cabeza de familia (España, 2002-2024)',
        sub='Miles de euros de 2024.',
        fuente='Banco de España, Encuesta Financiera de las Familias, olas de 2002 a 2024.',
        x=x, series=[('Menores de 35 años', col(r, 'mediana_miles_eur_2024_menor_de_35'), 0, '-'), ('De 35 a 44 años', col(r, 'mediana_miles_eur_2024_entre_35_y_44'), 3, '-'), ('De 45 a 54 años', col(r, 'mediana_miles_eur_2024_entre_45_y_54'), 4, '-'), ('De 55 a 64 años', col(r, 'mediana_miles_eur_2024_entre_55_y_64'), 1, '-'), ('De 65 a 74 años', col(r, 'mediana_miles_eur_2024_entre_65_y_74'), 2, '-'), ('75 años o más', col(r, 'mediana_miles_eur_2024_mayor_de_75'), 5, '-')],
        ylab='Miles de euros de 2024', ylim=(0, 400), dec=1, final=True, marcas=True))
    r = [a for a in leer('G05_espana_transferencia_alquiler_por_edad.csv') if a['tramo_edad'] in ('16-29', '30-44', '45-64', '65+')]
    S.append(dict(n=8, slug='alquileres_pagados_y_percibidos_por_edad', origen='G05', capitulo='Introducción general, nota 24', tipo='barras',
        titulo='Alquileres pagados y percibidos por los hogares, por edad de la persona responsable de la vivienda (España, 2025)',
        sub='Millones de euros al año. Los hogares pagan en total unos 27.900 millones; la diferencia con lo que declaran percibir corresponde a alquileres pagados a personas jurídicas y a rentas no declaradas.',
        fuente='Elaboración propia con microdatos de la Encuesta de Condiciones de Vida 2025 del INE.',
        x=['De 16 a 29 años', 'De 30 a 44 años', 'De 45 a 64 años', '65 años o más'],
        series=[('Alquiler pagado', col(r, 'alquiler_pagado_mill_eur'), 0, '-'), ('Alquiler percibido', col(r, 'alquiler_cobrado_mill_eur'), 2, '-')], ylab='Millones de euros', ylim=(0, 13500), dec=0))
    r = anios('G01f_espana_esfuerzo_teorico_por_edad_1987_2024.csv'); x = [int(a['anio']) for a in r]
    S.append(dict(n=9, slug='cuota_hipotecaria_sobre_renta_por_edad', origen='G01f', capitulo='Introducción general, nota 28',
        titulo='Cuota hipotecaria del primer año en porcentaje de la renta disponible del perceptor mediano, por grupo de edad (España, 1987-2024)',
        sub='Préstamo del 80 % del precio de la vivienda tipo, al tipo y plazo medios de cada año. Un valor superior al 100 % indica que la cuota no podía pagarse con una sola renta.',
        fuente=EDAD + 'Tipos y plazos: Banco de España, Síntesis de indicadores, cuadro 1.5.',
        x=x, series=[('Perceptor mediano de 18 a 35 años', col(r, 'esfuerzo_18_35_pct'), 0, '-'), ('Perceptor mediano de 55 a 64 años', col(r, 'esfuerzo_55_64_pct'), 1, '-'), ('Perceptor mediano de 65 a 74 años', col(r, 'esfuerzo_65_74_pct'), 2, '-')],
        ylab='% de la renta disponible', ylim=(0, 260), dec=0, final=True, sufijo=' %'))
    r = anios('G08a_espana_viviendas_iniciadas_anual.csv', 1970, 2025); x = [int(a['anio']) for a in r]
    S.append(dict(n=10, slug='viviendas_iniciadas_libres_y_protegidas', origen='G08a', capitulo='C. J. Rusillo Ramiro, epígrafes III.1 y VI; D. Raya Quero, epígrafe VI.1',
        titulo='Viviendas iniciadas, libres y protegidas (España, 1970-2025)',
        sub='Miles de viviendas al año. Las viviendas libres constan desde 1980.',
        fuente='Ministerio de Vivienda y Agenda Urbana y Banco de España, Síntesis de indicadores, cuadro 1.5.',
        x=x, series=[('Viviendas libres', col(r, 'iniciadas_libres', 1000), 0, '-'), ('Viviendas protegidas', col(r, 'iniciadas_protegidas', 1000), 1, '-')], ylab='Miles al año', ylim=(0, 720), dec=0, final=True,
        rotulos=[(2006, 0)]))
    r = anios('G01b_espana_precio_vs_renta_indexado.csv'); x = [int(a['anio']) for a in r]
    S.append(dict(n=11, slug='precio_metro_cuadrado_y_renta_hogar_indices', origen='G01b', capitulo='C. J. Rusillo Ramiro, epígrafe VI',
        titulo='Precio del metro cuadrado de vivienda y renta bruta disponible del hogar mediano (España, 1987 = 100, 1987-2025)',
        sub='Índices con base en 1987. El precio pasa de 327 a 2.127,6 euros por metro cuadrado, y la renta, de 9.913 a 26.245 euros.',
        fuente='Banco de España, Síntesis de indicadores, cuadro 1.5. Elaboración propia.',
        x=x, series=[('Precio del metro cuadrado', col(r, 'indice_precio_1987_100'), 0, '-'), ('Renta bruta disponible del hogar mediano', col(r, 'indice_rbd_1987_100'), 4, '-')], ylab='Índice (1987 = 100)', ylim=(0, 800), dec=0, final=True))
    r = anios('G10_espana_vpo_precio_maximo_1979_2025.csv'); x = [int(a['anio']) for a in r]
    S.append(dict(n=12, slug='precio_maximo_vivienda_protegida_en_renta', origen='G10', capitulo='C. J. Rusillo Ramiro, epígrafe VI',
        titulo='Precio máximo legal de una vivienda protegida de 90 m² útiles en años de renta del hogar mediano (España, 1979-2025)',
        sub='Precio máximo de venta fijado por las normas estatales de cada año, dividido por la renta bruta disponible del hogar mediano.',
        fuente='Elaboración propia a partir de las órdenes y reales decretos publicados en el BOE y de Banco de España, Síntesis de indicadores, cuadro 1.5.',
        x=x, series=[('Vivienda protegida de 90 m² útiles', col(r, 'vpo_en_anios_de_renta'), 0, '-')], ylab='Años de renta', ylim=(0, 6), dec=1,
        rotulos=[(1979, 0), (1997, 0), (2025, 0)]))
    for g in S:
        vacias = [s[0] for s in g['series'] if all(v is None for v in s[1])]
        if vacias:
            print('  sin datos, se omite:', g['n'], vacias)
        g['series'] = [s for s in g['series'] if s[0] not in vacias]
        g.update(PREF); g['orden'] = [s[2] for s in g['series']]
    return S


def estatico(g, modo):
    fig, ax = B.figura()
    x = g['x']
    if g.get('tipo') == 'barras':
        import numpy as np
        pos = np.arange(len(x)); w = 0.36
        rell = [B.COLOR[s[2]] for s in g['series']] if modo == 'color' else ['#2b2b2b', '#bdbdbd']
        for i, s in enumerate(g['series']):
            bs = ax.bar(pos + (i - 0.5) * (w + 0.03), s[1], w, color=rell[i], edgecolor='none' if modo == 'color' else '#2b2b2b', linewidth=0.5)
            for b, v in zip(bs, s[1]):
                ax.text(b.get_x() + b.get_width() / 2, v + g['ylim'][1] * 0.012, f'{v:,.0f}'.replace(',', '.'), ha='center', va='bottom', fontsize=7.5, color=B.TINTA, fontweight='bold')
        ax.set_xticks(pos); ax.set_xticklabels(x, fontsize=7.5, color=B.TINTA_2)
        ax.yaxis.set_major_formatter(lambda v, _: f'{v:,.0f}'.replace(',', '.'))
        h = [Patch(facecolor=rell[i], edgecolor='#2b2b2b' if modo == 'bn' else 'none', linewidth=0.5, label=s[0]) for i, s in enumerate(g['series'])]
        B.leyenda(ax, h, loc='upper left', handlelength=1.6)
    else:
        h = []
        for k, (nombre, v, i, trazo) in enumerate(g['series']):
            st = B.estilo(i, modo)
            if trazo == 'guion':
                st['linestyle'] = (0, (4, 2))
            xs = [a for a, b in zip(x, v) if b is not None]; ys = [b for b in v if b is not None]
            ax.plot(xs, ys, **st)
            extra = {}
            if g.get('marcas') or (modo == 'bn' and len(g['series']) > 1 and trazo != 'guion' and k > 0):
                paso = 1 if g.get('marcas') else max(1, len(xs) // 12)
                ax.plot(xs[::paso], ys[::paso], **B.marca(i, modo))
                extra = {a: b for a, b in B.marca(i, modo).items() if a != 'linestyle'}
            h.append(Line2D([0], [0], label=nombre, **st, **extra))
        rango = x[-1] - x[0]
        ax.set_xlim(x[0] - rango * 0.02, x[-1] + rango * (0.12 if g.get('final') or g.get('rotulos') else 0.03))
        if g.get('final'):
            fin = sorted(((next(b for b in reversed(v) if b is not None), nombre) for nombre, v, i, t in g['series']), reverse=True)
            minsep = (g['ylim'][1] - g['ylim'][0]) * 0.055; pos = []
            for val, nombre in fin:
                y = val if not pos else min(val, pos[-1] - minsep)
                pos.append(y)
                B.etiqueta(ax, x[-1], y, es(val, g['dec']) + g.get('sufijo', ''), dx=rango * 0.012)
        for (a, k) in g.get('rotulos', []):
            v = g['series'][k][1]
            if a not in x:
                continue
            val = v[x.index(a)]
            if val is None and len(g['series']) > 1:
                val = g['series'][1][1][x.index(a)]
            ultimo = a == x[-1]
            B.etiqueta(ax, a, val, es(val, g['dec']), dx=rango * 0.012 if ultimo else 0, dy=0 if ultimo else (g['ylim'][1] - g['ylim'][0]) * (0.05 if val >= sum(b for b in v if b is not None) / len([b for b in v if b is not None]) else -0.05), ha='left' if ultimo else 'center')
        if len(h) > 1:
            B.leyenda(ax, h, loc='upper center', bbox_to_anchor=(0.5, -0.09), ncol=2 if len(h) > 2 else 1)
    ax.set_ylim(*g['ylim'])
    ax.set_ylabel(g['ylab'], fontsize=7.5, color=B.TINTA_2)
    B.guardar(fig, g, modo)


def interactivo(g):
    import plotly.graph_objects as go
    cab = ['Año' if g.get('tipo') != 'barras' else 'Edad'] + [s[0] for s in g['series']] + [e[0] for e in g.get('extra', [])]
    filas = [[a] + [s[1][k] for s in g['series']] + [e[1][k] for e in g.get('extra', [])] for k, a in enumerate(g['x'])]
    B.exportar(g, cab, filas)
    B.excel(g, cab, filas, tipo='linea' if g.get('tipo') != 'barras' else 'columnas', eje_y=g['ylab'], n_series=len(g['series']), formato='0' if g['dec'] == 0 else '0.0')
    if g.get('tipo') == 'barras':
        f = go.Figure([go.Bar(x=g['x'], y=s[1], name=s[0], marker=dict(color=B.COLOR[s[2]], line=dict(color='#fcfcfb', width=2)),
                              hovertemplate='%{y:,.0f} millones de euros<extra>' + s[0] + '</extra>') for s in g['series']])
        f.update_layout(barmode='group', yaxis=dict(title=g['ylab'], range=list(g['ylim'])))
    else:
        f = go.Figure([B.linea_px(s[0], g['x'], s[1], s[2], g.get('sufijo', ''), dec=g['dec'], dash='dash' if s[3] == 'guion' else None) for s in g['series']])
        f.update_layout(hovermode='x unified', yaxis=dict(title=g['ylab'], range=list(g['ylim'])))
    B.html_pagina(g, f, cab, filas, dec=g['dec'])


if __name__ == '__main__':
    import shutil
    S = specs()
    for g in S:
        for modo in ('bn', 'color'):
            estatico(g, modo)
        interactivo(g)
    shutil.copyfile(B.PLOTLY_JS, os.path.join(B.SALIDA, 'interactivas', 'plotly.min.js'))
    with open(os.path.join(B.SALIDA, 'indice.tsv'), 'w', encoding='utf-8') as f:
        for g in S:
            f.write(f"{g['n']}\t{B.base(g)}\t{g['origen']}\t{g['capitulo']}\t{g['titulo']}\t{g['fuente']}\n")
    print('Hecho:', B.SALIDA, len(S))
