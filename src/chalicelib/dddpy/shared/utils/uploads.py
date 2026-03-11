import os
from slugify import slugify

class FileUploader:
    
    @staticmethod
    async def createFolders(directory_path:str):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    
    @staticmethod
    async def upload_image(picture_data: dict, folder:str="images/",new_name:str=None):
        try:

            picture_name, ext = os.path.splitext(picture_data["filename"])
            if new_name:
                picture_name = slugify(new_name)
            file_location = f"{folder}{picture_name}{ext}"
            await FileUploader.createFolders(os.path.dirname(file_location))
            with open(file_location, "wb") as file:
                file.write(picture_data["content"])
            return file_location
        except Exception as e:
            print(e)
            return None
        