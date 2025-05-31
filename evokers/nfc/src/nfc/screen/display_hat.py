import threading
import time
from queue import Queue, Empty
import os
import pygame
from events import Event, InfoEvent
from .screen import Screen
from ..strings import MESSAGES

DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
FONT_SIZE = 24

class DisplayHatScreen(Screen):
    def __init__(self):
        self._event_queue = Queue()
        self._running = True
        self._header = MESSAGES["header_title"]
        self._footer = MESSAGES["footer_title"]
        self._body = "⌛"  # hourglass emoji initially, waiting for events

        # Set environment variable to use the framebuffer
        os.putenv('SDL_FBDEV', '/dev/fb0')

        # Initialize Pygame
        pygame.init()
        pygame.mouse.set_visible(False)
        self._screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Display HAT Mini")

        # Load fonts
        pygame.font.init()
        self._font = pygame.font.SysFont(None, FONT_SIZE)

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while self._running:
            try:
                # Try to get event, update body with checkmark on success
                _ = self._event_queue.get(timeout=0.1)
                self._body = "✅"
            except Empty:
                # No event, show hourglass
                self._body = "⌛"

            self._render_display()
            time.sleep(0.5)

    def _render_display(self):
        # Clear the screen
        self._screen.fill((0, 0, 0))  # Black background

        # Render header
        header_surface = self._font.render(self._header, True, (0, 255, 255))  # Cyan
        header_rect = header_surface.get_rect(center=(DISPLAY_WIDTH // 2, FONT_SIZE))
        self._screen.blit(header_surface, header_rect)

        # Render body (emoji)
        body_surface = self._font.render(self._body, True, (255, 255, 255))  # White
        body_rect = body_surface.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
        self._screen.blit(body_surface, body_rect)

        # Render footer
        footer_surface = self._font.render(self._footer, True, (0, 255, 0))  # Green
        footer_rect = footer_surface.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - FONT_SIZE))
        self._screen.blit(footer_surface, footer_rect)

        # Update the display
        pygame.display.update()

    def update(self, event: Event):
        if isinstance(event, InfoEvent):
            self._event_queue.put(event.payload)

    def stop(self):
        self._running = False
        self._thread.join()
        pygame.quit()
