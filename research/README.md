# Investigación de mercado: oportunidad digital en Miami-Dade y Broward

**Entregable:** [`Miami_Oportunidad_Digital.xlsx`](Miami_Oportunidad_Digital.xlsx), con corte a septiembre de 2026.

## Hojas

| Hoja | Contenido |
|---|---|
| Resumen | Indicadores calculados con fórmulas, datos de mercado y 7 hallazgos |
| Prospectos | 95 empresas: municipio, industria NAICS, forma legal, estado web, redes, evidencia y fuente. Incluye puntaje y prioridad |
| TD_Area_Web | Tabla dinámica: condado × municipio × estado web |
| TD_Industria_Web | Tabla dinámica: industria × estado web (filtro por condado) |
| TD_Legal_Prioridad | Tabla dinámica: forma legal × prioridad (filtro por condado) |
| TD_Redes | Tabla dinámica: redes sociales × condado (filtro por industria) |
| Oportunidad_Industria | Brecha digital y valor potencial por industria. Tickets y CPL editables |
| Macro_Areas | Población, firmas y carácter económico de 14 áreas y 2 condados |
| Adopcion_Digital | Encuestas de adopción web y Ads, más formación de empresas en Florida |
| Google_Ads | CPC y CPL por industria y keywords de Miami, precios de agencias en Miami |
| Legal_Cumplimiento | Sunbiz, DBPR, BTR, FTSA, TCPA, CAN-SPAM, ADA, portales de datos abiertos |
| Parametros | Pesos del puntaje, editables |
| Metodologia | Criterios, limitaciones y siguiente fase |

## Uso

1. Filtra `Prospectos` por **Prioridad = A**.
2. Antes de contactar, valida cada empresa en [Sunbiz](https://search.sunbiz.org/) y Google Maps. Registra el resultado en las columnas *Estado Sunbiz* y *Próximo paso*.
3. Después de editar los datos, actualiza las tablas dinámicas: clic derecho → *Actualizar* / *Refresh*.

## Regenerar el archivo

Requiere `openpyxl` y LibreOffice Calc, que se usa para las tablas dinámicas nativas.

```bash
python3 research/scripts/build.py
```

Los datos están en `research/data/` (CSV de prospectos y módulos `macro.py` y `ads_legal.py`). Cada cifra lleva su fuente, y "estimado" indica que no se verificó en la fuente primaria.

## Limitaciones

- El estado web de cada empresa se dedujo de resultados de búsqueda, no de visitas a los sitios.
- La forma legal se tomó del sufijo del nombre (Inc, LLC, Corp), salvo cuando se indica Sunbiz.
- 50 de los 95 registros siguen como "No verificado".
