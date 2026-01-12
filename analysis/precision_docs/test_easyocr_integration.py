#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la integración de EasyOCR
"""

import sys
import os

# Agregar el directorio analysis/ al path (desde precision_docs)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)  # Subir un nivel a analysis/
sys.path.insert(0, parent_dir)

from process_plans_v6 import (
    EASYOCR_AVAILABLE,
    TESSERACT_AVAILABLE,
    OCR_AVAILABLE,
    extract_page_with_ocr,
    normalize_text,
    RENDER_DPI
)
import fitz

def test_ocr_integration():
    """Prueba la integración de EasyOCR con una página del plan PPSO."""
    
    print("=" * 60)
    print("PRUEBA DE INTEGRACIÓN EASYOCR")
    print("=" * 60)
    print()
    
    # Verificar disponibilidad
    print("📋 Estado de motores OCR:")
    print(f"   OCR disponible: {'✅' if OCR_AVAILABLE else '❌'}")
    print(f"   EasyOCR: {'✅' if EASYOCR_AVAILABLE else '❌'}")
    print(f"   Tesseract: {'✅' if TESSERACT_AVAILABLE else '❌'}")
    print()
    
    if not OCR_AVAILABLE:
        print("❌ No hay motores OCR disponibles")
        return False
    
    # Probar con una página del plan PPSO (desde precision_docs, subir un nivel)
    pdf_path = os.path.join("..", "planes", "PPSO.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"❌ Archivo no encontrado: {pdf_path}")
        return False
    
    print(f"📄 Probando con: {pdf_path}")
    print(f"   DPI: {RENDER_DPI}")
    print()
    
    try:
        doc = fitz.open(pdf_path)
        page = doc[3]  # Página 4 (índice 3) - tiene texto de presentación
        
        print("🔍 Extrayendo texto de la página 4...")
        text = extract_page_with_ocr(page, dpi=RENDER_DPI)
        
        if not text:
            print("❌ No se extrajo texto")
            return False
        
        print(f"✅ Texto extraído: {len(text)} caracteres")
        print()
        
        # Normalizar
        normalized = normalize_text(text)
        print(f"✅ Texto normalizado: {len(normalized)} caracteres")
        print()
        
        # Mostrar muestra
        print("📝 Muestra del texto extraído (primeros 300 caracteres):")
        print("-" * 60)
        print(normalized[:300])
        print("-" * 60)
        print()
        
        # Verificar correcciones de EasyOCR
        if "Ia " in text and "la " in normalized:
            print("✅ Corrección 'Ia' → 'la' aplicada correctamente")
        elif "Ia " in text:
            print("⚠️  'Ia' detectado pero no corregido")
        
        doc.close()
        
        print()
        print("=" * 60)
        print("✅ PRUEBA COMPLETADA")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_ocr_integration()
    sys.exit(0 if success else 1)
