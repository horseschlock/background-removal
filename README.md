# Background Removal Tool

Python tool for removing image backgrounds with a FastAPI service, CLI, and minimal web UI.

## Features
- FastAPI endpoint `/api/remove` accepts image uploads and returns background-removed PNG.
- CLI for batch or single-image removal and for running the API server.
- Minimal web UI to upload an image and preview/download the result.
- Dockerfile and Makefile for simple builds and local runs.

## Quickstart
1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the API (src layout):
   ```bash
  PYTHONPATH=src uvicorn background_removal.api:app --reload --host 0.0.0.0 --port 8000
   ```
4. Open the UI at `http://localhost:8000/`.

## CLI
- Remove a background and write a new file:
  ```bash
  PYTHONPATH=src python -m background_removal.cli remove input.jpg --output output.png \
    --model u2net --alpha-matting/--no-alpha-matting \
    --alpha-matting-foreground-threshold 240 \
    --alpha-matting-background-threshold 10 \
    --alpha-matting-erode-size 10
  ```
- Run the API server via CLI:
  ```bash
  PYTHONPATH=src python -m background_removal.cli serve --host 0.0.0.0 --port 8000 --reload
  ```

Quality tips
- Default model: `u2net` with alpha matting enabled for smoother edges.
- You can tweak via API query params, e.g. `POST /api/remove?model=u2net&alpha_matting=true&alpha_matting_foreground_threshold=240&alpha_matting_background_threshold=10&alpha_matting_erode_size=10`.

## Tests
```bash
PYTHONPATH=src pytest
```

## Docker
```bash
docker build -t background-removal .
docker run -p 8000:8000 background-removal
```
