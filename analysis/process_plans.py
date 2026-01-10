#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Planes de Gobierno - Costa Rica 2026-2030
Versión 2.0 - Con dimensión D5 de compatibilidad normativa y fiscal

Extrae propuestas de PDFs y las clasifica en 9 pilares nacionales.
Evalúa 4 dimensiones principales + 1 dimensión de control (D5).
"""

import fitz  # PyMuPDF
import json
import os
import re
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Optional
import unicodedata

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLANES_DIR = os.path.join(BASE_DIR, "planes")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Mapeo de partidos políticos de Costa Rica con candidatos conocidos
PARTY_INFO = {
    "ACRM": {"party_name": "Alianza Costarricense por la Responsabilidad y el Movimiento", "candidate_name": "Por determinar"},
    "CAC": {"party_name": "Coalición Agrícola y Campesina", "candidate_name": "Por determinar"},
    "CDS": {"party_name": "Ciudadanos de la Sierra", "candidate_name": "Por determinar"},
    "CR1": {"party_name": "Costa Rica Primero", "candidate_name": "Por determinar"},
    "FA": {"party_name": "Frente Amplio", "candidate_name": "Por determinar"},
    "PA": {"party_name": "Partido Accesibilidad sin Exclusión", "candidate_name": "Por determinar"},
    "PDLCT": {"party_name": "Partido de los Trabajadores", "candidate_name": "Por determinar"},
    "PEL": {"party_name": "Partido El Pueblo", "candidate_name": "Por determinar"},
    "PEN": {"party_name": "Partido Encuentro Nacional", "candidate_name": "Por determinar"},
    "PIN": {"party_name": "Partido Integración Nacional", "candidate_name": "Por determinar"},
    "PJSC": {"party_name": "Partido Justicia Social Costarricense", "candidate_name": "Por determinar"},
    "PLN": {"party_name": "Partido Liberación Nacional", "candidate_name": "Por determinar"},
    "PLP": {"party_name": "Partido Liberal Progresista", "candidate_name": "Por determinar"},
    "PNG": {"party_name": "Partido Nueva Generación", "candidate_name": "Por determinar"},
    "PNR": {"party_name": "Partido Nueva República", "candidate_name": "Por determinar"},
    "PPSO": {"party_name": "Partido Progreso Social Democrático", "candidate_name": "Por determinar"},
    "PSD": {"party_name": "Partido Social Demócrata", "candidate_name": "Por determinar"},
    "PUCD": {"party_name": "Partido Unidad Cristiana Demócrata", "candidate_name": "Por determinar"},
    "PUSC": {"party_name": "Partido Unidad Social Cristiana", "candidate_name": "Por determinar"},
    "UP": {"party_name": "Unidos Podemos", "candidate_name": "Por determinar"},
}

# Definición de pilares con pesos
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

# Palabras clave por pilar para identificación de propuestas
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

# D2: Indicadores de temporalidad (SOLO plazos verificables)
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

# Frases vagas que NO cuentan como plazo
TIME_INDICATORS_INVALID = [
    r"a\s*futuro",
    r"gradualmente",
    r"paulatinamente",
    r"progresivamente",
    r"eventualmente",
    r"en\s*su\s*momento",
    r"cuando\s*sea\s*posible",
    r"en\s*el\s*tiempo"
]

# D3: Indicadores de mecanismo/implementación
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

# D4: Indicadores de financiamiento
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
# DIMENSIÓN D5: COMPATIBILIDAD NORMATIVA Y FISCAL
# ====================================================================

# Indicadores de conflicto constitucional potencial
CONSTITUTIONAL_CONFLICT_PATTERNS = {
    "ccss_funds": {
        "patterns": [
            r"(?:usar|utilizar|destinar|redirigir)\s+(?:los\s+)?(?:fondos?|recursos?)\s+(?:de\s+la\s+)?CCSS\s+(?:para|en)\s+(?!salud|pensiones|seguros)",
            r"(?:fondos?|recursos?)\s+(?:de\s+la\s+)?CCSS\s+(?:para|hacia)\s+(?:infraestructura|seguridad|educación)"
        ],
        "reference": "Art. 73 Constitución - Fondos CCSS",
        "conflict_type": "constitutional"
    },
    "education_budget": {
        "patterns": [
            r"(?:reducir|recortar|disminuir)\s+(?:el\s+)?(?:presupuesto|gasto)\s+(?:de|en)\s+educación\s+(?:por\s+debajo\s+del|menos\s+del)\s+(?:6|8)%",
            r"(?:menos|inferior)\s+(?:del|al)\s+(?:6|8)%\s+(?:del\s+PIB)?\s+(?:para|en)\s+educación"
        ],
        "reference": "Art. 78 Constitución - 8% PIB para educación",
        "conflict_type": "constitutional"
    },
    "judicial_independence": {
        "patterns": [
            r"(?:eliminar|suprimir|abolir)\s+(?:la\s+)?(?:independencia|autonomía)\s+(?:del\s+)?(?:Poder\s+)?Judicial",
            r"(?:subordinar|someter)\s+(?:el\s+)?(?:Poder\s+)?Judicial\s+(?:al|a\s+la)\s+(?:Ejecutivo|Asamblea)"
        ],
        "reference": "Art. 9, 152-167 Constitución - Independencia judicial",
        "conflict_type": "constitutional"
    },
    "contraloría": {
        "patterns": [
            r"(?:eliminar|suprimir|abolir)\s+(?:la\s+)?Contraloría",
            r"(?:subordinar|someter)\s+(?:la\s+)?Contraloría\s+(?:al|a\s+la)\s+(?:Ejecutivo|Presidencia)"
        ],
        "reference": "Art. 183-184 Constitución - Contraloría General",
        "conflict_type": "constitutional"
    }
}

# Indicadores de conflicto fiscal potencial
FISCAL_CONFLICT_PATTERNS = {
    "unfunded_spending": {
        "patterns": [
            r"(?:aumentar|incrementar|duplicar|triplicar)\s+(?:el\s+)?(?:gasto|inversión|presupuesto)\s+(?:en|de|para)\s+\w+(?:\s+\w+)*(?!\s*(?:mediante|con|a\s+través|financiad))",
            r"(?:crear|establecer|implementar)\s+(?:un\s+)?(?:programa|subsidio|bono|transferencia)\s+(?:de|para)\s+\w+(?:\s+\w+)*(?!\s*(?:mediante|con|financiad))"
        ],
        "reference": "Regla fiscal vigente - Déficit fiscal",
        "conflict_type": "fiscal"
    },
    "debt_increase": {
        "patterns": [
            r"(?:aumentar|incrementar|expandir)\s+(?:la\s+)?deuda\s+(?:pública|del\s+Estado)\s+(?:sin\s+límite|indefinidamente|ilimitadamente)"
        ],
        "reference": "Art. 176-180 Constitución - Hacienda Pública",
        "conflict_type": "fiscal"
    }
}

# Indicadores de reforma legal mencionada (exime de conflicto)
REFORM_INDICATORS = [
    r"reforma\s+constitucional",
    r"modificar\s+(?:la\s+)?Constitución",
    r"enmienda\s+constitucional",
    r"cambio\s+(?:al\s+)?marco\s+legal",
    r"reforma\s+(?:a\s+la\s+)?ley",
    r"proyecto\s+de\s+ley\s+(?:para|de)\s+reform",
    r"modificar\s+(?:la\s+)?legislación",
    r"actualizar\s+(?:el\s+)?marco\s+(?:legal|normativo)"
]


def normalize_text(text: str) -> str:
    """Normaliza el texto para análisis."""
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


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
    """Intenta extraer información del candidato desde las primeras páginas."""
    info = PARTY_INFO.get(pdf_id, {
        "party_name": f"Partido {pdf_id}",
        "candidate_name": "Por determinar"
    }).copy()
    
    first_pages_text = " ".join([text for _, text in pages[:5]])
    
    candidate_patterns = [
        r"candidat[oa]\s+(?:a\s+la\s+)?presidencia[:\s]+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,4})",
        r"(?:Dr\.|Lic\.|Ing\.|Sr\.|Sra\.)\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,4})",
    ]
    
    for pattern in candidate_patterns:
        match = re.search(pattern, first_pages_text, re.IGNORECASE)
        if match:
            candidate_name = match.group(1).strip()
            if len(candidate_name) > 5 and len(candidate_name.split()) >= 2:
                info["candidate_name"] = candidate_name
                break
    
    return info


def identify_pillar(text: str) -> List[str]:
    """Identifica a qué pilares pertenece un texto basado en palabras clave."""
    text_lower = text.lower()
    matched_pillars = []
    
    for pillar_id, keywords in PILLAR_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text_lower:
                score += 1
        if score >= 2:
            matched_pillars.append((pillar_id, score))
    
    matched_pillars.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in matched_pillars[:3]]


def check_dimension_existence(text: str) -> bool:
    """D1: Verifica si la propuesta es concreta (acción, medida o política específica)."""
    action_patterns = [
        r"(?:vamos\s*a|se\s*va\s*a|proponemos?|impulsaremos?|crearemos?|estableceremos?|implementaremos?)\s+\w+",
        r"(?:crear|establecer|implementar|desarrollar|promover|impulsar|fortalecer|reformar)(?:á|emos)?\s+(?:una?|el|la)\s+\w+",
        r"(?:programa|proyecto|plan|estrategia|política)\s+(?:de|para|nacional)\s+\w+",
        r"(?:ley|decreto|reglamento|directriz)\s+(?:de|para|que)\s+\w+",
        r"(?:invertir|destinar|asignar)\s+(?:recursos?|fondos?|presupuesto)\s+(?:para|en|a)",
        r"(?:construcción|ampliación|mejora|rehabilitación)\s+de\s+\w+",
        r"(?:contratación|capacitación|formación)\s+de\s+\w+",
        r"(?:reducir|aumentar|eliminar|modificar)\s+(?:el|la|los|las)?\s*\w+",
        r"(?:meta|objetivo|indicador)\s*:\s*\d+"
    ]
    
    for pattern in action_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def check_dimension_when(text: str) -> Tuple[bool, str]:
    """D2: Verifica si especifica plazo/fecha/horizonte temporal verificable."""
    # Primero verificar que NO sean frases vagas
    for pattern in TIME_INDICATORS_INVALID:
        if re.search(pattern, text, re.IGNORECASE):
            # Si hay frase vaga, buscar si también hay plazo concreto
            pass
    
    # Buscar plazos válidos
    for pattern in TIME_INDICATORS_VALID:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return True, match.group(0).strip()
    
    return False, "no_especificado"


def check_dimension_how(text: str) -> Tuple[bool, str]:
    """D3: Verifica si describe mecanismo, pasos o implementación."""
    for pattern in HOW_INDICATORS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 10)
            end = min(len(text), match.end() + 60)
            context = text[start:end].strip()
            return True, context[:120]
    return False, "no_especificado"


def check_dimension_funding(text: str) -> Tuple[bool, str]:
    """D4: Verifica si indica fuente de financiamiento."""
    for pattern in FUNDING_INDICATORS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 10)
            end = min(len(text), match.end() + 60)
            context = text[start:end].strip()
            return True, context[:120]
    return False, "no_especificado"


def check_dimension_compatibility(text: str, pillar_id: str) -> Dict[str, Any]:
    """
    D5: Evalúa compatibilidad normativa y fiscal.
    
    Returns:
        Dict con:
        - normative_fiscal: 1 (compatible) o 0 (conflicto)
        - conflict_type: "constitutional" | "fiscal" | "none"
        - reference: Artículo o norma
        - note: Descripción técnica neutral
    """
    result = {
        "normative_fiscal": 1,
        "conflict_type": "none",
        "reference": "",
        "note": ""
    }
    
    text_lower = text.lower()
    
    # Verificar si menciona reforma legal (exime de conflicto)
    for pattern in REFORM_INDICATORS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return result  # D5 = 1, no hay conflicto si propone reforma
    
    # Verificar conflictos constitucionales
    for conflict_name, conflict_info in CONSTITUTIONAL_CONFLICT_PATTERNS.items():
        for pattern in conflict_info["patterns"]:
            if re.search(pattern, text, re.IGNORECASE):
                result["normative_fiscal"] = 0
                result["conflict_type"] = conflict_info["conflict_type"]
                result["reference"] = conflict_info["reference"]
                result["note"] = f"Potencial conflicto detectado: {conflict_name}"[:240]
                return result
    
    # Verificar conflictos fiscales
    # Solo aplicar si la propuesta implica gasto y NO tiene D4 (funding)
    has_spending_intent = bool(re.search(
        r"(?:aumentar|incrementar|crear|establecer|duplicar|triplicar)\s+(?:el\s+)?(?:gasto|inversión|programa|subsidio|presupuesto)",
        text, re.IGNORECASE
    ))
    
    has_funding_source = bool(re.search(
        r"(?:mediante|con\s+fondos?|financiad|a\s+través\s+de|con\s+recursos?|presupuesto\s+de|reasignación)",
        text, re.IGNORECASE
    ))
    
    if has_spending_intent and not has_funding_source:
        # Verificar si es gasto significativo
        significant_spending = bool(re.search(
            r"(?:millones?|billones?|\d+%\s*del\s*PIB|masivo|universal|todos?\s+los?\s+(?:ciudadanos?|costarricenses?))",
            text, re.IGNORECASE
        ))
        
        if significant_spending:
            result["normative_fiscal"] = 0
            result["conflict_type"] = "fiscal"
            result["reference"] = "Regla fiscal vigente - Déficit fiscal"
            result["note"] = "Propuesta de gasto sin fuente de financiamiento especificada"[:240]
    
    return result


def extract_proposals_from_page(page_num: int, text: str, pdf_id: str) -> List[Dict]:
    """Extrae propuestas de una página."""
    proposals = []
    
    # Dividir texto en párrafos
    paragraphs = re.split(r'\n\s*\n|\.\s+(?=[A-ZÁÉÍÓÚÑ])', text)
    
    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if len(paragraph) < 50:
            continue
        
        # Identificar pilares
        pillars = identify_pillar(paragraph)
        if not pillars:
            continue
        
        # D1: Verificar que sea una propuesta concreta
        is_concrete = check_dimension_existence(paragraph)
        if not is_concrete:
            continue
        
        # D2-D4: Verificar dimensiones
        has_when, when_text = check_dimension_when(paragraph)
        has_how, how_text = check_dimension_how(paragraph)
        has_funding, funding_text = check_dimension_funding(paragraph)
        
        # Crear snippet (máx 240 caracteres)
        snippet = paragraph[:240].strip()
        if len(paragraph) > 240:
            snippet = snippet[:237] + "..."
        
        # Crear título corto
        title = paragraph[:60].strip()
        if len(paragraph) > 60:
            title = title[:57] + "..."
        
        base_proposal_id = f"{pdf_id}_p{page_num}_i{i}"
        
        # Crear propuesta para cada pilar
        for pillar_id in pillars:
            # D5: Compatibilidad normativa y fiscal
            compatibility = check_dimension_compatibility(paragraph, pillar_id)
            
            proposal = {
                "proposal_id": f"{base_proposal_id}_{pillar_id}",
                "candidate_id": pdf_id.lower(),
                "pillar_id": pillar_id,
                "proposal_title": title,
                "proposal_text": paragraph[:500] if len(paragraph) > 500 else paragraph,
                "dimensions": {
                    "existence": 1,
                    "when": 1 if has_when else 0,
                    "how": 1 if has_how else 0,
                    "funding": 1 if has_funding else 0
                },
                "extracted_fields": {
                    "when_text": when_text,
                    "how_text": how_text,
                    "funding_text": funding_text
                },
                "compatibility": compatibility,
                "evidence": {
                    "pdf_id": pdf_id,
                    "page": page_num,
                    "snippet": snippet
                },
                "multi_pillar_source_proposal_id": base_proposal_id if len(pillars) > 1 else None
            }
            proposals.append(proposal)
    
    return proposals


def extract_proposals_from_sections(pages: List[Tuple[int, str]], pdf_id: str) -> List[Dict]:
    """Extrae propuestas de todas las páginas."""
    all_proposals = []
    
    for page_num, text in pages:
        page_proposals = extract_proposals_from_page(page_num, text, pdf_id)
        all_proposals.extend(page_proposals)
    
    return all_proposals


def create_placeholder_proposals(pdf_id: str, existing_pillars: set) -> List[Dict]:
    """Crea propuestas placeholder para pilares sin contenido."""
    placeholders = []
    all_pillar_ids = {p["pillar_id"] for p in PILLARS}
    missing_pillars = all_pillar_ids - existing_pillars
    
    for pillar_id in missing_pillars:
        placeholder = {
            "proposal_id": f"{pdf_id}_placeholder_{pillar_id}",
            "candidate_id": pdf_id.lower(),
            "pillar_id": pillar_id,
            "proposal_title": "No se encontró contenido para este pilar",
            "proposal_text": "No se encontró contenido suficiente para este pilar en el documento",
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
            "compatibility": {
                "normative_fiscal": 1,
                "conflict_type": "none",
                "reference": "",
                "note": ""
            },
            "evidence": {
                "pdf_id": pdf_id,
                "page": 1,
                "snippet": "No se encontró contenido suficiente para este pilar en el documento"
            },
            "multi_pillar_source_proposal_id": None
        }
        placeholders.append(placeholder)
    
    return placeholders


def calculate_candidate_scores(proposals: List[Dict], candidate_id: str) -> Dict:
    """Calcula los puntajes por pilar para un candidato, incluyendo penalizaciones D5."""
    pillar_proposals = defaultdict(list)
    
    for prop in proposals:
        if prop["candidate_id"] == candidate_id:
            pillar_proposals[prop["pillar_id"]].append(prop)
    
    pillar_scores = []
    
    for pillar in PILLARS:
        pillar_id = pillar["pillar_id"]
        weight = pillar["weight"]
        props = pillar_proposals.get(pillar_id, [])
        
        if not props:
            pillar_score = {
                "pillar_id": pillar_id,
                "raw_score": 0,
                "effective_score": 0,
                "normalized": 0.0,
                "weighted": 0.0,
                "dimension_counts": {
                    "existence": 0,
                    "when": 0,
                    "how": 0,
                    "funding": 0
                },
                "penalties": [],
                "evidence_refs": []
            }
        else:
            # Calcular score de cada propuesta
            scored_props = []
            for prop in props:
                dims = prop["dimensions"]
                raw = dims["existence"] + dims["when"] + dims["how"] + dims["funding"]
                scored_props.append((prop, raw, dims["funding"]))
            
            # Ordenar por raw_score, luego por funding
            scored_props.sort(key=lambda x: (x[1], x[2]), reverse=True)
            best_prop, best_raw, _ = scored_props[0]
            
            # Calcular dimension_counts agregados
            dim_counts = {
                "existence": max(p["dimensions"]["existence"] for p in props),
                "when": max(p["dimensions"]["when"] for p in props),
                "how": max(p["dimensions"]["how"] for p in props),
                "funding": max(p["dimensions"]["funding"] for p in props)
            }
            
            # Verificar penalizaciones D5
            penalties = []
            compatibility_conflicts = [
                p for p in props 
                if p["compatibility"]["normative_fiscal"] == 0
            ]
            
            if compatibility_conflicts:
                # Aplicar penalización por conflicto normativo/fiscal
                penalties.append({
                    "type": "compatibility",
                    "value": -1,
                    "reason": f"Conflicto {compatibility_conflicts[0]['compatibility']['conflict_type']}: {compatibility_conflicts[0]['compatibility']['note'][:80]}"
                })
            
            # Calcular effective_score
            total_penalty = sum(p["value"] for p in penalties)
            effective_score = max(0, best_raw + total_penalty)
            
            pillar_score = {
                "pillar_id": pillar_id,
                "raw_score": best_raw,
                "effective_score": effective_score,
                "normalized": effective_score / 4.0,
                "weighted": (effective_score / 4.0) * weight,
                "dimension_counts": dim_counts,
                "penalties": penalties,
                "evidence_refs": [
                    {"proposal_id": p["proposal_id"], "page": p["evidence"]["page"]}
                    for p in props[:5]
                ]
            }
        
        pillar_scores.append(pillar_score)
    
    # Calcular totales
    raw_sum = sum(ps["raw_score"] for ps in pillar_scores)
    effective_sum = sum(ps["effective_score"] for ps in pillar_scores)
    weighted_sum = sum(ps["weighted"] for ps in pillar_scores)
    
    # Pilares críticos: P1, P2, P3, P4, P5, P7
    critical_pillars = {"P1", "P2", "P3", "P4", "P5", "P7"}
    coverage_critical = sum(
        ps["weighted"] for ps in pillar_scores 
        if ps["pillar_id"] in critical_pillars
    )
    
    # Generar notas neutrales
    notes = []
    
    # Notas sobre financiamiento
    low_funding = [ps["pillar_id"] for ps in pillar_scores 
                   if ps["dimension_counts"]["funding"] == 0 and ps["raw_score"] > 0]
    if low_funding:
        notes.append(f"Sin especificaciones de financiamiento en: {', '.join(low_funding)}")
    
    # Notas sobre plazos
    low_when = [ps["pillar_id"] for ps in pillar_scores 
                if ps["dimension_counts"]["when"] == 0 and ps["raw_score"] > 0]
    if low_when:
        notes.append(f"Sin plazos específicos en: {', '.join(low_when)}")
    
    # Notas sobre pilares vacíos
    empty_pillars = [ps["pillar_id"] for ps in pillar_scores if ps["raw_score"] == 0]
    if empty_pillars:
        notes.append(f"Sin propuestas identificadas en: {', '.join(empty_pillars)}")
    
    # Notas sobre penalizaciones
    penalized_pillars = [ps["pillar_id"] for ps in pillar_scores if ps["penalties"]]
    if penalized_pillars:
        notes.append(f"Penalizaciones por compatibilidad en: {', '.join(penalized_pillars)}")
    
    return {
        "candidate_id": candidate_id,
        "pillar_scores": pillar_scores,
        "overall": {
            "raw_sum": raw_sum,
            "effective_sum": effective_sum,
            "weighted_sum": round(weighted_sum, 4),
            "coverage_critical_weighted_sum": round(coverage_critical, 4),
            "notes": " | ".join(notes) if notes else "Propuestas identificadas en todos los pilares"
        }
    }


def generate_ranking(candidate_scores: List[Dict]) -> Dict:
    """Genera el ranking de candidatos."""
    weights = {p["pillar_id"]: p["weight"] for p in PILLARS}
    
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
        "method_version": "v2",
        "weights": weights,
        "ranking_overall_weighted": [
            {"rank": i + 1, "candidate_id": cid, "weighted_sum": ws}
            for i, (cid, ws) in enumerate(ranking_overall)
        ],
        "ranking_critical_weighted": [
            {"rank": i + 1, "candidate_id": cid, "coverage_critical_weighted_sum": ccws}
            for i, (cid, ccws) in enumerate(ranking_critical)
        ]
    }


def process_all_pdfs():
    """Procesa todos los PDFs y genera los archivos JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(PLANES_DIR) if f.endswith('.pdf')]
    
    all_candidates = []
    all_proposals = []
    
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
        candidate_info = extract_candidate_info_from_pdf(pages, pdf_id)
        
        candidate = {
            "candidate_id": pdf_id.lower(),
            "candidate_name": candidate_info["candidate_name"],
            "party_name": candidate_info["party_name"],
            "pdf_id": pdf_id,
            "pdf_title": f"Plan de Gobierno {pdf_id} 2026-2030",
            "pdf_url": f"local://analysis/planes/{pdf_file}"
        }
        all_candidates.append(candidate)
        
        # Extraer propuestas
        proposals = extract_proposals_from_sections(pages, pdf_id)
        print(f"   → {len(proposals)} propuestas identificadas")
        
        # Contar conflictos D5
        conflicts = [p for p in proposals if p["compatibility"]["normative_fiscal"] == 0]
        if conflicts:
            print(f"   → ⚠️  {len(conflicts)} propuestas con conflictos normativos/fiscales")
        
        # Crear placeholders para pilares sin contenido
        existing_pillars = {p["pillar_id"] for p in proposals}
        placeholders = create_placeholder_proposals(pdf_id, existing_pillars)
        proposals.extend(placeholders)
        
        if placeholders:
            print(f"   → {len(placeholders)} pilares sin contenido")
        
        all_proposals.extend(proposals)
    
    print("\n" + "=" * 60)
    print(f"\n📊 RESUMEN GENERAL:")
    print(f"   • Candidatos procesados: {len(all_candidates)}")
    print(f"   • Propuestas totales: {len(all_proposals)}")
    
    # Contar conflictos totales
    total_conflicts = len([p for p in all_proposals if p["compatibility"]["normative_fiscal"] == 0])
    print(f"   • Propuestas con conflictos D5: {total_conflicts}")
    
    # Calcular scores por candidato
    all_candidate_scores = []
    for candidate in all_candidates:
        scores = calculate_candidate_scores(all_proposals, candidate["candidate_id"])
        all_candidate_scores.append(scores)
    
    # Generar ranking
    ranking = generate_ranking(all_candidate_scores)
    
    # Preparar salida final
    output = {
        "candidates.json": all_candidates,
        "pillars.json": PILLARS,
        "proposals.json": all_proposals,
        "candidate_scores.json": all_candidate_scores,
        "ranking.json": ranking
    }
    
    # Guardar archivos individuales
    print("\n📁 Guardando archivos:")
    for filename, data in output.items():
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"   ✅ {filepath}")
    
    # Guardar archivo combinado
    combined_path = os.path.join(DATA_DIR, "all_data.json")
    with open(combined_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"   ✅ {combined_path}")
    
    return output


if __name__ == "__main__":
    print("=" * 60)
    print("PROCESADOR DE PLANES DE GOBIERNO - COSTA RICA 2026-2030")
    print("Versión 2.0 - Con dimensión D5 (Compatibilidad Normativa)")
    print("=" * 60)
    result = process_all_pdfs()
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
