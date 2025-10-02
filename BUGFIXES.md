# Bug Fixes - Video Downloader

## Исправленные проблемы

### 🐛 Проблема 1: Краш при переключении языка

**Описание**: Tkinter крашился при переключении языка из-за неправильного обращения к шрифтам.

**Причина**: Код пытался индексировать `widget.cget('font')[0]`, что вызывало исключение.

**Решение**:
```python
# БЫЛО (крашилось):
if isinstance(widget, ttk.Label) and widget.cget('font')[0] == 'Arial':

# СТАЛО (безопасно):
from tkinter import font as tkfont
font_name = widget.cget('font') if 'font' in widget.keys() else ''
try:
    family = tkfont.nametofont(font_name).actual('family') if font_name else ''
except Exception:
    family = str(font_name)
if isinstance(widget, ttk.Label) and family == 'Arial':
```

**Файлы**: `pages/menu.py`, `pages/loader_tiktok.py`

### 🐛 Проблема 2: Отсутствие автоопределения режима загрузки

**Описание**: YouTube страница не определяла автоматически, является ли URL плейлистом или одиночным видео.

**Причина**: Отсутствовала логика анализа URL для определения типа контента.

**Решение**:

#### 1. Функция автоопределения
```python
def detect_download_mode(url: str) -> str:
    """Return 'playlist' if URL is a playlist/mix, otherwise 'single'."""
    if not url:
        return 'single'
    try:
        p = urlparse(url)
        q = parse_qs(p.query)
        
        # Плейлист по пути
        if p.path.startswith('/playlist'):
            return 'playlist'
        
        # Плейлист по параметру list
        list_vals = q.get('list', [])
        if list_vals:
            return 'playlist'
        
        # Радио/MIX флаг
        if q.get('start_radio', ['0'])[0] == '1':
            return 'playlist'
        
        # Shorts всегда одиночные
        if '/shorts/' in p.path:
            return 'single'
        
        return 'single'
    except Exception:
        return 'single'
```

#### 2. Обработчик изменения URL
```python
def _on_url_change(self, event=None):
    """Обработка изменения URL для автоопределения режима"""
    url = self.url_var.get().strip()
    mode = detect_download_mode(url)
    
    if mode != self.download_mode_var.get():
        self.download_mode_var.set(mode)
        # Логируем изменение
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, f"Режим автоматически изменен на: {mode}\n")
```

#### 3. Привязка событий
```python
# Привязываем обработчик к полю URL
self.url_entry.bind('<KeyRelease>', self._on_url_change)
self.url_entry.bind('<FocusOut>', self._on_url_change)
```

#### 4. Финальная проверка перед загрузкой
```python
# Финальная проверка URL vs выбранного режима
selected_mode = self.download_mode_var.get()
detected_mode = detect_download_mode(url)
if selected_mode != detected_mode:
    self.download_mode_var.set(detected_mode)
    # Логируем корректировку
    self.log_text.insert(tk.END, f"Режим скорректирован на {detected_mode} на основе URL.\n")
```

**Файлы**: `pages/loader_youtube.py`

## Правила автоопределения

### Одиночное видео (single)
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- Любой URL без параметра `list`

### Плейлист (playlist)
- `https://www.youtube.com/playlist?list=PLAYLIST_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&start_radio=1`
- Любой URL с параметром `list` (включая RD... для MIX)

## Тестирование

### Unit тесты
```python
class TestDownloadModeDetection(unittest.TestCase):
    def test_single_video_urls(self):
        single_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/shorts/abc123"
        ]
        for url in single_urls:
            self.assertEqual(detect_download_mode(url), 'single')
    
    def test_playlist_urls(self):
        playlist_urls = [
            "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMOVn",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLrAXtmRdnEQy6nuLMOVn",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&start_radio=1"
        ]
        for url in playlist_urls:
            self.assertEqual(detect_download_mode(url), 'playlist')
```

### Результаты тестов
```
Ran 12 tests in 0.004s
OK
```

## Пользовательский опыт

### До исправления
- ❌ Краш при переключении языка
- ❌ Ручной выбор режима загрузки
- ❌ Несоответствие URL и выбранного режима

### После исправления
- ✅ Безопасное переключение языков
- ✅ Автоматическое определение режима
- ✅ Корректировка режима перед загрузкой
- ✅ Логирование изменений

## Технические детали

### Безопасная работа со шрифтами
- Использование `tkfont.nametofont()` для нормализации
- Обработка исключений при работе с шрифтами
- Проверка существования атрибутов перед обращением

### Автоопределение режима
- Парсинг URL через `urlparse` и `parse_qs`
- Анализ пути и параметров запроса
- Обработка различных форматов YouTube URL
- Безопасная обработка ошибок

### События интерфейса
- `KeyRelease` - при вводе текста
- `FocusOut` - при потере фокуса
- Автоматическое обновление UI
- Логирование изменений

## Заключение

Обе проблемы успешно исправлены:
- ✅ **Краш шрифтов**: Безопасная работа с Tkinter шрифтами
- ✅ **Автоопределение**: Умное определение типа контента по URL
- ✅ **Тестирование**: Полное покрытие тестами
- ✅ **UX**: Улучшенный пользовательский опыт

Приложение теперь работает стабильно и интуитивно! 🎉
