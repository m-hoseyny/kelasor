from .models import File
import string, random


class FileController:
    def __init__(self):
        pass

    @staticmethod
    def make_id(n=6):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    def save(self, message, user):
        file = File.objects.filter(file_id=message.document.file_id).first()
        if file:
            return file.id
        id_ = self.make_id()
        File(
            id=id_,
            file_id=message.document.file_id,
            file_name=message.document.file_name,
            file_description=message.caption,
            file_size=message.document.file_size,
            mime_type=message.document.mime_type,
            sender=user,
        ).save()
        return id_

    @staticmethod
    def get(id_):
        file = File.objects.filter(id=id_).first()
        file.download_count += 1
        file.save()
        return file
