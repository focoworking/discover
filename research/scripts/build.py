"""Genera research/Miami_Oportunidad_Digital.xlsx (datos + fórmulas + tablas dinámicas nativas).
Uso: python3 research/scripts/build.py   (requiere openpyxl y LibreOffice Calc para las tablas dinámicas)"""
import csv, os, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data")); sys.path.insert(0, os.path.dirname(__file__))
from macro import AREAS, COUNTIES, DIGITAL
from ads_legal import ADS, PRECIOS, LEGAL

# ---- Estilo (minimalista: tinta + un acento) ----
INK, ACC, MUTED, LINE, SOFT = "1F2937", "0E7C86", "6B7280", "E5E7EB", "F3F7F8"
F = "Arial"
H = Font(name=F, bold=True, color="FFFFFF", size=10)
HF = PatternFill("solid", fgColor=INK)
B = Font(name=F, size=10, color=INK)
BB = Font(name=F, size=10, color=INK, bold=True)
T = Font(name=F, size=18, bold=True, color=INK)
ST = Font(name=F, size=10, color=MUTED, italic=True)
LINK = Font(name=F, size=10, color=ACC, underline="single")
INP = Font(name=F, size=10, color="0000FF")
KPI = Font(name=F, size=22, bold=True, color=ACC)
bd = Border(bottom=Side(style="thin", color=LINE))
WR = Alignment(wrap_text=True, vertical="top")

NAICS = {"11":"11 Agricultura/viveros","23":"23 Construcción y oficios","31":"31-33 Manufactura","32":"31-33 Manufactura",
 "33":"31-33 Manufactura","42":"42 Comercio mayorista","48":"48-49 Transporte y logística","53":"53 Inmobiliario/admin. propiedades",
 "54":"54 Servicios profesionales","62":"62 Salud","72":"72 Restaurantes/hotelería","81":"81 Servicios (auto, náutico, reparación)"}
ESTADO = {"Sin web detectada":"Sin sitio web","Sin sitio web":"Sin sitio web","Web posiblemente desactualizada":"Sitio obsoleto",
 "Sitio básico/obsoleto":"Sitio obsoleto","Tiene web":"Tiene web (auditar)","Presencia desordenada":"Presencia desordenada","No verificado":"No verificado"}
BARRIO = {"Allapattah (Miami)":("Miami (ciudad)","Allapattah"),"Little Havana (Miami)":("Miami (ciudad)","Little Havana")}

def legal(s):
    u = s.upper()
    if "NO VERIFICADO" in u and not any(k in u for k in ("LLC","INC","CORP")): return "No verificado"
    for k, v in (("LLC","LLC"),("CORP","Corp"),("INC","Inc")):
        if k in u: return v
    return "No verificado"

def size_signals(ev):
    m = re.search(r"~?(\d+)(?:-\d+)?\+?\s*(?:empleados|camiones)", ev)
    emp = int(m.group(1)) if m else None
    y = re.search(r"(?:Est\.|Desde|desde|Fundada|fundada|Inc\.|Incorporada|registrada \d\d/\d\d/)\s*(19\d\d|20\d\d)", ev)
    return emp, (int(y.group(1)) if y else None)

def sunbiz_default(p):
    if "Sunbiz" in p["forma_legal"]: return "Active"
    if "ADM DISS" in p["evidencia"]: return "Inactive"
    return "Pendiente"

def header(ws, row, cols, widths=None):
    for i, c in enumerate(cols, 1):
        x = ws.cell(row=row, column=i, value=c); x.font = H; x.fill = HF
        x.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 30
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[L(i)].width = w

def title(ws, t, sub):
    ws["A1"] = t; ws["A1"].font = T
    ws["A2"] = sub; ws["A2"].font = ST
    ws.sheet_view.showGridLines = False

def body(ws, r1, r2, c2, url_cols=()):
    for r in range(r1, r2 + 1):
        for c in range(1, c2 + 1):
            x = ws.cell(row=r, column=c)
            x.font = B; x.border = bd; x.alignment = WR
            if c in url_cols and isinstance(x.value, str) and x.value.startswith("http"):
                x.hyperlink = x.value; x.font = LINK

# ---- Prospectos ----
rows = []
for f in ("prospectos_miami_dade.csv", "prospectos_broward.csv"):
    with open(os.path.join(ROOT, "data", f), encoding="utf-8") as fh:
        rows += list(csv.DictReader(fh))

# ---- Contactos (dirección, teléfono, web, redes) y reclasificación con esa evidencia ----
import json
CONT = {c["id"]: c for c in json.load(open(os.path.join(ROOT, "data", "contactos.json"), encoding="utf-8"))}
SIN_WEB = ("web no encontrada", "web propia no encontrada", "web y redes no encontradas", "web/redes no encontradas")
SUNBIZ = {"P001": "Inactive", "P083": "Inactive", "P027": "Duplicado"}
def alerta(n):
    n = n.lower()
    for k, v in (("duplicado", "Duplicado"), ("posible cerrado", "Posible cerrado"), ("disuelta", "Disuelta en Sunbiz"),
                 ("no encontrado", "Sin datos de contacto"), ("dudosa", "Coincidencia dudosa")):
        if k in n: return v
    return ""
for i, p in enumerate(rows, 1):
    pid = f"P{i:03d}"
    c = CONT.get(pid, {})
    p["_c"] = c
    web, nota = c.get("web", ""), c.get("nota", "").lower()
    if web and ("wixsite" in web or "wordpress.com" in web):
        if p["estado_web"] in ("No verificado", "Sin sitio web", "Sin web detectada"): p["estado_web"] = "Sitio básico/obsoleto"
    elif web and p["estado_web"] == "No verificado":
        p["estado_web"] = "Tiene web"
    elif not web and p["estado_web"] == "No verificado" and any(k in nota for k in SIN_WEB):
        p["estado_web"] = "Sin sitio web"
    redes = [n for k, n in (("facebook", "Facebook"), ("instagram", "Instagram"), ("linkedin", "LinkedIn"), ("yelp", "Yelp")) if c.get(k)]
    if redes: p["redes_sociales"] = "; ".join(redes)
    elif c and p["redes_sociales"] == "No verificado": p["redes_sociales"] = "Ninguna encontrada"
    p["_sunbiz"] = SUNBIZ.get(pid)
    p["_alerta"] = alerta(c.get("nota", ""))

wb = Workbook()
res = wb.active; res.title = "Resumen"
ws = wb.create_sheet("Prospectos")
title(ws, "Prospectos: empresas con brecha digital", "Fuente por fila. Columnas azules/amarillas = completar tras verificación en Sunbiz y Google Maps.")
cols = ["ID","Empresa","Municipio","Barrio/zona","Condado","Sector (detalle)","NAICS","Industria (NAICS)","Forma legal","Estado web",
        "Redes sociales","Tiene redes","Evidencia","Fuente","Empleados (est.)","Año fundación","Peso web","Peso sector","Señal tamaño",
        "Puntaje","Prioridad","Estado Sunbiz","Próximo paso",
        "Dirección","Teléfono","Web","Facebook","Instagram","LinkedIn","Yelp","Fuente contacto","Alerta","Nota contacto"]
HR = 4
header(ws, HR, cols, [6,34,17,15,12,30,7,30,13,20,22,11,48,40,10,10,8,8,8,8,10,13,26,36,16,28,30,30,30,30,36,18,40])
for i, p in enumerate(rows, 1):
    r = HR + i
    mun, barrio = BARRIO.get(p["area"], (p["area"], ""))
    red = p["redes_sociales"]
    tiene = "No verificado" if red == "No verificado" else ("No" if red.startswith("Ninguna") else "Sí")
    vals = [f"P{i:03d}", p["nombre"], mun, barrio, p["condado"], p["sector"], p["naics2"], NAICS[p["naics2"]], legal(p["forma_legal"]),
            ESTADO[p["estado_web"]], red, tiene, p["evidencia"] + ("" if legal(p["forma_legal"]) == p["forma_legal"] else f" | Forma legal fuente: {p['forma_legal']}"),
            p["fuente_url"]]
    for c, v in enumerate(vals, 1): ws.cell(row=r, column=c, value=v)
    emp, yr = size_signals(p["evidencia"])
    ws.cell(row=r, column=15, value=emp); ws.cell(row=r, column=16, value=yr)
    ws.cell(row=r, column=17, value=f"=IFERROR(VLOOKUP(J{r},Parametros!$A$5:$B$9,2,FALSE),0)")
    ws.cell(row=r, column=18, value=f"=IFERROR(VLOOKUP(H{r},Parametros!$D$5:$E$16,2,FALSE),1)")
    ws.cell(row=r, column=19, value=f'=IF(OR(N(O{r})>=Parametros!$H$9,AND(N(P{r})>0,N(P{r})<=Parametros!$H$10)),1,0)')
    ws.cell(row=r, column=20, value=f"=Q{r}+R{r}+S{r}")
    ws.cell(row=r, column=21, value=f'=IF(OR(V{r}="Inactive",V{r}="No encontrada",V{r}="Duplicado"),"Descartada",IF(AND(T{r}>=Parametros!$H$5,S{r}=1),"A",IF(T{r}>=Parametros!$H$6,"B","C")))')
    ws.cell(row=r, column=22, value=p["_sunbiz"] or sunbiz_default(p))
    c = p["_c"]
    for j, k in enumerate(("direccion", "telefono", "web", "facebook", "instagram", "linkedin", "yelp", "fuente_contacto"), 24):
        ws.cell(row=r, column=j, value=c.get(k) or None)
    ws.cell(row=r, column=32, value=p["_alerta"] or None)
    ws.cell(row=r, column=33, value=c.get("nota") or None)
    ws.cell(row=r, column=23, value="Verificar Sunbiz (posible inactiva)" if "inactiv" in (p["forma_legal"]+p["evidencia"]).lower() or "revocada" in p["evidencia"] else "")
LAST = HR + len(rows)
body(ws, HR + 1, LAST, len(cols), url_cols=(14, 26, 27, 28, 29, 30, 31))
for r in range(HR + 1, LAST + 1):
    for c in (22, 23):
        ws.cell(row=r, column=c).font = INP
        ws.cell(row=r, column=c).fill = PatternFill("solid", fgColor="FFF9DB")
    for c in (7, 12, 15, 16, 17, 18, 19, 20, 21):
        ws.cell(row=r, column=c).alignment = Alignment(horizontal="center", vertical="top")
dv = DataValidation(type="list", formula1='"Active,Inactive,Pendiente,No encontrada,Duplicado"', allow_blank=True)
ws.add_data_validation(dv); dv.add(f"V{HR+1}:V{LAST}")
dv2 = DataValidation(type="list", formula1='"Verificar web en Google Maps,Auditoría web,Email B2B 1 a 1,Visita presencial,Descartar"', allow_blank=True)
ws.add_data_validation(dv2); dv2.add(f"W{HR+1}:W{LAST}")
rng = f"U{HR+1}:U{LAST}"
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"A"'], font=Font(name=F, bold=True, color="FFFFFF"), fill=PatternFill("solid", fgColor=ACC)))
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"B"'], fill=PatternFill("solid", fgColor="CCE7E9")))
ws.conditional_formatting.add(f"J{HR+1}:J{LAST}", FormulaRule(formula=[f'OR(J{HR+1}="Sin sitio web",J{HR+1}="Sitio obsoleto")'], font=Font(name=F, bold=True, color="B42318")))
ws.freeze_panes = f"C{HR+1}"
ws.auto_filter.ref = f"A{HR}:{L(len(cols))}{LAST}"

# ---- Parámetros ----
pa = wb.create_sheet("Parametros")
title(pa, "Parámetros del puntaje", "Azul = supuestos editables. El puntaje de Prospectos se recalcula al cambiarlos.")
header(pa, 4, ["Estado web", "Peso", "", "Industria (NAICS)", "Peso", "", "Prioridad", "Puntaje mínimo"], [24,8,3,36,8,3,12,16])
for c in (3, 6): pa.cell(row=4, column=c).fill = PatternFill(fill_type=None)
pe = [("Sin sitio web",3),("Sitio obsoleto",3),("Presencia desordenada",2),("No verificado",1),("Tiene web (auditar)",1)]
ps = [("23 Construcción y oficios",3,"CPL $76–228: alto valor por cliente"),("48-49 Transporte y logística",3,"B2B, tamaño medio, baja madurez digital"),
      ("62 Salud",3,"CPC $5–10, alta intención local"),("54 Servicios profesionales",3,"CPC legal $9.87+, ticket alto"),
      ("42 Comercio mayorista",2,"B2B CPL $103; decisión lenta"),("31-33 Manufactura",2,"B2B, catálogo/cotizador"),
      ("53 Inmobiliario/admin. propiedades",2,"CPL $100"),("81 Servicios (auto, náutico, reparación)",2,"Náutico FTL: ticket alto; auto CPL $28"),
      ("72 Restaurantes/hotelería",1,"Ticket bajo, CPC $2"),("11 Agricultura/viveros",1,"Mayorista, baja demanda de search"),
      ("Sin clasificar",1,""),("",None,"")]
for i, (k, v) in enumerate(pe, 5): pa.cell(row=i, column=1, value=k); pa.cell(row=i, column=2, value=v).font = INP
for i, (k, v, n) in enumerate(ps, 5):
    pa.cell(row=i, column=4, value=k); c = pa.cell(row=i, column=5, value=v); c.font = INP
    if n: pa.cell(row=i + 0, column=9, value=n).font = ST
pa.cell(row=5, column=7, value="A"); pa.cell(row=5, column=8, value=6).font = INP
pa.cell(row=6, column=7, value="B"); pa.cell(row=6, column=8, value=4).font = INP
pa.cell(row=7, column=7, value="C"); pa.cell(row=7, column=8, value="< B")
pa.cell(row=9, column=7, value="Empleados mín."); pa.cell(row=9, column=8, value=10).font = INP
pa.cell(row=10, column=7, value="Fundada hasta"); pa.cell(row=10, column=8, value=2000).font = INP
pa["A18"] = "Puntaje = Peso web + Peso sector + Señal tamaño (1 si ≥10 empleados/camiones o fundada ≤2000). Máx. 7. Prioridad A exige además Señal tamaño = 1 (empresa mediana/establecida). Inactive en Sunbiz = Descartada."; pa["A18"].font = ST
pa["A19"] = "Pesos de sector derivados de benchmarks Google Ads (hoja Google_Ads) y ticket de servicio esperado. Criterio propio, ajustable."; pa["A19"].font = ST
for r in range(5, 17):
    for c in (1,2,4,5,7,8):
        x = pa.cell(row=r, column=c)
        if x.font != INP: x.font = B
        x.border = bd

# ---- Oportunidad por industria (fórmulas) ----
op = wb.create_sheet("Oportunidad_Industria")
title(op, "Matriz de oportunidad por industria", "Conteos vivos desde Prospectos. Ticket y CPL = supuestos editables (azul) con fuente en Google_Ads.")
oc = ["Industria (NAICS)","Prospectos","Sin web","Sitio obsoleto","Desordenada","Brecha (sin web+obsoleto+desordenada)","% brecha",
      "Prioridad A","Ticket web (USD)","Retainer mensual (USD)","Valor potencial año 1 (USD)","CPL ref. Google Ads (USD)"]
header(op, 4, oc, [36,11,9,11,11,18,9,11,14,15,18,15])
inds = [k for k, _, _ in ps if k and k != "Sin clasificar"]
tick = {"23":(4500,1500,76.40),"48":(5000,1500,103.54),"62":(4500,1800,56.83),"54":(6000,2000,131.63),"42":(4000,1200,103.54),
        "31":(4000,1200,103.54),"53":(3500,1200,100.48),"81":(3000,1000,28.50),"72":(2500,800,30.27),"11":(3000,800,70.11)}
P = f"Prospectos!$H${HR+1}:$H${LAST}"; E = f"Prospectos!$J${HR+1}:$J${LAST}"; S = f"Prospectos!$U${HR+1}:$U${LAST}"
for i, ind in enumerate(inds, 5):
    code = ind[:2]
    t = tick[code]
    op.cell(row=i, column=1, value=ind)
    op.cell(row=i, column=2, value=f'=COUNTIF({P},A{i})')
    op.cell(row=i, column=3, value=f'=COUNTIFS({P},A{i},{E},"Sin sitio web")')
    op.cell(row=i, column=4, value=f'=COUNTIFS({P},A{i},{E},"Sitio obsoleto")')
    op.cell(row=i, column=5, value=f'=COUNTIFS({P},A{i},{E},"Presencia desordenada")')
    op.cell(row=i, column=6, value=f"=C{i}+D{i}+E{i}")
    op.cell(row=i, column=7, value=f"=IF(B{i}=0,0,F{i}/B{i})").number_format = "0%"
    op.cell(row=i, column=8, value=f'=COUNTIFS({P},A{i},{S},"A")')
    for c, v in ((9, t[0]), (10, t[1]), (12, t[2])):
        x = op.cell(row=i, column=c, value=v); x.number_format = "$#,##0"
    op.cell(row=i, column=11, value=f"=F{i}*(I{i}+J{i}*12)").number_format = "$#,##0"
    op.cell(row=i, column=12).number_format = "$#,##0.00"
end = 4 + len(inds)
tr = end + 1
op.cell(row=tr, column=1, value="Total")
for c in (2,3,4,5,6,8,11):
    op.cell(row=tr, column=c, value=f"=SUM({L(c)}5:{L(c)}{end})")
op.cell(row=tr, column=7, value=f"=IF(B{tr}=0,0,F{tr}/B{tr})").number_format = "0%"
op.cell(row=tr, column=11).number_format = "$#,##0"
body(op, 5, tr, len(oc))
for r in range(5, end + 1):
    for c in (9, 10, 12): op.cell(row=r, column=c).font = INP
    op.cell(row=r, column=7).number_format = "0%"; op.cell(row=r, column=11).number_format = "$#,##0"
    for c in (9,10): op.cell(row=r, column=c).number_format = "$#,##0"
    op.cell(row=r, column=12).number_format = "$#,##0.00"
for c in range(1, len(oc) + 1): op.cell(row=tr, column=c).font = BB
op.cell(row=tr + 2, column=1, value="Valor potencial año 1 = empresas con brecha × (ticket web + retainer × 12). Asume 100% de cierre: aplicar tasa de conversión real (típico B2B frío 2–5%).").font = ST
op.cell(row=tr + 3, column=1, value="Tickets: rangos Miami web pyme $2,500–15,000; SEO local $750–3,000/mes; redes $1,000–3,000/mes (ver Google_Ads). Valores de la tabla = punto medio conservador.").font = ST
op.freeze_panes = "B5"

# ---- Macro por área ----
ma = wb.create_sheet("Macro_Areas")
title(ma, "Contexto económico por área", "Census QuickFacts / ABS 2022, municipios y DataUSA. 'Estimado' = no verificado en fuente primaria.")
mc = ["Área","Condado","Población","Año","Firmas empleadoras (ABS 2022)","Carácter económico","NAICS clave","Verificación","Fuente"]
header(ma, 4, mc, [18,12,12,7,16,52,16,14,48])
for i, a in enumerate(AREAS, 5):
    for c, v in enumerate(a, 1): ma.cell(row=i, column=c, value=v)
    ma.cell(row=i, column=3).number_format = "#,##0"; ma.cell(row=i, column=5).number_format = "#,##0"
e = 4 + len(AREAS)
body(ma, 5, e, len(mc), url_cols=(9,))
r0 = e + 3
ma.cell(row=r0 - 1, column=1, value="Condados").font = BB
header(ma, r0, ["Condado","Población","Establecimientos (CBP)","Año","Est. 20–99 empl.","Est. 100–499 empl.","Mid-market (20–499)","% mid-market","Fuente"])
for i, cty in enumerate(COUNTIES, r0 + 1):
    for c, v in enumerate(cty[:6], 1): ma.cell(row=i, column=c, value=v)
    ma.cell(row=i, column=7, value=f"=E{i}+F{i}"); ma.cell(row=i, column=8, value=f"=IF(C{i}=0,0,G{i}/C{i})")
    ma.cell(row=i, column=9, value=cty[6])
    for c in (2,3,5,6,7): ma.cell(row=i, column=c).number_format = "#,##0"
    ma.cell(row=i, column=8).number_format = "0.0%"
body(ma, r0 + 1, r0 + len(COUNTIES), 9, url_cols=(9,))
for i in range(r0 + 1, r0 + 1 + len(COUNTIES)):
    for c in (5, 6): ma.cell(row=i, column=c).font = INP
ma.cell(row=r0 + len(COUNTIES) + 1, column=1, value="Est. 20–99 y 100–499 = ESTIMADO (proporciones nacionales CBP ≈12% y ≈2.2%). Verificar en data.census.gov tabla CB2300CBP, FIPS 12086 y 12011.").font = ST

# ---- Adopción digital ----
ad = wb.create_sheet("Adopcion_Digital")
title(ad, "Adopción digital y formación de empresas", "Encuestas nacionales (no hay datos específicos de Florida) + estadísticas oficiales.")
header(ad, 4, ["Indicador","Valor","Año","Fuente","URL"], [52,18,8,34,60])
for i, d in enumerate(DIGITAL, 5):
    for c, v in enumerate(d, 1): ad.cell(row=i, column=c, value=v)
body(ad, 5, 4 + len(DIGITAL), 5, url_cols=(5,))

# ---- Google Ads ----
ga = wb.create_sheet("Google_Ads")
title(ga, "Google Ads: benchmarks y precios de servicios", "WordStream/LocaliQ = muestras grandes. Keywords Miami = herramientas de agencia (orientativo). Confirmar con Keyword Planner.")
header(ga, 4, ["Industria / keyword","NAICS","CPC (USD)","CPL (USD)","Nota","Fuente"], [36,8,11,11,40,60])
for i, a in enumerate(ADS, 5):
    for c, v in enumerate(a, 1): ga.cell(row=i, column=c, value=v)
    ga.cell(row=i, column=3).number_format = "$#,##0.00"; ga.cell(row=i, column=4).number_format = "$#,##0.00"
e = 4 + len(ADS)
body(ga, 5, e, 6, url_cols=(6,))
r0 = e + 3
ga.cell(row=r0 - 1, column=1, value="Precios de mercado de servicios digitales (Miami)").font = BB
header(ga, r0, ["Servicio","Mínimo (USD)","Máximo (USD)","Punto medio","Unidad","Fuente"])
for i, p in enumerate(PRECIOS, r0 + 1):
    ga.cell(row=i, column=1, value=p[0]); ga.cell(row=i, column=2, value=p[1]); ga.cell(row=i, column=3, value=p[2])
    ga.cell(row=i, column=4, value=f"=AVERAGE(B{i}:C{i})"); ga.cell(row=i, column=5, value=p[3]); ga.cell(row=i, column=6, value=p[4])
    for c in (2,3,4): ga.cell(row=i, column=c).number_format = "$#,##0"
body(ga, r0 + 1, r0 + len(PRECIOS), 6, url_cols=(6,))

# ---- Legal ----
lg = wb.create_sheet("Legal_Cumplimiento")
title(lg, "Legalidad de empresas y cumplimiento comercial", "Florida Division of Corporations (Sunbiz), DBPR, BTR condado/ciudad, FTSA, TCPA, CAN-SPAM, ADA. No es asesoría legal.")
header(lg, 4, ["Tema","Regla / dato","Implicación comercial","Fuente oficial"], [30,62,52,56])
for i, x in enumerate(LEGAL, 5):
    for c, v in enumerate(x, 1): lg.cell(row=i, column=c, value=v)
body(lg, 5, 4 + len(LEGAL), 4, url_cols=(4,))
r = 6 + len(LEGAL)
lg.cell(row=r, column=1, value="Portales de datos abiertos para escalar la base de prospectos").font = BB
portales = [("Miami-Dade Open Data – Local Business Tax View","https://opendata.miamidade.gov/datasets/local-business-tax-view"),
            ("Miami-Dade – Certificates of Use","https://gis-mdc.opendata.arcgis.com/datasets/1952228619b0463cb6f9f7dc839bff88"),
            ("Broward GeoHub – Business Tax Records","https://geohub-bcgis.opendata.arcgis.com/datasets/business-tax-records/about"),
            ("Sunbiz – descargas masivas (SFTP)","https://dos.fl.gov/sunbiz/other-services/data-downloads/"),
            ("DBPR – búsqueda de licencias","https://www2.myfloridalicense.com/")]
for j, (n, u) in enumerate(portales, r + 1):
    lg.cell(row=j, column=1, value=n); lg.cell(row=j, column=4, value=u)
body(lg, r + 1, r + len(portales), 4, url_cols=(4,))

# ---- Metodología ----
me = wb.create_sheet("Metodologia")
title(me, "Metodología, alcance y limitaciones", "Investigación de escritorio con fuentes públicas gratuitas. Fecha de corte: septiembre 2026.")
txt = [
 ("Objetivo","Identificar empresas medianas/establecidas en Miami-Dade y Broward (Fort Lauderdale, Kendall, Miami Beach, Medley, Doral, Hialeah, Homestead y alrededores) sin sitio web, con sitio obsoleto o con presencia digital fragmentada."),
 ("Fuentes","Census (QuickFacts, CBP, ABS, BFS), Florida Division of Corporations (Sunbiz), DBPR, tax collectors de Miami-Dade y Broward, sitios municipales, FDACS, FTC, Florida Senate; directorios públicos (BBB, Manta, Yelp, YellowPages, D&B, Bizapedia); benchmarks WordStream/LocaliQ."),
 ("Criterio estado web","Sin sitio web = ningún dominio propio en resultados de búsqueda. Sitio obsoleto = señales técnicas (http sin HTTPS, .html estático, plantilla sin personalizar, erratas). Presencia desordenada = varios dominios/fichas duplicadas. Tiene web (auditar) = dominio propio, calidad no auditada."),
 ("Limitación 1","El estado web se infirió de fragmentos de búsqueda, no de visitas a cada sitio. Verificar antes de contactar."),
 ("Limitación 2","Forma legal inferida del sufijo del nombre (Inc/LLC/Corp) salvo que se indique Sunbiz. Columna 'Estado Sunbiz' queda 'Pendiente' para validación manual en search.sunbiz.org."),
 ("Limitación 3","Empleados y ventas = estimaciones de Manta/D&B. Establecimientos 20–499 empleados por condado = estimado con proporciones nacionales."),
 ("Limitación 4","Muestra: 95 empresas (no censo). Sesgo hacia industrias con presencia en directorios. Cobertura baja en Miami Beach, Wynwood, restaurantes y salud."),
 ("Siguiente fase","Descargar datasets BTR (Miami-Dade, Broward) + archivo trimestral Sunbiz → cruzar por dirección → verificar dominio automáticamente (DNS/HTTP) → escalar a miles de prospectos con estado web medido."),
 ("Cumplimiento","Contacto recomendado: email B2B 1 a 1 conforme a CAN-SPAM y visita presencial. Evitar marcadores automáticos y SMS masivos (FTSA/TCPA)."),
]
header(me, 4, ["Tema","Detalle"], [22,120])
for i, (k, v) in enumerate(txt, 5): me.cell(row=i, column=1, value=k); me.cell(row=i, column=2, value=v)
body(me, 5, 4 + len(txt), 2)
for i in range(5, 5 + len(txt)): me.cell(row=i, column=1).font = BB

# ---- Resumen (KPIs con fórmulas) ----
title(res, "Oportunidad digital – Miami-Dade y Broward", "Empresas establecidas sin web o con web obsoleta. Tablas dinámicas en hojas TD_*. Septiembre 2026.")
for c, w in zip("ABCDEFGH", (26,14,3,26,14,3,26,14)): res.column_dimensions[c].width = w
kp = [("Prospectos identificados", f"=COUNTA(Prospectos!B{HR+1}:B{LAST})", "0"),
      ("Sin sitio web", f'=COUNTIF({E},"Sin sitio web")', "0"),
      ("Sitio obsoleto / desordenado", f'=COUNTIF({E},"Sitio obsoleto")+COUNTIF({E},"Presencia desordenada")', "0"),
      ("Brecha confirmada (%)", f"=IF(B5=0,0,(B6+B7)/B5)", "0%"),
      ("Prioridad A", f'=COUNTIF({S},"A")', "0"),
      ("Pendientes de verificar web", f'=COUNTIF({E},"No verificado")', "0")]
res["A4"] = "Indicadores"; res["A4"].font = BB
for i, (k, f, nf) in enumerate(kp, 5):
    res.cell(row=i, column=1, value=k).font = B
    x = res.cell(row=i, column=2, value=f); x.font = Font(name=F, size=14, bold=True, color=ACC); x.number_format = nf
    res.cell(row=i, column=1).border = bd; x.border = bd
res["D4"] = "Por condado"; res["D4"].font = BB
C = f"Prospectos!$E${HR+1}:$E${LAST}"
for i, cty in enumerate(("Miami-Dade", "Broward"), 5):
    res.cell(row=i, column=4, value=cty).font = B
    x = res.cell(row=i, column=5, value=f'=COUNTIF({C},D{i})'); x.font = Font(name=F, size=14, bold=True, color=ACC)
res["D8"] = "Con brecha en Miami-Dade"; res["E8"] = f'=COUNTIFS({C},"Miami-Dade",{E},"Sin sitio web")+COUNTIFS({C},"Miami-Dade",{E},"Sitio obsoleto")+COUNTIFS({C},"Miami-Dade",{E},"Presencia desordenada")'
res["D9"] = "Con brecha en Broward"; res["E9"] = f'=COUNTIFS({C},"Broward",{E},"Sin sitio web")+COUNTIFS({C},"Broward",{E},"Sitio obsoleto")+COUNTIFS({C},"Broward",{E},"Presencia desordenada")'
for r in (8, 9):
    res[f"D{r}"].font = B; res[f"E{r}"].font = Font(name=F, size=14, bold=True, color=ACC)
res["G4"] = "Mercado"; res["G4"].font = BB
mk = [("Establecimientos Miami-Dade (CBP 2023)", 98394), ("Establecimientos Broward (CBP 2022)", 67274),
      ("Solicitudes de negocio FL 2024", 634000), ("Pymes EE.UU. sin web (Clutch 2025)", 0.17),
      ("Demandas ADA Title III FL 2025", 1823), ("CPC promedio Google Ads 2025", 5.26)]
for i, (k, v) in enumerate(mk, 5):
    res.cell(row=i, column=7, value=k).font = B
    x = res.cell(row=i, column=8, value=v); x.font = Font(name=F, size=12, bold=True, color=INK)
    x.number_format = "0%" if v < 1 else ("$0.00" if v < 10 else "#,##0")
res["A13"] = "Hallazgos clave"; res["A13"].font = BB
hall = [
 "1. Medley, Hialeah y Doral concentran la brecha más valiosa: manufactura, transporte y distribución B2B con 10–100 empleados, décadas operando y presencia solo en directorios (BBB, Manta, Yelp).",
 "2. Transporte de carga (flotas de 55–66 camiones en Medley) y contratistas (Construct Group ~100 empleados con plantilla web sin editar) = prioridad A: ticket alto y competidores ya digitalizados.",
 "3. En la náutica de Fort Lauderdale la mayoría ya tiene web. La oportunidad está en talleres antiguos (desde 1976–1999) con solo BBB/Yelp y en rediseño de sitios básicos.",
 "4. HVAC, plomería y administración de propiedades (Davie, Sunrise, North Miami) muestran alta proporción de negocios sin dominio propio y CPL de Google Ads de $76–100: fácil demostrar ROI.",
 "5. Florida es 2.º estado en demandas ADA (1,823 en 2025): una web accesible (WCAG 2.2 AA) es un argumento de venta con riesgo legal cuantificable.",
 "6. Canal de contacto recomendado: email B2B 1 a 1 (CAN-SPAM) + visita presencial. Evitar llamadas/SMS automatizados (FTSA: $500–1,500 por violación).",
 "7. Escalamiento: datasets abiertos BTR de Miami-Dade/Broward + SFTP de Sunbiz permiten pasar de ~95 a miles de prospectos con verificación automática de dominio.",
]
for i, h in enumerate(hall, 14):
    res.merge_cells(start_row=i, start_column=1, end_row=i, end_column=8)
    c = res.cell(row=i, column=1, value=h); c.font = B; c.alignment = WR
    res.row_dimensions[i].height = 30
res["A22"] = "Hojas: Prospectos · TD_Area_Web · TD_Industria_Web · TD_Legal_Prioridad · TD_Redes · Oportunidad_Industria · Macro_Areas · Adopcion_Digital · Google_Ads · Legal_Cumplimiento · Parametros · Metodologia"
res["A22"].font = ST

tmp = os.path.join(ROOT, "_tmp_build.xlsx")
out = os.path.join(ROOT, "Miami_Oportunidad_Digital.xlsx")
wb.save(tmp)

from pivot_uno import run
data_rows = LAST
run(tmp, out, [
  dict(src="Prospectos", dst="TD_Area_Web", name="TD1", hdr_row=HR, last_row=LAST,
       fields=[("Condado","row"),("Municipio","row"),("Estado web","col"),("Empresa","data_count")]),
  dict(src="Prospectos", dst="TD_Industria_Web", name="TD2", hdr_row=HR, last_row=LAST,
       fields=[("Condado","page"),("Industria (NAICS)","row"),("Estado web","col"),("Empresa","data_count")]),
  dict(src="Prospectos", dst="TD_Legal_Prioridad", name="TD3", hdr_row=HR, last_row=LAST,
       fields=[("Condado","page"),("Forma legal","row"),("Prioridad","col"),("Empresa","data_count")]),
  dict(src="Prospectos", dst="TD_Redes", name="TD4", hdr_row=HR, last_row=LAST,
       fields=[("Industria (NAICS)","page"),("Tiene redes","row"),("Condado","col"),("Empresa","data_count")]),
], sheet_titles={
  "TD_Area_Web": "Tabla dinámica: prospectos por condado, municipio y estado web",
  "TD_Industria_Web": "Tabla dinámica: industria × estado web (filtro: condado)",
  "TD_Legal_Prioridad": "Tabla dinámica: forma legal × prioridad (filtro: condado)",
  "TD_Redes": "Tabla dinámica: presencia en redes sociales × condado (filtro: industria)",
}, after="Prospectos")
os.remove(tmp)
print("OK", out, len(rows), "prospectos")
