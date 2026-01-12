# Guía de Mejora de OCR - Costa Rica Decide 2026

## Análisis Actual

### Stack Actual
- **PyMuPDF (fitz)**: Extracción directa de texto
- **Tesseract OCR**: Para PDFs con texto corrupto
- **DPI**: 200 (configurable)
- **Configuración**: `--oem 3 --psm 6 -l spa`

### Problemas Identificados
1. **Calidad de OCR**: El texto extraído muestra:
   - Caracteres extraños y mal reconocidos
   - Espacios mal ubicados
   - Errores en reconocimiento de acentos y caracteres especiales
   - Problemas con tablas y formato complejo

2. **Precisión estimada**: ~85-90% (basado en benchmarks de Tesseract)

---

## Recomendaciones

### 🥇 Opción 1: PaddleOCR (RECOMENDADO)

**Ventajas:**
- ✅ **96.5% de precisión** (mejor que Tesseract)
- ✅ Excelente con español
- ✅ Mejor manejo de tablas y formato complejo
- ✅ Soporte para detección de orientación de texto
- ✅ Open source y gratuito

**Desventajas:**
- ⚠️ Más lento (~4.85s por página vs 0.77s de Tesseract)
- ⚠️ Requiere más memoria RAM
- ⚠️ Instalación más compleja (requiere PaddlePaddle)

**Instalación:**
```bash
# CPU version (recomendado para empezar)
pip install paddlepaddle paddleocr

# GPU version (si tienes CUDA)
pip install paddlepaddle-gpu paddleocr
```

**Uso:**
```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='es', use_gpu=False)
results = ocr.ocr(img_array, cls=True)
```

---

### 🥈 Opción 2: EasyOCR (ALTERNATIVA BALANCEADA)

**Ventajas:**
- ✅ **90-95% de precisión** (mejor que Tesseract)
- ✅ Más rápido que PaddleOCR (~1.2s por página)
- ✅ Fácil instalación
- ✅ Soporte para 80+ idiomas
- ✅ Buen balance precisión/velocidad

**Desventajas:**
- ⚠️ Menos preciso que PaddleOCR
- ⚠️ Puede tener problemas con texto muy pequeño

**Instalación:**
```bash
pip install easyocr
```

**Uso:**
```python
import easyocr

reader = easyocr.Reader(['es', 'en'], gpu=False)
results = reader.readtext(img_array)
```

---

### 🥉 Opción 3: Mejorar Tesseract Actual

**Mejoras sugeridas:**
1. **Aumentar DPI**: De 200 a 300-400 para mejor calidad
2. **Preprocesamiento de imágenes**:
   - Aumentar contraste
   - Binarización (blanco/negro)
   - Desenfoque suave para reducir ruido
3. **Ajustar PSM (Page Segmentation Mode)**:
   - `--psm 1`: Orientación y detección de script
   - `--psm 3`: Completamente automático
   - `--psm 6`: Asume bloque uniforme de texto (actual)
4. **Usar modelo entrenado específico para español**

---

## Comparación de Motores

| Motor | Precisión | Velocidad | Instalación | Recomendación |
|-------|-----------|-----------|-------------|---------------|
| **Tesseract** (actual) | 85-90% | ⚡⚡⚡ Rápido (0.77s/página) | Fácil | Mantener si velocidad es crítica |
| **EasyOCR** | 90-95% | ⚡⚡ Medio (1.2s/página) | Fácil | **Mejor balance** |
| **PaddleOCR** | **96.5%** | ⚡ Lento (4.85s/página) | Media | **Mejor precisión** |

---

## Scripts Disponibles

### 1. `ocr_comparison.py`
Compara los tres motores OCR en un PDF específico:
```bash
python ocr_comparison.py planes/PPSO.pdf --output comparison_results
```

Genera:
- Textos extraídos por cada motor
- Reporte JSON con métricas (tiempo, caracteres, etc.)
- Permite comparación manual de calidad

### 2. `ocr_extractor_v2.py`
Versión mejorada del extractor con soporte para múltiples motores:
```bash
# Usar Tesseract (actual)
python ocr_extractor_v2.py planes/PPSO.pdf --engine tesseract

# Usar EasyOCR
python ocr_extractor_v2.py planes/PPSO.pdf --engine easyocr

# Usar PaddleOCR
python ocr_extractor_v2.py planes/PPSO.pdf --engine paddleocr
```

---

## Plan de Migración Recomendado

### Fase 1: Evaluación (1-2 días)
1. Ejecutar `ocr_comparison.py` en 2-3 PDFs problemáticos
2. Comparar manualmente la calidad de extracción
3. Medir tiempos de procesamiento

### Fase 2: Prueba Piloto (3-5 días)
1. Integrar EasyOCR o PaddleOCR en `process_plans_v6.py`
2. Procesar todos los PDFs con el nuevo motor
3. Comparar resultados con versión anterior
4. Validar que las propuestas extraídas son más precisas

### Fase 3: Optimización (opcional)
1. Ajustar DPI según resultados
2. Implementar preprocesamiento de imágenes si es necesario
3. Considerar procesamiento en paralelo para múltiples páginas

---

## Integración en `process_plans_v6.py`

### Cambio Mínimo (Solo función OCR)

Reemplazar la función `extract_page_with_ocr`:

```python
# ANTES (Tesseract)
def extract_page_with_ocr(page, dpi: int = RENDER_DPI) -> str:
    if not OCR_AVAILABLE:
        return ""
    try:
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)
        return text
    except Exception as e:
        print(f"    ⚠️  Error OCR en página: {e}")
        return ""

# DESPUÉS (PaddleOCR - ejemplo)
def extract_page_with_ocr(page, dpi: int = RENDER_DPI, ocr=None) -> str:
    if not OCR_AVAILABLE:
        return ""
    try:
        from paddleocr import PaddleOCR
        import numpy as np
        
        if ocr is None:
            ocr = PaddleOCR(use_angle_cls=True, lang='es', use_gpu=False)
        
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        img_array = np.array(img)
        
        results = ocr.ocr(img_array, cls=True)
        text_lines = []
        if results and results[0]:
            for line in results[0]:
                if line and len(line) >= 2:
                    text_lines.append(line[1][0])
        
        return "\n".join(text_lines)
    except Exception as e:
        print(f"    ⚠️  Error OCR en página: {e}")
        return ""
```

**Nota**: Inicializar el objeto OCR una sola vez fuera del loop de páginas para mejor rendimiento.

---

## Consideraciones Adicionales

### APIs de Nube (Alternativa Premium)
Si el presupuesto lo permite, considerar:
- **Google Cloud Vision API**: ~99% precisión, pero requiere API key y tiene costos
- **AWS Textract**: Excelente para documentos estructurados
- **Azure Computer Vision**: Buena integración con otros servicios Azure

**Ventajas**: Mayor precisión, menos mantenimiento  
**Desventajas**: Costos, dependencia de internet, límites de uso

### Preprocesamiento de Imágenes
Mejoras adicionales que pueden aumentar precisión:
```python
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(img: Image.Image) -> Image.Image:
    # Convertir a escala de grises
    img = img.convert('L')
    
    # Aumentar contraste
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    # Aplicar filtro de desenfoque suave
    img = img.filter(ImageFilter.SMOOTH)
    
    return img
```

---

## Conclusión

**Recomendación final**: 
1. **Corto plazo**: Probar **EasyOCR** (balance precisión/velocidad)
2. **Largo plazo**: Migrar a **PaddleOCR** si la precisión es crítica
3. **Mantener Tesseract** como fallback si los otros fallan

La mejora esperada en fidelidad de extracción es de **5-10 puntos porcentuales**, lo que debería resultar en:
- Menos errores en reconocimiento de propuestas
- Mejor identificación de keywords por pilar
- Análisis más preciso de las dimensiones (D1-D4)
