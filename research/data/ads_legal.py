# Benchmarks Google Ads por industria (CPC/CPL USD). Fuentes en cada fila.
ADS = [
 # industria, naics2, cpc, cpl, nota, fuente
 ("Promedio todas las industrias",None,5.26,70.11,"WordStream 2025 (16k+ campañas)","https://www.wordstream.com/blog/2025-google-ads-benchmarks"),
 ("Legal / abogados","54",9.87,131.63,"CPC 2026; CPL más alto","https://www.wordstream.com/blog/2026-google-ads-benchmarks"),
 ("Dental","62",8.00,None,"CPC 2026; conv. 9.08%","https://www.wordstream.com/blog/2026-google-ads-benchmarks"),
 ("Médicos y cirujanos","62",5.00,56.83,"WordStream 2025","https://www.wordstream.com/blog/2025-google-ads-benchmarks"),
 ("Techos (roofing)","23",10.70,228.15,"LocaliQ home services 2025","https://localiq.com/blog/home-services-search-advertising-benchmarks/"),
 ("Plomería","23",None,76.40,"LocaliQ home services 2025","https://localiq.com/blog/home-services-search-advertising-benchmarks/"),
 ("HVAC","23",None,84.92,"LocaliQ home services 2025","https://localiq.com/blog/home-services-search-advertising-benchmarks/"),
 ("Construcción","23",5.31,None,"LocaliQ home services 2025","https://localiq.com/blog/home-services-search-advertising-benchmarks/"),
 ("Automotriz (reparación)","81",None,28.50,"WordStream 2025","https://www.wordstream.com/blog/2025-google-ads-benchmarks"),
 ("Restaurantes","72",2.05,30.27,"WordStream 2025","https://www.wordstream.com/blog/2025-google-ads-benchmarks"),
 ("Business services (B2B)","42",None,103.54,"WordStream 2025","https://www.wordstream.com/blog/2025-google-ads-benchmarks"),
 ("Real estate","53",None,100.48,"WordStream 2025","https://www.wordstream.com/blog/2025-google-ads-benchmarks"),
 ("'dentist miami'","62",9.81,105.00,"Herramienta de agencia; orientativo","https://ppcchief.com/google-ads-cost/dental/miami"),
 ("Accidentes / PI Miami (inglés)","54",70.00,300.00,"Rango CPC $70–250+; CPL $300–1,000","https://custom.legal/practice-areas/personal-injury-law-firm-marketing/cost-per-click-benchmarks-for-personal-injury/"),
 ("'abogado de accidentes' FL (español)","54",45.00,None,"CPC $45–85; 30–60% más barato que inglés","https://www.greatmarketing.ai/blog/spanish-speaking-personal-injury-lawyer-marketing"),
]
PRECIOS = [
 # servicio, min, max, unidad, fuente
 ("Diseño web pyme (Miami)",2500,15000,"proyecto","https://tamer.marketing/blog/web-design-cost-miami/"),
 ("Diseño web freelance / precio fijo",500,2000,"proyecto","https://startupstarz.com/how-much-does-a-website-cost-for-a-small-business-in-miami-2026-pricing-guide/"),
 ("SEO local pyme (Miami)",750,3000,"mes","https://tamer.marketing/blog/seo-cost-miami/"),
 ("Gestión redes sociales pyme (Miami)",1000,3000,"mes","https://onceonceagency.com/social-media-management-cost-miami/"),
 ("Gestión Google Ads (fee)",500,2500,"mes (10–20% del gasto, mín. ~$500)","https://www.2pointagency.com/glossary/pricing-for-ppc-management-services-in-miami/"),
 ("Presupuesto Google Ads pyme local",1000,2500,"mes (inversión del cliente)","https://www.americaneagle.com/insights/blog/post/how-much-does-it-cost-to-advertise-on-google-ads-in-2025"),
]
LEGAL = [
 # tema, detalle, implicación comercial, fuente
 ("Sunbiz – tipos de entidad","Florida Profit Corp, Not For Profit, LLC, LP/LLLP, Foreign, Fictitious Name (DBA, $50, 5 años, F.S. 865.09)","'Inc/Corp/LLC' en el nombre no confirma estatus: validar siempre en Sunbiz","https://dos.fl.gov/sunbiz/start-business/efile/fl-fictitious-name-registration/"),
 ("Sunbiz – estados","Active / Inactive (Admin Dissolution for Annual Report, Voluntary Dissolution, Revoked, Merged)","Solo prospectar entidades Active; Inactive recientes = empresas desorganizadas (posible servicio)","https://search.sunbiz.org/"),
 ("Sunbiz – Annual Report","Vence 1 de mayo; LLC $138.75; recargo $400 (Corp/LLC/LP), no condonable","Pico de disoluciones administrativas en la 4.ª semana de septiembre","https://dos.fl.gov/sunbiz/manage-business/efile/annual-report/"),
 ("Sunbiz – datos públicos","Document No., FEI/EIN, fecha, estado, dirección, registered agent, officers, historial","Nombre del officer = decisor para contacto B2B","https://dos.fl.gov/sunbiz/search/"),
 ("Sunbiz – descargas masivas","SFTP sftp.floridados.gov: trimestral (todas las activas) y diario (nuevas altas), ancho fijo","Fuente para lead-gen automatizado de empresas nuevas (siguiente fase)","https://dos.fl.gov/sunbiz/other-services/data-downloads/"),
 ("DBPR – licencias","Contratistas (CILB), hoteles y restaurantes, real estate, cosmetología, CPA, etc. 1.6M+ licenciatarios","Cruzar licencia activa = negocio operativo y regulado","https://www2.myfloridalicense.com/services-requiring-a-dbpr-license/"),
 ("BTR Miami-Dade","Por local y clasificación; ciudad + condado; año fiscal 1 oct–30 sep","Dataset abierto 'Local Business Tax – View' para prospección por dirección","https://www.mdctaxcollector.gov/services/local-business-tax-receipt"),
 ("BTR Broward","Obligatorio; renovación 1 jul–30 sep; tarifa por tipo y empleados","Dataset 'Business Tax Records' en Broward GeoHub","https://browardtax.org/business-tax-receipt/"),
 ("BTR/CU Fort Lauderdale","BTR municipal obligatorio antes de operar (Sec. 15-28)","Validar negocio operativo","https://www.fortlauderdale.gov/Government/Departments/Community-Services/Business-Tax"),
 ("BTR/CU Miami Beach","Certificate of Use + inspección bomberos + BTR","Validar negocio operativo","https://www.miamibeachfl.gov/city-hall/finance/business-tax-receipts-btr/"),
 ("BTR/CU Medley","Sin CU no hay BTR; CU municipal exige CU del condado","Validar negocio operativo","https://www.townofmedley.com/local-business-tax-receipts"),
 ("FTSA (F.S. 501.059) + HB 761 (2023)","Consentimiento escrito para llamadas/SMS de venta con sistema automatizado; $500–$1,500 por violación; STOP + 15 días antes de demandar","NO usar marcadores/SMS masivos; llamadas manuales 1 a 1","https://www.flsenate.gov/Committees/BillSummaries/2023/html/761"),
 ("Florida Telemarketing Act (501.601–626)","Licencia FDACS + fianza $50k salvo exención (B2B); 8am–8pm; máx. 3 llamadas/24h","Venta B2B exenta de licencia, no de horarios ni DNC","https://www.fdacs.gov/Consumer-Resources/Consumer-Rights-and-Responsibilities/Telemarketing"),
 ("TCPA / DNC","PEWC para autodialer a celulares; DNC nacional y de Florida","Depurar móviles contra DNC antes de llamar","https://www.fdacs.gov/Business-Services/Florida-Do-Not-Call"),
 ("CAN-SPAM","Sin excepción B2B: remitente veraz, asunto no engañoso, dirección física, opt-out; hasta $53,088 por email","Canal principal recomendado: email B2B 1 a 1 que cumpla","https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business"),
 ("Florida Digital Bill of Rights","Solo controllers con +$1,000M de ingresos + criterio Big Tech","No aplica a la agencia ni a los prospectos pyme","https://privacylawmap.com/states/florida"),
 ("ADA web (Title III)","Florida: 1,823 demandas ADA Title III en 2025 (2.º de EE.UU.); ~950 digitales (24%)","Argumento de venta: sitio accesible (WCAG 2.2 AA) reduce riesgo legal","https://www.adatitleiii.com/2026/02/ada-title-iii-federal-lawsuit-filings-fall-slightly-to-8667-in-2025/"),
]
