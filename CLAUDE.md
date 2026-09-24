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

## Estado
- v1 (2026-09): 95 prospectos, 4 tablas dinámicas, matriz de oportunidad. Rama `claude/miami-market-research-pun0i6`.
- Pendiente: validar en Sunbiz los 13 prospectos A, verificar los 50 "No verificado", ampliar la cobertura de Miami Beach, Wynwood, salud y restaurantes, e integrar los datasets BTR y el SFTP de Sunbiz.
