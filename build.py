#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для сборки исполняемого файла
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_executable():
    """Собрать исполняемый файл с PyInstaller"""
    
    print("Начинаем сборку VideoDownloader.exe...")
    
    # Проверяем наличие PyInstaller
    try:
        import PyInstaller
        print(f"PyInstaller версия: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller не установлен. Устанавливаем...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    # Команда сборки
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconsole',
        '--name', 'VideoDownloader',
        '--distpath', 'dist',
        '--workpath', 'build',
        '--specpath', '.',
        'app.py'
    ]
    
    print("Выполняем сборку...")
    print(f"Команда: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Сборка завершена успешно!")
        
        # Проверяем результат
        exe_path = Path('dist/VideoDownloader.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"Исполняемый файл создан: {exe_path}")
            print(f"Размер файла: {size_mb:.1f} MB")
        else:
            print("ОШИБКА: Исполняемый файл не найден!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Ошибка сборки: {e}")
        print(f"Вывод: {e.stdout}")
        print(f"Ошибки: {e.stderr}")
        return False
    
    # Очистка временных файлов
    print("Очищаем временные файлы...")
    for path in ['build', 'VideoDownloader.spec']:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    
    print("Готово! Исполняемый файл находится в папке dist/")
    return True


def main():
    """Главная функция"""
    print("=== Сборка Video Downloader ===")
    
    # Проверяем наличие основного файла
    if not os.path.exists('app.py'):
        print("ОШИБКА: Файл app.py не найден!")
        print("Убедитесь, что вы находитесь в корневой папке проекта.")
        return False
    
    # Проверяем зависимости
    print("Проверяем зависимости...")
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        for req in requirements:
            if req.strip():
                print(f"Проверяем: {req}")
                subprocess.run([sys.executable, '-m', 'pip', 'install', req], 
                             check=True, capture_output=True)
        
        print("Все зависимости установлены.")
        
    except Exception as e:
        print(f"Ошибка при установке зависимостей: {e}")
        return False
    
    # Собираем исполняемый файл
    success = build_executable()
    
    if success:
        print("\n=== Сборка завершена успешно! ===")
        print("Исполняемый файл: dist/VideoDownloader.exe")
        print("\nДля запуска:")
        print("1. Убедитесь, что FFmpeg установлен и добавлен в PATH")
        print("2. Запустите dist/VideoDownloader.exe")
    else:
        print("\n=== Ошибка сборки ===")
        print("Проверьте сообщения об ошибках выше.")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
