# Guía: Base de Datos de Evidencia Histórica (Fase 2)

## Objetivo

Crear una base de datos de evidencia histórica verificable sobre comportamiento de partidos/candidatos que pueda informar (sin penalizar) al ciudadano.

---

## Ubicación del Archivo

**Archivo**: `analysis/data/historical_evidence.json`

---

## Estructura del Archivo

### Formato JSON

```json
[
  {
    "candidate_id": "candidate-id-aqui",
    "evidence": [
      {
        "type": "judicial_sentence",
        "date": "2020-01-15",
        "source": "Poder Judicial de Costa Rica",
        "description": "Descripción breve y objetiva de la evidencia",
        "verification_url": "https://url-verificable.com/...",
        "category": "anti_democratic_behavior",
        "severity": "high"
      }
    ],
    "last_updated": "2026-01-11",
    "notes": "Notas opcionales sobre la evidencia"
  }
]
```

---

## Campos Requeridos

### Por Candidato

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `candidate_id` | string | ✅ Sí | ID del candidato (debe coincidir con `candidates.json`) |
| `evidence` | array | ✅ Sí | Lista de evidencias verificables |
| `last_updated` | string | ⚠️ Recomendado | Fecha de última actualización (YYYY-MM-DD) |
| `notes` | string | ❌ Opcional | Notas adicionales |

### Por Evidencia

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `type` | string | ✅ Sí | Tipo de evidencia (ver tipos abajo) |
| `date` | string | ✅ Sí | Fecha de la evidencia (YYYY-MM-DD) |
| `source` | string | ✅ Sí | Fuente de la evidencia (ej: "Poder Judicial") |
| `description` | string | ✅ Sí | Descripción breve y objetiva |
| `verification_url` | string | ✅ Sí | URL pública donde se puede verificar |
| `category` | string | ✅ Sí | Categoría (ver categorías abajo) |
| `severity` | string | ✅ Sí | Severidad: "low", "medium", "high" |

---

## Tipos de Evidencia Aceptables

### ✅ Evidencia Objetiva (Aceptable)

1. **`judicial_sentence`**: Sentencia judicial
   - Fuente: Poder Judicial de Costa Rica
   - Ejemplo: Sentencia por corrupción, violación de derechos, etc.

2. **`cidh_resolution`**: Resolución de CIDH
   - Fuente: Comisión Interamericana de Derechos Humanos
   - Ejemplo: Resolución por violación de derechos humanos

3. **`corte_interamericana_sentence`**: Sentencia de Corte Interamericana
   - Fuente: Corte Interamericana de Derechos Humanos
   - Ejemplo: Sentencia condenatoria

4. **`contraloria_report`**: Informe de Contraloría
   - Fuente: Contraloría General de la República
   - Ejemplo: Informe de auditoría que detecta irregularidades

5. **`assembly_resolution`**: Resolución de Asamblea
   - Fuente: Asamblea Legislativa
   - Ejemplo: Resolución que sanciona comportamiento

6. **`un_report`**: Informe de ONU
   - Fuente: Organización de las Naciones Unidas
   - Ejemplo: Informe sobre violaciones de derechos humanos

### ❌ Evidencia Subjetiva (NO Aceptable)

- ❌ Opiniones políticas
- ❌ Acusaciones sin sentencia
- ❌ Rumores o especulaciones
- ❌ Artículos de opinión
- ❌ Redes sociales

---

## Categorías de Evidencia

### 1. `anti_democratic_behavior`

**Descripción**: Comportamiento anti-democrático verificable

**Ejemplos**:
- Intentos verificables de eliminar instituciones democráticas
- Violaciones de separación de poderes verificadas
- Ataques a libertad de prensa verificables
- Restricciones a derechos fundamentales verificables

**Severidad**: Generalmente "high"

### 2. `human_rights_violations`

**Descripción**: Violaciones de derechos humanos verificables

**Ejemplos**:
- Sentencias de cortes internacionales
- Resoluciones de CIDH
- Informes de ONU sobre violaciones

**Severidad**: Generalmente "high"

### 3. `corruption_convictions`

**Descripción**: Corrupción verificada

**Ejemplos**:
- Sentencias judiciales por corrupción
- Investigaciones concluidas de Contraloría
- Resoluciones de organismos internacionales

**Severidad**: Generalmente "high"

---

## Ejemplos de Evidencia

### Ejemplo 1: Comportamiento Anti-Democrático

```json
{
  "type": "judicial_sentence",
  "date": "2020-01-15",
  "source": "Poder Judicial de Costa Rica",
  "description": "Sentencia por intento de eliminar independencia del Poder Judicial mediante proyecto de ley inconstitucional",
  "verification_url": "https://www.poder-judicial.go.cr/sentencias/2020/...",
  "category": "anti_democratic_behavior",
  "severity": "high"
}
```

### Ejemplo 2: Violación de Derechos Humanos

```json
{
  "type": "cidh_resolution",
  "date": "2018-05-20",
  "source": "Comisión Interamericana de Derechos Humanos",
  "description": "Resolución que determina violación de derechos humanos en caso específico",
  "verification_url": "https://www.oas.org/es/cidh/decisiones/2018/...",
  "category": "human_rights_violations",
  "severity": "high"
}
```

### Ejemplo 3: Corrupción Verificada

```json
{
  "type": "judicial_sentence",
  "date": "2019-03-10",
  "source": "Poder Judicial de Costa Rica",
  "description": "Sentencia condenatoria por corrupción en caso específico",
  "verification_url": "https://www.poder-judicial.go.cr/sentencias/2019/...",
  "category": "corruption_convictions",
  "severity": "high"
}
```

---

## Fuentes de Evidencia

### Fuentes Objetivas y Verificables

1. **Poder Judicial de Costa Rica**
   - URL: https://www.poder-judicial.go.cr/
   - Buscar: Sentencias, resoluciones

2. **Contraloría General de la República**
   - URL: https://www.cgr.go.cr/
   - Buscar: Informes de auditoría, resoluciones

3. **Corte Interamericana de Derechos Humanos**
   - URL: https://www.corteidh.or.cr/
   - Buscar: Sentencias

4. **Comisión Interamericana de Derechos Humanos**
   - URL: https://www.oas.org/es/cidh/
   - Buscar: Informes, resoluciones

5. **Asamblea Legislativa**
   - URL: https://www.asamblea.go.cr/
   - Buscar: Actas de sesiones, resoluciones

6. **Organización de las Naciones Unidas**
   - URL: https://www.un.org/
   - Buscar: Informes sobre derechos humanos

---

## Proceso de Agregar Evidencia

### Paso 1: Investigar Evidencia

1. Buscar en fuentes oficiales (Poder Judicial, CIDH, etc.)
2. Verificar que sea evidencia concluida (no acusaciones pendientes)
3. Obtener URL de verificación pública

### Paso 2: Verificar Objetividad

- ✅ ¿Es evidencia verificable?
- ✅ ¿Tiene fuente oficial?
- ✅ ¿Tiene URL de verificación?
- ✅ ¿Es evidencia concluida (no pendiente)?

### Paso 3: Agregar al Archivo

1. Abrir `analysis/data/historical_evidence.json`
2. Buscar entrada del candidato (o crear nueva)
3. Agregar evidencia al array `evidence`
4. Actualizar `last_updated`
5. Guardar archivo

### Paso 4: Procesar

1. Ejecutar `python3 process_plans_v7.py`
2. Verificar que flags históricos se generen correctamente
3. Revisar en `candidate_scores.json`

---

## Criterios de Objetividad

### ✅ Evidencia Objetiva (Aceptable)

1. **Sentencias judiciales**: Poder Judicial, cortes internacionales
2. **Resoluciones oficiales**: CIDH, ONU, Contraloría
3. **Informes públicos**: Organismos oficiales
4. **Actas públicas**: Asamblea Legislativa

### ❌ Evidencia Subjetiva (NO Aceptable)

1. **Opiniones políticas**: No son evidencia objetiva
2. **Acusaciones sin sentencia**: No son evidencia concluida
3. **Rumores o especulaciones**: No son verificables
4. **Artículos de opinión**: No son fuentes oficiales
5. **Redes sociales**: No son fuentes verificables

---

## Neutralidad y Objetividad

### Principios

1. **Solo evidencia verificable**: Todas las evidencias deben tener URL de verificación
2. **Fuentes oficiales**: Solo organismos oficiales y verificables
3. **Evidencia concluida**: No acusaciones pendientes
4. **Aplicación igualitaria**: Mismos criterios para todos los candidatos

### Evitar Sesgo

- ❌ NO incluir solo ciertos partidos
- ❌ NO incluir opiniones políticas
- ❌ NO incluir acusaciones sin sentencia
- ✅ SÍ incluir evidencia de TODOS los candidatos (si existe)
- ✅ SÍ usar solo fuentes oficiales
- ✅ SÍ verificar todas las evidencias

---

## Ejemplo Completo

```json
[
  {
    "candidate_id": "ejemplo-candidato",
    "evidence": [
      {
        "type": "judicial_sentence",
        "date": "2020-01-15",
        "source": "Poder Judicial de Costa Rica",
        "description": "Sentencia por intento de eliminar independencia del Poder Judicial mediante proyecto de ley inconstitucional",
        "verification_url": "https://www.poder-judicial.go.cr/sentencias/2020/12345",
        "category": "anti_democratic_behavior",
        "severity": "high"
      },
      {
        "type": "cidh_resolution",
        "date": "2018-05-20",
        "source": "Comisión Interamericana de Derechos Humanos",
        "description": "Resolución que determina violación de derechos humanos en caso específico",
        "verification_url": "https://www.oas.org/es/cidh/decisiones/2018/67890",
        "category": "human_rights_violations",
        "severity": "high"
      }
    ],
    "last_updated": "2026-01-11",
    "notes": "Evidencia verificable de fuentes oficiales"
  }
]
```

---

## Verificación

### Después de Agregar Evidencia

1. **Ejecutar procesamiento**:
   ```bash
   cd analysis
   python3 process_plans_v7.py
   ```

2. **Verificar flags históricos**:
   ```bash
   python3 -c "
   import json
   with open('data/candidate_scores.json', 'r') as f:
       scores = json.load(f)
   for s in scores:
       if s['candidate_id'] == 'tu-candidate-id':
           flags = s.get('informative_flags', {}).get('historical', {})
           print(json.dumps(flags, indent=2, ensure_ascii=False))
   "
   ```

3. **Verificar en frontend**: Los flags históricos aparecerán en `informative_flags.historical`

---

## Conclusión

### ✅ Sistema Listo para Uso

**Implementación**:
- ✅ Estructura de datos creada
- ✅ Funciones de carga y análisis implementadas
- ✅ Integración en sistema de flags completada
- ✅ Documentación completa

**Próximos pasos**:
1. Investigar evidencia histórica verificable
2. Agregar al archivo `historical_evidence.json`
3. Procesar y verificar flags

**Resultado**:
- Sistema informativo completo
- Neutralidad mantenida (solo evidencia verificable)
- Transparencia total (ciudadano puede verificar)

---

**Fecha**: 2026-01-11  
**Estado**: Fase 2 implementada, lista para llenar con evidencia real
