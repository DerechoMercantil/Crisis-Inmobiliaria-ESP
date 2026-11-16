"""Gráficos definitivos de la monografía (numeración por orden de aparición).

Genera, para cada gráfico impreso:
  bn/      TIFF 600 ppp en escala de grises + PDF vectorial (imprenta)
  color/   TIFF 600 ppp + PDF vectorial + PNG (eBook y repositorio)
  editables/  libro Excel con los datos y el gráfico editable (color y B/N)
  interactivas/  HTML con Plotly (título, subtítulo, fuente y tabla de datos)
  datos/   CSV con la serie exacta representada

Uso:  python3 generar_graficos_definitivos.py [--con-titulo]
Por defecto las imágenes de imprenta NO llevan el título incrustado: el título y la
fuente van en el pie del gráfico, en el texto. Con --con-titulo se incrustan título y fuente.
Los gráficos complementarios, que no tienen pie en el libro, los llevan siempre.

Datos de partida: tablas del repositorio de la obra (carpeta TABLAS) y cuadro 1.5 de la
Síntesis de indicadores del Banco de España (BDE).
"""
import csv, io, os, shutil, sys, html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SALIDA = os.path.join(RAIZ, 'graficos_impresos')
TABLAS = os.path.join(RAIZ, 'tablas')
BDE = os.path.join(RAIZ, 'datos_fuente', 'bde_si_1_5.csv')
PLOTLY_JS = os.path.join(AQUI, 'plotly.min.js')
CON_TITULO = '--con-titulo' in sys.argv

# ---------------------------------------------------------------- estilo
# Paleta categórica en orden fijo (validada: validate_palette.js, modo claro, todo PASS).
COLOR = ['#2a78d6', '#1baf7a', '#eda100', '#008300', '#4a3aa7', '#e87ba4']
GRIS = ['#000000', '#6e6e6e', '#a8a8a8', '#3d3d3d', '#8c8c8c', '#5a5a5a']
TRAZO_BN = ['-', '-', '-', (0, (6, 2)), (0, (1, 1.2)), (0, (5, 1.5, 1, 1.5))]
MARCA = ['o', 's', '^', 'D', 'v', 'x']
TINTA, TINTA_2, MUTED, REJILLA, EJE = '#0b0b0b', '#3f3e3b', '#6b6a66', '#e1e0d9', '#b5b4aa'
ANCHO_MM, ALTO_MM = 150, 92
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'pdf.fonttype': 42,
                     'axes.unicode_minus': False, 'hatch.linewidth': 0.6})


def base(g):
    return f"{g.get('prefijo', 'Grafico')}_{g['n']:02d}_{g['slug']}"


def es(v, dec=1):
    return f'{v:.{dec}f}'.replace('.', ',')


def figura(alto_mm=ALTO_MM):
    fig, ax = plt.subplots(figsize=(ANCHO_MM / 25.4, alto_mm / 25.4), facecolor='white')
    ax.set_facecolor('white')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color(EJE)
        ax.spines[s].set_linewidth(0.7)
    ax.grid(axis='y', color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(colors=TINTA_2, labelsize=7.5, length=2.5, width=0.6)
    return fig, ax


def estilo(i, modo):
    if modo == 'color':
        return dict(color=COLOR[i], linestyle='-', linewidth=1.6)
    return dict(color=GRIS[i], linestyle=TRAZO_BN[i], linewidth=1.4)


def marca(i, modo):
    c = COLOR[i] if modo == 'color' else GRIS[i]
    return dict(marker=MARCA[i], markersize=3.2, markerfacecolor='white', markeredgecolor=c,
                markeredgewidth=0.9, linestyle='none')


def etiqueta(ax, x, y, texto, dx=0.0, dy=0.0, ha='left', negrita=True):
    ax.annotate(texto, xy=(x, y), xytext=(x + dx, y + dy), fontsize=7.5, color=TINTA,
                va='center', ha=ha, fontweight='bold' if negrita else 'normal')


def leyenda(ax, handles, **kw):
    base = dict(frameon=False, fontsize=7.5, labelcolor=TINTA_2, handlelength=2.8, borderaxespad=0.2)
    base.update(kw)
    return ax.legend(handles=handles, **base)


def guardar(fig, g, modo):
    nombre = f"{base(g)}_{'BN' if modo == 'bn' else 'color'}"
    carpeta = os.path.join(SALIDA, modo)
    os.makedirs(carpeta, exist_ok=True)
    if CON_TITULO or g.get('con_titulo'):
        # Título arriba y fuente abajo, fuera de la caja ocupada por el gráfico y su leyenda.
        import textwrap
        fig.canvas.draw()
        caja = fig.get_tightbbox(fig.canvas.get_renderer())
        ancho, alto = fig.get_size_inches()
        x0 = caja.x0 / ancho
        rotulo = f"{g.get('rotulo', 'Gráfico')} {g['n']}. "
        fig.text(x0, (caja.y1 + 0.10) / alto, textwrap.fill(rotulo + g['titulo'], 82), ha='left', va='bottom',
                 fontsize=8.5, fontweight='bold', color=TINTA, linespacing=1.25)
        fig.text(x0, (caja.y0 - 0.10) / alto, textwrap.fill('Fuente: ' + g['fuente'], 112), ha='left', va='top',
                 fontsize=6.8, color=MUTED, linespacing=1.25)
    fig.savefig(os.path.join(carpeta, nombre + '.pdf'), bbox_inches='tight', pad_inches=0.03)
    tmp = os.path.join(carpeta, nombre + '.png')
    fig.savefig(tmp, dpi=600, bbox_inches='tight', pad_inches=0.03, facecolor='white')
    im = Image.open(tmp)
    fondo = Image.new('RGB', im.size, 'white')
    fondo.paste(im, mask=im.split()[3] if im.mode == 'RGBA' else None)
    fondo = fondo.convert('L') if modo == 'bn' else fondo
    fondo.save(os.path.join(carpeta, nombre + '.tif'), dpi=(600, 600), compression='tiff_lzw')
    if modo == 'bn':
        os.remove(tmp)
    else:
        fondo.resize((1800, int(fondo.height * 1800 / fondo.width)), Image.LANCZOS).save(tmp, dpi=(300, 300))
    plt.close(fig)


def leer(nombre):
    with open(os.path.join(TABLAS, nombre), encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def num(v):
    return float(v) if v not in ('', None) else None


def exportar(g, cabecera, filas):
    os.makedirs(os.path.join(SALIDA, 'datos'), exist_ok=True)
    ruta = os.path.join(SALIDA, 'datos', base(g) + '.csv')
    with open(ruta, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(cabecera)
        w.writerows(filas)


def linea_medida(ax, x, y, medido, i, modo):
    """Serie con tramos medidos (trazo continuo) e interpolados (punteado); marcas en años con encuesta."""
    st = estilo(i, modo)
    for a in range(len(x) - 1):
        solido = medido[a] and medido[a + 1]
        ax.plot(x[a:a + 2], y[a:a + 2], color=st['color'], linewidth=st['linewidth'],
                linestyle='-' if solido else (0, (1, 1.6)), solid_capstyle='round')
    xm = [a for a, m in zip(x, medido) if m]
    ym = [b for b, m in zip(y, medido) if m]
    ax.plot(xm, ym, **marca(i, modo))


def mango(i, modo, texto):
    st = estilo(i, modo)
    mk = marca(i, modo)
    return Line2D([0], [0], color=st['color'], linewidth=st['linewidth'], linestyle='-', marker=mk['marker'],
                  markersize=mk['markersize'], markerfacecolor='white', markeredgecolor=st['color'],
                  markeredgewidth=0.9, label=texto)


# ---------------------------------------------------------------- metadatos
FUENTE_EDAD = ('Elaboración propia con microdatos del INE (EPF 1980-1981, EBPF 1990-1991, PHOGUE 1994-2001 y '
               'ECV 2004-2025). Precio: valor de tasación (Ministerio; BIS antes de 1987) hasta 2007 e Índice de '
               'Precios de Vivienda del INE desde 2008.')
G = {
    1: dict(n=1, slug='precio_vivienda_renta_joven_y_hogar', origen='G01c', capitulo='Introducción general',
            titulo='Precio de la vivienda tipo en años de renta disponible del perceptor mediano de 18 a 35 años y del hogar mediano (España, 1980-2024)',
            sub='Vivienda libre de 93,75 m² construidos. Renta disponible anual mediana, neta de impuestos y cotizaciones. Trazo punteado: años sin encuesta, interpolados.',
            fuente=FUENTE_EDAD),
    2: dict(n=2, slug='precio_vivienda_renta_por_edad', origen='G01d', capitulo='Introducción general',
            titulo='Precio de la vivienda tipo en años de renta disponible del perceptor mediano, por grupo de edad (España, 1980-2024)',
            sub='Vivienda libre de 93,75 m² construidos. Perceptor mediano de 18 a 35, de 55 a 64 y de 65 a 74 años. Trazo punteado: años sin encuesta, interpolados.',
            fuente=FUENTE_EDAD),
    3: dict(n=3, slug='credito_construccion_y_hogares_pib', origen='G21', capitulo='D. Raya Quero, epígrafe IV.3',
            titulo='Crédito con garantía inmobiliaria a la construcción y las actividades inmobiliarias y crédito a los hogares para vivienda, en porcentaje del PIB (España, 1999-2025)',
            sub='Saldo vivo a diciembre de cada año, en porcentaje del PIB.',
            fuente='Banco de España, Síntesis de indicadores, cuadro 1.5 (series SI_1_5.54 y SI_1_5.56).'),
    4: dict(n=4, slug='tenencia_jovenes_emancipados', origen='G23', capitulo='D. Raya Quero, epígrafe VI.2',
            titulo='Régimen de tenencia de los jóvenes de 18 a 34 años que se emancipan y tasa anual de emancipación (España, 2005-2025)',
            sub='Jóvenes que vivían con sus padres un año y en su propio hogar el siguiente, por régimen de tenencia del nuevo hogar (% del total de cada periodo).',
            fuente='Elaboración propia con los ficheros longitudinales de la Encuesta de Condiciones de Vida del INE (2005-2008, 2009-2012, 2015-2018 y 2022-2025).'),
    5: dict(n=5, slug='precios_reales_vivienda_comparados', origen='G04', capitulo='V. Blazsek, epígrafe IV',
            titulo='Precios reales de la vivienda en España, Hungría, Italia, el Reino Unido y la zona del euro (índice 2015 = 100, 1971-2025)',
            sub='Índice de precios de la vivienda deflactado por el IPC de cada país, medias anuales. Hungría, desde 1992; zona del euro, desde 1975.',
            fuente='Banco de Pagos Internacionales, Selected residential property prices (series reales). Elaboración propia.'),
    6: dict(n=6, slug='viviendas_terminadas_y_hogares', origen='G11', capitulo='C. J. Rusillo Ramiro, epígrafe VI',
            titulo='Viviendas terminadas y variación anual del número de hogares (España, 1971-2025)',
            sub='Viviendas libres y protegidas terminadas cada año y hogares nuevos. Hogares: promedio entre censos hasta 2001 (trazo discontinuo), EPA en 2002-2020 y Estadística Continua de Población desde 2021.',
            fuente='Ministerio de Vivienda y Agenda Urbana (viviendas terminadas; 1971-1990, vía OCDE) e INE (censos, Encuesta de Población Activa y Estadística Continua de Población). Elaboración propia.'),
}


# ---------------------------------------------------------------- datos
def datos_1():
    r = leer('G01c_espana_ratio_precio_renta_joven_1980_2024.csv')
    x = [int(a['anio']) for a in r]
    med = [a['tipo'].startswith('medido') for a in r]
    return x, [float(a['anios_renta_joven_18_35']) for a in r], [float(a['anios_renta_hogar_mediano']) for a in r], med


def datos_2():
    r = leer('G01d_espana_ratio_precio_renta_por_edad_1980_2024.csv')
    x = [int(a['anio']) for a in r]
    med = [a['tipo'].startswith('medido') for a in r]
    return x, [[float(a[f'anios_renta_{k}']) for a in r] for k in ('18_35', '55_64', '65_74')], med


def datos_3():
    raw = open(BDE, 'rb').read().decode('latin-1')
    filas = list(csv.reader(io.StringIO(raw)))
    cab = None
    for f in filas[:8]:
        if any('SI_1_5.54' in c for c in f):
            cab = f
            break
    i54 = next(k for k, c in enumerate(cab) if 'SI_1_5.54' in c)
    i56 = next(k for k, c in enumerate(cab) if 'SI_1_5.56' in c)
    meses = {'DIC': 12}
    out = {}
    for f in filas:
        if not f or len(f) <= max(i54, i56):
            continue
        t = f[0].strip().upper()
        if t[:3] in meses and t[-4:].isdigit():
            try:
                out[int(t[-4:])] = (float(f[i54].replace(',', '.')), float(f[i56].replace(',', '.')))
            except ValueError:
                pass
    x = sorted(a for a in out if 1999 <= a <= 2025)
    return x, [out[a][0] for a in x], [out[a][1] for a in x]


def datos_4():
    r = leer('G19_espana_emancipacion_y_alquiler_de_entrada_2005_2025.csv')
    cats = [('destino_propiedad_hipoteca_pct', 'Vivienda en propiedad con hipoteca'),
            ('destino_propiedad_sin_hipoteca_pct', 'Vivienda en propiedad sin hipoteca'),
            ('destino_alquiler_mercado_pct', 'Alquiler a precio de mercado'),
            ('destino_otros_pct', 'Otros (cesión, alquiler inferior al de mercado)')]
    return r, cats


def datos_5():
    r = leer('G04_comparativa_precios_reales_anual.csv')
    paises = [('Hungria', 'Hungría'), ('Espana', 'España'), ('ZonaEuro', 'Zona del euro'),
              ('Italia', 'Italia'), ('ReinoUnido', 'Reino Unido')]
    r = [a for a in r if 1971 <= int(a['anio']) <= 2025]
    return [int(a['anio']) for a in r], {k: [num(a[k]) for a in r] for k, _ in paises}, paises


def datos_6():
    r = leer('G11_espana_hogares_vs_viviendas_terminadas_1971_2025.csv')
    x = [int(a['anio']) for a in r]
    viv = [float(a['viviendas_terminadas']) / 1000 for a in r]
    hog, fuente = [], []
    for a in r:
        if a.get('hogares_nuevos_ecp'):
            hog.append(float(a['hogares_nuevos_ecp']) / 1000)
            fuente.append('Estadística Continua de Población')
        else:
            hog.append(float(a['hogares_nuevos']) / 1000)
            fuente.append('promedio entre censos' if int(a['anio']) <= 2001 else 'EPA / parque de viviendas principales')
    return x, viv, hog, fuente


# ---------------------------------------------------------------- gráficos estáticos
def g1(modo):
    x, joven, hogar, med = datos_1()
    fig, ax = figura()
    linea_medida(ax, x, joven, med, 0, modo)
    linea_medida(ax, x, hogar, med, 4, modo)
    ax.set_ylim(0, 20)
    ax.set_yticks(range(0, 21, 5))
    ax.set_xlim(1978.5, 2027.5)
    ax.set_xticks(range(1980, 2021, 10))
    ax.set_ylabel('Años de renta disponible', fontsize=7.5, color=TINTA_2)
    for serie, dy in ((joven, 0.9), (hogar, -0.9)):
        etiqueta(ax, x[0], serie[0], es(serie[0]), dy=dy, ha='center')
        etiqueta(ax, x[-1], serie[-1], es(serie[-1]), dx=0.6)
    etiqueta(ax, 2007, joven[x.index(2007)], es(joven[x.index(2007)]), dy=0.9, ha='center')
    leyenda(ax, [mango(0, modo, 'Perceptor mediano de 18 a 35 años'), mango(4, modo, 'Hogar mediano'),
                 Line2D([0], [0], color=MUTED, linestyle=(0, (1, 1.6)), linewidth=1.4, label='Años sin encuesta (interpolado)')],
            loc='upper left')
    guardar(fig, G[1], modo)


def g2(modo):
    x, series, med = datos_2()
    nombres = ['Perceptor mediano de 18 a 35 años', 'Perceptor mediano de 55 a 64 años', 'Perceptor mediano de 65 a 74 años']
    fig, ax = figura()
    for i, s in enumerate(series):
        linea_medida(ax, x, s, med, i, modo)
    ax.set_ylim(0, 28)
    ax.set_yticks(range(0, 26, 5))
    ax.set_xticks(range(1980, 2021, 10))
    ax.set_ylabel('Años de renta disponible', fontsize=7.5, color=TINTA_2)
    etiqueta(ax, x[0], series[2][0], es(series[2][0]), dx=-0.6, ha='right')
    etiqueta(ax, x[0], series[1][0], es(series[1][0]), dx=-0.6, dy=0.45, ha='right')
    etiqueta(ax, x[0], series[0][0], es(series[0][0]), dx=-0.6, dy=-0.5, ha='right')
    etiqueta(ax, x[-1], series[0][-1], es(series[0][-1]), dx=0.6)
    etiqueta(ax, x[-1], series[1][-1], es(series[1][-1]) + ' (ambos)', dx=0.6, negrita=True)
    k = x.index(2007)
    etiqueta(ax, 2007, series[2][k], es(series[2][k]), dy=1.0, ha='center')
    ax.set_xlim(1976.5, 2030.5)
    leyenda(ax, [mango(i, modo, n) for i, n in enumerate(nombres)] +
            [Line2D([0], [0], color=MUTED, linestyle=(0, (1, 1.6)), linewidth=1.4, label='Años sin encuesta (interpolado)')],
            loc='upper left')
    guardar(fig, G[2], modo)


def g3(modo):
    x, constr, hog = datos_3()
    fig, ax = figura()
    ax.plot(x, hog, **estilo(0, modo))
    ax.plot(x, constr, **estilo(1, modo))
    if modo == 'bn':
        ax.plot(x[::2], constr[::2], **marca(1, modo))
    ax.set_ylim(0, 70)
    ax.set_xlim(1998.3, 2028.5)
    ax.yaxis.set_major_formatter(lambda v, _: f'{v:.0f} %')
    k = x.index(2007)
    etiqueta(ax, 2007, constr[k], es(constr[k]) + ' %', dy=3.2, ha='center')
    etiqueta(ax, 2007, hog[k], es(hog[k]) + ' %', dx=-0.5, dy=3.2, ha='right')
    etiqueta(ax, x[-1], constr[-1], es(constr[-1]) + ' %', dx=0.5)
    etiqueta(ax, x[-1], hog[-1], es(hog[-1]) + ' %', dx=0.5)
    h = [Line2D([0], [0], label='Crédito a los hogares para adquisición de vivienda', **estilo(0, modo)),
         Line2D([0], [0], label='Crédito con garantía inmobiliaria a la construcción y las actividades inmobiliarias',
                **estilo(1, modo), **({k2: v for k2, v in marca(1, modo).items() if k2 != 'linestyle'} if modo == 'bn' else {}))]
    leyenda(ax, h, loc='upper center', bbox_to_anchor=(0.5, -0.1))
    guardar(fig, G[3], modo)


def g4(modo):
    r, cats = datos_4()
    fig, ax = figura(alto_mm=80)
    ax.grid(False)
    ax.grid(axis='x', color=REJILLA, linewidth=0.6)
    rellenos = COLOR[:4] if modo == 'color' else ['#2b2b2b', '#8c8c8c', '#ffffff', '#d4d4d4']
    tramas = [None] * 4 if modo == 'color' else [None, None, '////', None]
    etiquetas_y = []
    for j, fila in enumerate(r):
        izq = 0.0
        for i, (col, _) in enumerate(cats):
            v = float(fila[col])
            ax.barh(j, v, left=izq, height=0.62, color=rellenos[i], edgecolor='white' if modo == 'color' else '#2b2b2b',
                    linewidth=1.2 if modo == 'color' else 0.6, hatch=tramas[i])
            if v >= 8:
                oscuro = rellenos[i] in ('#2b2b2b', '#2a78d6', '#008300')
                ax.text(izq + v / 2, j, f'{es(v, 0)} %', ha='center', va='center', fontsize=7.5, fontweight='bold',
                        color='white' if oscuro else TINTA,
                        bbox=dict(facecolor='white', edgecolor='none', pad=0.6) if tramas[i] else None)
            izq += v
        etiquetas_y.append(f"{fila['panel']}\n(tasa anual: {es(float(fila['tasa_emancipacion_anual_pct']))} %)")
    ax.set_yticks(range(len(r)))
    ax.set_yticklabels(etiquetas_y, fontsize=7.5, color=TINTA_2)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(lambda v, _: f'{v:.0f} %')
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    h = [Patch(facecolor=rellenos[i], edgecolor='#2b2b2b' if modo == 'bn' else 'none', linewidth=0.5, hatch=tramas[i], label=n)
         for i, (_, n) in enumerate(cats)]
    leyenda(ax, h, loc='upper center', bbox_to_anchor=(0.42, -0.1), ncol=2, handlelength=1.6)
    guardar(fig, G[4], modo)


def g5(modo):
    x, d, paises = datos_5()
    fig, ax = figura()
    for i, (k, nombre) in enumerate(paises):
        xs = [a for a, v in zip(x, d[k]) if v is not None]
        ys = [v for v in d[k] if v is not None]
        st = estilo(i, modo)
        if i == 0:
            st['linewidth'] = 2.0
        ax.plot(xs, ys, **st)
        if modo == 'bn' and i in (1, 2):
            ax.plot(xs[::4], ys[::4], **marca(i, modo))
    ax.set_xlim(1969.5, 2036)
    ax.set_xticks(range(1970, 2021, 10))
    ax.set_ylim(0, 230)
    ax.set_ylabel('Índice (2015 = 100)', fontsize=7.5, color=TINTA_2)
    fin = {k: next(v for v in reversed(d[k]) if v is not None) for k, _ in paises}
    pos = {'Hungria': fin['Hungria'], 'Espana': fin['Espana'], 'ZonaEuro': fin['ZonaEuro'] + 5,
           'ReinoUnido': fin['ReinoUnido'] - 3, 'Italia': fin['Italia'] - 6}
    for k, nombre in paises:
        etiqueta(ax, 2025, pos[k], f'{nombre} ({es(fin[k], 0)})', dx=0.7, negrita=(k in ('Hungria', 'Espana')))
    kk = x.index(2007)
    etiqueta(ax, 2007, d['Espana'][kk], f"España, 2007: {es(d['Espana'][kk], 0)}", dx=-1.0, dy=7, ha='right', negrita=False)
    h = []
    for i, (k, nombre) in enumerate(paises):
        st = estilo(i, modo)
        if i == 0:
            st['linewidth'] = 2.0
        extra = {a: b for a, b in marca(i, modo).items() if a != 'linestyle'} if (modo == 'bn' and i in (1, 2)) else {}
        h.append(Line2D([0], [0], label=nombre, **st, **extra))
    leyenda(ax, h, loc='upper left')
    guardar(fig, G[5], modo)


def g6(modo):
    x, viv, hog, fuente = datos_6()
    fig, ax = figura()
    corte = x.index(2001)
    ax.fill_between(x, viv, hog, where=[h > v for h, v in zip(hog, viv)], interpolate=True,
                    color='#e4e3dc' if modo == 'color' else '#dcdcdc', linewidth=0)
    st0, st1 = estilo(0, modo), estilo(1, modo)
    ax.plot(x, viv, **st0)
    ax.plot(x[:corte + 1], hog[:corte + 1], color=st1['color'], linewidth=st1['linewidth'], linestyle=(0, (4, 2)))
    ax.plot(x[corte:], hog[corte:], color=st1['color'], linewidth=st1['linewidth'], linestyle='-')
    if modo == 'bn':
        ax.plot(x[corte + 1::2], hog[corte + 1::2], **marca(1, modo))
    ax.set_ylim(0, 720)
    ax.set_xlim(1969.5, 2027)
    ax.set_xticks(range(1970, 2021, 10))
    ax.set_ylabel('Miles al año', fontsize=7.5, color=TINTA_2)
    def ratio(a, b):
        ia, ib = x.index(a), x.index(b) + 1
        return sum(viv[ia:ib]) / sum(hog[ia:ib])
    ax.annotate(f'1997-2007: {es(ratio(1997, 2007), 2)} viviendas\npor cada hogar nuevo', xy=(2001, 600), fontsize=7.5,
                color=TINTA, ha='right', va='center', fontweight='bold')
    ax.annotate(f'2021-2025: {es(ratio(2021, 2025), 2)} viviendas\npor cada hogar nuevo', xy=(2023, 400), fontsize=7.5,
                color=TINTA, ha='center', va='center', fontweight='bold')
    extra = {a: b for a, b in marca(1, modo).items() if a != 'linestyle'} if modo == 'bn' else {}
    h = [Line2D([0], [0], label='Viviendas terminadas (libres y protegidas)', **st0),
         Line2D([0], [0], label='Hogares nuevos', **st1, **extra),
         Line2D([0], [0], color=st1['color'], linewidth=st1['linewidth'], linestyle=(0, (4, 2)),
                label='Hogares nuevos, promedio entre censos (1971-2001)'),
         Patch(facecolor='#e4e3dc' if modo == 'color' else '#dcdcdc', label='Más hogares nuevos que viviendas terminadas')]
    leyenda(ax, h, loc='upper center', bbox_to_anchor=(0.5, -0.09), ncol=2)
    guardar(fig, G[6], modo)


# ---------------------------------------------------------------- Excel editable
def excel(g, cabecera, filas, tipo='linea', eje_y='', n_series=None, formato='0.0'):
    from openpyxl import Workbook
    from openpyxl.chart import LineChart, BarChart, Reference
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = 'Datos'
    ws['A1'] = f"{g.get('rotulo', 'Gráfico')} {g['n']}. {g['titulo']}"
    ws['A1'].font = Font(bold=True)
    ws['A2'] = g['sub']
    ws['A3'] = 'Fuente: ' + g['fuente']
    ws.append([])
    ws.append(cabecera)
    for c in ws[5]:
        c.font = Font(bold=True)
    for f in filas:
        ws.append(f)
    n_series = n_series or (len(cabecera) - 1)
    f0, f1 = 5, 5 + len(filas)
    ws.column_dimensions['A'].width = 14
    for modo, nombre in (('color', 'Gráfico (color)'), ('bn', 'Gráfico (B y N)')):
        hoja = wb.create_sheet(nombre)
        if tipo == 'linea':
            ch = LineChart()
        elif tipo == 'columnas':
            ch = BarChart()
            ch.type = 'col'
        else:
            ch = BarChart()
            ch.type = 'bar'
            ch.grouping = 'percentStacked'
            ch.overlap = 100
        ch.add_data(Reference(ws, min_col=2, max_col=1 + n_series, min_row=f0, max_row=f1), titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=1, min_row=f0 + 1, max_row=f1))
        ch.title = None
        ch.y_axis.title = eje_y
        ch.y_axis.number_format = formato
        ch.legend.position = 'b'
        ch.height, ch.width = 9.2, 15.0
        ch.x_axis.delete = False
        ch.y_axis.delete = False
        guiones = ['solid', 'solid', 'solid', 'dash', 'sysDot', 'dashDot']
        orden = g.get('orden') or ([0, 4] if (g['n'] == 1 and 'prefijo' not in g) else list(range(6)))
        for i, s in enumerate(ch.series):
            j = orden[i % len(orden)]
            c = (COLOR[j] if modo == 'color' else GRIS[j]).lstrip('#').upper()
            if tipo == 'linea':
                s.graphicalProperties.line.solidFill = c
                s.graphicalProperties.line.width = 20000
                s.smooth = False
                if modo == 'bn':
                    s.graphicalProperties.line.dashStyle = guiones[j]
                s.marker.symbol = 'none'
            else:
                relleno = COLOR[j] if modo == 'color' else ['#2b2b2b', '#8c8c8c', '#ffffff', '#d4d4d4'][i]
                s.graphicalProperties.solidFill = relleno.lstrip('#').upper()
                s.graphicalProperties.line.solidFill = 'FFFFFF' if modo == 'color' else '2B2B2B'
        hoja.add_chart(ch, 'A1')
    os.makedirs(os.path.join(SALIDA, 'editables'), exist_ok=True)
    wb.save(os.path.join(SALIDA, 'editables', base(g) + '.xlsx'))


# ---------------------------------------------------------------- HTML interactivo
PLANTILLA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{rotulo} {n}. {titulo_corto}</title>
<style>
:root{{--tinta:#0b0b0b;--tinta2:#3f3e3b;--muted:#6b6a66;--linea:#e1e0d9;--fondo:#fcfcfb}}
body{{margin:0;background:var(--fondo);color:var(--tinta);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
main{{max-width:960px;margin:0 auto;padding:24px 16px 40px}}
.n{{font-size:13px;color:var(--muted);margin:0 0 4px}}
h1{{font-size:19px;line-height:1.35;margin:0 0 8px;font-weight:650}}
.sub{{font-size:14px;line-height:1.5;color:var(--tinta2);margin:0 0 12px;max-width:75ch}}
.fuente{{font-size:12.5px;line-height:1.5;color:var(--muted);margin:10px 0 18px;max-width:85ch}}
details{{border-top:1px solid var(--linea);padding-top:10px}}
summary{{cursor:pointer;font-size:14px;color:var(--tinta2)}}
.tabla{{overflow-x:auto;margin-top:10px}}
table{{border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums}}
th,td{{padding:4px 12px;border-bottom:1px solid var(--linea);text-align:right;white-space:nowrap}}
th:first-child,td:first-child{{text-align:left}}
th{{color:var(--tinta2);font-weight:600}}
</style><script src="plotly.min.js"></script></head>
<body><main>
<p class="n">{rotulo} {n} · {capitulo}</p>
<h1>{titulo}</h1>
<p class="sub">{sub}</p>
{grafico}
<p class="fuente">Fuente: {fuente}</p>
<details><summary>Ver los datos en tabla</summary><div class="tabla">{tabla}</div></details>
</main></body></html>
"""


def html_pagina(g, fig, cabecera, filas, dec=1):
    fig.update_layout(template='plotly_white', paper_bgcolor='#fcfcfb', plot_bgcolor='#fcfcfb',
                      font=dict(family='system-ui, -apple-system, Segoe UI, Roboto, sans-serif', size=13, color='#3f3e3b'),
                      margin=dict(l=56, r=24, t=16, b=48), height=460, separators=',.',
                      legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
                      hoverlabel=dict(bgcolor='white', font_size=13))
    fig.update_xaxes(showgrid=False, linecolor='#b5b4aa', ticks='outside', tickcolor='#b5b4aa')
    fig.update_yaxes(gridcolor='#e1e0d9', zeroline=False)
    cuerpo = fig.to_html(full_html=False, include_plotlyjs=False, config=dict(displaylogo=False, responsive=True,
                         modeBarButtonsToRemove=['lasso2d', 'select2d', 'autoScale2d']))
    def celda(v):
        if v is None or v == '':
            return '—'
        return es(v, dec) if isinstance(v, float) else html.escape(str(v))
    tabla = '<table><thead><tr>' + ''.join(f'<th>{html.escape(c)}</th>' for c in cabecera) + '</tr></thead><tbody>'
    tabla += ''.join('<tr>' + ''.join(f'<td>{celda(v)}</td>' for v in f) + '</tr>' for f in filas) + '</tbody></table>'
    os.makedirs(os.path.join(SALIDA, 'interactivas'), exist_ok=True)
    corto = g['titulo'].split(' (')[0]
    with open(os.path.join(SALIDA, 'interactivas', base(g) + '.html'), 'w', encoding='utf-8') as f:
        f.write(PLANTILLA.format(rotulo=g.get('rotulo', 'Gráfico'), n=g['n'], titulo=html.escape(g['titulo']), titulo_corto=html.escape(corto[:60]),
                                 capitulo=html.escape(g['capitulo']), sub=html.escape(g['sub']),
                                 fuente=html.escape(g['fuente']), grafico=cuerpo, tabla=tabla))


def linea_px(nombre, x, y, i, sufijo='', dec=1, dash=None, marcas=None, grupo=None, mostrar=True):
    import plotly.graph_objects as go
    return go.Scatter(x=x, y=y, name=nombre, mode='lines+markers' if marcas is not None else 'lines',
                      line=dict(color=COLOR[i], width=2, dash=dash),
                      marker=dict(size=[8 if m else 0 for m in marcas] if marcas is not None else 0, color='#fcfcfb',
                                  line=dict(color=COLOR[i], width=2)),
                      legendgroup=grupo or nombre, showlegend=mostrar, connectgaps=False,
                      hovertemplate='%{y:.' + str(dec) + 'f}' + sufijo + '<extra>' + nombre + '</extra>')


def interactivos_y_tablas():
    import plotly.graph_objects as go
    # 1
    x, joven, hogar, med = datos_1()
    cab = ['Año', 'Perceptor mediano de 18 a 35 años', 'Hogar mediano', 'Tipo de dato']
    filas = [[a, j, h, 'medido' if m else 'interpolado'] for a, j, h, m in zip(x, joven, hogar, med)]
    exportar(G[1], cab, filas)
    excel(G[1], cab, filas, eje_y='Años de renta disponible', n_series=2)
    f = go.Figure([linea_px(cab[1], x, joven, 0, ' años', marcas=med), linea_px(cab[2], x, hogar, 4, ' años', marcas=med)])
    f.update_layout(hovermode='x unified', yaxis=dict(title='Años de renta disponible', range=[0, 20]))
    html_pagina(G[1], f, cab, filas)
    # 2
    x, s, med = datos_2()
    cab = ['Año', 'Perceptor mediano de 18 a 35 años', 'Perceptor mediano de 55 a 64 años', 'Perceptor mediano de 65 a 74 años', 'Tipo de dato']
    filas = [[a, s[0][k], s[1][k], s[2][k], 'medido' if med[k] else 'interpolado'] for k, a in enumerate(x)]
    exportar(G[2], cab, filas)
    excel(G[2], cab, filas, eje_y='Años de renta disponible', n_series=3)
    f = go.Figure([linea_px(cab[i + 1], x, s[i], i, ' años', marcas=med) for i in range(3)])
    f.update_layout(hovermode='x unified', yaxis=dict(title='Años de renta disponible', range=[0, 24]))
    html_pagina(G[2], f, cab, filas)
    # 3
    x, constr, hog = datos_3()
    cab = ['Año', 'Crédito a los hogares para adquisición de vivienda (% del PIB)',
           'Crédito con garantía inmobiliaria a la construcción y las actividades inmobiliarias (% del PIB)']
    filas = [[a, h, c] for a, h, c in zip(x, hog, constr)]
    exportar(G[3], cab, filas)
    excel(G[3], cab, filas, eje_y='% del PIB')
    f = go.Figure([linea_px('Crédito a los hogares para vivienda', x, hog, 0, ' %'),
                   linea_px('Crédito a la construcción y las actividades inmobiliarias', x, constr, 1, ' %')])
    f.update_layout(hovermode='x unified', yaxis=dict(title='% del PIB', range=[0, 70], ticksuffix=' %'))
    html_pagina(G[3], f, cab, filas)
    # 4
    r, cats = datos_4()
    cab = ['Periodo'] + [n for _, n in cats] + ['Tasa anual de emancipación (%)', 'Emancipaciones observadas (n)']
    filas = [[a['panel']] + [float(a[c]) for c, _ in cats] + [float(a['tasa_emancipacion_anual_pct']), int(a['n_emancipaciones'])] for a in r]
    exportar(G[4], cab, filas)
    excel(G[4], cab, filas, tipo='barra', eje_y='% de quienes se emancipan', n_series=4, formato='0%')
    f = go.Figure()
    ejes = [f"{a['panel']} (tasa anual: {es(float(a['tasa_emancipacion_anual_pct']))} %)" for a in r]
    for i, (c, n) in enumerate(cats):
        v = [float(a[c]) for a in r]
        f.add_bar(y=ejes, x=v, name=n, orientation='h', marker=dict(color=COLOR[i], line=dict(color='#fcfcfb', width=2)),
                  text=[f'{es(t, 0)} %' if t >= 8 else '' for t in v], textposition='inside', insidetextanchor='middle',
                  hovertemplate='%{x:.1f} %<extra>' + n + '</extra>')
    f.update_layout(barmode='stack', yaxis=dict(autorange='reversed'), xaxis=dict(range=[0, 100], ticksuffix=' %'))
    html_pagina(G[4], f, cab, filas)
    # 5
    x, d, paises = datos_5()
    cab = ['Año'] + [n for _, n in paises]
    filas = [[a] + [d[k][j] for k, _ in paises] for j, a in enumerate(x)]
    exportar(G[5], cab, filas)
    excel(G[5], cab, filas, eje_y='Índice (2015 = 100)', formato='0')
    f = go.Figure([linea_px(n, x, d[k], i, '', dec=1) for i, (k, n) in enumerate(paises)])
    f.update_layout(hovermode='x unified', yaxis=dict(title='Índice (2015 = 100)', range=[0, 230]))
    html_pagina(G[5], f, cab, filas)
    # 6
    x, viv, hog, fuente = datos_6()
    cab = ['Año', 'Viviendas terminadas (miles)', 'Hogares nuevos (miles)', 'Fuente del dato de hogares']
    filas = [[a, v, h, s] for a, v, h, s in zip(x, viv, hog, fuente)]
    exportar(G[6], cab, filas)
    excel(G[6], cab, filas, eje_y='Miles al año', n_series=2, formato='0')
    c = x.index(2001)
    f = go.Figure([linea_px('Viviendas terminadas (libres y protegidas)', x, viv, 0, ' mil'),
                   linea_px('Hogares nuevos (promedio entre censos, 1971-2001)', x[:c + 1], hog[:c + 1], 1, ' mil', dash='dash'),
                   linea_px('Hogares nuevos (EPA y Estadística Continua de Población)', x[c + 1:], hog[c + 1:], 1, ' mil')])
    f.update_layout(hovermode='x unified', yaxis=dict(title='Miles al año', range=[0, 720]))
    html_pagina(G[6], f, cab, filas)
    shutil.copyfile(PLOTLY_JS, os.path.join(SALIDA, 'interactivas', 'plotly.min.js'))


if __name__ == '__main__':
    for fn in (g1, g2, g3, g4, g5, g6):
        for modo in ('bn', 'color'):
            fn(modo)
    interactivos_y_tablas()
    print('Hecho:', SALIDA)
