#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль работы с cookies
"""

import os
import tempfile
from pathlib import Path
from tkinter import filedialog, messagebox

try:
    import browser_cookie3
    BROWSER_COOKIE3_AVAILABLE = True
except ImportError:
    BROWSER_COOKIE3_AVAILABLE = False


class CookieManager:
    def __init__(self, i18n):
        self.i18n = i18n
        self.cookies_file = None
    
    def create_cookies_from_browser(self, browser='chrome', profile='Default'):
        """Создать cookies.txt из браузера"""
        if not BROWSER_COOKIE3_AVAILABLE:
            messagebox.showerror(
                self.i18n.get('error'),
                "browser-cookie3 не установлен. Установите: pip install browser-cookie3"
            )
            return None
        
        try:
            # Получить cookies из браузера
            if browser == 'chrome':
                cj = browser_cookie3.chrome(domain_name='youtube.com')
            elif browser == 'edge':
                cj = browser_cookie3.edge(domain_name='youtube.com')
            elif browser == 'chromium':
                cj = browser_cookie3.chromium(domain_name='youtube.com')
            else:
                raise ValueError(f"Неподдерживаемый браузер: {browser}")
            
            # Запросить путь для сохранения
            cookies_path = filedialog.asksaveasfilename(
                title=self.i18n.get('create_cookies'),
                defaultextension='.txt',
                filetypes=[('Text files', '*.txt'), ('All files', '*.*')],
                initialname='cookies.txt'
            )
            
            if not cookies_path:
                return None
            
            # Сохранить cookies в Netscape формате
            with open(cookies_path, 'w', encoding='utf-8') as f:
                f.write("# Netscape HTTP Cookie File\n")
                f.write("# This is a generated file! Do not edit.\n\n")
                
                for cookie in cj:
                    # Формат Netscape cookies.txt
                    domain = cookie.domain
                    if domain.startswith('.'):
                        domain_flag = 'TRUE'
                        domain = domain[1:]
                    else:
                        domain_flag = 'FALSE'
                    
                    path = cookie.path or '/'
                    secure = 'TRUE' if cookie.secure else 'FALSE'
                    expires = str(int(cookie.expires)) if cookie.expires else '0'
                    name = cookie.name
                    value = cookie.value
                    
                    f.write(f"{domain}\t{domain_flag}\t{path}\t{secure}\t{expires}\t{name}\t{value}\n")
            
            self.cookies_file = cookies_path
            messagebox.showinfo(
                self.i18n.get('success'),
                f"Cookies сохранены в: {cookies_path}"
            )
            
            return cookies_path
            
        except Exception as e:
            messagebox.showerror(
                self.i18n.get('error'),
                f"{self.i18n.get('error_cookies_export')}: {str(e)}"
            )
            return None
    
    def choose_cookies_file(self):
        """Выбрать файл cookies.txt"""
        cookies_path = filedialog.askopenfilename(
            title=self.i18n.get('choose_cookies_file'),
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')]
        )
        
        if cookies_path and os.path.exists(cookies_path):
            self.cookies_file = cookies_path
            return cookies_path
        
        return None
    
    def get_cookies_file(self):
        """Получить путь к файлу cookies"""
        return self.cookies_file
    
    def clear_cookies(self):
        """Очистить cookies"""
        self.cookies_file = None
