#!/usr/bin/env python3


"""
Программа генерирует png-шрифт из ttf-, otf-шрифтов.

Позволяет использовать тени и размытие теней.
"""

import sys
sys.path.insert(0, "../")
import font_generator


if __name__ == "__main__":
    font_generator.font_generate(filename='test.txt', use_shadow=1)
