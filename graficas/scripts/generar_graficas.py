#!/usr/bin/env python3
"""Genera las gráficas de la monografía en dos versiones (color y B/N)
a partir de las tablas validadas en tablas/. PNG 300 ppp + SVG."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import estilo
from estilo import nueva_figura, serie, titulos, leyenda, guardar, etiqueta_final

BASE = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
T = os.path.join(BASE, 'tablas')


def fmt(v, dec=1):
    s = f'{v:,.{dec}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


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


def g1(modo):
    rows = leer('G1_espana_ratio_precio_rbd_anual.csv')
    x, y = col(rows, 'precio_vivienda_en_anios_de_rbd_hogar_mediano')
    fig, ax = nueva_figura()
    serie(ax, x, y, 0, modo, 'España')
    # hitos anotados
    for anio, va in [(2007, 'top'), (1997, 'bottom')]:
        v = dict(zip(x, y))[anio]
        ax.annotate(fmt(v), xy=(anio, v), xytext=(anio, v + (0.35 if va == 'top' else -0.55)),
                    ha='center', fontsize=8.5, color=estilo.TINTA_2, fontweight='bold')
    ax.annotate(fmt(y[-1]), xy=(x[-1], y[-1]), xytext=(x[-1] + 0.6, y[-1]),
                fontsize=8.5, color=estilo.TINTA_2, fontweight='bold', va='center')
    ax.set_ylim(0, 10)
    ax.set_xlim(1986, 2028)
    titulos(fig, ax,
            'El precio de la vivienda, en años de renta de un hogar mediano (España)',
            'Precio medio de una vivienda libre de 93,75 m² construidos / renta bruta anual del hogar mediano. 1987-2025, media anual de datos trimestrales.',
            'Fuente: Banco de España, Síntesis de Indicadores, cuadro 1.5 (serie SI_1_5.43). Elaboración propia.')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'G01_ratio_precio_renta_espana', modo)


def g1b(modo):
    rows = leer('G1b_espana_precio_vs_renta_indexado.csv')
    x, p = col(rows, 'indice_precio_1987_100')
    _, r = col(rows, 'indice_rbd_1987_100')
    fig, ax = nueva_figura()
    serie(ax, x, p, 0, modo, 'Precio del m² de vivienda libre')
    serie(ax, x, r, 1, modo, 'Renta bruta del hogar mediano')
    etiqueta_final(ax, x[-1], p[-1], '×' + fmt(p[-1]/100), modo, 0)
    etiqueta_final(ax, x[-1], r[-1], '×' + fmt(r[-1]/100), modo, 1)
    ax.set_xlim(1986, 2029)
    titulos(fig, ax,
            'El precio de la vivienda se multiplica por 8; la renta por hogar, por 2,6 (1987-2025)',
            'Índices nominales, base 1987 = 100. Serie de precio enlazada (Mº Fomento base 1987 / MIVAU 1995-).',
            'Fuente: Mº de Fomento (1987-94, reproducido en Vergés, Estadística Española 179/2012); MIVAU y Banco de España (1995-2025). Elaboración propia.')
    leyenda(ax, loc='upper left')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'G01b_precio_vs_renta_indexado', modo)


def g1bis(modo):
    rows = leer('G1bis_espana_ratio_precio_rbd_anual_1971.csv')
    retro = [(int(r['anio']), float(r['precio_vivienda_en_anios_de_rbd_hogar_mediano']))
             for r in rows if r['metodo'].startswith('retropolación')]
    oficial = [(int(r['anio']), float(r['precio_vivienda_en_anios_de_rbd_hogar_mediano']))
               for r in rows if r['metodo'] == 'serie oficial BdE' and int(r['anio']) <= 2025]
    color = estilo.COLOR[0] if modo == 'color' else '#000000'
    xr, yr = zip(*retro)
    xo, yo = zip(*oficial)
    # se añade 1987 al tramo retropolado para que el trazo discontinuo enlace sin salto visual
    xr, yr = list(xr) + [xo[0]], list(yr) + [yo[0]]
    fig, ax = nueva_figura()
    ax.plot(xr, yr, color=color, linestyle='--', linewidth=1.9,
            label='Retropolación 1971-1986 (BIS y Prados de la Escosura)')
    ax.plot(xo, yo, color=color, linestyle='-', linewidth=2.2,
            label='Serie oficial del Banco de España (1987-2025)')
    hitos = dict(zip(list(xr) + list(xo), list(yr) + list(yo)))
    for anio, dy in [(1982, -0.55), (1997, -0.55), (2007, 0.4)]:
        ax.annotate(fmt(hitos[anio]), xy=(anio, hitos[anio]), xytext=(anio, hitos[anio] + dy),
                    ha='center', fontsize=8.5, color=estilo.TINTA_2, fontweight='bold')
    ax.annotate(fmt(yo[-1]), xy=(xo[-1], yo[-1]), xytext=(xo[-1] + 0.6, yo[-1]),
                fontsize=8.5, color=estilo.TINTA_2, fontweight='bold', va='center')
    ax.set_ylim(0, 10)
    ax.set_xlim(1969, 2029)
    titulos(fig, ax,
            'Medio siglo de precio de la vivienda, en años de renta del hogar mediano (España)',
            'Precio medio de una vivienda libre de 93,75 m² construidos / renta bruta anual del hogar mediano. 1971-2025.\n'
            'Tramo 1971-1986 retropolado: precios BIS enlazados a la serie de Fomento; renta según Prados de la Escosura y hogares censales (método de G10).',
            'Fuente: Banco de España (SI_1_5.43, 1987-); BIS, Selected residential property prices; Prados de la Escosura (2017, act. 2025); censos INE. Elaboración propia.')
    leyenda(ax, loc='upper left')
    fig.subplots_adjust(top=0.78, bottom=0.12)
    guardar(fig, 'G01bis_ratio_precio_renta_espana_1971', modo)


PAISES = [('Espana', 'España', 0), ('Italia', 'Italia', 1), ('ReinoUnido', 'Reino Unido', 2),
          ('Hungria', 'Hungría', 3), ('ZonaEuro', 'Zona euro', 4)]


def g2(modo, tabla, nombre, titulo, subtitulo, fuente, ref100=False):
    rows = leer(tabla)
    fig, ax = nueva_figura()
    if ref100:
        ax.axhline(100, color=estilo.EJE, linewidth=1.0, linestyle='-')
    finales = []
    for campo, etiqueta, i in PAISES:
        x, y = col(rows, campo)
        if not x:
            continue
        serie(ax, x, y, i, modo, etiqueta)
        finales.append((y[-1], x[-1], etiqueta, i))
    # etiquetas directas separadas verticalmente
    finales.sort()
    ys_usadas = []
    for v, xf, etiqueta, i in finales:
        yy = v
        while any(abs(yy - u) < 6 for u in ys_usadas):
            yy += 6
        ys_usadas.append(yy)
        etiqueta_final(ax, xf, yy, etiqueta, modo, i, dx=0.7)
    ax.set_xlim(1968, 2037)
    ax.set_xticks(range(1970, 2021, 10))
    titulos(fig, ax, titulo, subtitulo, fuente)
    leyenda(ax, loc='upper left')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, nombre, modo)


def g3(modo):
    rows = leer('G3_espana_ipc_vs_vivienda_anual.csv')
    x, pv = col(rows, 'precio_vivienda_nominal_1971_100')
    _, ipc = col(rows, 'ipc_1971_100')
    _, real = col(rows, 'precio_vivienda_real_1971_100')
    fig, ax = nueva_figura()
    serie(ax, x, pv, 0, modo, 'Precio de la vivienda (nominal)')
    serie(ax, x, ipc, 1, modo, 'IPC (inflación acumulada)')
    serie(ax, x, real, 2, modo, 'Precio de la vivienda real (deflactado)')
    ax.set_yscale('log')
    ax.set_yticks([100, 200, 400, 800, 1600, 3200, 6400])
    ax.get_yaxis().set_major_formatter(lambda v, p: f'{v:,.0f}'.replace(',', '.'))
    etiqueta_final(ax, x[-1], pv[-1], '×' + fmt(pv[-1]/100, 0), modo, 0)
    etiqueta_final(ax, x[-1], ipc[-1], '×' + fmt(ipc[-1]/100, 0), modo, 1)
    etiqueta_final(ax, x[-1], real[-1], '×' + fmt(real[-1]/100), modo, 2)
    ax.set_xlim(1970, 2030)
    titulos(fig, ax,
            'Vivienda e inflación en España desde 1971: ×84 nominal, ×24 el IPC, ×3,4 real',
            'Índices base 1971 = 100, escala logarítmica. Medias anuales.',
            'Fuente: BIS, Selected residential property prices (serie de España, proveedor: Banco de España) y BIS Long consumer prices. Elaboración propia.')
    leyenda(ax, loc='upper left')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'G03_espana_inflacion_vs_vivienda', modo)


def g4(modo):
    rows = leer('G4_comparativa_precios_reales_anual.csv')
    fig, ax = nueva_figura()
    finales = []
    for campo, etiqueta, i in PAISES:
        xs, ys = [], []
        for r in rows:
            y = int(r['anio'])
            if y < 1971 or y > 2025 or not r[campo]:
                continue
            xs.append(y); ys.append(float(r[campo]))
        if not xs:
            continue
        serie(ax, xs, ys, i, modo, etiqueta)
        finales.append((ys[-1], xs[-1], etiqueta, i))
    finales.sort()
    ys_usadas = []
    for v, xf, etiqueta, i in finales:
        yy = v
        while any(abs(yy - u) < 9 for u in ys_usadas):
            yy += 9
        ys_usadas.append(yy)
        etiqueta_final(ax, xf, yy, etiqueta, modo, i, dx=0.7)
    ax.set_xlim(1969, 2036)
    ax.set_xticks(range(1970, 2021, 10))
    titulos(fig, ax,
            'Precios reales de la vivienda: Hungría, el país más "burbujeado" del panel',
            'Índice de precios de la vivienda deflactado por el IPC nacional, base 2015 = 100. 1971-2025 (Hungría desde 1992).',
            'Fuente: BIS, Selected residential property prices (series reales). Elaboración propia.')
    leyenda(ax, loc='upper left')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'G04_comparativa_precios_reales', modo)


def g5(modo):
    rows = leer('G5_espana_transferencia_alquiler_por_edad.csv')
    tramos = ['16-29', '30-44', '45-64', '65+']
    paga = {r['tramo_edad']: float(r['alquiler_pagado_mill_eur']) for r in rows if r['tramo_edad'] in tramos}
    cobra = {r['tramo_edad']: float(r['alquiler_cobrado_mill_eur']) for r in rows if r['tramo_edad'] in tramos}
    resid = next(float(r['alquiler_cobrado_mill_eur']) for r in rows if r['tramo_edad'].startswith('empresas'))
    import numpy as np
    ypos = np.arange(len(tramos))[::-1]
    fig, ax = nueva_figura(9.0, 4.6)
    ax.grid(False); ax.grid(axis='x', color=estilo.REJILLA, linewidth=0.7)
    alto = 0.36
    if modo == 'color':
        c1, c2 = estilo.COLOR[0], estilo.COLOR[5]
        kw1 = dict(color=c1); kw2 = dict(color=c2)
    else:
        kw1 = dict(color='#4d4d4d')
        kw2 = dict(color='white', edgecolor='#0b0b0b', hatch='///', linewidth=0.8)
    b1 = ax.barh(ypos + alto/2 + 0.02, [paga[t]/1000 for t in tramos], height=alto, label='Alquiler pagado', **kw1)
    b2 = ax.barh(ypos - alto/2 - 0.02, [cobra[t]/1000 for t in tramos], height=alto, label='Alquiler cobrado', **kw2)
    for yy, t in zip(ypos, tramos):
        ax.text(paga[t]/1000 + 0.15, yy + alto/2 + 0.02, fmt(paga[t]/1000),
                va='center', fontsize=8.5, color=estilo.TINTA_2, fontweight='bold')
        ax.text(cobra[t]/1000 + 0.15, yy - alto/2 - 0.02, fmt(cobra[t]/1000),
                va='center', fontsize=8.5, color=estilo.TINTA_2, fontweight='bold')
    ax.set_yticks(ypos)
    ax.set_yticklabels([f'{t} años' if t != '65+' else '65 y más' for t in tramos], color=estilo.TINTA, fontsize=10)
    ax.set_xlabel('Miles de millones de euros al año', fontsize=9, color=estilo.TINTA_2)
    titulos(fig, ax,
            'Quién paga y quién cobra el alquiler en España, por edad',
            'Alquiler anual pagado (mensualidad 2025 ×12) y cobrado (renta declarada del ejercicio 2024) por los hogares, según edad de la persona de referencia.\n'
            f'Además, {fmt(resid/1000)} miles de millones de euros pagados van a empresas, alquiler no declarado y otros.',
            'Fuente: elaboración propia sobre microdatos de la Encuesta de Condiciones de Vida 2025 (INE). Script reproducible en el repositorio.')
    leyenda(ax, loc='upper right')
    ax.set_xlim(0, 13.5)
    fig.subplots_adjust(top=0.80, bottom=0.14)
    guardar(fig, 'G05_transferencia_alquiler_edad', modo)


def g6(modo):
    rows = leer('G6_espana_riqueza_neta_mediana_por_edad.csv')
    grupos = [('mediana_miles_eur_2024_menor_de_35', 'Menos de 35', 0),
              ('mediana_miles_eur_2024_entre_35_y_44', '35-44', 1),
              ('mediana_miles_eur_2024_entre_45_y_54', '45-54', 2),
              ('mediana_miles_eur_2024_entre_55_y_64', '55-64', 3),
              ('mediana_miles_eur_2024_entre_65_y_74', '65-74', 4),
              ('mediana_miles_eur_2024_mayor_de_75', '75 y más', 5)]
    fig, ax = nueva_figura(9.0, 5.6)
    for campo, etiqueta, i in grupos:
        x, y = col(rows, campo, fin=2024)
        serie(ax, x, y, i, modo, etiqueta, marcador=True)
    # resaltar la caída de los jóvenes
    x, y = col(rows, grupos[0][0], fin=2024)
    ax.annotate(fmt(y[x.index(2005)], 0), xy=(2005, y[x.index(2005)]), xytext=(2004.2, y[x.index(2005)] + 16),
                fontsize=8.5, color=estilo.TINTA, fontweight='bold')
    ax.annotate(fmt(y[x.index(2014)], 0), xy=(2014, y[x.index(2014)]), xytext=(2013.5, y[x.index(2014)] + 14),
                fontsize=8.5, color=estilo.TINTA, fontweight='bold')
    ax.set_xticks([2002, 2005, 2008, 2011, 2014, 2017, 2020, 2022, 2024])
    ax.set_ylabel('Miles de euros de 2024', fontsize=9, color=estilo.TINTA_2)
    titulos(fig, ax,
            'La riqueza de los jóvenes se hunde: de 104.000 € (2005) a 23.000 € (2024)',
            'Riqueza neta mediana de los hogares por edad del cabeza de familia. Miles de euros constantes de 2024. Olas EFF 2002-2024.',
            'Fuente: Banco de España, Encuesta Financiera de las Familias (EFF), resultados oficiales. Elaboración propia.')
    leg = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09), ncol=6, frameon=False, fontsize=8.5, labelcolor=estilo.TINTA_2, handlelength=2.2)
    fig.subplots_adjust(top=0.83, bottom=0.18)
    guardar(fig, 'G06_riqueza_por_edad_espana', modo)


def g7(modo):
    rows = leer('G7_eeuu_riqueza_por_edad_anual.csv')
    grupos = [('pct_riqueza_neta_menores_40', 'Menores de 40', 0),
              ('pct_riqueza_neta_40_54', '40-54', 1),
              ('pct_riqueza_neta_55_69', '55-69', 2),
              ('pct_riqueza_neta_70_o_mas', '70 y más', 3)]
    fig, ax = nueva_figura()
    for campo, etiqueta, i in grupos:
        x, y = col(rows, campo)
        serie(ax, x, y, i, modo, etiqueta)
        etiqueta_final(ax, x[-1], y[-1], fmt(y[-1],0) + '%', modo, i)
    ax.set_ylim(0, 50)
    ax.set_xlim(1988, 2028)
    ax.set_ylabel('% de la riqueza neta total de los hogares', fontsize=9, color=estilo.TINTA_2)
    titulos(fig, ax,
            'EE.UU.: los menores de 40 años pasan del 12% al 7% de la riqueza (1989-2025)',
            'Participación de cada grupo de edad en la riqueza neta total de los hogares. Medias anuales de datos trimestrales.',
            'Fuente: Reserva Federal, Distributional Financial Accounts. Elaboración propia.')
    leyenda(ax, loc='upper left', ncol=2)
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'G07_eeuu_riqueza_por_edad', modo)


def g8a(modo):
    rows = leer('G8a_espana_viviendas_iniciadas_anual.csv')
    fig, ax = nueva_figura()
    x, tot = col(rows, 'iniciadas_total')
    _, prot = col(rows, 'iniciadas_protegidas')
    xl, lib = col(rows, 'iniciadas_libres')
    serie(ax, x, [v/1000 for v in tot], 0, modo, 'Total iniciadas')
    serie(ax, xl, [v/1000 for v in lib], 1, modo, 'Libres')
    serie(ax, x, [v/1000 for v in prot], 2, modo, 'Protegidas')
    ax.axvspan(1970, 1980, color=estilo.REJILLA, alpha=0.35, zorder=0)
    ax.text(1975, ax.get_ylim()[1]*0.93, 'Hasta 1979 el total\nsolo recoge protegidas', ha='center',
            fontsize=7.5, color=estilo.MUTED)
    ax.set_ylabel('Miles de viviendas iniciadas al año', fontsize=9, color=estilo.TINTA_2)
    ax.set_xlim(1969, 2026)
    titulos(fig, ax,
            'La vivienda protegida se desploma: de 250.000 iniciadas al año a menos de 20.000',
            'Viviendas iniciadas en España por régimen, 1970-2025 (sumas anuales de datos mensuales).',
            'Fuente: Mº de Vivienda y Agenda Urbana, vía Banco de España (Síntesis de Indicadores, cuadro 1.5). Elaboración propia.')
    leyenda(ax, loc='upper right')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'G08a_viviendas_iniciadas', modo)


def g8b(modo):
    rows = leer('G8b_espana_compraventas_anual.csv')
    fig, ax = nueva_figura()
    x, tot = col(rows, 'compraventas_total')
    _, nue = col(rows, 'vivienda_nueva')
    _, usa = col(rows, 'vivienda_usada')
    serie(ax, x, [v/1000 for v in tot], 0, modo, 'Total')
    serie(ax, x, [v/1000 for v in nue], 1, modo, 'Vivienda nueva')
    serie(ax, x, [v/1000 for v in usa], 2, modo, 'Vivienda usada')
    ax.set_ylabel('Miles de compraventas al año', fontsize=9, color=estilo.TINTA_2)
    ax.set_xlim(2003.5, 2026)
    titulos(fig, ax,
            'El mercado pos-burbuja es de segunda mano: la vivienda nueva no se recupera',
            'Compraventas de vivienda ante notario en España, 2004-2025 (sumas anuales de datos trimestrales).',
            'Fuente: Mº de Vivienda y Agenda Urbana (Consejo General del Notariado), vía Banco de España. Elaboración propia.')
    leyenda(ax, loc='upper right')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'G08b_compraventas', modo)


def g9(modo):
    rows = leer('G9_ue_permisos_viviendas_anual.csv')
    series9 = [('EU27_2020', 'UE-27', 0), ('ES', 'España', 1), ('IT', 'Italia', 2), ('HU', 'Hungría', 3)]
    fig, ax = nueva_figura()
    for campo, etiqueta, i in series9:
        x, y = col(rows, campo)
        serie(ax, x, y, i, modo, etiqueta, marcador=True)
        etiqueta_final(ax, x[-1], y[-1], etiqueta, modo, i, dx=0.3)
    ax.set_yscale('log')
    ax.set_yticks([20, 50, 100, 200, 500, 1000, 2000])
    ax.get_yaxis().set_major_formatter(lambda v, p: f'{v:,.0f}'.replace(',', '.'))
    ax.set_ylabel('Miles de viviendas autorizadas (escala log.)', fontsize=9, color=estilo.TINTA_2)
    ax.set_xlim(2004.5, 2029)
    titulos(fig, ax,
            'Permisos de construcción de vivienda: la UE construye la mitad que en 2006',
            'Viviendas en permisos de construcción (edificios residenciales, miles). 2005-2025. Escala logarítmica.',
            'Fuente: Eurostat, Building permits (sts_cobp_a). Elaboración propia.')
    leyenda(ax, loc='lower left', ncol=2)
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'G09_permisos_ue', modo)


def g10(modo):
    rows = leer('G10_espana_vpo_precio_maximo_1979_2025.csv')
    x, vpo = col(rows, 'vpo_en_anios_de_renta')
    r1 = leer('G1_espana_ratio_precio_rbd_anual.csv')
    xl, libre = col(r1, 'precio_vivienda_en_anios_de_rbd_hogar_mediano')
    fig, ax = nueva_figura()
    serie(ax, xl, libre, 0, modo, 'Vivienda libre (93,75 m² construidos)')
    serie(ax, x, vpo, 1, modo, 'VPO régimen general (90 m² útiles)')
    etiqueta_final(ax, xl[-1], libre[-1], fmt(libre[-1]), modo, 0)
    etiqueta_final(ax, x[-1], vpo[-1], fmt(vpo[-1]), modo, 1)
    ax.annotate('Mínimo: 2,5 (1997)', xy=(1997, 2.48), xytext=(1992.5, 1.1),
                fontsize=8, color=estilo.TINTA_2,
                arrowprops=dict(arrowstyle='-', color=estilo.MUTED, lw=0.8))
    ax.annotate('MBE congelado en 758 €/m²\ndesde diciembre de 2008', xy=(2016, 6.2), fontsize=8,
                color=estilo.TINTA_2, ha='center')
    ax.set_ylim(0, 10)
    ax.set_xlim(1978, 2029)
    ax.set_ylabel('Años de renta bruta del hogar mediano', fontsize=9, color=estilo.TINTA_2)
    titulos(fig, ax,
            'La vivienda protegida también se encarece: de 2,5 años de renta (1997) a 4,2 (2025)',
            'Precio máximo legal de una VPO de 90 m² útiles (área media nacional) y precio de la vivienda libre, en años de renta del hogar mediano. 1979-2025.',
            'Fuente: elaboración propia a partir del BOE (19 órdenes y 8 reales decretos, ver FUENTES.md), Banco de España y Prados de la Escosura (renta 1979-86).')
    leyenda(ax, loc='upper left')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'G10_vpo_en_anios_de_renta', modo)


TODAS = [g1, g1b, g1bis, g3, g4, g5, g6, g7, g8a, g8b, g9, g10]

if __name__ == '__main__':
    for modo in ('color', 'bn'):
        for fn in TODAS:
            fn(modo)
        g2(modo, 'G2_ratio_precio_renta_anual.csv', 'G02_ratio_precio_renta_comparativa',
           'Precio de la vivienda sobre renta por hogar: cinco mercados, un mismo destino',
           'Ratio precio/renta por hogar, índice 2015 = 100. 1970-2025 (Hungría desde 2007; Reino Unido desde 1987).',
           'Fuente: OCDE, Analytical House Prices Indicators (price-to-income ratio). Elaboración propia.')
        g2(modo, 'G2b_ratio_precio_renta_estandarizado_anual.csv', 'G02b_ratio_estandarizado_comparativa',
           'Sobrevaloración de la vivienda respecto a la renta: desviación sobre la media histórica',
           'Ratio precio/renta estandarizado: 100 = media de largo plazo de cada país. 1970-2025. La OCDE no calcula esta serie para Hungría.',
           'Fuente: OCDE, Analytical House Prices Indicators (standardised price-to-income ratio). Elaboración propia.',
           ref100=True)
    print('Gráficas generadas en graficas/color y graficas/bn')
