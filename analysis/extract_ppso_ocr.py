#!/usr/bin/env python3
"""
Script para extraer texto del PDF PPSO usando OCR de alta calidad.
Genera el archivo ppso_ocr_text.txt que será usado automáticamente por process_plans_v7.py
"""

import os
import sys
import fitz  # PyMuPDF
from PIL import Image
import io

# Verificar disponibilidad de OCR
EASYOCR_AVAILABLE = False
TESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
    print("✅ EasyOCR disponible")
except ImportError:
    print("⚠️  EasyOCR no disponible")

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
    print("✅ Tesseract disponible")
except ImportError:
    print("⚠️  Tesseract no disponible")

if not EASYOCR_AVAILABLE and not TESSERACT_AVAILABLE:
    print("❌ Error: No hay motores OCR disponibles")
    print("   Instalar: pip install easyocr pytesseract")
    sys.exit(1)

# Configuración
RENDER_DPI = 300  # Alta resolución para mejor calidad
TESSERACT_CONFIG = '--oem 3 --psm 6 -l spa'

# Usar Tesseract por defecto (más rápido) o EasyOCR (mejor calidad pero más lento)
USE_EASYOCR = False  # Cambiar a True para mejor calidad (pero más lento)

# Rutas
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLANES_DIR = os.path.join(SCRIPT_DIR, "planes")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
PDF_PATH = os.path.join(PLANES_DIR, "PPSO.pdf")
OUTPUT_FILE = os.path.join(DATA_DIR, "ppso_ocr_text.txt")

# Inicializar EasyOCR (una sola vez)
_easyocr_reader = None

def get_easyocr_reader():
    """Inicializa EasyOCR una sola vez (es costoso)"""
    global _easyocr_reader
    if _easyocr_reader is None and EASYOCR_AVAILABLE:
        try:
            print("  🔄 Inicializando EasyOCR (esto puede tomar unos segundos)...")
            _easyocr_reader = easyocr.Reader(['es', 'en'], gpu=False)
            print("  ✅ EasyOCR inicializado")
        except Exception as e:
            print(f"  ⚠️  Error inicializando EasyOCR: {e}")
    return _easyocr_reader

def extract_page_with_ocr(page, dpi: int = RENDER_DPI) -> str:
    """Extrae texto de una página usando OCR"""
    try:
        # Renderizar página como imagen
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # Intentar EasyOCR si está configurado (mejor calidad pero más lento)
        if USE_EASYOCR and EASYOCR_AVAILABLE:
            try:
                reader = get_easyocr_reader()
                if reader:
                    import numpy as np
                    img_array = np.array(img)
                    results = reader.readtext(img_array)
                    # Combinar todos los textos detectados
                    text = "\n".join([result[1] for result in results])
                    return text
            except Exception as e:
                print(f"    ⚠️  Error EasyOCR, usando Tesseract: {e}")
        
        # Usar Tesseract (más rápido, buena calidad)
        if TESSERACT_AVAILABLE:
            text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)
            return text
        
        # Fallback a EasyOCR si Tesseract no está disponible
        if EASYOCR_AVAILABLE:
            try:
                reader = get_easyocr_reader()
                if reader:
                    import numpy as np
                    img_array = np.array(img)
                    results = reader.readtext(img_array)
                    text = "\n".join([result[1] for result in results])
                    return text
            except Exception as e:
                print(f"    ⚠️  Error EasyOCR: {e}")
        
        return ""
        
    except Exception as e:
        print(f"    ⚠️  Error OCR en página: {e}")
        return ""

def main():
    """Extrae texto del PDF PPSO usando OCR"""
    
    if not os.path.exists(PDF_PATH):
        print(f"❌ Error: No se encuentra el PDF: {PDF_PATH}")
        sys.exit(1)
    
    print("=" * 80)
    print("EXTRACCIÓN OCR PARA PPSO")
    print("=" * 80)
    print(f"📄 PDF: {PDF_PATH}")
    print(f"💾 Salida: {OUTPUT_FILE}")
    ocr_engine = "EasyOCR" if USE_EASYOCR and EASYOCR_AVAILABLE else "Tesseract"
    print(f"🔧 OCR: {ocr_engine}")
    print(f"📐 DPI: {RENDER_DPI}")
    print("=" * 80)
    
    try:
        doc = fitz.open(PDF_PATH)
        num_pages = len(doc)
        print(f"\n📖 Total de páginas: {num_pages}\n")
        
        pages_text = []
        
        for page_num in range(num_pages):
            page = doc[page_num]
            print(f"  Procesando página {page_num + 1}/{num_pages}...", end=" ", flush=True)
            
            text = extract_page_with_ocr(page, RENDER_DPI)
            
            if text.strip():
                pages_text.append((page_num + 1, text))
                print(f"✅ ({len(text)} caracteres)")
            else:
                print("⚠️  (sin texto)")
        
        doc.close()
        
        # Guardar en formato esperado
        print(f"\n💾 Guardando {len(pages_text)} páginas en {OUTPUT_FILE}...")
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for page_num, text in pages_text:
                f.write(f"--- Página {page_num} ---\n")
                f.write(text)
                f.write("\n\n")
        
        total_chars = sum(len(text) for _, text in pages_text)
        print(f"✅ Archivo guardado exitosamente")
        print(f"   Páginas procesadas: {len(pages_text)}/{num_pages}")
        print(f"   Total de caracteres: {total_chars:,}")
        print(f"\n📝 El archivo {OUTPUT_FILE} será usado automáticamente")
        print(f"   en la próxima ejecución de process_plans_v7.py")
        
    except Exception as e:
        print(f"\n❌ Error procesando PDF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
