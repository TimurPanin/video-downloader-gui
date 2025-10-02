#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль конфигурации приложения
"""

import json
import os
from pathlib import Path


class Config:
    def __init__(self):
        self.config_path = Path.home() / '.vd_settings.json'
        self.data = self.load()
    
    def load(self):
        """Загрузка конфигурации из файла"""
        defaults = {
            'download_dir': str(Path.home() / 'Downloads' / 'VD_Logs'),
            'ratelimit_kbps': 0,
            'concurrent_frags': 3,
            'outtmpl': '%(playlist_title,playlist)s/%(playlist_index>03d)s - %(title).95s.%(ext)s',
            'use_cookies_from_browser': True,
            'cookies_browser': 'chrome',
            'cookies_profile': 'Default',
            'cookies_txt': '',
            'last_tab': 'menu',
            'language': 'ru'
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Объединить с дефолтными значениями
                for key, value in defaults.items():
                    if key not in data:
                        data[key] = value
                return data
            except (json.JSONDecodeError, IOError):
                return defaults
        else:
            return defaults
    
    def save(self):
        """Сохранение конфигурации в файл"""
        try:
            # Создать директорию если не существует
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения конфигурации: {e}")
    
    def get(self, key, default=None):
        """Получить значение по ключу"""
        return self.data.get(key, default)
    
    def set(self, key, value):
        """Установить значение по ключу"""
        self.data[key] = value
        self.save()
    
    def update(self, **kwargs):
        """Обновить несколько значений"""
        self.data.update(kwargs)
        self.save()
