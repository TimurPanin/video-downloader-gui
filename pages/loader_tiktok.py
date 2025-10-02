#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Страница загрузки с TikTok
"""

import tkinter as tk
from tkinter import ttk, messagebox
from core.validation import Validation
from core.downloader import Downloader
from I18N import tr


class TikTokPage:
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
        title_label = ttk.Label(self.frame, text=self.app.i18n.get('tiktok'),
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Основной контент
        self.create_content()
    
    def create_content(self):
        """Создать содержимое страницы"""
        # Левая панель - настройки
        left_frame = ttk.Frame(self.frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Поле ссылки
        link_frame = ttk.LabelFrame(left_frame, text=self.app.i18n.get('tt_link'), padding=10)
        link_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(link_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Обработчик Enter для запуска загрузки (независимо от раскладки)
        self.url_entry.bind('<Return>', self._on_enter_pressed)
        self.url_entry.bind('<KP_Enter>', self._on_enter_pressed)  # Numpad Enter
        
        # Качество
        quality_frame = ttk.LabelFrame(left_frame, text=self.app.i18n.get('quality'), padding=10)
        quality_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.quality_var = tk.StringVar(value="best")
        qualities = [
            ("best", self.app.i18n.get('best')),
            ("720p", "720p"),
            ("480p", "480p")
        ]
        
        for value, text in qualities:
            ttk.Radiobutton(quality_frame, text=text, variable=self.quality_var,
                           value=value).pack(anchor=tk.W)
        
        # Только аудио
        self.audio_only_var = tk.BooleanVar()
        ttk.Checkbutton(quality_frame, text=self.app.i18n.get('only_audio'),
                        variable=self.audio_only_var).pack(anchor=tk.W, pady=(10, 0))
        
        # Кнопки управления
        self.create_control_buttons(left_frame)
        
        # Правая панель - прогресс и логи
        self.create_progress_panel()
    
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
    
    def _on_enter_pressed(self, event=None):
        """Обработка нажатия Enter для запуска загрузки"""
        # Проверяем, что загрузка не идет
        if not self.downloader.is_downloading_active():
            self.start_download()
    
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
    
    def start_download(self):
        """Начать загрузку"""
        url = self.url_var.get().strip()
        
        # Валидация URL
        is_valid, error_type = Validation.validate_url_for_service(url, 'tiktok')
        
        if not is_valid:
            if error_type == 'empty':
                messagebox.showerror(self.app.i18n.get('error'), 
                                   self.app.i18n.get('error_empty_url'))
            elif error_type == 'invalid_domain':
                messagebox.showerror(self.app.i18n.get('error'), 
                                   self.app.i18n.get('error_invalid_domain'))
            return
        
        # Получить настройки
        quality = self.quality_var.get()
        audio_only = self.audio_only_var.get()
        
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
                service='tiktok',
                quality=quality,
                audio_only=audio_only,
                playlist=False,
                first_n=0,
                allow_mix=False,
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
            log_file = self.app.config.get('download_dir', '') + '/tiktok_log.txt'
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
            from tkinter import font as tkfont
            for widget in self.frame.winfo_children():
                if isinstance(widget, ttk.Label):
                    font_name = widget.cget('font') if 'font' in widget.keys() else ''
                    try:
                        family = tkfont.nametofont(font_name).actual('family') if font_name else ''
                    except Exception:
                        family = str(font_name)
                    if family == 'Arial':
                        # Проверяем размер шрифта для заголовка
                        try:
                            size = tkfont.nametofont(font_name).actual('size') if font_name else 0
                            if size == 16:  # Заголовок
                                widget.config(text=self.app.i18n.get('tiktok'))
                                break
                        except Exception:
                            pass
