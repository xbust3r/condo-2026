import magic

class ImagesUtils:
    
    @staticmethod
    async def CheckPictureMimetype(picture_data):
        """
        Check mimetype
        """
        # Check mimetype
        mime = magic.Magic(mime=True)
        mimetype = mime.from_buffer(picture_data["content"])

        if mimetype not in ["image/jpeg", "image/png"]:
            return None
        else:
            return True
        
    @staticmethod
    async def GetExtensionByMimetype(mimetype):
        """
        Get extension by mimetype
        """
        if mimetype == "image/jpeg":
            return ".jpg"
        elif mimetype == "image/png":
            return ".png"
        elif mimetype == "application/pdf":
            return ".pdf"
        else:
            return None