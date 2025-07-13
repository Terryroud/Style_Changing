# StarGAN Face Attributes Transfer

## Описание продукта

Это веб-приложение для изменения атрибутов лица с использованием дообученной мною модели StarGAN. Пользователи могут загружать фотографии и применять различные изменения:
- Изменение цвета волос (черные, светлые, каштановые)
- Изменение пола
- Изменение возраста

## Структура проекта

```
project/
├── ai_model/
│   ├── stargan_celeba_128/
│   │   ├── models/              # Модели нейросети
│   │   ├── my_results/          # Результаты обработки
│   │   └── list_attr_celeba.txt # Файл атрибутов изображений
│   ├── data_loader.py           # Загрузчик данных
│   ├── logger.py                # Логирование
│   ├── main.py                  # Основной скрипт модели
│   ├── model.py                 # Архитектура модели
│   ├── solver.py                # Обучение и тестирование
│   └── style_changing.py        # Интерфейс для работы с моделью
├── media/
│   ├── uploads/                 # Загруженные пользователями изображения
│   └── results/                 # Результаты обработки
├── static/
│   └── js/
│       └── script.js            # Клиентские скрипты
├── templates/
│   └── index.html               # Главная страница
├── manage.py                    # Django management script
└── requirements.txt             # Зависимости
```

## Как это работает

1. **Пользователь загружает фото** (рекомендуется 178×178 px)
2. **Указывает исходные характеристики**:
   - Пол (мужской/женский)
   - Цвет волос
   - Возраст
3. **Выбирает желаемый атрибут** для изменения
4. **Система обрабатывает изображение**:
   - Сохраняет метаданные в `list_attr_celeba.txt`
   - Применяет модель StarGAN
   - Возвращает результат
5. **Пользователь скачивает** измененное изображение

## Установка и запуск

### Требования
- Python 3.8+
- Django 3.2+
- PyTorch 1.8+
- CUDA (рекомендуется для GPU)

### Инструкция по установке

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-repo/stargan-face-transfer.git
cd stargan-face-transfer
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте Django:
```bash
python manage.py migrate
```

4. Запустите сервер:
```bash
python manage.py runserver
```

5. Откройте в браузере:
```
http://127.0.0.1:8000
```

### Настройка модели

1. Поместите предобученные веса модели в:
```
ai_model/stargan_celeba_128/models/200000-G.ckpt
```

2. Убедитесь, что существуют папки:
```
media/uploads/
media/results/
```

## Примеры использования

1. Изменение цвета волос с черных на светлые
2. Изменение пола с женского на мужской
3. Омоложение лица

## Источник

Этот проект основан на исследовательской работе StarGAN:

- Choi, Y., Choi, M., Kim, M., Ha, J., Kim, S., & Choo, J. (2018). **StarGAN: Unified Generative Adversarial Networks for Multi-Domain Image-to-Image Translation**. *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*.
  [![arXiv](https://img.shields.io/badge/arXiv-1711.09020-b31b1b)](https://arxiv.org/abs/1711.09020)

## Контакты

Для вопросов и предложений:

Почта: kolibri.alia@yandex.ru

Телеграм: @alia_work
