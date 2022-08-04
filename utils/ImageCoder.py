import base64


class ImageCoder:
    def __init__(self, path: str):
        self.path = path

    def convert_image_to_base64(self) -> bytes:
        with open(self.path, "rb") as image_file:
            return base64.b64encode(image_file.read())

    def convert_base64_to_image(self, image: bytes | str) -> str:
        with open(self.path, "wb") as image_file:
            image_file.write(base64.b64decode(image))

        return self.path
