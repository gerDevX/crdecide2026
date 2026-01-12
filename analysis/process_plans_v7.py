#!/usr/bin/env python3
"""
PROCESADOR DE PLANES v7.0 - NEUTRAL + ESTRICTO + BONOS + VIABILIDAD LEGAL (AMPLIADA)

Cambios desde v6:
1. MANTENIDO: Todo el sistema v6 (neutral + estricto)
2. AGREGADO: Sistema de bonos por múltiples propuestas:
   - Extrae hasta 3 propuestas válidas por pilar (score >= 2)
   - Bono +1.0 si tiene 3+ propuestas válidas por pilar
   - Bono +0.25 por cada propuesta completa (E+W+H+F = 4/4)
   - Bono +0.1 por cada propuesta con financiamiento (score >= 3)
3. AGREGADO: Verificación de viabilidad legal (Fase 1 Ampliada):
   - Viola separación de poderes: -1.0
   - Viola derechos fundamentales: -1.0
   - Viola garantías constitucionales: -1.0
   - Viola procedimientos constitucionales: -0.5
   - NOTA: NO se penaliza reforma constitucional (puede ser legítima y necesaria)
4. MEJORADO: Cobertura de propuestas (hasta 30 propuestas por candidato)

Este sistema es:
- NEUTRAL: No penaliza posiciones ideológicas legítimas ni reformas constitucionales legítimas
- ESTRICTO: Penaliza omitir urgencias críticas del país
- PREMIADOR: Premia planes detallados con múltiples propuestas
- VIABLE: Verifica violaciones objetivas de la Constitución (separación de poderes, derechos, garantías, procedimientos)
- OBJETIVO: Basado en ley vigente y necesidades nacionales
"""

import os
import re
import json
import hashlib
import io
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

# ====================================================================
# CONFIGURACIÓN OCR (heredada de v5)
# ====================================================================

try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ PyMuPDF no disponible. Instalar: pip install PyMuPDF")

# Verificar disponibilidad de pdfplumber (mejor para PDFs corruptos)
PDFPLUMBER_AVAILABLE = False
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    pass  # pdfplumber es opcional pero recomendado

# Verificar disponibilidad de motores OCR
OCR_AVAILABLE = False
EASYOCR_AVAILABLE = False
TESSERACT_AVAILABLE = False

try:
    from PIL import Image
    import numpy as np
    OCR_AVAILABLE = True
except ImportError:
    print("⚠️ PIL/Pillow no disponible. Instalar: pip install Pillow")

try:
    import easyocr
    EASYOCR_AVAILABLE = True
    OCR_AVAILABLE = True
except ImportError:
    print("⚠️ EasyOCR no disponible. Instalar: pip install easyocr")

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
    if not OCR_AVAILABLE:
        OCR_AVAILABLE = True
except ImportError:
    print("⚠️ Tesseract no disponible. Instalar: pip install pytesseract")

# Configuración OCR
RENDER_DPI = 300  # Aumentado para mejor calidad
TESSERACT_CONFIG = '--oem 3 --psm 6 -l spa'  # Configuración optimizada

# Caracteres de fuentes corruptas (ampliado para detectar más casos)
CORRUPT_CHARS = set([
    # Unicode privado (fuentes corruptas comunes)
    '\uf0b7', '\uf0a7', '\uf0d8', '\uf020', '\uf06c', '\uf06f', '\uf073',
    '\uf061', '\uf065', '\uf06e', '\uf072', '\uf074', '\uf075', '\uf069',
    '\uf064', '\uf063', '\uf06d', '\uf070', '\uf067', '\uf0fc', '\uf0e0',
    # Caracteres cirílicos/extraños que aparecen en PDFs corruptos
    'ӌ', 'Ǣ', 'ņ', 'Ğ', 'ļ', 'š', 'Ź', 'ĵ', 'ū', 'Ô', 'Ť', 'Ņ', 'ƕ', 'ý', 'ð', 'ų', 'ö', 'Ē', 'Ľ', 'Ě',
    'Ņ', 'Ť', 'Ź', 'Ľ', 'Ť', 'Ņ', 'ƕ', 'ý', 'ð', 'ų', 'ö', 'Ē', 'Ľ', 'Ě',
])
CORRUPT_THRESHOLD = 0.02  # 2% de caracteres corruptos

# Rutas
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLANES_DIR = os.path.join(SCRIPT_DIR, "planes")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

# ====================================================================
# PILARES NACIONALES (10 pilares)
# ====================================================================

PILLARS = [
    {"pillar_id": "P1", "pillar_name": "Responsabilidad Fiscal", "weight": 0.14},
    {"pillar_id": "P2", "pillar_name": "Empleo e Inversión", "weight": 0.11},
    {"pillar_id": "P3", "pillar_name": "Seguridad Ciudadana", "weight": 0.18},
    {"pillar_id": "P4", "pillar_name": "Salud y CCSS", "weight": 0.16},
    {"pillar_id": "P5", "pillar_name": "Educación", "weight": 0.10},
    {"pillar_id": "P6", "pillar_name": "Ambiente y Sostenibilidad", "weight": 0.03},
    {"pillar_id": "P7", "pillar_name": "Reforma del Estado", "weight": 0.12},
    {"pillar_id": "P8", "pillar_name": "Pobreza y Vulnerabilidad", "weight": 0.05},
    {"pillar_id": "P9", "pillar_name": "Política Exterior", "weight": 0.02},
    {"pillar_id": "P10", "pillar_name": "Infraestructura", "weight": 0.09},
]

PILLAR_WEIGHTS = {p["pillar_id"]: p["weight"] for p in PILLARS}

# Pilares prioritarios (urgencia nacional 2026)
PRIORITY_PILLARS = {"P3", "P4", "P1", "P7"}  # Seguridad, Salud, Fiscal, Reforma

# Pilares críticos (incluye empleo y educación)
CRITICAL_PILLARS = {"P3", "P4", "P1", "P7", "P2", "P5"}

# ====================================================================
# KEYWORDS POR PILAR
# ====================================================================

PILLAR_KEYWORDS = {
    "P1": [
        "fiscal", "presupuesto", "deuda", "déficit", "regla fiscal", "gasto público",
        "Hacienda", "finanzas", "tributario", "austeridad", "eficiencia",
        "racionalización", "consolidación fiscal", "sostenibilidad", "reforma tributaria"
    ],
    "P2": [
        "empleo", "trabajo", "desempleo", "informalidad", "PYME", "inversión extranjera",
        "zona franca", "nearshoring", "competitividad", "IED", "exportación",
        "productividad", "capacitación laboral", "salario", "formalización"
    ],
    "P3": [
        "seguridad", "crimen", "narcotráfico", "policía", "fuerza pública", "OIJ",
        "violencia", "homicidio", "robo", "hurto", "extorsión", "sicariato",
        "cárcel", "prisión", "delito", "penitenciario", "vigilancia", "inteligencia"
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
# PENALIZACIONES v6 - NEUTRAL + ESTRICTO
# ====================================================================

# PENALIZACIÓN FISCAL SEVERA: Flexibilizar regla fiscal (-2)
# Objetivo: basado en Ley 9635 vigente
FISCAL_RULE_ATTACK_PATTERNS = [
    r"(?:flexibilizar|reformar|modificar|eliminar|excluir|suspender).*regla\s*fiscal",
    r"regla\s*fiscal.*(?:flexibilizar|reformar|modificar|eliminar|excluir|suspender)",
    r"(?:limita|impide|obstaculiza).*regla\s*fiscal",
    r"regla\s*fiscal.*(?:limita|impide|obstaculiza)",
    r"(?:revisión|revisar).*(?:crítica|profunda).*regla\s*fiscal",
]

# PENALIZACIÓN FISCAL: Proponer aumento de deuda (-1)
DEBT_INCREASE_PATTERNS = [
    r"(?:aumentar|incrementar|ampliar|expandir)\s*(?:la\s*)?(?:deuda|endeudamiento)",
    r"(?:nuevo|nueva|más)\s*(?:deuda|endeudamiento|crédito\s*público)",
    r"(?:emitir|emisión)\s*(?:de\s*)?(?:bonos?|deuda)",
    r"financiar.*(?:mediante|con)\s*(?:deuda|endeudamiento)",
]

# NOTA v6: ELIMINADO - proponer impuestos NO se penaliza (es posición ideológica legítima)
# TAX_INCREASE_PATTERNS = [...]  # REMOVIDO

# INDICADORES POSITIVOS (mitigan riesgo)
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
# URGENCIAS NACIONALES v6 - CRITERIOS DE OMISIÓN
# ====================================================================

# Términos que indican que el candidato aborda la urgencia
URGENCY_TERMS = {
    "security_operations": {
        "terms": ["policía", "fuerza pública", "OIJ", "inteligencia", "patrullaje", 
                  "operativo", "vigilancia", "control territorial"],
        "description": "Seguridad operativa",
        "penalty": -1
    },
    "ccss_crisis": {
        "terms": ["CCSS", "Caja Costarricense", "déficit actuarial", "listas de espera", 
                  "IVM", "régimen de pensiones", "sostenibilidad CCSS"],
        "description": "Crisis de la CCSS",
        "penalty": -1
    },
    "formal_employment": {
        "terms": ["empleo formal", "formalización", "informalidad laboral", "trabajo decente",
                  "cotizante", "seguro social obligatorio"],
        "description": "Empleo formal",
        "penalty": -0.5
    },
    "organized_crime": {
        "terms": ["crimen organizado", "narcotráfico", "sicariato", "extorsión",
                  "lavado de dinero", "cartel", "banda criminal"],
        "description": "Crimen organizado",
        "penalty": -0.5
    }
}

# Penalización por pilar prioritario sin propuesta concreta
MISSING_PRIORITY_PILLAR_PENALTY = -0.5

# ====================================================================
# FUNCIONES UTILITARIAS
# ====================================================================

def normalize_text(text: str) -> str:
    """Normaliza el texto extraído, incluyendo correcciones para EasyOCR."""
    if not text:
        return ""
    
    # Eliminar caracteres de control
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    # Correcciones específicas para EasyOCR
    # "Ia" → "la" (error común de EasyOCR en español)
    text = re.sub(r'\bIa\b', 'la', text)
    text = re.sub(r'\bIa\n', 'la\n', text)
    
    # Normalizar espacios múltiples
    text = re.sub(r'\s+', ' ', text)
    
    # Normalizar saltos de línea múltiples
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    
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
# EXTRACCIÓN DE PDF CON SOPORTE OCR (heredado de v5)
# ====================================================================

def detect_corrupt_text(text: str) -> Tuple[bool, float]:
    """Detecta si un texto tiene caracteres de fuentes corruptas."""
    if not text:
        return False, 0.0
    total_chars = len(text)
    corrupt_count = sum(1 for char in text if char in CORRUPT_CHARS)
    corrupt_ratio = corrupt_count / total_chars if total_chars > 0 else 0
    return corrupt_ratio > CORRUPT_THRESHOLD, corrupt_ratio


# Variable global para el lector EasyOCR (inicializado una sola vez)
_easyocr_reader = None

def get_easyocr_reader():
    """Obtiene o inicializa el lector EasyOCR (singleton)."""
    global _easyocr_reader
    if _easyocr_reader is None and EASYOCR_AVAILABLE:
        try:
            import easyocr
            _easyocr_reader = easyocr.Reader(['es', 'en'], gpu=False)
        except Exception as e:
            print(f"    ⚠️  Error inicializando EasyOCR: {e}")
            return None
    return _easyocr_reader


def extract_page_with_ocr(page, dpi: int = RENDER_DPI) -> str:
    """
    Extrae texto de una página usando OCR.
    Prioriza EasyOCR, con fallback a Tesseract si EasyOCR no está disponible.
    """
    if not OCR_AVAILABLE:
        return ""
    
    try:
        # Renderizar página como imagen
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # Intentar EasyOCR primero (mejor calidad)
        if EASYOCR_AVAILABLE:
            try:
                reader = get_easyocr_reader()
                if reader:
                    import numpy as np
                    img_array = np.array(img)
                    results = reader.readtext(img_array)
                    # Combinar todos los textos detectados
                    text = "\n".join([result[1] for result in results])
                    return text
            except Exception as e:
                print(f"    ⚠️  Error EasyOCR, usando Tesseract: {e}")
        
        # Fallback a Tesseract
        if TESSERACT_AVAILABLE:
            text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)
            return text
        
        return ""
        
    except Exception as e:
        print(f"    ⚠️  Error OCR en página: {e}")
        return ""


def extract_text_with_pdfplumber(pdf_path: str) -> Tuple[List[Tuple[int, str]], str]:
    """
    Extrae texto usando pdfplumber (mejor para PDFs con texto corrupto).
    Retorna páginas y texto completo.
    """
    pages = []
    full_text = ""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            
            for page_num in range(num_pages):
                page = pdf.pages[page_num]
                text = page.extract_text()
                
                if text:
                    normalized = normalize_text(text)
                    if normalized:
                        pages.append((page_num + 1, normalized))
                        full_text += " " + normalized
            
            return pages, full_text
    except Exception as e:
        print(f"  ⚠️  Error con pdfplumber: {e}")
        return [], ""


def extract_text_from_pdf(pdf_path: str) -> Tuple[List[Tuple[int, str]], str]:
    """
    Extrae texto de un PDF usando estrategia híbrida:
    1. PyMuPDF para detección rápida de corrupción
    2. pdfplumber si hay texto corrupto (mejor calidad, sin OCR)
    3. EasyOCR/Tesseract como último recurso
    
    Retorna páginas y texto completo.
    """
    pages = []
    full_text = ""
    ocr_pages = 0
    doc = None
    pdf_name = os.path.basename(pdf_path)
    pdf_id = os.path.splitext(pdf_name)[0].lower()
    
    # Verificar si existe un archivo de texto OCR pre-extraído
    ocr_text_file = os.path.join(DATA_DIR, f"{pdf_id}_ocr_text.txt")
    if os.path.exists(ocr_text_file):
        print(f"  📄 {pdf_name}: Usando texto OCR pre-extraído...")
        try:
            with open(ocr_text_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parsear el archivo de texto OCR (formato: --- Página N ---)
            page_pattern = r'--- Página (\d+) ---\n(.*?)(?=--- Página \d+ ---|$)'
            matches = re.findall(page_pattern, content, re.DOTALL)
            
            for page_num_str, page_text in matches:
                page_num = int(page_num_str)
                normalized = normalize_text(page_text)
                if normalized:
                    pages.append((page_num, normalized))
                    full_text += " " + normalized
            
            print(f"  ✅ Cargadas {len(pages)} páginas desde archivo OCR")
            return pages, full_text
        except Exception as e:
            print(f"  ⚠️  Error leyendo archivo OCR: {e}, intentando extraer del PDF...")
    
    doc = None
    try:
        # ESTRATEGIA HÍBRIDA: Detección rápida con PyMuPDF
        doc = fitz.open(pdf_path)
        num_pages = len(doc)
        
        # Primera pasada: detectar si hay texto corrupto (muestra de primeras 10 páginas)
        sample_text = ""
        for page_num in range(min(10, num_pages)):
            sample_text += doc[page_num].get_text()
        
        is_corrupt, ratio = detect_corrupt_text(sample_text)
        doc.close()
        doc = None  # Marcar como cerrado
        
        # ESTRATEGIA RECOMENDADA:
        # 1. Si hay corrupción significativa (>5%) y pdfplumber disponible → usar pdfplumber
        # 2. Si pdfplumber falla o no disponible → usar PyMuPDF + OCR
        # 3. Si no hay corrupción → usar PyMuPDF directo (rápido)
        
        if is_corrupt and ratio > 0.05 and PDFPLUMBER_AVAILABLE:
            # ESTRATEGIA 1: pdfplumber para PDFs corruptos (mejor calidad, sin OCR)
            print(f"  ⚠️  {pdf_name}: Texto corrupto ({ratio*100:.1f}%), usando pdfplumber...")
            pages, full_text = extract_text_with_pdfplumber(pdf_path)
            if pages:
                print(f"  ✅ pdfplumber completado: {len(pages)} páginas procesadas")
                return pages, full_text
            else:
                # pdfplumber falló, usar OCR como último recurso
                print(f"  ⚠️  pdfplumber falló, usando PyMuPDF + OCR como último recurso...")
                doc = fitz.open(pdf_path)
                use_ocr = True  # Forzar OCR ya que hay corrupción
        elif is_corrupt and ratio > 0.05 and not PDFPLUMBER_AVAILABLE:
            # ESTRATEGIA 2: Corrupción detectada pero pdfplumber no disponible → usar OCR
            if OCR_AVAILABLE:
                engine = "EasyOCR" if EASYOCR_AVAILABLE else ("Tesseract" if TESSERACT_AVAILABLE else "N/A")
                print(f"  ⚠️  {pdf_name}: Texto corrupto ({ratio*100:.1f}%), extrayendo con {engine}...")
                doc = fitz.open(pdf_path)
                use_ocr = True
            else:
                print(f"  ⚠️  {pdf_name}: Texto corrupto ({ratio*100:.1f}%) pero OCR no disponible")
                doc = fitz.open(pdf_path)
                use_ocr = False
        else:
            # ESTRATEGIA 3: PDF limpio → usar PyMuPDF directo (rápido y fidedigno)
            if is_corrupt:
                print(f"  ℹ️  {pdf_name}: Corrupción menor ({ratio*100:.1f}%), usando PyMuPDF directo...")
            else:
                print(f"  ✅ {pdf_name}: Texto limpio, usando PyMuPDF directo...")
            doc = fitz.open(pdf_path)
            use_ocr = False  # No usar OCR para PDFs limpios
        
        # Segunda pasada: extraer texto con PyMuPDF (con o sin OCR según estrategia)
        for page_num in range(num_pages):
            page = doc[page_num]
            
            if use_ocr:
                # Usar OCR para esta página (último recurso)
                text = extract_page_with_ocr(page)
                ocr_pages += 1
            else:
                # Extracción directa con PyMuPDF
                text = page.get_text()
                # Verificar si esta página específica tiene problemas (fallback por página)
                page_corrupt, _ = detect_corrupt_text(text)
                if page_corrupt and OCR_AVAILABLE:
                    # Solo esta página tiene problemas, usar OCR solo para esta
                    text = extract_page_with_ocr(page)
                    ocr_pages += 1
            
            normalized = normalize_text(text)
            if normalized:
                pages.append((page_num + 1, normalized))
                full_text += " " + normalized
        
        if ocr_pages > 0:
            engine_used = "EasyOCR" if EASYOCR_AVAILABLE else "Tesseract"
            print(f"  ✅ OCR completado ({engine_used}): {ocr_pages}/{num_pages} páginas procesadas")
            
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
# VERIFICACIÓN DE VIABILIDAD LEGAL v7 - FASE 1
# ====================================================================

# Indicadores de reforma constitucional REAL (alta confianza)
# Solo cambios estructurales que realmente requieren reforma constitucional
CONSTITUTIONAL_REFORM_INDICATORS = [
    # Eliminar/modificar instituciones constitucionales
    r"eliminar\s+(?:la\s+)?asamblea\s+legislativa",
    r"eliminar\s+(?:el\s+)?poder\s+judicial",
    r"disolver\s+(?:la\s+)?asamblea\s+legislativa",
    r"disolver\s+(?:el\s+)?poder\s+judicial",
    r"suprimir\s+(?:la\s+)?asamblea\s+legislativa",
    r"suprimir\s+(?:el\s+)?poder\s+judicial",
    # Modificar artículos constitucionales específicos
    r"modificar.*art\.?\s*\d+.*constitución",
    r"modificar.*artículo\s*\d+.*constitución",
    r"cambiar.*art\.?\s*\d+.*constitución",
    r"cambiar.*artículo\s*\d+.*constitución",
    r"reformar.*art\.?\s*\d+.*constitución",
    r"reformar.*artículo\s*\d+.*constitución",
    # Cambios estructurales del Estado
    r"cambiar\s+(?:la\s+)?estructura\s+del\s+estado",
    r"modificar\s+(?:la\s+)?estructura\s+del\s+estado",
    r"reformar\s+constitución\s+para\s+(?:eliminar|modificar|cambiar|suprimir)",
    # Reforma general (Asamblea Constituyente)
    r"asamblea\s+constituyente",
    r"reforma\s+general\s+de\s+la\s+constitución",
]

# Menciones genéricas que NO requieren reforma constitucional (excluir)
# Estas son menciones de "reforma constitucional" pero sin cambios reales
GENERIC_CONSTITUTIONAL_MENTIONS = [
    r"reforma\s+constitucional\s+y\s+[a-z]+",  # "reforma constitucional y fiscal"
    r"reafirmar.*(?:art\.?\s*\d+|constitución|derecho)",
    r"garantizar.*(?:art\.?\s*\d+|constitución|derecho)",
    r"fortalecer.*(?:art\.?\s*\d+|constitución|derecho)",
    r"respetar.*(?:art\.?\s*\d+|constitución)",
    r"cumplir.*(?:art\.?\s*\d+|constitución)",
]

# Indicadores de violación de separación de poderes
SEPARATION_POWERS_VIOLATIONS = [
    # Eliminar/disolver instituciones constitucionales (viola separación de poderes)
    r"(?:eliminar|disolver|cerrar|suprimir).*asamblea\s+legislativa",
    r"asamblea\s+legislativa.*(?:eliminar|disolver|cerrar|suprimir)",
    r"(?:eliminar|disolver|cerrar|suprimir).*poder\s+judicial",
    r"poder\s+judicial.*(?:eliminar|disolver|cerrar|suprimir)",
    # Gobernar por decreto sin Asamblea (viola separación de poderes)
    r"gobierno\s+por\s+decreto\s+(?:sin|sin\s+la\s+)?asamblea",
    r"gobernar\s+por\s+decreto\s+(?:sin|sin\s+la\s+)?asamblea",
    r"decretos?\s+(?:permanentes?|indefinidos?)\s+(?:sin|sin\s+la\s+)?asamblea",
    # Ejecutivo legisla/juzga (viola separación de poderes)
    r"ejecutivo.*(?:legislar|juzgar)",
    r"presidente.*(?:legislar|juzgar)",
    r"poder\s+ejecutivo.*(?:legislar|juzgar)",
    # Concentración de poderes
    r"ejecutivo\s+legislativo",
    r"concentración\s+de\s+poderes",
]

# Indicadores de violación de derechos fundamentales (art. 11-89)
# NOTA: Solo detectar eliminación/suspensión completa, NO reformas legítimas
FUNDAMENTAL_RIGHTS_VIOLATIONS = [
    # Suspender/eliminar libertades fundamentales
    r"suspender.*libertad\s+de\s+expresión",
    r"eliminar.*libertad\s+de\s+expresión",
    r"prohibir.*libertad\s+de\s+expresión",
    r"suspender.*libertad\s+de\s+prensa",
    r"eliminar.*libertad\s+de\s+prensa",
    r"prohibir.*libertad\s+de\s+prensa",
    # Eliminar derechos laborales fundamentales
    r"eliminar.*derecho\s+a\s+huelga",
    r"prohibir.*derecho\s+a\s+huelga",
    r"suspender.*derecho\s+a\s+huelga",
    # Prohibir manifestaciones
    r"prohibir.*manifestaciones",
    r"eliminar.*derecho\s+a\s+manifestación",
    r"suspender.*derecho\s+a\s+manifestación",
    # Eliminar instituciones constitucionales de derechos (solo eliminación completa)
    r"eliminar.*(?:ccss|caja\s+costarricense).*(?:completamente|totalmente|por\s+completo)",
    r"privatizar.*(?:ccss|caja\s+costarricense).*(?:completamente|totalmente|por\s+completo)",
    r"eliminar.*educación\s+pública.*(?:completamente|totalmente|por\s+completo)",
    r"privatizar.*educación\s+pública.*(?:completamente|totalmente|por\s+completo)",
    # Restringir acceso a servicios públicos fundamentales
    r"restringir.*acceso\s+a\s+salud\s+pública.*(?:completamente|totalmente)",
    r"restringir.*acceso\s+a\s+educación\s+pública.*(?:completamente|totalmente)",
]

# Indicadores de violación de garantías constitucionales (art. 40-71)
CONSTITUTIONAL_GUARANTEES_VIOLATIONS = [
    # Eliminar/suspender garantías procesales
    r"eliminar.*hábeas\s+corpus",
    r"suspender.*hábeas\s+corpus",
    r"prohibir.*hábeas\s+corpus",
    r"eliminar.*garantía\s+de\s+amparo",
    r"suspender.*garantía\s+de\s+amparo",
    r"prohibir.*garantía\s+de\s+amparo",
    # Suspender garantías individuales
    r"suspender.*garantías\s+individuales",
    r"eliminar.*garantías\s+individuales",
    r"suspender.*garantías\s+constitucionales",
    r"eliminar.*garantías\s+constitucionales",
    # Restringir garantías procesales
    r"restringir.*garantías\s+procesales.*(?:completamente|totalmente)",
    r"eliminar.*debido\s+proceso",
    r"suspender.*debido\s+proceso",
]

# Indicadores de violación de procedimientos constitucionales
CONSTITUTIONAL_PROCEDURE_VIOLATIONS = [
    # Aprobar/ratificar sin Asamblea (viola procedimientos)
    r"aprobar\s+presupuesto\s+sin\s+(?:la\s+)?asamblea",
    r"ratificar\s+tratados\s+sin\s+(?:la\s+)?asamblea",
    r"declarar\s+guerra\s+sin\s+(?:la\s+)?asamblea",
    r"nombrar\s+ministros\s+sin\s+(?:la\s+)?asamblea",
    # Ejecutivo hace funciones de Asamblea
    r"ejecutivo.*(?:aprueba|ratifica|declara).*(?:sin|sin\s+la\s+)?asamblea",
    r"presidente.*(?:aprueba|ratifica|declara).*(?:sin|sin\s+la\s+)?asamblea",
]

def check_viability(text: str, pillar_id: str) -> Dict:
    """
    v7 Fase 1 Ampliada: Verifica viabilidad legal y constitucional de una propuesta.
    
    Verificaciones:
    - Viola separación de poderes: -1.0
    - Viola derechos fundamentales: -1.0
    - Viola garantías constitucionales: -1.0
    - Viola procedimientos constitucionales: -0.5
    
    NOTA: Eliminada penalización por "requiere reforma constitucional" porque:
    - Una reforma constitucional puede ser legítima y necesaria
    - No tenemos contexto para evaluar si es "necesaria" o no
    - Es más neutral y objetivo solo penalizar violaciones claras
    
    Retorna penalizaciones por inviabilidad.
    """
    penalties = []
    flags = {
        "violates_separation_powers": False,
        "violates_fundamental_rights": False,
        "violates_constitutional_guarantees": False,
        "violates_constitutional_procedures": False,
    }
    
    text_lower = text.lower()
    
    # Función auxiliar para extraer evidencia
    def extract_evidence(pattern):
        match = re.search(pattern, text_lower)
        if match:
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 150)
            return text[start:end].strip()[:200]
        return text[:200]
    
    # 1. Verificación: Viola separación de poderes (-1.0)
    for pattern in SEPARATION_POWERS_VIOLATIONS:
        if re.search(pattern, text_lower):
            flags["violates_separation_powers"] = True
            penalties.append({
                "type": "violates_separation_powers",
                "value": -1.0,
                "reason": "Viola separación de poderes (art. 9, 11, 12 de la Constitución)",
                "evidence": extract_evidence(pattern)
            })
            break  # Solo una penalización por tipo
    
    # 2. Verificación: Viola derechos fundamentales (-1.0)
    for pattern in FUNDAMENTAL_RIGHTS_VIOLATIONS:
        if re.search(pattern, text_lower):
            flags["violates_fundamental_rights"] = True
            penalties.append({
                "type": "violates_fundamental_rights",
                "value": -1.0,
                "reason": "Viola derechos fundamentales (art. 11-89 de la Constitución)",
                "evidence": extract_evidence(pattern)
            })
            break  # Solo una penalización por tipo
    
    # 3. Verificación: Viola garantías constitucionales (-1.0)
    for pattern in CONSTITUTIONAL_GUARANTEES_VIOLATIONS:
        if re.search(pattern, text_lower):
            flags["violates_constitutional_guarantees"] = True
            penalties.append({
                "type": "violates_constitutional_guarantees",
                "value": -1.0,
                "reason": "Viola garantías constitucionales (art. 40-71 de la Constitución)",
                "evidence": extract_evidence(pattern)
            })
            break  # Solo una penalización por tipo
    
    # 4. Verificación: Viola procedimientos constitucionales (-0.5)
    for pattern in CONSTITUTIONAL_PROCEDURE_VIOLATIONS:
        if re.search(pattern, text_lower):
            flags["violates_constitutional_procedures"] = True
            penalties.append({
                "type": "violates_constitutional_procedures",
                "value": -0.5,
                "reason": "Viola procedimientos constitucionales",
                "evidence": extract_evidence(pattern)
            })
            break  # Solo una penalización por tipo
    
    return {
        "flags": flags,
        "penalties": penalties,
        "total_penalty": sum(p["value"] for p in penalties),
        "viability_score": max(0, 1.0 + sum(p["value"] for p in penalties))  # 0.0-1.0
    }

# ====================================================================
# DETECCIÓN DE PATRONES DICTATORIALES (v7 - Flags Informativos)
# ====================================================================

# Patrones objetivos de Cuba (históricamente verificables)
# NOTA: Solo patrones de comportamiento, NO ideología
CUBA_DICTATORIAL_PATTERNS = [
    r"eliminar.*separación\s+de\s+poderes",
    r"eliminar.*asamblea\s+legislativa",
    r"eliminar.*libertad\s+de\s+prensa",
    r"control.*estatal.*medios",
    r"eliminar.*garantías\s+constitucionales",
    r"concentración\s+de\s+poderes.*ejecutivo",
    r"ejecutivo.*legislativo",
    r"control.*total.*medios\s+de\s+comunicación",
]

# Patrones objetivos de Venezuela (históricamente verificables)
# NOTA: Solo patrones de comportamiento, NO ideología
VENEZUELA_DICTATORIAL_PATTERNS = [
    r"eliminar.*independencia\s+judicial",
    r"control.*poder\s+judicial.*ejecutivo",
    r"gobernar\s+por\s+decreto\s+sin\s+asamblea",
    r"eliminar.*libertad\s+de\s+expresión",
    r"cerrar.*medios\s+de\s+comunicación",
    r"concentración\s+de\s+poderes.*ejecutivo",
    r"asamblea\s+constituyente.*sin\s+asamblea",
    r"control.*total.*poder\s+judicial",
]

def detect_dictatorial_patterns(proposals: List[Dict]) -> Dict:
    """
    v7: Detecta similitudes objetivas con modelos dictatoriales históricos.
    
    NO juzga ideología, solo detecta patrones objetivos de comportamiento
    que coincidan con modelos dictatoriales históricamente verificables.
    
    Retorna flags informativos (NO penalizaciones).
    """
    patterns = {
        "cuba_similarity": {
            "active": False,
            "severity": "high",
            "evidence": [],
            "historical_sources": [
                "Resoluciones CIDH",
                "Informes ONU",
                "Documentos históricos verificables"
            ]
        },
        "venezuela_similarity": {
            "active": False,
            "severity": "high",
            "evidence": [],
            "historical_sources": [
                "Resoluciones CIDH",
                "Sentencias Corte Interamericana",
                "Informes ONU"
            ]
        }
    }
    
    for proposal in proposals:
        proposal_text = proposal.get("proposal_text", proposal.get("text", ""))
        if not proposal_text:
            continue
        
        text_lower = proposal_text.lower()
        pillar_id = proposal.get("pillar_id", "unknown")
        
        # Detectar similitudes con Cuba
        cuba_matches = []
        for pattern in CUBA_DICTATORIAL_PATTERNS:
            if re.search(pattern, text_lower):
                cuba_matches.append(pattern)
        
        if cuba_matches:
            patterns["cuba_similarity"]["active"] = True
            patterns["cuba_similarity"]["evidence"].append({
                "pillar_id": pillar_id,
                "proposal_text": proposal_text[:200],
                "matched_patterns": cuba_matches,
                "detection_method": "pattern_matching"
            })
        
        # Detectar similitudes con Venezuela
        venezuela_matches = []
        for pattern in VENEZUELA_DICTATORIAL_PATTERNS:
            if re.search(pattern, text_lower):
                venezuela_matches.append(pattern)
        
        if venezuela_matches:
            patterns["venezuela_similarity"]["active"] = True
            patterns["venezuela_similarity"]["evidence"].append({
                "pillar_id": pillar_id,
                "proposal_text": proposal_text[:200],
                "matched_patterns": venezuela_matches,
                "detection_method": "pattern_matching"
            })
    
    return patterns

# Patrones que indican necesidad de negociación entre poderes
# NOTA: Esto es legítimo pero informativo (complejidad de implementación)
POWER_NEGOTIATION_INDICATORS = [
    # Requiere aprobación de Asamblea (legítimo, pero requiere negociación)
    r"requiere\s+aprobación\s+de\s+la\s+asamblea",
    r"necesita\s+aprobación\s+legislativa",
    r"requiere\s+consenso\s+legislativo",
    r"aprobación\s+de\s+la\s+asamblea\s+legislativa",
    # Requiere mayoría calificada (2/3)
    r"mayoría\s+calificada",
    r"dos\s+tercios",
    r"2\/3",
    r"mayoría\s+de\s+dos\s+tercios",
    # Requiere coordinación entre poderes
    r"coordinación\s+entre\s+poderes",
    r"negociación\s+con\s+la\s+asamblea",
    r"consenso\s+entre\s+poderes",
    r"acuerdo\s+con\s+la\s+asamblea",
    # Requiere reforma legal que necesita Asamblea
    r"reforma\s+legal.*asamblea",
    r"modificar\s+ley.*asamblea",
    r"nueva\s+ley.*asamblea",
    r"proyecto\s+de\s+ley",
    # Requiere presupuesto aprobado por Asamblea
    r"presupuesto.*asamblea",
    r"aprobación\s+presupuestaria",
    r"asignación\s+presupuestaria.*asamblea",
    # Requiere ratificación de tratados
    r"ratificación.*asamblea",
    r"tratado.*asamblea",
    r"convenio.*asamblea",
]

def detect_power_negotiation_requirements(proposals: List[Dict]) -> Dict:
    """
    v7: Detecta propuestas que requieren negociación/coordinación entre poderes.
    
    Esto es legítimo pero informativo (indica complejidad de implementación).
    NO es una violación, solo información sobre la necesidad de negociación política.
    
    Retorna flags informativos (NO penalizaciones).
    """
    flags = {
        "requires_assembly_approval": {
            "active": False,
            "severity": "medium",
            "evidence": [],
            "description": "Requiere aprobación de la Asamblea Legislativa"
        },
        "requires_qualified_majority": {
            "active": False,
            "severity": "high",
            "evidence": [],
            "description": "Requiere mayoría calificada (2/3) en Asamblea"
        },
        "requires_inter_branch_coordination": {
            "active": False,
            "severity": "medium",
            "evidence": [],
            "description": "Requiere coordinación entre poderes del Estado"
        }
    }
    
    for proposal in proposals:
        proposal_text = proposal.get("proposal_text", proposal.get("text", ""))
        if not proposal_text:
            continue
        
        text_lower = proposal_text.lower()
        pillar_id = proposal.get("pillar_id", "unknown")
        
        # Detectar necesidad de aprobación de Asamblea
        assembly_approval_matches = []
        for pattern in [
            r"requiere\s+aprobación\s+de\s+la\s+asamblea",
            r"necesita\s+aprobación\s+legislativa",
            r"requiere\s+consenso\s+legislativo",
            r"aprobación\s+de\s+la\s+asamblea\s+legislativa",
            r"reforma\s+legal.*asamblea",
            r"modificar\s+ley.*asamblea",
            r"nueva\s+ley.*asamblea",
            r"proyecto\s+de\s+ley",
            r"presupuesto.*asamblea",
            r"aprobación\s+presupuestaria",
            r"ratificación.*asamblea",
            r"tratado.*asamblea"
        ]:
            if re.search(pattern, text_lower):
                assembly_approval_matches.append(pattern)
        
        if assembly_approval_matches:
            flags["requires_assembly_approval"]["active"] = True
            flags["requires_assembly_approval"]["evidence"].append({
                "pillar_id": pillar_id,
                "proposal_text": proposal_text[:200],
                "matched_patterns": assembly_approval_matches,
                "detection_method": "pattern_matching"
            })
        
        # Detectar necesidad de mayoría calificada
        qualified_majority_matches = []
        for pattern in [
            r"mayoría\s+calificada",
            r"dos\s+tercios",
            r"2\/3",
            r"mayoría\s+de\s+dos\s+tercios"
        ]:
            if re.search(pattern, text_lower):
                qualified_majority_matches.append(pattern)
        
        if qualified_majority_matches:
            flags["requires_qualified_majority"]["active"] = True
            flags["requires_qualified_majority"]["evidence"].append({
                "pillar_id": pillar_id,
                "proposal_text": proposal_text[:200],
                "matched_patterns": qualified_majority_matches,
                "detection_method": "pattern_matching"
            })
        
        # Detectar necesidad de coordinación entre poderes
        coordination_matches = []
        for pattern in [
            r"coordinación\s+entre\s+poderes",
            r"negociación\s+con\s+la\s+asamblea",
            r"consenso\s+entre\s+poderes",
            r"acuerdo\s+con\s+la\s+asamblea"
        ]:
            if re.search(pattern, text_lower):
                coordination_matches.append(pattern)
        
        if coordination_matches:
            flags["requires_inter_branch_coordination"]["active"] = True
            flags["requires_inter_branch_coordination"]["evidence"].append({
                "pillar_id": pillar_id,
                "proposal_text": proposal_text[:200],
                "matched_patterns": coordination_matches,
                "detection_method": "pattern_matching"
            })
    
    return flags

def load_historical_evidence() -> Dict[str, List[Dict]]:
    """
    v7 Fase 2: Carga evidencia histórica verificable desde archivo JSON.
    
    Retorna diccionario con candidate_id como clave y lista de evidencias como valor.
    Si el archivo no existe o está vacío, retorna diccionario vacío.
    """
    historical_evidence_path = os.path.join(DATA_DIR, "historical_evidence.json")
    
    if not os.path.exists(historical_evidence_path):
        return {}
    
    try:
        with open(historical_evidence_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convertir lista a diccionario para acceso rápido
        evidence_dict = {}
        for entry in data:
            candidate_id = entry.get("candidate_id")
            if candidate_id:
                evidence_dict[candidate_id] = entry.get("evidence", [])
        
        return evidence_dict
    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
        print(f"⚠️  Error cargando evidencia histórica: {e}")
        return {}

def analyze_historical_evidence(candidate_id: str, historical_evidence: List[Dict]) -> Dict:
    """
    v7 Fase 2: Analiza evidencia histórica verificable del candidato.
    
    Retorna flags informativos basados en evidencia histórica (NO penalizaciones).
    """
    flags = {
        "anti_democratic_behavior": {
            "active": False,
            "severity": "high",
            "evidence": [],
            "description": "Evidencia histórica de comportamiento anti-democrático verificable"
        },
        "human_rights_violations": {
            "active": False,
            "severity": "high",
            "evidence": [],
            "description": "Evidencia histórica de violaciones de derechos humanos"
        },
        "corruption_convictions": {
            "active": False,
            "severity": "high",
            "evidence": [],
            "description": "Evidencia histórica de corrupción verificada"
        }
    }
    
    if not historical_evidence:
        return flags
    
    for evidence_item in historical_evidence:
        category = evidence_item.get("category", "")
        severity = evidence_item.get("severity", "medium")
        
        # Comportamiento anti-democrático
        if category == "anti_democratic_behavior":
            flags["anti_democratic_behavior"]["active"] = True
            flags["anti_democratic_behavior"]["evidence"].append({
                "type": evidence_item.get("type", "unknown"),
                "date": evidence_item.get("date", "unknown"),
                "source": evidence_item.get("source", "unknown"),
                "description": evidence_item.get("description", ""),
                "verification_url": evidence_item.get("verification_url", ""),
                "severity": severity
            })
        
        # Violaciones de derechos humanos
        elif category == "human_rights_violations":
            flags["human_rights_violations"]["active"] = True
            flags["human_rights_violations"]["evidence"].append({
                "type": evidence_item.get("type", "unknown"),
                "date": evidence_item.get("date", "unknown"),
                "source": evidence_item.get("source", "unknown"),
                "description": evidence_item.get("description", ""),
                "verification_url": evidence_item.get("verification_url", ""),
                "severity": severity
            })
        
        # Corrupción verificada
        elif category == "corruption_convictions":
            flags["corruption_convictions"]["active"] = True
            flags["corruption_convictions"]["evidence"].append({
                "type": evidence_item.get("type", "unknown"),
                "date": evidence_item.get("date", "unknown"),
                "source": evidence_item.get("source", "unknown"),
                "description": evidence_item.get("description", ""),
                "verification_url": evidence_item.get("verification_url", ""),
                "severity": severity
            })
    
    return flags

def analyze_informative_flags(
    candidate_id: str,
    proposals: List[Dict],
    viability_flags_by_pillar: Dict[str, Dict],
    historical_evidence: List[Dict] = None
) -> Dict:
    """
    v7: Analiza flags informativos basados en propuestas actuales, viabilidad e historia.
    
    Flags informativos NO penalizan, solo informan al ciudadano.
    
    Tipos de flags:
    1. Propuestas actuales problemáticas (basadas en viabilidad)
    2. Similitudes con modelos dictatoriales (Cuba, Venezuela)
    3. Requisitos de negociación entre poderes (complejidad de implementación)
    4. Evidencia histórica verificable (Fase 2)
    """
    flags = {
        "current_proposals": {
            "violates_separation_powers": {
                "active": False,
                "severity": "high",
                "evidence": []
            },
            "violates_fundamental_rights": {
                "active": False,
                "severity": "high",
                "evidence": []
            },
            "violates_constitutional_guarantees": {
                "active": False,
                "severity": "high",
                "evidence": []
            },
            "violates_constitutional_procedures": {
                "active": False,
                "severity": "medium",
                "evidence": []
            }
        },
        "dictatorial_patterns": {},
        "power_negotiation_requirements": {},  # NUEVO
        "historical": {},  # Fase 2: Evidencia histórica
        "contradictions": {}  # Fase 3: Contradicciones histórico-actual
    }
    
    # 1. Analizar propuestas actuales problemáticas (usar flags de viabilidad)
    for pillar_id, viability_data in viability_flags_by_pillar.items():
        viability_flags = viability_data.get("flags", {})
        
        # Separación de poderes
        if viability_flags.get("violates_separation_powers", False):
            flags["current_proposals"]["violates_separation_powers"]["active"] = True
            flags["current_proposals"]["violates_separation_powers"]["evidence"].append({
                "pillar_id": pillar_id,
                "evidence": viability_data.get("evidence", ""),
                "detected_by": "viability_check"
            })
        
        # Derechos fundamentales
        if viability_flags.get("violates_fundamental_rights", False):
            flags["current_proposals"]["violates_fundamental_rights"]["active"] = True
            flags["current_proposals"]["violates_fundamental_rights"]["evidence"].append({
                "pillar_id": pillar_id,
                "evidence": viability_data.get("evidence", ""),
                "detected_by": "viability_check"
            })
        
        # Garantías constitucionales
        if viability_flags.get("violates_constitutional_guarantees", False):
            flags["current_proposals"]["violates_constitutional_guarantees"]["active"] = True
            flags["current_proposals"]["violates_constitutional_guarantees"]["evidence"].append({
                "pillar_id": pillar_id,
                "evidence": viability_data.get("evidence", ""),
                "detected_by": "viability_check"
            })
        
        # Procedimientos constitucionales
        if viability_flags.get("violates_constitutional_procedures", False):
            flags["current_proposals"]["violates_constitutional_procedures"]["active"] = True
            flags["current_proposals"]["violates_constitutional_procedures"]["evidence"].append({
                "pillar_id": pillar_id,
                "evidence": viability_data.get("evidence", ""),
                "detected_by": "viability_check"
            })
    
    # 2. Detectar similitudes con modelos dictatoriales
    dictatorial_patterns = detect_dictatorial_patterns(proposals)
    flags["dictatorial_patterns"] = dictatorial_patterns
    
    # 3. Detectar requisitos de negociación entre poderes (NUEVO)
    power_negotiation = detect_power_negotiation_requirements(proposals)
    flags["power_negotiation_requirements"] = power_negotiation
    
    # 4. Analizar evidencia histórica (Fase 2)
    if historical_evidence is None:
        historical_evidence = []
    historical_flags = analyze_historical_evidence(candidate_id, historical_evidence)
    flags["historical"] = historical_flags
    
    # 5. Detectar contradicciones entre histórico y actual (Fase 3)
    contradictions = detect_historical_current_contradictions(
        historical_flags,
        flags["current_proposals"],
        flags["dictatorial_patterns"]
    )
    flags["contradictions"] = contradictions
    
    return flags

def detect_historical_current_contradictions(
    historical_flags: Dict,
    current_proposals_flags: Dict,
    dictatorial_patterns: Dict
) -> Dict:
    """
    v7 Fase 3: Detecta contradicciones entre evidencia histórica y propuestas actuales.
    
    Detecta patrones consistentes que indican comportamiento problemático tanto histórico como actual.
    
    Retorna flags informativos (NO penalizaciones).
    """
    contradictions = {
        "historical_current_contradiction": {
            "active": False,
            "severity": "high",
            "evidence": {
                "historical": None,
                "current": None,
                "pattern": None
            },
            "description": "Patrón consistente: evidencia histórica problemática + propuestas actuales problemáticas"
        },
        "corruption_transparency_concern": {
            "active": False,
            "severity": "medium",
            "evidence": {
                "historical": None,
                "current": None,
                "pattern": None
            },
            "description": "Evidencia histórica de corrupción + propuestas actuales sin mecanismos de transparencia"
        }
    }
    
    # Contradicción 1: Histórico anti-democrático + Propuestas actuales problemáticas
    has_historical_anti_democratic = historical_flags.get("anti_democratic_behavior", {}).get("active", False)
    has_current_violations = any([
        current_proposals_flags.get("violates_separation_powers", {}).get("active", False),
        current_proposals_flags.get("violates_fundamental_rights", {}).get("active", False),
        current_proposals_flags.get("violates_constitutional_guarantees", {}).get("active", False)
    ])
    
    if has_historical_anti_democratic and has_current_violations:
        contradictions["historical_current_contradiction"]["active"] = True
        contradictions["historical_current_contradiction"]["evidence"]["historical"] = "Comportamiento anti-democrático histórico verificable"
        contradictions["historical_current_contradiction"]["evidence"]["current"] = "Propuestas actuales que violan principios constitucionales"
        contradictions["historical_current_contradiction"]["evidence"]["pattern"] = "Patrón consistente de comportamiento no democrático"
    
    # Contradicción 2: Histórico corrupto + Propuestas actuales sin transparencia
    has_historical_corruption = historical_flags.get("corruption_convictions", {}).get("active", False)
    
    # Detectar si propuestas actuales mencionan mecanismos de transparencia
    # (Esto es una simplificación - en el futuro se podría analizar el texto de las propuestas)
    # Por ahora, si hay corrupción histórica Y propuestas problemáticas, es una preocupación
    if has_historical_corruption and has_current_violations:
        contradictions["corruption_transparency_concern"]["active"] = True
        contradictions["corruption_transparency_concern"]["evidence"]["historical"] = "Corrupción verificada históricamente"
        contradictions["corruption_transparency_concern"]["evidence"]["current"] = "Propuestas actuales problemáticas"
        contradictions["corruption_transparency_concern"]["evidence"]["pattern"] = "Preocupación sobre transparencia y rendición de cuentas"
    
    # Contradicción 3: Histórico problemático + Similitudes dictatoriales actuales
    has_historical_issues = any([
        has_historical_anti_democratic,
        has_historical_corruption,
        historical_flags.get("human_rights_violations", {}).get("active", False)
    ])
    has_dictatorial_similarities = any([
        dictatorial_patterns.get("cuba_similarity", {}).get("active", False),
        dictatorial_patterns.get("venezuela_similarity", {}).get("active", False)
    ])
    
    if has_historical_issues and has_dictatorial_similarities:
        if not contradictions["historical_current_contradiction"]["active"]:
            contradictions["historical_current_contradiction"]["active"] = True
            contradictions["historical_current_contradiction"]["evidence"]["historical"] = "Evidencia histórica problemática verificable"
            contradictions["historical_current_contradiction"]["evidence"]["current"] = "Similitudes con modelos dictatoriales en propuestas actuales"
            contradictions["historical_current_contradiction"]["evidence"]["pattern"] = "Patrón consistente de comportamiento problemático"
    
    return contradictions

# ====================================================================
# ANÁLISIS FISCAL v6 (neutral - sin penalización por impuestos)
# ====================================================================

def analyze_fiscal_responsibility(full_text: str) -> Dict:
    """
    Analiza la posición fiscal del candidato.
    v6: Elimina penalización por impuestos (posición ideológica legítima).
    """
    text_lower = full_text.lower()
    
    analysis = {
        "penalties": [],
        "flags": {
            "attacks_fiscal_rule": False,
            "proposes_debt_increase": False,
            "shows_fiscal_responsibility": False,
        },
        "evidence": [],
        "total_penalty": 0
    }
    
    # Verificar indicadores de responsabilidad fiscal
    for pattern in FISCAL_RESPONSIBILITY_INDICATORS:
        if re.search(pattern, text_lower):
            analysis["flags"]["shows_fiscal_responsibility"] = True
            break
    
    # PENALIZACIÓN SEVERA: Atacar regla fiscal (-2)
    for pattern in FISCAL_RULE_ATTACK_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            analysis["flags"]["attacks_fiscal_rule"] = True
            start = max(0, match.start() - 50)
            end = min(len(text_lower), match.end() + 100)
            evidence = full_text[start:end].strip()[:200]
            
            analysis["penalties"].append({
                "type": "attacks_fiscal_rule",
                "value": -2,
                "reason": "Propone flexibilizar/reformar la regla fiscal (Ley 9635)",
                "evidence": evidence
            })
            analysis["evidence"].append(evidence)
            break
    
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
                "reason": "Propone aumentar deuda pública sin plan de sostenibilidad",
                "evidence": evidence
            })
            analysis["evidence"].append(evidence)
            break
    
    # NOTA v6: NO se penaliza proponer impuestos
    # Es una posición ideológica legítima, no irresponsabilidad fiscal
    
    analysis["total_penalty"] = sum(p["value"] for p in analysis["penalties"])
    
    return analysis

# ====================================================================
# ANÁLISIS DE OMISIONES v6 - URGENCIAS NACIONALES
# ====================================================================

def analyze_urgency_omissions(full_text: str) -> Dict:
    """
    Analiza si el candidato omite urgencias nacionales críticas.
    v6: Nueva función para penalizar omisiones.
    """
    text_lower = full_text.lower()
    
    analysis = {
        "penalties": [],
        "coverage": {},
        "total_penalty": 0
    }
    
    for urgency_key, urgency_data in URGENCY_TERMS.items():
        found_terms = []
        for term in urgency_data["terms"]:
            if term.lower() in text_lower:
                found_terms.append(term)
        
        is_covered = len(found_terms) > 0
        analysis["coverage"][urgency_key] = {
            "covered": is_covered,
            "terms_found": found_terms,
            "description": urgency_data["description"]
        }
        
        # Si no cubre la urgencia, aplicar penalización
        if not is_covered:
            analysis["penalties"].append({
                "type": f"ignores_{urgency_key}",
                "value": urgency_data["penalty"],
                "reason": f"No aborda: {urgency_data['description']}",
                "evidence": "Término no encontrado en el documento"
            })
    
    analysis["total_penalty"] = sum(p["value"] for p in analysis["penalties"])
    
    return analysis

def analyze_pillar_omissions(proposals: List[Dict], candidate_id: str) -> Dict:
    """
    Analiza si faltan propuestas en pilares prioritarios.
    v6: Penalización por cada pilar prioritario sin propuesta.
    """
    analysis = {
        "penalties": [],
        "missing_pillars": [],
        "total_penalty": 0
    }
    
    candidate_proposals = [p for p in proposals if p["candidate_id"] == candidate_id]
    
    for pillar_id in PRIORITY_PILLARS:
        prop = next((p for p in candidate_proposals if p["pillar_id"] == pillar_id), None)
        
        # Si no hay propuesta o es placeholder
        if not prop or prop["dimensions"]["existence"] == 0:
            analysis["missing_pillars"].append(pillar_id)
            analysis["penalties"].append({
                "type": "missing_priority_pillar",
                "value": MISSING_PRIORITY_PILLAR_PENALTY,
                "reason": f"Sin propuesta concreta en pilar prioritario {pillar_id}",
                "pillar_id": pillar_id
            })
    
    analysis["total_penalty"] = sum(p["value"] for p in analysis["penalties"])
    
    return analysis

# ====================================================================
# EXTRACCIÓN DE PROPUESTAS
# ====================================================================

def extract_best_proposal_per_pillar(pages: List[Tuple[int, str]], pdf_id: str) -> Dict[str, List[Dict]]:
    """
    v7: Extrae hasta 3 propuestas válidas por pilar (score >= 2).
    Retorna lista de propuestas en lugar de solo la mejor.
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
    
    # v7: Filtrar propuestas válidas (score >= 2) y guardar hasta 3 mejores
    best_by_pillar = {}
    for pillar_id, proposals in candidates_by_pillar.items():
        # Filtrar propuestas válidas (score >= 2, E=1 obligatorio)
        valid_proposals = [p for p in proposals if p["raw_score"] >= 2]
        # Ordenar por score (desc), luego por funding (desc)
        valid_proposals.sort(key=lambda p: (p["raw_score"], p["dimensions"]["funding"]), reverse=True)
        # Guardar hasta 3 mejores propuestas válidas
        best_by_pillar[pillar_id] = valid_proposals[:3] if valid_proposals else []
    
    return best_by_pillar

def create_proposals_json(best_by_pillar: Dict[str, List[Dict]], candidate_id: str, pdf_id: str) -> List[Dict]:
    """
    v7: Crea propuestas JSON con múltiples propuestas por pilar (hasta 3).
    """
    proposals = []
    
    for pillar in PILLARS:
        pillar_id = pillar["pillar_id"]
        
        if pillar_id in best_by_pillar and best_by_pillar[pillar_id]:
            # v7: Guardar múltiples propuestas (hasta 3)
            for p in best_by_pillar[pillar_id]:
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
                proposals.append(proposal)
        else:
            # Placeholder si no hay propuestas
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
# SCORING v6 - CON TODAS LAS PENALIZACIONES
# ====================================================================

def calculate_candidate_score(
    proposals: List[Dict], 
    candidate_id: str, 
    full_text: str, 
    fiscal_analysis: Dict,
    urgency_analysis: Dict,
    pillar_analysis: Dict
) -> Dict:
    """
    v7: Calcula scores con penalizaciones v6 + bonos por múltiples propuestas.
    Sistema de bonos:
    - 3+ propuestas válidas: +1.0
    - Propuesta completa (4/4): +0.25
    - Propuesta con financiamiento (3+): +0.1
    """
    
    # Obtener todas las propuestas del candidato agrupadas por pilar
    candidate_proposals_by_pillar = defaultdict(list)
    for p in proposals:
        if p["candidate_id"] == candidate_id:
            candidate_proposals_by_pillar[p["pillar_id"]].append(p)
    
    pillar_scores = []
    # v7: Recopilar información de viabilidad por pilar para flags informativos
    viability_flags_by_pillar = {}
    
    for pillar in PILLARS:
        pillar_id = pillar["pillar_id"]
        weight = pillar["weight"]
        
        # Obtener propuestas válidas para este pilar (score >= 2, E=1)
        pillar_proposals = candidate_proposals_by_pillar.get(pillar_id, [])
        valid_proposals = [
            p for p in pillar_proposals
            if p["dimensions"]["existence"] == 1 and 
            sum(p["dimensions"].values()) >= 2
        ]
        
        # Mejor propuesta (score base)
        if valid_proposals:
            best_prop = max(valid_proposals, key=lambda p: sum(p["dimensions"].values()))
            base_score = sum(best_prop["dimensions"].values())
        else:
            base_score = 0
        
        # v7: Bono por múltiples propuestas (SOLO si tiene 3+)
        num_valid = len(valid_proposals)
        if num_valid >= 3:
            bonus_multiple = 1.0
        else:
            bonus_multiple = 0.0  # No bono para 1 o 2 propuestas
        
        # v7: Bono por calidad
        complete_count = len([p for p in valid_proposals if sum(p["dimensions"].values()) == 4])
        funding_count = len([
            p for p in valid_proposals 
            if p["dimensions"]["funding"] == 1 and sum(p["dimensions"].values()) >= 3
        ])
        bonus_quality = (complete_count * 0.25) + (funding_count * 0.1)
        
        # v7 Fase 1: Verificación de viabilidad legal (aplicar a mejor propuesta)
        viability_penalty = 0
        viability_flags = {}
        pillar_penalties_viability = []
        if valid_proposals and best_prop:
            # Obtener texto de la propuesta (puede estar en "text" o "proposal_text")
            best_prop_text = best_prop.get("proposal_text", best_prop.get("text", ""))
            if best_prop_text:
                viability_analysis = check_viability(best_prop_text, pillar_id)
                viability_penalty = viability_analysis["total_penalty"]
                viability_flags = viability_analysis["flags"]
                # Agregar penalizaciones de viabilidad a pillar_penalties para registro
                pillar_penalties_viability = viability_analysis["penalties"]
                # v7: Guardar información de viabilidad para flags informativos
                viability_flags_by_pillar[pillar_id] = {
                    "flags": viability_flags,
                    "evidence": best_prop_text[:200]
                }
        
        pillar_penalties = []
        
        # Aplicar penalizaciones fiscales a P1
        if pillar_id == "P1":
            pillar_penalties.extend(fiscal_analysis["penalties"])
        
        # Aplicar penalizaciones de urgencias a pilares relevantes
        if pillar_id == "P3":  # Seguridad
            for p in urgency_analysis["penalties"]:
                if "security" in p["type"] or "organized_crime" in p["type"]:
                    pillar_penalties.append(p)
        
        if pillar_id == "P4":  # Salud
            for p in urgency_analysis["penalties"]:
                if "ccss" in p["type"]:
                    pillar_penalties.append(p)
        
        if pillar_id == "P2":  # Empleo
            for p in urgency_analysis["penalties"]:
                if "employment" in p["type"]:
                    pillar_penalties.append(p)
        
        # Aplicar penalizaciones de pilares prioritarios faltantes
        for p in pillar_analysis["penalties"]:
            if p.get("pillar_id") == pillar_id:
                pillar_penalties.append(p)
        
        # v7 Fase 1: Agregar penalizaciones de viabilidad
        pillar_penalties.extend(pillar_penalties_viability)
        
        # Calcular effective_score con bonos y penalizaciones de viabilidad (mínimo 0, máximo 4.0)
        total_penalty = sum(p["value"] for p in pillar_penalties)
        effective_score = max(0, min(4.0, base_score + bonus_multiple + bonus_quality + total_penalty))
        
        normalized = effective_score / 4.0
        weighted = normalized * weight
        
        pillar_scores.append({
            "pillar_id": pillar_id,
            "raw_score": base_score,
            "bonus_multiple": round(bonus_multiple, 2),
            "bonus_quality": round(bonus_quality, 2),
            "viability_penalty": round(viability_penalty, 2),
            "viability_flags": viability_flags,
            "effective_score": round(effective_score, 2),
            "normalized": round(normalized, 4),
            "weighted": round(weighted, 4),
            "num_proposals": num_valid,
            "penalties": pillar_penalties
        })
    
    # Totales
    raw_sum = sum(ps["raw_score"] for ps in pillar_scores)
    effective_sum = sum(ps["effective_score"] for ps in pillar_scores)
    weighted_sum = sum(ps["weighted"] for ps in pillar_scores)
    
    # Coverage de pilares prioritarios
    priority_weighted = sum(
        ps["weighted"] for ps in pillar_scores
        if ps["pillar_id"] in PRIORITY_PILLARS
    )
    
    # Coverage de pilares críticos
    critical_weighted = sum(
        ps["weighted"] for ps in pillar_scores
        if ps["pillar_id"] in CRITICAL_PILLARS
    )
    
    # Calcular penalización total
    all_penalties = (
        fiscal_analysis["penalties"] + 
        urgency_analysis["penalties"] + 
        pillar_analysis["penalties"]
    )
    total_penalties = sum(p["value"] for p in all_penalties)
    
    # Notas
    notes = []
    
    if fiscal_analysis["flags"]["attacks_fiscal_rule"]:
        notes.append("🔴 ATACA REGLA FISCAL (-2)")
    if fiscal_analysis["flags"]["proposes_debt_increase"]:
        notes.append("🟠 PROPONE MÁS DEUDA (-1)")
    if fiscal_analysis["flags"]["shows_fiscal_responsibility"]:
        notes.append("✅ Responsabilidad fiscal")
    
    # Notas de omisiones
    omitted = [k for k, v in urgency_analysis["coverage"].items() if not v["covered"]]
    if omitted:
        notes.append(f"⚠️ Omite: {', '.join(omitted)}")
    
    if pillar_analysis["missing_pillars"]:
        notes.append(f"❌ Sin propuesta: {', '.join(pillar_analysis['missing_pillars'])}")
    
    # v7: Analizar flags informativos (NO penalizan, solo informan)
    candidate_proposals = [p for p in proposals if p["candidate_id"] == candidate_id]
    
    # v7 Fase 2: Cargar evidencia histórica
    all_historical_evidence = load_historical_evidence()
    candidate_historical_evidence = all_historical_evidence.get(candidate_id, [])
    
    informative_flags = analyze_informative_flags(
        candidate_id,
        candidate_proposals,
        viability_flags_by_pillar,
        candidate_historical_evidence
    )
    
    return {
        "candidate_id": candidate_id,
        "pillar_scores": pillar_scores,
        "fiscal_analysis": {
            "flags": fiscal_analysis["flags"],
            "total_penalty": fiscal_analysis["total_penalty"],
            "evidence": fiscal_analysis["evidence"][:2]
        },
        "omission_analysis": {
            "urgency_coverage": urgency_analysis["coverage"],
            "urgency_penalty": urgency_analysis["total_penalty"],
            "missing_pillars": pillar_analysis["missing_pillars"],
            "pillar_penalty": pillar_analysis["total_penalty"]
        },
        "informative_flags": informative_flags,  # v7: Flags informativos (NO penalizan)
        "overall": {
            "raw_sum": raw_sum,
            "effective_sum": effective_sum,
            "weighted_sum": round(weighted_sum, 4),
            "priority_weighted_sum": round(priority_weighted, 4),
            "critical_weighted_sum": round(critical_weighted, 4),
            "total_penalties_applied": total_penalties,
            "notes": " | ".join(notes) if notes else ""
        }
    }

# ====================================================================
# ANÁLISIS DETALLADO v6
# ====================================================================

def analyze_candidate_detailed(
    pages: List[Tuple[int, str]], 
    full_text: str, 
    pdf_id: str, 
    fiscal_analysis: Dict,
    urgency_analysis: Dict,
    pillar_analysis: Dict
) -> Dict:
    """Genera análisis detallado con nuevo sistema v6."""
    
    analysis = {
        "pdf_id": pdf_id,
        "total_pages": len(pages),
        "version": "v7_neutral_strict_bonus_viability_informative_flags",
        "fiscal_flags": fiscal_analysis["flags"],
        "fiscal_evidence": fiscal_analysis["evidence"],
        "urgency_coverage": urgency_analysis["coverage"],
        "missing_priority_pillars": pillar_analysis["missing_pillars"],
        "strengths": [],
        "weaknesses": [],
        "risk_level": "BAJO"
    }
    
    risk_score = 0
    
    # Fortalezas y debilidades por urgencias
    for key, data in urgency_analysis["coverage"].items():
        if data["covered"]:
            analysis["strengths"].append(f"✅ Aborda: {data['description']}")
        else:
            analysis["weaknesses"].append(f"⚠️ No aborda: {data['description']}")
            risk_score += 1
    
    # Riesgo fiscal
    if fiscal_analysis["flags"]["attacks_fiscal_rule"]:
        analysis["weaknesses"].append("🔴 ATACA REGLA FISCAL - Riesgo alto para finanzas públicas")
        risk_score += 3
    if fiscal_analysis["flags"]["proposes_debt_increase"]:
        analysis["weaknesses"].append("🟠 Propone aumentar deuda pública")
        risk_score += 2
    
    if fiscal_analysis["flags"]["shows_fiscal_responsibility"]:
        analysis["strengths"].append("✅ Demuestra responsabilidad fiscal")
        risk_score -= 1
    
    # Pilares prioritarios faltantes
    for pillar_id in pillar_analysis["missing_pillars"]:
        analysis["weaknesses"].append(f"❌ Sin propuesta en pilar prioritario {pillar_id}")
        risk_score += 1
    
    # Determinar nivel de riesgo
    if risk_score >= 5:
        analysis["risk_level"] = "ALTO"
    elif risk_score >= 2:
        analysis["risk_level"] = "MEDIO"
    else:
        analysis["risk_level"] = "BAJO"
    
    return analysis

# ====================================================================
# RANKING v6
# ====================================================================

def generate_ranking(candidate_scores: List[Dict]) -> Dict:
    ranking_overall = sorted(
        [(cs["candidate_id"], cs["overall"]["weighted_sum"], cs["overall"]["total_penalties_applied"]) 
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
        "method_version": "v7_neutral_strict_bonus_viability_informative_flags",
        "description": "Neutral (sin sesgo ideológico) + Estricto (penaliza omisiones) + Bonos (múltiples propuestas) + Viabilidad legal ampliada + Flags informativos (propuestas problemáticas, similitudes dictatoriales)",
        "weights": PILLAR_WEIGHTS,
        "priority_pillars": list(PRIORITY_PILLARS),
        "critical_pillars": list(CRITICAL_PILLARS),
        "penalties_applied": {
            "fiscal": {
                "attacks_fiscal_rule": -2,
                "proposes_debt_increase": -1,
            },
            "omissions": {
                "ignores_security_operations": -1,
                "ignores_ccss_crisis": -1,
                "ignores_formal_employment": -0.5,
                "ignores_organized_crime": -0.5,
                "missing_priority_pillar": -0.5,
            }
        },
        "ranking_overall_weighted": [
            {
                "rank": i + 1, 
                "candidate_id": cid, 
                "weighted_sum": ws,
                "total_penalties": tp
            }
            for i, (cid, ws, tp) in enumerate(ranking_overall)
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
    """Carga el archivo candidates.json existente."""
    candidates_file = os.path.join(DATA_DIR, "candidates.json")
    if os.path.exists(candidates_file):
        with open(candidates_file, 'r', encoding='utf-8') as f:
            candidates = json.load(f)
            return {c["pdf_id"]: c["candidate_id"] for c in candidates}
    return {}

def process_all_pdfs():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    existing_candidates = load_existing_candidates()
    print(f"📋 Cargados {len(existing_candidates)} candidate_ids del archivo existente")
    
    pdf_files = [f for f in os.listdir(PLANES_DIR) if f.endswith('.pdf')]
    
    all_candidates = []
    all_proposals = []
    all_scores = []
    all_analysis = []
    
    print(f"Procesando {len(pdf_files)} planes de gobierno...")
    print("=" * 80)
    print("Modelo: v7 NEUTRAL + ESTRICTO + BONOS + VIABILIDAD LEGAL")
    print("Estrategia de extracción:")
    if PDFPLUMBER_AVAILABLE:
        print("  • pdfplumber: PDFs con texto corrupto (calidad)")
    print("  • PyMuPDF: PDFs limpios (velocidad)")
    if EASYOCR_AVAILABLE:
        print("  • EasyOCR: Último recurso (OCR)")
    elif TESSERACT_AVAILABLE:
        print("  • Tesseract: Último recurso (OCR)")
    print("=" * 80)
    print("PENALIZACIONES FISCALES (objetivas - basadas en ley):")
    print("  • Atacar regla fiscal (Ley 9635): -2 puntos")
    print("  • Proponer más deuda: -1 punto")
    print("-" * 80)
    print("PENALIZACIONES POR OMISIÓN (urgencias nacionales):")
    print("  • No mencionar seguridad operativa: -1 punto")
    print("  • No mencionar crisis CCSS: -1 punto")
    print("  • No mencionar empleo formal: -0.5 puntos")
    print("  • No mencionar crimen organizado: -0.5 puntos")
    print("  • Por cada pilar prioritario sin propuesta: -0.5 puntos")
    print("-" * 80)
    print("BONOS POR MÚLTIPLES PROPUESTAS (v7):")
    print("  • 3+ propuestas válidas por pilar: +1.0 puntos")
    print("  • Propuesta completa (E+W+H+F): +0.25 puntos")
    print("  • Propuesta con financiamiento (score >= 3): +0.1 puntos")
    print("-" * 80)
    print("VERIFICACIÓN DE VIABILIDAD LEGAL (v7 Fase 1 Ampliada):")
    print("  • Viola separación de poderes: -1.0 puntos")
    print("  • Viola derechos fundamentales: -1.0 puntos")
    print("  • Viola garantías constitucionales: -1.0 puntos")
    print("  • Viola procedimientos constitucionales: -0.5 puntos")
    print("  • NOTA: No se penaliza reforma constitucional (puede ser legítima y necesaria)")
    print("--------------------------------------------------------------------------------")
    print("FLAGS INFORMATIVOS (v7 - NO penalizan, solo informan):")
    print("  • Propuestas actuales problemáticas (violaciones constitucionales)")
    print("  • Similitudes con modelos dictatoriales (Cuba, Venezuela)")
    print("  • Requisitos de negociación entre poderes (complejidad de implementación)")
    print("  • Evidencia histórica verificable (Fase 2: comportamiento, derechos, corrupción)")
    print("  • Contradicciones histórico-actual (Fase 3: patrones consistentes)")
    print("  • NOTA: Flags informativos NO afectan el score, solo informan al ciudadano")
    print("=" * 80)
    print("NOTA: No se penaliza proponer impuestos (posición ideológica legítima)")
    print("=" * 80)
    
    for pdf_file in sorted(pdf_files):
        pdf_id = pdf_file.replace('.pdf', '')
        pdf_path = os.path.join(PLANES_DIR, pdf_file)
        
        print(f"\n📄 {pdf_id}...")
        
        pages, full_text = extract_text_from_pdf(pdf_path)
        
        if not pages:
            print(f"   ⚠️ No se pudo extraer texto")
            continue
        
        info = extract_candidate_info(pages, pdf_id)
        
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
        
        # Análisis fiscal (v7: sin penalización por impuestos, igual que v6)
        fiscal_analysis = analyze_fiscal_responsibility(full_text)
        
        # Extraer propuestas
        best_by_pillar = extract_best_proposal_per_pillar(pages, pdf_id)
        proposals = create_proposals_json(best_by_pillar, candidate_id, pdf_id)
        all_proposals.extend(proposals)
        
        # Análisis de omisiones (v7: igual que v6)
        urgency_analysis = analyze_urgency_omissions(full_text)
        pillar_analysis = analyze_pillar_omissions(proposals, candidate_id)
        
        # Calcular scores con penalizaciones v6 + bonos v7
        scores = calculate_candidate_score(
            proposals, candidate_id, full_text, 
            fiscal_analysis, urgency_analysis, pillar_analysis
        )
        all_scores.append(scores)
        
        # Análisis detallado
        analysis = analyze_candidate_detailed(
            pages, full_text, pdf_id, 
            fiscal_analysis, urgency_analysis, pillar_analysis
        )
        analysis["candidate_id"] = candidate_id
        all_analysis.append(analysis)
        
        # Resumen
        total_penalties = scores["overall"]["total_penalties_applied"]
        risk = analysis["risk_level"]
        risk_emoji = {"ALTO": "🔴", "MEDIO": "🟠", "BAJO": "🟢"}.get(risk, "⚪")
        
        # Contar propuestas totales (v7: puede haber múltiples por pilar)
        total_proposals = sum(len(props) if isinstance(props, list) else 1 for props in best_by_pillar.values())
        print(f"   → Págs: {len(pages)} | Propuestas: {total_proposals} | Pilares: {len(best_by_pillar)}/10")
        print(f"   → Score: {scores['overall']['weighted_sum']:.1%} | Penalizaciones: {total_penalties}")
        print(f"   → Riesgo: {risk_emoji} {risk}")
    
    # Generar ranking
    ranking = generate_ranking(all_scores)
    
    print("\n" + "=" * 80)
    print("📊 RANKING FINAL - MODELO v7 NEUTRAL + ESTRICTO + BONOS + VIABILIDAD")
    print("=" * 80)
    print(f"{'#':<3} {'CANDIDATO':<20} {'SCORE':<10} {'PENALIZACIONES':<15} {'RIESGO'}")
    print("-" * 80)
    
    for entry in ranking["ranking_overall_weighted"]:
        analysis = next((a for a in all_analysis if a["candidate_id"] == entry["candidate_id"]), None)
        risk = analysis["risk_level"] if analysis else "?"
        risk_emoji = {"ALTO": "🔴", "MEDIO": "🟠", "BAJO": "🟢"}.get(risk, "⚪")
        
        print(f"{entry['rank']:<3} {entry['candidate_id']:<20} {entry['weighted_sum']:.1%}      {entry['total_penalties']:<15} {risk_emoji} {risk}")
    
    # Guardar archivos
    print("\n📁 Guardando archivos...")
    print("   ⚠️  candidates.json NO se regenera (mantener datos manuales)")
    
    outputs = {
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
    print("=" * 80)
    print("PROCESADOR DE PLANES v7.0 - NEUTRAL + ESTRICTO + BONOS + VIABILIDAD")
    print("10 pilares | OCR automático | Penalizaciones por omisión | Bonos múltiples propuestas | Verificación viabilidad legal")
    print("=" * 80)
    result = process_all_pdfs()
    print("\n✅ PROCESO COMPLETADO")
