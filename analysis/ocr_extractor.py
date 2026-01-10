#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR Extractor para PDFs con texto corrupto
Usa Tesseract OCR para extraer texto de PDFs que tienen problemas de encoding de fuentes.

Uso:
    python ocr_extractor.py planes/PPSO.pdf
    python ocr_extractor.py --check planes/  # Detecta PDFs con texto corrupto
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import sys
import re
import argparse
from typing import List, Tuple, Optional

# ====================================================================
# CONFIGURACIÓN
# ====================================================================

# Caracteres que indican texto corrupto (fuentes con encoding incorrecto)
CORRUPT_CHARS = set('ӌǢņĞļšŹĵūÔŤŅƕýðųöĒĽĚÔūŤýĵÔūðŅĽųŤÔļšŹĵūÔŤšŤŅƕýðųŅŤýĒŅŤļÔ')

# Umbral de caracteres corruptos para considerar un PDF problemático
CORRUPT_THRESHOLD = 0.05  # 5% de caracteres corruptos

# Configuración de Tesseract
TESSERACT_CONFIG = '--oem 3 --psm 6 -l spa'  # OCR Engine Mode 3, Page Segmentation Mode 6, Español

# DPI para renderizar páginas (mayor = mejor calidad pero más lento)
RENDER_DPI = 200

# ====================================================================
# FUNCIONES DE DETECCIÓN
# ====================================================================

def detect_corrupt_text(text: str) -> Tuple[bool, float]:
    """
    Detecta si un texto tiene caracteres de fuentes corruptas.
    
    Returns:
        Tuple[bool, float]: (es_corrupto, porcentaje_caracteres_corruptos)
    """
    if not text:
        return False, 0.0
    
    total_chars = len(text)
    corrupt_count = sum(1 for char in text if char in CORRUPT_CHARS)
    corrupt_ratio = corrupt_count / total_chars if total_chars > 0 else 0
    
    return corrupt_ratio > CORRUPT_THRESHOLD, corrupt_ratio


def check_pdf_for_corruption(pdf_path: str) -> Tuple[bool, float, List[int]]:
    """
    Revisa un PDF completo para detectar texto corrupto.
    
    Returns:
        Tuple[bool, float, List[int]]: (es_corrupto, ratio_promedio, páginas_afectadas)
    """
    doc = None
    try:
        doc = fitz.open(pdf_path)
        corrupt_pages = []
        total_ratio = 0.0
        num_pages = len(doc)
        
        for page_num in range(num_pages):
            page = doc[page_num]
            text = page.get_text()
            
            is_corrupt, ratio = detect_corrupt_text(text)
            total_ratio += ratio
            
            if is_corrupt:
                corrupt_pages.append(page_num + 1)
        
        avg_ratio = total_ratio / num_pages if num_pages > 0 else 0
        is_corrupt_result = len(corrupt_pages) > 0
        
        return is_corrupt_result, avg_ratio, corrupt_pages
        
    except Exception as e:
        print(f"Error al revisar {pdf_path}: {e}")
        return False, 0.0, []
    finally:
        if doc:
            doc.close()


def check_directory_for_corruption(directory: str) -> dict:
    """
    Revisa todos los PDFs en un directorio y reporta cuáles tienen texto corrupto.
    """
    results = {}
    
    for filename in sorted(os.listdir(directory)):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            is_corrupt, ratio, pages = check_pdf_for_corruption(pdf_path)
            
            results[filename] = {
                'is_corrupt': is_corrupt,
                'corruption_ratio': ratio,
                'affected_pages': pages,
                'total_affected': len(pages)
            }
    
    return results


# ====================================================================
# FUNCIONES DE OCR
# ====================================================================

def extract_text_with_ocr(pdf_path: str, dpi: int = RENDER_DPI) -> List[Tuple[int, str]]:
    """
    Extrae texto de un PDF usando OCR.
    Renderiza cada página como imagen y aplica Tesseract.
    
    Returns:
        List[Tuple[int, str]]: Lista de (número_página, texto)
    """
    pages = []
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        print(f"  📄 Procesando {total_pages} páginas con OCR...")
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            # Renderizar página como imagen
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat)
            
            # Convertir a PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Aplicar OCR
            text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)
            
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


def extract_text_hybrid(pdf_path: str) -> List[Tuple[int, str]]:
    """
    Extrae texto de un PDF usando método híbrido:
    - Usa extracción directa para páginas sin corrupción
    - Usa OCR para páginas con texto corrupto
    
    Returns:
        List[Tuple[int, str]]: Lista de (número_página, texto)
    """
    pages = []
    ocr_count = 0
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        print(f"  📄 Procesando {total_pages} páginas (modo híbrido)...")
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            # Primero intentar extracción directa
            text = page.get_text()
            is_corrupt, ratio = detect_corrupt_text(text)
            
            if is_corrupt:
                # Usar OCR para esta página
                mat = fitz.Matrix(RENDER_DPI / 72, RENDER_DPI / 72)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)
                ocr_count += 1
            
            # Normalizar texto
            text = normalize_text(text)
            
            if text:
                pages.append((page_num + 1, text))
        
        doc.close()
        print(f"  ✅ Completado: {len(pages)} páginas ({ocr_count} con OCR)")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
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

def process_single_pdf(pdf_path: str, force_ocr: bool = False) -> dict:
    """
    Procesa un PDF individual y retorna el texto extraído.
    """
    print(f"\n🔍 Analizando: {pdf_path}")
    
    # Verificar corrupción
    is_corrupt, ratio, affected_pages = check_pdf_for_corruption(pdf_path)
    
    result = {
        'pdf_path': pdf_path,
        'is_corrupt': is_corrupt,
        'corruption_ratio': ratio,
        'affected_pages': affected_pages,
        'pages': []
    }
    
    if is_corrupt or force_ocr:
        print(f"  ⚠️  Texto corrupto detectado ({ratio*100:.1f}%)")
        print(f"  📸 Usando OCR para extracción...")
        result['pages'] = extract_text_with_ocr(pdf_path)
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
        description='Extractor OCR para PDFs con texto corrupto'
    )
    parser.add_argument(
        'path',
        help='Ruta al PDF o directorio de PDFs'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Solo verificar corrupción, no extraer texto'
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
    
    if os.path.isdir(args.path):
        # Procesar directorio
        print(f"\n📁 Escaneando directorio: {args.path}")
        results = check_directory_for_corruption(args.path)
        
        print("\n" + "=" * 60)
        print("REPORTE DE CORRUPCIÓN DE PDFs")
        print("=" * 60)
        
        corrupt_count = 0
        for filename, info in results.items():
            if info['is_corrupt']:
                corrupt_count += 1
                print(f"\n❌ {filename}")
                print(f"   Ratio de corrupción: {info['corruption_ratio']*100:.2f}%")
                print(f"   Páginas afectadas: {info['total_affected']}")
                if info['affected_pages'][:5]:
                    print(f"   Primeras páginas: {info['affected_pages'][:5]}")
            else:
                print(f"✅ {filename} - OK")
        
        print("\n" + "=" * 60)
        print(f"Total: {len(results)} PDFs, {corrupt_count} con problemas")
        
    elif os.path.isfile(args.path):
        # Procesar archivo individual
        if args.check:
            is_corrupt, ratio, pages = check_pdf_for_corruption(args.path)
            print(f"\n{'❌ CORRUPTO' if is_corrupt else '✅ OK'}")
            print(f"Ratio: {ratio*100:.2f}%")
            if pages:
                print(f"Páginas afectadas: {pages}")
        else:
            result = process_single_pdf(args.path, force_ocr=args.force_ocr)
            
            if args.output:
                # Guardar texto extraído
                with open(args.output, 'w', encoding='utf-8') as f:
                    for page_num, text in result['pages']:
                        f.write(f"\n--- Página {page_num} ---\n")
                        f.write(text)
                        f.write("\n")
                print(f"\n💾 Texto guardado en: {args.output}")
            else:
                # Mostrar resumen
                total_chars = sum(len(text) for _, text in result['pages'])
                print(f"\n📊 Resumen:")
                print(f"   Páginas extraídas: {len(result['pages'])}")
                print(f"   Caracteres totales: {total_chars:,}")
                print(f"   Método: {result['method']}")
    else:
        print(f"❌ Ruta no encontrada: {args.path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
