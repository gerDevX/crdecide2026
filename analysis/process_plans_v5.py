#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador de Planes de Gobierno - Costa Rica 2026-2030
Versión 5.0 - Modelo ajustado a realidad CR con penalizaciones fiscales severas

Prioridades:
1. Seguridad ciudadana
2. Salud pública
3. Finanzas públicas (sostenibilidad)
4. Inversión extranjera / Empleo
5. Educación

Penalizaciones severas:
- Flexibilizar regla fiscal: -2 puntos
- Proponer aumento de deuda: -1 punto
- Proponer aumento de impuestos: -1 punto
"""

import fitz
import json
import os
import re
import hashlib
import io
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Optional

# OCR imports (optional, used when text is corrupted)
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️  OCR no disponible. Instala: pip install pytesseract pillow")

# Caracteres que indican texto corrupto (fuentes con encoding incorrecto)
CORRUPT_CHARS = set('ӌǢņĞļšŹĵūÔŤŅƕýðųöĒĽĚÔūŤýĵÔūðŅĽųŤÔļšŹĵūÔŤšŤŅƕýðųŅŤýĒŅŤļÔ')
CORRUPT_THRESHOLD = 0.05  # 5% de caracteres corruptos
TESSERACT_CONFIG = '--oem 3 --psm 6 -l spa'
RENDER_DPI = 200

# ====================================================================
# CONFIGURACIÓN
# ====================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLANES_DIR = os.path.join(BASE_DIR, "planes")
DATA_DIR = os.path.join(BASE_DIR, "data")

# ====================================================================
# 10 PILARES NACIONALES - PESOS AJUSTADOS A REALIDAD CR 2026
# Prioridad: Seguridad > Salud > Finanzas > Reforma Estado > IED/Empleo > Educación
# ====================================================================

PILLARS = [
    {"pillar_id": "P1", "pillar_name": "Sostenibilidad fiscal y finanzas públicas", "weight": 0.14},
    {"pillar_id": "P2", "pillar_name": "Empleo, competitividad e inversión extranjera", "weight": 0.11},
    {"pillar_id": "P3", "pillar_name": "Seguridad ciudadana y justicia", "weight": 0.18},  # 1° MÁXIMA
    {"pillar_id": "P4", "pillar_name": "Salud pública y seguridad social (CCSS)", "weight": 0.16},  # 2° MUY ALTA
    {"pillar_id": "P5", "pillar_name": "Educación y talento humano", "weight": 0.10},  # 7°
    {"pillar_id": "P6", "pillar_name": "Ambiente y desarrollo sostenible", "weight": 0.03},  # 9°
    {"pillar_id": "P7", "pillar_name": "Reforma del Estado y lucha contra la corrupción", "weight": 0.12},  # 4° ALTA (SUBE)
    {"pillar_id": "P8", "pillar_name": "Política social focalizada", "weight": 0.05},  # 8°
    {"pillar_id": "P9", "pillar_name": "Política exterior y comercio internacional", "weight": 0.02},  # 10°
    {"pillar_id": "P10", "pillar_name": "Infraestructura y obra pública", "weight": 0.09},  # 8°
]

# Pesos: P3(18) + P4(16) + P1(14) + P7(12) + P2(11) + P5(10) + P10(9) + P8(5) + P6(3) + P9(2) = 100%

PILLAR_WEIGHTS = {p["pillar_id"]: p["weight"] for p in PILLARS}
PRIORITY_PILLARS = {"P3", "P4", "P1", "P7"}  # Top 4: 60% del peso (Seguridad, Salud, Finanzas, Reforma)
CRITICAL_PILLARS = {"P3", "P4", "P1", "P7", "P2", "P5"}  # Top 6: 81% del peso

# ====================================================================
# PALABRAS CLAVE POR PILAR
# ====================================================================

PILLAR_KEYWORDS = {
    "P1": [
        "fiscal", "tributar", "impuesto", "presupuest", "déficit", "deuda", "hacienda",
        "recaudación", "gasto público", "austeridad", "PIB", "regla fiscal",
        "finanzas públicas", "equilibrio fiscal", "reforma tributaria", "FMI",
        "sostenibilidad", "banco central", "inflación", "estabilidad monetaria"
    ],
    "P2": [
        "empleo", "trabajo", "desempleo", "competitividad", "PYME", "mipyme", "empresa",
        "emprendimiento", "innovación", "productividad", "exportación", "zona franca",
        "inversión extranjera", "IED", "nearshoring", "multinacional", "atracción",
        "salario", "informalidad", "capacitación laboral", "mercado laboral"
    ],
    "P3": [
        "seguridad", "policía", "crimen", "delincuencia", "narcotráfico", "drogas",
        "violencia", "homicidio", "robo", "extorsión", "sicariato", "pandillas",
        "cárcel", "prisión", "justicia", "OIJ", "fuerza pública", "criminalidad",
        "crimen organizado", "lavado de dinero", "armas", "inteligencia policial"
    ],
    "P4": [
        "salud", "CCSS", "Caja Costarricense", "hospital", "clínica", "médic",
        "EBAIS", "lista de espera", "seguridad social", "pensión", "jubilación",
        "IVM", "déficit actuarial", "cotizante", "asegurado", "farmacia"
    ],
    "P5": [
        "educación", "escuela", "colegio", "universidad", "docente", "MEP",
        "deserción escolar", "aprendizaje", "PISA", "educación técnica", "INA",
        "beca", "infraestructura educativa", "calidad educativa", "8% PIB"
    ],
    "P6": [
        "ambiente", "ambiental", "cambio climático", "carbono", "emisiones",
        "renovable", "agua", "bosque", "biodiversidad", "conservación",
        "contaminación", "reciclaje", "residuos", "SINAC", "MINAE"
    ],
    "P7": [
        "reforma del estado", "modernización", "digitalización", "gobierno digital",
        "simplificación", "corrupción", "transparencia", "contraloría", "auditoría",
        "ética", "servidor público", "eficiencia", "burocracia", "trámite"
    ],
    "P8": [
        "pobreza", "vulnerable", "desigualdad", "bono", "subsidio", "IMAS",
        "FODESAF", "programa social", "niñez", "adulto mayor", "discapacidad",
        "vivienda social", "BANHVI", "focalización"
    ],
    "P9": [
        "política exterior", "diplomacia", "comercio internacional", "TLC",
        "exportación", "cooperación internacional", "ONU", "OEA", "SICA",
        "bilateral", "multilateral", "Estados Unidos", "China"
    ],
    "P10": [
        "infraestructura", "carretera", "ruta", "puente", "puerto", "aeropuerto",
        "obra pública", "concesión", "APP", "alianza público-privada", "CONAVI",
        "MOPT", "transporte", "ferrocarril", "tren", "vial", "construcción"
    ]
}

# ====================================================================
# INDICADORES PARA DIMENSIONES D1-D4
# ====================================================================

TIME_INDICATORS_VALID = [
    r"primer(?:o|a)?\s*(?:año|mes|semestre|trimestre)",
    r"primeros?\s*100\s*días",
    r"primeros?\s*\d+\s*(?:años?|meses?|días?)",
    r"20\d{2}[-–]20\d{2}",
    r"cuatrienio",
    r"durante\s*el\s*(?:gobierno|período|cuatrienio)",
    r"al\s*(?:inicio|final)\s*del?\s*gobierno",
]

HOW_INDICATORS = [
    r"mediante\s+(?:la|el|un|una)\s+\w+",
    r"a\s*través\s*de",
    r"proyecto\s*de\s*ley",
    r"decreto\s*ejecutivo",
    r"programa\s+(?:de|para|nacional)",
    r"plan\s*(?:de\s*)?(?:acción|nacional)",
    r"reforma\s+(?:a|de|del|al)",
    r"crear(?:á|emos)?\s+(?:una?|el|la)",
    r"establecer(?:á|emos)?",
    r"implementar(?:á|emos)?",
]

FUNDING_INDICATORS = [
    r"financ(?:iar|iamiento|iado)",
    r"presupuest(?:o|ar|ario)",
    r"recursos?\s*(?:públicos?|del\s+Estado)",
    r"fondos?\s*(?:públicos?|del\s+Estado)",
    r"reasignación",
    r"ahorro\s*(?:fiscal|público)",
    r"eficiencia\s*en\s*el\s*gasto",
    r"cooperación\s*internacional",
    r"APP\b",
    r"alianza\s*público[-\s]?privada",
    r"concesión",
    r"\d+(?:\.\d+)?\s*(?:millones?|billones?)",
    r"\d+(?:[.,]\d+)?%\s*del\s*(?:PIB|presupuesto)",
]

# ====================================================================
# PATRONES DE PENALIZACIÓN D5 - RESPONSABILIDAD FISCAL
# ====================================================================

# PENALIZACIÓN SEVERA: Flexibilizar regla fiscal (-2)
FISCAL_RULE_ATTACK_PATTERNS = [
    r"(?:flexibilizar|reformar|modificar|eliminar|excluir|suspender).*regla\s*fiscal",
    r"regla\s*fiscal.*(?:flexibilizar|reformar|modificar|eliminar|excluir|suspender)",
    r"(?:limita|impide|obstaculiza).*regla\s*fiscal",
    r"regla\s*fiscal.*(?:limita|impide|obstaculiza)",
    r"(?:revisión|revisar).*(?:crítica|profunda).*regla\s*fiscal",
]

# PENALIZACIÓN: Proponer aumento de deuda (-1)
DEBT_INCREASE_PATTERNS = [
    r"(?:aumentar|incrementar|ampliar|expandir)\s*(?:la\s*)?(?:deuda|endeudamiento)",
    r"(?:nuevo|nueva|más)\s*(?:deuda|endeudamiento|crédito\s*público)",
    r"(?:emitir|emisión)\s*(?:de\s*)?(?:bonos?|deuda)",
    r"financiar.*(?:mediante|con)\s*(?:deuda|endeudamiento)",
]

# PENALIZACIÓN: Proponer aumento de impuestos (-1)
TAX_INCREASE_PATTERNS = [
    r"(?:aumentar|incrementar|subir|elevar)\s*(?:los?\s*)?(?:impuestos?|tributos?|cargas?\s*tributarias?)",
    r"(?:nuevo|nueva|nuevos|nuevas)\s*(?:impuestos?|tributos?|cargas?\s*fiscales?)",
    r"(?:crear|creación)\s*(?:de\s*)?(?:impuestos?|tributos?)",
    r"(?:gravar|gravamen)\s*(?:adicional|nuevo)",
    r"(?:reforma\s*tributaria).*(?:progresiv|aumentar|incrementar)",
]

# INDICADORES POSITIVOS (no penalizar)
FISCAL_RESPONSIBILITY_INDICATORS = [
    r"sostenibilidad\s*fiscal",
    r"responsabilidad\s*fiscal",
    r"equilibrio\s*fiscal",
    r"reducir\s*(?:el\s*)?(?:déficit|gasto)",
    r"eficiencia\s*(?:del\s*)?gasto",
    r"austeridad",
    r"respetar.*regla\s*fiscal",
    r"cumplir.*regla\s*fiscal",
    r"mantener.*regla\s*fiscal",
]

# ====================================================================
# FUNCIONES UTILITARIAS
# ====================================================================

def normalize_text(text: str) -> str:
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def generate_proposal_id(pdf_id: str, text: str) -> str:
    hash_input = f"{pdf_id}:{text[:100]}"
    short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
    return f"{pdf_id.lower()}-{short_hash}"

def slugify(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text

# ====================================================================
# EXTRACCIÓN DE PDF CON SOPORTE OCR
# ====================================================================

def detect_corrupt_text(text: str) -> Tuple[bool, float]:
    """Detecta si un texto tiene caracteres de fuentes corruptas."""
    if not text:
        return False, 0.0
    total_chars = len(text)
    corrupt_count = sum(1 for char in text if char in CORRUPT_CHARS)
    corrupt_ratio = corrupt_count / total_chars if total_chars > 0 else 0
    return corrupt_ratio > CORRUPT_THRESHOLD, corrupt_ratio


def extract_page_with_ocr(page, dpi: int = RENDER_DPI) -> str:
    """Extrae texto de una página usando OCR."""
    if not OCR_AVAILABLE:
        return ""
    try:
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)
        return text
    except Exception as e:
        print(f"    ⚠️  Error OCR en página: {e}")
        return ""


def extract_text_from_pdf(pdf_path: str) -> Tuple[List[Tuple[int, str]], str]:
    """
    Extrae texto de un PDF, retorna páginas y texto completo.
    Detecta automáticamente texto corrupto y usa OCR cuando es necesario.
    """
    pages = []
    full_text = ""
    ocr_pages = 0
    doc = None
    
    try:
        doc = fitz.open(pdf_path)
        pdf_name = os.path.basename(pdf_path)
        num_pages = len(doc)
        
        # Primera pasada: detectar si hay texto corrupto (muestra de primeras 10 páginas)
        sample_text = ""
        for page_num in range(min(10, num_pages)):
            sample_text += doc[page_num].get_text()
        
        is_corrupt, ratio = detect_corrupt_text(sample_text)
        use_ocr = is_corrupt and OCR_AVAILABLE
        
        if is_corrupt:
            if OCR_AVAILABLE:
                print(f"  ⚠️  {pdf_name}: Texto corrupto ({ratio*100:.1f}%), usando OCR...")
            else:
                print(f"  ⚠️  {pdf_name}: Texto corrupto ({ratio*100:.1f}%) pero OCR no disponible")
        
        # Segunda pasada: extraer texto
        for page_num in range(num_pages):
            page = doc[page_num]
            
            if use_ocr:
                # Usar OCR para esta página
                text = extract_page_with_ocr(page)
                ocr_pages += 1
            else:
                # Extracción directa
                text = page.get_text()
                # Verificar si esta página específica tiene problemas
                page_corrupt, _ = detect_corrupt_text(text)
                if page_corrupt and OCR_AVAILABLE:
                    text = extract_page_with_ocr(page)
                    ocr_pages += 1
            
            normalized = normalize_text(text)
            if normalized:
                pages.append((page_num + 1, normalized))
                full_text += " " + normalized
        
        if ocr_pages > 0:
            print(f"  ✅ OCR completado: {ocr_pages}/{num_pages} páginas procesadas")
            
    except Exception as e:
        print(f"Error leyendo {pdf_path}: {e}")
    finally:
        if doc:
            doc.close()
    
    return pages, full_text

def extract_candidate_info(pages: List[Tuple[int, str]], pdf_id: str) -> Dict[str, str]:
    """Extrae información del candidato."""
    first_pages_text = " ".join([text for _, text in pages[:5]])
    
    candidate_name = "no_especificado"
    party_name = "no_especificado"
    
    patterns = [
        r"candidat[oa].*?presidencia[:\s]+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,4})",
        r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})\s+(?:para\s+)?[Pp]residente",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, first_pages_text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name) > 5 and len(name.split()) >= 2:
                candidate_name = name
                break
    
    party_patterns = [
        r"[Pp]artido\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-Za-záéíóúñ]+){0,4})",
        r"[Cc]oalición\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-Za-záéíóúñ]+){0,4})",
        r"[Ff]rente\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-Za-záéíóúñ]+){0,4})",
    ]
    
    for pattern in party_patterns:
        match = re.search(pattern, first_pages_text)
        if match:
            party = match.group(0).strip()[:60]
            party_name = party
            break
    
    return {"candidate_name": candidate_name, "party_name": party_name}

# ====================================================================
# EVALUACIÓN DE DIMENSIONES
# ====================================================================

def identify_primary_pillar(text: str) -> Optional[str]:
    text_lower = text.lower()
    scores = {}
    
    for pillar_id, keywords in PILLAR_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score >= 2:
            scores[pillar_id] = score
    
    if not scores:
        return None
    return max(scores, key=scores.get)

def check_existence(text: str) -> bool:
    patterns = [
        r"(?:crear|establecer|implementar|desarrollar|reformar|construir|ampliar)(?:á|emos)?",
        r"(?:programa|proyecto|plan|estrategia|política)\s+(?:de|para|nacional)",
        r"(?:ley|decreto|reglamento)",
        r"(?:invertir|destinar|asignar)\s+(?:recursos?|fondos?)",
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def check_when(text: str) -> Tuple[bool, str]:
    for pattern in TIME_INDICATORS_VALID:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return True, match.group(0).strip()
    return False, "no_especificado"

def check_how(text: str) -> Tuple[bool, str]:
    for pattern in HOW_INDICATORS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 10)
            end = min(len(text), match.end() + 50)
            return True, text[start:end].strip()[:100]
    return False, "no_especificado"

def check_funding(text: str) -> Tuple[bool, str]:
    for pattern in FUNDING_INDICATORS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 10)
            end = min(len(text), match.end() + 50)
            return True, text[start:end].strip()[:100]
    return False, "no_especificado"

# ====================================================================
# PENALIZACIONES D5 - RESPONSABILIDAD FISCAL
# ====================================================================

def analyze_fiscal_responsibility(full_text: str) -> Dict:
    """
    Analiza la posición fiscal del candidato.
    Retorna penalizaciones y análisis detallado.
    """
    text_lower = full_text.lower()
    
    analysis = {
        "penalties": [],
        "flags": {
            "attacks_fiscal_rule": False,
            "proposes_debt_increase": False,
            "proposes_tax_increase": False,
            "shows_fiscal_responsibility": False,
        },
        "evidence": [],
        "total_penalty": 0
    }
    
    # Verificar indicadores de responsabilidad fiscal (exime de algunas penalizaciones)
    for pattern in FISCAL_RESPONSIBILITY_INDICATORS:
        if re.search(pattern, text_lower):
            analysis["flags"]["shows_fiscal_responsibility"] = True
            break
    
    # PENALIZACIÓN SEVERA: Atacar regla fiscal (-2)
    for pattern in FISCAL_RULE_ATTACK_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            analysis["flags"]["attacks_fiscal_rule"] = True
            # Extraer contexto
            start = max(0, match.start() - 50)
            end = min(len(text_lower), match.end() + 100)
            evidence = full_text[start:end].strip()[:200]
            
            analysis["penalties"].append({
                "type": "attacks_fiscal_rule",
                "value": -2,
                "reason": "Propone flexibilizar/reformar la regla fiscal",
                "evidence": evidence
            })
            analysis["evidence"].append(evidence)
            break  # Solo una vez
    
    # PENALIZACIÓN: Proponer aumento de deuda (-1)
    for pattern in DEBT_INCREASE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            analysis["flags"]["proposes_debt_increase"] = True
            start = max(0, match.start() - 50)
            end = min(len(text_lower), match.end() + 100)
            evidence = full_text[start:end].strip()[:200]
            
            analysis["penalties"].append({
                "type": "proposes_debt_increase",
                "value": -1,
                "reason": "Propone aumentar deuda pública",
                "evidence": evidence
            })
            analysis["evidence"].append(evidence)
            break
    
    # PENALIZACIÓN: Proponer aumento de impuestos (-1)
    for pattern in TAX_INCREASE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            analysis["flags"]["proposes_tax_increase"] = True
            start = max(0, match.start() - 50)
            end = min(len(text_lower), match.end() + 100)
            evidence = full_text[start:end].strip()[:200]
            
            analysis["penalties"].append({
                "type": "proposes_tax_increase",
                "value": -1,
                "reason": "Propone aumentar impuestos al pueblo",
                "evidence": evidence
            })
            analysis["evidence"].append(evidence)
            break
    
    analysis["total_penalty"] = sum(p["value"] for p in analysis["penalties"])
    
    return analysis

def check_urgency_omission(full_text: str, pillar_id: str) -> List[Dict]:
    """Verifica si omite urgencias nacionales para un pilar específico."""
    penalties = []
    text_lower = full_text.lower()
    
    urgency_requirements = {
        "P3": {  # Seguridad
            "required_terms": ["policía", "fuerza pública", "OIJ", "inteligencia", "operativ"],
            "penalty_reason": "No propone medidas operativas de seguridad"
        },
        "P2": {  # Empleo/IED
            "required_terms": ["inversión extranjera", "zona franca", "IED", "nearshoring", "multinacional"],
            "penalty_reason": "No menciona inversión extranjera como generador de empleo"
        },
        "P10": {  # Infraestructura
            "required_terms": ["APP", "concesión", "alianza público", "inversión privada"],
            "penalty_reason": "No propone mecanismos privados de financiamiento para infraestructura"
        }
    }
    
    if pillar_id not in urgency_requirements:
        return penalties
    
    req = urgency_requirements[pillar_id]
    found = any(term.lower() in text_lower for term in req["required_terms"])
    
    if not found:
        penalties.append({
            "type": "urgency_omission",
            "value": -1,
            "reason": req["penalty_reason"]
        })
    
    return penalties

# ====================================================================
# EXTRACCIÓN DE PROPUESTAS
# ====================================================================

def extract_best_proposal_per_pillar(pages: List[Tuple[int, str]], pdf_id: str) -> Dict[str, Dict]:
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
            
            is_concrete = check_existence(paragraph)
            if not is_concrete:
                continue
            
            has_when, when_text = check_when(paragraph)
            has_how, how_text = check_how(paragraph)
            has_funding, funding_text = check_funding(paragraph)
            
            dimensions = {
                "existence": 1,
                "when": 1 if has_when else 0,
                "how": 1 if has_how else 0,
                "funding": 1 if has_funding else 0
            }
            
            raw_score = sum(dimensions.values())
            snippet = paragraph[:237] + "…" if len(paragraph) > 240 else paragraph
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
    
    best_by_pillar = {}
    for pillar_id, proposals in candidates_by_pillar.items():
        proposals.sort(key=lambda p: (p["raw_score"], p["dimensions"]["funding"]), reverse=True)
        best_by_pillar[pillar_id] = proposals[0]
    
    return best_by_pillar

def create_proposals_json(best_by_pillar: Dict[str, Dict], candidate_id: str, pdf_id: str) -> List[Dict]:
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
                }
            }
        else:
            proposal = {
                "proposal_id": generate_proposal_id(pdf_id, f"placeholder_{pillar_id}"),
                "candidate_id": candidate_id,
                "pillar_id": pillar_id,
                "proposal_title": "Sin propuesta identificada para este pilar",
                "proposal_text": "El documento no contiene propuestas concretas para este pilar.",
                "dimensions": {"existence": 0, "when": 0, "how": 0, "funding": 0},
                "extracted_fields": {
                    "when_text": "no_especificado",
                    "how_text": "no_especificado",
                    "funding_text": "no_especificado"
                },
                "evidence": {"pdf_id": pdf_id, "page": 1, "snippet": "Sin contenido para este pilar."}
            }
        
        proposals.append(proposal)
    
    return proposals

# ====================================================================
# SCORING CON PENALIZACIONES FISCALES
# ====================================================================

def calculate_candidate_score(proposals: List[Dict], candidate_id: str, full_text: str, fiscal_analysis: Dict) -> Dict:
    """Calcula scores con penalizaciones D5 fiscales."""
    
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
        
        # Penalizaciones específicas del pilar
        pillar_penalties = check_urgency_omission(full_text, pillar_id)
        
        # Aplicar penalizaciones fiscales globales a P1
        if pillar_id == "P1":
            pillar_penalties.extend(fiscal_analysis["penalties"])
        
        # Calcular effective_score (mínimo 0)
        total_penalty = sum(p["value"] for p in pillar_penalties)
        effective_score = max(0, raw_score + total_penalty)
        
        normalized = effective_score / 4.0
        weighted = normalized * weight
        
        pillar_scores.append({
            "pillar_id": pillar_id,
            "raw_score": raw_score,
            "effective_score": effective_score,
            "normalized": round(normalized, 4),
            "weighted": round(weighted, 4),
            "penalties": pillar_penalties
        })
    
    # Totales
    raw_sum = sum(ps["raw_score"] for ps in pillar_scores)
    effective_sum = sum(ps["effective_score"] for ps in pillar_scores)
    weighted_sum = sum(ps["weighted"] for ps in pillar_scores)
    
    # Coverage de pilares prioritarios (P1-P5)
    priority_weighted = sum(
        ps["weighted"] for ps in pillar_scores
        if ps["pillar_id"] in PRIORITY_PILLARS
    )
    
    # Coverage de pilares críticos (incluye P10)
    critical_weighted = sum(
        ps["weighted"] for ps in pillar_scores
        if ps["pillar_id"] in CRITICAL_PILLARS
    )
    
    # Notas
    notes = []
    
    # Notas sobre penalizaciones fiscales
    if fiscal_analysis["flags"]["attacks_fiscal_rule"]:
        notes.append("⚠️ ATACA REGLA FISCAL (-2)")
    if fiscal_analysis["flags"]["proposes_debt_increase"]:
        notes.append("⚠️ PROPONE MÁS DEUDA (-1)")
    if fiscal_analysis["flags"]["proposes_tax_increase"]:
        notes.append("⚠️ PROPONE MÁS IMPUESTOS (-1)")
    if fiscal_analysis["flags"]["shows_fiscal_responsibility"]:
        notes.append("✅ Muestra responsabilidad fiscal")
    
    penalized = [ps["pillar_id"] for ps in pillar_scores if ps["penalties"] and ps["pillar_id"] != "P1"]
    if penalized:
        notes.append(f"Penalizados: {', '.join(penalized)}")
    
    empty = [ps["pillar_id"] for ps in pillar_scores if ps["raw_score"] == 0]
    if empty:
        notes.append(f"Sin propuestas: {', '.join(empty)}")
    
    return {
        "candidate_id": candidate_id,
        "pillar_scores": pillar_scores,
        "fiscal_analysis": {
            "flags": fiscal_analysis["flags"],
            "total_penalty": fiscal_analysis["total_penalty"],
            "evidence": fiscal_analysis["evidence"][:2]  # Solo 2 evidencias
        },
        "overall": {
            "raw_sum": raw_sum,
            "effective_sum": effective_sum,
            "weighted_sum": round(weighted_sum, 4),
            "priority_weighted_sum": round(priority_weighted, 4),
            "critical_weighted_sum": round(critical_weighted, 4),
            "fiscal_penalty_applied": fiscal_analysis["total_penalty"],
            "notes": " | ".join(notes) if notes else ""
        }
    }

# ====================================================================
# ANÁLISIS DETALLADO POR CANDIDATO
# ====================================================================

def analyze_candidate_detailed(pages: List[Tuple[int, str]], full_text: str, pdf_id: str, fiscal_analysis: Dict) -> Dict:
    """Genera análisis detallado de coherencia."""
    
    text_lower = full_text.lower()
    
    analysis = {
        "pdf_id": pdf_id,
        "total_pages": len(pages),
        "fiscal_responsibility": fiscal_analysis["flags"],
        "fiscal_evidence": fiscal_analysis["evidence"],
        "urgency_coverage": {},
        "strengths": [],
        "weaknesses": [],
        "risk_level": "BAJO"
    }
    
    # Análisis de cobertura de urgencias
    urgencies = {
        "seguridad_operativa": {
            "terms": ["policía", "fuerza pública", "OIJ", "inteligencia", "patrullaje", "operativo"],
            "found": []
        },
        "salud_ccss": {
            "terms": ["CCSS", "hospital", "lista de espera", "EBAIS", "seguridad social"],
            "found": []
        },
        "inversion_extranjera": {
            "terms": ["inversión extranjera", "zona franca", "IED", "nearshoring", "multinacional"],
            "found": []
        },
        "empleo": {
            "terms": ["empleo", "desempleo", "trabajo", "informalidad", "capacitación"],
            "found": []
        },
        "educacion": {
            "terms": ["educación", "MEP", "deserción", "calidad educativa", "docente"],
            "found": []
        },
        "infraestructura_APP": {
            "terms": ["APP", "alianza público-privada", "concesión", "inversión privada"],
            "found": []
        },
        "crimen_organizado": {
            "terms": ["crimen organizado", "narcotráfico", "sicariato", "extorsión", "lavado"],
            "found": []
        }
    }
    
    for key, data in urgencies.items():
        for term in data["terms"]:
            count = text_lower.count(term.lower())
            if count > 0:
                data["found"].append(f"{term} ({count})")
        
        analysis["urgency_coverage"][key] = {
            "covered": len(data["found"]) > 0,
            "mentions": data["found"]
        }
    
    # Determinar fortalezas y debilidades
    if analysis["urgency_coverage"]["seguridad_operativa"]["covered"]:
        analysis["strengths"].append("Aborda seguridad con enfoque operativo")
    else:
        analysis["weaknesses"].append("No propone medidas operativas de seguridad")
    
    if analysis["urgency_coverage"]["salud_ccss"]["covered"]:
        analysis["strengths"].append("Aborda salud y CCSS")
    else:
        analysis["weaknesses"].append("No aborda salud/CCSS explícitamente")
    
    if analysis["urgency_coverage"]["inversion_extranjera"]["covered"]:
        analysis["strengths"].append("Considera inversión extranjera para empleo")
    else:
        analysis["weaknesses"].append("Omite inversión extranjera como motor de empleo")
    
    if analysis["urgency_coverage"]["infraestructura_APP"]["covered"]:
        analysis["strengths"].append("Propone APP para infraestructura")
    else:
        analysis["weaknesses"].append("No propone mecanismos privados para infraestructura")
    
    # Riesgo fiscal
    risk_score = 0
    if fiscal_analysis["flags"]["attacks_fiscal_rule"]:
        analysis["weaknesses"].append("🔴 ATACA REGLA FISCAL - Riesgo alto para finanzas públicas")
        risk_score += 3
    if fiscal_analysis["flags"]["proposes_debt_increase"]:
        analysis["weaknesses"].append("🟠 Propone aumentar deuda pública")
        risk_score += 2
    if fiscal_analysis["flags"]["proposes_tax_increase"]:
        analysis["weaknesses"].append("🟠 Propone aumentar impuestos al pueblo")
        risk_score += 2
    
    if fiscal_analysis["flags"]["shows_fiscal_responsibility"]:
        analysis["strengths"].append("✅ Demuestra responsabilidad fiscal")
        risk_score -= 1
    
    if risk_score >= 3:
        analysis["risk_level"] = "ALTO"
    elif risk_score >= 1:
        analysis["risk_level"] = "MEDIO"
    else:
        analysis["risk_level"] = "BAJO"
    
    return analysis

# ====================================================================
# RANKING
# ====================================================================

def generate_ranking(candidate_scores: List[Dict]) -> Dict:
    ranking_overall = sorted(
        [(cs["candidate_id"], cs["overall"]["weighted_sum"], cs["overall"]["fiscal_penalty_applied"]) 
         for cs in candidate_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    ranking_priority = sorted(
        [(cs["candidate_id"], cs["overall"]["priority_weighted_sum"]) for cs in candidate_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    ranking_critical = sorted(
        [(cs["candidate_id"], cs["overall"]["critical_weighted_sum"]) for cs in candidate_scores],
        key=lambda x: x[1],
        reverse=True
    )
    
    return {
        "method_version": "v5_fiscal_strict",
        "weights": PILLAR_WEIGHTS,
        "priority_pillars": list(PRIORITY_PILLARS),
        "critical_pillars": list(CRITICAL_PILLARS),
        "penalties_applied": {
            "attacks_fiscal_rule": -2,
            "proposes_debt_increase": -1,
            "proposes_tax_increase": -1
        },
        "ranking_overall_weighted": [
            {
                "rank": i + 1, 
                "candidate_id": cid, 
                "weighted_sum": ws,
                "fiscal_penalty": fp
            }
            for i, (cid, ws, fp) in enumerate(ranking_overall)
        ],
        "ranking_priority_weighted": [
            {"rank": i + 1, "candidate_id": cid, "priority_weighted_sum": pws}
            for i, (cid, pws) in enumerate(ranking_priority)
        ],
        "ranking_critical_weighted": [
            {"rank": i + 1, "candidate_id": cid, "critical_weighted_sum": ccws}
            for i, (cid, ccws) in enumerate(ranking_critical)
        ]
    }

# ====================================================================
# PROCESAMIENTO PRINCIPAL
# ====================================================================

def load_existing_candidates() -> Dict[str, str]:
    """Carga el archivo candidates.json existente y retorna un mapeo pdf_id -> candidate_id"""
    candidates_file = os.path.join(DATA_DIR, "candidates.json")
    if os.path.exists(candidates_file):
        with open(candidates_file, 'r', encoding='utf-8') as f:
            candidates = json.load(f)
            return {c["pdf_id"]: c["candidate_id"] for c in candidates}
    return {}

def process_all_pdfs():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Cargar mapeo de candidate_id existente
    existing_candidates = load_existing_candidates()
    print(f"📋 Cargados {len(existing_candidates)} candidate_ids del archivo existente")
    
    pdf_files = [f for f in os.listdir(PLANES_DIR) if f.endswith('.pdf')]
    
    all_candidates = []
    all_proposals = []
    all_scores = []
    all_analysis = []
    
    print(f"Procesando {len(pdf_files)} planes de gobierno...")
    print("Modelo: v5 RESPONSABILIDAD FISCAL (10 pilares + penalizaciones severas)")
    print("=" * 75)
    print("Penalizaciones:")
    print("  • Atacar regla fiscal: -2 puntos")
    print("  • Proponer más deuda:  -1 punto")
    print("  • Proponer más impuestos: -1 punto")
    print("=" * 75)
    
    for pdf_file in sorted(pdf_files):
        pdf_id = pdf_file.replace('.pdf', '')
        pdf_path = os.path.join(PLANES_DIR, pdf_file)
        
        print(f"\n📄 {pdf_id}...")
        
        pages, full_text = extract_text_from_pdf(pdf_path)
        
        if not pages:
            print(f"   ⚠️ No se pudo extraer texto")
            continue
        
        info = extract_candidate_info(pages, pdf_id)
        
        # Usar candidate_id del archivo existente si está disponible
        if pdf_id in existing_candidates:
            candidate_id = existing_candidates[pdf_id]
        elif info["candidate_name"] != "no_especificado":
            candidate_id = slugify(info["candidate_name"])
        else:
            candidate_id = pdf_id.lower()
        
        candidate = {
            "candidate_id": candidate_id,
            "candidate_name": info["candidate_name"],
            "party_name": info["party_name"],
            "pdf_id": pdf_id,
            "pdf_title": f"Plan de Gobierno {pdf_id} 2026-2030",
            "pdf_url": "no_especificado"
        }
        all_candidates.append(candidate)
        
        # Análisis fiscal
        fiscal_analysis = analyze_fiscal_responsibility(full_text)
        
        # Extraer propuestas
        best_by_pillar = extract_best_proposal_per_pillar(pages, pdf_id)
        proposals = create_proposals_json(best_by_pillar, candidate_id, pdf_id)
        all_proposals.extend(proposals)
        
        # Calcular scores con penalizaciones
        scores = calculate_candidate_score(proposals, candidate_id, full_text, fiscal_analysis)
        all_scores.append(scores)
        
        # Análisis detallado
        analysis = analyze_candidate_detailed(pages, full_text, pdf_id, fiscal_analysis)
        analysis["candidate_id"] = candidate_id
        all_analysis.append(analysis)
        
        # Resumen
        fiscal_flags = []
        if fiscal_analysis["flags"]["attacks_fiscal_rule"]:
            fiscal_flags.append("⚠️ REGLA")
        if fiscal_analysis["flags"]["proposes_debt_increase"]:
            fiscal_flags.append("💰 DEUDA")
        if fiscal_analysis["flags"]["proposes_tax_increase"]:
            fiscal_flags.append("📈 IMPUESTOS")
        
        fiscal_str = " | ".join(fiscal_flags) if fiscal_flags else "✅ Sin riesgo fiscal"
        
        print(f"   → Págs: {len(pages)} | Pilares: {len(best_by_pillar)}/10")
        print(f"   → Score: {scores['overall']['weighted_sum']:.1%} (raw: {scores['overall']['raw_sum']}/40)")
        print(f"   → Fiscal: {fiscal_str} (penalización: {fiscal_analysis['total_penalty']})")
    
    # Generar ranking
    ranking = generate_ranking(all_scores)
    
    print("\n" + "=" * 75)
    print("📊 RANKING FINAL - MODELO v5 RESPONSABILIDAD FISCAL")
    print("=" * 75)
    print(f"{'#':<3} {'PARTIDO':<15} {'SCORE':<10} {'PENALIZACIÓN':<15} {'RIESGO'}")
    print("-" * 75)
    
    for entry in ranking["ranking_overall_weighted"]:
        # Buscar análisis para obtener nivel de riesgo
        analysis = next((a for a in all_analysis if a["candidate_id"] == entry["candidate_id"]), None)
        risk = analysis["risk_level"] if analysis else "?"
        risk_emoji = {"ALTO": "🔴", "MEDIO": "🟠", "BAJO": "🟢"}.get(risk, "⚪")
        
        print(f"{entry['rank']:<3} {entry['candidate_id']:<15} {entry['weighted_sum']:.1%}      {entry['fiscal_penalty']:<15} {risk_emoji} {risk}")
    
    # Guardar archivos
    print("\n📁 Guardando archivos...")
    print("   ⚠️  candidates.json NO se regenera (mantener datos manuales)")
    
    outputs = {
        # "candidates.json": all_candidates,  # EXCLUIDO: se mantiene el archivo manual
        "pillars.json": PILLARS,
        "proposals.json": all_proposals,
        "candidate_scores.json": all_scores,
        "ranking.json": ranking,
        "detailed_analysis.json": all_analysis
    }
    
    for filename, data in outputs.items():
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"   ✅ {filename}")
    
    return outputs

if __name__ == "__main__":
    print("=" * 75)
    print("PROCESADOR DE PLANES v5.0 - RESPONSABILIDAD FISCAL")
    print("10 pilares | Penalizaciones severas por irresponsabilidad fiscal")
    print("Prioridad: Seguridad > Salud > Finanzas > IED/Empleo > Educación")
    print("=" * 75)
    result = process_all_pdfs()
    print("\n✅ PROCESO COMPLETADO")
