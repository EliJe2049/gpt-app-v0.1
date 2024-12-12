from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.theming import ThemeManager
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ColorProperty
import requests
import json
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.utils import platform
import emojis  # Добавляем импорт библиотеки emojis
import unicodedata
from kivy.base import EventLoop
from kivy.clock import Clock
from kivymd.uix.spinner import MDSpinner
from openai import OpenAI
import os
from functools import partial
import asyncio
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.threads import deferToThread
from kivy.animation import Animation
from kivymd.uix.snackbar import Snackbar
from kivy.core.clipboard import Clipboard
from datetime import datetime
from kivy.cache import Cache
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
import time

FONT_NAME = 'Roboto'

# Определяем шрифт в зависимости от платформы
if platform == 'android':
    FONT_NAME = 'Roboto'
elif platform == 'ios':
    FONT_NAME = 'Arial'
else:
    FONT_NAME = 'Roboto'  # Для десктопа тоже используем Roboto

# Настройки окна и клавиатуры
Window.softinput_mode = 'below_target'
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.keyboard_padding = 0
Window.allow_screensaver = True
Cache.register('kv.image', limit=10)
Cache.register('kv.texture', limit=10)

# Обновляем класс CustomTextInput
class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = None
        self.use_bubble = True
        self.use_handles = True
        self.background_color = [0, 0, 0, 0]
        self.cursor_width = '2sp'
        self.padding = [10, 10, 10, 10]
        self.multiline = True
        self.write_tab = False
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.scroll_y = 1
        self.line_spacing = 1.5
        # Добавляем флаг для отслеживания состояния фокуса
        self._is_focusable = True
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._is_focusable = True
            self.focus = True
            return super().on_touch_down(touch)
        return False

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            # Сохраняем фокус при отпускании
            self.focus = True
            return True
        return super().on_touch_up(touch)

    def _on_focus(self, instance, value, *largs):
        super()._on_focus(instance, value, *largs)
        if value and self._is_focusable:
            Window.softinput_mode = 'below_target'
            # Добавляем небольшую задержку для корректной прокрутки
            Clock.schedule_once(lambda dt: self.scroll_to_cursor(), 0.1)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Добавляем обработку Enter с Shift для переноса строки
        if keycode[1] == 'enter' and 'shift' in modifiers:
            self.insert_text('\n')
            return True
        elif keycode[1] == 'enter':
            # Вызываем отправку сообщения при нажатии Enter
            self.parent.parent.parent.send_message(None)
            return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def scroll_to_cursor(self):
        """Прокрутка к текущей позиции курсора"""
        # Получаем позицию курсора
        cursor_pos = self.cursor_pos
        if not cursor_pos:
            return

        # Получаем координаты курсора в пикселях
        cursor_y = self.cursor_pos[1]
        
        # Получаем размеры viewport
        viewport_height = self.height - self.padding[1] - self.padding[3]
        
        # Вычисляем позицию прокрутки
        total_height = len(self._lines) * self.line_height
        if total_height > viewport_height:
            # Определяем позицию курсора относительно общей высоты
            cursor_relative_y = cursor_y * self.line_height
            
            # Устанавливаем scroll_y так, чтобы курсор был виден
            if cursor_relative_y < self.scroll_y * total_height:
                self.scroll_y = max(0, cursor_relative_y / total_height)
            elif cursor_relative_y > (self.scroll_y * total_height) + viewport_height:
                self.scroll_y = min(1, (cursor_relative_y - viewport_height) / total_height)

class ChatApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Teal"
        self.bg_dark = "#343541"
        self.message_user_color = "#343541"
        self.message_bot_color = "#444654"
        self.text_color = "#FFFFFF"
        Window.size = (400, 700)
        Window.clearcolor = (0.204, 0.208, 0.255, 1)
        
        # Добавляем обработчик закрытия
        Window.bind(on_request_close=self.on_request_close)
        
    def on_request_close(self, *args):
        """Корректное закрытие приложения"""
        self.stop()
        return True
    
    def on_stop(self):
        """Вызывается при закрытии приложения"""
        try:
            # Останавливаем все запланированные события
            Clock.unschedule_all()
            
            # Останавливаем reactor
            if reactor.running:
                reactor.callFromThread(reactor.stop)
        except:
            pass
    
    def build(self):
        # Добавляем проверку подключения к интернету
        if not self.check_internet_connection():
            self.show_error_dialog("Нет подключения к интернету")
        return ChatScreen()

    def check_internet_connection(self):
        """Проверяет наличие подключения к интернету"""
        try:
            # Пробуем подключиться к надежному серверу
            requests.get("https://www.google.com", timeout=3)
            return True
        except:
            return False

    def show_error_dialog(self, message):
        """Показывает диалог с ошибкой"""
        snackbar = Snackbar(
            text=message,
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=0.95,
            bg_color=(0.8, 0, 0, 1)
        )
        snackbar.open()

class ChatScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(
            orientation='vertical',
            spacing=0,
            padding=0,
            md_bg_color=self.theme_cls.bg_dark
        )
        
        self.header = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            md_bg_color="#202123",
            padding=[dp(15), 0]
        )
        
        self.header_label = MDLabel(
            text="ChatGPT",
            halign="center",
            theme_text_color="Custom",
            text_color="#FFFFFF",
            font_style="H6",
            bold=True
        )
        self.header.add_widget(self.header_label)
        
        self.scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(10),
            bar_color=(0.7, 0.7, 0.7, 0.3),
            bar_inactive_color=(0.7, 0.7, 0.7, 0.1)
        )
        
        self.message_history = MessageHistory()
        self.scroll.add_widget(self.message_history)
        
        self.message_input = MessageInput()
        
        self.layout.add_widget(self.header)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.message_input)
        
        self.add_widget(self.layout)

class MessageInput(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(100)
        self.padding = [dp(15), dp(15), dp(15), dp(15)]
        self.md_bg_color = "#202123"
        
        self.input_container = MDCard(
            orientation='horizontal',
            size_hint_y=None,
            size_hint_x=0.95,
            height=dp(55),
            radius=[dp(10)],
            padding=[dp(15), dp(5)],
            pos_hint={'center_x': 0.5},
            md_bg_color="#2D2D35",
            elevation=0,
            line_color="#3E3F4B",
            line_width=1
        )
        
        self.text_input = CustomTextInput(
            hint_text="Message ChatGPT...",
            size_hint=(1, None),
            height=dp(45),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            selection_color=(0.5, 0.5, 0.5, 0.3),
            font_size='16sp',
            font_name=FONT_NAME,
            hint_text_color=(0.5, 0.5, 0.5, 1),
            background_active='',
            background_normal=''
        )
        
        # Устанавливаем начальный фокус после инициализации
        Clock.schedule_once(lambda dt: setattr(self.text_input, 'focus', True), 0.5)
        
        self._min_height = dp(45)
        self._max_height = dp(120)
        
        self.text_input.bind(
            text=self.on_text_change
        )
        
        self.send_button = MDIconButton(
            icon="send",
            theme_icon_color="Custom",
            icon_color="#7D7D8C",
            pos_hint={'center_y': 0.5},
            ripple_scale=0.5,
            on_release=self.send_message
        )
        
        self.send_button.bind(
            on_enter=lambda x: setattr(self.send_button, 'icon_color', "#FFFFFF"),
            on_leave=lambda x: setattr(self.send_button, 'icon_color', "#7D7D8C")
        )
        
        self.text_container = MDBoxLayout(
            size_hint=(1, None),
            height=dp(45),
            padding=[0, 0, dp(10), 0]
        )
        self.text_container.add_widget(self.text_input)
        
        self.input_container = MDBoxLayout(
            size_hint=(1, None),
            height=dp(45),
            padding=[0, 0, dp(10), 0]
        )
        self.input_container.add_widget(self.text_container)
        self.input_container.add_widget(self.send_button)
        self.add_widget(self.input_container)
    
    def on_text_change(self, instance, value):
        # Улучшенная обработка высоты текстового поля
        lines = len(value.split('\n'))
        line_height = dp(20)
        padding = dp(10)
        new_height = min(max(self._min_height, (lines * line_height) + padding), self._max_height)
        
        # Обновляем высоту всех компонентов
        self.text_input.height = new_height
        self.text_container.height = new_height
        self.input_container.height = new_height + dp(10)
        self.height = new_height + dp(30)
        
        # Используем встроенный метод cursor_offset вместо scroll_to_cursor
        Clock.schedule_once(lambda dt: setattr(self.text_input, '_cursor_offset',
                                             self.text_input.cursor_offset()), 0.1)
    
    def clean_text(self, text):
        """Очищаем текст от проблемных символов"""
        # Номализуем Unicode
        text = unicodedata.normalize('NFKC', text)
        # Удаляем невидимые символы
        return ''.join(char for char in text if not unicodedata.category(char).startswith('C'))
    
    def send_message(self, instance):
        text = self.text_input.text.strip()
        if text:
            try:
                screen = self.parent.parent
                cleaned_text = self.clean_text(text)
                screen.message_history.add_message(cleaned_text)
                
                screen.message_history.show_loading()
                
                self.text_input.text = ""
                self.text_input.height = self._min_height
                self.text_container.height = self._min_height
                self.input_container.height = self._min_height + dp(10)
                self.height = self._min_height + dp(55)
                
                Clock.schedule_once(lambda dt: setattr(self.text_input, 'focus', True), 0.1)
                
                d = deferToThread(self.get_gpt_response, cleaned_text)
                d.addCallback(lambda response: self.handle_response(response, screen.message_history))
                d.addErrback(self.handle_error)
                
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
    
    def get_gpt_response(self, text):
        """Получаем ответ от GPT API"""
        try:
            client = OpenAI(
                api_key='sk-D9q5ESTWg9ttOAC2o7hA8LNHgmR2cXKN',
                base_url="https://api.proxyapi.ru/openai/v1",
                timeout=30.0
            )
            
            # Получаем историю сообщений
            screen = self.parent.parent
            messages = screen.message_history.message_store.get_messages()
            
            # Добавляем текущее сообщение
            messages.append({"role": "user", "content": text})
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,  # Передаем всю историю сообщений
                        max_tokens=1000,
                        timeout=30
                    )
                    response = completion.choices[0].message.content
                    
                    # Сохраняем ответ в историю
                    screen.message_history.message_store.add_message(response, is_user=False)
                    return response
                    
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"Попытка {attempt + 1} не удалась: {e}")
                    time.sleep(1)
                
        except Exception as e:
            print(f"Ошибка при получении ответа от GPT: {e}")
            return "Извините, произошла ошибка при генерации ответа. Пожалуйста, попробуйте позже."
    
    def handle_response(self, response, message_history):
        """Обрабатывает полученный ответ"""
        message_history.hide_loading()
        message_history.add_message(response, is_user=False)
    
    def handle_error(self, failure):
        """Обрабатывает ошибки при получении ответа"""
        print(f"Произошла ошибка: {failure.getErrorMessage()}")
        screen = self.parent.parent
        screen.message_history.hide_loading()
        screen.message_history.add_message("Извините, произошла ошибка при обработке запроса.", is_user=False)

class MessageStore:
    def __init__(self):
        self.messages = []
        self.max_messages = 20
    
    def add_message(self, text, is_user=True):
        """Добавляет сообщение в историю"""
        message = {
            "role": "user" if is_user else "assistant",
            "content": text
        }
        self.messages.append(message)
        
        # Оставляем только последние max_messages сообщений
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self):
        """Возвращает список сообщений для API"""
        return self.messages.copy()
    
    def clear(self):
        """Очищает историю сообщений"""
        self.messages = []

class MessageHistory(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.loading_card = None
        self.loading_dots = None
        self.loading_anim = None
        self.message_store = MessageStore()  # Заменяем chat_history на message_store
        
        # Добавляем буферизацию для прокрутки
        self._scroll_timeout = None
        
        # Загружаем историю при запуске
        Clock.schedule_once(self.load_chat_history, 0.1)
    
    def scroll_to_bottom(self, *args):
        """Прокручивает чат к последнему сообщению"""
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)
    
    def _scroll_to_bottom(self):
        """Выполняет прокрутку к последнему сообщению"""
        scroll_view = self.parent
        if hasattr(scroll_view, 'scroll_y'):
            self.height = self.minimum_height
            # Анимируем прокрутку для плавности
            Animation(scroll_y=0, duration=0.1).start(scroll_view)
    
    def load_chat_history(self, dt):
        """Загружает и отображает историю чата"""
        history = self.message_store.get_messages()
        for message in history:
            self.add_message(message['content'], message['role'] == 'assistant', save_history=False)
    
    def _create_message_content(self, text, is_user):
        """Создает контент сообщения"""
        content_box = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            adaptive_height=True
        )
        
        message_label = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color="#FFFFFF",
            size_hint_y=None,
            font_name=FONT_NAME,
            font_size='16sp',
            halign='left',
            valign='middle'
        )
        
        message_label.bind(
            width=lambda *x: message_label.setter('text_size')(
                message_label, (message_label.width - dp(40), None)
            ),
            texture_size=lambda *x: message_label.setter('height')(
                message_label, message_label.texture_size[1]
            )
        )
        
        content_box.add_widget(message_label)
        
        # Добавляем кнопку копирования только для сообщений бота
        if not is_user:
            copy_button = MDIconButton(
                icon="content-copy",
                theme_icon_color="Custom",
                icon_color="#7D7D8C",
                pos_hint={'center_y': 0.5},
                size_hint=(None, None),
                size=(dp(30), dp(30)),
                on_release=lambda x: self.copy_to_clipboard(text)
            )
            content_box.add_widget(copy_button)
        
        return content_box

    @mainthread
    def add_message(self, text, is_user=True, save_history=True):
        """Оптимизированное добавление сообщений"""
        try:
            if save_history:
                self.message_store.add_message(text, is_user)
            
            # Создаем сообщение
            message_card = self._create_message_card(text, is_user)
            self.add_widget(message_card)
            
            # Устанавливаем начальную прозрачность
            message_card.opacity = 0
            
            # Анимация появления
            anim = Animation(opacity=1, duration=0.2)
            anim.start(message_card)
            
            # Буферизируем прокрутку
            Clock.schedule_once(lambda dt: self._buffer_scroll(), 0.1)
            
        except Exception as e:
            print(f"Ошибка при отображении сообщения: {e}")

    def _buffer_scroll(self):
        """Буферизированная прокрутка"""
        if self._scroll_timeout:
            Clock.unschedule(self._scroll_timeout)
        self._scroll_timeout = Clock.schedule_once(
            lambda dt: Animation(scroll_y=0, duration=0.2).start(self.parent), 
            0.1
        )
    
    def _create_message_card(self, text, is_user):
        """Создает карточку сообщения"""
        # Выносим создание карточки в отдельный метод для оптимизации
        message_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            size_hint_x=0.85,
            pos_hint={'right': 0.98} if is_user else {'x': 0.02},
            padding=[dp(15), dp(12)],
            radius=[dp(15)],
            elevation=0,
            md_bg_color="#343541" if is_user else "#444654",
            line_color="#4A4B52",
            line_width=1
        )
        
        # Создаем контент
        content = self._create_message_content(text, is_user)
        message_card.add_widget(content)
        message_card.bind(minimum_height=message_card.setter('height'))
        
        return message_card
    
    def show_loading(self):
        """Показывает улучшенную анимацию загрузки"""
        self.loading_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            size_hint_x=0.85,
            height=dp(50),
            pos_hint={'x': 0.02},
            padding=[dp(15), dp(8)],
            radius=[dp(15)],
            elevation=0,
            md_bg_color="#444654",
            line_color="#4A4B52",
            line_width=1
        )
        
        loading_box = MDBoxLayout(
            adaptive_height=True,
            padding=[dp(5), dp(5)]
        )
        
        # Создаем три точки для анимации
        dots_container = MDBoxLayout(
            spacing=dp(4),
            adaptive_size=True
        )
        
        self.loading_dots = []
        for i in range(3):
            dot = MDLabel(
                text="•",
                theme_text_color="Custom",
                text_color="#FFFFFF",
                font_size='24sp',
                size_hint=(None, None),
                size=(dp(10), dp(10)),
                opacity=0.3
            )
            self.loading_dots.append(dot)
            dots_container.add_widget(dot)
        
        loading_box.add_widget(dots_container)
        self.loading_card.add_widget(loading_box)
        self.add_widget(self.loading_card)
        
        # Создаем последовательную анимацию точек
        self.animate_loading_dots()
        self.scroll_to_bottom()

    def animate_loading_dots(self, *args):
        if not self.loading_dots:
            return
        
        animations = []
        for i, dot in enumerate(self.loading_dots):
            anim = Animation(opacity=1, duration=0.3) + \
                   Animation(opacity=0.3, duration=0.3)
            anim.start(dot)
            
            # Добавляем задержку для каждой следующей точки
            if i < len(self.loading_dots) - 1:
                Clock.schedule_once(
                    lambda dt, next_dot=self.loading_dots[i + 1]:
                    Animation(opacity=1, duration=0.3).start(next_dot),
                    0.1 * (i + 1)
                )
        
        # Повторяем анимацию
        Clock.schedule_once(self.animate_loading_dots, 0.9)

    def hide_loading(self):
        """Скрывает анимацию загрузки"""
        if self.loading_card:
            self.remove_widget(self.loading_card)
            self.loading_card = None
            self.loading_dots = None

    def copy_to_clipboard(self, text):
        """Копирует текст в буфер обмена"""
        try:
            Clipboard.copy(text)
            
            # Создаем кастомный MDCard для уведомления
            notification = MDCard(
                size_hint=(None, None),
                size=(dp(200), dp(40)),
                pos_hint={'center_x': 0.5, 'y': 0.02},
                md_bg_color="#2D2D35",
                radius=[5, 5, 5, 5],
                elevation=4,
                padding=[dp(10), dp(5)]
            )
            
            # Добавляем текст уведомления
            label = MDLabel(
                text="Текст скопирован",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_style="Caption",
                font_name=FONT_NAME
            )
            notification.add_widget(label)
            
            # Добавляем уведомление на экран
            screen = self.parent.parent
            screen.add_widget(notification)
            
            # Анимация появления и исчезновения
            notification.opacity = 0
            anim = (Animation(opacity=1, duration=0.2) + 
                   Animation(opacity=1, duration=1.0) +
                   Animation(opacity=0, duration=0.2))
            
            def on_complete(anim, widget):
                screen.remove_widget(widget)
            
            anim.bind(on_complete=on_complete)
            anim.start(notification)
            
        except Exception as e:
            print(f"Ошибка при копировании в буфер обмена: {e}")

if __name__ == '__main__':
    try:
        app = ChatApp()
        app.run()
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
    finally:
        # Очищаем кэш при выходе
        Cache.print_usage()
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
