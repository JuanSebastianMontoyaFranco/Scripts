import sys
from moviepy import VideoFileClip  # para MoviePy 2.x

# --- Test de entorno ---
print("Python ejecutado desde:", sys.executable)
print("Versión:", sys.version)

# --- Funciones ---

def optimizar_gif(input_path, output_path, width=None, fps=None):
    """
    Optimiza un GIF reduciendo dimensiones y FPS.
    - input_path: ruta del GIF original
    - output_path: ruta donde guardar el GIF optimizado
    - width: ancho en píxeles (ajusta la altura automáticamente)
    - fps: frames por segundo
    """
    clip = VideoFileClip(input_path)

    # Redimensionar si se especifica ancho
    if width:
        clip = clip.resized(width=width)   # ✅ MoviePy 2.x

    # Reducir FPS si se especifica
    if fps:
        clip = clip.with_fps(fps)          # ✅ MoviePy 2.x

    # Guardar GIF optimizado (sin program=)
    clip.write_gif(output_path, fps=fps if fps else None)
    print(f"GIF optimizado guardado en: {output_path}")


def gif_a_mp4(input_path, output_path, width=None, fps=None):
    """
    Convierte un GIF a MP4 mucho más liviano.
    - input_path: ruta del GIF original
    - output_path: ruta donde guardar el video
    - width: ancho en píxeles (ajusta la altura automáticamente)
    - fps: frames por segundo
    """
    clip = VideoFileClip(input_path)

    if width:
        clip = clip.resized(width=width)
    if fps:
        clip = clip.with_fps(fps)

    # Guardar como MP4 (codec H.264)
    clip.write_videofile(output_path, codec="libx264", audio=False)
    print(f"Video MP4 guardado en: {output_path}")


# --- Ejemplos de uso ---
if __name__ == "__main__":
    # Optimizar GIF a 480px ancho y 12fps
    optimizar_gif("OB-3.gif", "salida_opt.gif", width=480, fps=12)

    # Convertir a MP4 más liviano
    gif_a_mp4("OB-3.gif", "salida.mp4", width=480, fps=12)
