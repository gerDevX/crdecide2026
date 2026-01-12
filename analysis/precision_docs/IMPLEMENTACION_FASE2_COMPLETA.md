# Implementación Completa: Fase 2 - Base de Datos de Evidencia Histórica

## Implementación Completada

### Cambios Realizados en `process_plans_v7.py`

#### 1. Nueva Función: `load_historical_evidence()`

**Ubicación**: Líneas 1100-1125

**Funcionalidad**:
- Carga evidencia histórica verificable desde `historical_evidence.json`
- Retorna diccionario con `candidate_id` como clave
- Maneja errores gracefully (retorna diccionario vacío si no existe)

**Características**:
- ✅ Manejo de errores robusto
- ✅ Retorna estructura vacía si archivo no existe
- ✅ Conversión de lista a diccionario para acceso rápido

#### 2. Nueva Función: `analyze_historical_evidence()`

**Ubicación**: Líneas 1127-1200

**Funcionalidad**:
- Analiza evidencia histórica verificable del candidato
- Categoriza evidencia en 3 tipos:
  - Comportamiento anti-democrático
  - Violaciones de derechos humanos
  - Corrupción verificada
- Retorna flags informativos (NO penalizaciones)

**Categorías**:
1. **`anti_democratic_behavior`**: Comportamiento anti-democrático histórico
2. **`human_rights_violations`**: Violaciones de derechos humanos históricas
3. **`corruption_convictions`**: Corrupción verificada históricamente

#### 3. Integración en `analyze_informative_flags()`

**Ubicación**: Líneas 1210-1300

**Cambios**:
- Agregado parámetro `historical_evidence` (opcional)
- Agregado campo `historical` a estructura de flags
- Llamada a `analyze_historical_evidence()` al final del análisis

#### 4. Integración en `calculate_candidate_score()`

**Ubicación**: Líneas 1750-1760

**Cambios**:
- Carga evidencia histórica usando `load_historical_evidence()`
- Obtiene evidencia específica del candidato
- Pasa evidencia histórica a `analyze_informative_flags()`

---

## Estructura de Datos

### Archivo: `historical_evidence.json`

**Ubicación**: `analysis/data/historical_evidence.json`

**Formato**:
```json
[
  {
    "candidate_id": "candidate-id-aqui",
    "evidence": [
      {
        "type": "judicial_sentence",
        "date": "2020-01-15",
        "source": "Poder Judicial de Costa Rica",
        "description": "Descripción breve y objetiva",
        "verification_url": "https://url-verificable.com/...",
        "category": "anti_democratic_behavior",
        "severity": "high"
      }
    ],
    "last_updated": "2026-01-11",
    "notes": "Notas opcionales"
  }
]
```

### Flags Históricos en JSON de Scores

```json
{
  "candidate_id": "ejemplo-candidato",
  "informative_flags": {
    "historical": {
      "anti_democratic_behavior": {
        "active": true,
        "severity": "high",
        "evidence": [
          {
            "type": "judicial_sentence",
            "date": "2020-01-15",
            "source": "Poder Judicial de Costa Rica",
            "description": "Sentencia por intento de eliminar independencia del Poder Judicial",
            "verification_url": "https://www.poder-judicial.go.cr/...",
            "severity": "high"
          }
        ],
        "description": "Evidencia histórica de comportamiento anti-democrático verificable"
      },
      "human_rights_violations": {
        "active": false,
        "severity": "high",
        "evidence": []
      },
      "corruption_convictions": {
        "active": false,
        "severity": "high",
        "evidence": []
      }
    }
  }
}
```

---

## Pruebas Realizadas

### Test 1: Cargar Evidencia Histórica

**Input**: Archivo `historical_evidence.json` con ejemplo

**Resultado**: ✅ Carga correctamente (1 candidato con evidencia)

### Test 2: Analizar Evidencia Histórica

**Input**: Evidencia de prueba con comportamiento anti-democrático y violaciones de derechos humanos

**Resultado**: 
- ✅ Anti-democrático: True (1 evidencia)
- ✅ Derechos humanos: True (1 evidencia)
- ✅ Corrupción: False (0 evidencias)

### Test 3: Procesamiento Completo

**Resultado**:
- ✅ Todos los candidatos tienen estructura de flags históricos
- ✅ Sistema implementado correctamente
- ✅ Flags guardados en `candidate_scores.json`

---

## Características de Implementación

### ✅ Neutralidad Mantenida

1. **Solo evidencia verificable**: Todas las evidencias deben tener URL de verificación
2. **Fuentes oficiales**: Solo organismos oficiales y verificables
3. **Evidencia concluida**: No acusaciones pendientes
4. **No penaliza**: Flags son informativos, NO afectan scoring

### ✅ Objetividad Garantizada

1. **Tipos específicos**: Solo tipos de evidencia aceptables
2. **Categorías claras**: Comportamiento, derechos, corrupción
3. **Fuentes verificables**: URLs públicas de verificación
4. **Aplicación igualitaria**: Mismos criterios para todos

---

## Tipos de Evidencia Aceptables

### ✅ Evidencia Objetiva

1. **`judicial_sentence`**: Sentencia judicial (Poder Judicial)
2. **`cidh_resolution`**: Resolución de CIDH
3. **`corte_interamericana_sentence`**: Sentencia de Corte Interamericana
4. **`contraloria_report`**: Informe de Contraloría
5. **`assembly_resolution`**: Resolución de Asamblea
6. **`un_report`**: Informe de ONU

### ❌ Evidencia NO Aceptable

- ❌ Opiniones políticas
- ❌ Acusaciones sin sentencia
- ❌ Rumores o especulaciones
- ❌ Artículos de opinión
- ❌ Redes sociales

---

## Fuentes de Evidencia

### Fuentes Objetivas y Verificables

1. **Poder Judicial de Costa Rica**: https://www.poder-judicial.go.cr/
2. **Contraloría General**: https://www.cgr.go.cr/
3. **Corte Interamericana**: https://www.corteidh.or.cr/
4. **CIDH**: https://www.oas.org/es/cidh/
5. **Asamblea Legislativa**: https://www.asamblea.go.cr/
6. **ONU**: https://www.un.org/

---

## Proceso de Uso

### Paso 1: Investigar Evidencia

1. Buscar en fuentes oficiales
2. Verificar que sea evidencia concluida
3. Obtener URL de verificación pública

### Paso 2: Agregar al Archivo

1. Abrir `analysis/data/historical_evidence.json`
2. Buscar entrada del candidato (o crear nueva)
3. Agregar evidencia al array `evidence`
4. Actualizar `last_updated`
5. Guardar archivo

### Paso 3: Procesar

1. Ejecutar `python3 process_plans_v7.py`
2. Verificar que flags históricos se generen correctamente
3. Revisar en `candidate_scores.json`

---

## Ejemplo de Uso

### Caso: Candidato con Evidencia Histórica

**Evidencia en `historical_evidence.json`**:
```json
{
  "candidate_id": "ejemplo-candidato",
  "evidence": [
    {
      "type": "judicial_sentence",
      "date": "2020-01-15",
      "source": "Poder Judicial de Costa Rica",
      "description": "Sentencia por intento de eliminar independencia del Poder Judicial",
      "verification_url": "https://www.poder-judicial.go.cr/...",
      "category": "anti_democratic_behavior",
      "severity": "high"
    }
  ]
}
```

**Flags generados**:
- ✅ `anti_democratic_behavior`: True (1 evidencia)
- ✅ `human_rights_violations`: False
- ✅ `corruption_convictions`: False

**Presentación al ciudadano**:
```
⚠️ Información Adicional

Este candidato tiene evidencia histórica verificable:
- Comportamiento anti-democrático (2020): Sentencia judicial
  Fuente: Poder Judicial de Costa Rica
  [Ver evidencia completa]

[Ver detalles] [Cerrar]
```

**Score**: NO se afecta (solo informa)

---

## Resultados del Procesamiento

**Después de la implementación**:
- ✅ Estructura de flags históricos agregada a todos los candidatos
- ✅ Sistema carga evidencia histórica correctamente
- ✅ Flags NO afectan el score (solo informan)

**Estado actual**:
- Archivo `historical_evidence.json` existe con ejemplo
- Ningún candidato real tiene evidencia histórica aún (normal)
- Sistema listo para recibir evidencia real

---

## Documentación Creada

1. `GUIA_EVIDENCIA_HISTORICA.md` - Guía completa para llenar base de datos
2. `IMPLEMENTACION_FASE2_COMPLETA.md` - Este documento

---

## Conclusión

### ✅ Fase 2 Implementada y Validada

**Funcionalidades implementadas**:
- ✅ Carga de evidencia histórica desde JSON
- ✅ Análisis de evidencia histórica por categorías
- ✅ Integración en sistema de flags informativos
- ✅ Estructura de datos completa
- ✅ Pruebas validadas

**Resultado**:
- Sistema informativo completo
- Neutralidad mantenida (solo evidencia verificable)
- Objetividad garantizada (fuentes oficiales)
- Transparencia total (ciudadano puede verificar)
- Listo para recibir evidencia real

---

**Fecha**: 2026-01-11  
**Estado**: Fase 2 implementada, lista para llenar con evidencia real
