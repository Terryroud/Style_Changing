from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import time
from ai_model.main import Transfer

def get_latest_uploaded_image():
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

    files = []
    for filename in os.listdir(upload_dir):
        filepath = os.path.join(upload_dir, filename)
        if os.path.isfile(filepath):
            files.append({
                'name': filename,
                'path': filepath,
                'created': os.path.getctime(filepath)
            })

    files.sort(key=lambda x: x['created'], reverse=True)

    return files[0]['path'] if files else None

@csrf_exempt
def transfer_style_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        if 'content_image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)

        content_image = request.FILES['content_image']

        if not content_image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            return JsonResponse({'error': 'Invalid image format'}, status=400)

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        attribute = request.POST.get('attribute')
        print(attribute)
        gender = request.POST.get('gender', 'male')
        hair_color = request.POST.get('hair_color', 'Black_Hair')
        age = int(request.POST.get('age', 0))

        gender_value = 1 if gender == 'male' else -1
        hair_values = {'Black_Hair': -1, 'Blond_Hair': -1, 'Brown_Hair': -1}
        hair_values[hair_color] = 1
        age_value = 1 if age < 40 else -1

        os.makedirs(upload_dir, exist_ok=True)

        timestamp = int(time.time())
        file_name = f"{timestamp}_{content_image.name}"
        content_path = os.path.join(upload_dir, file_name)

        with open(content_path, 'wb+') as f:
            for chunk in content_image.chunks():
                f.write(chunk)

        attr_file_path = os.path.join(settings.BASE_DIR, 'ai_model/stargan_celeba_128/list_attr_celeba.txt')

        with open(attr_file_path, 'r') as f:
            lines = f.readlines()

        attr_line = f"{file_name} "
        attr_line += "-1 " * 8
        attr_line += f"{hair_values['Black_Hair']} {hair_values['Blond_Hair']} -1 {hair_values['Brown_Hair']} "
        attr_line += "-1 " * 8
        attr_line += f"{gender_value} "
        attr_line += "-1 " * 18
        attr_line += f"{age_value}\n"

        del lines[-1]
        lines.append(attr_line)

        with open(attr_file_path, 'w') as f:
            f.writelines(lines)

        result = Transfer(attribute, content_path)

        result_dir = os.path.join(settings.MEDIA_ROOT, 'results')
        os.makedirs(result_dir, exist_ok=True)
        result_filename = f'result_{file_name}'
        result_path = os.path.join(result_dir, result_filename)
        result.save(result_path)

        return JsonResponse({
            'status': 'success',
            'result_url': f'{settings.MEDIA_URL}results/{result_filename}'
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def home(request):
    return render(request, 'index.html')