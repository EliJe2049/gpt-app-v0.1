[app]

# (str) Название вашего приложения
title =  Chat Test

# (str) Пакет приложения
package.name = chatgpt_mobile

# (str) Домен пакета
package.domain = org.chatgpt

# (str) Исходный код приложения
source.dir = .

# (list) Исходные файлы для включения (позволяет использовать шаблоны)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Список приложений для включения
requirements = python3,\
    kivy==2.2.1,\
    kivymd==1.1.1,\
    openai==1.3.7,\
    requests==2.31.0,\
    charset-normalizer==3.3.2,\
    idna==3.6,\
    urllib3==2.1.0,\
    certifi==2023.11.17,\
    twisted==23.10.0,\
    pillow

# (str) Пользовательская иконка приложения (*.png)
icon.filename = %(source.dir)s/icon.png

# (str) Версионирование приложения
version = 1.0.0

# (list) Разрешения
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Целевая версия Android API (��екомендуется последняя стабильная)
android.api = 33

# (int) Минимальная версия Android API
android.minapi = 21

# (int) Android SDK версия (рекомендуется последняя)
android.sdk = 33

# (str) Android NDK версия
android.ndk = 25b

# (bool) Использовать --private данные
android.private_storage = True

# (str) Android NDK директория (если пустая - будет скачана автоматически)
#android.ndk_path =

# (str) Android SDK директория (если пустая - будет скачана автоматически)
#android.sdk_path =

# (str) ANT директория (если пустая - будет скачана автоматически)
#android.ant_path =

# (bool) Копировать библиотеку python вместо использования системной
android.copy_libs = 1

# (str) Имя python-for-android ветки для использования
p4a.branch = master

# (str) OUYA Console категория. Должна быть одной из GAME или APP
# Если вы оставите это пустым, оно по умолчанию будет приложением.
#android.ouya.category = GAME

# (str) Имя автора прилож��ния
author = Your Name

# (str) URL автора
#author.url = http://example.com

# (str) Описание приложения
#description = My Application Description

# (str) Полный путь к keystore файлу
#android.keystore = /path/to/keystorefile

# (str) Псевдоним keystore
#android.keyalias = mykeyalias

# (str) Пароль keystore
#android.keystore_password = keystorepassword

# (str) Пароль ключа keystore
#android.keyalias_password = keyaliaspassword

# (bool) Отключить режим отладки
#android.release_artifact = false

# (str) URL для автоматического обновления приложения
#update_url =

# (str) Пользовательский источник сборки (если не указан, используется по умолчанию)
#source.include_patterns = assets/*,images/*.png

# (list) Сервисы Garden для включения
#garden_requirements =

# (str) Presplash анимация
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Presplash цвет фона
android.presplash_color = #202123

# (list) Файлы для включения в .apk
android.add_src = %(source.dir)s/icon.png

# (bool) Указывает, следует ли пропустить компиляцию python в .pyc файлы
no-compile-pyo = False

# (bool) Включить оптимизацию при компиляции в .pyc файлы
optimize-python = True

# (list) Список модулей Python для включения
android.enable_androidx = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

[buildozer]

# (int) Уровень лога (0 = ошибка только, 1 = инфо, 2 = отладка)
log_level = 2

# (int) Отображать предупреждения
warn_on_root = 1

# (str) Путь к adb
#android.adb_path =

# (str) Путь к Java домашней директории
#java_home =

# (str) Путь к python-for-android домашней директории
#p4a_path =

# (str) Путь к ccache
#ccache = 
