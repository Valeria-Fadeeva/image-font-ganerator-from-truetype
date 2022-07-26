#!/usr/bin/env python3


"""
Программа генерирует png-шрифт из ttf-, otf-шрифтов.

Позволяет использовать тени и размытие теней.
"""

import font_generator


if __name__ == "__main__":
    font_generator.font_generate(use_shadow=False)
    font_generator.font_generate(use_shadow=1)
    font_generator.font_generate(use_shadow=2)
    font_generator.font_generate(use_shadow=3)
    font_generator.font_generate(use_shadow=4)
