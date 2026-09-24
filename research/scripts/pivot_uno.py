"""Crea tablas dinámicas nativas (DataPilot) con LibreOffice Calc vía UNO y guarda en .xlsx."""
import os, subprocess, tempfile, time
import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.table import CellAddress, CellRangeAddress
from com.sun.star.sheet.DataPilotFieldOrientation import ROW, COLUMN, DATA, PAGE
from com.sun.star.sheet.GeneralFunction import COUNT, SUM

XLSX = "Calc MS Excel 2007 XML"


def _pv(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p


def _idx(sheets, name):
    return [i for i in range(sheets.Count) if sheets.getByIndex(i).Name == name][0]


def run(inp, out, specs, sheet_titles=None, after=None, port=2002):
    prof = tempfile.mkdtemp(prefix="lo_profile_")
    env = dict(os.environ, SAL_USE_VCLPLUGIN="svp")
    proc = subprocess.Popen(["soffice", f"-env:UserInstallation=file://{prof}", "--headless", "--invisible",
                             "--norestore", f"--accept=socket,host=localhost,port={port};urp;"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
    local = uno.getComponentContext()
    res = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    ctx = None
    for _ in range(90):
        try:
            ctx = res.resolve(f"uno:socket,host=localhost,port={port};urp;StarOffice.ComponentContext"); break
        except Exception:
            time.sleep(1)
    desk = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desk.loadComponentFromURL(uno.systemPathToFileUrl(os.path.abspath(inp)), "_blank", 0,
                                    (_pv("Hidden", True), _pv("FilterName", XLSX)))
    doc.calculateAll()
    sheets = doc.Sheets
    pos = _idx(sheets, after) + 1 if after else sheets.Count
    for spec in specs:
        src = sheets.getByName(spec["src"])
        hr = spec.get("hdr_row", 1) - 1
        headers = []
        c = 0
        while src.getCellByPosition(c, hr).String:
            headers.append(src.getCellByPosition(c, hr).String); c += 1
        if not sheets.hasByName(spec["dst"]):
            sheets.insertNewByName(spec["dst"], pos); pos += 1
        dst = sheets.getByName(spec["dst"])
        t = dst.getCellByPosition(0, 0)
        t.String = (sheet_titles or {}).get(spec["dst"], spec["dst"])
        t.CharFontName = "Arial"; t.CharHeight = 14; t.CharWeight = 150; t.CharColor = 0x1F2937
        n = dst.getCellByPosition(0, 1)
        n.String = "Origen: hoja Prospectos. Clic derecho > Actualizar tras editar datos. Filtros en la fila superior de la tabla."
        n.CharFontName = "Arial"; n.CharHeight = 9; n.CharColor = 0x6B7280
        d = dst.getDataPilotTables().createDataPilotDescriptor()
        r = CellRangeAddress(); r.Sheet = _idx(sheets, spec["src"])
        r.StartColumn = 0; r.StartRow = hr; r.EndColumn = len(headers) - 1; r.EndRow = spec["last_row"] - 1
        d.setSourceRange(r)
        flds = d.getDataPilotFields()
        for name, orient in spec["fields"]:
            f = flds.getByIndex(headers.index(name))
            if orient == "row": f.Orientation = ROW
            elif orient == "col": f.Orientation = COLUMN
            elif orient == "page": f.Orientation = PAGE
            else:
                f.Orientation = DATA; f.Function = SUM if orient == "data_sum" else COUNT
        d.RowGrand = True; d.ColumnGrand = True
        a = CellAddress(); a.Sheet = _idx(sheets, spec["dst"]); a.Column = 0; a.Row = 3
        dst.getDataPilotTables().insertNewByName(spec["name"], a, d)
        cols = dst.Columns
        cols.getByIndex(0).Width = 8000
        for i in range(1, 10): cols.getByIndex(i).Width = 3600
    doc.storeToURL(uno.systemPathToFileUrl(os.path.abspath(out)), (_pv("FilterName", XLSX),))
    doc.close(True)
    try:
        desk.terminate()
    except Exception:
        pass
    proc.wait(timeout=60)
