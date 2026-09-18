"""Punto de entrada del juego. Ejecutar con: python main.py"""
import sys
import pygame
from app import GameApp


if __name__ == "__main__":
    try:
        GameApp().run()
    finally:
        pygame.quit()
        sys.exit()
