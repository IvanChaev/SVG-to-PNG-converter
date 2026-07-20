import os
import subprocess
import sys
import shutil

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_dir = os.path.join(script_dir, "SVG")
    png_dir = os.path.join(script_dir, "PNG")
    end_dir = os.path.join(script_dir, "SVG_END")
    bad_dir = os.path.join(script_dir, "SVG_BAD")
    resvg_exe = os.path.join(script_dir, "resvg.exe")

    # Создаём необходимые папки
    os.makedirs(png_dir, exist_ok=True)
    os.makedirs(end_dir, exist_ok=True)
    os.makedirs(bad_dir, exist_ok=True)

    if not os.path.isfile(resvg_exe):
        with open(os.path.join(script_dir, "error.log"), "a") as log:
            log.write("resvg.exe не найден в папке скрипта.\n")
        sys.exit(1)

    if not os.path.isdir(svg_dir):
        with open(os.path.join(script_dir, "error.log"), "a") as log:
            log.write("Папка SVG не найдена.\n")
        sys.exit(1)

    svg_files = [f for f in os.listdir(svg_dir) if f.lower().endswith('.svg')]
    if not svg_files:
        sys.exit(0)

    for filename in svg_files:
        svg_path = os.path.join(svg_dir, filename)
        png_name = os.path.splitext(filename)[0] + ".png"
        png_path = os.path.join(png_dir, png_name)

        result = subprocess.run([resvg_exe, svg_path, png_path],
                                capture_output=True, text=True)

        if result.returncode == 0:
            # Успех — перемещаем исходник в SVG_END
            shutil.move(svg_path, os.path.join(end_dir, filename))
        else:
            # Ошибка — перемещаем исходник в SVG_BAD и логируем
            with open(os.path.join(script_dir, "error.log"), "a") as log:
                log.write(f"Ошибка конвертации {filename}: {result.stderr.strip()}\n")
            shutil.move(svg_path, os.path.join(bad_dir, filename))

if __name__ == "__main__":
    main()