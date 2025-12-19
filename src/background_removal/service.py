"""Core background removal logic using rembg."""
import io
from functools import lru_cache

from PIL import Image
from rembg import new_session, remove


class BackgroundRemovalError(RuntimeError):
    """Raised when background removal fails."""


@lru_cache(maxsize=2)
def _get_session(model: str):
    """Return a cached rembg session for the given model."""
    return new_session(model)


def remove_background(
    image_bytes: bytes,
    model: str = "u2net",
    *,
    alpha_matting: bool = True,
    alpha_matting_foreground_threshold: int = 240,
    alpha_matting_background_threshold: int = 10,
    alpha_matting_erode_size: int = 10,
) -> bytes:
    """Remove background from an image and return PNG bytes.

    Args:
        image_bytes: Raw input image bytes.
        model: rembg model name, defaults to "u2net".
        alpha_matting: Enable matting for smoother edges.
        alpha_matting_foreground_threshold: Foreground threshold (0-255).
        alpha_matting_background_threshold: Background threshold (0-255).
        alpha_matting_erode_size: Erosion size to refine mask.

    Raises:
        BackgroundRemovalError: if removal fails.
    """
    try:
        input_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    except Exception as exc:  # pillow may raise various errors for bad images
        raise BackgroundRemovalError("Invalid image data") from exc

    def _clamp(value: int, low: int = 0, high: int = 255) -> int:
        return max(low, min(high, int(value)))

    try:
        session = _get_session(model)
        output = remove(
            input_image,
            session=session,
            alpha_matting=alpha_matting,
            alpha_matting_foreground_threshold=_clamp(alpha_matting_foreground_threshold),
            alpha_matting_background_threshold=_clamp(alpha_matting_background_threshold),
            alpha_matting_erode_size=max(1, int(alpha_matting_erode_size)),
        )
    except Exception as exc:  # rembg failures
        raise BackgroundRemovalError("Failed to remove background") from exc

    if isinstance(output, bytes):
        return output

    if hasattr(output, "save"):
        buffer = io.BytesIO()
        output.save(buffer, format="PNG")
        return buffer.getvalue()

    raise BackgroundRemovalError("Unexpected output format from rembg")
