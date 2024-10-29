from PIL import Image
import os

def process_image(upload_file):
    with Image.open(upload_file.file) as img:
        img_gray = img.convert("L")
        img_resized = img.resize((100, 100))
        file_path = f"images/{upload_file.filename}"
        img_resized.save(file_path, format="JPEG")
        resolution = f"{img_resized.width}x{img_resized.height}"
        size = os.path.getsize(file_path)
        return file_path, resolution, size
