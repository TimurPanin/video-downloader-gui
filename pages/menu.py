#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главное меню приложения
"""

import tkinter as tk
from tkinter import ttk
from I18N import tr


class MenuPage:
    def __init__(self, app):
        self.app = app
        self.frame = None
    
    def show(self):
        """Показать страницу"""
        if self.frame:
            self.frame.pack(fill=tk.BOTH, expand=True)
            return
        
        self.frame = ttk.Frame(self.app.content_frame)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        self.title_label = ttk.Label(self.frame, text=tr('menu.choose_service'),
                               font=('Arial', 16, 'bold'))
        self.title_label.pack(pady=(20, 40))
        
        # Контейнер для карточек
        cards_frame = ttk.Frame(self.frame)
        cards_frame.pack(expand=True)
        
        # Карточка YouTube
        self.youtube_frame = ttk.LabelFrame(cards_frame, text=tr('menu.youtube.card_title'),
                                     padding=20)
        self.youtube_frame.pack(side=tk.LEFT, padx=(0, 20), fill=tk.BOTH, expand=True)
        
        self.youtube_desc = ttk.Label(self.youtube_frame, 
                               text=tr('menu.youtube.card_desc'),
                               font=('Arial', 10))
        self.youtube_desc.pack(pady=(0, 20))
        
        self.youtube_btn = ttk.Button(self.youtube_frame, text="YouTube",
                               command=lambda: self.app.show_page('youtube'),
                               style='Accent.TButton')
        self.youtube_btn.pack()
        
        # Карточка TikTok
        self.tiktok_frame = ttk.LabelFrame(cards_frame, text=tr('menu.tiktok.card_title'),
                                     padding=20)
        self.tiktok_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.tiktok_desc = ttk.Label(self.tiktok_frame,
                              text=tr('menu.tiktok.card_desc'),
                              font=('Arial', 10))
        self.tiktok_desc.pack(pady=(0, 20))
        
        self.tiktok_btn = ttk.Button(self.tiktok_frame, text="TikTok",
                              command=lambda: self.app.show_page('tiktok'),
                              style='Accent.TButton')
        self.tiktok_btn.pack()
        
        # Панель настроек
        settings_frame = ttk.LabelFrame(self.frame, text=self.app.i18n.get('settings'), padding=10)
        settings_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Кнопки настроек
        settings_buttons_frame = ttk.Frame(settings_frame)
        settings_buttons_frame.pack(fill=tk.X)
        
        # Cookies
        cookies_btn = ttk.Button(settings_buttons_frame, text=self.app.i18n.get('create_cookies'),
                               command=self.create_cookies)
        cookies_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Версия yt-dlp
        version_btn = ttk.Button(settings_buttons_frame, text=self.app.i18n.get('check_version'),
                               command=self.check_version)
        version_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Обновление yt-dlp
        update_btn = ttk.Button(settings_buttons_frame, text=self.app.i18n.get('update_yt_dlp'),
                              command=self.update_yt_dlp)
        update_btn.pack(side=tk.LEFT)
    
    def hide(self):
        """Скрыть страницу"""
        if self.frame:
            self.frame.pack_forget()
    
    def create_cookies(self):
        """Создать cookies из браузера"""
        self.app.cookie_manager.create_cookies_from_browser()
    
    def check_version(self):
        """Проверить версию yt-dlp"""
        from core.downloader import Downloader
        downloader = Downloader(self.app.config, self.app.i18n)
        version = downloader.get_yt_dlp_version()
        
        from tkinter import messagebox
        messagebox.showinfo(self.app.i18n.get('yt_dlp_version'), version)
    
    def update_yt_dlp(self):
        """Обновить yt-dlp"""
        from core.downloader import Downloader
        downloader = Downloader(self.app.config, self.app.i18n)
        
        from tkinter import messagebox
        if downloader.update_yt_dlp():
            messagebox.showinfo(self.app.i18n.get('success'), 
                              "yt-dlp успешно обновлен")
        else:
            messagebox.showerror(self.app.i18n.get('error'), 
                               "Не удалось обновить yt-dlp")
    
    def update_language(self):
        """Обновить язык"""
        if self.frame:
            # Обновить заголовок
            self.title_label.config(text=tr('menu.choose_service'))
            self.youtube_frame.config(text=tr('menu.youtube.card_title'))
            self.youtube_desc.config(text=tr('menu.youtube.card_desc'))
            self.youtube_btn.config(text="YouTube")  # Статический текст
            self.tiktok_frame.config(text=tr('menu.tiktok.card_title'))
            self.tiktok_desc.config(text=tr('menu.tiktok.card_desc'))
            self.tiktok_btn.config(text="TikTok")  # Статический текст
