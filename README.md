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
│   │   ├── models_11/           # Веса обученной на 11 атрибутах модели
│   │   ├── model_5/             # Веса обученной на 5 атрибутах модели
│   │   └── list_attr_celeba.txt # Файл атрибутов изображений
│   ├── data_loader.py           # Загрузчик данных
│   ├── logger.py                # Логирование
│   ├── main.py                  # Основной скрипт модели и интерфейс для работы с ней
│   ├── model.py                 # Архитектура модели
│   ├── solver.py                # Тестирование
├── main_ai/                     # Пользовательское web-приложение
|   ├── static/                  # Статические файлы
│   |   ├── css/
│   |   |   └── style.css        # Стили
│   |   ├── examples/            # Примеры обработки изображений
|   |   |   └──...
│   |   └── js/
│   |       └── script.js        # Клиентские скрипты
|   ├── templates/
│   |   └── index.html           # Front основной страницы
|   └──...                       # Остальные файлы Django приложения
├── media/                       # Автоматически создается при запуске сервиса
│   ├── uploads/                 # Загруженные пользователями изображения
│   └── results/                 # Результаты обработки
├── stylechanging/               # Основное приложение Django
|   └──...                       # Остальные файлы Django приложения
├── manage.py                    # Django management script
└── requirements.txt             # Зависимости
```

## Как это работает

1. **Пользователь загружает фото** (рекомендуется 178×178 px, иначе произойдет обрезка или произвольное достроение изображения. Изменить размеры изображения можно, например, на [сайте](https://www.visualwatermark.com/ru/image-resizer/))
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
git clone git@github.com:Terryroud/Style_Changing.git
cd stylechanging
```

2. Установите зависимости (желательно в venv):
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

## Немного про обучение модели
Я обучила модель StarGAN на датасете Celeba изменять атрибуты лица в двух разных вариантах:

- В рамках 5 атрибутов: ```Black_Hair Blond_Hair Brown_Hair Male Young```
- В рамках 11 атрибутов: ``` Black_Hair Blond_Hair Brown_Hair Male Young Heavy_Makeup Eyeglasses Attractive Bald Wearing_Lipstick Goatee```

Затем, протестировав оба варианта на своих изображениях и изображениях из датасета, я пришла к выводу, что первая модель работает гораздо лучше и меньше путается в процессе изменения атрибутов лица. Именно поэтому итоговый вариант проекта работает именно на модели по 5 атрибутам. 

Ниже можно увидеть разницу работы первого и второго вариантов работы модели:

5_attributes:
![5_attributes](images/5_attributes.jpg)
11_attributes:
![11_attributes](images/11_attributes.jpg)

## Источник

Этот проект основан на исследовательской работе StarGAN:

- Choi, Y., Choi, M., Kim, M., Ha, J., Kim, S., & Choo, J. (2018). **StarGAN: Unified Generative Adversarial Networks for Multi-Domain Image-to-Image Translation**. *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*.
  [![arXiv](https://img.shields.io/badge/arXiv-1711.09020-b31b1b)](https://arxiv.org/abs/1711.09020)

## Контакты

Для вопросов и предложений:

Почта: kolibri.alia@yandex.ru

Телеграм: https://t.me/alia_work
