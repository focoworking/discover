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
- Barra superior (estilo archivado): bloque claro `#f5f6f7`, tinta `#07080b`, que contrasta con el cuerpo negro. Lleva isotipo (3 barras `#FEFD55` sobre `#0c2539`), FUNNEL’26 (Archivo 800) con el subtítulo «Estudio de Mercado» (mono, versalitas), Menú, Mi cuenta (Perfil, Consultas PDF · historial, Suscripciones, Salir) y «Obtén tu potencial» → focoworking.com/discover (negro con texto amarillo). Debajo, en una segunda fila sobria, las pestañas de sección como antes (píldora deslizante). Línea azul de progreso.
- Navegación: Menú a pantalla completa (botón magnético o tecla M) que se abre en círculo desde el botón, con secciones numeradas en tipografía grande (Archivo 600, tracking −0.035em), letras que ruedan al hover, las demás atenuadas a .28 y vista previa con cifra viva y número en contorno. Curva `cubic-bezier(.76,0,.24,1)`. Respeta reduced-motion. Referencia pedida: zalak-patel.com (no accesible desde el sandbox).
- Publicar: PR a `main` de FOCO → deploy FTP automático. Tras un squash merge, la rama se rehace desde `origin/main` antes de seguir.

## Estado
- v1 (2026-09): 95 prospectos, 4 tablas dinámicas, matriz de oportunidad. Rama `claude/miami-market-research-pun0i6`.
- v1.2 (2026-09): contactos de 92/95 empresas (`data/contactos.json`), reclasificación de estado web, 6 analizadores tipo dona y registro BTR de Miami-Dade en vivo (sin probar desde el sandbox).
- Regla de privacidad: solo datos comerciales públicos; se omiten direcciones residenciales, celulares y correos personales.
- v2 (2026-09-24): PUBLICADO en focoworking.com/funnel26/ (focoworking/FOCO#16 fusionado, deploy verde). 192 prospectos, 15 industrias, 22 ciudades. Acceso con clave vía PHP (hash en producto/funnel26/acceso.json; la clave en claro NO se versiona, se entregó por chat).
- v2.1 (2026-09-24): filtro por ciudad publicado (focoworking/FOCO#17).
- v3 (2026-09-26): mapa con ficha por ciudad, nichos y 285 prospectos en 29 ciudades (focoworking/FOCO#18). Nota: el tope de 200 WebSearch por sesión se comparte entre todos los subagentes.
- v3 (2026-09-25): mapa del Sur de Florida con ficha por ciudad, 40 nichos (`nichos.py`) y 285 prospectos (focoworking/FOCO#18).
- v4 (2026-09-26): asistente virtual. Es `producto/funnel26/asistente.php`, que se publica como `api.php`, sobre el SDK PHP de Anthropic (claude-opus-5, con web_search/web_fetch).
  - Herramientas: consultar_prospectos, resumen_mercado, agregar_prospecto, actualizar_prospecto y aplicar_filtros.
  - Toda escritura exige una fuente vista en la misma consulta. Las altas se marcan con `origen: asistente` y `sunbiz: Pendiente`, y hay registro y deshacer.
  - Los datos vivos van en `vivos.php`, fuera de la carpeta pública (`../f26-datos`), y el tablero los suma a `datos.js` al cargar.
  - Acceso: exige sesión, un token CSRF (meta `f26-csrf`) y un tope de 40 preguntas/hora. Todo `_*` está bloqueado.
  - Despliegue: `composer install -d producto/funnel26` → `empaquetar-sdk.php` → `_lib.phar` (un solo archivo: el FTP de GoDaddy cortó la conexión subiendo ~2.800 archivos). `_config.php` se genera desde el secreto **ANTHROPIC_API_KEY** (entorno production); sin él, el asistente queda desactivado.
  - `export_funnel26.py` exporta ahora `parametros` (pesos del puntaje) para que el asistente puntúe igual que el Excel.
  - Prueba local: `php -S` + un mock de la API con `ANTHROPIC_BASE_URL`.
- v4.1 (2026-09-26): menú dinámico (focoworking/FOCO#21).
- v4.2 (2026-09-26): barra superior clara + Mi cuenta. Las consultas al asistente se guardan en `vivos.php` (`consultas`, las últimas 200) y se exportan a PDF (focoworking/FOCO#22).
- v4.3 (2026-09-26): pestañas de sección recuperadas en la barra (focoworking/FOCO#23).
- v4.4 (2026-09-26): el tablero arranca sin esperar a `api.php` (antes un `await` de módulo lo dejaba vacío si el servidor tardaba). Los datos vivos se suman con un límite de 8 s, `flock` tiene un límite de 3 s y hay un aviso visible de errores JS (focoworking/FOCO#24). Regla: nunca bloquear el arranque del tablero con red.
- Pendiente: cuentas individuales y suscripciones reales si el tablero se vende a clientes; validar en Sunbiz los 38 prospectos A; cubrir Design District, Downtown, Little Haiti y fábricas de confección; verificar los 18 "No verificado"; reducir el peso de Hialeah (48/285) y cubrir Miami Lakes, Cutler Bay, Lauderhill y Deerfield, además de limpieza, concesionarios y limusinas; guardar las etapas del pipeline en el servidor; confirmar en producción la consulta BTR en vivo; buscar la capa BTR de Broward.
