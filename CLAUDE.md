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
- La página no lleva meta noindex, porque el workflow de producción aborta si lo encuentra. En su lugar usa `X-Robots-Tag` en `public/funnel26/.htaccess`.
- Acceso con clave: `index.php` (plantilla `acceso.php`) valida contra el hash bcrypt de `acceso.json` o del secreto `FUNNEL26_HASH`. La app va incrustada en el PHP, así que no hay ningún archivo estático con datos. El workflow de producción falla si los datos salen sin sesión.
- Filtros: condado, ciudad (chips con conteo o clic en el mapa), nicho, industria, estado web, prioridad y búsqueda, más el filtrado cruzado desde las donas.
- Mapa: SVG propio con los condados de `mapa.js` (generado por `research/scripts/mapa_funnel26.mjs` con us-atlas, en el corredor urbano) y las ciudades de `data/coordenadas.py`. Debajo va la ficha de la ciudad elegida. Si se añade una ciudad nueva, hay que agregar sus coordenadas.
- Nicho comercial: `research/scripts/nichos.py` (40 nichos). Si la fila trae su nicho explícito se respeta; si no, se aplican las reglas en orden. Los lotes nuevos van en `data/amp_*.json`, con el campo `nicho`.
- Publicar: PR a `main` de FOCO → deploy FTP automático. Tras un squash merge, la rama se rehace desde `origin/main` antes de seguir.

## Estado
- v1 (2026-09): 95 prospectos, 4 tablas dinámicas, matriz de oportunidad. Rama `claude/miami-market-research-pun0i6`.
- v1.2 (2026-09): contactos de 92/95 empresas (`data/contactos.json`), reclasificación de estado web, 6 analizadores tipo dona y registro BTR de Miami-Dade en vivo (sin probar desde el sandbox).
- Regla de privacidad: solo datos comerciales públicos; se omiten direcciones residenciales, celulares y correos personales.
- v2 (2026-09-24): PUBLICADO en focoworking.com/funnel26/ (focoworking/FOCO#16 fusionado, deploy verde). 192 prospectos, 15 industrias, 22 ciudades. Acceso con clave vía PHP (hash en producto/funnel26/acceso.json; la clave en claro NO se versiona, se entregó por chat).
- v2.1 (2026-09-24): filtro por ciudad publicado (focoworking/FOCO#17).
- v3 (2026-09-26): mapa con ficha por ciudad, nichos y 285 prospectos en 29 ciudades (focoworking/FOCO#18). Nota: el tope de 200 WebSearch por sesión se comparte entre todos los subagentes.
- Pendiente: validar en Sunbiz los 38 prospectos A; cubrir Design District, Downtown, Little Haiti y fábricas de confección; verificar los 18 "No verificado"; reducir el peso de Hialeah (48/285) y cubrir Miami Lakes, Cutler Bay, Lauderhill y Deerfield, además de limpieza, concesionarios y limusinas; guardar las etapas del pipeline en el servidor; confirmar en producción la consulta BTR en vivo; buscar la capa BTR de Broward.
