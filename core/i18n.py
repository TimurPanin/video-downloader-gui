#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль интернационализации
"""


class I18n:
    def __init__(self, language='ru'):
        self.language = language
        self.strings = {
            'ru': {
                'app_title': 'Video Downloader — YouTube & TikTok',
                'menu_title': 'Выберите сервис для скачивания',
                'youtube': 'YouTube',
                'tiktok': 'TikTok',
                'back': 'Назад',
                'open': 'Открыть',
                'change': 'Изменить',
                'download': 'СКАЧАТЬ',
                'cancel': 'ОТМЕНА',
                'settings': 'Настройки',
                'cookies': 'Куки',
                'create_cookies': 'Создать cookies.txt из браузера',
                'use_browser_cookies': 'Использовать куки из браузера',
                'choose_cookies_file': 'Выбрать cookies.txt',
                'language': 'Язык',
                'download_dir': 'Папка загрузки',
                'outtmpl': 'Шаблон имён (yt-dlp outtmpl)',
                'ratelimit': 'Лимит скорости (КБ/с, 0 = без лимита)',
                'frags': 'Параллельные фрагменты',
                'yt_link': 'Ссылка на YouTube',
                'tt_link': 'Ссылка на TikTok',
                'playlist': 'Скачать плейлист',
                'single_video': 'Скачать одно видео',
                'allow_mix': 'Разрешить MIX/радио (RD...)',
                'first_n': 'Скачать первые N из плейлиста',
                'all_zero': '(0 = все)',
                'quality': 'Качество',
                'best': 'Лучшее',
                'only_audio': 'Только аудио (mp3)',
                'progress': 'Прогресс',
                'eta': 'Осталось',
                'speed': 'Скорость',
                'yt_dlp_version': 'yt-dlp версия',
                'check_version': 'Проверить версию',
                'update_yt_dlp': 'Обновить yt-dlp',
                'logs': 'История / лог',
                'auto_save_logs': 'Автосохранять логи',
                'error_empty_url': 'Вставьте ссылку.',
                'error_invalid_domain': 'Этот экран принимает только ссылки допустимых доменов.',
                'error_download': 'Ошибка загрузки',
                'error_ffmpeg_missing': 'FFmpeg не найден. Добавьте его в PATH.',
                'error_cookies_export': 'Не удалось создать cookies.txt',
                'done': 'Готово',
                'canceled': 'Загрузка отменена',
                'error': 'Ошибка',
                'success': 'Успешно',
                'info': 'Информация',
                'warning': 'Предупреждение',
                'download_mode': 'Режим загрузки',
                'youtube_description': 'Скачивание видео и плейлистов с YouTube',
                'tiktok_description': 'Скачивание видео с TikTok'
            },
            'en': {
                'app_title': 'Video Downloader — YouTube & TikTok',
                'menu_title': 'Choose a service to download',
                'youtube': 'YouTube',
                'tiktok': 'TikTok',
                'back': 'Back',
                'open': 'Open',
                'change': 'Change',
                'download': 'Download',
                'cancel': 'Cancel',
                'settings': 'Settings',
                'cookies': 'Cookies',
                'create_cookies': 'Create cookies.txt from browser',
                'use_browser_cookies': 'Use cookies from browser',
                'choose_cookies_file': 'Pick cookies.txt',
                'language': 'Language',
                'download_dir': 'Download directory',
                'outtmpl': 'Name template (yt-dlp outtmpl)',
                'ratelimit': 'Rate limit (KB/s, 0 = unlimited)',
                'frags': 'Concurrent fragments',
                'yt_link': 'YouTube link',
                'tt_link': 'TikTok link',
                'playlist': 'Download playlist',
                'single_video': 'Download single video',
                'allow_mix': 'Allow MIX/radio (RD...)',
                'first_n': 'Download first N from playlist',
                'all_zero': '(0 = all)',
                'quality': 'Quality',
                'best': 'Best',
                'only_audio': 'Audio only (mp3)',
                'progress': 'Progress',
                'eta': 'ETA',
                'speed': 'Speed',
                'yt_dlp_version': 'yt-dlp version',
                'check_version': 'Check version',
                'update_yt_dlp': 'Update yt-dlp',
                'logs': 'History / log',
                'auto_save_logs': 'Autosave logs',
                'error_empty_url': 'Paste a link.',
                'error_invalid_domain': 'This screen accepts only allowed domains.',
                'error_download': 'Download error',
                'error_ffmpeg_missing': 'FFmpeg not found. Add it to PATH.',
                'error_cookies_export': 'Failed to create cookies.txt',
                'done': 'Done',
                'canceled': 'Download canceled',
                'error': 'Error',
                'success': 'Success',
                'info': 'Information',
                'warning': 'Warning',
                'download_mode': 'Download mode',
                'youtube_description': 'Download videos and playlists from YouTube',
                'tiktok_description': 'Download videos from TikTok'
            }
        }
    
    def get(self, key):
        """Получить строку по ключу"""
        return self.strings.get(self.language, {}).get(key, key)
    
    def set_language(self, language):
        """Установить язык"""
        if language in self.strings:
            self.language = language
