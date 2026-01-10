#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Planes de Gobierno - Costa Rica 2026-2030
Versión 3.0 - Scoring estructural sin penalizaciones + Coherencia contextual separada

Actúa como un analista cívico técnico, neutral, verificable y auditable.
Procesa planes de gobierno (PDF) y los convierte en datos estructurados comparables.

NO: juicios de valor, recomendaciones de voto, evaluación de ideologías,
inferencias, completar vacíos, asumir financiamiento/plazos implícitos.
"""

import fitz  # PyMuPDF
import json
import os
import re
import hashlib
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Optional

# ====================================================================
# CONFIGURACIÓN
# ====================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLANES_DIR = os.path.join(BASE_DIR, "planes")
DATA_DIR = os.path.join(BASE_DIR, "data")

# ====================================================================
# PILARES NACIONALES (FIJOS)
# ====================================================================

PILLARS = [
    {"pillar_id": "P1", "pillar_name": "Sostenibilidad fiscal y crecimiento económico", "weight": 0.15},
    {"pillar_id": "P2", "pillar_name": "Empleo y competitividad", "weight": 0.15},
    {"pillar_id": "P3", "pillar_name": "Seguridad ciudadana y justicia", "weight": 0.15},
    {"pillar_id": "P4", "pillar_name": "Salud pública y seguridad social (CCSS)", "weight": 0.15},
    {"pillar_id": "P5", "pillar_name": "Educación y talento humano", "weight": 0.15},
    {"pillar_id": "P6", "pillar_name": "Ambiente y desarrollo sostenible", "weight": 0.05},
    {"pillar_id": "P7", "pillar_name": "Reforma del Estado y lucha contra la corrupción", "weight": 0.10},
    {"pillar_id": "P8", "pillar_name": "Política social focalizada", "weight": 0.08},
    {"pillar_id": "P9", "pillar_name": "Política exterior y comercio internacional", "weight": 0.02},
]

PILLAR_WEIGHTS = {p["pillar_id"]: p["weight"] for p in PILLARS}
CRITICAL_PILLARS = {"P1", "P2", "P3", "P4", "P5", "P7"}

# ====================================================================
# PALABRAS CLAVE POR PILAR
# ====================================================================

PILLAR_KEYWORDS = {
    "P1": [
        "fiscal", "tributar", "impuesto", "presupuest", "déficit", "deuda", "hacienda",
        "recaudación", "gasto público", "austeridad", "PIB", "crecimiento económico",
        "inversión pública", "finanzas públicas", "equilibrio fiscal", "reforma tributaria",
        "ingreso", "egreso", "sostenibilidad", "banco central", "inflación", "estabilidad",
        "economía", "económic", "productiv", "desarrollo económico", "renta", "regla fiscal"
    ],
    "P2": [
        "empleo", "trabajo", "desempleo", "competitividad", "PYME", "mipyme", "empresa",
        "emprendimiento", "innovación", "productividad", "exportación", "importación",
        "industria", "manufactura", "zona franca", "comercio", "salario mínimo",
        "informalidad", "formal", "capacitación laboral", "reconversión", "empleabilidad",
        "negocio", "inversión privada", "atracción de inversión", "simplificación",
        "trámite", "regulación", "burocracia", "mercado laboral"
    ],
    "P3": [
        "seguridad", "policía", "crimen", "delincuencia", "narcotráfico", "drogas",
        "violencia", "homicidio", "robo", "asalto", "cárcel", "prisión", "penitenciar",
        "justicia", "tribunal", "judicial", "fiscal", "denuncia", "prevención del delito",
        "OIJ", "fuerza pública", "criminalidad", "armas", "extorsión", "sicariato",
        "pandillas", "crimen organizado", "lavado de dinero", "seguridad pública"
    ],
    "P4": [
        "salud", "CCSS", "Caja Costarricense", "hospital", "clínica", "médic",
        "enfermedad", "vacuna", "epidemia", "pandemia", "medicina", "farmacia",
        "EBAIS", "lista de espera", "atención primaria", "seguridad social", "pensión",
        "jubilación", "IVM", "régimen especial", "cotizante", "asegurado", "paciente",
        "cirugía", "tratamiento", "prevención", "promoción de la salud", "bienestar"
    ],
    "P5": [
        "educación", "escuela", "colegio", "universidad", "docente", "maestro", "profesor",
        "estudiante", "alumno", "MEP", "curriculum", "deserción escolar", "aprendizaje",
        "lectura", "matemática", "ciencia", "tecnología", "STEM", "educación técnica",
        "formación profesional", "INA", "beca", "infraestructura educativa", "conectividad",
        "digitalización educativa", "calidad educativa", "evaluación", "PISA", "talento"
    ],
    "P6": [
        "ambiente", "ambiental", "cambio climático", "carbono neutral", "descarbonización",
        "emisiones", "renovable", "solar", "eólico", "agua", "recurso hídrico", "bosque",
        "deforestación", "biodiversidad", "conservación", "parque nacional", "área protegida",
        "contaminación", "reciclaje", "residuos", "basura", "sostenible", "sostenibilidad",
        "verde", "ecológico", "protección ambiental", "SINAC", "MINAE", "huella de carbono"
    ],
    "P7": [
        "reforma del estado", "modernización", "digitalización", "gobierno digital",
        "simplificación administrativa", "corrupción", "transparencia", "rendición de cuentas",
        "contraloría", "auditoría", "procuraduría", "ética", "probidad", "servidor público",
        "funcionario", "planilla", "eficiencia", "burocracia", "trámite", "desregulación",
        "descentralización", "municipalidad", "autonomía", "gobernanza", "institucional"
    ],
    "P8": [
        "pobreza", "vulnerable", "vulnerabilidad", "desigualdad", "bono", "subsidio",
        "transferencia", "IMAS", "FODESAF", "programa social", "ayuda social", "asistencia",
        "niñez", "adolescencia", "PANI", "adulto mayor", "discapacidad", "CONAPDIS",
        "jefatura femenina", "mujer", "género", "indígena", "afrodescendiente", "migrante",
        "focalización", "extrema pobreza", "asentamiento", "vivienda social", "BANHVI"
    ],
    "P9": [
        "política exterior", "relaciones internacionales", "diplomacia", "embajada",
        "consulado", "comercio internacional", "tratado", "TLC", "OMC", "exportación",
        "importación", "inversión extranjera", "cooperación internacional", "ONU",
        "OEA", "SICA", "integración centroamericana", "fronteras", "Nicaragua", "Panamá",
        "Estados Unidos", "China", "Europa", "bilateral", "multilateral", "soberanía"
    ]
}

# ====================================================================
# INDICADORES PARA DIMENSIONES D1-D4
# ====================================================================

# D2: Plazos verificables (VÁLIDOS)
TIME_INDICATORS_VALID = [
    r"primer(?:o|a)?\s*(?:año|mes|semestre|trimestre)",
    r"segundo\s*(?:año|mes|semestre|trimestre)",
    r"tercer(?:o|a)?\s*(?:año|mes|semestre|trimestre)",
    r"cuarto\s*(?:año|mes|semestre|trimestre)",
    r"primeros?\s*\d+\s*(?:años?|meses?|días?|semanas?)",
    r"\d+\s*(?:años?|meses?)\s*(?:de\s+gobierno|del\s+cuatrienio)?",
    r"20\d{2}[-–]20\d{2}",
    r"(?:para|antes\s+de(?:l)?|en)\s*(?:el\s*)?20\d{2}",
    r"cuatrienio\s*20\d{2}[-–]20\d{2}",
    r"período?\s*20\d{2}[-–]20\d{2}",
    r"al\s*(?:inicio|final)\s*del?\s*(?:gobierno|administración|gestión|período|periodo)",
    r"en\s*los\s*primeros\s*\d+\s*(?:días?|meses?|años?)",
    r"fase\s*(?:\d+|I+V?|uno|dos|tres)",
    r"etapa\s*(?:\d+|I+V?|uno|dos|tres)",
    r"primeros?\s*100\s*días",
    r"durante\s*el\s*cuatrienio",
    r"corto\s*plazo\s*\(.*?\d+.*?\)",
    r"mediano\s*plazo\s*\(.*?\d+.*?\)",
    r"largo\s*plazo\s*\(.*?\d+.*?\)"
]

# D3: Mecanismos concretos
HOW_INDICATORS = [
    r"mediante\s+(?:la|el|un|una)\s+\w+",
    r"a\s*través\s*de\s+(?:la|el|un|una)\s+\w+",
    r"por\s*medio\s*de\s+(?:la|el|un|una)\s+\w+",
    r"(?:crear|establecer|implementar|desarrollar|promover|impulsar|fortalecer|reformar|modificar)(?:á|emos|emos)?\s+(?:una?|el|la)\s+\w+",
    r"proyecto\s*de\s*ley",
    r"decreto\s*ejecutivo",
    r"reglamento\s+(?:que|para|de)",
    r"directriz\s+(?:que|para|de)",
    r"convenio\s+(?:con|entre|de)",
    r"acuerdo\s+(?:con|entre|de)",
    r"alianza\s*(?:con|público[-\s]?privada)",
    r"coordinación\s*(?:con|inter)",
    r"articulación\s+(?:con|entre|de)",
    r"mesa\s*(?:de\s*)?(?:trabajo|diálogo|coordinación)",
    r"comisión\s+(?:para|de|que)",
    r"consejo\s+(?:para|de|que)",
    r"programa\s+(?:de|para|nacional)",
    r"plan\s*(?:de\s*)?(?:acción|trabajo|implementación|nacional)",
    r"estrategia\s+(?:de|para|nacional)",
    r"metodología\s+(?:de|para)",
    r"protocolo\s+(?:de|para)",
    r"sistema\s*(?:de|para)\s+\w+",
    r"plataforma\s+(?:de|para|digital)",
    r"aplicación\s+(?:de|para|móvil|digital)",
    r"reforma\s+(?:a|de|del|al)\s+(?:la|el)?\s*\w+"
]

# D4: Fuentes de financiamiento
FUNDING_INDICATORS = [
    r"financ(?:iar|iamiento|iado)\s+(?:con|mediante|por)",
    r"presupuest(?:o|ar|ario)\s+(?:de|del|para|nacional)",
    r"recursos?\s*(?:económicos?|financieros?|públicos?|del\s+Estado)",
    r"fondos?\s*(?:públicos?|del\s+Estado|de\s+(?:la|el)\s+\w+)",
    r"inversión\s*(?:de|pública|privada|del\s+Estado)",
    r"reasignación\s+(?:de\s+)?(?:recursos?|presupuest)",
    r"recorte\s+(?:de\s+)?(?:gasto|presupuest)",
    r"ahorro\s*(?:en|de|del)\s+(?:gasto|presupuest)",
    r"impuesto\s+(?:a|al|de|sobre)",
    r"tribut(?:o|ario|ación)\s+(?:a|al|de|sobre)",
    r"tasa\s+(?:a|al|de|sobre)",
    r"canon\s+(?:a|al|de|por)",
    r"tarifa\s+(?:de|por|para)",
    r"deuda\s*(?:pública|interna|externa)",
    r"crédito\s+(?:de|del|con|internacional)",
    r"préstamo\s+(?:de|del|con|internacional)",
    r"emisión\s+(?:de\s*)?(?:bonos?|títulos?)",
    r"cooperación\s*(?:internacional|técnica|financiera)",
    r"donación\s+(?:de|del|internacional)",
    r"alianza\s*público[-\s]?privada",
    r"APP\b",
    r"concesión\s+(?:de|para|a)",
    r"fideicomiso\s+(?:de|para)",
    r"(?:BID|Banco\s+Mundial|CAF|FMI|BCIE)",
    r"\d+(?:\.\d+)?\s*(?:millones?|billones?)\s*(?:de\s+)?(?:colones|dólares)",
    r"\d+(?:[.,]\d+)?%\s*del\s*(?:PIB|presupuesto|gasto)"
]

# ====================================================================
# COHERENCIA CONTEXTUAL (NO AFECTA SCORING)
# ====================================================================

CONSTITUTIONAL_CONFLICT_PATTERNS = {
    "ccss_funds": {
        "patterns": [
            r"(?:usar|utilizar|destinar|redirigir)\s+(?:los\s+)?(?:fondos?|recursos?)\s+(?:de\s+la\s+)?CCSS\s+(?:para|en)\s+(?!salud|pensiones|seguros)",
        ],
        "reference": "Art. 73 Constitución - Fondos CCSS",
    },
    "education_budget": {
        "patterns": [
            r"(?:reducir|recortar|disminuir)\s+(?:el\s+)?(?:presupuesto|gasto)\s+(?:de|en)\s+educación\s+(?:por\s+debajo|menos)",
        ],
        "reference": "Art. 78 Constitución - 8% PIB para educación",
    },
    "judicial_independence": {
        "patterns": [
            r"(?:eliminar|suprimir|abolir)\s+(?:la\s+)?(?:independencia|autonomía)\s+(?:del\s+)?(?:Poder\s+)?Judicial",
        ],
        "reference": "Art. 9, 152-167 Constitución - Independencia judicial",
    },
}

FISCAL_CONFLICT_PATTERNS = {
    "unfunded_spending": {
        "patterns": [
            r"(?:aumentar|incrementar|duplicar|triplicar)\s+(?:el\s+)?(?:gasto|inversión|presupuesto)",
        ],
        "reference": "Regla fiscal vigente",
    },
}


# ====================================================================
# FUNCIONES DE UTILIDAD
# ====================================================================

def normalize_text(text: str) -> str:
    """Normaliza el texto para análisis."""
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def generate_proposal_id(pdf_id: str, text: str) -> str:
    """Genera un ID único para una propuesta."""
    hash_input = f"{pdf_id}:{text[:100]}"
    short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
    return f"{pdf_id.lower()}-{short_hash}"


def slugify(text: str) -> str:
    """Convierte texto a slug."""
    import unicodedata
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text


# ====================================================================
# EXTRACCIÓN DE PDF
# ====================================================================

def extract_text_from_pdf(pdf_path: str) -> List[Tuple[int, str]]:
    """Extrae texto de un PDF, retornando lista de (página, texto)."""
    pages = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            normalized = normalize_text(text)
            if normalized:
                pages.append((page_num + 1, normalized))
        doc.close()
    except Exception as e:
        print(f"Error leyendo {pdf_path}: {e}")
    return pages


def extract_candidate_info_from_pdf(pages: List[Tuple[int, str]], pdf_id: str) -> Dict[str, str]:
    """Extrae información del candidato desde las primeras páginas."""
    first_pages_text = " ".join([text for _, text in pages[:5]])
    
    candidate_name = "no_especificado"
    party_name = "no_especificado"
    pdf_title = "Plan de Gobierno 2026–2030"
    
    # Buscar nombre del candidato
    candidate_patterns = [
        r"candidat[oa]\s+(?:a\s+la\s+)?presidencia[:\s]+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,4})",
        r"(?:Dr\.|Lic\.|Ing\.|Sr\.|Sra\.)\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,4})",
        r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\s+(?:para\s+)?[Pp]residente",
    ]
    
    for pattern in candidate_patterns:
        match = re.search(pattern, first_pages_text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name) > 5 and len(name.split()) >= 2:
                candidate_name = name
                break
    
    # Buscar nombre del partido
    party_patterns = [
        r"[Pp]artido\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-Za-záéíóúñ]+){0,5})",
        r"[Cc]oalición\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-Za-záéíóúñ]+){0,5})",
        r"[Aa]lianza\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-Za-záéíóúñ]+){0,5})",
    ]
    
    for pattern in party_patterns:
        match = re.search(pattern, first_pages_text)
        if match:
            party = match.group(0).strip()
            if len(party) > 5:
                party_name = party
                break
    
    # Buscar título del plan
    title_patterns = [
        r"[Pp]lan\s+(?:de\s+)?[Gg]obierno\s+([^\.]+)",
        r"[Pp]rograma\s+(?:de\s+)?[Gg]obierno\s+([^\.]+)",
        r"[Pp]ropuesta\s+(?:de\s+)?[Gg]obierno\s+([^\.]+)",
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, first_pages_text)
        if match:
            title = match.group(0).strip()[:100]
            pdf_title = title
            break
    
    return {
        "candidate_name": candidate_name,
        "party_name": party_name,
        "pdf_title": pdf_title
    }


# ====================================================================
# IDENTIFICACIÓN DE PILARES
# ====================================================================

def identify_primary_pillar(text: str) -> Optional[str]:
    """Identifica el pilar principal de un texto."""
    text_lower = text.lower()
    scores = {}
    
    for pillar_id, keywords in PILLAR_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score >= 2:
            scores[pillar_id] = score
    
    if not scores:
        return None
    
    return max(scores, key=scores.get)


# ====================================================================
# EVALUACIÓN DE DIMENSIONES D1-D4
# ====================================================================

def check_dimension_existence(text: str) -> bool:
    """D1: Verifica si describe una acción concreta."""
    action_patterns = [
        r"(?:crear|establecer|implementar|desarrollar|reformar|modificar|construir|ampliar)(?:á|emos)?\s+",
        r"(?:programa|proyecto|plan|estrategia|política)\s+(?:de|para|nacional)\s+\w+",
        r"(?:ley|decreto|reglamento|directriz)\s+(?:de|para|que)\s+\w+",
        r"(?:invertir|destinar|asignar)\s+(?:recursos?|fondos?|presupuesto)",
        r"(?:reducir|aumentar|eliminar|fortalecer)\s+(?:el|la|los|las)?\s*\w+",
        r"(?:meta|objetivo|indicador)\s*:\s*\d+",
    ]
    
    # Frases aspiracionales NO cuentan
    aspirational = [
        r"(?:buscar|aspirar|desear|esperar)\s+(?:que|a)",
        r"(?:sería|podría|debería)\s+(?:bueno|importante|necesario)",
    ]
    
    for pattern in aspirational:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    
    for pattern in action_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False


def check_dimension_when(text: str) -> Tuple[bool, str]:
    """D2: Verifica si indica plazo verificable."""
    for pattern in TIME_INDICATORS_VALID:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return True, match.group(0).strip()
    return False, "no_especificado"


def check_dimension_how(text: str) -> Tuple[bool, str]:
    """D3: Verifica si describe mecanismo concreto."""
    for pattern in HOW_INDICATORS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 10)
            end = min(len(text), match.end() + 50)
            context = text[start:end].strip()
            return True, context[:120]
    return False, "no_especificado"


def check_dimension_funding(text: str) -> Tuple[bool, str]:
    """D4: Verifica si identifica fuente de financiamiento."""
    for pattern in FUNDING_INDICATORS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 10)
            end = min(len(text), match.end() + 50)
            context = text[start:end].strip()
            return True, context[:120]
    return False, "no_especificado"


# ====================================================================
# EXTRACCIÓN DE PROPUESTAS
# ====================================================================

def extract_best_proposal_per_pillar(pages: List[Tuple[int, str]], pdf_id: str) -> Dict[str, Dict]:
    """
    Extrae COMO MÁXIMO una propuesta por pilar.
    Selecciona la mejor (mayor score de dimensiones).
    """
    candidates_by_pillar = defaultdict(list)
    
    for page_num, text in pages:
        paragraphs = re.split(r'\n\s*\n|\.\s+(?=[A-ZÁÉÍÓÚÑ])', text)
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if len(paragraph) < 50:
                continue
            
            pillar_id = identify_primary_pillar(paragraph)
            if not pillar_id:
                continue
            
            # D1: Verificar que sea propuesta concreta
            is_concrete = check_dimension_existence(paragraph)
            if not is_concrete:
                continue
            
            # D2-D4
            has_when, when_text = check_dimension_when(paragraph)
            has_how, how_text = check_dimension_how(paragraph)
            has_funding, funding_text = check_dimension_funding(paragraph)
            
            dimensions = {
                "existence": 1,
                "when": 1 if has_when else 0,
                "how": 1 if has_how else 0,
                "funding": 1 if has_funding else 0
            }
            
            raw_score = sum(dimensions.values())
            
            # Snippet (máx 240 caracteres)
            snippet = paragraph[:237] + "…" if len(paragraph) > 240 else paragraph
            
            # Título corto
            title = paragraph[:57] + "…" if len(paragraph) > 60 else paragraph[:60]
            
            proposal = {
                "pillar_id": pillar_id,
                "page_num": page_num,
                "text": paragraph[:500],
                "title": title,
                "dimensions": dimensions,
                "raw_score": raw_score,
                "extracted_fields": {
                    "when_text": when_text,
                    "how_text": how_text,
                    "funding_text": funding_text
                },
                "snippet": snippet
            }
            
            candidates_by_pillar[pillar_id].append(proposal)
    
    # Seleccionar la mejor propuesta por pilar
    best_by_pillar = {}
    for pillar_id, proposals in candidates_by_pillar.items():
        # Ordenar por raw_score (desc), luego por funding (desc)
        proposals.sort(key=lambda p: (p["raw_score"], p["dimensions"]["funding"]), reverse=True)
        best_by_pillar[pillar_id] = proposals[0]
    
    return best_by_pillar


def create_proposals_json(best_by_pillar: Dict[str, Dict], candidate_id: str, pdf_id: str) -> List[Dict]:
    """Crea la lista de propuestas en formato JSON."""
    proposals = []
    
    for pillar in PILLARS:
        pillar_id = pillar["pillar_id"]
        
        if pillar_id in best_by_pillar:
            p = best_by_pillar[pillar_id]
            proposal = {
                "proposal_id": generate_proposal_id(pdf_id, p["text"]),
                "candidate_id": candidate_id,
                "pillar_id": pillar_id,
                "proposal_title": p["title"],
                "proposal_text": p["text"],
                "dimensions": p["dimensions"],
                "extracted_fields": p["extracted_fields"],
                "evidence": {
                    "pdf_id": pdf_id,
                    "page": p["page_num"],
                    "snippet": p["snippet"]
                },
                "multi_pillar_source_proposal_id": "no_especificado"
            }
        else:
            # Placeholder para pilar sin contenido
            proposal = {
                "proposal_id": generate_proposal_id(pdf_id, f"placeholder_{pillar_id}"),
                "candidate_id": candidate_id,
                "pillar_id": pillar_id,
                "proposal_title": "No se encontró propuesta para este pilar",
                "proposal_text": "El documento no contiene propuestas concretas identificables para este pilar.",
                "dimensions": {
                    "existence": 0,
                    "when": 0,
                    "how": 0,
                    "funding": 0
                },
                "extracted_fields": {
                    "when_text": "no_especificado",
                    "how_text": "no_especificado",
                    "funding_text": "no_especificado"
                },
                "evidence": {
                    "pdf_id": pdf_id,
                    "page": 1,
                    "snippet": "No se encontró contenido para este pilar."
                },
                "multi_pillar_source_proposal_id": "no_especificado"
            }
        
        proposals.append(proposal)
    
    return proposals


# ====================================================================
# SCORING ESTRUCTURAL (SIN PENALIZACIONES)
# ====================================================================

def calculate_candidate_score(proposals: List[Dict], candidate_id: str) -> Dict:
    """
    Calcula scores por pilar.
    NO aplica penalizaciones (según nuevo prompt).
    """
    proposal_by_pillar = {p["pillar_id"]: p for p in proposals if p["candidate_id"] == candidate_id}
    
    pillar_scores = []
    
    for pillar in PILLARS:
        pillar_id = pillar["pillar_id"]
        weight = pillar["weight"]
        
        prop = proposal_by_pillar.get(pillar_id)
        
        if prop:
            dims = prop["dimensions"]
            raw_score = dims["existence"] + dims["when"] + dims["how"] + dims["funding"]
        else:
            raw_score = 0
        
        # effective_score = raw_score (sin penalizaciones)
        effective_score = raw_score
        normalized = effective_score / 4.0
        weighted = normalized * weight
        
        pillar_scores.append({
            "pillar_id": pillar_id,
            "raw_score": raw_score,
            "effective_score": effective_score,
            "normalized": round(normalized, 4),
            "weighted": round(weighted, 4),
            "penalties": []  # Sin penalizaciones
        })
    
    # Totales
    raw_sum = sum(ps["raw_score"] for ps in pillar_scores)
    weighted_sum = sum(ps["weighted"] for ps in pillar_scores)
    
    # Pilares críticos
    coverage_critical = sum(
        ps["weighted"] for ps in pillar_scores
        if ps["pillar_id"] in CRITICAL_PILLARS
    )
    
    # Notas técnicas neutrales
    notes = []
    empty_pillars = [ps["pillar_id"] for ps in pillar_scores if ps["raw_score"] == 0]
    if empty_pillars:
        notes.append(f"Sin propuestas identificadas: {', '.join(empty_pillars)}")
    
    low_score_pillars = [ps["pillar_id"] for ps in pillar_scores if 0 < ps["raw_score"] < 3]
    if low_score_pillars:
        notes.append(f"Propuestas parciales: {', '.join(low_score_pillars)}")
    
    return {
        "candidate_id": candidate_id,
        "pillar_scores": pillar_scores,
        "overall": {
            "raw_sum": raw_sum,
            "weighted_sum": round(weighted_sum, 4),
            "coverage_critical_weighted_sum": round(coverage_critical, 4),
            "notes": " | ".join(notes) if notes else ""
        }
    }


# ====================================================================
# COHERENCIA CONTEXTUAL (INFORMATIVA, NO AFECTA RANKING)
# ====================================================================

def analyze_contextual_coherence(pages: List[Tuple[int, str]], candidate_id: str) -> Dict:
    """
    Analiza coherencia constitucional y fiscal.
    Esta fase NO afecta puntajes ni ranking.
    """
    full_text = " ".join([text for _, text in pages])
    
    # Coherencia constitucional
    constitutional_status = "aligned"
    constitutional_reference = ""
    constitutional_note = ""
    
    for conflict_name, conflict_info in CONSTITUTIONAL_CONFLICT_PATTERNS.items():
        for pattern in conflict_info["patterns"]:
            if re.search(pattern, full_text, re.IGNORECASE):
                constitutional_status = "potential_conflict"
                constitutional_reference = conflict_info["reference"]
                constitutional_note = f"Se identificó posible conflicto: {conflict_name}"[:240]
                break
        if constitutional_status == "potential_conflict":
            break
    
    # Coherencia fiscal
    fiscal_status = "aligned"
    fiscal_reference = ""
    fiscal_note = ""
    
    # Verificar gasto sin financiamiento
    has_spending = bool(re.search(
        r"(?:aumentar|incrementar|crear|duplicar)\s+(?:el\s+)?(?:gasto|inversión|programa|subsidio)",
        full_text, re.IGNORECASE
    ))
    
    has_funding_mentioned = bool(re.search(
        r"(?:financiad|mediante\s+(?:impuesto|presupuesto|cooperación)|fuente\s+de\s+(?:fondos|recursos))",
        full_text, re.IGNORECASE
    ))
    
    if has_spending and not has_funding_mentioned:
        fiscal_status = "unclear"
        fiscal_reference = "Regla fiscal vigente - Déficit fiscal"
        fiscal_note = "El plan propone gastos sin especificar fuentes de financiamiento claras."
    
    # Observaciones contextuales (neutrales, descriptivas)
    context_notes = []
    
    # IED
    if not re.search(r"inversión\s+(?:extranjera|directa|IED)", full_text, re.IGNORECASE):
        context_notes.append({
            "topic": "Inversión extranjera",
            "observation": "No se menciona inversión extranjera directa pese a su peso en empleo nacional."
        })
    
    # Crimen organizado
    if not re.search(r"(?:crimen\s+organizado|narcotráfico|criminalidad\s+transnacional)", full_text, re.IGNORECASE):
        context_notes.append({
            "topic": "Criminalidad organizada",
            "observation": "No se aborda explícitamente la criminalidad organizada transnacional."
        })
    
    return {
        "candidate_id": candidate_id,
        "contextual_coherence": {
            "constitutional_alignment": {
                "status": constitutional_status,
                "reference": constitutional_reference,
                "note": constitutional_note
            },
            "fiscal_context_alignment": {
                "status": fiscal_status,
                "reference": fiscal_reference,
                "note": fiscal_note
            },
            "national_context_notes": context_notes
        }
    }


# ====================================================================
# RANKING
# ====================================================================

def generate_ranking(candidate_scores: List[Dict]) -> Dict:
    """Genera el ranking de candidatos."""
    # Ranking por weighted_sum
    ranking_overall = sorted(
        [(cs["candidate_id"], cs["overall"]["weighted_sum"]) for cs in candidate_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    # Ranking por coverage_critical_weighted_sum
    ranking_critical = sorted(
        [(cs["candidate_id"], cs["overall"]["coverage_critical_weighted_sum"]) for cs in candidate_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    return {
        "method_version": "v3",
        "weights": PILLAR_WEIGHTS,
        "ranking_overall_weighted": [
            {"rank": i + 1, "candidate_id": cid, "weighted_sum": ws}
            for i, (cid, ws) in enumerate(ranking_overall)
        ],
        "ranking_critical_weighted": [
            {"rank": i + 1, "candidate_id": cid, "coverage_critical_weighted_sum": ccws}
            for i, (cid, ccws) in enumerate(ranking_critical)
        ]
    }


# ====================================================================
# PROCESAMIENTO PRINCIPAL
# ====================================================================

def process_all_pdfs():
    """Procesa todos los PDFs y genera los archivos JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(PLANES_DIR) if f.endswith('.pdf')]
    
    all_candidates = []
    all_proposals = []
    all_coherence = []
    
    print(f"Procesando {len(pdf_files)} planes de gobierno...")
    print("=" * 60)
    
    for pdf_file in sorted(pdf_files):
        pdf_id = pdf_file.replace('.pdf', '')
        pdf_path = os.path.join(PLANES_DIR, pdf_file)
        
        print(f"\n📄 Procesando: {pdf_id}...")
        
        # Extraer texto del PDF
        pages = extract_text_from_pdf(pdf_path)
        
        if not pages:
            print(f"   ⚠️  No se pudo extraer texto de {pdf_file}")
            continue
        
        print(f"   → {len(pages)} páginas extraídas")
        
        # Extraer información del candidato
        info = extract_candidate_info_from_pdf(pages, pdf_id)
        
        # Generar candidate_id basado en nombre
        if info["candidate_name"] != "no_especificado":
            candidate_id = slugify(info["candidate_name"])
        else:
            candidate_id = pdf_id.lower()
        
        candidate = {
            "candidate_id": candidate_id,
            "candidate_name": info["candidate_name"],
            "party_name": info["party_name"],
            "pdf_id": pdf_id,
            "pdf_title": info["pdf_title"],
            "pdf_url": "no_especificado"
        }
        all_candidates.append(candidate)
        
        # Extraer mejor propuesta por pilar
        best_by_pillar = extract_best_proposal_per_pillar(pages, pdf_id)
        print(f"   → {len(best_by_pillar)} pilares con propuestas")
        
        # Crear propuestas JSON
        proposals = create_proposals_json(best_by_pillar, candidate_id, pdf_id)
        all_proposals.extend(proposals)
        
        # Análisis de coherencia contextual
        coherence = analyze_contextual_coherence(pages, candidate_id)
        all_coherence.append(coherence)
        
        # Resumen
        pillar_summary = ", ".join([
            f"{p_id}={best_by_pillar[p_id]['raw_score']}" 
            for p_id in sorted(best_by_pillar.keys())
        ])
        print(f"   → Scores: {pillar_summary}")
    
    print("\n" + "=" * 60)
    print(f"\n📊 RESUMEN GENERAL:")
    print(f"   • Candidatos procesados: {len(all_candidates)}")
    print(f"   • Propuestas totales: {len(all_proposals)} (máx 9 por candidato)")
    
    # Calcular scores por candidato
    all_candidate_scores = []
    for candidate in all_candidates:
        scores = calculate_candidate_score(all_proposals, candidate["candidate_id"])
        all_candidate_scores.append(scores)
    
    # Generar ranking
    ranking = generate_ranking(all_candidate_scores)
    
    # Guardar archivos
    print("\n📁 Guardando archivos:")
    
    outputs = {
        "candidates.json": all_candidates,
        "pillars.json": PILLARS,
        "proposals.json": all_proposals,
        "candidate_scores.json": all_candidate_scores,
        "ranking.json": ranking,
        "contextual_coherence.json": all_coherence
    }
    
    for filename, data in outputs.items():
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"   ✅ {filepath}")
    
    return outputs


if __name__ == "__main__":
    print("=" * 60)
    print("PROCESADOR DE PLANES DE GOBIERNO - COSTA RICA 2026-2030")
    print("Versión 3.0 - Scoring estructural + Coherencia contextual")
    print("=" * 60)
    result = process_all_pdfs()
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
