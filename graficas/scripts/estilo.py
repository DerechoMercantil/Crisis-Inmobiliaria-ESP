"""Sistema de estilo común para las gráficas de la monografía.

Dos modos:
- 'color': paleta categórica validada (CVD ΔE adyacente >= 24), para el repositorio.
- 'bn': escala de grises + estilos de trazo/marcador, para imprenta en blanco y negro.

Reglas aplicadas (método dataviz): un solo eje Y; orden fijo de tonos, nunca ciclado;
trazos finos (2 pt); rejilla y ejes recesivos; leyenda siempre con >= 2 series y
etiquetas directas selectivas; el texto siempre en tinta, nunca en el color de la serie.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

# Paleta categórica (orden fijo de slots; referencia validada del sistema dataviz)
COLOR = ['#2a78d6', '#1baf7a', '#eda100', '#008300', '#4a3aa7', '#e34948', '#e87ba4', '#eb6834']
# B/N: grises + diferenciación por trazo y marcador (canal de textura para imprenta)
GRIS = ['#000000', '#4d4d4d', '#8a8a8a', '#000000', '#4d4d4d', '#8a8a8a']
TRAZO_BN = ['-', '--', ':', '-.', (0, (5, 1, 1, 1)), (0, (1, 1))]
MARCA_BN = ['o', 's', '^', 'D', 'v', 'x']

TINTA = '#0b0b0b'
TINTA_2 = '#52514e'
MUTED = '#898781'
REJILLA = '#e1e0d9'
EJE = '#c3c2b7'
SURF = '#ffffff'


def nueva_figura(ancho=9.0, alto=5.2):
    fig, ax = plt.subplots(figsize=(ancho, alto), facecolor=SURF)
    ax.set_facecolor(SURF)
    for spine in ('top', 'right'):
        ax.spines[spine].set_visible(False)
    for spine in ('left', 'bottom'):
        ax.spines[spine].set_color(EJE)
        ax.spines[spine].set_linewidth(0.8)
    ax.grid(axis='y', color=REJILLA, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(colors=MUTED, labelsize=9, length=3)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_color(TINTA_2)
    return fig, ax


def serie(ax, x, y, i, modo, etiqueta, marcador=False, cada=1):
    """Dibuja una serie con el slot i de la paleta del modo."""
    if modo == 'color':
        kw = dict(color=COLOR[i % len(COLOR)], linestyle='-', linewidth=2.0)
        if marcador:
            kw.update(marker='o', markersize=3.5, markevery=cada)
    else:
        kw = dict(color=GRIS[i % len(GRIS)], linestyle=TRAZO_BN[i % len(TRAZO_BN)],
                  linewidth=1.7, marker=MARCA_BN[i % len(MARCA_BN)] if marcador or i >= 3 else None,
                  markersize=4, markevery=cada, markerfacecolor='white', markeredgewidth=1.0)
    return ax.plot(x, y, label=etiqueta, **kw)[0]


def titulos(fig, ax, titulo, subtitulo, fuente):
    fig.text(0.01, 0.985, titulo, ha='left', va='top', fontsize=13,
             fontweight='bold', color=TINTA)
    fig.text(0.01, 0.925, subtitulo, ha='left', va='top', fontsize=9.5, color=TINTA_2)
    fig.text(0.01, 0.01, fuente, ha='left', va='bottom', fontsize=7.5, color=MUTED, wrap=True)


def leyenda(ax, loc='best', ncol=1):
    leg = ax.legend(loc=loc, ncol=ncol, frameon=False, fontsize=9,
                    labelcolor=TINTA_2, handlelength=2.6)
    return leg


def etiqueta_final(ax, x, y, texto, modo, i, dx=0.5, dy=0):
    """Etiqueta directa al final de la línea, siempre en tinta."""
    ax.annotate(texto, xy=(x, y), xytext=(x + dx, y + dy), fontsize=8.5,
                color=TINTA_2, va='center', fontweight='bold')


def guardar(fig, nombre, modo, base='/Users/danielraya/dev/bitbucket/monografia-burbuja/graficas'):
    import os
    d = os.path.join(base, 'color' if modo == 'color' else 'bn')
    os.makedirs(d, exist_ok=True)
    for ext, dpi in (('png', 300), ('svg', None)):
        fig.savefig(os.path.join(d, f'{nombre}.{ext}'), dpi=dpi,
                    bbox_inches='tight', facecolor=SURF)
    plt.close(fig)
