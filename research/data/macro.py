# Datos macro por área. Fuente por fila. "estimado" = no verificado en fuente primaria.
AREAS = [
 # area, condado, poblacion, anio_pob, firmas_empleadoras_2022, caracter, sectores_clave, verificado, fuente
 ("Miami (ciudad)","Miami-Dade",455924,"2023",17986,"Finanzas, servicios profesionales, turismo, hub LatAm","54, 52, 72, 42","Sí","https://www.census.gov/quickfacts/fact/table/miamicityflorida/PST045224"),
 ("Hialeah","Miami-Dade",226000,"2024",None,"Manufactura ligera, salud, construcción, transporte","31-33, 62, 23, 48-49","Estimado","https://datausa.io/profile/geo/hialeah-fl/"),
 ("Doral","Miami-Dade",83625,"2024",5300,"Logística, comercio exterior, freight forwarders (junto a MIA)","48-49, 42, 54, 44-45","Estimado","https://www.census.gov/quickfacts/fact/table/doralcityflorida/PST045225"),
 ("Medley","Miami-Dade",1056,"2020",1800,"Industrial pura: cemento, canteras, +350 almacenes; población diurna +60k","31-33, 42, 48-49, 23","Sí (municipio)","https://www.townofmedley.com/about-us"),
 ("Miami Beach","Miami-Dade",82031,"2024",4174,"Hotelería, restaurantes, vida nocturna, real estate","72, 53, 71, 81","Sí","https://census.gov/quickfacts/fact/table/miamibeachcityflorida/POP060210"),
 ("Coral Gables","Miami-Dade",48353,"2023",5120,"Sedes multinacionales LatAm, legal, profesional","54, 52, 55, 62","Sí","https://www.census.gov/quickfacts/fact/table/coralgablescityflorida/PST045224"),
 ("Kendall","Miami-Dade",80241,"2020",None,"Retail (Dadeland), salud (Baptist), servicios","44-45, 62, 81, 61","Sí (población)","https://en.wikipedia.org/wiki/Kendall,_Florida"),
 ("Miami Gardens","Miami-Dade",111000,"2024",None,"Residencial, retail, Hard Rock Stadium","44-45, 71, 81","Estimado","https://www.census.gov/quickfacts/fact/table/miamigardenscityflorida/POP060210"),
 ("Homestead","Miami-Dade",82807,"2024",1212,"Agricultura/viveros, base aérea, puerta a Cayos","11, 44-45, 72, 23","Sí","https://census.gov/quickfacts/fact/table/homesteadcityflorida/PST120223"),
 ("Fort Lauderdale","Broward",184255,"2023",10690,"Industria náutica (111k empleos Broward), turismo, finanzas","48-49, 72, 52, 81","Sí","https://www.census.gov/quickfacts/fact/table/fortlauderdalecityflorida/PST045225"),
 ("Hollywood","Broward",152650,"2022",5007,"Turismo de playa, retail, servicios","72, 44-45, 81","Sí","https://www.census.gov/quickfacts/fact/table/hollywoodcityflorida/PST045222"),
 ("Pembroke Pines","Broward",179326,"2024",4128,"Residencial, retail, salud","44-45, 62, 81","Sí","https://www.census.gov/quickfacts/fact/table/pembrokepinescityflorida/SBO010222"),
 ("Sunrise","Broward",100128,"2024",2706,"Retail (Sawgrass Mills), oficinas corporativas","44-45, 55, 54","Sí","https://www.census.gov/quickfacts/fact/table/sunrisecityflorida/PST045222"),
 ("Plantation","Broward",96000,"2024",None,"Oficinas, salud, retail","54, 62, 44-45","Estimado","https://www.census.gov/quickfacts/fact/table/plantationcityflorida/PST045225"),
]
COUNTIES = [
 # condado, poblacion, establecimientos, anio, est_20_99, est_100_499, fuente
 ("Miami-Dade",2738356,98394,"2023",12000,2200,"https://www.miamidadematters.org/indicators/index/view?indicatorId=6371&localeId=414"),
 ("Broward",2000000,67274,"2022",8200,1500,"https://www.census.gov/quickfacts/fact/table/browardcountyflorida/PST045224"),
]
DIGITAL = [
 ("Pequeñas empresas EE.UU. sin sitio web","17%","2025","Clutch","https://clutch.co/press-releases/smb-websites-2025"),
 ("Sin sitio web (Top Design Firms)","27%","2022","Top Design Firms","https://www.prnewswire.com/news-releases/27-of-small-businesses-still-dont-have-a-website-in-2022-301542302.html"),
 ("De las que no tienen web: creen que no la necesitan","34%","2025","Clutch","https://clutch.co/press-releases/smb-websites-2025"),
 ("Invierten en publicidad de búsqueda (año en curso)","45%","2026","LocaliQ","https://localiq.com/blog/small-business-marketing-trends-report-2026/"),
 ("Invierten en search con presupuesto < $1k/mes","30%","2026","LocaliQ","https://localiq.com/blog/small-business-marketing-trends-report-2026/"),
 ("Pymes que usan IA generativa","58%","2025","US Chamber","https://www.uschamber.com/technology/artificial-intelligence/u-s-chambers-latest-empowering-small-business-report-shows-majority-of-businesses-in-all-50-states-are-embracing-ai"),
 ("Solicitudes de negocio Florida (Census BFS)","~634,000","2024","Census BFS / Business Observer","https://www.businessobserverfl.com/news/2025/may/19/florida-new-business-formations/"),
 ("Solicitudes por 10k hab. Miami-Dade (6.º EE.UU.)","532","2024","Census BFS / Business Observer","https://www.businessobserverfl.com/news/2025/may/19/florida-new-business-formations/"),
 ("Solicitudes por 10k hab. Broward (11.º EE.UU.)","418","2024","Census BFS / Business Observer","https://www.businessobserverfl.com/news/2025/may/19/florida-new-business-formations/"),
 ("Pequeñas empresas en Florida (99.8% del total)","3.5 M","2025","SBA Office of Advocacy","https://advocacy.sba.gov/wp-content/uploads/2025/06/Florida_2025-State-Profile.pdf"),
 ("Entidades registradas en Sunbiz","+3.5 M","2026","Florida Division of Corporations","https://dos.fl.gov/sunbiz/"),
 ("Nuevas entidades Sunbiz 2025 (≈1,800/día)","670,459 (estimado)","2025","Fuente secundaria; verificar en Yearly Statistics","https://dos.fl.gov/sunbiz/about-us/yearly-statistics/"),
 ("Demandas ADA Title III en Florida (2.º estado)","1,823","2025","Seyfarth ADA Title III","https://www.adatitleiii.com/2026/02/ada-title-iii-federal-lawsuit-filings-fall-slightly-to-8667-in-2025/"),
 ("Demandas digitales ADA Florida (fed.+estatal)","950 (24% EE.UU.)","2025","UsableNet","https://blog.usablenet.com/ada-web-lawsuit-trends-2026"),
]
