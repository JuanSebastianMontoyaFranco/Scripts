import os
from PIL import Image

def resize_if_needed(img, max_pixels=25_000_000):
    width, height = img.size
    total_pixels = width * height

    if total_pixels <= max_pixels:
        return img

    scale_factor = (max_pixels / total_pixels) ** 0.5
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    return img.resize((new_width, new_height), Image.LANCZOS)


def convert_images_to_webp(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.webp'
            output_path = os.path.join(output_folder, output_filename)

            try:
                with Image.open(input_path) as img:
                    img = img.convert("RGB")  # Para evitar errores con transparencias
                    img = resize_if_needed(img)
                    img.save(output_path, 'WEBP', quality=90)
                    print(f'Convertido: {filename} -> {output_filename}')
            except Exception as e:
                print(f'Error al procesar {filename}: {e}')


# Uso
input_folder = 'C:\\Users\\jsm21\\Downloads\\Imagenes Entre Amigas\\Originales'
output_folder = 'C:\\Users\\jsm21\\Downloads\\Imagenes Entre Amigas\\Nuevas'

convert_images_to_webp(input_folder, output_folder)
