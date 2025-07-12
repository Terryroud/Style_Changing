//document.addEventListener('DOMContentLoaded', function() {
//    // Элементы интерфейса
//    const contentUploadArea = document.getElementById('contentUploadArea');
//    const contentInput = document.getElementById('contentInput');
//    const contentPreview = document.getElementById('contentPreview');
//    const transferBtn = document.getElementById('transferBtn');
//    const loadingIndicator = document.getElementById('loadingIndicator');
//    const resultContainer = document.getElementById('resultContainer');
//    const resultImage = document.getElementById('resultImage');
//
//    // Загрузка изображения
//    contentUploadArea.addEventListener('click', () => contentInput.click());
//
//    contentInput.addEventListener('change', function(e) {
//        const file = e.target.files[0];
//        if (file && file.type.startsWith('image/')) {
//            const reader = new FileReader();
//            reader.onload = function(e) {
//                contentPreview.src = e.target.result;
//                contentPreview.classList.remove('d-none');
//                transferBtn.disabled = false;
//            };
//            reader.readAsDataURL(file);
//        }
//    });
//
//    transferBtn.addEventListener('click', async function() {
//        const file = contentInput.files[0];
//        if (!file) return;
//
//        // Получаем выбранный атрибут
//        const selectedAttr = document.querySelector('input[name="attribute"]:checked');
//        if (!selectedAttr) {
//            alert('Выберите один атрибут');
//            return;
//        }
//        const selectedAttrs = [selectedAttr.value];
//
//        const formData = new FormData();
//        formData.append('content_image', file);
//        selectedAttrs.forEach(attr => formData.append('attributes[]', attr));
//
//        // Показываем индикатор загрузки
//        loadingIndicator.style.display = 'block';
//        resultContainer.style.display = 'none';
//
//        try {
//            const response = await fetch('/transfer/', {
//                method: 'POST',
//                body: formData,
//                headers: {
//                    'X-CSRFToken': getCookie('csrftoken'),
//                },
//            });
//
//            if (!response.ok) {
//                const error = await response.json();
//                throw new Error(error.error || 'Ошибка сервера');
//            }
//
//            const data = await response.json();
//            if (!data.result_url) {
//                throw new Error('Некорректный ответ сервера');
//            }
//
//            // Показываем результат
//            resultImage.src = data.result_url;
//            resultContainer.style.display = 'block';
//
//            // Создаем кнопку скачивания ПОСЛЕ получения данных
//            const downloadBtn = document.createElement('a');
//            downloadBtn.href = data.result_url;
//            downloadBtn.className = 'btn btn-success mt-3';
//            downloadBtn.download = 'result_' + file.name;
//            downloadBtn.textContent = 'Скачать результат';
//
//            // Удаляем предыдущую кнопку если есть
//            const oldBtn = document.querySelector('.download-btn');
//            if (oldBtn) oldBtn.remove();
//
//            downloadBtn.classList.add('download-btn');
//            resultContainer.appendChild(downloadBtn);
//
//        } catch (error) {
//            console.error('Error:', error);
//            alert('Ошибка: ' + (error.message || 'Неизвестная ошибка'));
//        } finally {
//            loadingIndicator.style.display = 'none';
//        }
//    });
//
//    // Функция для получения CSRF-токена
//    function getCookie(name) {
//        const cookies = document.cookie.split(';');
//        for (let cookie of cookies) {
//            const [cookieName, cookieValue] = cookie.trim().split('=');
//            if (cookieName === name) {
//                return decodeURIComponent(cookieValue);
//            }
//        }
//        return null;
//    }
//});