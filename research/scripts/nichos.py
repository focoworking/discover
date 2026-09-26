"""Nicho comercial: más fino que el NAICS a 2 dígitos. Es lo que el equipo de ventas
reconoce («moda», «joyería», «música»). Si la fila trae 'nicho' se respeta; si no, se
deduce del detalle del sector con reglas en orden (la primera que coincide gana)."""
import re

REGLAS = [
    (r"joyer|reloj|jewel|\boro\b|empeño|pawn", "Joyería y relojería"),
    (r"botánica", "Botánicas y artículos religiosos"),
    (r"ferreter", "Ferreterías"),
    (r"cerrajer|locksmith", "Reparación y servicios técnicos"),
    (r"arquitect", "Arquitectura e ingeniería"),
    (r"perfum|cosmét", "Perfumería y cosmética"),
    (r"óptica|eyewear|optic", "Óptica"),
    (r"moda|boutique|ropa|textil|tejidos|guayaber|novias|confecci|sastrer|alteracion|nupcial|bridal|zapater[ií]a de moda|calzado|uniforme|lencer|trajes de baño", "Moda y confección"),
    (r"música|music|grabaci|recording|dj\b|instrumento|guitarra", "Música y entretenimiento"),
    (r"evento|\bbodas?\b|banquete|party rental|fiesta", "Eventos y bodas"),
    (r"\barte\b|galer[ií]a de arte|fotogr|\bvideo|diseño gráfico|enmarc", "Arte, fotografía y diseño"),
    (r"imprent|rótulo|\bsigns?\b|serigraf", "Imprenta y rótulos"),
    (r"florist|flores", "Floristería"),
    (r"tatu", "Tatuajes"),
    (r"náutic|yate|yacht|boat|marina|boatyard", "Náutico"),
    (r"escuela de belleza|cosmetolog", "Educación y academias"),
    (r"autoescuela|tránsito|tutor|guarder|vpk|preescolar", "Educación y academias"),
    (r"llanta|tire|carrocer|diésel|diesel|camiones|detailing|autolavado|automotriz|auto |colisión|mecánica", "Automotriz"),
    (r"hvac|aire acondicionado|electrodom|plomer", "Climatización y plomería"),
    (r"contratista|construc|paviment|ventanas|techo|acero|varilla|prefabricad|materiales", "Construcción y materiales"),
    (r"mudanza|transporte|carga|freight|forwarding|logíst|broker de carga", "Transporte y logística"),
    (r"panader|bakery|pastel|cafeter|heladería", "Panaderías y cafeterías"),
    (r"restaurante|\bdiner\b|grill|marisquer|tavern", "Restaurantes"),
    (r"hotel|motel|huéspedes", "Hoteles y alojamiento"),
    (r"barber|salón de belleza|belleza|uñas|spa\b", "Belleza y barberías"),
    (r"dental|odontolog", "Dental"),
    (r"farmacia", "Farmacias"),
    (r"veterinari|mascota|canina|perros|grooming", "Mascotas y veterinaria"),
    (r"médic|medicin|clínica|fisioterapia|quiropr|salud", "Salud médica"),
    (r"seguro|hipotecari|envío de dinero|remesa", "Seguros y finanzas"),
    (r"contabilidad|impuesto|income tax|bufete|abogad|legal", "Legal y contable"),
    (r"arquitect|ingenier", "Arquitectura e ingeniería"),
    (r"propiedades|inmobil|real estate|bienes raíces", "Inmobiliario"),
    (r"boxeo|gimnasio|baile|artes marciales|pesca|charter|fitness", "Fitness, deporte y recreación"),
    (r"tintorer|lavander|zapater", "Tintorerías y lavanderías"),
    (r"paisaj|jard[ií]n|césped|plagas|limpieza|janitorial", "Limpieza, jardinería y plagas"),
    (r"alarma|seguridad", "Seguridad"),
    (r"vivero|agricul|farm|empacadora", "Agricultura y viveros"),
    (r"botánica", "Botánicas y artículos religiosos"),
    (r"mueble|tapicer|decoraci", "Muebles y decoración"),
    (r"ferreter", "Ferreterías"),
    (r"viaje|turismo", "Viajes y turismo"),
    (r"limosina|limousine|party bus", "Transporte de pasajeros"),
    (r"funerari", "Funerarias"),
    (r"cerrajer|locksmith|celular|computadora|reparación de", "Reparación y servicios técnicos"),
    (r"distribuc|mayorista|import|suministro|alimentos|crucero|frutas|carnes", "Mayoristas y distribución"),
    (r"paleta|soldadura|taller mecánico|maquinado|manufactura|fabricaci", "Manufactura e industria"),
]

def nicho(sector, dado=None):
    if dado: return dado
    t = (sector or "").lower()
    for pat, n in REGLAS:
        if re.search(pat, t): return n
    return "Otros servicios"
