#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Downloader — YouTube & TikTok
Главный модуль приложения
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import threading
from pathlib import Path

# Импорт модулей приложения
from core.config import Config
from core.i18n import I18n
from core.cookies import CookieManager
from pages.menu import MenuPage
from pages.loader_youtube import YouTubePage
from pages.loader_tiktok import TikTokPage
from I18N import tr, set_language


class VideoDownloaderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(tr('title.main'))
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Инициализация модулей
        self.config = Config()
        self.i18n = I18n(self.config.get('language', 'ru'))
        self.cookie_manager = CookieManager(self.i18n)
        
        # Текущая страница
        self.current_page = None
        self.pages = {}
        
        # Создание интерфейса
        self.create_interface()
        
        # Загрузка страниц
        self.load_pages()
        
        # Показать главное меню
        self.show_page('menu')
    
    def create_interface(self):
        """Создание основного интерфейса"""
        # Главный контейнер
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Панель инструментов
        self.create_toolbar()
        
        # Область контента
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
    
    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Кнопка "Назад"
        self.back_btn = ttk.Button(toolbar, text=tr('nav.back'), 
                                  command=self.go_back, state=tk.DISABLED)
        self.back_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Путь к папке загрузки
        download_frame = ttk.Frame(toolbar)
        download_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Label(download_frame, text=tr('common.download_dir')).pack(side=tk.LEFT)
        
        self.download_path_var = tk.StringVar(value=self.config.get('download_dir', ''))
        self.download_path_label = ttk.Label(download_frame, textvariable=self.download_path_var,
                                           relief=tk.SUNKEN, width=40)
        self.download_path_label.pack(side=tk.LEFT, padx=(5, 5))
        
        ttk.Button(download_frame, text=tr('common.change'), 
                  command=self.change_download_dir).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(download_frame, text=tr('common.open'), 
                  command=self.open_download_dir).pack(side=tk.LEFT)
        
        # Выбор языка
        lang_frame = ttk.Frame(toolbar)
        lang_frame.pack(side=tk.RIGHT)
        
        ttk.Label(lang_frame, text=self.i18n.get('language') + ":").pack(side=tk.LEFT)
        self.language_var = tk.StringVar(value=self.config.get('language', 'ru'))
        self.language_combo = ttk.Combobox(lang_frame, textvariable=self.language_var,
                                          values=['ru', 'en'], state='readonly', width=5)
        self.language_combo.pack(side=tk.LEFT, padx=(5, 0))
        self.language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
    
    def load_pages(self):
        """Загрузка всех страниц"""
        self.pages = {
            'menu': MenuPage(self),
            'youtube': YouTubePage(self),
            'tiktok': TikTokPage(self)
        }
    
    def show_page(self, page_name):
        """Показать указанную страницу"""
        # Скрыть текущую страницу
        if self.current_page:
            self.current_page.hide()
        
        # Показать новую страницу
        self.current_page = self.pages[page_name]
        self.current_page.show()
        
        # Обновить кнопку "Назад"
        if page_name == 'menu':
            self.back_btn.config(state=tk.DISABLED)
        else:
            self.back_btn.config(state=tk.NORMAL)
    
    def go_back(self):
        """Вернуться к главному меню"""
        self.show_page('menu')
    
    def change_download_dir(self):
        """Изменить папку загрузки"""
        new_dir = filedialog.askdirectory(
            title=self.i18n.get('change') + " " + self.i18n.get('download_dir'),
            initialdir=self.config.get('download_dir', '')
        )
        if new_dir:
            self.config.set('download_dir', new_dir)
            self.download_path_var.set(new_dir)
    
    def open_download_dir(self):
        """Открыть папку загрузки"""
        download_dir = self.config.get('download_dir', '')
        if os.path.exists(download_dir):
            os.startfile(download_dir)
        else:
            messagebox.showerror(self.i18n.get('error'), 
                               f"Папка не найдена: {download_dir}")
    
    def on_language_change(self, event=None):
        """Обработка смены языка"""
        new_lang = self.language_var.get()
        self.config.set('language', new_lang)
        self.i18n.set_language(new_lang)
        set_language(new_lang)
        
        # Обновить интерфейс
        self.update_ui_language()
        
        # Обновить текущую страницу
        if self.current_page:
            self.current_page.update_language()
    
    def update_ui_language(self):
        """Обновить язык интерфейса"""
        self.root.title(tr('title.main'))
        self.back_btn.config(text=tr('nav.back'))
        # Обновить другие элементы панели инструментов
        # (остальные элементы обновляются в create_toolbar)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


def main():
    """Главная функция"""
    try:
        app = VideoDownloaderApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить приложение: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
