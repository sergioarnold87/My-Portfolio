# 📸 Screenshots Placeholder

Para hacer el portfolio más visual, agrega screenshots aquí:

## Cómo agregar screenshots:

1. **Toma screenshots de la aplicación:**
   ```bash
   # Ejecuta la app
   streamlit run app/main.py
   
   # Toma capturas de:
   # - Pantalla principal
   # - Modo "explore" con resultados
   # - Modo "combine" mostrando síntesis
   # - Modo "architecture" con diseño generado
   ```

2. **Guarda las imágenes aquí:**
   ```
   assets/
   ├── screenshot-home.png
   ├── screenshot-explore.png
   ├── screenshot-combine.png
   ├── screenshot-architecture.png
   └── demo.gif (opcional: grabación de uso)
   ```

3. **Referencia en README.md:**
   ```markdown
   ## 🎬 Demo
   
   ![RAG Demo Home](assets/screenshot-home.png)
   
   ### Modo Explore
   ![Explore Mode](assets/screenshot-explore.png)
   
   ### Modo Combine
   ![Combine Mode](assets/screenshot-combine.png)
   ```

## Herramientas recomendadas:

- **Para screenshots:** 
  - `gnome-screenshot` (viene con Linux Mint)
  - `flameshot` (más features)
  - Tecla PrtScr

- **Para GIFs animados:**
  - `peek` (simple, excelente)
  - `recordmydesktop` + `ffmpeg`
  
  Instalar peek:
  ```bash
  sudo add-apt-repository ppa:peek-developers/stable
  sudo apt update
  sudo apt install peek
  ```

## Tips para buenos screenshots:

- ✅ Ventana a tamaño completo
- ✅ Zoom al 100%
- ✅ Datos de ejemplo interesantes
- ✅ Fondo limpio (cierra otras ventanas)
- ✅ Resalta el feature que muestras
- ❌ No incluyas información sensible
- ❌ Evita screenshots oscuros o pixelados
