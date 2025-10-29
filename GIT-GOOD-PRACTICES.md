Buenas prácticas Git & GitHub

Resumen breve
- Usa ramas cortas y con nombre claro: feature/<ticket>-descripcion, fix/<issue>, chore/<task>.
- Commits pequeños y atómicos con mensajes convencionales: tipo: alcance - descripción corta (ej: feat: add synthetic data generator).
- Añade un archivo CONTRIBUTING.md con guías de PR, formato de mensajes y flujos de trabajo.
- No fuerces pushes a main: en su lugar, abre PRs y usa revisiones.

Flujo recomendado
1. Mantén `main` siempre desplegable.
2. Crea rama basada en `main`: git checkout -b feature/<ticket>-desc
3. Haz commits atómicos y firma si es necesario.
4. Push de la rama: git push origin feature/<ticket>-desc
5. Abre Pull Request con descripción, checklist y evidencias (capturas/tests)
6. Usa CI para validar lint/tests antes de merge.

Configuraciones útiles
- .gitignore: ignorar .venv, data/ (si no versionas datos grandes), .DS_Store, __pycache__
- pre-commit: añade black, ruff/isort, ruff autofix hooks
- Protection rules (en GitHub): exigir PR review, pasar CI, y squash/merge policy.

Comandos comunes
- Crear rama: git checkout -b feature/123-add-readme
- Actualizar main: git fetch origin && git switch main && git pull
- Rebase feature: git switch feature/... && git fetch origin && git rebase origin/main
- Push branch: git push -u origin feature/...
- Crear PR: desde GitHub web o gh cli: gh pr create --fill

Manejo de conflictos
- Rebase frecuentemente desde main para mantener history limpia.
- Si hay conflictos: resolver localmente, probar, y luego git rebase --continue (o merge si prefieres).

Políticas sobre secrets
- Nunca subir credenciales o tokens. Usa GitHub Secrets y .gitignore para archivos locales.

Notas finales
- Automatiza CI para tests/lint. Mantén `requirements.txt` o usa Poetry/poetry.lock para reproducibilidad.
