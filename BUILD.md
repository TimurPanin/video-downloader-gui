# Инструкции по сборке Video Downloader

## Требования

- Python 3.10+
- Windows 10/11 x64
- FFmpeg (для аудио-выгрузки MP3)

## Быстрая сборка

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Автоматическая сборка

```bash
python build.py
```

Исполняемый файл будет создан в папке `dist/VideoDownloader.exe`

### 3. Ручная сборка

```bash
# Установка PyInstaller
pip install pyinstaller

# Сборка
pyinstaller --onefile --noconsole --name VideoDownloader app.py
```

## Детальная сборка

### Шаг 1: Подготовка окружения

```bash
# Создание виртуального окружения (рекомендуется)
python -m venv venv
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

### Шаг 2: Тестирование

```bash
# Запуск тестов
python test_app.py

# Запуск приложения для проверки
python run.py
```

### Шаг 3: Сборка

```bash
# Автоматическая сборка
python build.py

# Или ручная сборка
pyinstaller --onefile --noconsole --name VideoDownloader app.py
```

### Шаг 4: Проверка результата

После сборки проверьте:
- Файл `dist/VideoDownloader.exe` создан
- Размер файла ~50-100 MB
- Файл запускается без ошибок

## Опции сборки

### Базовые опции

```bash
pyinstaller --onefile --noconsole --name VideoDownloader app.py
```

### Расширенные опции

```bash
pyinstaller \
  --onefile \
  --noconsole \
  --name VideoDownloader \
  --distpath dist \
  --workpath build \
  --specpath . \
  --add-data "core;core" \
  --add-data "pages;pages" \
  --hidden-import yt_dlp \
  --hidden-import browser_cookie3 \
  app.py
```

### Оптимизация размера

```bash
pyinstaller \
  --onefile \
  --noconsole \
  --name VideoDownloader \
  --exclude-module matplotlib \
  --exclude-module numpy \
  --exclude-module pandas \
  app.py
```

## Устранение проблем сборки

### Ошибка: ModuleNotFoundError

**Проблема**: Не найден модуль при запуске .exe

**Решение**:
```bash
# Добавить скрытые импорты
pyinstaller --hidden-import yt_dlp --hidden-import browser_cookie3 app.py
```

### Ошибка: FFmpeg not found

**Проблема**: FFmpeg не найден в .exe

**Решение**:
1. Установите FFmpeg в PATH
2. Или добавьте FFmpeg в папку с .exe

### Большой размер файла

**Проблема**: .exe файл слишком большой

**Решение**:
```bash
# Исключить ненужные модули
pyinstaller --exclude-module matplotlib --exclude-module numpy app.py
```

### Медленная сборка

**Проблема**: Сборка занимает много времени

**Решение**:
```bash
# Использовать кэш
pyinstaller --clean --noconfirm app.py
```

## Проверка сборки

### Тест 1: Запуск

```bash
# Запуск .exe файла
dist\VideoDownloader.exe
```

### Тест 2: Функциональность

1. Откройте приложение
2. Проверьте главное меню
3. Переключите язык
4. Проверьте настройки
5. Попробуйте загрузить тестовое видео

### Тест 3: Зависимости

```bash
# Проверка зависимостей в .exe
python -c "import sys; print(sys.path)"
```

## Распространение

### Подготовка к распространению

1. **Создайте папку для распространения**:
   ```
   VideoDownloader_Release/
   ├── VideoDownloader.exe
   ├── README.md
   └── USAGE.md
   ```

2. **Добавьте FFmpeg** (если не в PATH):
   ```
   VideoDownloader_Release/
   ├── VideoDownloader.exe
   ├── ffmpeg.exe
   ├── ffprobe.exe
   └── README.md
   ```

3. **Создайте установщик** (опционально):
   - Используйте NSIS, Inno Setup или другие инструменты
   - Добавьте ярлык на рабочий стол
   - Добавьте в меню "Пуск"

### Системные требования для пользователей

- Windows 10/11 x64
- FFmpeg в PATH (для аудио)
- Интернет-соединение
- ~100 MB свободного места

## Автоматизация сборки

### Скрипт для CI/CD

```bash
#!/bin/bash
# build_script.sh

echo "Начинаем сборку Video Downloader..."

# Установка зависимостей
pip install -r requirements.txt

# Запуск тестов
python test_app.py

# Сборка
python build.py

# Проверка результата
if [ -f "dist/VideoDownloader.exe" ]; then
    echo "Сборка успешна!"
    echo "Файл: dist/VideoDownloader.exe"
    echo "Размер: $(du -h dist/VideoDownloader.exe | cut -f1)"
else
    echo "Ошибка сборки!"
    exit 1
fi
```

### GitHub Actions

```yaml
name: Build Video Downloader

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Run tests
      run: python test_app.py
    
    - name: Build executable
      run: python build.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: VideoDownloader
        path: dist/VideoDownloader.exe
```

## Заключение

После успешной сборки у вас будет:

- ✅ Исполняемый файл `VideoDownloader.exe`
- ✅ Все зависимости включены
- ✅ Поддержка YouTube и TikTok
- ✅ Интерфейс на русском и английском языках
- ✅ Автоматическое создание cookies
- ✅ Прогресс-бар и логирование

Файл готов к распространению и использованию на любом Windows-компьютере!
