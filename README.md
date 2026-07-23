# Datos y gráficas — monografía sobre la burbuja inmobiliaria

Repositorio de ciencia abierta con los datos, tablas, scripts y gráficas que acompañan a la monografía.

## Estructura

- `anexo/` — textos del anexo estadístico: `comentarios_graficas.md` (comentario de cada gráfica) y `justificacion_propiedad_intelectual.md` (nota jurídica para la editorial).

- `tablas/` — una tabla CSV por gráfica, con [FUENTES.md](tablas/FUENTES.md) como memoria completa de fuentes (serie, definición, URL, fecha de descarga y advertencias metodológicas de cada dato).
- `datos/brutos/` — ficheros originales tal como se descargaron (BdE, INE, Eurostat, OCDE, BIS, Reserva Federal, MIVAU, BOE, Prados de la Escosura).
- `datos/procesados/` — series limpias intermedias.
- `graficas/color/` — figuras en color (PNG 300 ppp + SVG) para difusión.
- `graficas/bn/` — figuras en blanco y negro (trazos y tramas, PNG 300 ppp + SVG) para la edición impresa.
- `graficas/interactivas/` — versiones interactivas (HTML + Plotly): el valor exacto aparece al pasar el cursor; `index.html` es la galería. Funcionan abriendo el fichero en el navegador o publicadas en GitHub Pages.
- `graficas/scripts/` — scripts reproducibles: `generar_graficas.py` (figuras estáticas), `generar_interactivas.py` (versiones HTML), `estilo.py` (sistema de estilo), `g5_ecv_transferencia_alquiler.py` (procesado de microdatos ECV) y `g1bis_retropolacion_1971.py` (retropolación 1971-1986 de la Gráfica 1bis).

> Nota: la Gráfica 1bis (serie extendida 1971-2025) aún no tiene comentario en `anexo/comentarios_graficas.md`; el resto de gráficas sí.

## Reproducibilidad

```
python3 graficas/scripts/g5_ecv_transferencia_alquiler.py   # requiere microdatos ECV 2025 en datos/brutos/
python3 graficas/scripts/generar_graficas.py                # regenera las figuras estáticas desde tablas/
python3 graficas/scripts/generar_interactivas.py            # regenera las versiones interactivas (HTML)
```

## Publicación

- **GitHub Pages** (interactivas): en el repositorio, Settings → Pages → Deploy from branch, carpeta raíz.
  Las gráficas quedan accesibles en `https://<usuario>.github.io/<repo>/graficas/interactivas/`.
- **DOI citable (Zenodo)**: activar el repositorio en https://zenodo.org/account/settings/github/ y crear
  una *release* en GitHub; Zenodo archiva la versión y asigna un DOI para citar en la monografía.

Fuentes principales: Banco de España, INE, Ministerio de Vivienda y Agenda Urbana, BOE, Eurostat, OCDE, BIS, Reserva Federal de EE.UU. y las cuentas nacionales históricas de L. Prados de la Escosura. Todas las gráficas indican su fuente al pie; el detalle serie a serie está en `tablas/FUENTES.md`.
