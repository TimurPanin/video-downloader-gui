#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль интернационализации с полной схемой переводов
"""

I18N = {
    "en": {
        "title.main": "Video Downloader — YouTube & TikTok",
        "title.youtube": "YouTube",
        "nav.back": "Back",
        "menu.choose_service": "Choose a service to download",
        "menu.youtube.card_title": "YouTube",
        "menu.youtube.card_desc": "Download videos and playlists from YouTube",
        "menu.youtube.btn": "YouTube",
        "menu.tiktok.card_title": "TikTok",
        "menu.tiktok.card_desc": "Download videos from TikTok",
        "menu.tiktok.btn": "TikTok",
        "common.download_dir": "Download directory:",
        "common.change": "Change",
        "common.open": "Open",
        "yt.link.label": "YouTube link",
        "yt.progress": "Progress",
        "yt.history": "History / log",
        "yt.settings": "Settings",
        "yt.mode": "Download mode:",
        "yt.mode.single": "Download single video",
        "yt.mode.playlist": "Download playlist",
        "yt.quality": "Quality",
        "yt.quality.best": "Best",
        "yt.audio_only": "Audio only (mp3)",
        "yt.download": "Download",
        "yt.cancel": "Cancel",
        "err.url.title": "Error",
        "err.url.body": "This input accepts links only from allowed domains:\n{domains}\nPlease paste a valid URL.",
        "info.mode.adjusted": "Mode adjusted to {m} based on URL.",
        "warning.rd_playlist.title": "MIX/Radio Playlist Detected",
        "warning.rd_playlist.body": "This playlist is a MIX/radio playlist. To download it, enable the 'Allow MIX/radio (RD...)' option."
    },
    "ru": {
        "title.main": "Video Downloader — YouTube & TikTok",
        "title.youtube": "YouTube",
        "nav.back": "Назад",
        "menu.choose_service": "Выберите сервис для скачивания",
        "menu.youtube.card_title": "YouTube",
        "menu.youtube.card_desc": "Скачивание видео и плейлистов с YouTube",
        "menu.tiktok.card_title": "TikTok",
        "menu.tiktok.card_desc": "Скачивание видео с TikTok",
        "menu.tiktok.btn": "TikTok",
        "common.download_dir": "Папка загрузки:",
        "common.change": "Изменить",
        "common.open": "Открыть",
        "yt.link.label": "Ссылка на YouTube",
        "yt.progress": "Прогресс",
        "yt.history": "История / лог",
        "yt.settings": "Настройки",
        "yt.mode": "Режим загрузки:",
        "yt.mode.single": "Скачать одно видео",
        "yt.mode.playlist": "Скачать плейлист",
        "yt.quality": "Качество",
        "yt.quality.best": "Лучшее",
        "yt.audio_only": "Только аудио (mp3)",
        "yt.download": "Скачать",
        "yt.cancel": "Отмена",
        "err.url.title": "Ошибка",
        "err.url.body": "Это поле ввода принимает ссылки только с разрешённых доменов:\n{domains}\nПожалуйста, вставьте корректный URL.",
        "info.mode.adjusted": "Режим изменён на {m} по ссылке.",
        "warning.rd_playlist.title": "Обнаружен MIX/радио плейлист",
        "warning.rd_playlist.body": "Этот плейлист является MIX/радио. Чтобы загрузить, включите опцию 'Разрешить MIX/радио (RD...)'."
    }
}

CURRENT_LANG = 'ru'

def tr(key: str, **kwargs):
    """Получить переведенную строку"""
    txt = I18N.get(CURRENT_LANG, {}).get(key, key)
    return txt.format(**kwargs) if kwargs else txt

def set_language(lang: str):
    """Установить язык"""
    global CURRENT_LANG
    CURRENT_LANG = lang if lang in ('ru', 'en') else 'ru'
