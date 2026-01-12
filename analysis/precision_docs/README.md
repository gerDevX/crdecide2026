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
│   └── test_ppso_easyocr.py               # Prueba completa con plan PPSO
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

**Última actualización**: 2026-01-11
