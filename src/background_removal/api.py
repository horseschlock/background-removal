"""FastAPI application exposing the background removal service."""

from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from fastapi.responses import HTMLResponse, Response

from background_removal import service

app = FastAPI(title="Background Removal API", version="0.1.0")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/remove")
async def remove(
  file: UploadFile = File(...),
  model: str = Query("u2net", description="rembg model name"),
  alpha_matting: bool = Query(True, description="Enable alpha matting"),
  alpha_matting_foreground_threshold: int = Query(240, ge=0, le=255),
  alpha_matting_background_threshold: int = Query(10, ge=0, le=255),
  alpha_matting_erode_size: int = Query(10, ge=1, le=100),
) -> Response:
  data = await file.read()
  try:
    output_bytes = service.remove_background(
      data,
      model=model,
      alpha_matting=alpha_matting,
      alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
      alpha_matting_background_threshold=alpha_matting_background_threshold,
      alpha_matting_erode_size=alpha_matting_erode_size,
    )
  except service.BackgroundRemovalError as exc:
    raise HTTPException(status_code=400, detail=str(exc)) from exc

  return Response(content=output_bytes, media_type="image/png")


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    """Serve a minimal inline UI."""
    return """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Background Removal</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 2rem; display: flex; gap: 2rem; flex-wrap: wrap; }
        .panel { flex: 1 1 320px; border: 1px solid #ddd; padding: 1rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        button { padding: 0.5rem 1rem; }
        img { max-width: 100%; height: auto; }
        .preview { display: flex; flex-direction: column; gap: 1rem; }
      </style>
    </head>
    <body>
      <div class="panel">
        <h2>Upload Image</h2>
        <form id="upload-form">
          <input type="file" id="file" accept="image/*" required />
          <button type="submit">Remove Background</button>
        </form>
        <p id="status"></p>
      </div>
      <div class="panel preview">
        <div>
          <h3>Original</h3>
          <img id="original" alt="Original preview" />
        </div>
        <div>
          <h3>Result</h3>
          <img id="result" alt="Result preview" />
          <a id="download" href="#" download="output.png" style="display:none;">Download result</a>
        </div>
      </div>
      <script>
        const form = document.getElementById('upload-form');
        const fileInput = document.getElementById('file');
        const status = document.getElementById('status');
        const originalImg = document.getElementById('original');
        const resultImg = document.getElementById('result');
        const downloadLink = document.getElementById('download');

        fileInput.addEventListener('change', () => {
          const file = fileInput.files[0];
          if (file) {
            originalImg.src = URL.createObjectURL(file);
          }
        });

        form.addEventListener('submit', async (e) => {
          e.preventDefault();
          const file = fileInput.files[0];
          if (!file) { status.textContent = 'Please choose a file.'; return; }
          status.textContent = 'Processing...';

          const formData = new FormData();
          formData.append('file', file);

          try {
            const response = await fetch('/api/remove', { method: 'POST', body: formData });
            if (!response.ok) {
              const error = await response.json().catch(() => ({ detail: 'Error' }));
              throw new Error(error.detail || 'Failed to process image');
            }
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            resultImg.src = url;
            downloadLink.href = url;
            downloadLink.style.display = 'inline';
            status.textContent = 'Done!';
          } catch (err) {
            status.textContent = err.message;
            console.error(err);
          }
        });
      </script>
    </body>
    </html>
    """
