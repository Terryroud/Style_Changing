document.addEventListener('DOMContentLoaded', function() {
    // Обработчики загрузки изображения
    document.getElementById('contentUploadArea').addEventListener('click', function() {
        document.getElementById('contentInput').click();
    });

    document.getElementById('contentInput').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file && file.type.match('image.*')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById('contentPreview');
                preview.src = e.target.result;
                preview.classList.remove('d-none');
                document.getElementById('transferBtn').disabled = false;
            }
            reader.readAsDataURL(file);
        }
    });

    // Обработчик кнопки
    document.getElementById('transferBtn').addEventListener('click', function() {
        const file = document.getElementById('contentInput').files[0];
        if (!file) return;

        const selectedAttrs = [];
        document.querySelectorAll('.form-check-input:checked').forEach(checkbox => {
            selectedAttrs.push(checkbox.value);
        });

        const formData = new FormData();
        formData.append('content_image', file);
        selectedAttrs.forEach(attr => formData.append('attributes[]', attr));

        // Показываем загрузку и делаем запрос
    });
});