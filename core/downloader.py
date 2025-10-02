#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль загрузчика видео
"""

import os
import threading
import time
import subprocess
import sys
from pathlib import Path

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False


class Downloader:
    def __init__(self, config, i18n):
        self.config = config
        self.i18n = i18n
        self.is_downloading = False
        self.cancel_event = threading.Event()
        self.progress_callback = None
        self.status_callback = None
        
    def check_ffmpeg(self):
        """Проверить наличие FFmpeg"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def get_yt_dlp_version(self):
        """Получить версию yt-dlp"""
        if not YT_DLP_AVAILABLE:
            return "yt-dlp не установлен"
        
        try:
            return yt_dlp.version.__version__
        except:
            return "Неизвестная версия"
    
    def update_yt_dlp(self):
        """Обновить yt-dlp"""
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'],
                         check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def build_options(self, url, service, quality='best', audio_only=False, 
                     playlist=False, first_n=0, allow_mix=False, cookies_file=None):
        """Построить опции для yt-dlp"""
        if not YT_DLP_AVAILABLE:
            raise Exception("yt-dlp не установлен")
        
        # Базовые опции
        options = {
            'noprogress': False,
            'quiet': True,
            'ignoreerrors': True,
            'continuedl': True,
            'retries': 5,
            'fragment_retries': 5,
            'windowsfilenames': True,
            'outtmpl_na_placeholder': 'NA',
            'concurrent_fragment_downloads': self.config.get('concurrent_frags', 3),
        }
        
        # Лимит скорости
        ratelimit = self.config.get('ratelimit_kbps', 0)
        if ratelimit > 0:
            options['ratelimit'] = ratelimit * 1024
        
        # Cookies
        if cookies_file and os.path.exists(cookies_file):
            options['cookiefile'] = cookies_file
        
        # Шаблон имени файла
        outtmpl = self.config.get('outtmpl', '%(title)s.%(ext)s')
        options['outtmpl'] = outtmpl
        
        # Формат видео
        if audio_only:
            options['format'] = 'bestaudio/best'
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            if quality == 'best':
                options['format'] = 'bv*+ba/b'
            elif quality == '1080p':
                options['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]'
            elif quality == '720p':
                options['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]'
            elif quality == '480p':
                options['format'] = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]'
            elif quality == '360p':
                options['format'] = 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]'
            else:
                options['format'] = 'bv*+ba/b'
        
        # Плейлист
        if not playlist:
            options['noplaylist'] = True
        elif first_n > 0:
            options['playlistend'] = first_n
        
        # MIX/радио для YouTube
        if service == 'youtube' and not allow_mix:
            options['extractor_args'] = {
                'youtube': {
                    'skip': ['dash', 'hls']
                }
            }
        
        return options
    
    def progress_hook(self, d):
        """Хук для отслеживания прогресса"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                
                if self.progress_callback:
                    self.progress_callback(percent, speed, eta)
        
        elif d['status'] == 'finished':
            if self.status_callback:
                self.status_callback('finished', d.get('filename', ''))
    
    def download(self, url, service, quality='best', audio_only=False,
                playlist=False, first_n=0, allow_mix=False, cookies_file=None):
        """Загрузить видео"""
        if not YT_DLP_AVAILABLE:
            raise Exception("yt-dlp не установлен")
        
        if self.is_downloading:
            raise Exception("Загрузка уже выполняется")
        
        # Проверить FFmpeg для аудио
        if audio_only and not self.check_ffmpeg():
            raise Exception(self.i18n.get('error_ffmpeg_missing'))
        
        self.is_downloading = True
        self.cancel_event.clear()
        
        try:
            # Построить опции
            options = self.build_options(
                url, service, quality, audio_only, 
                playlist, first_n, allow_mix, cookies_file
            )
            
            # Добавить хук прогресса
            options['progress_hooks'] = [self.progress_hook]
            
            # Установить директорию загрузки
            download_dir = self.config.get('download_dir', '')
            if download_dir:
                os.makedirs(download_dir, exist_ok=True)
                options['outtmpl'] = os.path.join(download_dir, options['outtmpl'])
            
            # Создать экземпляр yt-dlp
            ydl = yt_dlp.YoutubeDL(options)
            
            # Запустить загрузку в отдельном потоке
            def download_thread():
                try:
                    ydl.download([url])
                    if not self.cancel_event.is_set():
                        if self.status_callback:
                            self.status_callback('completed', '')
                except Exception as e:
                    if not self.cancel_event.is_set():
                        if self.status_callback:
                            self.status_callback('error', str(e))
                finally:
                    self.is_downloading = False
            
            thread = threading.Thread(target=download_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.is_downloading = False
            raise e
    
    def cancel_download(self):
        """Отменить загрузку"""
        if self.is_downloading:
            self.cancel_event.set()
            self.is_downloading = False
            if self.status_callback:
                self.status_callback('canceled', '')
    
    def is_downloading_active(self):
        """Проверить, выполняется ли загрузка"""
        return self.is_downloading
