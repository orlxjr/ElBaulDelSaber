"""Controlador de sesión: coordina modelos, pantallas y efectos visuales (juice).

ENCAPSULAMIENTO: el avance, el álbum, los puntos y la racha solo cambian
mediante sus métodos (register_hit / register_miss / next_refran / ...).
"""
import random
import pygame
import os

from config import WIDTH, HEIGHT, FPS, BG_IDLE, GOLD, WHITE, SUCCESS, SECONDARY
from refranes import REFRANES
from screens import WelcomeScreen, GameScreen, ReflectionScreen, AlbumScreen
from ui import FXLayer


class SoundManager:
    """Gestor de sonidos del juego."""
    
    def __init__(self):
        self._sounds = {}
        self._music_loaded = False
        self._load_sounds()
    
    def _load_sounds(self):
        """Carga todos los sonidos desde la carpeta assets/Sonidos."""
        sound_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Sonidos")
        
        # Cargar efectos de sonido
        sound_files = {
            "intro": "intro.mp3",
            "acertado": "acertado.mp3",
            "victory": "victory.mp3"
        }
        
        for name, filename in sound_files.items():
            path = os.path.join(sound_dir, filename)
            if os.path.exists(path):
                self._sounds[name] = pygame.mixer.Sound(path)
            else:
                self._sounds[name] = None
    
    def play_music(self, name, loops=-1):
        """Reproduce música de fondo en bucle."""
        if name in self._sounds and self._sounds[name]:
            self._sounds[name].play(loops=loops)
    
    def play_sound(self, name):
        """Reproduce un efecto de sonido una vez."""
        if name in self._sounds and self._sounds[name]:
            self._sounds[name].play()
    
    def stop_music(self):
        """Detiene la música de fondo."""
        pygame.mixer.stop()


class GameApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Refranes y Recuerdos")
        self._surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self._clock = pygame.time.Clock()
        pygame.key.set_repeat(420, 42)
        self._running = True
        self._position = 0
        self._album = []
        self._score = 0
        self._streak = 0
        self._max_streak = 0
        self._hits = 0
        self._fx = FXLayer()
        self._shake_ttl = 0.0
        self._shake_power = 0.0
        self._shake_off = (0, 0)
        self._sound_manager = SoundManager()
        self._screen = WelcomeScreen(self)

    # ---------- consultas de solo lectura ----------
    @property
    def current(self):
        return REFRANES[self._position]

    @property
    def position(self):
        return self._position

    @property
    def total(self):
        return len(REFRANES)

    @property
    def album(self):
        return tuple(self._album)

    @property
    def score(self):
        return self._score

    @property
    def streak(self):
        return self._streak

    @property
    def hits(self):
        return self._hits

    @property
    def fx(self):
        return self._fx

    # ---------- navegación ----------
    def start_game(self):
        self._sound_manager.stop_music()
        self._screen = GameScreen(self)

    def go_home(self):
        self._sound_manager.play_music("intro", loops=-1)
        self._screen = WelcomeScreen(self)

    def show_reflection(self, message):
        if self.current not in self._album:
            self._album.append(self.current)
        self._sound_manager.play_sound("victory")
        self._screen = ReflectionScreen(self, message)

    def next_refran(self):
        if self._position + 1 >= self.total:
            self.show_album()
        else:
            self._position += 1
            self.start_game()

    def show_album(self):
        self._screen = AlbumScreen(self)

    def stop(self):
        self._running = False

    # ---------- puntuación y racha ----------
    def register_hit(self):
        self._score += 1
        self._streak += 1
        self._hits += 1
        self._max_streak = max(self._max_streak, self._streak)
        self._sound_manager.play_sound("acertado")

    def register_miss(self):
        self._streak = 0

    # ---------- efectos (juice) ----------
    def shake(self, power=4.0, duration=0.24):
        self._shake_power = max(self._shake_power, power)
        self._shake_ttl = max(self._shake_ttl, duration)

    def flash(self, color=GOLD, power=90):
        self._fx.flash(color, power)

    def celebrate(self, x, y, kind="hit"):
        if kind == "hit":
            self._fx.burst(x, y, [SUCCESS, GOLD, WHITE], n=26, speed=260)
            self._fx.confetti(x, y, n=18)
            self._fx.sparkle(x, y - 30, [GOLD, WHITE], n=8)
            self._fx.float_text("¡Muy bien!", x, y - 60, SUCCESS, size=42, life=1.8)
        else:
            self._fx.burst(x, y, [SECONDARY, GOLD], n=12, speed=170)
            self._fx.float_text("Excelente", x, y - 50, SECONDARY, size=34, life=1.4)

    # ---------- bucle principal ----------
    def run(self):
        self._sound_manager.play_music("intro", loops=-1)
        while self._running:
            dt = self._clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    break
                self._screen.handle_event(event)
            if not self._running:
                break

            self._screen.update(dt)
            self._fx.update(dt)
            self._update_shake(dt)

            if self._shake_ttl > 0:
                shot = self._surface.copy()
                self._screen.draw(shot)
                self._surface.fill(BG_IDLE)
                self._surface.blit(shot, self._shake_off)
            else:
                self._screen.draw(self._surface)
            self._fx.draw(self._surface)
            pygame.display.flip()
        pygame.quit()

    def _update_shake(self, dt):
        if self._shake_ttl > 0:
            self._shake_ttl -= dt
            phase = self._shake_ttl / 0.25
            magnitude = int(self._shake_power * max(0.0, min(1.0, phase)))
            self._shake_off = (random.randint(-magnitude, magnitude),
                               random.randint(-magnitude, magnitude))
            if self._shake_ttl <= 0:
                self._shake_power = 0.0
                self._shake_off = (0, 0)
        else:
            self._shake_off = (0, 0)