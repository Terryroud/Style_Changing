from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import StyleTransferResult
import os
from datetime import datetime
import uuid
import torch
from ai_model.style_changing import change_style

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def transfer_style_view(request):
    if request.method == 'POST':
        try:
            content_image = request.FILES['content_image']
            selected_attrs = request.POST.getlist('attributes[]')

            # Сохраняем загруженное изображение
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            content_path = os.path.join(upload_dir, content_image.name)

            with open(content_path, 'wb+') as f:
                for chunk in content_image.chunks():
                    f.write(chunk)

            # Обрабатываем изображение моделью
            result_path = change_style(
                content_path=content_path,
                selected_attrs=selected_attrs,
                output_dir=os.path.join(settings.MEDIA_ROOT, 'results')
            )

            # Сохраняем результат в БД
            result = StyleTransferResult(
                content_image=os.path.join('uploads', content_image.name),
                result_image=os.path.join('results', os.path.basename(result_path))
            result.save()

            return JsonResponse({
                'result_url': request.build_absolute_uri(result.result_image.url)
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)