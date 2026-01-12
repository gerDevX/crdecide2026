#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparación de librerías de lectura de PDFs
Compara PyMuPDF, pdfplumber, pypdf y pdfminer.six
"""

import os
import time
import json
from typing import Dict, List, Tuple

# ====================================================================
# PYMUPDF (Actual)
# ====================================================================

def extract_with_pymupdf(pdf_path: str) -> Tuple[str, float, int]:
    """Extrae texto usando PyMuPDF (fitz) - librería actual."""
    try:
        import fitz
    except ImportError:
        return "", 0.0, 0
    
    start_time = time.time()
    text = ""
    pages = 0
    
    try:
        doc = fitz.open(pdf_path)
        pages = len(doc)
        
        for page_num in range(pages):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        elapsed = time.time() - start_time
        
    except Exception as e:
        print(f"  ❌ Error PyMuPDF: {e}")
        elapsed = time.time() - start_time
    
    return text, elapsed, pages

# ====================================================================
# PDFPLUMBER (Alternativa 1 - Mejor para tablas y estructura)
# ====================================================================

def extract_with_pdfplumber(pdf_path: str) -> Tuple[str, float, int]:
    """Extrae texto usando pdfplumber - mejor para documentos estructurados."""
    try:
        import pdfplumber
    except ImportError:
        return "", 0.0, 0
    
    start_time = time.time()
    text = ""
    pages = 0
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = len(pdf.pages)
            
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        elapsed = time.time() - start_time
        
    except Exception as e:
        print(f"  ❌ Error pdfplumber: {e}")
        elapsed = time.time() - start_time
    
    return text, elapsed, pages

# ====================================================================
# PYPDF (Alternativa 2 - Puro Python, fácil instalación)
# ====================================================================

def extract_with_pypdf(pdf_path: str) -> Tuple[str, float, int]:
    """Extrae texto usando pypdf - puro Python."""
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return "", 0.0, 0
    
    start_time = time.time()
    text = ""
    pages = 0
    
    try:
        reader = PdfReader(pdf_path)
        pages = len(reader.pages)
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        elapsed = time.time() - start_time
        
    except Exception as e:
        print(f"  ❌ Error pypdf: {e}")
        elapsed = time.time() - start_time
    
    return text, elapsed, pages

# ====================================================================
# PDFMINER.SIX (Alternativa 3 - Detallado pero lento)
# ====================================================================

def extract_with_pdfminer(pdf_path: str) -> Tuple[str, float, int]:
    """Extrae texto usando pdfminer.six - muy detallado."""
    try:
        from pdfminer.high_level import extract_text
    except ImportError:
        return "", 0.0, 0
    
    start_time = time.time()
    text = ""
    pages = 0
    
    try:
        text = extract_text(pdf_path)
        
        # Contar páginas aproximado (pdfminer no da número directo)
        try:
            from pdfminer.pdfpage import PDFPage
            from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
            from pdfminer.converter import TextConverter
            from io import StringIO
            
            with open(pdf_path, 'rb') as file:
                pages = len(list(PDFPage.get_pages(file)))
        except:
            pages = text.count('\n\n') // 10  # Estimación
        
        elapsed = time.time() - start_time
        
    except Exception as e:
        print(f"  ❌ Error pdfminer: {e}")
        elapsed = time.time() - start_time
    
    return text, elapsed, pages

# ====================================================================
# ANÁLISIS DE CALIDAD
# ====================================================================

def analyze_text_quality(text: str, library_name: str) -> Dict:
    """Analiza la calidad del texto extraído."""
    if not text:
        return {
            "characters": 0,
            "words": 0,
            "corrupt_chars": 0,
            "corrupt_ratio": 0.0,
            "readable_ratio": 0.0
        }
    
    # Caracteres corruptos comunes
    corrupt_chars = set([
        '\uf0b7', '\uf0a7', '\uf0d8', '\uf020', '\uf06c', '\uf06f', '\uf073',
        '\uf061', '\uf065', '\uf06e', '\uf072', '\uf074', '\uf075', '\uf069',
        '\uf064', '\uf063', '\uf06d', '\uf070', '\uf067', '\uf0fc', '\uf0e0',
        'ӌ', 'Ǣ', 'ņ', 'Ğ', 'ļ', 'š', 'Ź', 'ĵ', 'ū', 'Ô', 'Ť', 'Ņ', 'ƕ', 'ý', 'ð', 'ų', 'ö', 'Ē', 'Ľ', 'Ě'
    ])
    
    total_chars = len(text)
    corrupt_count = sum(1 for char in text if char in corrupt_chars)
    corrupt_ratio = corrupt_count / total_chars if total_chars > 0 else 0
    
    # Contar palabras (aproximado)
    words = len(text.split())
    
    # Ratio de texto legible (sin caracteres corruptos)
    readable_ratio = 1.0 - corrupt_ratio
    
    return {
        "characters": total_chars,
        "words": words,
        "corrupt_chars": corrupt_count,
        "corrupt_ratio": round(corrupt_ratio, 4),
        "readable_ratio": round(readable_ratio, 4)
    }

# ====================================================================
# COMPARACIÓN
# ====================================================================

def compare_pdf_libraries(pdf_path: str, max_pages: int = None) -> Dict:
    """Compara todas las librerías de lectura de PDFs."""
    
    pdf_name = os.path.basename(pdf_path)
    print(f"\n{'='*80}")
    print(f"COMPARACIÓN DE LIBRERÍAS DE LECTURA DE PDFs")
    print(f"Archivo: {pdf_name}")
    if max_pages:
        print(f"Procesando muestra de {max_pages} páginas")
    print(f"{'='*80}\n")
    
    results = {
        "pdf": pdf_name,
        "max_pages": max_pages,
        "libraries": {}
    }
    
    # 1. PyMuPDF (Actual)
    print("📚 PyMuPDF (fitz) - Actual...")
    pymupdf_text, pymupdf_time, pymupdf_pages = extract_with_pymupdf(pdf_path)
    if pymupdf_text:
        pymupdf_quality = analyze_text_quality(pymupdf_text, "PyMuPDF")
        results["libraries"]["pymupdf"] = {
            "available": True,
            "pages": pymupdf_pages,
            "time_seconds": round(pymupdf_time, 2),
            "time_per_page": round(pymupdf_time / pymupdf_pages if pymupdf_pages > 0 else 0, 2),
            **pymupdf_quality
        }
        print(f"  ✅ {pymupdf_pages} páginas en {pymupdf_time:.2f}s")
        print(f"     Caracteres: {pymupdf_quality['characters']:,} | Corruptos: {pymupdf_quality['corrupt_chars']} ({pymupdf_quality['corrupt_ratio']*100:.2f}%)")
    else:
        results["libraries"]["pymupdf"] = {"available": False}
        print("  ❌ No disponible")
    print()
    
    # 2. pdfplumber
    print("📚 pdfplumber - Alternativa 1...")
    pdfplumber_text, pdfplumber_time, pdfplumber_pages = extract_with_pdfplumber(pdf_path)
    if pdfplumber_text:
        pdfplumber_quality = analyze_text_quality(pdfplumber_text, "pdfplumber")
        results["libraries"]["pdfplumber"] = {
            "available": True,
            "pages": pdfplumber_pages,
            "time_seconds": round(pdfplumber_time, 2),
            "time_per_page": round(pdfplumber_time / pdfplumber_pages if pdfplumber_pages > 0 else 0, 2),
            **pdfplumber_quality
        }
        print(f"  ✅ {pdfplumber_pages} páginas en {pdfplumber_time:.2f}s")
        print(f"     Caracteres: {pdfplumber_quality['characters']:,} | Corruptos: {pdfplumber_quality['corrupt_chars']} ({pdfplumber_quality['corrupt_ratio']*100:.2f}%)")
    else:
        results["libraries"]["pdfplumber"] = {"available": False}
        print("  ⚠️  No disponible. Instalar: pip install pdfplumber")
    print()
    
    # 3. pypdf
    print("📚 pypdf - Alternativa 2...")
    pypdf_text, pypdf_time, pypdf_pages = extract_with_pypdf(pdf_path)
    if pypdf_text:
        pypdf_quality = analyze_text_quality(pypdf_text, "pypdf")
        results["libraries"]["pypdf"] = {
            "available": True,
            "pages": pypdf_pages,
            "time_seconds": round(pypdf_time, 2),
            "time_per_page": round(pypdf_time / pypdf_pages if pypdf_pages > 0 else 0, 2),
            **pypdf_quality
        }
        print(f"  ✅ {pypdf_pages} páginas en {pypdf_time:.2f}s")
        print(f"     Caracteres: {pypdf_quality['characters']:,} | Corruptos: {pypdf_quality['corrupt_chars']} ({pypdf_quality['corrupt_ratio']*100:.2f}%)")
    else:
        results["libraries"]["pypdf"] = {"available": False}
        print("  ⚠️  No disponible. Instalar: pip install pypdf")
    print()
    
    # 4. pdfminer.six
    print("📚 pdfminer.six - Alternativa 3...")
    pdfminer_text, pdfminer_time, pdfminer_pages = extract_with_pdfminer(pdf_path)
    if pdfminer_text:
        pdfminer_quality = analyze_text_quality(pdfminer_text, "pdfminer")
        results["libraries"]["pdfminer"] = {
            "available": True,
            "pages": pdfminer_pages,
            "time_seconds": round(pdfminer_time, 2),
            "time_per_page": round(pdfminer_time / pdfminer_pages if pdfminer_pages > 0 else 0, 2),
            **pdfminer_quality
        }
        print(f"  ✅ {pdfminer_pages} páginas en {pdfminer_time:.2f}s")
        print(f"     Caracteres: {pdfminer_quality['characters']:,} | Corruptos: {pdfminer_quality['corrupt_chars']} ({pdfminer_quality['corrupt_ratio']*100:.2f}%)")
    else:
        results["libraries"]["pdfminer"] = {"available": False}
        print("  ⚠️  No disponible. Instalar: pip install pdfminer.six")
    print()
    
    # Comparación de muestras de texto
    print("="*80)
    print("MUESTRAS DE TEXTO EXTRAÍDO (primeros 300 caracteres)")
    print("="*80)
    
    if pymupdf_text:
        print("\n📚 PyMuPDF:")
        print("-" * 80)
        print(pymupdf_text[:300])
        print("-" * 80)
    
    if pdfplumber_text:
        print("\n📚 pdfplumber:")
        print("-" * 80)
        print(pdfplumber_text[:300])
        print("-" * 80)
    
    if pypdf_text:
        print("\n📚 pypdf:")
        print("-" * 80)
        print(pypdf_text[:300])
        print("-" * 80)
    
    if pdfminer_text:
        print("\n📚 pdfminer.six:")
        print("-" * 80)
        print(pdfminer_text[:300])
        print("-" * 80)
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE COMPARACIÓN")
    print("="*80)
    print(f"{'Librería':<15} {'Disponible':<12} {'Páginas':<10} {'Tiempo':<10} {'Caracteres':<12} {'Corruptos %':<12} {'Legible %':<12}")
    print("-" * 80)
    
    for lib_name, lib_data in results["libraries"].items():
        if lib_data.get("available"):
            print(f"{lib_name:<15} {'✅':<12} {lib_data['pages']:<10} {lib_data['time_seconds']:<10.2f} "
                  f"{lib_data['characters']:<12,} {lib_data['corrupt_ratio']*100:<12.2f}% {lib_data['readable_ratio']*100:<12.2f}%")
        else:
            print(f"{lib_name:<15} {'❌':<12} {'-':<10} {'-':<10} {'-':<12} {'-':<12} {'-':<12}")
    
    # Guardar resultados (en el directorio actual de precision_docs)
    output_file = "pdf_library_comparison.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Compara librerías de lectura de PDFs'
    )
    parser.add_argument('pdf_path', help='Ruta al PDF a comparar (relativa desde analysis/ o absoluta)')
    parser.add_argument('--max-pages', '-n', type=int, help='Número máximo de páginas a procesar', default=None)
    
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
    
    compare_pdf_libraries(args.pdf_path, args.max_pages)
