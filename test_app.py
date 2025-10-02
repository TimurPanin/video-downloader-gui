#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тесты для Video Downloader
"""

import unittest
import sys
import os
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.validation import Validation
from core.config import Config
from core.i18n import I18n

# Импорт функций автоопределения режима
try:
    from pages.loader_youtube import detect_download_mode, is_rd_playlist
except ImportError:
    # Если импорт не удался, создаем заглушки
    def detect_download_mode(url):
        return 'single'
    def is_rd_playlist(url):
        return False


class TestValidation(unittest.TestCase):
    """Тесты валидации URL"""
    
    def test_youtube_urls(self):
        """Тест валидации YouTube URL"""
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ"
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(Validation.is_youtube_url(url))
                is_valid, error = Validation.validate_url_for_service(url, 'youtube')
                self.assertTrue(is_valid)
    
    def test_tiktok_urls(self):
        """Тест валидации TikTok URL"""
        valid_urls = [
            "https://www.tiktok.com/@user/video/1234567890",
            "https://tiktok.com/@user/video/1234567890",
            "https://m.tiktok.com/@user/video/1234567890",
            "https://vt.tiktok.com/ZSd8K9m2/"
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(Validation.is_tiktok_url(url))
                is_valid, error = Validation.validate_url_for_service(url, 'tiktok')
                self.assertTrue(is_valid)
    
    def test_invalid_urls(self):
        """Тест невалидных URL"""
        invalid_urls = [
            "",
            "not_a_url",
            "ftp://example.com"
        ]
        
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(Validation.is_http_url(url))
    
    def test_wrong_domain_urls(self):
        """Тест URL с неправильными доменами"""
        wrong_domain_urls = [
            "https://example.com",
            "https://vimeo.com/123456"
        ]
        
        for url in wrong_domain_urls:
            with self.subTest(url=url):
                # URL валидный по схеме, но неправильный домен
                self.assertTrue(Validation.is_http_url(url))
                # Но не должен проходить валидацию для YouTube/TikTok
                is_valid_youtube, _ = Validation.validate_url_for_service(url, 'youtube')
                is_valid_tiktok, _ = Validation.validate_url_for_service(url, 'tiktok')
                self.assertFalse(is_valid_youtube)
                self.assertFalse(is_valid_tiktok)


class TestConfig(unittest.TestCase):
    """Тесты конфигурации"""
    
    def setUp(self):
        """Настройка тестов"""
        self.config = Config()
    
    def test_default_values(self):
        """Тест значений по умолчанию"""
        # Проверяем, что можем получить значение по умолчанию
        self.assertIsNotNone(self.config.get('language'))
        self.assertIsInstance(self.config.get('ratelimit_kbps', 0), int)
    
    def test_set_get(self):
        """Тест установки и получения значений"""
        test_value = "test_value"
        self.config.set('test_key', test_value)
        self.assertEqual(self.config.get('test_key'), test_value)


class TestDownloadModeDetection(unittest.TestCase):
    """Тесты автоопределения режима загрузки"""
    
    def test_single_video_urls(self):
        """Тест URL одиночных видео"""
        single_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/shorts/abc123",
            "https://youtube.com/watch?v=dQw4w9WgXcQ"
        ]
        
        for url in single_urls:
            with self.subTest(url=url):
                self.assertEqual(detect_download_mode(url), 'single')
    
    def test_playlist_urls(self):
        """Тест URL плейлистов"""
        playlist_urls = [
            "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMOVn",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLrAXtmRdnEQy6nuLMOVn",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&start_radio=1"
        ]
        
        for url in playlist_urls:
            with self.subTest(url=url):
                self.assertEqual(detect_download_mode(url), 'playlist')
    
    def test_invalid_urls(self):
        """Тест невалидных URL"""
        invalid_urls = ["", "not_a_url", "https://example.com"]
        
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertEqual(detect_download_mode(url), 'single')
    
    def test_rd_playlist_detection(self):
        """Тест определения RD-плейлистов"""
        rd_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=abc123&list=RDMIX123",
            "https://youtube.com/watch?v=test&list=RDPLAYLIST"
        ]
        
        for url in rd_urls:
            with self.subTest(url=url):
                self.assertTrue(is_rd_playlist(url))
    
    def test_non_rd_playlist_detection(self):
        """Тест обычных плейлистов (не RD)"""
        non_rd_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=abc123&list=PL123456789",
            "https://www.youtube.com/playlist?list=PL123456789"
        ]
        
        for url in non_rd_urls:
            with self.subTest(url=url):
                self.assertFalse(is_rd_playlist(url))


class TestI18n(unittest.TestCase):
    """Тесты интернационализации"""
    
    def setUp(self):
        """Настройка тестов"""
        self.i18n_ru = I18n('ru')
        self.i18n_en = I18n('en')
    
    def test_russian_strings(self):
        """Тест русских строк"""
        self.assertEqual(self.i18n_ru.get('app_title'), 'Video Downloader — YouTube & TikTok')
        self.assertEqual(self.i18n_ru.get('youtube'), 'YouTube')
        self.assertEqual(self.i18n_ru.get('download_mode'), 'Режим загрузки')
        self.assertEqual(self.i18n_ru.get('youtube_description'), 'Скачивание видео и плейлистов с YouTube')
        self.assertEqual(self.i18n_ru.get('tiktok_description'), 'Скачивание видео с TikTok')
    
    def test_english_strings(self):
        """Тест английских строк"""
        self.assertEqual(self.i18n_en.get('app_title'), 'Video Downloader — YouTube & TikTok')
        self.assertEqual(self.i18n_en.get('youtube'), 'YouTube')
        self.assertEqual(self.i18n_en.get('download_mode'), 'Download mode')
        self.assertEqual(self.i18n_en.get('youtube_description'), 'Download videos and playlists from YouTube')
        self.assertEqual(self.i18n_en.get('tiktok_description'), 'Download videos from TikTok')
    
    def test_language_switch(self):
        """Тест переключения языка"""
        self.i18n_ru.set_language('en')
        self.assertEqual(self.i18n_ru.language, 'en')


def run_tests():
    """Запуск тестов"""
    print("Запуск тестов Video Downloader...")
    
    # Создаем тестовый набор
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем тесты
    suite.addTests(loader.loadTestsFromTestCase(TestValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestDownloadModeDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestI18n))
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Возвращаем результат
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
