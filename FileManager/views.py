from django.http import JsonResponse
from FileManager.models import File
from FileManager.FileManager import FileController
# Create your views here.
fc = FileController()


def update_search_file_text_view(request):
    files = File.objects.all()
    for file in files:
        try:
            name = fc.clean_text(file.file_name)
            desc = fc.clean_text(file.file_description)
            file.search_field = name + desc
            file.save(force_update=True)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'description': str(e)})
    return JsonResponse({'status': 'OK'})

