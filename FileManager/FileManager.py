from .models import File
import string, random
from django.contrib.postgres.search import SearchVector
import string
arabic_number = {1776: 48,  # 0
                 1777: 49,  # 1
                 1778: 50,  # 2
                 1779: 51,  # 3
                 1780: 52,  # 4
                 1781: 53,  # 5
                 1782: 54,  # 6
                 1783: 55,  # 7
                 1784: 56,  # 8
                 1785: 57}  # 9


class FileController:
    def __init__(self):
        self.map_punc_space = str.maketrans(string.punctuation, ' '*(len(string.punctuation)))

    @staticmethod
    def make_id(n=6):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    @staticmethod
    def clean_text(text):
        if text is None:
            return ''
        text = text.translate(text)
        text = text.translate(arabic_number)
        text = text.replace(b'\xe2\x80\x8c'.decode('utf-8'), ' ') # remove ZWSP :)
        return text

    def save(self, message, user):
        file = File.objects.filter(file_id=message.document.file_id).first()
        if file:
            return file.id
        id_ = self.make_id()
        name = ''.join(message.document.file_name.split('.')[:-1])
        name = self.clean_text(name)
        desc = self.clean_text(message.caption)
        search_field = name + desc
        File(
            id=id_,
            file_id=message.document.file_id,
            file_name=name,
            file_description=message.caption,
            search_field=search_field,
            file_size=message.document.file_size,
            mime_type=message.document.mime_type,
            sender=user,
        ).save(force_insert=True)
        return id_

    @staticmethod
    def get(id_):
        file = File.objects.filter(id=id_).first()
        file.download_count += 1
        file.save()
        return file

    @staticmethod
    def search_file(query):
        query = query.translate(arabic_number)
        return File.objects.annotate(
            search=SearchVector(
                'file_name',
                'file_description'
            )).filter(search=query).all()
