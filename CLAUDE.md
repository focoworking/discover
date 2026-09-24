# Memoria del proyecto: discover

## Propósito
Investigación de mercado y prospección B2B de servicios digitales: web, SEO, redes y Google Ads para empresas medianas de Miami-Dade y Broward.

## Reglas de datos
- Todas las cifras llevan su fuente (URL). Si no están verificadas en la fuente primaria, se marcan como "estimado".
- Nunca inventar empresas. Toda fila de prospecto necesita su `fuente_url`.
- Solo fuentes públicas y gratuitas: Census, Sunbiz, DBPR, tax collectors, municipios y directorios públicos.
- Las columnas normalizadas de estado web son: Sin sitio web · Sitio obsoleto · Presencia desordenada · Tiene web (auditar) · No verificado.
- Prioridad A = puntaje ≥ 6 **y** señal de tamaño (≥ 10 empleados/camiones o fundada ≤ 2000). Si la empresa está Inactive en Sunbiz, se marca Descartada.

## Estilo de entregables (Excel)
- Fuente Arial. Tinta `#1F2937`, acento `#0E7C86`, gris `#6B7280`, líneas `#E5E7EB`. Sin cuadrícula. Estilo minimalista.
- Los inputs editables van en texto azul `#0000FF`, y las columnas que hay que completar llevan fondo `#FFF9DB`.
- Las tablas dinámicas deben ser nativas (DataPilot vía LibreOffice UNO, en `research/scripts/pivot_uno.py`).

## Entorno
- En la sesión cloud, la red bloquea Census, Sunbiz y los portales de los condados, tanto en bash como en WebFetch. Solo funciona WebSearch.
- LibreOffice Calc se instala con: `apt-get install --no-install-recommends libreoffice-calc`.

## Funnel 26 (sitio web)
- Es la página `/funnel26/` de focoworking.com. Vive en el repo `focoworking/FOCO`, en `producto/funnel26/`, y sigue el mismo patrón que Online Consulting (`producto/nivel`).
- Flujo de datos: Excel → `research/scripts/export_funnel26.py <FOCO>/producto/funnel26/datos.js` → `npm run pages` lo empaqueta en `public/funnel26/`.
- Estilo: el sistema «vidrio» de Nivel (fondo negro, tarjetas translúcidas, Archivo). El amarillo `#FEFD55` se reserva para la acción principal. Colores de estado web, validados para daltonismo (CVD): sin web `#c44429` · deficiente `#aa8d0e` · no verificado `#9a66ff` · tiene web `#0fa383`. La serie simple va en azul `#588cff`. Donas: categórica `#3987e5 #d95926 #199e70 #c98500 #d55181 #008300 #9085e9`, «Otras» `#5b5d63`, antigüedad en rampa ordinal `#9ec5f4 #6da7ec #3987e5 #256abf #184f95`.
- La página no lleva meta noindex, porque el workflow de producción aborta si lo encuentra. En su lugar usa `X-Robots-Tag` en `public/funnel26/.htaccess`. No tiene control de acceso: queda pendiente ponerle contraseña.

## Estado
- v1 (2026-09): 95 prospectos, 4 tablas dinámicas, matriz de oportunidad. Rama `claude/miami-market-research-pun0i6`.
- v1.1 (2026-09): Funnel 26 publicado en la rama `claude/miami-market-research-pun0i6` de FOCO. Todavía no está fusionado a main.
- v1.2 (2026-09): contactos de 92/95 empresas (`data/contactos.json`), reclasificación de estado web, 6 analizadores tipo dona y registro BTR de Miami-Dade en vivo (sin probar desde el sandbox).
- Regla de privacidad: solo datos comerciales públicos; se omiten direcciones residenciales, celulares y correos personales.
- Pendiente: validar en Sunbiz los 13 prospectos A, verificar los 50 "No verificado", ampliar la cobertura de Miami Beach, Wynwood, salud y restaurantes, e integrar los datasets BTR y el SFTP de Sunbiz.
