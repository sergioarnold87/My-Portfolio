# 🔒 Política de Seguridad

## 🛡️ Versiones Soportadas

| Versión | Soportada          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## 🚨 Reportar una Vulnerabilidad

La seguridad de este proyecto es importante. Si descubres una vulnerabilidad de seguridad, por favor sigue estos pasos:

### 1. **NO** Crear un Issue Público

Por favor **NO** crees un issue público en GitHub para vulnerabilidades de seguridad.

### 2. Reportar Privadamente

Envía un email a: **anol1987.com** con:

- Descripción detallada de la vulnerabilidad
- Pasos para reproducir el problema
- Impacto potencial
- Sugerencias de solución (opcional)

### 3. Qué Esperar

- **Respuesta inicial**: Dentro de 48 horas
- **Actualización de progreso**: Cada 5 días
- **Resolución estimada**: 30 días para vulnerabilidades críticas

### 4. Proceso de Divulgación

Seguimos un proceso de **divulgación responsable**:

1. Recibes confirmación del reporte
2. Investigamos y validamos
3. Desarrollamos un fix
4. Publicamos una actualización de seguridad
5. Se publica un advisory después del fix

## 🔐 Mejores Prácticas de Seguridad

### Para Usuarios del Proyecto

#### Configuración de API Keys

**❌ NUNCA hagas esto:**
```python
# ¡NO HARDCODEES API KEYS!
openai.api_key = "sk-abc123..."
```

**✅ Haz esto:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
```

#### Archivo .env

```bash
# ✅ CORRECTO: Usa .env para secrets
OPENAI_API_KEY=sk-your-key-here

# ✅ CORRECTO: .env debe estar en .gitignore
echo ".env" >> .gitignore

# ✅ CORRECTO: Nunca commitees .env
git status  # Verifica que .env no aparezca
```

#### Permisos de Archivos

```bash
# Protege tu archivo .env
chmod 600 .env

# Solo el dueño puede leer/escribir
ls -la .env
# -rw------- 1 user user 50 Oct 21 20:00 .env
```

### Para Contribuidores

#### Antes de Commitear

```bash
# ✅ Verifica que no haya secrets
git diff

# ✅ Usa git-secrets (recomendado)
git secrets --scan

# ✅ Revisa el staging area
git status
```

#### Pre-commit Hooks

Considera instalar git hooks para prevenir commits accidentales de secrets:

```bash
# Instala pre-commit
pip install pre-commit

# Crea .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: check-added-large-files
      - id: detect-private-key
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
EOF

# Instala los hooks
pre-commit install
```

## 🔍 Áreas de Atención

### 1. Inyección de Prompts

**Riesgo**: Los usuarios podrían intentar inyectar prompts maliciosos.

**Mitigación**:
- Sanitiza inputs del usuario
- Limita longitud de queries
- Implementa rate limiting

### 2. Acceso a Archivos

**Riesgo**: Path traversal en sistema de upload.

**Mitigación**:
- Valida extensiones de archivo
- Sanitiza nombres de archivo
- Usa paths seguros (no user input directo)

### 3. API Keys

**Riesgo**: Exposición de API keys en código o logs.

**Mitigación**:
- Usa variables de entorno
- Nunca logees API keys
- Rota keys regularmente
- Usa API keys con permisos mínimos

### 4. Dependencias

**Riesgo**: Vulnerabilidades en paquetes de terceros.

**Mitigación**:
```bash
# Audita dependencias regularmente
pip install safety
safety check -r requirements.txt

# Actualiza dependencias
pip list --outdated
pip install --upgrade <package>
```

## 📋 Checklist de Seguridad

### Para Desarrollo Local

- [ ] `.env` está en `.gitignore`
- [ ] No hay API keys hardcodeadas
- [ ] Archivo `.env` tiene permisos 600
- [ ] Dependencies actualizadas (`pip list --outdated`)
- [ ] Sin secrets en git history

### Para Producción

- [ ] Usa HTTPS para todas las conexiones
- [ ] API keys en secret manager (no en .env)
- [ ] Rate limiting implementado
- [ ] Logging sin información sensible
- [ ] Inputs del usuario validados/sanitizados
- [ ] Actualización automática de dependencias
- [ ] Monitoring de seguridad activo

### Para GitHub

- [ ] Branch protection rules configuradas
- [ ] Require reviews antes de merge
- [ ] Status checks deben pasar
- [ ] GitHub Dependabot habilitado
- [ ] Secret scanning habilitado
- [ ] No hay secrets en el repositorio

## 🛠️ Herramientas de Seguridad

### Análisis Estático

```bash
# Bandit - encuentra issues de seguridad comunes
pip install bandit
bandit -r app/

# Safety - verifica vulnerabilidades conocidas
pip install safety
safety check
```

### Git Secrets

```bash
# git-secrets previene commits de secrets
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
sudo make install

# Configura para tu repo
cd /path/to/rag-demo-data-engineering
git secrets --install
git secrets --register-aws
```

### GitHub Actions

El proyecto incluye workflows para:
- Lint de código
- Análisis de seguridad (puedes agregar)
- Dependency scanning

## 🚫 Qué NO Hacer

❌ Hardcodear API keys  
❌ Commitear archivos .env  
❌ Publicar secrets en issues/PRs  
❌ Usar API keys de producción en desarrollo  
❌ Ignorar warnings de seguridad  
❌ Ejecutar código sin revisar  
❌ Usar HTTP en lugar de HTTPS  
❌ Deshabilitar validaciones de seguridad  

## ✅ Qué SÍ Hacer

✅ Usar variables de entorno  
✅ Revisar código antes de commitear  
✅ Mantener dependencias actualizadas  
✅ Reportar vulnerabilidades responsablemente  
✅ Seguir el principio de menor privilegio  
✅ Validar todos los inputs  
✅ Implementar logging seguro  
✅ Usar HTTPS siempre  

## 📚 Recursos Adicionales

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OpenAI Security Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)

## 🙏 Agradecimientos

Agradecemos a todos los que reportan vulnerabilidades de manera responsable y ayudan a mantener este proyecto seguro.

---

**Última actualización**: Octubre 2025  
**Mantenedor**: Sergio Arnold (@sergioarnold87)
