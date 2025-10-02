#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Страница загрузки с YouTube
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
from urllib.parse import urlparse, parse_qs
from core.validation import Validation
from core.downloader import Downloader
from I18N import tr


def detect_download_mode(url: str) -> str:
    """Return 'playlist' if URL is a playlist/mix, otherwise 'single'.
    Rules: list=<id> in query OR path '/playlist' => playlist; 'start_radio=1' or list starts with 'RD' => mix (also playlist).
    Shorts and normal watch without 'list' => single.
    """
    if not url:
        return 'single'
    try:
        p = urlparse(url)
        q = parse_qs(p.query)
        # explicit playlist endpoints
        if p.path.startswith('/playlist'):
            return 'playlist'
        # watch/any with list param (PL..., RD..., OLAK5uy... etc.)
        list_vals = q.get('list', [])
        if list_vals:
            return 'playlist'
        # radio/mix flag
        if q.get('start_radio', ['0'])[0] == '1':
            return 'playlist'
        # shorts are always single
        if '/shorts/' in p.path:
            return 'single'
        return 'single'
    except Exception:
        return 'single'


def is_rd_playlist(url: str) -> bool:
    """Проверить, является ли URL RD-плейлистом (MIX/радио)"""
    if not url:
        return False
    try:
        p = urlparse(url)
        q = parse_qs(p.query)
        list_vals = q.get('list', [])
        if list_vals:
            # Проверяем, начинается ли list с 'RD'
            return any(list_val.startswith('RD') for list_val in list_vals)
        return False
    except Exception:
        return False


def validate_url_or_warn(url: str) -> bool:
    """Валидация URL с улучшенным сообщением об ошибке"""
    allowed_domains = ['youtube.com', 'm.youtube.com', 'youtu.be']
    is_valid = any(domain in url for domain in allowed_domains)
    
    if not is_valid:
        domains_list = '\n'.join(allowed_domains)
        messagebox.showerror(tr('err.url.title'), tr('err.url.body', domains=domains_list))
    
    return is_valid


class YouTubePage:
    def __init__(self, app):
        self.app = app
        self.frame = None
        self.downloader = Downloader(app.config, app.i18n)
        self.setup_callbacks()
    
    def setup_callbacks(self):
        """Настроить колбэки для загрузчика"""
        self.downloader.progress_callback = self.on_progress
        self.downloader.status_callback = self.on_status
    
    def show(self):
        """Показать страницу"""
        if self.frame:
            self.frame.pack(fill=tk.BOTH, expand=True)
            return
        
        self.frame = ttk.Frame(self.app.content_frame)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        self.title_label = ttk.Label(self.frame, text=tr('title.youtube'),
                               font=('Arial', 16, 'bold'))
        self.title_label.pack(pady=(0, 20))
        
        # Основной контент
        self.create_content()
    
    def create_content(self):
        """Создать содержимое страницы"""
        # Левая панель - настройки
        left_frame = ttk.Frame(self.frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Поле ссылки
        self.link_frame = ttk.LabelFrame(left_frame, text=tr('yt.link.label'), padding=10)
        self.link_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self.link_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Привязываем обработчик изменения URL
        self.url_entry.bind('<KeyRelease>', self._on_url_change)
        self.url_entry.bind('<FocusOut>', self._on_url_change)
        
        # Обработчик Enter для запуска загрузки (независимо от раскладки)
        self.url_entry.bind('<Return>', self._on_enter_pressed)
        self.url_entry.bind('<KP_Enter>', self._on_enter_pressed)  # Numpad Enter
        
        # Опции загрузки
        options_frame = ttk.LabelFrame(left_frame, text=self.app.i18n.get('settings'), padding=10)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Тип загрузки - Radio Group
        self.download_mode_var = tk.StringVar(value="single")
        self.is_playlist_var = tk.BooleanVar(value=False)
        
        # Создаем radio group для режима загрузки
        mode_frame = ttk.Frame(options_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(mode_frame, text=self.app.i18n.get('download_mode') + ":", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        
        single_radio = ttk.Radiobutton(mode_frame, text=self.app.i18n.get('single_video'),
                                      variable=self.download_mode_var, value="single",
                                      command=self.on_type_change)
        single_radio.pack(anchor=tk.W, padx=(10, 0))
        
        playlist_radio = ttk.Radiobutton(mode_frame, text=self.app.i18n.get('playlist'),
                                       variable=self.download_mode_var, value="playlist",
                                       command=self.on_type_change)
        playlist_radio.pack(anchor=tk.W, padx=(10, 0))
        
        # Дополнительные опции для плейлиста (изначально скрыты)
        self.playlist_options_frame = ttk.Frame(options_frame)
        # Не упаковываем сразу - будет показан только при выборе плейлиста
        
        self.allow_mix_var = tk.BooleanVar()
        ttk.Checkbutton(self.playlist_options_frame, text=self.app.i18n.get('allow_mix'),
                       variable=self.allow_mix_var).pack(anchor=tk.W)
        
        first_n_frame = ttk.Frame(self.playlist_options_frame)
        first_n_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(first_n_frame, text=self.app.i18n.get('first_n')).pack(side=tk.LEFT)
        self.first_n_var = tk.StringVar(value="0")
        ttk.Entry(first_n_frame, textvariable=self.first_n_var, width=5).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Label(first_n_frame, text=self.app.i18n.get('all_zero')).pack(side=tk.LEFT)
        
        # Привязываем обновление видимости к изменению переменной режима
        self.download_mode_var.trace_add('write', self._on_mode_change)
        
        # Качество - Radio Group
        quality_frame = ttk.LabelFrame(left_frame, text=self.app.i18n.get('quality'), padding=10)
        quality_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.quality_var = tk.StringVar(value="best")
        
        # Создаем radio group для качества
        quality_mode_frame = ttk.Frame(quality_frame)
        quality_mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        qualities = [
            ("best", self.app.i18n.get('best')),
            ("1080p", "1080p"),
            ("720p", "720p"),
            ("480p", "480p"),
            ("360p", "360p")
        ]
        
        for value, text in qualities:
            ttk.Radiobutton(quality_mode_frame, text=text, variable=self.quality_var,
                           value=value).pack(anchor=tk.W)
        
        # Только аудио - отдельная секция
        audio_frame = ttk.Frame(quality_frame)
        audio_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.audio_only_var = tk.BooleanVar()
        ttk.Checkbutton(audio_frame, text=self.app.i18n.get('only_audio'),
                        variable=self.audio_only_var).pack(anchor=tk.W)
        
        # Кнопки управления
        self.create_control_buttons(left_frame)
        
        # Правая панель - прогресс и логи
        self.create_progress_panel()
        
        # Обновить видимость опций плейлиста в соответствии с текущим режимом
        self.update_playlist_options_visibility()
        
        # Обновить состояние опций плейлиста
        self.on_type_change()
    
    def _on_url_change(self, event=None):
        """Обработка изменения URL для автоопределения режима"""
        url = self.url_var.get().strip() if hasattr(self, 'url_var') else (self.url_entry.get().strip() if hasattr(self, 'url_entry') else '')
        mode = detect_download_mode(url)
        
        # Обновляем режим загрузки если он изменился
        try:
            if mode != self.download_mode_var.get():
                self.download_mode_var.set(mode)
                # Обновляем видимость опций плейлиста
                self._on_mode_change()
                # Логируем изменение режима
                if hasattr(self, 'log_text'):
                    self.log_text.insert(tk.END, tr('info.mode.adjusted', m=mode) + "\n")
                    self.log_text.see(tk.END)
        except Exception:
            pass
    
    def _on_enter_pressed(self, event=None):
        """Обработка нажатия Enter для запуска загрузки"""
        # Проверяем, что загрузка не идет
        if not self.downloader.is_downloading_active():
            self.start_download()
    
    def _on_mode_change(self, *args):
        """Обработка изменения режима загрузки"""
        is_playlist = (self.download_mode_var.get() == "playlist")
        self.is_playlist_var.set(is_playlist)
        self.update_playlist_options_visibility()
    
    def update_playlist_options_visibility(self):
        """Обновить видимость опций плейлиста"""
        if self.is_playlist_var.get():
            # Показываем опции плейлиста
            self.playlist_options_frame.pack(fill=tk.X, pady=(5, 0))
        else:
            # Скрываем опции плейлиста
            self.playlist_options_frame.pack_forget()
    
    def create_control_buttons(self, parent):
        """Создать кнопки управления"""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.download_btn = ttk.Button(buttons_frame, text=self.app.i18n.get('download'),
                                     command=self.start_download, style='Accent.TButton')
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(buttons_frame, text=self.app.i18n.get('cancel'),
                                   command=self.cancel_download, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT)
    
    def create_progress_panel(self):
        """Создать панель прогресса"""
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Прогресс-бар
        progress_frame = ttk.LabelFrame(right_frame, text=self.app.i18n.get('progress'), padding=10)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, length=300)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Информация о прогрессе
        self.progress_info_var = tk.StringVar(value="Готов к загрузке")
        ttk.Label(progress_frame, textvariable=self.progress_info_var).pack()
        
        # Логи
        logs_frame = ttk.LabelFrame(right_frame, text=self.app.i18n.get('logs'), padding=10)
        logs_frame.pack(fill=tk.BOTH, expand=True)
        
        # Текстовое поле для логов
        self.log_text = tk.Text(logs_frame, height=15, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(logs_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Автосохранение логов
        self.auto_save_logs_var = tk.BooleanVar(value=self.app.config.get('auto_save_logs', False))
        ttk.Checkbutton(logs_frame, text=self.app.i18n.get('auto_save_logs'),
                       variable=self.auto_save_logs_var).pack(anchor=tk.W, pady=(5, 0))
    
    def on_type_change(self):
        """Обработка изменения типа загрузки"""
        self._on_mode_change()
    
    def start_download(self):
        """Начать загрузку"""
        url = self.url_var.get().strip()
        
        # Валидация URL с улучшенным сообщением
        if not url.strip():
            messagebox.showerror(tr('err.url.title'), tr('err.url.body', domains='youtube.com, m.youtube.com, youtu.be'))
            return
        
        if not validate_url_or_warn(url):
            return
        
        # Проверка RD-плейлиста и опции Allow MIX
        if is_rd_playlist(url) and not self.allow_mix_var.get():
            messagebox.showwarning(tr('warning.rd_playlist.title'), tr('warning.rd_playlist.body'))
            return
        
        # Финальная проверка URL vs выбранного режима
        selected_mode = self.download_mode_var.get()
        detected_mode = detect_download_mode(url)
        if selected_mode != detected_mode:
            # Автоматически выравниваем режим
            self.download_mode_var.set(detected_mode)
            if hasattr(self, 'log_text'):
                self.log_text.insert(tk.END, tr('info.mode.adjusted', m=detected_mode) + "\n")
                self.log_text.see(tk.END)
        
        # Получить настройки
        quality = self.quality_var.get()
        audio_only = self.audio_only_var.get()
        playlist = (self.download_mode_var.get() == "playlist")
        allow_mix = self.allow_mix_var.get()
        
        try:
            first_n = int(self.first_n_var.get()) if self.first_n_var.get().isdigit() else 0
        except ValueError:
            first_n = 0
        
        # Обновить интерфейс
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.progress_info_var.set("Начинаем загрузку...")
        
        # Очистить логи
        self.log_text.delete(1.0, tk.END)
        self.log("Начинаем загрузку...")
        
        # Получить cookies
        cookies_file = None
        if hasattr(self.app, 'cookie_manager') and self.app.cookie_manager:
            cookies_file = self.app.cookie_manager.get_cookies_file()
        
        # Запустить загрузку
        try:
            self.downloader.download(
                url=url,
                service='youtube',
                quality=quality,
                audio_only=audio_only,
                playlist=playlist,
                first_n=first_n,
                allow_mix=allow_mix,
                cookies_file=cookies_file
            )
        except Exception as e:
            self.log(f"Ошибка: {str(e)}")
            self.reset_ui()
            messagebox.showerror(self.app.i18n.get('error'), str(e))
    
    def cancel_download(self):
        """Отменить загрузку"""
        self.downloader.cancel_download()
        self.log("Загрузка отменена пользователем")
        self.reset_ui()
    
    def on_progress(self, percent, speed, eta):
        """Обработка прогресса загрузки"""
        self.progress_var.set(percent)
        
        # Форматирование скорости
        if speed:
            if speed > 1024 * 1024:
                speed_str = f"{speed / (1024 * 1024):.1f} MB/s"
            elif speed > 1024:
                speed_str = f"{speed / 1024:.1f} KB/s"
            else:
                speed_str = f"{speed:.0f} B/s"
        else:
            speed_str = "0 B/s"
        
        # Форматирование ETA
        if eta and eta > 0:
            eta_str = f"{eta // 60:02d}:{eta % 60:02d}"
        else:
            eta_str = "--:--"
        
        self.progress_info_var.set(f"{percent:.1f}% | {speed_str} | ETA: {eta_str}")
    
    def on_status(self, status, message):
        """Обработка изменения статуса"""
        if status == 'completed':
            self.log("Загрузка завершена успешно!")
            self.progress_info_var.set("Загрузка завершена")
            self.reset_ui()
        elif status == 'error':
            self.log(f"Ошибка загрузки: {message}")
            self.progress_info_var.set("Ошибка загрузки")
            self.reset_ui()
            messagebox.showerror(self.app.i18n.get('error'), message)
        elif status == 'canceled':
            self.log("Загрузка отменена")
            self.progress_info_var.set("Загрузка отменена")
            self.reset_ui()
    
    def log(self, message):
        """Добавить сообщение в лог"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
        # Автосохранение логов
        if self.auto_save_logs_var.get():
            self.save_logs()
    
    def save_logs(self):
        """Сохранить логи в файл"""
        try:
            import datetime
            log_file = self.app.config.get('download_dir', '') + '/youtube_log.txt'
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.datetime.now()}] {self.log_text.get(1.0, tk.END)}\n")
        except Exception as e:
            print(f"Ошибка сохранения логов: {e}")
    
    def reset_ui(self):
        """Сбросить интерфейс"""
        self.download_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
    
    def hide(self):
        """Скрыть страницу"""
        if self.frame:
            self.frame.pack_forget()
    
    def update_language(self):
        """Обновить язык"""
        if self.frame:
            # Обновить заголовок
            self.title_label.config(text=tr('title.youtube'))
            self.link_frame.config(text=tr('yt.link.label'))
            # Обновить другие элементы интерфейса
            if hasattr(self, 'progress_frame'):
                self.progress_frame.config(text=tr('yt.progress'))
            if hasattr(self, 'logs_frame'):
                self.logs_frame.config(text=tr('yt.history'))
            if hasattr(self, 'settings_frame'):
                self.settings_frame.config(text=tr('yt.settings'))
            if hasattr(self, 'quality_frame'):
                self.quality_frame.config(text=tr('yt.quality'))
            if hasattr(self, 'download_btn'):
                self.download_btn.config(text=tr('yt.download'))
            if hasattr(self, 'cancel_btn'):
                self.cancel_btn.config(text=tr('yt.cancel'))
