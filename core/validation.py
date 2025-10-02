#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль валидации URL
"""

import re
from urllib.parse import urlparse


class Validation:
    # Допустимые хосты для YouTube
    YOUTUBE_HOSTS = [
        'youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be'
    ]
    
    # Допустимые хосты для TikTok
    TIKTOK_HOSTS = [
        'tiktok.com', 'www.tiktok.com', 'm.tiktok.com', 'vt.tiktok.com'
    ]
    
    @staticmethod
    def is_http_url(url):
        """Проверить, является ли строка HTTP/HTTPS URL"""
        if not url or not isinstance(url, str):
            return False
        
        # Проверка схемы
        if not re.match(r'^https?://', url):
            return False
        
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc)
        except:
            return False
    
    @staticmethod
    def is_youtube_url(url):
        """Проверить, является ли URL ссылкой на YouTube"""
        if not Validation.is_http_url(url):
            return False
        
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname.lower()
            
            # Убрать www. если есть
            if hostname.startswith('www.'):
                hostname = hostname[4:]
            
            return hostname in Validation.YOUTUBE_HOSTS
        except:
            return False
    
    @staticmethod
    def is_tiktok_url(url):
        """Проверить, является ли URL ссылкой на TikTok"""
        if not Validation.is_http_url(url):
            return False
        
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname.lower()
            
            # Убрать www. если есть
            if hostname.startswith('www.'):
                hostname = hostname[4:]
            
            return hostname in Validation.TIKTOK_HOSTS
        except:
            return False
    
    @staticmethod
    def validate_url_for_service(url, service):
        """Валидация URL для конкретного сервиса"""
        if not url or not url.strip():
            return False, 'empty'
        
        url = url.strip()
        
        if not Validation.is_http_url(url):
            return False, 'invalid_format'
        
        if service == 'youtube':
            if not Validation.is_youtube_url(url):
                return False, 'invalid_domain'
        elif service == 'tiktok':
            if not Validation.is_tiktok_url(url):
                return False, 'invalid_domain'
        else:
            return False, 'unknown_service'
        
        return True, 'valid'
