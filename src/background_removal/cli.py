"""Command-line interface for background removal."""
from pathlib import Path
from typing import Optional

import typer
import uvicorn

from background_removal import service

app = typer.Typer(help="Background removal utilities")


@app.command()
def remove(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image path"),
    output: Optional[Path] = typer.Option(None, help="Output path (defaults to <input>_no_bg.png)"),
    model: str = typer.Option("u2net", help="rembg model name"),
    alpha_matting: bool = typer.Option(True, help="Enable alpha matting for smoother edges"),
    alpha_matting_foreground_threshold: int = typer.Option(240, min=0, max=255, help="Alpha matting foreground threshold"),
    alpha_matting_background_threshold: int = typer.Option(10, min=0, max=255, help="Alpha matting background threshold"),
    alpha_matting_erode_size: int = typer.Option(10, min=1, max=100, help="Alpha matting erode size"),
) -> None:
    """Remove background from INPUT and save to OUTPUT."""
    data = input.read_bytes()
    result = service.remove_background(
        data,
        model=model,
        alpha_matting=alpha_matting,
        alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
        alpha_matting_background_threshold=alpha_matting_background_threshold,
        alpha_matting_erode_size=alpha_matting_erode_size,
    )
    target = output or input.with_name(f"{input.stem}_no_bg.png")
    target.write_bytes(result)
    typer.echo(f"Wrote {target}")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Bind host"),
    port: int = typer.Option(8000, help="Port to listen on"),
    reload: bool = typer.Option(True, help="Enable auto-reload"),
) -> None:
    """Run the FastAPI server."""
    uvicorn.run("background_removal.api:app", host=host, port=port, reload=reload)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
