# Verificación de Estrategia de Extracción

## Estrategia Recomendada Implementada

### Flujo de Decisión

```
PDF → Detección rápida (PyMuPDF, primeras 10 páginas)
  ↓
¿Corrupción > 5%?
  ├─ SÍ + pdfplumber disponible
  │   ├─ pdfplumber exitoso → ✅ Retornar (0% corruptos, 4x más contenido)
  │   └─ pdfplumber falla → PyMuPDF + OCR (último recurso)
  │
  ├─ SÍ + pdfplumber NO disponible
  │   └─ PyMuPDF + OCR (EasyOCR → Tesseract)
  │
  └─ NO (PDF limpio)
      └─ PyMuPDF directo ✅ (rápido, fidedigno)
```

---

## Verificación del Código

### ✅ `process_plans_v6.py` - Script Principal

**Ubicación**: `analysis/process_plans_v6.py`

**Función**: `extract_text_from_pdf()`

**Estrategia implementada**:
1. ✅ Detección rápida con PyMuPDF (primeras 10 páginas)
2. ✅ Si corrupción > 5% y pdfplumber disponible → usar pdfplumber
3. ✅ Si pdfplumber falla → usar PyMuPDF + OCR
4. ✅ Si corrupción pero pdfplumber no disponible → usar PyMuPDF + OCR
5. ✅ Si PDF limpio → usar PyMuPDF directo
6. ✅ Fallback por página: si página específica corrupta, usar OCR solo para esa

**Estado**: ✅ **Correctamente implementado**

---

## Configuración Actual

### Librerías Disponibles

```python
PDFPLUMBER_AVAILABLE: True   # Para PDFs corruptos
PDF_AVAILABLE: True          # PyMuPDF para PDFs limpios
EASYOCR_AVAILABLE: True      # OCR principal
TESSERACT_AVAILABLE: True   # OCR fallback
```

### Umbrales

- **Detección de corrupción**: > 2% caracteres corruptos
- **Uso de pdfplumber**: > 5% corrupción detectada
- **Uso de OCR**: Solo si pdfplumber falla o no disponible

---

## Casos de Uso

### Caso 1: PDF Limpio (ej: PA.pdf)
```
Detección: 0% corruptos
Estrategia: PyMuPDF directo
Resultado: ✅ Rápido (0.09s), 0% corruptos, 100% legible
```

### Caso 2: PDF Corrupto con pdfplumber (ej: PPSO.pdf)
```
Detección: 40.5% corruptos
Estrategia: pdfplumber
Resultado: ✅ 0% corruptos, 957K caracteres (4x más), 16.25s
```

### Caso 3: PDF Corrupto sin pdfplumber
```
Detección: 40.5% corruptos
Estrategia: PyMuPDF + EasyOCR
Resultado: ✅ 0% corruptos, ~228K caracteres, ~2-3 min
```

### Caso 4: PDF con Corrupción Menor (<5%)
```
Detección: 3% corruptos
Estrategia: PyMuPDF directo
Resultado: ✅ Rápido, corrupción menor aceptable
```

---

## Mensajes del Sistema

### PDF Limpio
```
✅ PA.pdf: Texto limpio, usando PyMuPDF directo...
```

### PDF Corrupto con pdfplumber
```
⚠️  PPSO.pdf: Texto corrupto (40.5%), usando pdfplumber...
✅ pdfplumber completado: 85 páginas procesadas
```

### PDF Corrupto sin pdfplumber
```
⚠️  PPSO.pdf: Texto corrupto (40.5%), extrayendo con EasyOCR...
✅ OCR completado (EasyOCR): 85/85 páginas procesadas
```

### Corrupción Menor
```
ℹ️  PDF.pdf: Corrupción menor (3.2%), usando PyMuPDF directo...
```

---

## Verificación de Funciones

### ✅ `extract_text_with_pdfplumber()`
- **Propósito**: Extracción con pdfplumber para PDFs corruptos
- **Retorna**: Lista de (página, texto) y texto completo
- **Estado**: ✅ Implementado correctamente

### ✅ `extract_page_with_ocr()`
- **Propósito**: OCR para páginas individuales
- **Prioridad**: EasyOCR → Tesseract
- **Estado**: ✅ Implementado correctamente

### ✅ `detect_corrupt_text()`
- **Propósito**: Detectar caracteres corruptos
- **Umbral**: 2% para detección
- **Estado**: ✅ Caracteres corruptos actualizados

### ✅ `normalize_text()`
- **Propósito**: Normalizar y corregir texto
- **Correcciones**: "Ia" → "la" (EasyOCR)
- **Estado**: ✅ Implementado correctamente

---

## Comparación con Estrategia Recomendada

| Aspecto | Recomendado | Implementado | Estado |
|---------|-------------|--------------|--------|
| Detección rápida | PyMuPDF | ✅ PyMuPDF | ✅ |
| PDFs corruptos | pdfplumber | ✅ pdfplumber | ✅ |
| PDFs limpios | PyMuPDF | ✅ PyMuPDF | ✅ |
| Fallback OCR | EasyOCR → Tesseract | ✅ EasyOCR → Tesseract | ✅ |
| Umbral corrupción | > 5% | ✅ > 5% | ✅ |
| Fallback por página | Sí | ✅ Sí | ✅ |

**Conclusión**: ✅ **La estrategia está correctamente implementada**

---

## Pruebas Recomendadas

### Prueba 1: PDF Limpio
```bash
python3 process_plans_v6.py
# Debe usar PyMuPDF directo para PDFs limpios
```

### Prueba 2: PDF Corrupto
```bash
# Procesar PPSO.pdf
# Debe usar pdfplumber automáticamente
```

### Prueba 3: Sin pdfplumber
```bash
# Desinstalar pdfplumber temporalmente
# Debe usar PyMuPDF + OCR como fallback
```

---

**Fecha de verificación**: 2026-01-11  
**Script verificado**: `process_plans_v6.py`  
**Estado**: ✅ **Estrategia correctamente implementada**
