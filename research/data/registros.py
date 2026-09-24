# Registros oficiales que la página consulta en vivo (ArcGIS REST, desde el navegador).
# Endpoint y campos tomados del directorio REST y del diccionario de datos del condado:
#   https://gisweb.miamidade.gov/arcgis/rest/services/BusinessTracker/MapServer
#   https://gisweb.miamidade.gov/GISSelfServices/Data/HTML/LocalBusinessTax.htm
# No verificado desde el entorno de desarrollo (red bloqueada): la página degrada con aviso si falla.
REGISTROS = [
  {
    "id": "mdc-lbt",
    "nombre": "Miami-Dade Local Business Tax",
    "condado": "Miami-Dade",
    "url": "https://gisweb.miamidade.gov/arcgis/rest/services/BusinessTracker/MapServer/0",
    "clases": "https://gisweb.miamidade.gov/arcgis/rest/services/BusinessTracker/MapServer/2",
    "campoTipo": "CODE1",
    "campoId": "OBJECTID",
    "whereCiudad": "UPPER(MAILCITY) = '{ciudad}'",
    "portal": "https://opendata.miamidade.gov/datasets/local-business-tax-view",
    "municipios": ["Doral", "Hialeah", "Hialeah Gardens", "Homestead", "Kendall", "Medley", "Miami (ciudad)", "Miami Beach",
                   "Miami Shores", "North Miami", "North Miami Beach", "Miami Gardens", "Aventura", "Coral Gables"],
    "alias": {"Miami (ciudad)": "MIAMI", "Kendall": "MIAMI"},
  },
]
# Broward (Business Tax Records, geohub-bcgis.opendata.arcgis.com): capa REST no identificada aún.
