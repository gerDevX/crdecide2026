# Documentación de Precisión y Comparaciones

Esta carpeta contiene toda la documentación relacionada con la evaluación de precisión, comparación de librerías y mejoras en la extracción de texto.

## Estructura

```
precision_docs/
├── README.md                          # Este archivo
│
├── 📊 Análisis y Documentación
│   ├── ANALISIS_LIBRERIAS_PDF.md          # Comparación de librerías de lectura PDF
│   ├── ANALISIS_FIDELIDAD_PDF_LIMPIOS.md  # Análisis de fidelidad para PDFs limpios
│   ├── RESUMEN_INTEGRACION_PDFPLUMBER.md  # Integración de pdfplumber
│   ├── RESUMEN_INTEGRACION_EASYOCR.md     # Integración de EasyOCR
│   ├── CHANGELOG_EASYOCR.md               # Changelog de cambios EasyOCR
│   └── README_OCR.md                      # Guía de OCR
│
├── 🔧 Scripts de Comparación
│   ├── ocr_comparison.py                  # Compara Tesseract, EasyOCR, PaddleOCR
│   ├── pdf_library_comparison.py          # Compara PyMuPDF, pdfplumber, pypdf, pdfminer
│   ├── ocr_extractor.py                   # Extractor OCR original (Tesseract)
│   ├── ocr_extractor_v2.py                # Extractor OCR mejorado (múltiples motores)
│   ├── test_easyocr_integration.py        # Prueba de integración EasyOCR
│   ├── test_ppso_easyocr.py               # Prueba completa con plan PPSO
│   └── simulate_multiple_proposals.py      # Simulación sistema de bonos múltiples propuestas
│
└── 📈 Resultados de Comparación
    ├── pdf_library_comparison.json        # Resultados de comparación de librerías PDF
    ├── test_ppso_results.json            # Resultados de prueba con PPSO
    └── ocr_comparison_results/             # Resultados de comparación OCR
        ├── COMPARACION_DETALLADA.md       # Comparación detallada Tesseract vs EasyOCR
        ├── RESUMEN_COMPARACION.md         # Resumen de comparación OCR
        ├── PPSO_tesseract.txt             # Texto extraído con Tesseract
        ├── PPSO_easyocr.txt               # Texto extraído con EasyOCR
        ├── PPSO_paddleocr.txt             # Texto extraído con PaddleOCR
        └── PPSO_comparison.json           # Métricas de comparación OCR
```

## Documentos Principales

### Análisis de Librerías PDF
- **ANALISIS_LIBRERIAS_PDF.md**: Comparación completa de PyMuPDF, pdfplumber, pypdf y pdfminer.six
- **ANALISIS_FIDELIDAD_PDF_LIMPIOS.md**: Análisis específico para PDFs sin corrupción
- **pdf_library_comparison.py**: Script que genera la comparación

### Integraciones
- **RESUMEN_INTEGRACION_PDFPLUMBER.md**: Documentación de la integración de pdfplumber
- **RESUMEN_INTEGRACION_EASYOCR.md**: Documentación de la integración de EasyOCR
- **CHANGELOG_EASYOCR.md**: Historial de cambios relacionados con EasyOCR

### OCR
- **README_OCR.md**: Guía completa sobre motores OCR y recomendaciones
- **ocr_comparison_results/**: Resultados detallados de comparación entre Tesseract y EasyOCR
- **ocr_comparison.py**: Script que genera la comparación OCR
- **ocr_extractor.py** / **ocr_extractor_v2.py**: Extractores OCR (versiones)

### Scripts de Prueba
- **test_easyocr_integration.py**: Prueba de integración EasyOCR
- **test_ppso_easyocr.py**: Prueba completa con plan PPSO
- **simulate_multiple_proposals.py**: Simula sistema de bonos por múltiples propuestas

### Análisis de Múltiples Propuestas
- **ANALISIS_MULTIPLES_PROPUESTAS.md**: Análisis del sistema actual
- **PROPUESTA_SISTEMA_BONOS.md**: Propuesta detallada de sistema de bonos (versión original)
- **PROPUESTA_SISTEMA_BONOS_SIMPLIFICADO.md**: Sistema simplificado (solo 3 propuestas) ⭐
- **RESUMEN_SISTEMA_SIMPLIFICADO.md**: Resumen ejecutivo del sistema simplificado ⭐
- **RECOMENDACIONES_MULTIPLES_PROPUESTAS.md**: Recomendaciones estratégicas

### Análisis de Viabilidad Legal y Realista
- **ANALISIS_DIMENSIONES_VIABILIDAD.md**: Análisis detallado de dimensiones y viabilidad
- **PROPUESTA_DIMENSIONES_MEJORADAS.md**: Propuesta técnica de dimensiones mejoradas ⭐
- **RESUMEN_VIABILIDAD_LEGAL.md**: Resumen ejecutivo con ejemplos de Costa Rica ⭐
- **ANALISIS_REFORMA_CONSTITUCIONAL.md**: Análisis de detección de reforma constitucional
- **MEJORA_DETECCION_REFORMA_CONSTITUCIONAL.md**: Mejora en precisión de detección ⭐
- **REVISION_PENALIZACION_REFORMA_CONSTITUCIONAL.md**: Revisión y eliminación de penalización ⭐
- **RESUMEN_REVISION_VIABILIDAD.md**: Resumen de revisión del sistema ⭐
- **ANALISIS_INCONSTITUCIONALIDAD.md**: Análisis de detección ampliada de inconstitucionalidad ⭐
- **IMPLEMENTACION_VIABILIDAD_AMPLIADA.md**: Implementación de detección ampliada ⭐

## Uso de los Scripts

Los scripts están configurados para ejecutarse desde `precision_docs/` y usar rutas relativas:

```bash
# Desde analysis/precision_docs/
cd precision_docs

# Comparar motores OCR
python3 ocr_comparison.py ../planes/PPSO.pdf --max-pages 5

# Comparar librerías PDF
python3 pdf_library_comparison.py ../planes/PA.pdf --max-pages 5

# Probar integración EasyOCR
python3 test_easyocr_integration.py

# Probar procesamiento completo PPSO
python3 test_ppso_easyocr.py
```

**Nota**: Todos los scripts buscan automáticamente en `../planes/` si la ruta proporcionada no existe.

## Estrategia Actual Implementada

### Extracción de PDFs
1. **Detección rápida**: PyMuPDF analiza primeras 10 páginas
2. **Si corrupción > 5%**: Usa pdfplumber (calidad, 0% corruptos)
3. **Si PDF limpio**: Usa PyMuPDF (velocidad, fidedigno)
4. **Fallback**: EasyOCR/Tesseract si pdfplumber falla

### Motores OCR
- **Principal**: EasyOCR (mejor calidad)
- **Fallback**: Tesseract (si EasyOCR no disponible)

## Resultados Clave

### pdfplumber vs PyMuPDF (PDFs corruptos)
- **pdfplumber**: 0% corruptos, 957K caracteres, 16.25s
- **PyMuPDF**: 29.46% corruptos, 234K caracteres, 0.29s

### EasyOCR vs Tesseract
- **EasyOCR**: 0% corruptos, mejor reconocimiento de palabras
- **Tesseract**: Algunos caracteres corruptos, más rápido

### PyMuPDF para PDFs limpios
- **Velocidad**: 20-50x más rápido que alternativas
- **Calidad**: 0% corruptos, 100% legible
- **Fidelidad**: Texto fiel al original

---

## Implementaciones Recientes

### Sistema de Bonos por Múltiples Propuestas (v7)
- **Estado**: ✅ Implementado
- **Documentación**: `PROPUESTA_SISTEMA_BONOS_SIMPLIFICADO.md`, `RESUMEN_SISTEMA_SIMPLIFICADO.md`
- **Script**: `simulate_multiple_proposals.py`

### Verificación de Viabilidad Legal (v7)
- **Fase 1 Inicial**: ✅ Implementado (reforma constitucional + separación de poderes)
- **Fase 1 Revisada**: ✅ Implementado (solo separación de poderes, eliminada reforma constitucional)
- **Fase 1 Ampliada**: ✅ Implementado (separación de poderes + derechos fundamentales + garantías + procedimientos)
- **Documentación**: 
  - `ANALISIS_DIMENSIONES_VIABILIDAD.md`
  - `IMPLEMENTACION_VIABILIDAD_FASE1.md`
  - `RESULTADOS_PRUEBA_VIABILIDAD_FASE1.md`
  - `REVISION_PENALIZACION_REFORMA_CONSTITUCIONAL.md`
  - `RESUMEN_REVISION_VIABILIDAD.md`
  - `ANALISIS_INCONSTITUCIONALIDAD.md`
  - `IMPLEMENTACION_VIABILIDAD_AMPLIADA.md`

---

**Última actualización**: 2026-01-11
