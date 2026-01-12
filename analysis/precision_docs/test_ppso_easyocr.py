#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba completa de procesamiento del plan PPSO con EasyOCR
"""

import os
import sys
import json
from pathlib import Path

# Importar funciones del procesador principal (desde analysis/)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)  # Subir un nivel a analysis/
sys.path.insert(0, parent_dir)

from process_plans_v6 import (
    extract_text_from_pdf,
    extract_candidate_info,
    extract_best_proposal_per_pillar,
    create_proposals_json,
    EASYOCR_AVAILABLE,
    TESSERACT_AVAILABLE,
    OCR_AVAILABLE
)

def test_ppso_processing():
    """Prueba el procesamiento completo del plan PPSO."""
    
    print("=" * 80)
    print("PRUEBA COMPLETA: PLAN PPSO CON EASYOCR")
    print("=" * 80)
    print()
    
    # Verificar estado de OCR
    print("📋 Estado de motores OCR:")
    print(f"   OCR disponible: {'✅' if OCR_AVAILABLE else '❌'}")
    print(f"   EasyOCR: {'✅' if EASYOCR_AVAILABLE else '❌'}")
    print(f"   Tesseract: {'✅' if TESSERACT_AVAILABLE else '❌'}")
    if EASYOCR_AVAILABLE:
        print("   → Usando EasyOCR como motor principal")
    elif TESSERACT_AVAILABLE:
        print("   → Usando Tesseract como fallback")
    print()
    
    # Ruta al PDF (desde precision_docs, subir un nivel)
    pdf_path = os.path.join("..", "planes", "PPSO.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"❌ Archivo no encontrado: {pdf_path}")
        return False
    
    print(f"📄 Procesando: {pdf_path}")
    print()
    
    try:
        # 1. Extraer texto
        print("🔍 Paso 1: Extracción de texto...")
        pages, full_text = extract_text_from_pdf(pdf_path)
        
        if not pages:
            print("❌ No se pudo extraer texto")
            return False
        
        print(f"   ✅ {len(pages)} páginas extraídas")
        print(f"   ✅ {len(full_text):,} caracteres totales")
        print()
        
        # 2. Extraer información del candidato
        print("🔍 Paso 2: Extracción de información del candidato...")
        pdf_id = "ppso"
        info = extract_candidate_info(pages, pdf_id)
        print(f"   ✅ Candidato: {info['candidate_name']}")
        print(f"   ✅ Partido: {info['party_name']}")
        print()
        
        # 3. Extraer propuestas
        print("🔍 Paso 3: Extracción de propuestas por pilar...")
        best_by_pillar = extract_best_proposal_per_pillar(pages, pdf_id)
        print(f"   ✅ {len(best_by_pillar)} pilares con propuestas identificadas")
        
        # Mostrar pilares encontrados
        for pillar_id, proposal in best_by_pillar.items():
            score = proposal['raw_score']
            title = proposal['title'][:60] + "..." if len(proposal['title']) > 60 else proposal['title']
            print(f"      • {pillar_id}: Score {score}/4 - {title}")
        print()
        
        # 4. Crear JSON de propuestas
        print("🔍 Paso 4: Generando estructura JSON...")
        candidate_id = "ppso"
        proposals = create_proposals_json(best_by_pillar, candidate_id, pdf_id)
        print(f"   ✅ {len(proposals)} propuestas generadas (10 pilares)")
        print()
        
        # 5. Análisis de calidad del texto
        print("🔍 Paso 5: Análisis de calidad del texto extraído...")
        
        # Verificar caracteres corruptos
        corrupt_chars = ['ӌ', 'Ǣ', 'ņ', 'Ğ', 'ļ', 'š', 'Ź', 'ĵ', 'ū', 'Ô', 'Ť', 'Ņ', 'ƕ', 'ý', 'ð', 'ų', 'ö', 'Ē', 'Ľ', 'Ě']
        corrupt_count = sum(1 for char in full_text if char in corrupt_chars)
        corrupt_ratio = corrupt_count / len(full_text) if full_text else 0
        
        print(f"   📊 Caracteres corruptos: {corrupt_count} ({corrupt_ratio*100:.2f}%)")
        
        if corrupt_ratio < 0.01:
            print("   ✅ Texto limpio (menos del 1% de caracteres corruptos)")
        elif corrupt_ratio < 0.05:
            print("   ⚠️  Texto con algunos caracteres corruptos (1-5%)")
        else:
            print("   ❌ Texto con muchos caracteres corruptos (>5%)")
        print()
        
        # 6. Muestra del texto extraído
        print("📝 Muestra del texto extraído (primeros 500 caracteres):")
        print("-" * 80)
        sample = full_text[:500]
        print(sample)
        if len(full_text) > 500:
            print(f"... ({len(full_text) - 500:,} caracteres más)")
        print("-" * 80)
        print()
        
        # 7. Resumen de propuestas
        print("📊 Resumen de propuestas extraídas:")
        print("-" * 80)
        for prop in proposals[:5]:  # Mostrar primeras 5
            pillar = prop['pillar_id']
            title = prop['proposal_title'][:50] + "..." if len(prop['proposal_title']) > 50 else prop['proposal_title']
            existence = prop['dimensions']['existence']
            when = prop['dimensions']['when']
            how = prop['dimensions']['how']
            funding = prop['dimensions']['funding']
            total = existence + when + how + funding
            print(f"   {pillar}: {title}")
            print(f"      Dimensiones: E={existence} W={when} H={how} F={funding} (Total: {total}/4)")
        print("-" * 80)
        print()
        
        # Guardar resultados de prueba
        results = {
            "pdf": "PPSO.pdf",
            "pages_extracted": len(pages),
            "total_characters": len(full_text),
            "corrupt_characters": corrupt_count,
            "corrupt_ratio": corrupt_ratio,
            "proposals_found": len(best_by_pillar),
            "ocr_engine": "EasyOCR" if EASYOCR_AVAILABLE else "Tesseract",
            "candidate_info": info,
            "sample_text": sample
        }
        
        output_file = "test_ppso_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Resultados guardados en: {output_file}")
        print()
        
        print("=" * 80)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 80)
        print()
        print("Resumen:")
        print(f"  • Páginas procesadas: {len(pages)}")
        print(f"  • Caracteres extraídos: {len(full_text):,}")
        print(f"  • Calidad del texto: {'✅ Excelente' if corrupt_ratio < 0.01 else '⚠️  Aceptable' if corrupt_ratio < 0.05 else '❌ Problemas'}")
        print(f"  • Propuestas identificadas: {len(best_by_pillar)}/10 pilares")
        print(f"  • Motor OCR usado: {'EasyOCR' if EASYOCR_AVAILABLE else 'Tesseract'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_ppso_processing()
    sys.exit(0 if success else 1)
