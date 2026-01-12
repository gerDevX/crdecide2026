#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de comparación de motores OCR
Compara Tesseract, EasyOCR y PaddleOCR para evaluar fidelidad de extracción
"""

import fitz  # PyMuPDF
from PIL import Image
import io
import os
import time
from typing import List, Tuple, Dict
import json

# ====================================================================
# CONFIGURACIÓN
# ====================================================================

RENDER_DPI = 300  # Aumentado para mejor calidad

# ====================================================================
# TESSERACT (Actual)
# ====================================================================

def extract_with_tesseract(pdf_path: str, max_pages: int = None) -> Tuple[List[Tuple[int, str]], float]:
    """Extrae texto usando Tesseract OCR (método actual)."""
    try:
        import pytesseract
    except ImportError:
        return [], 0.0
    
    pages = []
    start_time = time.time()
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        pages_to_process = min(max_pages or total_pages, total_pages)
        
        for page_num in range(pages_to_process):
            page = doc[page_num]
            mat = fitz.Matrix(RENDER_DPI / 72, RENDER_DPI / 72)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            text = pytesseract.image_to_string(img, config='--oem 3 --psm 6 -l spa')
            
            if text.strip():
                pages.append((page_num + 1, text.strip()))
        
        doc.close()
        elapsed = time.time() - start_time
        
    except Exception as e:
        print(f"  ❌ Error Tesseract: {e}")
        elapsed = time.time() - start_time
    
    return pages, elapsed

# ====================================================================
# EASYOCR (Alternativa 1)
# ====================================================================

def extract_with_easyocr(pdf_path: str, max_pages: int = None) -> Tuple[List[Tuple[int, str]], float]:
    """Extrae texto usando EasyOCR (90-95% precisión, balanceado)."""
    try:
        import easyocr
    except ImportError:
        print("  ⚠️  EasyOCR no instalado. Instalar: pip install easyocr")
        return [], 0.0
    
    pages = []
    start_time = time.time()
    
    # Inicializar lector (solo una vez, reutilizable)
    try:
        reader = easyocr.Reader(['es', 'en'], gpu=False)  # Español + Inglés
    except Exception as e:
        print(f"  ❌ Error inicializando EasyOCR: {e}")
        return [], 0.0
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        pages_to_process = min(max_pages or total_pages, total_pages)
        
        for page_num in range(pages_to_process):
            page = doc[page_num]
            mat = fitz.Matrix(RENDER_DPI / 72, RENDER_DPI / 72)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Convertir PIL Image a numpy array
            import numpy as np
            img_array = np.array(img)
            
            # EasyOCR retorna lista de tuplas: (bbox, text, confidence)
            results = reader.readtext(img_array)
            
            # Combinar todos los textos detectados
            text = "\n".join([result[1] for result in results])
            
            if text.strip():
                pages.append((page_num + 1, text.strip()))
        
        doc.close()
        elapsed = time.time() - start_time
        
    except Exception as e:
        print(f"  ❌ Error EasyOCR: {e}")
        elapsed = time.time() - start_time
    
    return pages, elapsed

# ====================================================================
# PADDLEOCR (Alternativa 2 - Mayor precisión)
# ====================================================================

def extract_with_paddleocr(pdf_path: str, max_pages: int = None) -> Tuple[List[Tuple[int, str]], float]:
    """Extrae texto usando PaddleOCR (96.5% precisión, más lento)."""
    try:
        from paddleocr import PaddleOCR
    except ImportError:
        print("  ⚠️  PaddleOCR no instalado. Instalar: pip install paddlepaddle paddleocr")
        return [], 0.0
    
    pages = []
    start_time = time.time()
    
    # Inicializar OCR (solo una vez, reutilizable)
    try:
        ocr = PaddleOCR(use_angle_cls=True, lang='es', use_gpu=False)
    except Exception as e:
        print(f"  ❌ Error inicializando PaddleOCR: {e}")
        return [], 0.0
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        pages_to_process = min(max_pages or total_pages, total_pages)
        
        for page_num in range(pages_to_process):
            page = doc[page_num]
            mat = fitz.Matrix(RENDER_DPI / 72, RENDER_DPI / 72)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Convertir PIL Image a numpy array
            import numpy as np
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
            
            if text.strip():
                pages.append((page_num + 1, text.strip()))
        
        doc.close()
        elapsed = time.time() - start_time
        
    except Exception as e:
        print(f"  ❌ Error PaddleOCR: {e}")
        elapsed = time.time() - start_time
    
    return pages, elapsed

# ====================================================================
# COMPARACIÓN
# ====================================================================

def compare_ocr_engines(pdf_path: str, output_dir: str = None, max_pages: int = None) -> Dict:
    """Compara los tres motores OCR y genera reporte."""
    
    pdf_name = os.path.basename(pdf_path)
    print(f"\n{'='*60}")
    print(f"Comparando motores OCR: {pdf_name}")
    if max_pages:
        print(f"Procesando muestra de {max_pages} páginas")
    print(f"{'='*60}\n")
    
    results = {
        "pdf": pdf_name,
        "max_pages": max_pages,
        "tesseract": {},
        "easyocr": {},
        "paddleocr": {}
    }
    
    # Tesseract (actual)
    print("📸 Tesseract OCR (actual)...")
    tesseract_pages, tesseract_time = extract_with_tesseract(pdf_path, max_pages)
    tesseract_text = " ".join([text for _, text in tesseract_pages])
    results["tesseract"] = {
        "pages": len(tesseract_pages),
        "characters": len(tesseract_text),
        "time_seconds": round(tesseract_time, 2),
        "time_per_page": round(tesseract_time / len(tesseract_pages) if tesseract_pages else 0, 2)
    }
    print(f"  ✅ {len(tesseract_pages)} páginas en {tesseract_time:.2f}s")
    
    # EasyOCR
    print("\n📸 EasyOCR (alternativa 1)...")
    easyocr_pages, easyocr_time = extract_with_easyocr(pdf_path, max_pages)
    easyocr_text = " ".join([text for _, text in easyocr_pages])
    results["easyocr"] = {
        "pages": len(easyocr_pages),
        "characters": len(easyocr_text),
        "time_seconds": round(easyocr_time, 2),
        "time_per_page": round(easyocr_time / len(easyocr_pages) if easyocr_pages else 0, 2)
    }
    print(f"  ✅ {len(easyocr_pages)} páginas en {easyocr_time:.2f}s")
    
    # PaddleOCR
    print("\n📸 PaddleOCR (alternativa 2 - mayor precisión)...")
    paddleocr_pages, paddleocr_time = extract_with_paddleocr(pdf_path, max_pages)
    paddleocr_text = " ".join([text for _, text in paddleocr_pages])
    results["paddleocr"] = {
        "pages": len(paddleocr_pages),
        "characters": len(paddleocr_text),
        "time_seconds": round(paddleocr_time, 2),
        "time_per_page": round(paddleocr_time / len(paddleocr_pages) if paddleocr_pages else 0, 2)
    }
    print(f"  ✅ {len(paddleocr_pages)} páginas en {paddleocr_time:.2f}s")
    
    # Guardar textos para comparación manual
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(pdf_name)[0]
        
        # Guardar textos
        for engine, pages, text in [
            ("tesseract", tesseract_pages, tesseract_text),
            ("easyocr", easyocr_pages, easyocr_text),
            ("paddleocr", paddleocr_pages, paddleocr_text)
        ]:
            output_file = os.path.join(output_dir, f"{base_name}_{engine}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                for page_num, page_text in pages:
                    f.write(f"\n--- Página {page_num} ---\n")
                    f.write(page_text)
                    f.write("\n")
            print(f"  💾 Texto guardado: {output_file}")
        
        # Guardar reporte JSON
        report_file = os.path.join(output_dir, f"{base_name}_comparison.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"  💾 Reporte guardado: {report_file}")
    
    # Resumen
    print(f"\n{'='*60}")
    print("RESUMEN DE COMPARACIÓN")
    print(f"{'='*60}")
    print(f"{'Motor':<15} {'Páginas':<10} {'Caracteres':<12} {'Tiempo':<10} {'s/página':<10}")
    print("-" * 60)
    for engine_name, engine_data in [
        ("Tesseract", results["tesseract"]),
        ("EasyOCR", results["easyocr"]),
        ("PaddleOCR", results["paddleocr"])
    ]:
        if engine_data.get("pages", 0) > 0:
            print(f"{engine_name:<15} {engine_data['pages']:<10} {engine_data['characters']:<12} "
                  f"{engine_data['time_seconds']:<10.2f} {engine_data['time_per_page']:<10.2f}")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Compara motores OCR: Tesseract, EasyOCR, PaddleOCR'
    )
    parser.add_argument('pdf_path', help='Ruta al PDF a comparar (relativa desde analysis/ o absoluta)')
    parser.add_argument('--output', '-o', help='Directorio para guardar resultados', default='ocr_comparison_results')
    parser.add_argument('--max-pages', '-n', type=int, help='Número máximo de páginas a procesar (muestra)', default=None)
    
    args = parser.parse_args()
    
    # Si la ruta no existe, intentar con ../planes/ (desde precision_docs)
    if not os.path.exists(args.pdf_path):
        alt_path = os.path.join('..', 'planes', os.path.basename(args.pdf_path))
        if os.path.exists(alt_path):
            args.pdf_path = alt_path
        else:
            print(f"❌ Archivo no encontrado: {args.pdf_path}")
            print(f"   Intentado también: {alt_path}")
            exit(1)
    
    compare_ocr_engines(args.pdf_path, args.output, args.max_pages)
