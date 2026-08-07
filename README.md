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
- `graficas/scripts/` — scripts reproducibles: `generar_graficas.py` (figuras estáticas G1-G10), `generar_interactivas.py` (versiones HTML G1-G10), `estilo.py` (sistema de estilo), `g5_ecv_transferencia_alquiler.py` (procesado de microdatos ECV), `g1bis_retropolacion_1971.py` (retropolación 1971-1986 de la Gráfica 1bis), `n_series_boletin_mitms.py`, `n4_n5_costes_visados.py` y `n4b_indices_materiales.py` (extracción de las series N desde el Boletín estadístico del MITMS), `generar_graficas_n.py` y `generar_interactivas_n.py` (figuras N1-N6 y N4b).

Además de las gráficas principales (G1-G10 y variantes), el repositorio incluye seis series complementarias (N1-N6): vivienda protegida del franquismo (anuarios INE 1958-1975) y plazos normativos del régimen de protección, VPO por tipo de promotor, destinos de los Patrimonios Municipales de Suelo (Tribunal de Cuentas, 2004), coste de construcción frente a precio de venta (1992-2025), precio del suelo urbano (2004-2025) y viviendas iniciadas por décadas, libres frente a protegidas (1976-2025).

> Nota: la Gráfica 1bis y las series N1-N6 aún no tienen comentario en `anexo/comentarios_graficas.md`; el resto de gráficas sí.

## Reproducibilidad

```
python3 graficas/scripts/g5_ecv_transferencia_alquiler.py   # requiere microdatos ECV 2025 en datos/brutos/
python3 graficas/scripts/generar_graficas.py                # regenera las figuras estáticas desde tablas/
python3 graficas/scripts/generar_interactivas.py            # regenera las versiones interactivas (HTML)
python3 graficas/scripts/n_series_boletin_mitms.py          # reconstruye las tablas N2, N5 y N6 desde datos/brutos/
python3 graficas/scripts/n4_n5_costes_visados.py            # reconstruye la tabla N4 (visados y PEM)
python3 graficas/scripts/generar_graficas_n.py              # regenera las figuras estáticas N1-N6
python3 graficas/scripts/generar_interactivas_n.py          # regenera las interactivas N1-N6 y la galería
```

## Licencia

Licencia dual, según el tipo de contenido:

- **Código** (`graficas/scripts/*.py`): [Licencia MIT](LICENSE).
- **Datos, tablas, gráficas y documentación** de elaboración propia: [Creative Commons Atribución 4.0 Internacional (CC BY 4.0)](LICENSE-DATA).

Los ficheros originales de terceros en `datos/brutos/` (Eurostat, OCDE, BIS, INE, Banco de España, MIVAU, BOE, Reserva Federal, Prados de la Escosura) siguen sujetos a las condiciones de sus proveedores respectivos, con independencia de lo anterior — véase `tablas/FUENTES.md` y `anexo/justificacion_propiedad_intelectual.md`.

> El titular de los derechos figura en LICENSE/LICENSE-DATA como «los autores del repositorio»; sustituidlo por los nombres completos que prefiráis antes de publicar.

## Publicación

- **GitHub Pages** (interactivas): en el repositorio, Settings → Pages → Deploy from branch, carpeta raíz.
  Las gráficas quedan accesibles en `https://<usuario>.github.io/<repo>/graficas/interactivas/`.
- **DOI citable (Zenodo)**: activar el repositorio en https://zenodo.org/account/settings/github/ y crear
  una *release* en GitHub; Zenodo archiva la versión y asigna un DOI para citar en la monografía.

Fuentes principales: Banco de España, INE, Ministerio de Vivienda y Agenda Urbana, BOE, Eurostat, OCDE, BIS, Reserva Federal de EE.UU. y las cuentas nacionales históricas de L. Prados de la Escosura. Todas las gráficas indican su fuente al pie; el detalle serie a serie está en `tablas/FUENTES.md`.
