#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Запуск приложения Video Downloader
"""

import sys
import os
from pathlib import Path

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import main
    main()
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что все зависимости установлены:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Ошибка запуска: {e}")
    sys.exit(1)
