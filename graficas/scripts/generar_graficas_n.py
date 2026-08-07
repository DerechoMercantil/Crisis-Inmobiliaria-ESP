#!/usr/bin/env python3
"""Gráficas de los nuevos grupos de datos N1-N6 (segunda entrega),
en color y B/N, desde las tablas de tablas/. PNG 300 ppp + SVG."""
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


def n1(modo):
    rows = leer('N1_espana_vpo_franquismo_anual.csv')
    x = [int(r['anio']) for r in rows]
    y = [float(r['vpo_terminadas']) / 1000 for r in rows]
    fig, ax = nueva_figura()
    color = estilo.COLOR[0] if modo == 'color' else '#4d4d4d'
    ax.bar(x, y, color=color, width=0.72)
    i65 = x.index(1965)
    ax.annotate(fmt(y[i65], 1), xy=(1965, y[i65]), xytext=(1965, y[i65] + 6),
                ha='center', fontsize=8.5, color=estilo.TINTA_2, fontweight='bold')
    ax.annotate(fmt(y[0], 1), xy=(x[0], y[0]), xytext=(x[0], y[0] + 6),
                ha='center', fontsize=8.5, color=estilo.TINTA_2, fontweight='bold')
    ax.set_ylabel('Miles de viviendas protegidas terminadas al año', fontsize=9, color=estilo.TINTA_2)
    ax.set_xticks(range(1958, 1976, 2))
    titulos(fig, ax,
            'La vivienda protegida del franquismo: hasta 241.000 terminadas en un año',
            'Viviendas acogidas a la protección del Estado terminadas (calificación definitiva), 1958-1975. Serie validada entre anuarios.',
            'Fuente: Anuarios Estadísticos de España (INE, fondo documental): anuarios 1965, 1971 y 1976. Elaboración propia.')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'N01_vpo_franquismo', modo)


def n2(modo):
    rows = [r for r in leer('N2_espana_vpo_por_promotor_anual.csv') if not r['nota']]
    x = [int(r['anio']) for r in rows]
    priv = [float(r['definitivas_promotor_privado']) / 1000 for r in rows]
    pub = [float(r['definitivas_promotor_publico']) / 1000 for r in rows]
    fig, ax = nueva_figura()
    if modo == 'color':
        kw1, kw2 = dict(color=estilo.COLOR[0]), dict(color=estilo.COLOR[2])
    else:
        kw1 = dict(color='#4d4d4d')
        kw2 = dict(color='white', edgecolor='#0b0b0b', hatch='///', linewidth=0.8)
    ax.bar(x, priv, width=0.72, label='Promotor privado', **kw1)
    ax.bar(x, pub, width=0.72, bottom=priv, label='Promotor público', **kw2)
    for xi, pv, pb in zip(x, priv, pub):
        pct = 100 * pb / (pv + pb)
        ax.annotate(fmt(pct, 0) + '%', xy=(xi, pv + pb), xytext=(xi, pv + pb + 0.35),
                    ha='center', fontsize=8, color=estilo.TINTA_2)
    ax.set_ylabel('Miles de calificaciones definitivas al año', fontsize=9, color=estilo.TINTA_2)
    ax.set_xticks(x)
    titulos(fig, ax,
            'Quién construye la VPO: el promotor público gana peso, pero sobre cifras mínimas',
            'Calificaciones definitivas de vivienda protegida por tipo de promotor (planes estatales y autonómicos), 2014-2025.\n'
            'Sobre cada barra, porcentaje del promotor público.',
            'Fuente: Mº de Vivienda y Agenda Urbana / MITMS, Boletín estadístico (cuadros 1.6.2.1-1.6.2.2). Elaboración propia.')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=False,
              fontsize=9, labelcolor=estilo.TINTA_2, handlelength=2.2)
    fig.subplots_adjust(top=0.80, bottom=0.17)
    guardar(fig, 'N02_vpo_por_promotor', modo)


def n3(modo):
    rows = leer('N3_espana_destinos_pms_2004.csv')
    etiquetas = [r['destino'] for r in rows]
    vals = [float(r['pct_sobre_valor_total']) for r in rows]
    cortas = ['Vivienda protegida', 'Interés social: urbanización y dotaciones',
              'Interés social: otros usos', 'Conservación del propio PMS',
              'Vivienda libre y otros usos autonómicos', 'Usos no previstos legalmente']
    import numpy as np
    orden = np.argsort(vals)
    ypos = np.arange(len(vals))
    fig, ax = nueva_figura(9.0, 4.8)
    ax.grid(False); ax.grid(axis='x', color=estilo.REJILLA, linewidth=0.7)
    for i, o in enumerate(orden):
        ilegal = 'no previstos' in etiquetas[o]
        protegida = 'protección pública' in etiquetas[o] or 'protegida' in cortas[o].lower()
        if modo == 'color':
            c = '#d03b3b' if ilegal else (estilo.COLOR[0] if protegida else '#9ec5f4')
            kw = dict(color=c)
        else:
            if ilegal:
                kw = dict(color='white', edgecolor='#0b0b0b', hatch='xxx', linewidth=0.9)
            elif protegida:
                kw = dict(color='#0b0b0b')
            else:
                kw = dict(color='#b5b5b5')
        ax.barh(i, vals[o], height=0.62, **kw)
        ax.text(vals[o] + 0.4, i, fmt(vals[o]) + ' %', va='center', fontsize=9,
                color=estilo.TINTA, fontweight='bold')
    ax.set_yticks(ypos)
    ax.set_yticklabels([cortas[o] for o in orden], fontsize=9.5, color=estilo.TINTA)
    ax.set_xlim(0, 26)
    ax.set_xlabel('% del valor total de los recursos empleados en 2004', fontsize=9, color=estilo.TINTA_2)
    titulos(fig, ax,
            'El suelo cedido para vivienda pública: solo el 16% acabó en vivienda protegida',
            'Destino de los recursos de los Patrimonios Municipales de Suelo, ejercicio 2004 (muestra de 144 grandes ayuntamientos).\n'
            'Un 18,4% se destinó a usos no previstos en la legislación. Solo el 14,6% de los ayuntamientos tenía el PMS formalmente constituido.',
            'Fuente: Tribunal de Cuentas, Informe de fiscalización de los PMS, ejercicio 2004 (BOE núm. 33, 7-2-2009, BOE-A-2009-2122). Elaboración propia.')
    fig.subplots_adjust(top=0.78, bottom=0.13, left=0.28)
    guardar(fig, 'N03_destinos_pms', modo)


def n4(modo):
    rows = leer('N4_espana_coste_construccion_vs_precio.csv')
    x = [int(r['anio']) for r in rows]
    pem = [float(r['pem_residencial_eur_m2']) for r in rows]
    pv = [float(r['precio_venta_eur_m2']) for r in rows]
    fig, ax = nueva_figura()
    serie(ax, x, pv, 0, modo, 'Precio de venta de la vivienda libre')
    serie(ax, x, pem, 1, modo, 'Coste de construcción (PEM de los visados)')
    if modo == 'color':
        ax.fill_between(x, pem, pv, color=estilo.COLOR[0], alpha=0.08)
    for anio, va in [(1996, 36.5), (2006, 18.5), (2025, 30.7)]:
        i = x.index(anio)
        ax.annotate(f'coste = {fmt(100*pem[i]/pv[i], 0)}%\ndel precio', xy=(anio, (pem[i]+pv[i])/2),
                    ha='center', fontsize=8, color=estilo.TINTA_2)
    ax.set_ylabel('Euros por m²', fontsize=9, color=estilo.TINTA_2)
    titulos(fig, ax,
            'La burbuja no fue de costes: construir costaba el 18% de lo que se cobraba (2006)',
            'Presupuesto de ejecución material por m² de la edificación residencial visada frente a precio de venta del m² de vivienda libre, 1992-2025.\n'
            'La franja entre ambas líneas (suelo, márgenes y demás costes) llegó al 81,5% del precio en 2006.',
            'Fuente: MITMS, visados de dirección de obra (cuadros 9.2-9.3); Mº Fomento/MIVAU y BdE (precio de venta). El PEM excluye IVA, honorarios, suelo y márgenes. Elaboración propia.')
    leyenda(ax, loc='upper left')
    fig.subplots_adjust(top=0.78, bottom=0.12)
    guardar(fig, 'N04_coste_vs_precio', modo)


def n4b(modo):
    rows = leer('N4b_espana_indices_costes_materiales.csv')
    x = [int(r['anio']) for r in rows]
    series = [('mano_de_obra', 'Mano de obra'), ('cemento', 'Cemento'),
              ('acero', 'Acero'), ('madera', 'Madera'), ('ceramica', 'Cerámica')]
    fig, ax = nueva_figura()
    tot = [float(r['coste_total_residencial']) for r in rows]
    if modo == 'color':
        ax.plot(x, tot, color=estilo.TINTA, linewidth=2.6, label='Coste total residencial')
    else:
        ax.plot(x, tot, color='#0b0b0b', linewidth=2.6, label='Coste total residencial')
    for i, (col, etq) in enumerate(series):
        serie(ax, x, [float(r[col]) for r in rows], i, modo, etq, marcador=True, cada=3)
    i22 = x.index(2022)
    ax.annotate(fmt(float(rows[i22]['acero']), 0), xy=(2022, float(rows[i22]['acero'])),
                xytext=(2019.8, 268), fontsize=8.5, color=estilo.TINTA_2, fontweight='bold')
    ax.set_ylabel('Índice de costes (2005 = 100)', fontsize=9, color=estilo.TINTA_2)
    ax.set_xticks(range(2005, 2024, 2))
    titulos(fig, ax,
            'Qué encareció construir: acero y energía, no la mano de obra',
            'Índice de Costes del Sector de la Construcción, componentes seleccionados, 2005-2023 (2005 = 100).\n'
            'Coste total de la edificación residencial en trazo grueso; el acero llegó a +176% en 2022.',
            'Fuente: MITMS, Índice de Costes del Sector de la Construcción, base 2015 (cuadros 1 y 2.1-2.2 del Boletín estadístico). Elaboración propia.')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=False,
              fontsize=9, labelcolor=estilo.TINTA_2, handlelength=2.2)
    fig.subplots_adjust(top=0.78, bottom=0.19)
    guardar(fig, 'N04b_indices_costes_materiales', modo)


def n5(modo):
    rows = leer('N5_espana_precio_suelo_anual.csv')
    x = [int(r['anio']) for r in rows]
    nac = [float(r['precio_suelo_eur_m2_nacional']) for r in rows]
    g50 = [float(r['precio_suelo_eur_m2_mun_mas_50k']) for r in rows]
    fig, ax = nueva_figura()
    serie(ax, x, g50, 0, modo, 'Municipios de más de 50.000 habitantes', marcador=True)
    serie(ax, x, nac, 1, modo, 'Total nacional', marcador=True)
    etiqueta_final(ax, x[-1], g50[-1], fmt(g50[-1], 0), modo, 0, dx=0.3)
    etiqueta_final(ax, x[-1], nac[-1], fmt(nac[-1], 0), modo, 1, dx=0.3)
    ax.set_ylabel('Euros por m² de suelo urbano transaccionado', fontsize=9, color=estilo.TINTA_2)
    ax.set_ylim(0, 750)
    titulos(fig, ax,
            'El precio del suelo urbano transaccionado: del pico de 2007 a la mitad',
            'Precio medio del m² de suelo urbano en transacciones, medias anuales, 2004-2025. La composición de lo transaccionado varía con el ciclo.',
            'Fuente: MITMS/MIVAU, Estadística de Precios de Suelo Urbano (cuadros 4 y 4.5). Elaboración propia.')
    leyenda(ax, loc='upper right')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'N05_precio_suelo', modo)


def n6(modo):
    rows = leer('N6_espana_iniciadas_por_decadas.csv')
    per = [r['periodo'] for r in rows]
    lib = [float(r['iniciadas_libres']) / 1e6 for r in rows]
    pro = [float(r['iniciadas_protegidas']) / 1e6 for r in rows]
    pct = [r['pct_protegidas'] for r in rows]
    import numpy as np
    xpos = np.arange(len(per))
    fig, ax = nueva_figura()
    if modo == 'color':
        kw1, kw2 = dict(color=estilo.COLOR[0]), dict(color=estilo.COLOR[2])
    else:
        kw1 = dict(color='#4d4d4d')
        kw2 = dict(color='white', edgecolor='#0b0b0b', hatch='///', linewidth=0.8)
    ax.bar(xpos, lib, width=0.6, label='Libres', **kw1)
    ax.bar(xpos, pro, width=0.6, bottom=lib, label='Protegidas', **kw2)
    for xi, l, p, q in zip(xpos, lib, pro, pct):
        ax.annotate(f'{fmt(float(q))}%\nprotegidas', xy=(xi, l + p), xytext=(xi, l + p + 0.15),
                    ha='center', fontsize=8.5, color=estilo.TINTA_2)
    ax.set_xticks(xpos)
    ax.set_xticklabels(per, fontsize=10, color=estilo.TINTA)
    ax.set_ylabel('Millones de viviendas iniciadas en la década', fontsize=9, color=estilo.TINTA_2)
    ax.set_ylim(0, 6.2)
    titulos(fig, ax,
            'Cinco décadas de construcción: de 7 de cada 10 protegidas a 1 de cada 8',
            'Viviendas iniciadas por décadas, libres y protegidas, 1976-2025. En 1976-1985 las libres solo constan desde 1980.',
            'Fuente: Mº de Vivienda y Agenda Urbana, vía Banco de España (Síntesis de Indicadores, cuadro 1.5). Elaboración propia.')
    leyenda(ax, loc='upper right')
    fig.subplots_adjust(top=0.83, bottom=0.12)
    guardar(fig, 'N06_decadas_libres_protegidas', modo)


TODAS_N = [n1, n2, n3, n4, n4b, n5, n6]

if __name__ == '__main__':
    for modo in ('color', 'bn'):
        for fn in TODAS_N:
            fn(modo)
    print('Gráficas N1-N6 generadas en graficas/color y graficas/bn')
