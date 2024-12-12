[app]

# (str) Название вашего приложения
title = Chat Test

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
    openai==1.3.7,\
    requests==2.31.0,\
    charset-normalizer==3.3.2,\
    idna==3.6,\
    urllib3==2.1.0,\
    certifi==2023.11.17,\
    twisted==23.10.0,\
    pillow,\
    https://github.com/kivymd/KivyMD/archive/master.zip,\
    sdl2_ttf==2.0.15,\
    emojis

# (str) Пользовательская иконка приложения (*.png)
icon.filename = %(source.dir)s/icon.png

# (str) Версионирование приложения
version = 1.0.0

# (list) Разрешения
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Целевая версия Android API
android.api = 33

# (int) Минимальная версия Android API
android.minapi = 21

# (int) Android SDK версия
android.sdk = 33

# (str) Android NDK версия
android.ndk = 25b

# (bool) Использовать --private данные
android.private_storage = True

# (bool) Копировать библиотеку python вместо использования системной
android.copy_libs = 1

# (str) Имя python-for-android ветки для использования
p4a.branch = master

# (str) Имя автора приложения
author = Your Name

# (str) Presplash цвет фона
android.presplash_color = #202123

# (bool) Включить оптимизацию при компиляции в .pyc файлы
optimize-python = True

# (list) Список модулей Python для включения
android.enable_androidx = True

# (list) The Android archs to build for
android.archs = armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (list) Android application meta-data
android.meta_data = android.support.FILE_PROVIDER_PATHS=paths.xml

# (list) Android библиотеки для добавления
android.add_libs_armeabi_v7a = libs/android/*.so
android.add_libs_arm64_v8a = libs/android/*.so

# (list) Дополнительные jar файлы
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) Gradle зависимости
android.gradle_dependencies = "androidx.core:core:1.6.0"

# (bool) Использовать --private данные
android.private_storage = True

# (str) python-for-android fork для использования
p4a.fork = kivy

# (str) python-for-android branch для использования
p4a.branch = master

# (str) bootstrap для использования
p4a.bootstrap = sdl2

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
