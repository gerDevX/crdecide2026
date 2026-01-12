# Análisis de Cambios Necesarios para v7

## Resumen Ejecutivo

Revisión completa del sitio para asegurar que refleje correctamente el modelo v7:
- ✅ **Penalizaciones**: Fiscales, Omisión, Viabilidad Legal
- ✅ **Bonos**: Múltiples propuestas, Calidad, Financiamiento
- ✅ **Flags Informativos**: NO penalizan, solo informan
- ✅ **Versión**: Actualizar todas las referencias de v6 a v7

---

## Cambios Necesarios por Página

### 1. `/pilares/index.astro` ⚠️ **CAMBIOS REQUERIDOS**

**Línea 166**: Referencia a v6
```astro
<h2 class="text-xl font-bold text-slate-900">Distribución de Pesos (v6)</h2>
```
**Cambio**: Actualizar a v7

**Estado**: ❌ **PENDIENTE**

---

### 2. `/metodologia.astro` ✅ **MAYORMENTE ACTUALIZADO**

**Verificaciones**:
- ✅ Bonos v7: Presente en Dashboard, Express y Reading
- ✅ Penalizaciones: Presente (fiscales, omisión, viabilidad)
- ✅ Flags informativos: Presente
- ✅ Versión v7: Presente en footer

**Estado**: ✅ **COMPLETO** (ya actualizado anteriormente)

---

### 3. `/tecnico.astro` ✅ **ACTUALIZADO**

**Verificaciones**:
- ✅ Referencias a v7: Presente
- ✅ Constantes de penalización: Incluye viabilidad legal
- ✅ Bonos: Presente en código de ejemplo
- ✅ Versión v7: Presente en footer

**Estado**: ✅ **COMPLETO**

---

### 4. `/acerca.astro` ✅ **ACTUALIZADO**

**Verificaciones**:
- ✅ Footer con v7: Presente

**Estado**: ✅ **COMPLETO**

---

### 5. `/index.astro` ✅ **ACTUALIZADO**

**Verificaciones**:
- ✅ Descripción v7: Presente (línea 160)
- ✅ Menciona bonos, penalizaciones y flags

**Estado**: ✅ **COMPLETO**

---

### 6. `/ranking.astro` ✅ **ACTUALIZADO**

**Verificaciones**:
- ✅ Referencia v7: Presente (línea 473)
- ✅ Bonos mostrados: Presente en todos los modos
- ✅ Flags informativos: Presente

**Estado**: ✅ **COMPLETO**

---

### 7. `/comparar.astro` ✅ **ACTUALIZADO**

**Verificaciones**:
- ✅ Bonos mostrados: Presente en comparación
- ✅ Penalizaciones: Presente
- ✅ Flags informativos: Presente

**Estado**: ✅ **COMPLETO**

---

### 8. `/candidatos/[id].astro` ✅ **ACTUALIZADO**

**Verificaciones**:
- ✅ Bonos mostrados: Presente en todos los modos
- ✅ Penalizaciones: Presente
- ✅ Flags informativos: Presente (componente InformativeFlags)
- ✅ Viabilidad: Presente

**Estado**: ✅ **COMPLETO**

---

### 9. `/candidatos/index.astro` ⚠️ **REVISAR**

**Verificaciones**:
- ❓ No hay referencias explícitas a metodología
- ❓ Solo muestra ranking y riesgo

**Estado**: ⚠️ **REVISAR** (puede no necesitar cambios si solo muestra datos)

---

### 10. `/pilares/[id].astro` ⚠️ **REVISAR**

**Verificaciones**:
- ❓ Muestra penalizaciones pero no menciona bonos explícitamente
- ❓ No menciona flags informativos
- ❓ No menciona viabilidad legal

**Estado**: ⚠️ **REVISAR** (puede necesitar mención de bonos/viabilidad)

---

## Cambios Específicos Requeridos

### 🔴 **CRÍTICO - Cambio Inmediato**

1. **`/pilares/index.astro` línea 166**:
   - Cambiar "Distribución de Pesos (v6)" → "Distribución de Pesos (v7)"

### 🟡 **RECOMENDADO - Mejoras**

2. **`/pilares/[id].astro`**:
   - Considerar agregar mención de bonos si se muestran en el pilar
   - Considerar agregar mención de viabilidad si hay violaciones

3. **`/candidatos/index.astro`**:
   - Verificar si necesita mención de metodología v7 (probablemente no, ya que solo lista candidatos)

---

## Verificación de Contenido

### Penalizaciones ✅
- ✅ Fiscales: Ataca regla fiscal (-2), Propone más deuda (-1)
- ✅ Omisión: Seguridad (-1), CCSS (-1), Empleo (-0.5), Crimen (-0.5), Pilar faltante (-0.5)
- ✅ Viabilidad Legal: Separación de poderes (-1.0), Derechos fundamentales (-1.0), Garantías (-1.0), Procedimientos (-0.5)

### Bonos ✅
- ✅ Múltiples propuestas (3+): +1.0
- ✅ Propuesta completa (4/4): +0.25
- ✅ Financiamiento claro (score >=3): +0.1

### Flags Informativos ✅
- ✅ Propuestas problemáticas actuales
- ✅ Similitudes con modelos históricos
- ✅ Requisitos de negociación
- ✅ Evidencia histórica
- ✅ Contradicciones histórico-actual

---

## Conclusión

**Total de cambios requeridos**: **1 cambio crítico**

1. ✅ Actualizar referencia v6 → v7 en `/pilares/index.astro`

**Total de cambios recomendados**: **0-2 mejoras opcionales**

1. ⚠️ Considerar agregar información de bonos/viabilidad en `/pilares/[id].astro` (opcional)
2. ⚠️ Verificar `/candidatos/index.astro` (probablemente no necesita cambios)

---

## Prioridad

- 🔴 **Alta**: Actualizar v6 → v7 en pilares/index.astro
- 🟡 **Media**: Mejoras opcionales en pilares/[id].astro
- 🟢 **Baja**: Verificación de candidatos/index.astro
