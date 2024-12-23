import os


def get_image_path(image_name: str, dir_name="widget") -> str:
    """
    Возвращает полный путь к изображению в папке `data/widget`.

    :param image_name: Имя файла изображения (например, "image_1.png").
    :return: Полный путь к файлу.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join("/app", "data", dir_name)
    return os.path.join(images_dir, image_name)
