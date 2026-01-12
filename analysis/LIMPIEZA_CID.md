# Limpieza de Caracteres CID en Extracción de PDFs

## Problema Identificado

Los caracteres CID (Character ID) aparecen en el formato `(cid:XXX)` cuando PyMuPDF no puede interpretar correctamente ciertos caracteres del PDF, especialmente en PDFs con problemas de encoding de fuentes.

**Ejemplo encontrado en PPSO:**
```
Hacienda (cid:246)(cid:286)(cid:363)(cid:253)(cid:323)(cid:325)(cid:1228) (cid:253)(cid:1228)
```

## Solución Implementada

Se agregó la función `clean_cid_characters()` en `process_plans_v7.py` que:

1. **Mapea CID comunes** a caracteres reales (letras, números, espacios)
2. **Elimina CID desconocidos** o los reemplaza con espacios según contexto
3. **Se integra automáticamente** en `normalize_text()` que se llama en todos los puntos de extracción

### Ubicación de la Función

- **Función:** `clean_cid_characters(text: str) -> str` (línea ~308)
- **Integrada en:** `normalize_text(text: str) -> str` (línea ~360)
- **Se aplica en:**
  - Extracción directa de PDF con PyMuPDF
  - Carga de archivos OCR pre-extraídos
  - Procesamiento con pdfplumber
  - Resultados de OCR (EasyOCR/Tesseract)

## Mapeo de CID Comunes

El mapeo incluye:
- **Letras ASCII** (A-Z, a-z)
- **Números** (0-9)
- **Caracteres comunes en español** (é, í, ó, etc.)
- **Espacios y separadores** comunes
- **Viñetas** (bullet points)

## Cómo Aplicar la Limpieza a Datos Existentes

### Opción 1: Reprocesar el PDF (Recomendado)

Si los datos en `proposals.json` ya tienen caracteres CID, la mejor solución es reprocesar el PDF:

```bash
cd analysis/
python process_plans_v7.py
```

Esto regenerará todos los archivos JSON con el texto limpio.

### Opción 2: Limpiar Archivo OCR Pre-extraído

Si existe un archivo `ppso_ocr_text.txt` en `analysis/data/`, puede limpiarse manualmente:

```python
from process_plans_v7 import clean_cid_characters

with open('data/ppso_ocr_text.txt', 'r', encoding='utf-8') as f:
    content = f.read()

cleaned = clean_cid_characters(content)

with open('data/ppso_ocr_text.txt', 'w', encoding='utf-8') as f:
    f.write(cleaned)
```

### Opción 3: Script de Limpieza de JSON Existente

Si necesita limpiar `proposals.json` directamente (no recomendado, mejor reprocesar):

```python
import json
from process_plans_v7 import clean_cid_characters

with open('data/proposals.json', 'r', encoding='utf-8') as f:
    proposals = json.load(f)

for proposal in proposals:
    for field in ['proposal_text', 'proposal_title', 'when_text', 'how_text', 'funding_text']:
        if field in proposal and proposal[field]:
            proposal[field] = clean_cid_characters(proposal[field])

with open('data/proposals.json', 'w', encoding='utf-8') as f:
    json.dump(proposals, f, ensure_ascii=False, indent=2)
```

## Verificación

Para verificar que la limpieza funciona:

```python
from process_plans_v7 import clean_cid_characters

test_text = "Hacienda (cid:246)(cid:286)(cid:363)(cid:253)(cid:323)(cid:325)(cid:1228) (cid:253)(cid:1228)"
cleaned = clean_cid_characters(test_text)
print(f"Antes: {test_text}")
print(f"Después: {cleaned}")
```

## Notas Importantes

1. **Los CID son específicos de cada PDF**: El mapeo es aproximado y puede no ser 100% preciso para todos los casos
2. **Mejor usar OCR**: Para PDFs con muchos CID, es mejor usar OCR (EasyOCR/Tesseract) que extracción directa
3. **Archivos OCR pre-extraídos**: Si existe un archivo `{pdf_id}_ocr_text.txt`, se usará en lugar de extraer del PDF
4. **Reprocesamiento**: La solución más limpia es reprocesar el PDF completo con la nueva función

## Estado Actual

✅ Función `clean_cid_characters()` implementada
✅ Integrada en `normalize_text()`
✅ Se aplica automáticamente en todas las extracciones
⚠️ Datos existentes en `proposals.json` necesitan reprocesamiento

## Próximos Pasos

1. Reprocesar el PDF de PPSO: `python process_plans_v7.py`
2. Verificar que los caracteres CID se hayan limpiado correctamente
3. Si persisten problemas, considerar usar OCR para PPSO específicamente
