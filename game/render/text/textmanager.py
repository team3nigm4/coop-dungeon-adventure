# Static lass to manage loads, manages and unloads fonts

import json

from game.render.text import font


class TextManager:

    fonts = {}

    @staticmethod
    def init():
        fontInfo = json.load(open("game/resources/textures/fonts/fonts.json"))["fonts"]
        for i in fontInfo:
            TextManager.fonts[i] = font.Font(fontInfo[i])

    @staticmethod
    def bind(font):
        TextManager.fonts[font].bind()

    @staticmethod
    def constructVbo(font, text, size, centering="center"):
        return TextManager.fonts[font].constructVbo(text, size, centering)
