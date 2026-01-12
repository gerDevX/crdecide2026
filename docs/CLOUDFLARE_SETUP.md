# Configuración de Cloudflare Pages - Guía de Verificación

## Problema: Error de Autenticación (Código 10000)

El error indica que el token API no tiene los permisos correctos para desplegar a Cloudflare Pages.

## ✅ Verificaciones Necesarias

### 1. Verificar Permisos del Token API

El token `CLOUDFLARE_API_TOKEN` debe tener los siguientes permisos:

1. Ve a: https://dash.cloudflare.com/profile/api-tokens
2. Busca el token que estás usando (o crea uno nuevo)
3. Verifica que tenga estos permisos:
   - **Account** → **Cloudflare Pages** → **Edit** (requerido para desplegar)
   - **User** → **Memberships** → **Read** (requerido para leer membresías)

### 2. Crear un Nuevo Token (si es necesario)

Si el token actual no tiene los permisos correctos:

1. Ve a: https://dash.cloudflare.com/profile/api-tokens
2. Click en **"Create Token"**
3. Selecciona **"Create Custom Token"**
4. Asigna un nombre descriptivo (ej: "Pages Deploy - crdecide2026")
5. Configura los permisos:
   - **Account** → **Cloudflare Pages** → **Edit**
   - **User** → **Memberships** → **Read**
6. En **Account Resources**, selecciona:
   - **Include** → **All accounts** (o la cuenta específica)
7. Click en **"Continue to summary"** y luego **"Create Token"**
8. **Copia el token inmediatamente** (solo se muestra una vez)

### 3. Configurar Variables de Entorno en Cloudflare Pages

En el dashboard de Cloudflare Pages:

1. Ve a tu proyecto `crdecide2026`
2. Ve a **Settings** → **Environment Variables**
3. Verifica que exista:
   - **Variable:** `CLOUDFLARE_API_TOKEN`
   - **Value:** [Tu token API con permisos correctos]
   - **Environment:** Production (y Preview si aplica)

### 4. Verificar que el Proyecto Existe

Asegúrate de que el proyecto `crdecide2026` exista en Cloudflare Pages:

1. Ve a: https://dash.cloudflare.com/pages
2. Verifica que el proyecto `crdecide2026` esté listado
3. Si no existe, créalo primero desde el dashboard

### 5. Configuración del Proyecto (Build Settings)

En Cloudflare Pages, verifica la configuración de build:

- **Build command:** `npm run build` (o `cd site && npm run build` si el proyecto está en la raíz)
- **Build output directory:** `dist` (o `site/dist` si aplica)
- **Root directory:** `site` (si el proyecto está en la carpeta `site/`)

## 📝 Configuración Actual del Proyecto

### wrangler.toml
```toml
name = "crdecide2026"
pages_build_output_dir = "./dist"
compatibility_date = "2024-01-01"
```

### Scripts de Deploy
```json
"pages:deploy": "wrangler pages deploy dist"
```

## 🔍 Comandos para Probar Localmente

Si quieres probar el deploy localmente (requiere tener el token configurado):

```bash
cd site
export CLOUDFLARE_API_TOKEN="tu-token-aqui"
npm run build
npm run pages:deploy
```

## ⚠️ Notas Importantes

1. **No incluyas `account_id` en `wrangler.toml`** - No es compatible con Cloudflare Pages
2. El token API debe tener permisos específicos, aunque tu cuenta sea Super Administrador
3. El token solo se muestra una vez al crearlo - guárdalo de forma segura
4. Si cambias el token, actualiza la variable de entorno en Cloudflare Pages

## 🐛 Troubleshooting

### Error: "Authentication error [code: 10000]"
- Verifica que el token tenga los permisos correctos
- Verifica que el token no haya expirado o sido revocado
- Verifica que la variable de entorno esté configurada correctamente

### Error: "Configuration file for Pages projects does not support 'account_id'"
- Ya está resuelto: el `account_id` fue removido del `wrangler.toml`

### Error: "Project not found"
- Verifica que el proyecto `crdecide2026` exista en Cloudflare Pages
- Verifica que el nombre en `wrangler.toml` coincida con el nombre del proyecto
