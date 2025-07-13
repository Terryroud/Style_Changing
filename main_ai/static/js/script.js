document.addEventListener('DOMContentLoaded', function() {
    const contentUploadArea = document.getElementById('contentUploadArea');
    const contentInput = document.getElementById('contentInput');
    const contentPreview = document.getElementById('contentPreview');
    const transferBtn = document.getElementById('transferBtn');
    const resultContainer = document.getElementById('resultContainer');
    const resultImage = document.getElementById('resultImage');

    contentUploadArea.addEventListener('click', () => contentInput.click());

    contentInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                contentPreview.src = e.target.result;
                contentPreview.classList.remove('d-none');
                transferBtn.disabled = false;
            };
            reader.readAsDataURL(file);
        }
    });

    transferBtn.addEventListener('click', function() {
        const file = contentInput.files[0];
        if (!file) return;

        const selectedAttr = document.querySelector('input[name="attribute"]:checked');
        if (!selectedAttr) {
            alert('Выберите один атрибут');
            return;
        }

        const formData = new FormData();
        formData.append('content_image', file);
        formData.append('attribute', selectedAttr.value);

        formData.append('gender', document.querySelector('input[name="gender"]:checked').value);
        formData.append('hair_color', document.querySelector('select[name="hair_color"]').value);
        formData.append('age', document.querySelector('input[name="age"]').value);

        document.getElementById('loadingIndicator').style.display = 'block';
        resultContainer.style.display = 'none';

        const oldDownloadBtn = document.getElementById('downloadBtn');
        if (oldDownloadBtn) {
            oldDownloadBtn.remove();
        }

        fetch('/main_ai/transfer/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(async response => {
            if (!response.ok) {
                const error = await response.json().catch(() => null);
                throw new Error(error?.error || 'Server error');
            }
            return response.json();
        })
        .then(data => {
            if (!data.result_url) {
                throw new Error('Invalid response format');
            }

            resultImage.src = data.result_url;
            resultImage.style.maxWidth = '100%';
            resultImage.style.maxHeight = '400px';
            resultImage.style.width = 'auto';
            resultImage.style.height = 'auto';
            resultImage.style.objectFit = 'contain';
            resultContainer.style.display = 'block';

            const downloadContainer = document.createElement('div');
            downloadContainer.className = 'mt-3 text-center';

            const downloadBtn = document.createElement('a');
            downloadBtn.id = 'downloadBtn';
            downloadBtn.href = data.result_url;
            downloadBtn.className = 'btn btn-success';
            downloadBtn.textContent = 'Скачать результат';
            downloadBtn.download = 'result_' + file.name;

            downloadContainer.appendChild(downloadBtn);

            const oldDownloadContainer = document.getElementById('downloadContainer');
            if (oldDownloadContainer) {
                oldDownloadContainer.remove();
            }

            downloadContainer.id = 'downloadContainer';
            resultContainer.appendChild(downloadContainer);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ошибка: ' + (error.message || 'Неизвестная ошибка'));
        })
        .finally(() => {
            document.getElementById('loadingIndicator').style.display = 'none';
        });
    });

    // Функция для получения CSRF-токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});