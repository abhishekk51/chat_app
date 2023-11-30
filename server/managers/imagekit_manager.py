from imagekitio import ImageKit
from settings import get_settings


settings = get_settings()


class ImageKitManager:

    def __init__(self):
        self.imagekit = ImageKit(
            private_key=settings.IMAGE_KIT_PRIVATE_KEY,
            public_key=settings.IMAGE_KIT_PUBLIC_KEY,
            url_endpoint=settings.IMAGE_KIT_URL
        )

    def upload_file(self, file):
        print(file, file.filename, 'fjslkfjsdlfkdjsflk')
        upload = self.imagekit.upload_file(
            file=file.file,
            file_name=file.filename
        )
        print(upload)

        # Raw Response
        print(upload.response_metadata.raw)

        # print that uploaded file's ID
        print(upload.file_id)