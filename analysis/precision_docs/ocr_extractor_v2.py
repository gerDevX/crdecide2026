#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR Extractor v2 - Con soporte para múltiples motores OCR
Versión mejorada con EasyOCR y PaddleOCR como alternativas a Tesseract
"""

import fitz  # PyMuPDF
from PIL import Image
import io
import os
import sys
import re
import argparse
from typing import List, Tuple, Optional, Literal

# ====================================================================
# CONFIGURACIÓN
# ====================================================================

# Caracteres que indican texto corrupto
CORRUPT_CHARS = set('ӌǢņĞļšŹĵūÔŤŅƕýðųöĒĽĚÔūŤýĵÔūðŅĽųŤÔļšŹĵūÔŤšŤŅƕýðųŅŤýĒŅŤļÔ')
CORRUPT_THRESHOLD = 0.05

# DPI para renderizar páginas
RENDER_DPI = 300  # Aumentado de 200 para mejor calidad

# Motor OCR por defecto
DEFAULT_OCR_ENGINE = "tesseract"  # "tesseract", "easyocr", "paddleocr"

# ====================================================================
# DETECCIÓN DE CORRUPCIÓN
# ====================================================================

def detect_corrupt_text(text: str) -> Tuple[bool, float]:
    """Detecta si un texto tiene caracteres de fuentes corruptas."""
    if not text:
        return False, 0.0
    
    total_chars = len(text)
    corrupt_count = sum(1 for char in text if char in CORRUPT_CHARS)
    corrupt_ratio = corrupt_count / total_chars if total_chars > 0 else 0
    
    return corrupt_ratio > CORRUPT_THRESHOLD, corrupt_ratio

# ====================================================================
# EXTRACCIÓN CON TESSERACT (Actual)
# ====================================================================

def extract_with_tesseract(img: Image.Image) -> str:
    """Extrae texto usando Tesseract OCR."""
    try:
        import pytesseract
        text = pytesseract.image_to_string(img, config='--oem 3 --psm 6 -l spa')
        return text
    except ImportError:
        raise ImportError("pytesseract no instalado. Instalar: pip install pytesseract")
    except Exception as e:
        print(f"  ⚠️  Error Tesseract: {e}")
        return ""

# ====================================================================
# EXTRACCIÓN CON EASYOCR (Alternativa 1)
# ====================================================================

def extract_with_easyocr(img: Image.Image, reader=None) -> str:
    """Extrae texto usando EasyOCR (90-95% precisión)."""
    try:
        import easyocr
        import numpy as np
        
        # Inicializar lector si no existe
        if reader is None:
            reader = easyocr.Reader(['es', 'en'], gpu=False)
        
        # Convertir PIL Image a numpy array
        img_array = np.array(img)
        
        # EasyOCR retorna lista de tuplas: (bbox, text, confidence)
        results = reader.readtext(img_array)
        
        # Combinar todos los textos detectados
        text = "\n".join([result[1] for result in results])
        
        return text
    except ImportError:
        raise ImportError("easyocr no instalado. Instalar: pip install easyocr")
    except Exception as e:
        print(f"  ⚠️  Error EasyOCR: {e}")
        return ""

# ====================================================================
# EXTRACCIÓN CON PADDLEOCR (Alternativa 2 - Mayor precisión)
# ====================================================================

def extract_with_paddleocr(img: Image.Image, ocr=None) -> str:
    """Extrae texto usando PaddleOCR (96.5% precisión)."""
    try:
        from paddleocr import PaddleOCR
        import numpy as np
        
        # Inicializar OCR si no existe
        if ocr is None:
            ocr = PaddleOCR(use_angle_cls=True, lang='es', use_gpu=False)
        
        # Convertir PIL Image a numpy array
        img_array = np.array(img)
        
        # PaddleOCR retorna lista de listas: [[bbox, (text, confidence)], ...]
        results = ocr.ocr(img_array, cls=True)
        
        # Extraer textos
        text_lines = []
        if results and results[0]:
            for line in results[0]:
                if line and len(line) >= 2:
                    text_lines.append(line[1][0])  # text está en [1][0]
        
        text = "\n".join(text_lines)
        
        return text
    except ImportError:
        raise ImportError("paddleocr no instalado. Instalar: pip install paddlepaddle paddleocr")
    except Exception as e:
        print(f"  ⚠️  Error PaddleOCR: {e}")
        return ""

# ====================================================================
# EXTRACCIÓN PRINCIPAL
# ====================================================================

def extract_text_with_ocr(
    pdf_path: str, 
    engine: Literal["tesseract", "easyocr", "paddleocr"] = DEFAULT_OCR_ENGINE,
    dpi: int = RENDER_DPI
) -> List[Tuple[int, str]]:
    """
    Extrae texto de un PDF usando el motor OCR especificado.
    
    Args:
        pdf_path: Ruta al PDF
        engine: Motor OCR a usar ("tesseract", "easyocr", "paddleocr")
        dpi: Resolución para renderizar páginas
    
    Returns:
        Lista de (número_página, texto)
    """
    pages = []
    
    # Inicializar motor OCR una sola vez (para EasyOCR y PaddleOCR)
    reader = None
    ocr = None
    
    if engine == "easyocr":
        try:
            import easyocr
            reader = easyocr.Reader(['es', 'en'], gpu=False)
            print(f"  ✅ EasyOCR inicializado")
        except Exception as e:
            print(f"  ❌ Error inicializando EasyOCR: {e}")
            return []
    
    elif engine == "paddleocr":
        try:
            from paddleocr import PaddleOCR
            ocr = PaddleOCR(use_angle_cls=True, lang='es', use_gpu=False)
            print(f"  ✅ PaddleOCR inicializado")
        except Exception as e:
            print(f"  ❌ Error inicializando PaddleOCR: {e}")
            return []
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        print(f"  📄 Procesando {total_pages} páginas con {engine.upper()}...")
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            # Renderizar página como imagen
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Aplicar OCR según motor seleccionado
            if engine == "tesseract":
                text = extract_with_tesseract(img)
            elif engine == "easyocr":
                text = extract_with_easyocr(img, reader)
            elif engine == "paddleocr":
                text = extract_with_paddleocr(img, ocr)
            else:
                raise ValueError(f"Motor OCR desconocido: {engine}")
            
            # Normalizar texto
            text = normalize_text(text)
            
            if text:
                pages.append((page_num + 1, text))
            
            # Progreso
            if (page_num + 1) % 10 == 0:
                print(f"    ... {page_num + 1}/{total_pages} páginas procesadas")
        
        doc.close()
        print(f"  ✅ OCR completado: {len(pages)} páginas con texto")
        
    except Exception as e:
        print(f"  ❌ Error en OCR: {e}")
    
    return pages


def normalize_text(text: str) -> str:
    """Normaliza el texto extraído."""
    if not text:
        return ""
    
    # Reemplazar múltiples espacios/newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Eliminar caracteres de control
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    return text.strip()


# ====================================================================
# FUNCIONES PRINCIPALES
# ====================================================================

def process_single_pdf(
    pdf_path: str, 
    engine: Literal["tesseract", "easyocr", "paddleocr"] = DEFAULT_OCR_ENGINE,
    force_ocr: bool = False
) -> dict:
    """
    Procesa un PDF individual y retorna el texto extraído.
    """
    print(f"\n🔍 Analizando: {pdf_path}")
    
    # Verificar corrupción
    doc = fitz.open(pdf_path)
    sample_text = ""
    for page_num in range(min(10, len(doc))):
        sample_text += doc[page_num].get_text()
    doc.close()
    
    is_corrupt, ratio = detect_corrupt_text(sample_text)
    
    result = {
        'pdf_path': pdf_path,
        'is_corrupt': is_corrupt,
        'corruption_ratio': ratio,
        'pages': [],
        'engine': engine
    }
    
    if is_corrupt or force_ocr:
        print(f"  ⚠️  Texto corrupto detectado ({ratio*100:.1f}%)")
        print(f"  📸 Usando {engine.upper()} para extracción...")
        result['pages'] = extract_text_with_ocr(pdf_path, engine=engine)
        result['method'] = 'ocr'
    else:
        print(f"  ✅ Texto limpio, usando extracción directa")
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = normalize_text(page.get_text())
                if text:
                    result['pages'].append((page_num + 1, text))
            doc.close()
        except Exception as e:
            print(f"  ❌ Error: {e}")
        result['method'] = 'direct'
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Extractor OCR v2 - Soporte para múltiples motores OCR'
    )
    parser.add_argument(
        'path',
        help='Ruta al PDF o directorio de PDFs (desde precision_docs usar ../planes/)'
    )
    parser.add_argument(
        '--engine',
        choices=['tesseract', 'easyocr', 'paddleocr'],
        default=DEFAULT_OCR_ENGINE,
        help=f'Motor OCR a usar (default: {DEFAULT_OCR_ENGINE})'
    )
    parser.add_argument(
        '--force-ocr',
        action='store_true',
        help='Forzar uso de OCR incluso si el texto parece limpio'
    )
    parser.add_argument(
        '--output',
        help='Archivo de salida para el texto extraído'
    )
    
    args = parser.parse_args()
    
    if os.path.isfile(args.path):
        result = process_single_pdf(args.path, engine=args.engine, force_ocr=args.force_ocr)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                for page_num, text in result['pages']:
                    f.write(f"\n--- Página {page_num} ---\n")
                    f.write(text)
                    f.write("\n")
            print(f"\n💾 Texto guardado en: {args.output}")
        else:
            total_chars = sum(len(text) for _, text in result['pages'])
            print(f"\n📊 Resumen:")
            print(f"   Páginas extraídas: {len(result['pages'])}")
            print(f"   Caracteres totales: {total_chars:,}")
            print(f"   Método: {result['method']}")
            print(f"   Motor OCR: {result.get('engine', 'N/A')}")
    else:
        print(f"❌ Ruta no encontrada: {args.path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
