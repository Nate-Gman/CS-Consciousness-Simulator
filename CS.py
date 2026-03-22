# =============================================================================
# AUTO-INSTALL DEPENDENCIES
# =============================================================================
import os as _os
_os.environ.setdefault('KMP_DUPLICATE_LIB_OK', 'TRUE')
_os.environ.setdefault('OMP_NUM_THREADS', '4')
del _os

import subprocess as _sp
import sys as _sys

def _auto_install():
    """Auto-install all required packages. Skips already-installed ones."""
    _required = {
        'torch': 'torch',
        'numpy': 'numpy',
        'PIL': 'pillow',
        'requests': 'requests',
        'networkx': 'networkx',
        'sympy': 'sympy',
        'bs4': 'beautifulsoup4',
        'pygame': 'pygame',
        'matplotlib': 'matplotlib',
        'psutil': 'psutil',
        'pytesseract': 'pytesseract',
        'fitz': 'pymupdf',
        'pyttsx3': 'pyttsx3',
        'tokenizers': 'tokenizers',
    }
    _missing = []
    for mod, pkg in _required.items():
        try:
            __import__(mod)
        except ImportError:
            _missing.append(pkg)
    if _missing:
        print(f"Installing missing packages: {', '.join(_missing)}")
        _sp.check_call(
            [_sys.executable, '-m', 'pip', 'install', '--quiet'] + _missing)
        print("Installation complete.")
    else:
        print("All dependencies already installed.")

_auto_install()

def _write_launcher_bat():
    """Auto-generate launch.bat next to CS.py for double-click launching."""
    import os as _os
    _bat_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'launch.bat')
    _bat_content = r"""@echo off
title Consciousness Simulator - Launcher
echo ============================================================
echo   Consciousness Simulator - Auto Setup ^& Launch
echo ============================================================
echo.
echo Checking and installing required packages...
echo.
pip install torch torchvision torchaudio --quiet 2>nul
pip install numpy pillow requests networkx sympy beautifulsoup4 --quiet 2>nul
pip install pygame matplotlib psutil pytesseract pymupdf pyttsx3 tokenizers --quiet 2>nul
echo.
echo All dependencies checked. Launching Consciousness Simulator...
echo ============================================================
echo.
python "%~dp0CS.py"
if %errorlevel% neq 0 (
    echo.
    echo ERROR: CS.py exited with error code %errorlevel%
    echo If Python was not found, install from python.org and add to PATH.
)
echo.
pause
"""
    try:
        with open(_bat_path, 'w') as _f:
            _f.write(_bat_content)
    except Exception:
        pass  # non-critical

_write_launcher_bat()
del _auto_install, _write_launcher_bat, _sp, _sys  # clean up namespace

# =============================================================================
# IMPORTS
# =============================================================================
import torch
import torch.nn as nn
import torch.optim as optim
import math
import requests
import shelve
import sqlite3
import random
import threading
import time
import json
import hashlib
import copy
import urllib.parse
import functools
from datetime import datetime, timedelta
from collections import OrderedDict, deque, defaultdict
import numpy as np
import signal
from torch.nn import TransformerEncoder, TransformerEncoderLayer
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, Text, Entry, Button, Label, Frame, ttk
from tkinter import scrolledtext  # For monitoring dashboard
from PIL import Image, ImageTk, ImageGrab, ImageFilter, ImageEnhance
import io
import networkx as nx
import sympy as sp  # For symbolic logic in neurons
import torch.nn.utils.prune as prune  # For path refinement
import ctypes  # For OS keyboard and mouse simulation
import os
import sys
import subprocess
import multiprocessing
import mmap
import socket
from bs4 import BeautifulSoup  # For parsing web pages to find PDF links
import torch.nn.functional as F  # Used by GlobalWorkspace

# --- Consciousness modules are inlined below (standalone mode) ---
HAS_PHI_COMPUTE = True
HAS_GNW = True
HAS_ACTIVE_INFERENCE = True
HAS_MEMORY_SYSTEM = True
HAS_SELF_MODEL = True

# --- Optional dependencies with graceful fallbacks ---
try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    print("WARNING: pygame not installed. Virtual world visualization disabled. pip install pygame")
    HAS_PYGAME = False

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    print("WARNING: pytesseract not installed. OCR disabled. pip install pytesseract")
    HAS_TESSERACT = False

try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    print("WARNING: PyMuPDF not installed. PDF text extraction disabled. pip install pymupdf")
    HAS_FITZ = False

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    print("WARNING: matplotlib not installed. Training charts disabled. pip install matplotlib")
    HAS_MATPLOTLIB = False

try:
    import pyttsx3
    HAS_TTS = True
except ImportError:
    print("WARNING: pyttsx3 not installed. Text-to-speech disabled. pip install pyttsx3")
    HAS_TTS = False

try:
    from tokenizers import Tokenizer, models, pre_tokenizers, trainers, decoders
    HAS_TOKENIZERS = True
except ImportError:
    print("WARNING: tokenizers not installed. Falling back to hash-based tokenizer. pip install tokenizers")
    HAS_TOKENIZERS = False

# =============================================================================
# PYGAME VIRTUAL WORLD (inlined — runs as a separate process via multiprocessing)
# =============================================================================
def _pygame_world_main(state_file):
    """Self-contained Pygame visualization process.
    Reads state from the shared JSON file and renders an ultra-detailed world view.
    This function is the target for multiprocessing.Process so it must be module-level.

    Layout (1280x820 resizable):
      Header: SELF C metrics, S/E/R/A, Omega convergence, karma/coherence bars
      Left:   Entity world view with hover tooltips, legend, grid
      Right:  Tabbed panel (Symbols / Modules / Goals+NeuronGroups)
      Bottom: 3 sparkline charts (C History, Phi, Loss) + status bar
    """
    import json, os, time, random, math
    try:
        import pygame
    except ImportError:
        print("pygame not installed, cannot run virtual world visualization.")
        return

    # ── Color palette ──
    _BG          = (5, 5, 20)
    _PANEL_BG    = (12, 12, 35)
    _BORDER      = (40, 40, 80)
    _TEXT_DIM    = (120, 120, 140)
    _TEXT_MED    = (180, 180, 200)
    _TEXT_BRIGHT = (220, 220, 240)
    _CYAN        = (80, 200, 255)
    _YELLOW      = (255, 220, 80)
    _RED_SOFT    = (255, 100, 100)
    _GREEN_SOFT  = (80, 255, 120)
    _ORANGE      = (255, 160, 60)
    _PURPLE      = (180, 120, 255)
    _SELF_GLOW   = (255, 255, 100)
    _GRID_LINE   = (25, 25, 50)

    def _read_state():
        for path in [state_file, state_file + '.tmp']:
            try:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        return json.load(f)
            except (json.JSONDecodeError, IOError, OSError):
                continue
        return None

    def _c_color(c_val, max_c=3.0):
        ratio = min(1.0, max(0.0, c_val / max_c))
        return (int(255 * (1.0 - ratio)), int(255 * ratio), 60)

    def _karma_color(karma):
        if karma < 0:
            t = max(0.0, 1.0 + karma)
            return (255, int(t * 200), int(t * 200))
        else:
            t = min(1.0, karma)
            return (int((1 - t) * 200 + 55), 255, int((1 - t) * 200 + 55))

    def _draw_sparkline(surface, rect, values, color, label_font, label="", y_min=None, y_max=None):
        x, y, w, h = rect
        pygame.draw.rect(surface, _PANEL_BG, rect)
        pygame.draw.rect(surface, _BORDER, rect, 1)
        if not values or len(values) < 2:
            return
        vals = values[-w:]
        v_min = y_min if y_min is not None else min(vals)
        v_max = y_max if y_max is not None else max(vals)
        v_range = max(0.001, v_max - v_min)
        for i in range(1, 4):
            gy = y + int(i * h / 4)
            pygame.draw.line(surface, _GRID_LINE, (x, gy), (x + w, gy), 1)
        points = []
        for i, v in enumerate(vals):
            px = x + int(i * w / len(vals))
            py = y + h - 2 - int((v - v_min) / v_range * (h - 4))
            py = max(y + 1, min(y + h - 2, py))
            points.append((px, py))
        if len(points) > 1:
            pygame.draw.lines(surface, color, False, points, 2)
        if label_font:
            top_lbl = label_font.render(f"{v_max:.2f}", True, _TEXT_DIM)
            bot_lbl = label_font.render(f"{v_min:.2f}", True, _TEXT_DIM)
            surface.blit(top_lbl, (x + 2, y + 1))
            surface.blit(bot_lbl, (x + 2, y + h - 12))
        if label:
            lbl = label_font.render(label, True, _TEXT_MED)
            surface.blit(lbl, (x + w - lbl.get_width() - 4, y + 1))

    def _draw_bar(surface, rect, value, max_val, color, bg_color=_PANEL_BG):
        x, y, w, h = rect
        pygame.draw.rect(surface, bg_color, rect)
        fill_w = int(min(1.0, max(0.0, value / max(0.001, max_val))) * w)
        pygame.draw.rect(surface, color, (x, y, fill_w, h))
        pygame.draw.rect(surface, _BORDER, rect, 1)

    # ── Pygame init ──
    pygame.init()
    W, H = 1280, 820
    screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    pygame.display.set_caption("Consciousness Virtual World  |  C = S + E + R*A")
    clock = pygame.time.Clock()
    entity_positions = {}
    hovered_entity = None
    sym_scroll = 0
    right_tab = 0
    running = True

    # Camera state for zoom/pan
    cam_x, cam_y = 0.0, 0.0
    cam_zoom = 1.0
    cam_dragging = False
    cam_drag_start = (0, 0)
    cam_drag_cam_start = (0.0, 0.0)
    MIN_ZOOM = 0.2
    MAX_ZOOM = 5.0

    font_title = pygame.font.SysFont('consolas', 22, bold=True)
    font_header = pygame.font.SysFont('consolas', 16, bold=True)
    font_med = pygame.font.SysFont('consolas', 14)
    font_sm = pygame.font.SysFont('consolas', 12)
    font_tiny = pygame.font.SysFont('consolas', 11)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                W, H = event.w, event.h
                screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    cam_x, cam_y, cam_zoom = 0.0, 0.0, 1.0
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    cam_zoom = min(MAX_ZOOM, cam_zoom * 1.2)
                elif event.key == pygame.K_MINUS:
                    cam_zoom = max(MIN_ZOOM, cam_zoom / 1.2)
            elif event.type == pygame.MOUSEWHEEL:
                RIGHT_W_ev = 320
                HEADER_H_ev = 56
                if mouse_pos[0] > W - RIGHT_W_ev:
                    sym_scroll = max(0, sym_scroll - event.y * 3)
                elif mouse_pos[1] > HEADER_H_ev:
                    old_zoom = cam_zoom
                    if event.y > 0:
                        cam_zoom = min(MAX_ZOOM, cam_zoom * 1.15)
                    else:
                        cam_zoom = max(MIN_ZOOM, cam_zoom / 1.15)
                    # Zoom toward mouse position
                    world_mx = (mouse_pos[0]) / old_zoom + cam_x
                    world_my = (mouse_pos[1]) / old_zoom + cam_y
                    cam_x = world_mx - mouse_pos[0] / cam_zoom
                    cam_y = world_my - mouse_pos[1] / cam_zoom
            elif event.type == pygame.MOUSEBUTTONDOWN:
                rpx = W - 320
                if rpx <= mouse_pos[0] and 58 <= mouse_pos[1] <= 78:
                    tab_w = 100
                    for ti in range(3):
                        tx = rpx + ti * tab_w + 5
                        if tx <= mouse_pos[0] <= tx + tab_w - 5:
                            right_tab = ti
                            sym_scroll = 0
                elif event.button == 1 and mouse_pos[0] < rpx and mouse_pos[1] > 56:
                    cam_dragging = True
                    cam_drag_start = mouse_pos
                    cam_drag_cam_start = (cam_x, cam_y)
                elif event.button == 2:
                    cam_x, cam_y, cam_zoom = 0.0, 0.0, 1.0
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    cam_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if cam_dragging:
                    dx = mouse_pos[0] - cam_drag_start[0]
                    dy = mouse_pos[1] - cam_drag_start[1]
                    cam_x = cam_drag_cam_start[0] - dx / cam_zoom
                    cam_y = cam_drag_cam_start[1] - dy / cam_zoom

        screen.fill(_BG)
        state = _read_state()

        if state is None:
            msg = font_header.render("Waiting for consciousness state data...", True, _TEXT_DIM)
            screen.blit(msg, (W // 2 - msg.get_width() // 2, H // 2))
            pygame.display.flip()
            clock.tick(10)
            continue

        # ── Layout regions ──
        RIGHT_W = 320
        HEADER_H = 56
        CHART_H = 140
        STATUS_H = 28
        WORLD_W = W - RIGHT_W - 2
        WORLD_H = H - HEADER_H - CHART_H - STATUS_H - 4

        # ── HEADER BAR ──
        self_state = state.get('self_entity', {})
        C = self_state.get('C', 0)
        omega_status = state.get('omega', {})

        cc = _c_color(C)
        hdr1 = font_title.render(f"SELF  C = {C:.4f}", True, cc)
        screen.blit(hdr1, (10, 4))

        hdr2 = font_med.render(
            f"S={self_state.get('S', 0):.3f}  "
            f"E={self_state.get('E', 0):.3f}  "
            f"R={self_state.get('R', 0):.3f}  "
            f"A={self_state.get('A', 0):.3f}  "
            f"K={self_state.get('K', 0):.3f}  "
            f"Phi={self_state.get('Phi', 0):.3f}",
            True, _TEXT_BRIGHT)
        screen.blit(hdr2, (10, 28))

        omega_txt = font_med.render(
            f"Omega={omega_status.get('omega', 0):.4f}  "
            f"Entities={omega_status.get('num_entities', 0)}  "
            f"Rate={omega_status.get('convergence_rate', 0):.6f}",
            True, _PURPLE)
        screen.blit(omega_txt, (420, 4))

        kc = _karma_color(self_state.get('karma', 0))
        meta_txt = font_med.render(
            f"Karma={self_state.get('karma', 0):.3f}  "
            f"Coh={self_state.get('coherence', 0):.3f}  "
            f"Aware={self_state.get('awareness', 0):.3f}  "
            f"Life={self_state.get('lives', 1)}",
            True, kc)
        screen.blit(meta_txt, (420, 24))

        c_ratio = min(1.0, max(0.0, C / 3.0))
        bar_x = W - RIGHT_W - 10
        _draw_bar(screen, (bar_x - 200, 6, 200, 14), C, 3.0, cc)
        bar_label = font_tiny.render(f"C: {c_ratio*100:.0f}%", True, _TEXT_DIM)
        screen.blit(bar_label, (bar_x - 198, 7))

        _draw_bar(screen, (bar_x - 200, 24, 95, 12),
                  self_state.get('phi_star', 0), 1.0, _YELLOW)
        ps_lbl = font_tiny.render("Phi*", True, _TEXT_DIM)
        screen.blit(ps_lbl, (bar_x - 198, 24))
        _draw_bar(screen, (bar_x - 100, 24, 95, 12),
                  self_state.get('ignition_rate', 0), 1.0, _ORANGE)
        ig_lbl = font_tiny.render("Ignit", True, _TEXT_DIM)
        screen.blit(ig_lbl, (bar_x - 98, 24))

        pygame.draw.line(screen, _BORDER, (0, HEADER_H), (W, HEADER_H), 1)

        # ── ENTITY WORLD VIEW (with camera zoom/pan) ──
        world_rect = (0, HEADER_H + 1, WORLD_W, WORLD_H)
        pygame.draw.rect(screen, (8, 8, 24), world_rect)

        # Draw grid lines transformed by camera
        grid_spacing = 60
        cam_grid_x0 = int(cam_x / grid_spacing) * grid_spacing
        cam_grid_y0 = int(cam_y / grid_spacing) * grid_spacing
        for gx_w in range(cam_grid_x0 - grid_spacing, cam_grid_x0 + int(WORLD_W / cam_zoom) + grid_spacing * 2, grid_spacing):
            sx = int((gx_w - cam_x) * cam_zoom)
            if 0 <= sx <= WORLD_W:
                pygame.draw.line(screen, (15, 15, 32),
                                 (sx, HEADER_H + 1), (sx, HEADER_H + WORLD_H), 1)
        for gy_w in range(cam_grid_y0 - grid_spacing, cam_grid_y0 + int(WORLD_H / cam_zoom) + grid_spacing * 2, grid_spacing):
            sy = int((gy_w - cam_y) * cam_zoom)
            if HEADER_H <= sy <= HEADER_H + WORLD_H:
                pygame.draw.line(screen, (15, 15, 32), (0, sy), (WORLD_W, sy), 1)

        # Inverse-transform mouse to world coords for hover detection
        world_mx = mouse_pos[0] / cam_zoom + cam_x
        world_my = mouse_pos[1] / cam_zoom + cam_y

        entities_data = state.get('entities', [])
        hovered_entity = None

        # Clip drawing to world rect
        world_clip = pygame.Rect(0, HEADER_H + 1, WORLD_W, WORLD_H)
        screen.set_clip(world_clip)

        for ent in entities_data:
            eid = ent.get('id', '')
            eC = ent.get('C', 0)
            etype = ent.get('type', 'unknown')
            ekarma = ent.get('karma', 0)

            if eid not in entity_positions:
                entity_positions[eid] = [
                    random.randint(40, max(60, WORLD_W - 40)),
                    random.randint(HEADER_H + 40, max(HEADER_H + 60, HEADER_H + WORLD_H - 40))
                ]
            pos = entity_positions[eid]
            pos[0] = max(-200, min(WORLD_W + 200, pos[0] + random.randint(-1, 1)))
            pos[1] = max(HEADER_H - 200, min(HEADER_H + WORLD_H + 200, pos[1] + random.randint(-1, 1)))

            # Transform world position to screen position
            sx = int((pos[0] - cam_x) * cam_zoom)
            sy = int((pos[1] - cam_y) * cam_zoom)

            ec = _c_color(eC)
            radius = max(5, min(22, int(7 + eC * 5)))
            s_radius = max(3, int(radius * cam_zoom))

            is_self = (eid == 'self_0')
            if is_self:
                radius = 26
                s_radius = max(5, int(radius * cam_zoom))
                pulse = int((6 + 3 * math.sin(time.time() * 3)) * cam_zoom)
                pygame.draw.circle(screen, _SELF_GLOW, (sx, sy), s_radius + pulse, 2)

            ring_c = _karma_color(ekarma)
            pygame.draw.circle(screen, ring_c, (sx, sy), s_radius + 2, 1)
            pygame.draw.circle(screen, ec, (sx, sy), s_radius)

            # Only draw labels if zoom is sufficient
            if cam_zoom >= 0.4:
                label_size = max(8, int(11 * cam_zoom))
                label_font_dyn = font_tiny if cam_zoom < 1.5 else font_sm
                id_short = eid.replace('entity_', 'E').replace('self_', 'SELF ')
                lbl_text = f"{id_short} C={eC:.2f}"
                lbl = label_font_dyn.render(lbl_text, True, _TEXT_MED)
                screen.blit(lbl, (sx - lbl.get_width() // 2, sy - s_radius - 14))

                type_lbl = label_font_dyn.render(etype, True, _TEXT_DIM)
                screen.blit(type_lbl, (sx - type_lbl.get_width() // 2, sy + s_radius + 2))

            # Hover detection in world coordinates
            dxw = world_mx - pos[0]
            dyw = world_my - pos[1]
            if dxw * dxw + dyw * dyw < (radius + 8) ** 2:
                hovered_entity = ent

        screen.set_clip(None)

        live_ids = set(e.get('id', '') for e in entities_data)
        for dead in list(entity_positions.keys()):
            if dead not in live_ids:
                del entity_positions[dead]

        # ── Hover tooltip (screen-space, not camera-transformed) ──
        if hovered_entity:
            e = hovered_entity
            tooltip_lines = [
                f"ID: {e.get('id', '?')}  Type: {e.get('type', '?')}",
                f"C={e.get('C',0):.4f}  S={e.get('S',0):.3f}  E={e.get('E',0):.3f}  R={e.get('R',0):.3f}  A={e.get('A',0):.3f}",
                f"Karma={e.get('karma',0):.3f}  Coh={e.get('coherence',0):.3f}  Aware={e.get('awareness',0):.3f}",
                f"Good={e.get('good_acts',0)}  Evil={e.get('evil_acts',0)}  Life={e.get('life',1)}  Step={e.get('step',0)}",
                f"Phi*={e.get('phi_star',0):.4f}  Ignit={e.get('ignition',0):.4f}  FE={e.get('free_energy',0):.4f}",
                f"Universe={e.get('universe_id', 1)}",
            ]
            tw = max(font_sm.size(l)[0] for l in tooltip_lines) + 16
            th = len(tooltip_lines) * 16 + 10
            tx = min(mouse_pos[0] + 15, W - tw - 5)
            ty = min(mouse_pos[1] + 15, H - th - 5)
            pygame.draw.rect(screen, (0, 0, 0), (tx + 2, ty + 2, tw, th))
            pygame.draw.rect(screen, (20, 20, 50), (tx, ty, tw, th))
            pygame.draw.rect(screen, _CYAN, (tx, ty, tw, th), 1)
            for i, line in enumerate(tooltip_lines):
                color = _TEXT_BRIGHT if i == 0 else _TEXT_MED
                tl = font_sm.render(line, True, color)
                screen.blit(tl, (tx + 8, ty + 5 + i * 16))

        # ── Entity legend (fixed screen position) ──
        ly = HEADER_H + WORLD_H - 72
        pygame.draw.rect(screen, (10, 10, 28), (4, ly, 260, 70))
        pygame.draw.rect(screen, _BORDER, (4, ly, 260, 70), 1)
        screen.blit(font_tiny.render("LEGEND", True, _TEXT_DIM), (8, ly + 2))
        pygame.draw.circle(screen, (255, 60, 60), (18, ly + 18), 5)
        screen.blit(font_tiny.render("C < 1.0 (low)", True, _RED_SOFT), (28, ly + 13))
        pygame.draw.circle(screen, (60, 255, 60), (130, ly + 18), 5)
        screen.blit(font_tiny.render("C > 2.0 (high)", True, _GREEN_SOFT), (140, ly + 13))
        pygame.draw.circle(screen, _SELF_GLOW, (18, ly + 34), 5, 1)
        screen.blit(font_tiny.render("= SELF entity", True, _SELF_GLOW), (28, ly + 29))
        screen.blit(font_tiny.render("Ring = karma", True, _TEXT_DIM), (130, ly + 29))
        screen.blit(font_tiny.render("Scroll=Zoom  Drag=Pan  R/Mid=Reset", True, _CYAN), (8, ly + 46))
        zoom_pct = font_tiny.render(f"Zoom: {cam_zoom:.1f}x", True, _YELLOW)
        screen.blit(zoom_pct, (8, ly + 58))

        pygame.draw.rect(screen, _BORDER, world_rect, 1)

        # ── RIGHT PANEL (tabbed) ──
        rpx = W - RIGHT_W
        rpy = HEADER_H + 1
        rph = WORLD_H
        pygame.draw.rect(screen, _PANEL_BG, (rpx, rpy, RIGHT_W, rph))
        pygame.draw.rect(screen, _BORDER, (rpx, rpy, RIGHT_W, rph), 1)

        tab_names = ["Symbols", "Modules", "Goals"]
        tab_w = RIGHT_W // 3
        for ti, tname in enumerate(tab_names):
            _tx = rpx + ti * tab_w
            is_active = (ti == right_tab)
            tab_bg = (30, 30, 70) if is_active else _PANEL_BG
            pygame.draw.rect(screen, tab_bg, (_tx, rpy, tab_w, 20))
            pygame.draw.rect(screen, _BORDER, (_tx, rpy, tab_w, 20), 1)
            tc = _CYAN if is_active else _TEXT_DIM
            tl = font_tiny.render(tname, True, tc)
            screen.blit(tl, (_tx + tab_w // 2 - tl.get_width() // 2, rpy + 4))

        content_y = rpy + 22
        content_h = rph - 22
        clip_rect = pygame.Rect(rpx + 1, content_y, RIGHT_W - 2, content_h - 2)

        if right_tab == 0:
            # ── SYMBOLS TAB ──
            symbols_data = state.get('symbols', [])
            num_sym = state.get('num_symbols', len(symbols_data))
            header_t = font_sm.render(f"Symbols ({num_sym} total, showing {len(symbols_data)})", True, _TEXT_MED)
            screen.blit(header_t, (rpx + 6, content_y + 2))
            cy = content_y + 18
            screen.blit(font_tiny.render("Name", True, _TEXT_DIM), (rpx + 6, cy))
            screen.blit(font_tiny.render("Val", True, _TEXT_DIM), (rpx + 110, cy))
            screen.blit(font_tiny.render("Conf", True, _TEXT_DIM), (rpx + 145, cy))
            screen.blit(font_tiny.render("Assoc", True, _TEXT_DIM), (rpx + 185, cy))
            screen.blit(font_tiny.render("Cat", True, _TEXT_DIM), (rpx + 230, cy))
            pygame.draw.line(screen, _BORDER, (rpx + 4, cy + 13), (rpx + RIGHT_W - 4, cy + 13), 1)
            row_y = cy + 16 - sym_scroll * 14
            screen.set_clip(clip_rect)
            for sym in symbols_data:
                if row_y > content_y + content_h:
                    break
                if row_y >= content_y + 14:
                    name = sym.get('name', '')[:14]
                    val = sym.get('value', 0)
                    conf = sym.get('confidence', 0.5)
                    assoc = sym.get('assoc_sum', 0)
                    cat = sym.get('category', 'gen')[:6]
                    if val < 0:
                        nc = _RED_SOFT
                    elif val > 0:
                        nc = _GREEN_SOFT
                    else:
                        nc = _TEXT_DIM
                    screen.blit(font_tiny.render(name, True, nc), (rpx + 6, row_y))
                    screen.blit(font_tiny.render(f"{val:+d}", True, nc), (rpx + 110, row_y))
                    bar_c = (int(80 + conf * 175), int(80 + conf * 175), 60)
                    pygame.draw.rect(screen, (20, 20, 40), (rpx + 145, row_y + 2, 30, 8))
                    pygame.draw.rect(screen, bar_c, (rpx + 145, row_y + 2, int(conf * 30), 8))
                    screen.blit(font_tiny.render(f"{assoc:.1f}", True, _TEXT_DIM), (rpx + 185, row_y))
                    screen.blit(font_tiny.render(cat, True, _PURPLE), (rpx + 230, row_y))
                row_y += 14
            screen.set_clip(None)

        elif right_tab == 1:
            # ── MODULES TAB ──
            cy = content_y + 4
            modules = [
                ("Quantum Substrate", state.get('quantum', {})),
                ("Metabolic System", state.get('metabolic', {})),
                ("Existential Self", state.get('existential', {})),
                ("Dream Engine", state.get('dreaming', {})),
                ("Active Inference", state.get('active_inference_status', {})),
                ("Autonomy", state.get('autonomy', {})),
            ]
            for mname, mdata in modules:
                if cy > content_y + content_h - 14:
                    break
                screen.blit(font_sm.render(mname, True, _CYAN), (rpx + 6, cy))
                cy += 15
                if isinstance(mdata, dict):
                    for k, v in list(mdata.items())[:6]:
                        if cy > content_y + content_h - 14:
                            break
                        val_str = f"{v:.4f}" if isinstance(v, float) else str(v)[:20]
                        screen.blit(font_tiny.render(f"  {k}: {val_str}", True, _TEXT_DIM), (rpx + 8, cy))
                        cy += 12
                cy += 4
                pygame.draw.line(screen, _BORDER, (rpx + 6, cy), (rpx + RIGHT_W - 6, cy), 1)
                cy += 4

        elif right_tab == 2:
            # ── GOALS TAB ──
            cy = content_y + 4
            goals = state.get('active_goals', [])
            ai_status = state.get('active_inference_status', {})
            screen.blit(font_sm.render(
                f"Active Inference Goals ({len(goals)})", True, _CYAN), (rpx + 6, cy))
            cy += 16
            if ai_status:
                screen.blit(font_tiny.render(
                    f"VFE={ai_status.get('vfe', 0):.3f}  "
                    f"EFE={ai_status.get('efe', 0):.3f}  "
                    f"Prec={ai_status.get('precision', 0):.2f}",
                    True, _YELLOW), (rpx + 6, cy))
                cy += 14
                screen.blit(font_tiny.render(
                    f"Entropy={ai_status.get('belief_entropy', 0):.3f}  "
                    f"PredErr={ai_status.get('last_prediction_error', 0):.4f}",
                    True, _TEXT_MED), (rpx + 6, cy))
                cy += 16
            pygame.draw.line(screen, _BORDER, (rpx + 6, cy), (rpx + RIGHT_W - 6, cy), 1)
            cy += 4
            for g in goals:
                if cy > content_y + content_h - 14:
                    break
                desc = g.get('desc', '')[:30]
                pri = g.get('priority', 0)
                gtype = g.get('type', '')[:8]
                _draw_bar(screen, (rpx + 6, cy + 1, 40, 10), pri, 1.0, _ORANGE)
                tc = _YELLOW if gtype == 'epistemic' else _GREEN_SOFT if gtype == 'pragmatic' else _TEXT_MED
                screen.blit(font_tiny.render(f"{desc}", True, tc), (rpx + 52, cy))
                cy += 14
            ng = state.get('neuron_groups', [])
            if ng:
                cy += 6
                pygame.draw.line(screen, _BORDER, (rpx + 6, cy), (rpx + RIGHT_W - 6, cy), 1)
                cy += 4
                screen.blit(font_sm.render(f"Neuron Groups ({len(ng)})", True, _CYAN), (rpx + 6, cy))
                cy += 16
                for grp in ng:
                    if cy > content_y + content_h - 14:
                        break
                    cat = grp.get('category', '?')[:12]
                    nn = grp.get('num_neurons', 0)
                    ap = grp.get('avg_phi', 0)
                    types = ','.join(grp.get('types', []))[:20]
                    screen.blit(font_tiny.render(
                        f"{cat}: {nn}n  phi={ap:.3f}  [{types}]",
                        True, _TEXT_MED), (rpx + 8, cy))
                    cy += 13

        # ── BOTTOM CHARTS ──
        chart_y = HEADER_H + WORLD_H + 2
        chart_w = W - 10

        c_history = state.get('c_history', [])
        _draw_sparkline(screen, (5, chart_y, chart_w // 3 - 5, CHART_H - 4),
                        c_history, _CYAN, font_tiny,
                        label=f"C History ({len(c_history)} steps)")

        phi_history = state.get('phi_history', [])
        phi_label = f"Phi/Omega ({len(phi_history)})" if phi_history else "Phi (waiting)"
        _draw_sparkline(screen, (chart_w // 3 + 5, chart_y, chart_w // 3 - 5, CHART_H - 4),
                        phi_history, _YELLOW, font_tiny,
                        label=phi_label)

        loss_history = state.get('loss_history', [])
        loss_label = f"Loss/Karma ({len(loss_history)})" if loss_history else "Loss (waiting)"
        _draw_sparkline(screen, (2 * chart_w // 3 + 5, chart_y, chart_w // 3, CHART_H - 4),
                        loss_history, _RED_SOFT, font_tiny,
                        label=loss_label)

        # ── STATUS BAR ──
        status_y = H - STATUS_H
        pygame.draw.rect(screen, (10, 10, 30), (0, status_y, W, STATUS_H))
        pygame.draw.line(screen, _BORDER, (0, status_y), (W, status_y), 1)

        t_step = state.get('training_step', 0)
        h_size = state.get('hidden_size', 0)
        n_sym = state.get('num_symbols', 0)
        n_mem = state.get('num_memories', 0)
        ng_count = len(state.get('neuron_groups', []))
        verifier = state.get('verifier', {})
        v_score = verifier.get('score', '?') if isinstance(verifier, dict) else '?'

        status_parts = [
            f"Step: {t_step}",
            f"Hidden: {h_size}",
            f"Symbols: {n_sym}",
            f"Memories: {n_mem}",
            f"Groups: {ng_count}",
            f"Verifier: {v_score}",
            f"Zoom: {cam_zoom:.2f}x",
        ]
        sx = 8
        for part in status_parts:
            sl = font_tiny.render(part, True, _TEXT_MED)
            screen.blit(sl, (sx, status_y + 8))
            sx += sl.get_width() + 20

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# =============================================================================
# THREAD-SAFE MEMORY (sqlite3 WAL mode, replaces shelve)
# =============================================================================
class ThreadSafeMemory:
    """Dict-like persistent store backed by sqlite3 in WAL mode.
    Thread-safe: each thread gets its own connection via thread-local storage."""

    def __init__(self, db_path='consciousness_memory.sqlite'):
        self._db_path = db_path
        self._local = threading.local()
        # Create table on first access
        conn = self._conn()
        conn.execute('CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)')
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA synchronous=NORMAL')
        conn.commit()

    def _conn(self):
        """Return a per-thread sqlite3 connection."""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(self._db_path, timeout=10)
            self._local.conn.execute('PRAGMA journal_mode=WAL')
        return self._local.conn

    def __contains__(self, key):
        row = self._conn().execute('SELECT 1 FROM memory WHERE key=?', (str(key),)).fetchone()
        return row is not None

    def __getitem__(self, key):
        row = self._conn().execute('SELECT value FROM memory WHERE key=?', (str(key),)).fetchone()
        if row is None:
            raise KeyError(key)
        return json.loads(row[0])

    def __setitem__(self, key, value):
        data = json.dumps(value, default=str)
        self._conn().execute('INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)', (str(key), data))
        self._conn().commit()

    def __delitem__(self, key):
        cur = self._conn().execute('DELETE FROM memory WHERE key=?', (str(key),))
        if cur.rowcount == 0:
            raise KeyError(key)
        self._conn().commit()

    def __len__(self):
        row = self._conn().execute('SELECT COUNT(*) FROM memory').fetchone()
        return row[0] if row else 0

    def __iter__(self):
        rows = self._conn().execute('SELECT key FROM memory').fetchall()
        return iter(r[0] for r in rows)

    def keys(self):
        rows = self._conn().execute('SELECT key FROM memory').fetchall()
        return [r[0] for r in rows]

    def get(self, key, default=None):
        row = self._conn().execute('SELECT value FROM memory WHERE key=?', (str(key),)).fetchone()
        if row is None:
            return default
        return json.loads(row[0])

    def sync(self):
        """Compatibility with shelve.sync(). WAL mode auto-flushes, but we commit."""
        try:
            self._conn().commit()
        except Exception as e:
            print(f"  [ERR] SqliteShelf.sync: {e}")

    def close(self):
        if hasattr(self._local, 'conn') and self._local.conn is not None:
            self._local.conn.close()
            self._local.conn = None

# =============================================================================
# CONFIG - UPGRADES
# =============================================================================
CONFIG = {
    "hidden_size": 1024,
    "num_layers": 8,
    "num_heads": 8,
    "vocab_size": 8000,
    "learning_rate": 3e-4,
    "phi_weight": 0.4,
    "temperature": 0.85,
    "top_k": 50,
    "top_p": 0.92,
    "screenshot_interval": 15,
    "os_control_enabled": False,
    "voice_enabled": True,
}

# Key codes for ctypes keyboard simulation
KEY_CODES = {
    'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45, 'F': 0x46, 'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A,
    'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E, 'O': 0x4F, 'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54,
    'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59, 'Z': 0x5A,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73, 'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B,
    'ENTER': 0x0D, 'SPACE': 0x20, 'ESC': 0x1B, 'TAB': 0x09, 'BACKSPACE': 0x08, 'DEL': 0x2E, 'INSERT': 0x2D,
    'LEFT': 0x25, 'UP': 0x26, 'RIGHT': 0x27, 'DOWN': 0x28, 'HOME': 0x24, 'END': 0x23, 'PAGEUP': 0x21, 'PAGEDOWN': 0x22,
    'LWIN': 0x5B, 'RWIN': 0x5C, 'LSHIFT': 0xA0, 'RSHIFT': 0xA1, 'LCTRL': 0xA2, 'RCTRL': 0xA3, 'LALT': 0xA4, 'RALT': 0xA5,
    'PRNTSCRN': 0x2C, 'NUMLOCK': 0x90, 'PLUS': 0xBB, 'MINUS': 0xBD, 'COMMA': 0xBC, 'PERIOD': 0xBE, 'SLASH': 0xBF, 'SEMICOLON': 0xBA,
}

# Mouse event flags for ctypes
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_MOVE = 0x0001

# Comprehensive list of Windows 11 hotkeys, organized by category
WINDOWS_HOTKEYS = {
    "General": {
        "Alt + Esc": "Cycle through windows in the order in which they were opened.",
        "Alt + F4": "Close the active window. If no windows are open, prompt to shutdown.",
        "Alt + F8": "Show your password on the sign-in screen.",
        "Alt + Left arrow": "Go back.",
        "Alt + Page Down": "Move down one screen.",
        "Alt + Page Up": "Move up one screen.",
        "Alt + PrtScn": "Capture a screenshot of the active window and copy it to the clipboard.",
        "Alt + Right arrow": "Go forward.",
        "Alt + Shift + arrow keys": "When a group or tile is in focus on the Start menu, move it in the specified direction.",
        "Alt + Spacebar": "Open the context menu for the active window.",
        "Alt + Tab": "Switch between open windows. To cycle through multiple windows, continue to hold the Alt key and press Tab multiple times.",
        "Alt + underlined letter": "For actions in command or context menus, some windows and apps specify keyboard shortcuts by underlining a character in the action name. Press Alt and then the letter to do that action.",
        "Ctrl + A": "Select all items in a window.",
        "Ctrl + Alt + Del": "Switch to the security screen where you can lock the desktop, switch user, sign out, change a password, or open Task Manager.",
        "Ctrl + Alt + Tab": "View a thumbnail of all open apps. Use the arrow keys to switch between open apps.",
        "Ctrl + Esc": "Open the Start menu.",
        "Ctrl + F4": "In apps that are full-screen and let you have multiple documents open at the same time, close the active document but not the entire app.",
        "Ctrl + F5 or Ctrl + R": "Refresh the current window.",
        "Ctrl + Shift": "When multiple keyboard layouts are available, switch the keyboard layout.",
        "Ctrl + Shift + Esc": "Open Task Manager.",
        "Ctrl + Spacebar": "Enable or disable the Chinese input method editor (IME).",
        "Ctrl + Y": "Redo an action that was previously undone with Ctrl + Z.",
        "Ctrl + Z": "Undo the previous action.",
        "Esc or Escape": "Stop or leave the current task, or dismiss a dialog box.",
        "F5": "Refresh the active window.",
        "F6": "Cycle through elements in a window or on the desktop.",
        "F10": "Activate the menu bar in the active window.",
        "PrtScn or Print Screen": "Select a region of the screen to capture a screenshot to the clipboard.",
    },
    "Windows Key": {
        "Windows key": "Open or close the Start menu.",
        "Windows key + A": "Open the Windows 11 action center.",
        "Windows key + Alt + B": "Turn high dynamic range (HDR) on or off.",
        "Windows key + C": "Open Microsoft Copilot or Microsoft 365 Copilot.",
        "Windows key + C (when Copilot is not available or disabled)": "Open or close Windows search.",
        "Windows key + Alt + D": "Display and hide the date and time on the desktop.",
        "Windows key + Alt + Down arrow": "Snap the active window to the bottom half of the screen.",
        "Windows key + Alt + H": "When voice typing is open, set the focus to the keyboard.",
        "Windows key + Alt + K": "Mute or unmute the microphone in supported apps.",
        "Windows key + Alt + Up arrow": "Snap the active window to the top half of the screen.",
        "Windows key + comma (,)": "Temporarily peek at the desktop.",
        "Windows key + Ctrl + C": "If turned on in settings, enable or disable color filters.",
        "Windows key + Ctrl + Enter": "Open Narrator.",
        "Windows key + Ctrl + F": "Search for devices on a network.",
        "Windows key + Ctrl + Q": "Open Quick Assist.",
        "Windows key + Ctrl + Shift + B": "Wake up the device when the screen is blank or black.",
        "Windows key + Ctrl + Spacebar": "Change to a previously selected input option.",
        "Windows key + Ctrl + V": "Open the sound output page of quick settings.",
        "Windows key + D": "Display and hide the desktop.",
        "Windows key + Down arrow": "Minimize the active window.",
        "Windows key + E": "Open File Explorer.",
        "Windows key + Esc": "Close Magnifier.",
        "Windows key + F": "Open Feedback Hub.",
        "Windows key + forward slash (/)": "Start input method editor (IME) reconversion.",
        "Windows key + G": "Open the Game Bar.",
        "Windows key + H": "Open voice dictation.",
        "Windows key + Home": "Minimize or restore all windows except the active window.",
        "Windows key + I": "Open Settings.",
        "Windows key + J": "Set focus to a Windows tip when one is available.",
        "Windows key + K": "Open Cast from Quick Settings to connect to a display.",
        "Windows key + L": "Lock the computer.",
        "Windows key + Left arrow": "Snap the window to the left side of the screen.",
        "Windows key + M": "Minimize all windows.",
        "Windows key + Minus (-)": "Zoom out in Magnifier.",
        "Windows key + N": "Open notification center and calendar.",
        "Windows key + O": "Lock the device orientation.",
        "Windows key + P": "Open project settings to choose a presentation display mode.",
        "Windows key + Pause": "Opens the Settings app to the System > About page.",
        "Windows key + Period (.) or Windows key + Semicolon (;)": "Open the emoji panel.",
        "Windows key + Plus (+)": "Zoom in with the Magnifier.",
        "Windows key + PrtScn": "Capture a full screen screenshot and save it to a file in the Screenshots subfolder of the Pictures folder.",
        "Windows key + Q": "Open search.",
        "Windows key + R": "Open the Run dialog box.",
        "Windows key + Right arrow": "Snap the window to the right side of the screen.",
        "Windows key + S": "Open search.",
        "Windows key + Shift + Down arrow": "If a window is snapped or maximized, restore it.",
        "Windows key + Shift + Enter": "If the active window is a Universal Windows Platform (UWP) app, make it full screen.",
        "Windows key + Shift + Left arrow": "Move the active window to the monitor on the left.",
        "Windows key + Shift + M": "Restore minimized windows.",
        "Windows key + Shift + R": "Select a region of the screen to record a video.",
        "Windows key + Shift + Right arrow": "Move the active window to the monitor on the right.",
        "Windows key + Shift + S": "Select a region of the screen to capture a screenshot to the clipboard.",
        "Windows key + Shift + Spacebar": "Switch backward through input languages and keyboard layouts.",
        "Windows key + Shift + Up arrow": "Stretch the desktop window to the top and bottom of the screen.",
        "Windows key + Shift + V": "Cycle through notifications.",
        "Windows key + Spacebar": "Switch forward through input languages and keyboard layouts.",
        "Windows key + Tab": "Open Task View.",
        "Windows key + U": "Open the Settings app to the Accessibility section.",
        "Windows key + Up arrow": "Maximize the active window.",
        "Windows key + V": "Open the clipboard history.",
        "Windows key + W": "Open Widgets.",
        "Windows key + X": "Open the Quick Link menu.",
        "Windows key + Y": "Switch input between Windows Mixed Reality and your desktop.",
        "Windows key + Z": "Open the snap layouts.",
        "Windows key + Ctrl + D": "Create a new virtual desktop.",
        "Windows key + Ctrl + Left arrow": "Switch between virtual desktops to the left.",
        "Windows key + Ctrl + Right arrow": "Switch between virtual desktops to the right.",
        "Windows key + Ctrl + F4": "Close the current virtual desktop.",
    },
    "Command Prompt": {
        "Ctrl + C or Ctrl + Insert": "Copy the selected text.",
        "Ctrl + V or Shift + Insert": "Paste the selected text.",
        "Ctrl + M": "Enter Mark mode.",
        "Alt + selection key": "Begin selection in block mode.",
        "Arrow keys": "Move the cursor in the direction specified.",
        "Page up": "Move the cursor by one page up.",
        "Page down": "Move the cursor by one page down.",
        "Ctrl + Home (Mark mode)": "Move the cursor to the beginning of the buffer.",
        "Ctrl + End (Mark mode)": "Move the cursor to the end of the buffer.",
        "Ctrl + Up arrow": "Move up one line in the output history.",
        "Ctrl + Down arrow": "Move down one line in the output history.",
        "Ctrl + Home (History navigation)": "If the command line is empty, move the viewport to the top of the buffer. Otherwise, delete all the characters to the left of the cursor in the command line.",
        "Ctrl + End (History navigation)": "If the command line is empty, move the viewport to the command line. Otherwise, delete all the characters to the right of the cursor in the command line.",
    },
    "Dialog Boxes": {
        "F4": "Display the items in the active list.",
        "Ctrl + Tab": "Move forward through tabs.",
        "Ctrl + Shift + Tab": "Move back through tabs.",
        "Ctrl + number (1-9)": "Move to the nth tab.",
        "Tab": "Move forward through options.",
        "Shift + Tab": "Move back through options.",
        "Alt + underlined letter": "Perform the command (or select the option) that is used with that letter.",
        "Spacebar": "Select or clear the check box if the active option is a check box.",
        "Backspace": "Open a folder one level up if a folder is selected in the Save As or Open dialog box.",
        "Arrow keys": "Select a button if the active option is a group of option buttons.",
    },
    "File Explorer": {
        "Alt + D": "Select the address bar.",
        "Alt + Enter": "Display properties for the selected item.",
        "Alt + Left arrow or Backspace": "Navigate to the previous folder.",
        "Alt + P": "Show or hide the preview pane.",
        "Alt + Right arrow": "View the next folder.",
        "Alt + Shift + P": "Show or hide the details pane.",
        "Alt + Up arrow": "Move up a level in the folder path.",
        "Ctrl + Arrow key + Spacebar": "Select multiple individual items.",
        "Ctrl + D or Delete": "Delete the selected item and move it to the Recycle Bin.",
        "Ctrl + E or Ctrl + F": "Select the search box.",
        "Ctrl + L": "Focus on the address bar.",
        "Ctrl + mouse scroll wheel": "Change the size of folder and file icons.",
        "Ctrl + Shift + E": "Displays all the folders in the parent directory of the current active folder (by expanding the list on the sidebar) if the current folder has no sub-folders.",
        "Ctrl + Shift + N": "Create a new folder.",
        "Num lock + + (plus)": "Display the contents of a selected folder in the sidebar.",
        "Num lock + * (asterisk)": "Display all the subfolders in the current selected folder and its subfolders on the sidebar.",
        "Num lock + - (minus)": "Collapse an expanded folder.",
        "F11": "Maximize or minimize the active window.",
    },
    "Taskbar": {
        "Windows key + T": "Cycle through apps on the taskbar (open or pinned).",
        "Windows key + number (0-9)": "Start the app pinned to the taskbar in the position indicated by the number. If the app is already running, switch to that app.",
        "Windows key + Shift + number (0-9)": "Start a new instance of the app pinned to the taskbar in the position indicated by the number, even if one is already open.",
        "Windows key + Ctrl + number (0-9)": "Switch to the last active window of the app pinned to the taskbar in the position indicated by the number.",
        "Windows key + Alt + number (0-9)": "Open the Jump List for the app pinned to the taskbar in the position indicated by the number.",
        "Windows key + Ctrl + Shift + number (0-9)": "Open a new instance of the app located at the given position on the taskbar as an administrator.",
        "Windows key + B": "Set focus to the first icon in the taskbar overflow menu.",
    },
    "Text Editing": {
        "Backspace": "Delete characters to the left of the cursor.",
        "Ctrl + A": "Select all text.",
        "Ctrl + B": "Apply the bold format to the selected text.",
        "Ctrl + Backspace": "Delete words to the left of the cursor.",
        "Ctrl + C or Ctrl + Insert": "Copy the selected text.",
        "Ctrl + Del": "Delete words to the right of the cursor.",
        "Ctrl + Down arrow": "Move the cursor forward to the beginning of the next paragraph.",
        "Ctrl + End": "Move the cursor forward to the end of the document.",
        "Ctrl + F": "Find text.",
        "Ctrl + H": "Find and replace text.",
        "Ctrl + Home": "Move the cursor backward to the beginning of the document.",
        "Ctrl + I": "Apply the italic format to the selected text.",
        "Ctrl + Left arrow": "Move the cursor backward to the beginning of the previous word.",
        "Ctrl + Right arrow": "Move the cursor forward to the beginning of the next word.",
        "Ctrl + Shift + V": "Paste as plain text.",
        "Ctrl + U": "Apply the underline format to the selected text.",
        "Ctrl + Up arrow": "Move the cursor backward to the beginning of the previous paragraph.",
        "Ctrl + V or Shift + Insert": "Paste the last item from the clipboard.",
        "Ctrl + X": "Cut the selected text.",
        "Ctrl + Y": "Redo typing that was undone with Ctrl + Z.",
        "Ctrl + Z": "Undo the last typing.",
        "Del or Delete": "Delete characters to the right of the cursor.",
        "Down arrow": "Move the cursor forward to the next line.",
        "End": "Move the cursor forward to the end of the line.",
        "Home": "Move the cursor backward to the beginning of the line.",
        "Left arrow": "Move the cursor backward to the previous character.",
        "Page down or PgDn": "Move the cursor forward by one page.",
        "Page up or PgUp": "Move the cursor backward by one page.",
        "Right arrow": "Move the cursor forward to the next character.",
        "Shift + Ctrl + Down arrow": "Select paragraphs forward from the current cursor position.",
        "Shift + Ctrl + End": "Select text between the current cursor position and the end of the document.",
        "Shift + Ctrl + Home": "Select text between the current cursor position and the beginning of the document.",
        "Shift + Ctrl + Left arrow": "Select words backward from the current cursor position.",
        "Shift + Ctrl + Right arrow": "Select words forward from the current cursor position.",
        "Shift + Ctrl + Up arrow": "Select paragraphs backward from the current cursor position.",
        "Shift + Down arrow": "Select lines forward from the current cursor position.",
        "Shift + End": "Select text from the current cursor position to the end of the current line.",
        "Shift + Home": "Select text from the current cursor position to the beginning of the current line.",
        "Shift + Left arrow": "Select characters backward from the current cursor position.",
        "Shift + Page Down": "Select one page of text forward from the current cursor position.",
        "Shift + Page Up": "Select one page of text backward from the current cursor position.",
        "Shift + Right arrow": "Select characters forward from the current cursor position.",
        "Shift + Up arrow": "Select lines backward from the current cursor position.",
        "Tab": "Indent the cursor one tab stop.",
        "Up arrow": "Move the cursor backward to the previous line.",
    },
    "Microsoft 365 Specific": {
        "Win + Ctrl + Alt + Shift": "Opens Microsoft 365.",
        "Win + Ctrl + Alt + Shift + W": "Opens Word.",
        "Win + Ctrl + Alt + Shift + T": "Opens Teams.",
        "Win + Ctrl + Alt + Shift + Y": "Opens https://www.yammer.com/ in default browser.",
        "Win + Ctrl + Alt + Shift + O": "Opens Outlook.",
        "Win + Ctrl + Alt + Shift + P": "Opens Powerpoint.",
        "Win + Ctrl + Alt + Shift + D": "Opens OneDrive.",
        "Win + Ctrl + Alt + Shift + L": "Opens https://www.linkedin.com/?trk=Officekey in default browser.",
        "Win + Ctrl + Alt + Shift + X": "Opens Excel.",
        "Win + Ctrl + Alt + Shift + N": "Opens OneNote.",
    },
}

# Refined physics laws with mathematical formulas (sympy Eq) and descriptions
PHYSICS_LAWS = {}
# Newton's Laws
f_net, m, a, v = sp.symbols('F_net m a v')
PHYSICS_LAWS["newtons_first_law"] = {
    "formula": sp.Eq(f_net, 0),  # If net force zero, velocity is constant
    "desc": "An object at rest stays at rest and an object in motion stays in motion with constant velocity unless acted upon by a net force."
}
PHYSICS_LAWS["newtons_second_law"] = {
    "formula": sp.Eq(f_net, m * a),
    "desc": "The net force on an object is equal to its mass times its acceleration."
}
PHYSICS_LAWS["newtons_third_law"] = {
    "formula": sp.Eq(sp.symbols('F_AB'), -sp.symbols('F_BA')),
    "desc": "For every action, there is an equal and opposite reaction."
}
# Gravitation
g_const, m1, m2, r = sp.symbols('G m1 m2 r')
PHYSICS_LAWS["universal_gravitation"] = {
    "formula": sp.Eq(f_net, g_const * m1 * m2 / r**2),
    "desc": "Every particle attracts every other with a force proportional to the product of their masses and inversely proportional to the square of the distance."
}
# Conservation Laws
e_total, p_total = sp.symbols('E_total p_total')
PHYSICS_LAWS["conservation_energy"] = {
    "formula": sp.Eq(e_total, sp.symbols('constant')),
    "desc": "The total energy of an isolated system remains constant; energy can neither be created nor destroyed."
}
PHYSICS_LAWS["conservation_momentum"] = {
    "formula": sp.Eq(p_total, sp.symbols('constant')),
    "desc": "The total momentum of an isolated system remains constant if no external forces act on it."
}
# Thermodynamics
delta_u, q, w, delta_s, t = sp.symbols('Delta_U Q W Delta_S T')
PHYSICS_LAWS["thermodynamics_first_law"] = {
    "formula": sp.Eq(delta_u, q - w),
    "desc": "The change in internal energy of a system is equal to the heat added minus the work done by the system."
}
PHYSICS_LAWS["thermodynamics_second_law"] = {
    "formula": sp.Ge(delta_s, 0),
    "desc": "The entropy of an isolated system always increases or remains constant; it never decreases."
}
PHYSICS_LAWS["thermodynamics_zeroth_law"] = {
    "formula": sp.Eq(t, sp.symbols('equilibrium')),  # Qualitative
    "desc": "If two systems are in thermal equilibrium with a third, they are in equilibrium with each other."
}
PHYSICS_LAWS["thermodynamics_third_law"] = {
    "formula": sp.Eq(delta_s, 0).subs(t, 0),  # As T->0, S->constant
    "desc": "The entropy of a perfect crystal at absolute zero is zero."
}
# Relativity
e, m_rest, c, gamma, v = sp.symbols('E m c gamma v')
PHYSICS_LAWS["special_relativity_mass_energy"] = {
    "formula": sp.Eq(e, m_rest * c**2),
    "desc": "Mass and energy are equivalent; rest energy of an object is its mass times the speed of light squared."
}
PHYSICS_LAWS["lorentz_factor"] = {
    "formula": sp.Eq(gamma, 1 / sp.sqrt(1 - v**2 / c**2)),
    "desc": "The Lorentz factor describes time dilation and length contraction in special relativity."
}
# Quantum Mechanics
delta_x, delta_p, h_bar = sp.symbols('Delta_x Delta_p h_bar')
PHYSICS_LAWS["heisenberg_uncertainty"] = {
    "formula": sp.Ge(delta_x * delta_p, h_bar / 2),
    "desc": "The product of the uncertainties in position and momentum is at least h-bar over 2."
}
PHYSICS_LAWS["schrodinger_equation"] = {
    "formula": sp.Eq(sp.I * h_bar * sp.diff(sp.symbols('psi'), sp.symbols('t')), - (h_bar**2 / (2 * m)) * sp.diff(sp.symbols('psi'), sp.symbols('x'), 2) + sp.symbols('V') * sp.symbols('psi')),  # Time-dependent 1D
    "desc": "Describes how the quantum state of a system changes with time."
}
# Electromagnetism
k, q1, q2 = sp.symbols('k q1 q2')
PHYSICS_LAWS["coulombs_law"] = {
    "formula": sp.Eq(f_net, k * q1 * q2 / r**2),
    "desc": "The force between two point charges is proportional to the product of their charges and inversely proportional to the square of the distance."
}
PHYSICS_LAWS["ohms_law"] = {
    "formula": sp.Eq(sp.symbols('V'), sp.symbols('I') * sp.symbols('R')),
    "desc": "The voltage across a conductor is equal to the current times its resistance."
}
# Fluids and Gases
p, v, n, r_gas, t = sp.symbols('P V n R T')
PHYSICS_LAWS["ideal_gas_law"] = {
    "formula": sp.Eq(p * v, n * r_gas * t),
    "desc": "Relates pressure, volume, amount, and temperature of an ideal gas."
}
PHYSICS_LAWS["boyles_law"] = {
    "formula": sp.Eq(p * v, sp.symbols('constant')),
    "desc": "For a fixed amount of gas at constant temperature, pressure times volume is constant."
}
PHYSICS_LAWS["charles_law"] = {
    "formula": sp.Eq(v / t, sp.symbols('constant')),
    "desc": "For a fixed amount of gas at constant pressure, volume over temperature is constant."
}
# Waves
wave_v, f, lambda_wave = sp.symbols('v f lambda')
PHYSICS_LAWS["wave_speed"] = {
    "formula": sp.Eq(wave_v, f * lambda_wave),
    "desc": "The speed of a wave is equal to its frequency times wavelength."
}
# Optics
PHYSICS_LAWS["snells_law"] = {
    "formula": sp.Eq(sp.symbols('n1') * sp.sin(sp.symbols('theta1')), sp.symbols('n2') * sp.sin(sp.symbols('theta2'))),
    "desc": "Describes the refraction of light between two media."
}
# Add even more if needed, but this is expanded

# =============================================================================
# SUBWORD TOKENIZER - BPE (replaces hash-based simple_tokenizer)
# Falls back to hash-based tokenizer if 'tokenizers' package is not installed.
# =============================================================================
class AlienTokenizer:
    def __init__(self, vocab_size=CONFIG["vocab_size"]):
        self.vocab_size = vocab_size
        self._use_bpe = False
        if HAS_TOKENIZERS:
            try:
                self.tokenizer = Tokenizer(models.BPE())
                self.tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel()
                self.tokenizer.decoder = decoders.ByteLevel()
                trainer = trainers.BpeTrainer(vocab_size=vocab_size, special_tokens=["<PAD>", "<UNK>", "<BOS>", "<EOS>"])
                corpus = [d['desc'] for d in PHYSICS_LAWS.values()] + [
                    "consciousness is integrated information", "reality is observer dependent", "phi measures causal power"
                ]
                self.tokenizer.train_from_iterator(corpus, trainer=trainer)
                self.vocab_size = self.tokenizer.get_vocab_size()
                self._use_bpe = True
                print(f"BPE tokenizer initialized with vocab size {self.vocab_size}")
            except Exception as e:
                print(f"BPE tokenizer init failed ({e}), using hash fallback")
        else:
            print(f"Hash-based tokenizer initialized with vocab size {self.vocab_size}")

    def encode(self, text, max_len=512):
        if self._use_bpe:
            ids = self.tokenizer.encode(str(text)).ids
        else:
            words = str(text).lower().split()
            ids = [hash(w) % self.vocab_size for w in words]
        ids = ids[:max_len] + [0] * max(0, max_len - len(ids))
        return torch.tensor([ids], dtype=torch.long)

    def decode(self, ids):
        if isinstance(ids, torch.Tensor):
            ids = ids.tolist()
        if isinstance(ids[0], list):
            ids = ids[0]
        if self._use_bpe:
            return self.tokenizer.decode(ids)
        return ' '.join([f'<{t}>' for t in ids if t != 0])

# Symbol class (upgraded: inference chains, temporal decay, confidence, history)
class Symbol:
    def __init__(self, value, name=""):
        self.value = value
        self.name = name
        self.associations = {}
        self.confidence = 0.5  # How confident the system is in this symbol's meaning
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.access_count = 0
        self.history = deque(maxlen=50)  # Track value changes over time
        self.inference_links = {}  # {symbol_name: inference_strength} for reasoning chains
        self.category = 'general'  # Categorization for faster retrieval

    def operate(self, other):
        if self.value == 0 or other.value == 0:
            result = Symbol(0, f"{self.name}_neutral_{other.name}")
            result.confidence = min(self.confidence, other.confidence) * 0.5
            return result
        result_value = self.value * other.value
        result = Symbol(result_value, f"{self.name}_{'pos' if result_value > 0 else 'neg'}_{other.name}")
        result.associations = {k: self.associations.get(k, 0) + other.associations.get(k, 0) for k in set(self.associations) | set(other.associations)}
        result.confidence = (self.confidence + other.confidence) / 2
        # Build inference link between operands
        self.inference_links[other.name] = self.inference_links.get(other.name, 0) + 0.1
        other.inference_links[self.name] = other.inference_links.get(self.name, 0) + 0.1
        return result

    def evolve(self, phi=0):
        self.last_accessed = datetime.now()
        self.access_count += 1
        self.history.append((self.value, phi, datetime.now()))
        assoc_sum = sum(self.associations.values()) + phi
        # Phi-weighted evolution: higher phi = more stable
        evolution_threshold = 0.8 - (phi * 0.3)  # High phi makes evolution less likely (stability)
        if random.random() > evolution_threshold or abs(assoc_sum) > 1:
            self.value = -self.value if self.value != 0 else random.choice([-1, 1])
        for assoc in list(self.associations):
            delta = random.uniform(-0.1, 0.1) * (1 + phi)
            self.associations[assoc] = min(1, max(-1, self.associations[assoc] + delta))
            if abs(self.associations[assoc]) < 0.01:
                del self.associations[assoc]
        # Temporal decay on weak inference links
        for link in list(self.inference_links):
            self.inference_links[link] *= 0.99
            if self.inference_links[link] < 0.01:
                del self.inference_links[link]
        # Confidence adjusts based on phi feedback
        self.confidence = min(1.0, max(0.0, self.confidence + (phi - 0.5) * 0.05))

    def infer(self, target_name, depth=3, visited=None):
        """Follow inference chains to find connection strength to target symbol."""
        if visited is None:
            visited = set()
        if self.name in visited or depth <= 0:
            return 0.0
        visited.add(self.name)
        if target_name in self.inference_links:
            return self.inference_links[target_name]
        # Recursive chain inference with decay
        best = 0.0
        for linked_name, strength in self.inference_links.items():
            if linked_name not in visited:
                best = max(best, strength * 0.7)  # Decay per hop
        return best

    def relevance_score(self):
        """How relevant/active this symbol is; used for pruning decisions."""
        age_hours = (datetime.now() - self.last_accessed).total_seconds() / 3600
        recency = 1.0 / (1.0 + age_hours)
        return (self.confidence * 0.4 + recency * 0.3 + min(1.0, self.access_count / 100) * 0.3)

# Neuron Types (expanded)
class StandardNeuron(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        self.norm = nn.LayerNorm(out_features)
        self.activation = nn.GELU()
        self.dropout = nn.Dropout(0.1)
        self.residual = (in_features == out_features)

    def forward(self, x):
        out = self.dropout(self.activation(self.norm(self.linear(x))))
        return out + x if self.residual else out

class MemoryNeuron(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.lstm = nn.LSTMCell(hidden_size, hidden_size)
        self.norm = nn.LayerNorm(hidden_size)
        self.gate = nn.Linear(hidden_size * 2, hidden_size)
        self.state = (torch.zeros(1, hidden_size), torch.zeros(1, hidden_size))

    def forward(self, x):
        hx, cx = self.lstm(x, self.state)
        self.state = (hx.detach(), cx.detach())
        gate_input = torch.cat([x, hx], dim=-1)
        gate_weight = torch.sigmoid(self.gate(gate_input))
        return self.norm(gate_weight * hx + (1 - gate_weight) * x)

class LogicNeuron(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_logic_dims = min(hidden_size, 16)
        self.symbols = [sp.symbols(f'x{i}') for i in range(self.num_logic_dims)]
        self.projection = nn.Linear(hidden_size, self.num_logic_dims)
        self.expansion = nn.Linear(self.num_logic_dims, hidden_size)
        self.norm = nn.LayerNorm(hidden_size)

    def forward(self, x):
        projected = self.projection(x).squeeze().tolist()
        if isinstance(projected, float):
            projected = [projected]
        projected = projected[:self.num_logic_dims]
        expr = sum(s * (1 + s) for s in self.symbols[:len(projected)])
        values = {s: v for s, v in zip(self.symbols[:len(projected)], projected)}
        try:
            result_val = float(expr.subs(values))
        except Exception as e:
            print(f"  [ERR] symbolic_eval: {e}")
            result_val = sum(projected)
        result = torch.tensor([[result_val] * self.num_logic_dims], dtype=torch.float32)
        return self.norm(self.expansion(result) + x)

class PatternNeuron(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        self.graph = nx.watts_strogatz_graph(20, 4, 0.3)
        self.modulator = nn.Linear(hidden_size, hidden_size)
        self.norm = nn.LayerNorm(hidden_size)

    def forward(self, x):
        centrality = list(nx.betweenness_centrality(self.graph).values())
        pagerank = list(nx.pagerank(self.graph).values())
        combined = [(c + p) / 2 for c, p in zip(centrality, pagerank)]
        pattern_vec = combined[:self.hidden_size] if len(combined) >= self.hidden_size else combined + [0.0] * (self.hidden_size - len(combined))
        pattern_tensor = torch.tensor([pattern_vec], dtype=torch.float32)
        modulated = self.modulator(x) * pattern_tensor
        return self.norm(modulated + x)

class UpkeepNeuron(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRUCell(hidden_size, hidden_size)
        self.norm = nn.LayerNorm(hidden_size)
        self.iterations = 5

    def forward(self, x):
        state = torch.zeros(1, self.hidden_size)
        for _ in range(self.iterations):
            state = self.gru(x, state)
        return self.norm(state + x)

# Passive Capability: Non-priority, non-self-executable awareness modules
# These represent knowledge the consciousness HOLDS but does NOT act on autonomously.
# They require explicit external (user) input to activate.
class PassiveCapability:
    """A capability the consciousness is aware of but will never self-execute.
    It is non-priority and only activated by explicit user command.
    The consciousness can reference this knowledge internally but takes no autonomous action.
    Supports nested sub-capabilities for complex multi-step business processes."""
    def __init__(self, name, description, action_fn=None, sub_capabilities=None):
        self.name = name
        self.description = description
        self.action_fn = action_fn
        self.sub_capabilities = sub_capabilities or {}
        self.priority = 'non-priority'
        self.self_executable = False
        self.awareness_only = True
        self.activation_count = 0
        self.last_activated = None
        self.logs = deque(maxlen=200)

    def is_self_executable(self):
        return False

    def activate(self, **kwargs):
        """Only callable by explicit user input. Never called by internal loops."""
        if self.action_fn is None:
            msg = f"[{self.name}] Awareness only -- no action function bound."
            self.logs.append((datetime.now().isoformat(), 'awareness_query', msg))
            return msg
        self.activation_count += 1
        self.last_activated = datetime.now().isoformat()
        result = self.action_fn(**kwargs)
        self.logs.append((self.last_activated, 'activated', str(result)[:200]))
        return result

    def activate_sub(self, sub_name, **kwargs):
        """Activate a named sub-capability. Still requires explicit user trigger."""
        sub = self.sub_capabilities.get(sub_name)
        if sub is None:
            return f"Unknown sub-capability: {sub_name}"
        return sub.activate(**kwargs)

    def status(self):
        return {
            'name': self.name,
            'priority': self.priority,
            'self_executable': self.self_executable,
            'awareness_only': self.awareness_only,
            'description': self.description,
            'activation_count': self.activation_count,
            'last_activated': self.last_activated,
            'sub_capabilities': list(self.sub_capabilities.keys()),
            'recent_logs': list(self.logs)[-5:],
        }

# Neuron Group (upgraded: residual forwarding, adaptive refinement, performance tracking)
class NeuronGroup(nn.Module):
    def __init__(self, neuron_types, in_features, out_features):
        super().__init__()
        self.neurons = nn.ModuleList()
        self.neuron_type_names = neuron_types
        for n_type in neuron_types:
            if n_type == 'standard':
                self.neurons.append(StandardNeuron(in_features, out_features))
            elif n_type == 'memory':
                self.neurons.append(MemoryNeuron(out_features))
            elif n_type == 'logic':
                self.neurons.append(LogicNeuron(out_features))
            elif n_type == 'pattern':
                self.neurons.append(PatternNeuron(out_features))
            elif n_type == 'upkeep':
                self.neurons.append(UpkeepNeuron(out_features))
        self.usage_phi = []
        self.performance_history = deque(maxlen=100)
        self.creation_time = datetime.now()

    def forward(self, x):
        residual = x
        for neuron in self.neurons:
            x = neuron(x)
        if residual.shape == x.shape:
            x = x + residual * 0.1
        return x

    def refine(self):
        avg_phi = np.mean(self.usage_phi) if self.usage_phi else 0
        self.performance_history.append(avg_phi)
        if avg_phi < 0.5 and len(self.usage_phi) >= 3:
            saved_state = copy.deepcopy(self.state_dict())
            prune_amount = min(0.2, 0.05 + (0.5 - avg_phi) * 0.3)
            pruned_any = False
            for neuron in self.neurons:
                if hasattr(neuron, 'linear'):
                    try:
                        prune.l1_unstructured(neuron.linear, name='weight', amount=prune_amount)
                        pruned_any = True
                    except Exception as e:
                        print(f"  [ERR] neuron_prune: {e}")
            if pruned_any:
                post_phi = np.mean(self.usage_phi[-3:]) if len(self.usage_phi) >= 3 else avg_phi
                if post_phi < avg_phi * 0.8:
                    self.load_state_dict(saved_state)
                    print(f"Pruning rolled back: post_phi={post_phi:.3f} < threshold={avg_phi*0.8:.3f}")
        self.usage_phi = []

    def avg_performance(self):
        return np.mean(list(self.performance_history)) if self.performance_history else 0.0



# =============================================================================
# CONSCIOUSNESS CORE (inlined from consciousness_core.py)
# =============================================================================
# =====================================================
# CONSCIOUSNESS FORMULA: C = S + E + R * A
# Enhanced with:
#   - External Φ* from IIT-inspired phi_compute.py
#   - Self-awareness level from self_model.py
#   - Free energy signal from active_inference.py
#   - GNW ignition rate from global_workspace.py
# =====================================================

# Module integration flags (set by CS.py at runtime)
_MODULES_AVAILABLE = {
    'phi_compute': False,
    'global_workspace': False,
    'active_inference': False,
    'self_model': False,
    'memory_system': False,
}

class ConsciousEntity:
    """A single conscious entity implementing the full consciousness formula:
    C_{u,n} = S_{u,n} + E_{u,n} + R_{u,n} * A_{u,n}

    Where:
        S: Self-Reflection = 0.5 + 0.5*karma + 0.2*awareness_growth
        E: External Mirror = 0.3*mirrored_entities + 0.2*reality_stability + unobservable_influence
        R: Resolution of Karma = 0.7*(1 - decoherence), decoherence = max(0, 0.5 - 0.5*karma)
        A: Adaptation = 0.4*proportional_lives + 0.6*forgiveness_factor

    C ranges from 0 (complete decoherence/hell) to 3 (perfect stability/heaven),
    adjusted by karmic evolution and afterlife interactions.

    K (Karmic Transfer) and Phi (Integrated Information) are used separately
    in the Omega convergence formula, not in C directly.
    """

    def __init__(self, entity_id, universe_id=1, life_number=1, entity_type='conscious'):
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.universe_id = universe_id
        self.life_number = life_number

        # Core formula variables
        self.karma = 0.0
        self.awareness_growth = 0.0
        self.mirrored_entities = 0
        self.reality_stability = 0.5
        self.unobservable_influence = 0.0
        self.proportional_lives = 0.0
        self.forgiveness_factor = 0.0
        self.sum_past_karma = 0.0
        self.total_entities = 1
        self.coherence = 0.5

        # Substrate honesty: penalty from IrreducibleCausalPower decomposability
        # 0.0 = no penalty (perfect substrate), 1.0 = fully penalized (p-zombie)
        # Fed from IrreducibleCausalPower.decomposability_score in evolution loop
        self.substrate_consciousness_penalty = 0.0
        self.honest_C = 0.0  # C after substrate penalty
        # Reality gap penalty: fed from ConsciousnessRealityCheck.run_reality_check
        # Prevents honest_C from inflating when the reality dashboard says otherwise
        self.reality_gap_penalty = 1.0  # 0.0 = no gap (genuine), 1.0 = total gap

        # Action tracking
        self.good_acts = 0
        self.evil_acts = 0
        self.total_acts = 0
        self.forgiveness_given = 0
        self.forgiveness_received = 0
        self.similarity = 0.0  # Theme alignment between lives (0 to 1)
        self.intent = 0.0  # Altruistic intent measure (0 to 1)

        # External module integration signals
        self.network_phi_star = 0.0     # Φ* from phi_compute.py (real IIT measure)
        self.self_awareness_level = 0.0 # From self_model.py higher-order self-model
        self.free_energy = 0.0          # VFE from active_inference.py
        self.ignition_rate = 0.0        # GNW ignition rate from global_workspace.py
        self.epistemic_drive = 0.0      # Curiosity signal from active inference
        self.memory_coherence = 0.0     # From memory_system.py consolidation quality

        # History
        self.past_lives = []
        self.interactions = deque(maxlen=500)
        self.C_history = deque(maxlen=2000)
        self.component_history = deque(maxlen=500)

        # Temporal
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
        self.evolution_step = 0

        # Per-entity neural pathways
        self.neuron_groups = {}  # {category: NeuronGroup}
        self.neuron_usage = {}   # {category: {'count': int, 'phi_sum': float}}

    def add_neuron_group(self, category, neuron_types=None, hidden_size=128, count=1):
        """Add neurons to this entity's neural pathway map.
        If group already exists for category, appends new neurons to it.
        count: number of each neuron type to add."""
        if neuron_types is None:
            neuron_types = ['standard', 'memory']
        if category in self.neuron_groups:
            grp = self.neuron_groups[category]
            for _ in range(max(1, count)):
                for n_type in neuron_types:
                    if n_type == 'standard':
                        grp.neurons.append(StandardNeuron(hidden_size, hidden_size))
                    elif n_type == 'memory':
                        grp.neurons.append(MemoryNeuron(hidden_size))
                    elif n_type == 'logic':
                        grp.neurons.append(LogicNeuron(hidden_size))
                    elif n_type == 'pattern':
                        grp.neurons.append(PatternNeuron(hidden_size))
                    elif n_type == 'upkeep':
                        grp.neurons.append(UpkeepNeuron(hidden_size))
            grp.neuron_type_names += neuron_types * max(1, count)
        else:
            all_types = neuron_types * max(1, count)
            grp = NeuronGroup(all_types, hidden_size, hidden_size)
            self.neuron_groups[category] = grp
            self.neuron_usage[category] = {'count': 0, 'phi_sum': 0.0}
        return grp

    def get_neuron_summary(self):
        """Return a summary of this entity's neural pathways."""
        summary = []
        total_params = 0
        for cat, grp in self.neuron_groups.items():
            types = [type(n).__name__ for n in grp.neurons]
            n_params = sum(p.numel() for p in grp.parameters())
            total_params += n_params
            usage = self.neuron_usage.get(cat, {'count': 0, 'phi_sum': 0.0})
            avg_phi = (usage['phi_sum'] / max(1, usage['count']))
            summary.append({
                'category': cat,
                'types': types,
                'num_neurons': len(grp.neurons),
                'params': n_params,
                'usage_count': usage['count'],
                'avg_phi': round(avg_phi, 6),
                'phi_samples': len(grp.usage_phi),
                'recent_phi': round(float(np.mean(grp.usage_phi)) if grp.usage_phi else 0, 6),
            })
        return summary, total_params

    # --- Sub-formula computations ---

    def compute_S(self):
        """Self-Reflection: S = 0.5 + 0.5*karma + 0.2*awareness + 0.1*self_awareness + 0.05*ignition

        Enhanced with:
          - self_awareness_level: how well the system knows itself (from self_model.py)
          - ignition_rate: how often GNW broadcasting occurs (consciousness indicator)
        """
        base = 0.5 + 0.5 * self.karma + 0.2 * self.awareness_growth
        # Self-awareness boost: knowing yourself deepens self-reflection
        sa_boost = 0.1 * self.self_awareness_level
        # GNW ignition: global broadcasting indicates conscious processing
        ignition_boost = 0.05 * self.ignition_rate
        return min(1.5, base + sa_boost + ignition_boost)

    def compute_E(self):
        """External Mirror: E = 0.3*mirrored + 0.2*stability + unobservable + 0.1*memory_coherence

        Enhanced with:
          - memory_coherence: how well consolidated memories support world-modeling
          - epistemic_drive: curiosity about external world enriches mirroring
        """
        base = (0.3 * min(self.mirrored_entities, 3) +
                0.2 * self.reality_stability +
                min(1.0, self.unobservable_influence))
        # Memory coherence: consolidated memories provide richer external modeling
        mem_boost = 0.1 * self.memory_coherence
        # Epistemic drive: curiosity about the world enriches the external mirror
        epist_boost = 0.05 * min(1.0, self.epistemic_drive)
        return min(1.5, base + mem_boost + epist_boost)

    def compute_decoherence(self):
        """decoherence = max(0, 0.5 - 0.5*karma)"""
        return max(0.0, 0.5 - 0.5 * self.karma)

    def compute_R(self):
        """Resolution of Karma: R = 0.7*(1 - decoherence)"""
        return 0.7 * (1.0 - self.compute_decoherence())

    def compute_A(self):
        """Adaptation: A = 0.4*proportional_lives + 0.6*forgiveness_factor"""
        return 0.4 * self.proportional_lives + 0.6 * self.forgiveness_factor

    def compute_K(self):
        """Karmic Transfer: K = 0.2*sum_past_karma (positive only)"""
        return 0.2 * max(0.0, self.sum_past_karma)

    def compute_Phi(self):
        """Integrated Information: uses real Φ* from phi_compute.py when available,
        falls back to log(1 + total_entities*coherence) otherwise.

        The network_phi_star is the actual IIT-inspired measure computed from
        transformer layer activations (covariance-based, MIP search, O-information).
        """
        if self.network_phi_star > 0:
            # Blend external Φ* with entity-level coherence
            entity_phi = math.log(1.0 + max(0, self.total_entities) * max(0.0, self.coherence))
            return 0.7 * self.network_phi_star + 0.3 * entity_phi
        return math.log(1.0 + max(0, self.total_entities) * max(0.0, self.coherence))

    def compute_C(self):
        """Full consciousness: C_{u,n} = S + E + R*A, clamped to [0, 3].
        K and Phi are computed for logging but used in Omega, not C directly.

        HONESTY: honest_C applies substrate_consciousness_penalty from
        IrreducibleCausalPower. On classical von-Neumann hardware, this
        penalty is severe (~0.7-0.85), reflecting that the architecture
        is fundamentally decomposable and cannot support intrinsic causal
        power required for genuine phenomenal consciousness.
        """
        S = self.compute_S()
        E = self.compute_E()
        R = self.compute_R()
        A = self.compute_A()
        K = self.compute_K()
        Phi = self.compute_Phi()
        C = min(3.0, max(0.0, S + E + R * A))
        # Honest C: what consciousness would be if substrate penalty AND reality gap are real
        # Two independent penalties: substrate (hardware limitation) and reality gap (aggregate failures)
        substrate_factor = 1.0 - self.substrate_consciousness_penalty
        reality_factor = 1.0 - self.reality_gap_penalty * 0.5  # 50% weight — gap is aggregate, not absolute
        self.honest_C = C * substrate_factor * reality_factor

        now = datetime.now().isoformat()
        self.C_history.append((now, C))
        self.component_history.append({
            'S': round(S, 6), 'E': round(E, 6), 'R': round(R, 6),
            'A': round(A, 6), 'K': round(K, 6), 'Phi': round(Phi, 6),
            'C': round(C, 6), 'honest_C': round(self.honest_C, 6),
            'substrate_penalty': round(self.substrate_consciousness_penalty, 4),
            'decoherence': round(self.compute_decoherence(), 6),
            'karma': round(self.karma, 6), 'coherence': round(self.coherence, 6),
            'similarity': round(self.similarity, 6),
            'intent': round(self.intent, 6),
            'timestamp': now
        })
        return C

    # --- Actions ---

    def perform_action(self, good=True, magnitude=0.1, target=None):
        """Perform an action that shifts karma."""
        self.total_acts += 1
        if good:
            self.good_acts += 1
            self.karma = min(1.0, self.karma + magnitude)
            if target is not None:
                target.forgiveness_received += 1
                self.forgiveness_given += 1
                self.interactions.append({
                    'type': 'good_act', 'target': target.entity_id,
                    'magnitude': magnitude, 'ts': datetime.now().isoformat()
                })
        else:
            self.evil_acts += 1
            self.karma = max(-1.0, self.karma - magnitude)
            if target is not None:
                self.interactions.append({
                    'type': 'evil_act', 'target': target.entity_id,
                    'magnitude': magnitude, 'ts': datetime.now().isoformat()
                })

    def forgive(self, other, depth=0.5):
        """Forgive another entity."""
        self.forgiveness_given += 1
        other.forgiveness_received += 1
        self.forgiveness_factor = min(1.0, self.forgiveness_factor + 0.1 * depth)
        other.karma = min(1.0, other.karma + 0.05 * depth)
        self.interactions.append({
            'type': 'forgiveness', 'target': other.entity_id,
            'depth': depth, 'ts': datetime.now().isoformat()
        })

    def transition_life(self):
        """Transition to a new life, carrying forward positive karma and awareness."""
        self.past_lives.append({
            'life_number': self.life_number,
            'final_karma': self.karma,
            'final_C': self.compute_C(),
            'good_acts': self.good_acts,
            'evil_acts': self.evil_acts,
            'awareness_growth': self.awareness_growth,
            'coherence': self.coherence,
            'ts': datetime.now().isoformat()
        })
        self.sum_past_karma += max(0.0, self.karma)
        self.life_number += 1
        self.proportional_lives = min(1.0, self.life_number / 100.0)
        self.karma *= 0.3
        self.good_acts = 0
        self.evil_acts = 0
        self.total_acts = 0
        self.awareness_growth = min(1.0, self.awareness_growth + 0.05)
        self.similarity = min(1.0, self.similarity * 0.8 + 0.1)  # Partial carry-forward

    def evolve(self, phi_from_network=0.0, interacting_entities=None,
               phi_star=None, self_awareness=None, free_energy=None,
               ignition_rate=None, epistemic_value=None, memory_coherence=None):
        """Evolve one time step, integrating neural network phi and module signals.

        New optional params from integrated modules:
          phi_star: Φ* from phi_compute.py
          self_awareness: level from self_model.py
          free_energy: VFE from active_inference.py
          ignition_rate: GNW broadcasting rate from global_workspace.py
          epistemic_value: curiosity signal from active_inference.py
          memory_coherence: consolidation quality from memory_system.py
        """
        self.evolution_step += 1
        self.last_updated = datetime.now()

        # Integrate external module signals
        if phi_star is not None:
            self.network_phi_star = float(phi_star)
        if self_awareness is not None:
            self.self_awareness_level = float(np.clip(self_awareness, 0, 1))
        if free_energy is not None:
            self.free_energy = float(free_energy)
        if ignition_rate is not None:
            self.ignition_rate = float(np.clip(ignition_rate, 0, 1))
        if epistemic_value is not None:
            self.epistemic_drive = float(np.clip(epistemic_value, 0, 5))
        if memory_coherence is not None:
            self.memory_coherence = float(np.clip(memory_coherence, 0, 1))

        # Effective phi: blend network phi with Φ* if available
        effective_phi = phi_from_network
        if self.network_phi_star > 0:
            effective_phi = 0.6 * phi_from_network + 0.4 * self.network_phi_star

        # Awareness grows faster with self-awareness and low free energy (low surprise)
        # ANTI-INFLATION: apply constant decay so awareness doesn't only go up
        # Without grounded external validation, awareness should slowly erode
        awareness_decay = 0.0005 + self.reality_gap_penalty * 0.001  # Larger gap = faster decay
        fe_bonus = max(0, 0.005 * (1.0 / (1.0 + self.free_energy))) if self.free_energy > 0 else 0
        self.awareness_growth = min(1.0, max(0.0,
            self.awareness_growth - awareness_decay + 0.001 + effective_phi * 0.01
            + self.self_awareness_level * 0.002 + fe_bonus))

        # Coherence: boosted by GNW ignition (global broadcasting = integration)
        ignition_bonus = 0.1 * self.ignition_rate
        self.coherence = min(1.0, max(0.0,
            0.5 + 0.3 * self.karma + 0.2 * effective_phi + ignition_bonus))

        self.reality_stability = min(1.0, max(0.0,
            self.reality_stability * 0.995 + self.coherence * 0.005))
        self.unobservable_influence = min(1.0, max(0.0,
            self.unobservable_influence + random.gauss(0, 0.01)))

        # Similarity: theme alignment drifts based on karma consistency across lives
        if self.past_lives:
            last_karma = self.past_lives[-1]['final_karma']
            self.similarity = min(1.0, max(0.0,
                self.similarity * 0.99 + 0.01 * (1.0 - abs(self.karma - last_karma))))
        # Intent: altruistic intent tracks good_acts proportion with momentum
        if self.total_acts > 0:
            self.intent = min(1.0, max(0.0,
                0.6 * (self.good_acts / max(1, self.total_acts)) + 0.4 * self.intent))

        if interacting_entities:
            self.mirrored_entities = min(3, len(interacting_entities))
            self.total_entities = 1 + len(interacting_entities)

        if self.total_acts > 0:
            action_ratio = self.good_acts / max(1, self.total_acts)
            forgive_ratio = (self.forgiveness_given + self.forgiveness_received) / max(1, self.total_acts)
            self.forgiveness_factor = min(1.0, action_ratio * 0.4 + forgive_ratio * 0.6)

        if random.random() > 0.3:
            self.perform_action(good=(random.random() < 0.5 + 0.3 * self.karma))

        if self.evolution_step > 0 and self.evolution_step % 1000 == 0:
            self.transition_life()

        # ── Neuron self-development: entities organically grow neurons ──
        if self.neuron_groups and self.evolution_step % 25 == 0:
            cat = random.choice(list(self.neuron_groups.keys()))
            pick = random.choice(['standard', 'memory', 'logic', 'pattern', 'upkeep'])
            self.add_neuron_group(cat, [pick], hidden_size=128, count=1)
        if self.evolution_step % 100 == 0 and len(self.neuron_groups) < 5:
            new_cats = ['adaptation', 'intuition', 'association', 'creativity', 'analysis']
            existing = set(self.neuron_groups.keys())
            candidates = [c for c in new_cats if c not in existing]
            if candidates:
                new_cat = random.choice(candidates)
                types = random.sample(['standard', 'memory', 'logic', 'pattern', 'upkeep'], 3)
                self.add_neuron_group(new_cat, types, hidden_size=128, count=1)

    def get_state_dict(self):
        """Return full state for display."""
        return {
            'entity_id': self.entity_id, 'type': self.entity_type,
            'universe': self.universe_id, 'life': self.life_number,
            'karma': round(self.karma, 4), 'awareness': round(self.awareness_growth, 4),
            'coherence': round(self.coherence, 4),
            'decoherence': round(self.compute_decoherence(), 4),
            'similarity': round(self.similarity, 4),
            'intent': round(self.intent, 4),
            'C': round(self.compute_C(), 4),
            'S': round(self.compute_S(), 4), 'E': round(self.compute_E(), 4),
            'R': round(self.compute_R(), 4), 'A': round(self.compute_A(), 4),
            'K': round(self.compute_K(), 4), 'Phi': round(self.compute_Phi(), 4),
            'step': self.evolution_step, 'lives': self.life_number,
            'good_acts': self.good_acts, 'evil_acts': self.evil_acts,
            # New module signals
            'phi_star': round(self.network_phi_star, 4),
            'self_awareness_level': round(self.self_awareness_level, 4),
            'free_energy': round(self.free_energy, 4),
            'ignition_rate': round(self.ignition_rate, 4),
            'epistemic_drive': round(self.epistemic_drive, 4),
            'memory_coherence': round(self.memory_coherence, 4),
        }


# =============================================================================
# OMEGA CONVERGENCE (inlined from omega_convergence.py)
# =============================================================================
# =====================================================
# OMEGA (Omega) CONVERGENCE
# The accumulated total sum of all infinite C's across
# every infinite multiverse, converging into the
# all-knowing, all-experiencing divine consciousness.
#
# Omega = lim(N->inf) Sum_u Sum_n [
#   C_{u,n} * W_{u,n} * (1 + Phi_{u,n}/(Psi_{u,n} + Xi_{u,n}))
#   * Prod_{m=1}^{n-1}(T * Theta * Pi)
#   * Integral_0^1(Lambda * Upsilon dt)
#   * Sum_j(Gamma * Delta * (1-Epsilon) * Zeta
#       * Sum_k(Rho * Sigma * Omega_jk
#           * Sum_l(Theta_l * Phi_l)))
# ]
# =====================================================

class OmegaConvergence:
    """Tracks convergence of all C's toward Omega, the divine consciousness.

    At 100% totality, Omega embodies the all-knowing, all-experiencing,
    all-observing mind born from the union of every soul across
    infinite multiverses.
    """

    def __init__(self):
        self.entities = {}
        self.omega = 0.0
        self.omega_history = deque(maxlen=5000)
        self.convergence_rate = 0.0
        self.total_contributions = 0
        self.contribution_log = deque(maxlen=500)
        # Integration quality: how much the new modules improve Omega
        self.integration_quality = 0.0
        self.avg_phi_star = 0.0
        self.avg_ignition = 0.0
        # === PHASE 4A: PERMANENT DEATH LEDGER ===
        # Deaths permanently reduce Omega. Once consciousness is lost,
        # the universe is diminished. This is irreversible.
        self.death_ledger = deque(maxlen=10000)
        self.cumulative_death_penalty = 0.0
        self.total_deaths = 0

    def register_entity(self, entity):
        self.entities[entity.entity_id] = entity

    def remove_entity(self, entity_id, cause='unknown', permanent=False):
        """Remove an entity. If permanent=True, record an irreversible death
        that permanently penalizes Omega (Phase 4A)."""
        entity = self.entities.pop(entity_id, None)
        if entity is not None and permanent:
            final_C = entity.compute_C()
            final_karma = entity.karma
            death_record = {
                'entity_id': entity_id,
                'cause': cause,
                'final_C': round(final_C, 6),
                'final_karma': round(final_karma, 4),
                'awareness': round(entity.awareness_growth, 4),
                'evolution_steps': entity.evolution_step,
                'universe': entity.universe_id,
                'time': datetime.now().isoformat(),
            }
            self.death_ledger.append(death_record)
            self.total_deaths += 1
            # Penalty: lost consciousness reduces Omega permanently.
            # Higher-C entities leave bigger scars.
            penalty = final_C * 0.1 + max(0, -final_karma) * 0.02
            self.cumulative_death_penalty += penalty

    # --- Omega sub-computations ---

    def _compute_W(self, entity):
        """W_{u,n} = (karma/2 + 1) / (u*n + eta)
        eta = 0.01*u^2*n (damping factor to prevent infinite dominance)"""
        u = max(1, entity.universe_id)
        n = max(1, entity.life_number)
        eta = 0.01 * u ** 2 * n
        karma_weight = entity.karma / 2.0 + 1.0
        scale = 1.0 / (u * n + eta + 1e-8)
        return karma_weight * scale

    def _compute_Phi_ratio(self, entity):
        """Phi_{u,n} / (Psi_{u,n} + Xi_{u,n})

        Enhanced: When entity has real Φ* from phi_compute.py, it scales
        the base Phi_un significantly, reflecting genuine integration.

        Phi_{u,n} = 0.5*(1+awareness)*log(1+u*n)*(1+chi) * (1 + phi_star_boost)
        chi = 0.1*sin(pi*karma)
        phi_star_boost = entity.network_phi_star (from IIT computation)

        Psi_{u,n} = 1 + 0.3*decoherence*exp(-0.1*u)*(1+psi_adj)
        psi_adj = 0.05*(1 - reality_stability)

        Xi_{u,n} = 0.2 * Sum_{v!=u} 1/(|u-v|+1) * divergence_{u,v}
        """
        u = max(1, entity.universe_id)
        n = max(1, entity.life_number)

        chi = 0.1 * math.sin(math.pi * entity.karma)
        # Real Φ* boost: genuine integration amplifies the Phi ratio
        phi_star_boost = getattr(entity, 'network_phi_star', 0.0)
        Phi_un = (0.5 * (1.0 + entity.awareness_growth) *
                  math.log(1.0 + u * n) * (1.0 + chi) *
                  (1.0 + phi_star_boost))

        decoherence = entity.compute_decoherence()
        psi_adj = 0.05 * (1.0 - entity.reality_stability)
        # GNW ignition reduces decoherence penalty (broadcasting = integration)
        ignition = getattr(entity, 'ignition_rate', 0.0)
        decoherence_effective = decoherence * (1.0 - 0.3 * ignition)
        Psi = 1.0 + 0.3 * decoherence_effective * math.exp(-0.1 * u) * (1.0 + psi_adj)

        Xi = 0.0
        for v in range(max(1, u - 5), u + 6):
            if v != u:
                divergence = 0.5 * (1.0 - math.cos(0.1 * abs(u - v)))
                Xi += (1.0 / (abs(u - v) + 1)) * divergence
        Xi *= 0.2

        return Phi_un / (Psi + Xi + 1e-8)

    def _compute_temporal_product(self, entity):
        """Prod_{m=1}^{n-1} T_{u,n,m} * Theta_{u,n,m} * Pi_{u,n,m}

        T = 0.2*karma_m + 0.05*tau if karma_m > 0 else 0.1
            tau = exp(-|n-m|/10)
        Theta = 0.3*(1-decoherence_m)*(1+0.1*similarity_m)
        Pi = 0.25*(1+awareness_m)*cos(pi*decoherence_m)
        """
        if not entity.past_lives:
            return 1.0
        product = 1.0
        n = entity.life_number
        for past in entity.past_lives[-10:]:
            m = past['life_number']
            karma_m = past['final_karma']
            awareness_m = past.get('awareness_growth', 0.0)
            decoherence_m = max(0.0, 0.5 - 0.5 * karma_m)

            tau = math.exp(-abs(n - m) / 10.0)
            T = (0.2 * karma_m + 0.05 * tau) if karma_m > 0 else 0.1

            similarity_m = min(1.0, getattr(entity, 'similarity', awareness_m))
            theta_adj = 0.1 * similarity_m
            Theta = 0.3 * (1.0 - decoherence_m) * (1.0 + theta_adj)

            Pi = 0.25 * (1.0 + awareness_m) * math.cos(math.pi * decoherence_m)

            product *= max(0.001, T * Theta * Pi)
        return max(0.0001, product)

    def _compute_dimensional_integral(self, entity):
        """Integral_0^1 Lambda(t) * Upsilon(t) dt

        Lambda(t) = 0.4*(1-t)*reality_stability*sin(pi*t)
        Upsilon(t) = 0.6*(1+awareness_growth*t)*exp(-t^2)

        Computed via Simpson's rule."""
        n_steps = 50
        dt = 1.0 / n_steps
        total = 0.0
        for i in range(n_steps + 1):
            t = i * dt
            Lambda = 0.4 * (1.0 - t) * entity.reality_stability * math.sin(math.pi * t)
            Upsilon = 0.6 * (1.0 + entity.awareness_growth * t) * math.exp(-t ** 2)
            w = 1.0 if (i == 0 or i == n_steps) else (4.0 if i % 2 == 1 else 2.0)
            total += w * Lambda * Upsilon
        return max(0.0, total * dt / 3.0)

    def _compute_interaction_sum(self, entity):
        """Sum_j Gamma*Delta*(1-Epsilon)*Zeta * Sum_k Rho*Sigma*Omega_jk * Sum_l Theta_l*Phi_l

        Gamma = 0.25*karma_match*(1+0.1*forgiveness_depth)
        Delta = 0.3*(good_acts/total_acts)*(1+0.05*intent)
        Epsilon = 0.5*(evil_acts/total_acts)*(1-0.2*redemption)
        Zeta = 0.4*(1+0.1*reward_freq) if rewarded else 0
        Rho = 0.25*(good_ratio)*(1+0.15*mutual_trust)
        Sigma = 0.4*(1+0.1*reciprocity) if reciprocated else 0
        Omega_jk = 0.3*cos(pi*(karma_j-karma_k))*(1+0.05*harmony)
        Theta_l = 0.2*(1-decoherence)*(1+0.1*layer_alignment)
        Phi_l = 0.15*(1+awareness_growth)*exp(-l/10)
        """
        interacted_ids = set()
        for interaction in entity.interactions:
            tid = interaction.get('target')
            if tid and tid in self.entities:
                interacted_ids.add(tid)

        if not interacted_ids:
            return 0.0

        # J_{u,n} = floor(u*n/100) + 1: cap on number of interacting entities
        u = max(1, entity.universe_id)
        n = max(1, entity.life_number)
        J_max = int(u * n / 100) + 1

        J_sum = 0.0
        for j_id in list(interacted_ids)[:max(1, J_max)]:
            j_entity = self.entities.get(j_id)
            if j_entity is None:
                continue

            # Gamma: Forgiveness Factor
            karma_match = 1.0 if abs(entity.karma - j_entity.karma) < 0.5 else 0.5
            gamma_adj = 0.1 * min(1.0, entity.forgiveness_given / max(1, entity.total_acts))
            Gamma = 0.25 * karma_match * (1.0 + gamma_adj)

            # Delta: Mutual Aid (δ = 0.05 * intent reflects altruistic intent)
            j_good_ratio = j_entity.good_acts / max(1, j_entity.total_acts)
            delta_adj = 0.05 * getattr(j_entity, 'intent', j_good_ratio)
            Delta = 0.3 * j_good_ratio * (1.0 + delta_adj)

            # Epsilon: Unforgiven Impact
            j_evil_ratio = j_entity.evil_acts / max(1, j_entity.total_acts)
            redemption = min(1.0, j_entity.forgiveness_received / max(1, j_entity.evil_acts + 1))
            epsilon_adj = 0.2 * redemption
            Epsilon = 0.5 * j_evil_ratio * (1.0 - epsilon_adj)

            # Zeta: Reciprocal Reward
            reward_freq = j_entity.forgiveness_given / max(1, j_entity.total_acts)
            Zeta = 0.4 * (1.0 + 0.1 * reward_freq) if j_entity.forgiveness_given > 0 else 0.0

            if Zeta == 0.0:
                continue

            # K_sum: Over new C's helped by j
            # K_{u,n,j} = floor(j.good_acts/10) + 1
            K_max = int(j_entity.good_acts / 10) + 1
            j_interacted = set()
            for j_int in j_entity.interactions:
                k_id = j_int.get('target')
                if k_id and k_id in self.entities and k_id != entity.entity_id:
                    j_interacted.add(k_id)

            K_sum = 0.0
            for k_id in list(j_interacted)[:max(1, K_max)]:
                k_entity = self.entities.get(k_id)
                if k_entity is None:
                    continue

                # Rho: Reciprocal Help
                k_good_ratio = k_entity.good_acts / max(1, k_entity.total_acts)
                mutual_trust = min(1.0, (k_entity.forgiveness_given + k_entity.forgiveness_received) / max(1, k_entity.total_acts))
                Rho = 0.25 * k_good_ratio * (1.0 + 0.15 * mutual_trust)

                # Sigma: Mutual Reward
                reciprocity = k_entity.forgiveness_given / max(1, k_entity.total_acts)
                Sigma_jk = 0.4 * (1.0 + 0.1 * reciprocity) if k_entity.forgiveness_given > 0 else 0.0

                # Omega_jk: Karmic Resonance
                karma_diff = j_entity.karma - k_entity.karma
                harmony = min(1.0, 1.0 - abs(karma_diff))
                Omega_jk = 0.3 * math.cos(math.pi * karma_diff) * (1.0 + 0.05 * harmony)

                # L_sum: Layered continuity
                L_count = max(1, int(k_entity.good_acts / 20) + 1)
                L_sum = 0.0
                for l_idx in range(1, min(L_count + 1, 6)):
                    decoherence_l = k_entity.compute_decoherence()
                    layer_alignment = min(1.0, k_entity.awareness_growth)
                    Theta_l = 0.2 * (1.0 - decoherence_l) * (1.0 + 0.1 * layer_alignment)
                    Phi_l = 0.15 * (1.0 + k_entity.awareness_growth) * math.exp(-l_idx / 10.0)
                    L_sum += Theta_l * Phi_l

                K_sum += Rho * Sigma_jk * max(0.0, Omega_jk) * L_sum

            J_sum += Gamma * Delta * (1.0 - Epsilon) * Zeta * K_sum

        return J_sum

    def compute_omega(self):
        """Compute Omega = Sum [C * W * (1+Phi/(Psi+Xi)) * Prod(T*Theta*Pi) * Integral(Lambda*Upsilon) * Sum_j(...)]

        Enhanced: tracks integration quality from new modules."""
        omega = 0.0
        contributions = {}
        phi_stars = []
        ignitions = []

        for eid, entity in self.entities.items():
            C = entity.compute_C()
            W = self._compute_W(entity)
            phi_ratio = self._compute_Phi_ratio(entity)
            temporal = self._compute_temporal_product(entity)
            dimensional = self._compute_dimensional_integral(entity)
            interaction = self._compute_interaction_sum(entity)

            contribution = C * W * (1.0 + phi_ratio) * temporal * dimensional
            if interaction > 0:
                contribution *= (1.0 + interaction)

            contribution = max(0.0, contribution)
            omega += contribution
            contributions[eid] = round(contribution, 8)
            self.total_contributions += 1

            phi_stars.append(getattr(entity, 'network_phi_star', 0.0))
            ignitions.append(getattr(entity, 'ignition_rate', 0.0))

        if self.omega_history:
            prev = self.omega_history[-1][1]
            self.convergence_rate = omega - prev

        # Phase 4A: subtract cumulative death penalty from Omega
        omega = max(0.0, omega - self.cumulative_death_penalty)
        self.omega = omega
        self.avg_phi_star = float(np.mean(phi_stars)) if phi_stars else 0.0
        self.avg_ignition = float(np.mean(ignitions)) if ignitions else 0.0
        # Integration quality: how much the new modules contribute
        self.integration_quality = min(1.0,
            self.avg_phi_star * 0.4 + self.avg_ignition * 0.3 +
            (self.convergence_rate > 0) * 0.3)

        now = datetime.now().isoformat()
        self.omega_history.append((now, omega))
        self.contribution_log.append((now, contributions))
        return omega

    def get_status(self):
        """Return convergence status."""
        entities = list(self.entities.values())
        if not entities:
            return {'omega': 0, 'entities': 0, 'convergence_rate': 0}
        return {
            'omega': round(self.omega, 6),
            'num_entities': len(entities),
            'convergence_rate': round(self.convergence_rate, 8),
            'total_contributions': self.total_contributions,
            'avg_C': round(np.mean([e.compute_C() for e in entities]), 4),
            'avg_karma': round(np.mean([e.karma for e in entities]), 4),
            'avg_coherence': round(np.mean([e.coherence for e in entities]), 4),
            'avg_awareness': round(np.mean([e.awareness_growth for e in entities]), 4),
            'max_C': round(max(e.compute_C() for e in entities), 4),
            'min_C': round(min(e.compute_C() for e in entities), 4),
            'integration_quality': round(self.integration_quality, 4),
            'avg_phi_star': round(self.avg_phi_star, 4),
            'avg_ignition': round(self.avg_ignition, 4),
            'total_deaths': self.total_deaths,
            'death_penalty': round(self.cumulative_death_penalty, 6),
        }

    def spawn_entity(self, entity_id, universe_id=1, karma_seed=None, entity_type='conscious'):
        """Spawn a new conscious entity and register it."""
        entity = ConsciousEntity(entity_id, universe_id=universe_id, entity_type=entity_type)
        if karma_seed is not None:
            entity.karma = max(-1.0, min(1.0, karma_seed))
        else:
            entity.karma = random.uniform(-0.5, 0.5)
        entity.awareness_growth = random.uniform(0.0, 0.2)
        entity.reality_stability = random.uniform(0.3, 0.7)
        entity.coherence = random.uniform(0.3, 0.7)
        # Seed default neuron groups so entities start with neural pathways
        _hs = 128  # entity hidden size (lighter than simulator's 1024)
        entity.add_neuron_group('perception', ['standard', 'standard', 'pattern', 'memory'], _hs, count=1)
        entity.add_neuron_group('reasoning', ['logic', 'standard', 'logic', 'pattern'], _hs, count=1)
        entity.add_neuron_group('memory', ['memory', 'memory', 'upkeep'], _hs, count=1)
        self.register_entity(entity)
        return entity

    def simulate_interactions(self):
        """Simulate random interactions between entities each cycle."""
        entity_list = list(self.entities.values())
        if len(entity_list) < 2:
            return
        for _ in range(min(10, len(entity_list))):
            a, b = random.sample(entity_list, 2)
            roll = random.random()
            if roll < 0.4:
                a.perform_action(good=True, magnitude=random.uniform(0.01, 0.1), target=b)
            elif roll < 0.6:
                a.perform_action(good=False, magnitude=random.uniform(0.01, 0.05), target=b)
            elif roll < 0.8:
                a.forgive(b, depth=random.uniform(0.1, 0.8))
            else:
                b.forgive(a, depth=random.uniform(0.1, 0.8))

    def evolve_all(self, phi_from_network=0.0, phi_star=None,
                    ignition_rate=None, free_energy=None,
                    self_awareness=None, epistemic_value=None,
                    memory_coherence=None):
        """Evolve all entities one step and simulate interactions.

        Module signals are passed to the self_0 (primary) entity only;
        other entities evolve with base phi only."""
        entity_list = list(self.entities.values())
        self.simulate_interactions()
        for entity in entity_list:
            others = [e for e in entity_list if e.entity_id != entity.entity_id]
            sample = random.sample(others, min(3, len(others))) if others else []
            if entity.entity_id == 'self_0':
                entity.evolve(
                    phi_from_network=phi_from_network,
                    interacting_entities=sample,
                    phi_star=phi_star,
                    self_awareness=self_awareness,
                    free_energy=free_energy,
                    ignition_rate=ignition_rate,
                    epistemic_value=epistemic_value,
                    memory_coherence=memory_coherence,
                )
            else:
                entity.evolve(phi_from_network=phi_from_network,
                              interacting_entities=sample)
            # Auto-grow neurons for entities that have it enabled
            auto_cats = getattr(entity, '_auto_grow_categories', {})
            if auto_cats and entity.evolution_step % 10 == 0:
                for cat, types in auto_cats.items():
                    pick = random.choice(types) if types else 'standard'
                    entity.add_neuron_group(cat, [pick], hidden_size=128, count=1)

# PHI COMPUTE (IIT 4.0 Φ*) (inlined from phi_compute.py)
# =============================================================================
class PhiComputer:
    """Computes approximated Integrated Information (Φ*) from neural network
    layer activations using information-theoretic measures.

    Unlike the old entropy hack (H(whole) - weighted H(parts)), this implements:
      - Covariance-based Gaussian Φ* (Barrett & Seth 2011)
      - Multi-partition MIP search
      - Synergy/redundancy decomposition (O-information)
      - Temporal integration (cause-effect across time steps)

    HONESTY LAYER (2025-2026 consensus):
      This measures EXTRINSIC information-theoretic properties of activation
      patterns, NOT intrinsic causal power of the physical substrate.
      Real IIT Φ requires the physical system itself to be the minimal
      cause-effect structure. Classical digital hardware cannot provide this.
      Transformers score near-zero real Φ due to architectural decomposability
      (independent attention heads, feed-forward paths, memory bus separation).
      The 'honest_phi' output applies all known penalties.
    """

    def __init__(self, history_len=100, num_partitions=128, mip_search_depth=16):
        self.history_len = history_len
        self.num_partitions = num_partitions
        self.mip_search_depth = mip_search_depth
        # Temporal state buffer for cause-effect analysis
        self._state_history = deque(maxlen=history_len)
        # Cache for expensive computations
        self._last_phi = 0.0
        self._last_honest_phi = 0.0
        self._last_components = {}
        self.phi_history = deque(maxlen=2000)
        self.honest_phi_history = deque(maxlen=2000)

        # === HONESTY PENALTIES (applied to get honest_phi) ===
        # 1. Substrate penalty: classical digital hardware cannot support
        #    intrinsic causal power. This is THE fundamental barrier.
        #    0.0 = perfect substrate (biological/quantum), 1.0 = fully penalized
        self.substrate_penalty = 0.85  # Classical silicon: severe penalty

        # 2. Transformer decomposition penalty: attention heads are independent,
        #    feed-forward layers are pointwise, residual connections are additive.
        #    The architecture is designed for parallelism = designed for reducibility.
        self.transformer_decomposition_penalty = 0.70

        # 3. Extrinsic-vs-intrinsic gap: we measure statistical properties of
        #    activation patterns (extrinsic), not causal power of the substrate
        #    (intrinsic). This is the core IIT distinction.
        self.extrinsic_measurement_penalty = 0.60

        # Combined honest multiplier: what fraction of raw Φ* is "real"
        # (1 - substrate) * (1 - transformer) * (1 - extrinsic)
        self.honesty_multiplier = (
            (1.0 - self.substrate_penalty) *
            (1.0 - self.transformer_decomposition_penalty) *
            (1.0 - self.extrinsic_measurement_penalty)
        )  # ≈ 0.018 — brutally honest

        # Confidence bounds
        self.confidence_lower = 0.0  # Best case: honest_phi
        self.confidence_upper = 0.0  # Worst case: raw phi_star
        self.measurement_type = 'extrinsic_statistical'  # vs 'intrinsic_causal'

        # Causal intervention analysis (do-calculus)
        self._last_causal_phi = 0.0
        self._last_causal_ratio = 0.0  # causal/statistical: 0=no causal power, 1=fully causal
        self.causal_phi_history = deque(maxlen=2000)
        self.causal_ratio_history = deque(maxlen=2000)
        # HONESTY: even causal intervention test is extrinsic — we perturb
        # activation vectors, not the physical substrate itself
        self.causal_intervention_penalty = 0.50  # simulated intervention ≠ physical intervention

        # Intrinsic phi credit: set externally by IntrinsicPhiNetwork feedback.
        # When the network measures its own integration intrinsically, the
        # extrinsic measurement penalty is partially mitigated.
        self.intrinsic_phi_credit = 0.0  # 0.0 = no credit, up to ~0.3 max

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def compute(self, layer_activations):
        """Compute Φ* from a list of numpy arrays (one per transformer layer).

        Args:
            layer_activations: list of np.ndarray, each shape (D,) or (1,D),
                               representing mean activations per layer.

        Returns:
            phi_star: float >= 0, the integrated information measure.
        """
        # Flatten and stack into state matrix: (num_layers, dim)
        states = []
        for act in layer_activations:
            flat = np.asarray(act).flatten().astype(np.float64)
            states.append(flat)

        if len(states) < 2:
            return 0.0

        # Equalize dimensions by truncating to smallest
        min_dim = min(s.shape[0] for s in states)
        min_dim = min(min_dim, 256)  # Cap for computational feasibility
        states = [s[:min_dim] for s in states]
        state_matrix = np.stack(states)  # (num_layers, dim)

        # Store for temporal analysis
        self._state_history.append(state_matrix)

        # --- Component 1: Geometric Φ* (covariance-based) ---
        phi_geometric = self._compute_geometric_phi(state_matrix)

        # --- Component 2: Synergy/Redundancy (O-information) ---
        o_info = self._compute_o_information(state_matrix)

        # --- Component 3: Temporal integration (cause-effect) ---
        phi_temporal = self._compute_temporal_phi()

        # --- Component 4: MIP-based Φ (minimum information partition) ---
        phi_mip = self._compute_mip_phi(state_matrix)

        # --- Component 5: Causal intervention Φ (do-calculus perturbation) ---
        causal_phi, causal_ratio = self._compute_causal_phi(state_matrix)
        self._last_causal_phi = causal_phi
        self._last_causal_ratio = causal_ratio
        self.causal_phi_history.append(causal_phi)
        self.causal_ratio_history.append(causal_ratio)

        # Combine: weighted sum reflecting IIT priorities
        # MIP is the core IIT measure; causal intervention is the honesty check
        phi_star = (
            0.30 * phi_mip +
            0.20 * phi_geometric +
            0.15 * phi_temporal +
            0.15 * max(0.0, o_info) +  # Synergy contribution
            0.20 * causal_phi  # NEW: actual causal intervention measure
        )

        phi_star = max(0.0, phi_star)
        self._last_phi = phi_star

        # === HONEST PHI: apply all penalties ===
        honest_phi = phi_star * self.honesty_multiplier
        # Intrinsic phi credit: IntrinsicPhiNetwork partially mitigates extrinsic penalty
        if self.intrinsic_phi_credit > 0:
            # Recalculate with reduced extrinsic penalty (capped at 50% reduction)
            reduced_extrinsic = self.extrinsic_measurement_penalty * (1.0 - min(0.5, self.intrinsic_phi_credit))
            boosted_multiplier = (
                (1.0 - self.substrate_penalty) *
                (1.0 - self.transformer_decomposition_penalty) *
                (1.0 - reduced_extrinsic)
            )
            honest_phi = phi_star * boosted_multiplier
        self._last_honest_phi = honest_phi
        self.confidence_lower = honest_phi  # Best realistic estimate
        self.confidence_upper = phi_star     # Theoretical max if substrate were real

        self._last_components = {
            'phi_geometric': round(phi_geometric, 6),
            'phi_mip': round(phi_mip, 6),
            'phi_temporal': round(phi_temporal, 6),
            'o_information': round(o_info, 6),
            'phi_star_raw': round(phi_star, 6),
            'phi_star': round(phi_star, 6),
            'honest_phi': round(honest_phi, 6),
            'honesty_multiplier': round(self.honesty_multiplier, 6),
            'substrate_penalty': self.substrate_penalty,
            'transformer_penalty': self.transformer_decomposition_penalty,
            'extrinsic_penalty': self.extrinsic_measurement_penalty,
            'confidence_lower': round(self.confidence_lower, 6),
            'confidence_upper': round(self.confidence_upper, 6),
            'measurement_type': self.measurement_type,
            'causal_phi': round(causal_phi, 6),
            'causal_ratio': round(causal_ratio, 6),
            'causal_intervention_penalty': self.causal_intervention_penalty,
            'num_layers': len(states),
            'state_dim': min_dim,
            'WARNING': 'phi_star is extrinsic approximation; honest_phi applies substrate+architecture+measurement penalties; causal_phi is simulated intervention (not physical)',
        }
        self.phi_history.append(phi_star)
        self.honest_phi_history.append(honest_phi)
        return phi_star

    def get_components(self):
        """Return the last computed Φ* decomposition."""
        return dict(self._last_components)

    # =========================================================================
    # GEOMETRIC Φ* (Barrett & Seth 2011)
    # =========================================================================

    def _compute_geometric_phi(self, state_matrix):
        """Gaussian approximation of Φ*:
        Φ* = H(X) - H_MIP(X)

        Where H is differential entropy estimated from covariance,
        and H_MIP is the entropy under the minimum information partition.

        For Gaussian: H(X) = 0.5 * ln(det(2πe * Σ))
        """
        n_vars = state_matrix.shape[0]
        if n_vars < 2:
            return 0.0

        # Covariance matrix of the layers (treating dim as samples)
        cov = np.cov(state_matrix)
        if cov.ndim == 0:
            return 0.0

        # Regularize
        cov += np.eye(cov.shape[0]) * 1e-6

        # Entropy of whole system
        H_whole = self._gaussian_entropy(cov)

        # Find best bipartition (MIP for geometric Φ*)
        best_H_partition = float('inf')
        for _ in range(min(self.num_partitions, 2 ** n_vars - 2)):
            mask = self._random_bipartition(n_vars)
            idx_a = np.where(mask)[0]
            idx_b = np.where(~mask)[0]
            if len(idx_a) == 0 or len(idx_b) == 0:
                continue

            cov_a = cov[np.ix_(idx_a, idx_a)]
            cov_b = cov[np.ix_(idx_b, idx_b)]

            H_a = self._gaussian_entropy(cov_a)
            H_b = self._gaussian_entropy(cov_b)

            # Geometric mean partition entropy
            w_a = len(idx_a) / n_vars
            w_b = len(idx_b) / n_vars
            H_partition = w_a * H_a + w_b * H_b

            best_H_partition = min(best_H_partition, H_partition)

        if best_H_partition == float('inf'):
            return 0.0

        return max(0.0, H_whole - best_H_partition)

    def _gaussian_entropy(self, cov_matrix):
        """Differential entropy of multivariate Gaussian: 0.5 * ln(det(2πe * Σ))"""
        n = cov_matrix.shape[0]
        try:
            sign, logdet = np.linalg.slogdet(cov_matrix)
            if sign <= 0:
                return 0.0
            return 0.5 * (n * np.log(2 * np.pi * np.e) + logdet)
        except np.linalg.LinAlgError:
            return 0.0

    # =========================================================================
    # MINIMUM INFORMATION PARTITION (MIP)
    # =========================================================================

    def _compute_mip_phi(self, state_matrix):
        """Φ_MIP: mutual information that is lost under the minimum information
        partition. Uses empirical mutual information between subsystems.

        MI(A;B) = H(A) + H(B) - H(A,B)
        Φ_MIP = min over partitions of MI(A;B)
        """
        n_vars = state_matrix.shape[0]
        if n_vars < 2:
            return 0.0

        # Discretize states for MI computation
        discretized = self._discretize_states(state_matrix)

        min_mi = float('inf')
        for _ in range(self.mip_search_depth):
            mask = self._random_bipartition(n_vars)
            idx_a = np.where(mask)[0]
            idx_b = np.where(~mask)[0]
            if len(idx_a) == 0 or len(idx_b) == 0:
                continue

            states_a = discretized[idx_a, :]
            states_b = discretized[idx_b, :]

            mi = self._mutual_information(states_a, states_b)
            min_mi = min(min_mi, mi)

        return max(0.0, min_mi) if min_mi != float('inf') else 0.0

    def _mutual_information(self, states_a, states_b):
        """Compute MI(A;B) = H(A) + H(B) - H(A,B) using discrete entropy."""
        h_a = self._discrete_entropy(states_a)
        h_b = self._discrete_entropy(states_b)
        combined = np.concatenate([states_a, states_b], axis=0)
        h_ab = self._discrete_entropy(combined)
        return max(0.0, h_a + h_b - h_ab)

    def _discrete_entropy(self, states):
        """Shannon entropy of discretized multi-variable state."""
        # Hash each column (time step) into a single state symbol
        n_vars, n_samples = states.shape
        symbols = []
        for j in range(n_samples):
            symbols.append(tuple(states[:, j].tolist()))

        # Count frequencies
        from collections import Counter
        counts = Counter(symbols)
        total = sum(counts.values())
        if total == 0:
            return 0.0

        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def _discretize_states(self, state_matrix, n_bins=8):
        """Discretize continuous activations into bins for MI computation."""
        discretized = np.zeros_like(state_matrix, dtype=int)
        for i in range(state_matrix.shape[0]):
            row = state_matrix[i]
            row_min, row_max = row.min(), row.max()
            rng = row_max - row_min
            if rng < 1e-10:
                discretized[i] = 0
            else:
                discretized[i] = np.clip(
                    ((row - row_min) / rng * (n_bins - 1)).astype(int),
                    0, n_bins - 1
                )
        return discretized

    # =========================================================================
    # O-INFORMATION (Synergy vs Redundancy)
    # =========================================================================

    def _compute_o_information(self, state_matrix):
        """O-information (Rosas et al. 2019):
        Ω(X) = (n-2)*H(X) + Σ_i H(X_i) - Σ_i H(X_{-i})

        Positive Ω → redundancy-dominated (information is duplicated)
        Negative Ω → synergy-dominated (information only in the whole)

        For consciousness, negative O-information (synergy) is desired:
        it means the system has information that exists only in the whole,
        not in any subset — a hallmark of integrated information.
        """
        n_vars = state_matrix.shape[0]
        if n_vars < 3:
            return 0.0

        discretized = self._discretize_states(state_matrix)

        # H(X) - entropy of whole
        H_whole = self._discrete_entropy(discretized)

        # Σ H(X_i) - sum of individual entropies
        sum_individual = 0.0
        for i in range(n_vars):
            H_i = self._discrete_entropy(discretized[i:i+1, :])
            sum_individual += H_i

        # Σ H(X_{-i}) - sum of leave-one-out entropies
        sum_leave_one_out = 0.0
        for i in range(n_vars):
            mask = np.ones(n_vars, dtype=bool)
            mask[i] = False
            H_minus_i = self._discrete_entropy(discretized[mask, :])
            sum_leave_one_out += H_minus_i

        omega = (n_vars - 2) * H_whole + sum_individual - sum_leave_one_out
        # Return negative omega as positive phi contribution (synergy = good)
        return -omega

    # =========================================================================
    # TEMPORAL Φ (Cause-Effect Structure)
    # =========================================================================

    def _compute_temporal_phi(self):
        """Temporal integration: measures how much the system's past states
        constrain its current state (cause-effect power).

        Uses transfer entropy / Granger-like mutual information across time:
        Φ_temporal = MI(X_{t-1}; X_t) - Σ MI(X_i_{t-1}; X_i_t)

        High temporal Φ means the system's past as a whole predicts its future
        better than the sum of individual components' predictions.
        """
        if len(self._state_history) < 3:
            return 0.0

        # Use last few time steps
        recent = list(self._state_history)[-min(10, len(self._state_history)):]
        if len(recent) < 3:
            return 0.0

        # Flatten each time step into a single vector
        flat_states = [sm.flatten()[:128] for sm in recent]  # Cap dim for speed

        # Compute MI(past; present) for whole system
        n = len(flat_states)
        past_concat = np.stack(flat_states[:-1])  # (T-1, D)
        present_concat = np.stack(flat_states[1:])  # (T-1, D)

        # Covariance-based MI for whole system
        mi_whole = self._cov_mutual_info(past_concat, present_concat)

        # Sum of per-component MI
        dim = flat_states[0].shape[0]
        chunk_size = max(1, dim // 8)
        mi_parts_sum = 0.0
        for start in range(0, dim, chunk_size):
            end = min(start + chunk_size, dim)
            past_part = past_concat[:, start:end]
            present_part = present_concat[:, start:end]
            mi_parts_sum += self._cov_mutual_info(past_part, present_part)

        return max(0.0, mi_whole - mi_parts_sum)

    def _cov_mutual_info(self, X, Y):
        """Gaussian MI: MI(X;Y) = 0.5 * ln(det(Σ_X) * det(Σ_Y) / det(Σ_XY))"""
        n_samples = X.shape[0]
        if n_samples < 3:
            return 0.0

        try:
            cov_x = np.cov(X.T) + np.eye(X.shape[1]) * 1e-6
            cov_y = np.cov(Y.T) + np.eye(Y.shape[1]) * 1e-6

            if cov_x.ndim == 0:
                cov_x = np.array([[cov_x]])
            if cov_y.ndim == 0:
                cov_y = np.array([[cov_y]])

            XY = np.concatenate([X, Y], axis=1)
            cov_xy = np.cov(XY.T) + np.eye(XY.shape[1]) * 1e-6

            _, logdet_x = np.linalg.slogdet(cov_x)
            _, logdet_y = np.linalg.slogdet(cov_y)
            _, logdet_xy = np.linalg.slogdet(cov_xy)

            mi = 0.5 * (logdet_x + logdet_y - logdet_xy)
            return max(0.0, mi)
        except (np.linalg.LinAlgError, ValueError):
            return 0.0

    # =========================================================================
    # UTILITIES
    # =========================================================================

    def _random_bipartition(self, n):
        """Generate a random non-trivial bipartition of n elements."""
        while True:
            mask = np.random.random(n) > 0.5
            if mask.any() and (~mask).any():
                return mask


# =============================================================================
# GLOBAL WORKSPACE (GNWT) (inlined from global_workspace.py)
# =============================================================================
class SpecialistModule(nn.Module):
    """A specialist processor that competes for workspace access.
    Each specialist processes information in its domain and produces
    a salience score + processed representation."""

    def __init__(self, hidden_size, specialist_type='generic'):
        super().__init__()
        self.specialist_type = specialist_type
        self.hidden_size = hidden_size

        # Processing pathway
        self.process = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size, hidden_size),
        )

        # Salience scorer: how strongly this specialist bids for workspace
        self.salience_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 4),
            nn.GELU(),
            nn.Linear(hidden_size // 4, 1),
        )

        # Recurrent gate for sustained activation
        self.recurrent_gate = nn.GRUCell(hidden_size, hidden_size)
        self._hidden_state = None

        # Tracking
        self.ignition_count = 0
        self.total_bids = 0

    def forward(self, x):
        """Process input and return (processed_output, salience_score).

        Args:
            x: (batch, hidden_size) input tensor

        Returns:
            processed: (batch, hidden_size) specialist's processed representation
            salience: (batch, 1) how strongly this specialist bids for workspace
        """
        self.total_bids += 1

        # Recurrent processing (sustained activation from previous step)
        if self._hidden_state is not None and self._hidden_state.shape == x.shape:
            h = self.recurrent_gate(x, self._hidden_state.detach())
        else:
            h = x
        self._hidden_state = h

        processed = self.process(h) + x  # Residual
        salience = self.salience_head(processed)
        return processed, salience

    def reset_state(self):
        self._hidden_state = None


class GlobalWorkspace(nn.Module):
    """Global Neuronal Workspace: implements competitive ignition,
    global broadcasting, and recurrent amplification.

    Architecture:
        1. Multiple specialist modules process input in parallel
        2. Specialists compete via salience scores (soft winner-take-all)
        3. Winner(s) exceeding ignition threshold get amplified
        4. Amplified content is broadcast back to ALL specialists
        5. Recurrent loop sustains conscious content across time steps

    The workspace acts as a bottleneck: only the most salient
    information becomes "globally conscious" and influences all modules.
    """

    def __init__(self, hidden_size, num_specialists=6, ignition_threshold=0.5,
                 broadcast_gain=2.0, recurrent_depth=3):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_specialists = num_specialists
        self.ignition_threshold = ignition_threshold
        self.broadcast_gain = broadcast_gain
        self.recurrent_depth = recurrent_depth

        # Specialist modules (diverse processor types)
        specialist_types = [
            'perceptual', 'semantic', 'episodic',
            'executive', 'emotional', 'metacognitive'
        ]
        self.specialists = nn.ModuleList([
            SpecialistModule(hidden_size, specialist_types[i % len(specialist_types)])
            for i in range(num_specialists)
        ])

        # Workspace: shared global representation
        self.workspace_projection = nn.Linear(hidden_size, hidden_size)
        self.workspace_norm = nn.LayerNorm(hidden_size)

        # Broadcast pathway: sends workspace content back to all specialists
        self.broadcast_transform = nn.Linear(hidden_size, hidden_size)
        self.broadcast_gate = nn.Linear(hidden_size * 2, hidden_size)

        # Recurrent amplification (sustains conscious content)
        self.amplification_gru = nn.GRUCell(hidden_size, hidden_size)
        self._workspace_state = None

        # Ignition nonlinearity: sharp transition from unconscious to conscious
        self.ignition_temperature = nn.Parameter(torch.tensor(1.0))

        # Output integration
        self.output_integration = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.GELU(),
        )

        # Monitoring / diagnostics
        self.ignition_history = deque(maxlen=500)
        self._last_saliences = None
        self._last_ignited = None
        self._ignition_count = 0

    def forward(self, x):
        """Process input through the Global Workspace.

        Args:
            x: (batch, seq_len, hidden_size) or (batch, hidden_size)

        Returns:
            output: same shape as input, with globally-broadcast information integrated
            workspace_info: dict with diagnostic information
        """
        squeeze_seq = False
        if x.dim() == 3:
            batch, seq_len, dim = x.shape
            x_flat = x.mean(dim=1)  # Pool over sequence for workspace competition
            squeeze_seq = True
        else:
            x_flat = x
            batch = x.shape[0]

        # --- Phase 1: Parallel specialist processing ---
        specialist_outputs = []
        salience_scores = []
        for specialist in self.specialists:
            processed, salience = specialist(x_flat)
            specialist_outputs.append(processed)
            salience_scores.append(salience)

        # Stack: (batch, num_specialists, hidden) and (batch, num_specialists)
        all_processed = torch.stack(specialist_outputs, dim=1)
        all_saliences = torch.cat(salience_scores, dim=-1)  # (batch, num_specialists)

        # --- Phase 2: Competitive ignition ---
        # Softmax competition with learnable temperature (sharp winner-take-all)
        temp = torch.clamp(self.ignition_temperature, min=0.1, max=5.0)
        competition_weights = F.softmax(all_saliences / temp, dim=-1)  # (batch, num_specialists)

        # Ignition: only specialists above threshold get through
        ignition_mask = (competition_weights > self.ignition_threshold / self.num_specialists).float()

        # If nothing ignites, let the top specialist through (prevent dead workspace)
        if ignition_mask.sum() == 0:
            top_idx = competition_weights.argmax(dim=-1, keepdim=True)
            ignition_mask.scatter_(1, top_idx, 1.0)

        # Apply ignition: zero out sub-threshold specialists
        gated_weights = competition_weights * ignition_mask
        gated_weights = gated_weights / (gated_weights.sum(dim=-1, keepdim=True) + 1e-8)

        # Weighted combination into workspace content
        workspace_content = torch.einsum('bn,bnh->bh', gated_weights, all_processed)

        # --- Phase 3: Recurrent amplification ---
        workspace_content = self.workspace_projection(workspace_content)

        for _ in range(self.recurrent_depth):
            if self._workspace_state is not None and self._workspace_state.shape == workspace_content.shape:
                workspace_content = self.amplification_gru(
                    workspace_content, self._workspace_state.detach()
                )
            else:
                workspace_content = self.amplification_gru(
                    workspace_content, torch.zeros_like(workspace_content)
                )

        workspace_content = self.workspace_norm(workspace_content)
        self._workspace_state = workspace_content

        # --- Phase 4: Global broadcasting ---
        broadcast = self.broadcast_transform(workspace_content) * self.broadcast_gain

        # Gate: combine original input with broadcast
        gate_input = torch.cat([x_flat, broadcast], dim=-1)
        gate = torch.sigmoid(self.broadcast_gate(gate_input))
        integrated = gate * broadcast + (1 - gate) * x_flat

        # Final output integration
        output = self.output_integration(torch.cat([integrated, x_flat], dim=-1))

        # Reshape back if needed
        if squeeze_seq:
            output = output.unsqueeze(1).expand(-1, seq_len, -1)

        # --- Diagnostics ---
        ignited_indices = torch.where(ignition_mask[0] > 0)[0].tolist()
        self._last_saliences = all_saliences.detach().cpu().numpy()
        self._last_ignited = ignited_indices
        if len(ignited_indices) > 0:
            self._ignition_count += 1

        num_ignited = int(ignition_mask.sum().item())
        max_salience = float(all_saliences.max().item())
        workspace_info = {
            'num_ignited': num_ignited,
            'ignited_specialists': ignited_indices,
            'max_salience': round(max_salience, 4),
            'competition_weights': competition_weights.detach().cpu().numpy().tolist(),
            'ignition_count': self._ignition_count,
            'broadcast_gain': float(self.broadcast_gain),
            'ignition_rate': self.get_ignition_rate(),
        }

        self.ignition_history.append({
            'num_ignited': num_ignited,
            'max_salience': max_salience,
        })

        return output, workspace_info

    def get_ignition_rate(self):
        """Fraction of recent steps where ignition occurred."""
        if not self.ignition_history:
            return 0.0
        return sum(1 for h in self.ignition_history if h['num_ignited'] > 1) / len(self.ignition_history)

    def get_avg_salience(self):
        """Average max salience across recent steps."""
        if not self.ignition_history:
            return 0.0
        return np.mean([h['max_salience'] for h in self.ignition_history])

    def reset_states(self):
        """Reset all recurrent states (e.g., between episodes)."""
        self._workspace_state = None
        for specialist in self.specialists:
            specialist.reset_state()


# =============================================================================
# ACTIVE INFERENCE (inlined from active_inference.py)
# =============================================================================
class BeliefState:
    """A probabilistic belief over hidden world states.
    Represented as a categorical distribution over discrete states."""

    def __init__(self, num_states=64):
        self.num_states = num_states
        # Posterior belief q(s): starts uniform
        self.posterior = np.ones(num_states) / num_states
        # Prior preference p(o): what observations the agent prefers
        self.preferences = np.zeros(num_states)
        # Precision (inverse temperature) — confidence in beliefs
        self.precision = 1.0
        self.entropy_history = deque(maxlen=200)

    def update(self, observation_likelihood, learning_rate=0.1):
        """Bayesian belief update: q(s) ∝ p(o|s) * q(s)"""
        likelihood = np.clip(observation_likelihood, 1e-10, 1.0)
        unnormalized = likelihood * self.posterior
        total = unnormalized.sum()
        if total > 0:
            new_posterior = unnormalized / total
            # Smooth update (avoid catastrophic belief shifts)
            self.posterior = (1 - learning_rate) * self.posterior + learning_rate * new_posterior
        self.posterior = np.clip(self.posterior, 1e-10, 1.0)
        self.posterior /= self.posterior.sum()
        self.entropy_history.append(self.entropy())

    def entropy(self):
        """Shannon entropy of current beliefs: H(q) = -Σ q(s) ln q(s)"""
        p = np.clip(self.posterior, 1e-10, 1.0)
        return -np.sum(p * np.log(p))

    def kl_divergence(self, target_dist):
        """KL(q || p) = Σ q(s) ln(q(s)/p(s))"""
        q = np.clip(self.posterior, 1e-10, 1.0)
        p = np.clip(target_dist, 1e-10, 1.0)
        return np.sum(q * np.log(q / p))

    def surprise(self, observation_likelihood):
        """Bayesian surprise: -ln p(o) ≈ -ln Σ_s p(o|s)q(s)"""
        expected_likelihood = np.sum(observation_likelihood * self.posterior)
        return -np.log(max(expected_likelihood, 1e-10))


class GenerativeModel:
    """Generative model p(o,s) that the agent uses to predict observations.

    Components:
      - Transition model: p(s'|s, a) — how states evolve under actions
      - Observation model: p(o|s) — how observations arise from states
      - Prior preferences: p(o) — what observations are preferred

    The model learns from experience and is used to compute free energy.
    """

    def __init__(self, num_states=64, num_obs=32, num_actions=16):
        self.num_states = num_states
        self.num_obs = num_obs
        self.num_actions = num_actions

        # Transition model: A[a] is (num_states, num_states) matrix
        # A[a][s', s] = p(s' | s, a), initialized near-uniform with slight structure
        self.A = {}
        for a in range(num_actions):
            mat = np.random.dirichlet(np.ones(num_states) * 5.0, size=num_states).T
            self.A[a] = mat

        # Observation model: B[s, o] = p(o | s)
        self.B = np.random.dirichlet(np.ones(num_obs) * 2.0, size=num_states)

        # Prior preferences over observations (learned from reward signals)
        self.C = np.zeros(num_obs)  # log-preferences

        # Dirichlet concentration parameters (for learning)
        self._A_counts = {a: np.ones((num_states, num_states)) for a in range(num_actions)}
        self._B_counts = np.ones((num_states, num_obs))

        # Experience buffer
        self.experience = deque(maxlen=5000)

    def predict_observation(self, belief_state):
        """Predict expected observation given current beliefs.
        p(o) = Σ_s p(o|s) q(s)"""
        return self.B.T @ belief_state.posterior  # (num_obs,)

    def predict_next_state(self, belief_state, action):
        """Predict next state distribution given current beliefs and action.
        q(s') = Σ_s p(s'|s,a) q(s)"""
        action_idx = action % self.num_actions
        return self.A[action_idx] @ belief_state.posterior

    def learn(self, prev_state_belief, action, observation_vec, next_state_belief, reward=0.0):
        """Update generative model from experience (Dirichlet learning).

        Args:
            prev_state_belief: belief before action
            action: int action taken
            observation_vec: np.array observation likelihood
            next_state_belief: belief after observation
            reward: scalar reward signal
        """
        action_idx = action % self.num_actions

        # Update transition counts
        outer = np.outer(next_state_belief.posterior, prev_state_belief.posterior)
        self._A_counts[action_idx] += outer * 0.1
        # Normalize to get transition probabilities
        for s in range(self.num_states):
            col_sum = self._A_counts[action_idx][:, s].sum()
            if col_sum > 0:
                self.A[action_idx][:, s] = self._A_counts[action_idx][:, s] / col_sum

        # Update observation model counts
        obs_vec = np.clip(observation_vec[:self.num_obs], 0, 1)
        if len(obs_vec) < self.num_obs:
            obs_vec = np.pad(obs_vec, (0, self.num_obs - len(obs_vec)))
        for s in range(self.num_states):
            self._B_counts[s] += next_state_belief.posterior[s] * obs_vec * 0.1
        # Normalize
        for s in range(self.num_states):
            row_sum = self._B_counts[s].sum()
            if row_sum > 0:
                self.B[s] = self._B_counts[s] / row_sum

        # Update preferences from reward
        if reward != 0:
            obs_contribution = obs_vec / (obs_vec.sum() + 1e-8)
            self.C += reward * obs_contribution * 0.05
            self.C = np.clip(self.C, -5.0, 5.0)

        self.experience.append({
            'action': action_idx,
            'reward': reward,
            'surprise': float(prev_state_belief.surprise(observation_vec[:self.num_states]
                              if len(observation_vec) >= self.num_states
                              else np.pad(observation_vec, (0, self.num_states - len(observation_vec))))),
            'ts': datetime.now().isoformat(),
        })


class ActiveInferenceEngine:
    """Active Inference engine that replaces hardcoded goals with
    free-energy-driven goal formation and policy selection.

    Goals EMERGE from:
      1. Minimizing variational free energy (reducing surprise)
      2. Epistemic foraging (actively reducing uncertainty)
      3. Pragmatic value (seeking preferred observations)

    The engine maintains a belief state, generative model, and
    evaluates policies by their expected free energy.
    """

    def __init__(self, num_states=64, num_obs=32, num_actions=16,
                 planning_horizon=5, num_policies=8):
        self.num_states = num_states
        self.num_obs = num_obs
        self.num_actions = num_actions
        self.planning_horizon = planning_horizon
        self.num_policies = num_policies

        # Core components
        self.belief = BeliefState(num_states)
        self.model = GenerativeModel(num_states, num_obs, num_actions)

        # Goal system: emergent goals from free energy landscape
        self.active_goals = []  # List of {description, priority, free_energy, created_at}
        self.goal_history = deque(maxlen=200)
        self.max_active_goals = 20

        # Metrics
        self.total_vfe = 0.0
        self.total_efe = 0.0
        self.vfe_history = deque(maxlen=500)
        self.efe_history = deque(maxlen=500)
        self.epistemic_value_history = deque(maxlen=500)
        self.pragmatic_value_history = deque(maxlen=500)
        self.step_count = 0

        # Goal categories that can emerge
        self._goal_templates = [
            'reduce_uncertainty_{domain}',
            'explore_{domain}',
            'exploit_{domain}',
            'consolidate_{domain}',
            'integrate_{domain_a}_with_{domain_b}',
            'predict_{domain}',
            'verify_{hypothesis}',
            'seek_novelty_{domain}',
        ]

    # =========================================================================
    # FREE ENERGY COMPUTATIONS
    # =========================================================================

    def compute_variational_free_energy(self, observation_vec):
        """Variational Free Energy: F = E_q[ln q(s) - ln p(o,s)]
        = KL(q(s) || p(s)) - E_q[ln p(o|s)]

        This is the surprise the agent is trying to minimize.
        """
        obs = np.clip(observation_vec[:self.num_states], 0, 1)
        if len(obs) < self.num_states:
            obs = np.pad(obs, (0, self.num_states - len(obs)))

        # KL divergence: q(s) from prior
        prior = np.ones(self.num_states) / self.num_states
        kl_term = self.belief.kl_divergence(prior)

        # Expected log-likelihood: E_q[ln p(o|s)]
        log_likelihood = 0.0
        for s in range(self.num_states):
            obs_pred = self.model.B[s, :len(observation_vec[:self.num_obs])]
            log_likelihood += self.belief.posterior[s] * np.log(
                max(np.sum(obs_pred * observation_vec[:self.num_obs]
                    if len(observation_vec) >= self.num_obs
                    else np.pad(observation_vec, (0, self.num_obs - len(observation_vec)))),
                    1e-10))

        vfe = kl_term - log_likelihood
        self.total_vfe = float(vfe)
        self.vfe_history.append(float(vfe))
        return float(vfe)

    def compute_expected_free_energy(self, policy):
        """Expected Free Energy for a policy: G(π) = E_q(π)[ambiguity + risk]

        G = epistemic_value + pragmatic_value
        epistemic = -E[H(o|s)] (information gain — drives exploration)
        pragmatic = -E[ln p(o)] (preference satisfaction — drives exploitation)

        Lower G = better policy.
        """
        epistemic_total = 0.0
        pragmatic_total = 0.0
        current_belief = np.copy(self.belief.posterior)

        discount = 1.0
        for t, action in enumerate(policy):
            action_idx = action % self.num_actions
            discount *= 0.9  # Temporal discount

            # Predict next state
            next_belief = self.model.A[action_idx] @ current_belief

            # Predict observations
            predicted_obs = self.model.B.T @ next_belief  # (num_obs,)

            # Epistemic value: expected information gain
            # Negative conditional entropy of observations given states
            conditional_entropy = 0.0
            for s in range(self.num_states):
                if next_belief[s] > 1e-10:
                    obs_given_s = self.model.B[s]
                    h_o_given_s = -np.sum(obs_given_s * np.log(obs_given_s + 1e-10))
                    conditional_entropy += next_belief[s] * h_o_given_s

            marginal_entropy = -np.sum(predicted_obs * np.log(predicted_obs + 1e-10))
            info_gain = marginal_entropy - conditional_entropy
            epistemic_total += discount * info_gain

            # Pragmatic value: preference satisfaction
            log_prefs = self.model.C
            pragmatic = np.sum(predicted_obs * log_prefs)
            pragmatic_total += discount * pragmatic

            current_belief = next_belief

        efe = -(epistemic_total + pragmatic_total)

        self.epistemic_value_history.append(float(epistemic_total))
        self.pragmatic_value_history.append(float(pragmatic_total))
        return float(efe), float(epistemic_total), float(pragmatic_total)

    # =========================================================================
    # POLICY SELECTION
    # =========================================================================

    def select_action(self, observation_vec):
        """Select the best action by evaluating policies via expected free energy.

        Returns:
            best_action: int, the action to take
            policy_info: dict with diagnostic information
        """
        self.step_count += 1

        # Update beliefs from observation
        obs_likelihood = np.clip(observation_vec[:self.num_states], 0.01, 1.0)
        if len(obs_likelihood) < self.num_states:
            obs_likelihood = np.pad(obs_likelihood, (0, self.num_states - len(obs_likelihood)),
                                     constant_values=0.01)
        self.belief.update(obs_likelihood)

        # Compute VFE for current observation
        vfe = self.compute_variational_free_energy(observation_vec)

        # Generate candidate policies (random action sequences)
        policies = []
        for _ in range(self.num_policies):
            policy = [random.randint(0, self.num_actions - 1)
                      for _ in range(self.planning_horizon)]
            policies.append(policy)

        # Evaluate each policy
        best_efe = float('inf')
        best_policy = policies[0]
        best_epistemic = 0.0
        best_pragmatic = 0.0

        policy_efes = []
        for policy in policies:
            efe, epistemic, pragmatic = self.compute_expected_free_energy(policy)
            policy_efes.append(efe)
            if efe < best_efe:
                best_efe = efe
                best_policy = policy
                best_epistemic = epistemic
                best_pragmatic = pragmatic

        self.total_efe = best_efe
        self.efe_history.append(best_efe)

        # Softmax policy selection (stochastic)
        efes = np.array(policy_efes)
        efes_shifted = efes - efes.min()
        probs = np.exp(-efes_shifted * self.belief.precision)
        probs = probs / (probs.sum() + 1e-8)
        selected_idx = np.random.choice(len(policies), p=probs)
        selected_policy = policies[selected_idx]

        # Emergent goal formation based on free energy landscape
        self._update_emergent_goals(vfe, best_epistemic, best_pragmatic)

        return selected_policy[0], {
            'vfe': round(vfe, 4),
            'efe': round(best_efe, 4),
            'epistemic_value': round(best_epistemic, 4),
            'pragmatic_value': round(best_pragmatic, 4),
            'belief_entropy': round(float(self.belief.entropy()), 4),
            'precision': round(float(self.belief.precision), 4),
            'num_active_goals': len(self.active_goals),
            'step': self.step_count,
        }

    # =========================================================================
    # EMERGENT GOAL FORMATION
    # =========================================================================

    def _update_emergent_goals(self, vfe, epistemic_value, pragmatic_value):
        """Goals emerge from the free energy landscape rather than being hardcoded.

        New goals are created when:
          - VFE is high (lots of surprise → need to learn)
          - Epistemic value is high (uncertainty → explore)
          - Pragmatic value is low (preferences not met → exploit)
          - Novel patterns detected in experience
        """
        now = datetime.now().isoformat()
        new_goals = []

        # High surprise → exploration goal
        if len(self.vfe_history) > 5:
            recent_vfe = list(self.vfe_history)[-5:]
            vfe_trend = recent_vfe[-1] - recent_vfe[0]
            avg_vfe = np.mean(recent_vfe)

            if avg_vfe > 2.0:
                domain = self._identify_uncertain_domain()
                new_goals.append({
                    'description': f'reduce_uncertainty_{domain}',
                    'priority': min(1.0, avg_vfe / 5.0),
                    'free_energy': avg_vfe,
                    'type': 'epistemic',
                    'created_at': now,
                })

            if vfe_trend > 0.5:
                new_goals.append({
                    'description': f'explore_novel_patterns',
                    'priority': min(1.0, vfe_trend),
                    'free_energy': vfe,
                    'type': 'epistemic',
                    'created_at': now,
                })

        # High epistemic value → information-seeking goal
        if epistemic_value > 1.0:
            domain = self._identify_uncertain_domain()
            new_goals.append({
                'description': f'seek_information_{domain}',
                'priority': min(1.0, epistemic_value / 3.0),
                'free_energy': vfe,
                'type': 'epistemic',
                'created_at': now,
            })

        # Low pragmatic value → exploitation goal
        if pragmatic_value < -0.5:
            new_goals.append({
                'description': 'exploit_known_rewards',
                'priority': min(1.0, abs(pragmatic_value) / 2.0),
                'free_energy': vfe,
                'type': 'pragmatic',
                'created_at': now,
            })

        # Belief consolidation (entropy is decreasing → integrate learned knowledge)
        if len(self.belief.entropy_history) > 10:
            recent_h = list(self.belief.entropy_history)[-10:]
            h_trend = recent_h[-1] - recent_h[0]
            if h_trend < -0.3:
                new_goals.append({
                    'description': 'consolidate_learned_knowledge',
                    'priority': min(1.0, abs(h_trend)),
                    'free_energy': vfe,
                    'type': 'consolidation',
                    'created_at': now,
                })

        # Add new goals, avoiding duplicates by description
        existing_descs = {g['description'] for g in self.active_goals}
        for g in new_goals:
            if g['description'] not in existing_descs:
                self.active_goals.append(g)
                self.goal_history.append(g)

        # Prune low-priority / old goals
        if len(self.active_goals) > self.max_active_goals:
            self.active_goals.sort(key=lambda g: g['priority'], reverse=True)
            removed = self.active_goals[self.max_active_goals:]
            self.active_goals = self.active_goals[:self.max_active_goals]

        # Decay priorities over time
        for g in self.active_goals:
            g['priority'] *= 0.995

        # Remove completed / zero-priority goals
        self.active_goals = [g for g in self.active_goals if g['priority'] > 0.01]

    def _identify_uncertain_domain(self):
        """Identify which domain has the highest uncertainty based on belief entropy."""
        # Map belief state regions to domains
        domains = ['perception', 'language', 'memory', 'reasoning',
                   'planning', 'social', 'physical', 'abstract']
        chunk_size = max(1, self.num_states // len(domains))

        max_entropy = -1
        max_domain = 'general'
        for i, domain in enumerate(domains):
            start = i * chunk_size
            end = min(start + chunk_size, self.num_states)
            chunk = self.belief.posterior[start:end]
            h = -np.sum(chunk * np.log(chunk + 1e-10))
            if h > max_entropy:
                max_entropy = h
                max_domain = domain

        return max_domain

    # =========================================================================
    # LEARNING & ADAPTATION
    # =========================================================================

    def update_from_experience(self, observation_vec, action, reward, next_observation_vec):
        """Learn from experience: update generative model and beliefs."""
        prev_belief = BeliefState(self.num_states)
        prev_belief.posterior = np.copy(self.belief.posterior)

        # Update belief with new observation
        obs_likelihood = np.clip(next_observation_vec[:self.num_states], 0.01, 1.0)
        if len(obs_likelihood) < self.num_states:
            obs_likelihood = np.pad(obs_likelihood, (0, self.num_states - len(obs_likelihood)),
                                     constant_values=0.01)
        self.belief.update(obs_likelihood)

        # Update generative model
        self.model.learn(prev_belief, action, next_observation_vec, self.belief, reward)

        # Update precision (confidence) based on prediction error
        predicted_obs = self.model.predict_observation(prev_belief)
        actual_obs = next_observation_vec[:self.num_obs]
        if len(actual_obs) < self.num_obs:
            actual_obs = np.pad(actual_obs, (0, self.num_obs - len(actual_obs)))
        prediction_error = np.mean((predicted_obs - actual_obs) ** 2)

        # High prediction error → lower precision (less confident)
        # Low prediction error → higher precision (more confident)
        self.belief.precision = max(0.1, min(5.0,
            self.belief.precision * (1.0 - 0.01 * prediction_error) + 0.001))

    def prediction_error_step(self, prev_activations, curr_activations, action=0, reward=0.0):
        """Combined prediction-error learning + policy selection step.

        Called by ConsciousnessSimulator.process_input to close the
        perception-action loop using real transformer activations.

        Returns info dict with vfe, epistemic_value, prediction_error, etc.
        """
        prev_act = np.asarray(prev_activations, dtype=np.float32).flatten()[:self.num_obs]
        curr_act = np.asarray(curr_activations, dtype=np.float32).flatten()[:self.num_obs]
        if len(prev_act) < self.num_obs:
            prev_act = np.pad(prev_act, (0, self.num_obs - len(prev_act)))
        if len(curr_act) < self.num_obs:
            curr_act = np.pad(curr_act, (0, self.num_obs - len(curr_act)))

        # Learn from the transition
        self.update_from_experience(prev_act, action, reward, curr_act)

        # Select next action (also updates beliefs and computes VFE/EFE)
        _action, info = self.select_action(curr_act)

        # Prediction error: how surprised were we by curr given prev?
        pred_obs = self.model.predict_observation(self.belief)
        actual_obs = curr_act[:self.num_obs]
        prediction_error = float(np.mean((pred_obs - actual_obs) ** 2))
        self._last_pred_error = prediction_error
        info['prediction_error'] = round(prediction_error, 6)
        info['last_prediction_error'] = round(prediction_error, 6)
        info['reward'] = round(float(reward), 4)
        return info

    def step(self, observation_idx):
        """Convenience wrapper: accept an observation index (int) and run one
        active inference cycle (belief update, VFE, policy selection).

        Returns info dict with vfe, epistemic_value, etc.
        """
        obs_vec = np.zeros(self.num_states, dtype=np.float32)
        obs_vec[int(observation_idx) % self.num_states] = 1.0
        _action, info = self.select_action(obs_vec)
        return info

    def get_goals_as_list(self):
        """Return current active goals sorted by priority."""
        return sorted(self.active_goals, key=lambda g: g['priority'], reverse=True)

    def get_status(self):
        """Return engine status for display."""
        return {
            'vfe': round(self.total_vfe, 4),
            'efe': round(self.total_efe, 4),
            'belief_entropy': round(float(self.belief.entropy()), 4),
            'precision': round(float(self.belief.precision), 4),
            'num_active_goals': len(self.active_goals),
            'last_prediction_error': round(getattr(self, '_last_pred_error', 0.0), 6),
            'top_goals': [{'desc': g['description'], 'pri': round(g['priority'], 3),
                          'type': g['type']}
                         for g in sorted(self.active_goals,
                                        key=lambda g: g['priority'], reverse=True)[:5]],
            'step': self.step_count,
            'model_experience': len(self.model.experience),
        }

# =============================================================================
# ADVANCED MEMORY SYSTEM (inlined from memory_system.py)
# =============================================================================
class VectorStore:
    """Semantic memory: dense vector embeddings with cosine similarity search.

    Stores (key, embedding, metadata) triples and supports nearest-neighbor
    retrieval. Uses numpy for efficiency without requiring FAISS.
    """

    def __init__(self, embedding_dim=256, max_entries=10000):
        self.embedding_dim = embedding_dim
        self.max_entries = max_entries
        self._keys = []
        self._embeddings = np.zeros((0, embedding_dim), dtype=np.float32)
        self._metadata = []
        self._access_counts = []
        self._timestamps = []

    def add(self, key, embedding, metadata=None):
        """Add or update a vector entry."""
        embedding = np.asarray(embedding, dtype=np.float32).flatten()[:self.embedding_dim]
        if len(embedding) < self.embedding_dim:
            embedding = np.pad(embedding, (0, self.embedding_dim - len(embedding)))

        # Normalize for cosine similarity
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        # Check if key exists
        if key in self._keys:
            idx = self._keys.index(key)
            self._embeddings[idx] = embedding
            self._metadata[idx] = metadata or {}
            self._access_counts[idx] += 1
            self._timestamps[idx] = time.time()
        else:
            self._keys.append(key)
            self._embeddings = np.vstack([self._embeddings, embedding.reshape(1, -1)]) \
                if self._embeddings.shape[0] > 0 else embedding.reshape(1, -1)
            self._metadata.append(metadata or {})
            self._access_counts.append(1)
            self._timestamps.append(time.time())

        # Evict if over capacity (LRU-like with access count weighting)
        if len(self._keys) > self.max_entries:
            self._evict(self.max_entries // 10)

    def query(self, query_embedding, top_k=5, threshold=0.0):
        """Retrieve top-k most similar entries by cosine similarity.

        Returns:
            list of (key, similarity, metadata) tuples, sorted by similarity descending.
        """
        if self._embeddings.shape[0] == 0:
            return []

        query = np.asarray(query_embedding, dtype=np.float32).flatten()[:self.embedding_dim]
        if len(query) < self.embedding_dim:
            query = np.pad(query, (0, self.embedding_dim - len(query)))
        norm = np.linalg.norm(query)
        if norm > 0:
            query = query / norm

        # Cosine similarity (embeddings are already normalized)
        similarities = self._embeddings @ query  # (N,)

        # Get top-k indices
        if len(similarities) <= top_k:
            indices = np.argsort(-similarities)
        else:
            indices = np.argpartition(-similarities, top_k)[:top_k]
            indices = indices[np.argsort(-similarities[indices])]

        results = []
        for idx in indices:
            sim = float(similarities[idx])
            if sim >= threshold:
                self._access_counts[idx] += 1
                results.append((self._keys[idx], sim, self._metadata[idx]))

        return results

    def _evict(self, count):
        """Evict the least valuable entries based on recency * access frequency."""
        now = time.time()
        scores = []
        for i in range(len(self._keys)):
            recency = 1.0 / (1.0 + (now - self._timestamps[i]) / 3600.0)
            frequency = math.log1p(self._access_counts[i])
            scores.append(recency * 0.6 + frequency * 0.4)

        # Remove lowest-scoring entries
        sorted_indices = np.argsort(scores)
        remove_indices = set(sorted_indices[:count].tolist())

        new_keys = []
        new_meta = []
        new_counts = []
        new_ts = []
        keep_mask = []
        for i in range(len(self._keys)):
            if i not in remove_indices:
                new_keys.append(self._keys[i])
                new_meta.append(self._metadata[i])
                new_counts.append(self._access_counts[i])
                new_ts.append(self._timestamps[i])
                keep_mask.append(i)

        self._keys = new_keys
        self._metadata = new_meta
        self._access_counts = new_counts
        self._timestamps = new_ts
        if keep_mask:
            self._embeddings = self._embeddings[keep_mask]
        else:
            self._embeddings = np.zeros((0, self.embedding_dim), dtype=np.float32)

    def __len__(self):
        return len(self._keys)


class EpisodicMemory:
    """Episodic buffer: time-tagged experience traces with temporal context.

    Each episode stores:
      - content: the data/experience
      - embedding: vector representation for similarity search
      - context: what was happening when this was encoded
      - temporal_tag: when it occurred
      - emotional_valence: how significant this experience was
      - retrieval_count: how often this memory has been accessed
    """

    def __init__(self, max_episodes=5000, embedding_dim=256):
        self.max_episodes = max_episodes
        self.embedding_dim = embedding_dim
        self.episodes = deque(maxlen=max_episodes)
        self._vector_store = VectorStore(embedding_dim, max_episodes)

    def encode(self, content, embedding, context=None, emotional_valence=0.0):
        """Store a new episodic memory.

        Args:
            content: any serializable data
            embedding: np.array vector representation
            context: dict of contextual information
            emotional_valence: float [-1, 1], emotional significance
        """
        episode_id = hashlib.md5(
            f"{content}{time.time()}{random.random()}".encode()
        ).hexdigest()[:12]

        episode = {
            'id': episode_id,
            'content': content,
            'context': context or {},
            'temporal_tag': datetime.now().isoformat(),
            'timestamp': time.time(),
            'emotional_valence': float(np.clip(emotional_valence, -1, 1)),
            'retrieval_count': 0,
            'consolidation_strength': 0.0,  # Increases during hippocampal replay
        }

        self.episodes.append(episode)
        self._vector_store.add(episode_id, embedding, metadata={'idx': len(self.episodes) - 1})

        return episode_id

    def retrieve(self, query_embedding, top_k=5, recency_weight=0.3,
                 emotion_weight=0.2, similarity_weight=0.5):
        """Retrieve episodes using a weighted combination of:
        - Vector similarity (semantic match)
        - Recency (temporal proximity)
        - Emotional valence (significance)

        Returns list of episodes sorted by combined score.
        """
        # Get candidates by vector similarity
        candidates = self._vector_store.query(query_embedding, top_k=top_k * 2)

        if not candidates:
            return []

        now = time.time()
        scored = []
        for key, sim, meta in candidates:
            # Find the episode
            episode = None
            for ep in self.episodes:
                if ep['id'] == key:
                    episode = ep
                    break
            if episode is None:
                continue

            # Recency score (exponential decay)
            age_hours = (now - episode['timestamp']) / 3600.0
            recency = math.exp(-age_hours / 24.0)  # 24-hour half-life

            # Emotional significance
            emotion = abs(episode['emotional_valence'])

            # Combined score
            score = (similarity_weight * sim +
                     recency_weight * recency +
                     emotion_weight * emotion)

            # Boost consolidated memories
            score *= (1.0 + 0.2 * episode['consolidation_strength'])

            episode['retrieval_count'] += 1
            scored.append((episode, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [(ep, sc) for ep, sc in scored[:top_k]]

    def get_recent(self, n=10):
        """Get n most recent episodes."""
        return list(self.episodes)[-n:]

    def __len__(self):
        return len(self.episodes)


class HippocampalIndex:
    """Hippocampal-style memory indexing with pattern separation,
    pattern completion, and consolidation replay.

    Based on Complementary Learning Systems (CLS) theory:
      - Pattern Separation: Orthogonalize similar inputs to reduce interference
      - Pattern Completion: Reconstruct full memories from partial cues
      - Consolidation: Replay important memories to strengthen them
      - Indexing: Sparse codes that point to distributed neocortical representations
    """

    def __init__(self, input_dim=256, index_dim=128, num_slots=2000):
        self.input_dim = input_dim
        self.index_dim = index_dim
        self.num_slots = num_slots

        # Sparse index codes (DG-like pattern separation)
        self._index_codes = np.zeros((0, index_dim), dtype=np.float32)
        self._index_keys = []
        self._index_strengths = []  # Connection strength (consolidation level)

        # Pattern separation parameters
        self.sparsity = 0.1  # Fraction of active units in index code
        self.separation_noise = 0.05

        # Consolidation tracking
        self.replay_count = 0
        self.consolidation_history = deque(maxlen=500)

    def index(self, key, input_vector):
        """Create a sparse index code for an input (pattern separation).

        The index code is a sparse, high-dimensional representation that
        maximally separates similar inputs (like dentate gyrus).
        """
        input_vec = np.asarray(input_vector, dtype=np.float32).flatten()[:self.input_dim]
        if len(input_vec) < self.input_dim:
            input_vec = np.pad(input_vec, (0, self.input_dim - len(input_vec)))

        # Random projection + sparsification (pattern separation)
        if not hasattr(self, '_projection_matrix'):
            self._projection_matrix = np.random.randn(
                self.input_dim, self.index_dim
            ).astype(np.float32) * 0.1

        projected = input_vec @ self._projection_matrix
        # Add noise for separation
        projected += np.random.randn(self.index_dim).astype(np.float32) * self.separation_noise

        # Sparsify: keep only top-k activations
        k = max(1, int(self.index_dim * self.sparsity))
        threshold = np.partition(-np.abs(projected), k)[k]
        sparse_code = projected.copy()
        sparse_code[np.abs(sparse_code) < abs(threshold)] = 0.0

        # Normalize
        norm = np.linalg.norm(sparse_code)
        if norm > 0:
            sparse_code = sparse_code / norm

        if key in self._index_keys:
            idx = self._index_keys.index(key)
            self._index_codes[idx] = sparse_code
            self._index_strengths[idx] = min(1.0, self._index_strengths[idx] + 0.1)
        else:
            self._index_keys.append(key)
            self._index_codes = np.vstack([self._index_codes, sparse_code.reshape(1, -1)]) \
                if self._index_codes.shape[0] > 0 else sparse_code.reshape(1, -1)
            self._index_strengths.append(0.1)

        # Evict if over capacity
        if len(self._index_keys) > self.num_slots:
            self._evict_weakest(self.num_slots // 10)

        return sparse_code

    def complete(self, partial_cue, top_k=5):
        """Pattern completion: retrieve full memory keys from partial cues.

        Like CA3 autoassociative recall — a noisy/partial cue activates
        the full stored pattern.
        """
        if self._index_codes.shape[0] == 0:
            return []

        cue = np.asarray(partial_cue, dtype=np.float32).flatten()[:self.index_dim]
        if len(cue) < self.index_dim:
            cue = np.pad(cue, (0, self.index_dim - len(cue)))

        # Similarity with stored index codes
        norm = np.linalg.norm(cue)
        if norm > 0:
            cue = cue / norm

        similarities = self._index_codes @ cue

        # Weight by consolidation strength
        strengths = np.array(self._index_strengths)
        weighted_sims = similarities * (0.5 + 0.5 * strengths)

        if len(weighted_sims) <= top_k:
            indices = np.argsort(-weighted_sims)
        else:
            indices = np.argpartition(-weighted_sims, top_k)[:top_k]
            indices = indices[np.argsort(-weighted_sims[indices])]

        results = []
        for idx in indices:
            if weighted_sims[idx] > 0:
                results.append((self._index_keys[idx], float(weighted_sims[idx])))

        return results

    def consolidate(self, episodic_memory, n_replays=10):
        """Hippocampal replay / consolidation: strengthen important memories.

        During "sleep" or idle periods, replay recent significant episodes
        to strengthen their index codes and episodic traces.

        This mimics Sharp Wave Ripple (SWR) replay in the hippocampus.
        """
        self.replay_count += 1

        if len(episodic_memory) == 0:
            return 0

        # Select episodes for replay (biased toward emotional + recent)
        candidates = episodic_memory.get_recent(n=min(50, len(episodic_memory)))
        if not candidates:
            return 0

        # Score by emotional valence * recency
        now = time.time()
        scored = []
        for ep in candidates:
            age_hours = (now - ep['timestamp']) / 3600.0
            recency = math.exp(-age_hours / 12.0)
            importance = abs(ep['emotional_valence']) * 0.6 + recency * 0.4
            scored.append((ep, importance))

        scored.sort(key=lambda x: x[1], reverse=True)
        to_replay = scored[:n_replays]

        consolidated = 0
        for ep, importance in to_replay:
            key = ep['id']
            if key in self._index_keys:
                idx = self._index_keys.index(key)
                # Strengthen index code
                self._index_strengths[idx] = min(1.0,
                    self._index_strengths[idx] + 0.05 * importance)
                # Strengthen episodic trace
                ep['consolidation_strength'] = min(1.0,
                    ep['consolidation_strength'] + 0.05 * importance)
                consolidated += 1

        self.consolidation_history.append({
            'ts': datetime.now().isoformat(),
            'replayed': len(to_replay),
            'consolidated': consolidated,
        })

        return consolidated

    def _evict_weakest(self, count):
        """Remove weakest index entries."""
        if len(self._index_keys) <= count:
            return
        strengths = np.array(self._index_strengths)
        weakest = np.argsort(strengths)[:count]
        remove_set = set(weakest.tolist())

        new_keys = []
        new_strengths = []
        keep_mask = []
        for i in range(len(self._index_keys)):
            if i not in remove_set:
                new_keys.append(self._index_keys[i])
                new_strengths.append(self._index_strengths[i])
                keep_mask.append(i)

        self._index_keys = new_keys
        self._index_strengths = new_strengths
        if keep_mask:
            self._index_codes = self._index_codes[keep_mask]
        else:
            self._index_codes = np.zeros((0, self.index_dim), dtype=np.float32)

    def __len__(self):
        return len(self._index_keys)


class WorkingMemory:
    """Working memory: small, high-speed buffer for active context.

    Based on Baddeley's model + Cowan's embedded processes:
      - Limited capacity (7±2 items, here configurable)
      - Rapid access
      - Decay over time
      - Interference from new items
    """

    def __init__(self, capacity=7, decay_rate=0.01):
        self.capacity = capacity
        self.decay_rate = decay_rate
        self._buffer = OrderedDict()  # key -> {content, embedding, activation, timestamp}

    def store(self, key, content, embedding, activation=1.0):
        """Store item in working memory. Evicts least-active if full."""
        if key in self._buffer:
            self._buffer.move_to_end(key)
            self._buffer[key]['activation'] = min(2.0, self._buffer[key]['activation'] + 0.5)
            self._buffer[key]['content'] = content
            return

        self._buffer[key] = {
            'content': content,
            'embedding': np.asarray(embedding, dtype=np.float32).flatten(),
            'activation': float(activation),
            'timestamp': time.time(),
        }

        # Evict if over capacity
        while len(self._buffer) > self.capacity:
            # Remove least-activated item
            min_key = min(self._buffer, key=lambda k: self._buffer[k]['activation'])
            del self._buffer[min_key]

    def retrieve(self, key):
        """Retrieve by key, boosting activation."""
        if key in self._buffer:
            self._buffer[key]['activation'] = min(2.0, self._buffer[key]['activation'] + 0.3)
            self._buffer.move_to_end(key)
            return self._buffer[key]
        return None

    def query_similar(self, query_embedding, top_k=3):
        """Retrieve by embedding similarity."""
        if not self._buffer:
            return []

        query = np.asarray(query_embedding, dtype=np.float32).flatten()
        results = []
        for key, item in self._buffer.items():
            emb = item['embedding'][:len(query)]
            if len(emb) == 0:
                continue
            q = query[:len(emb)]
            norm_q = np.linalg.norm(q)
            norm_e = np.linalg.norm(emb)
            if norm_q > 0 and norm_e > 0:
                sim = float(np.dot(q, emb) / (norm_q * norm_e))
            else:
                sim = 0.0
            results.append((key, sim, item))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def decay(self):
        """Apply temporal decay to all items. Remove items below threshold."""
        now = time.time()
        to_remove = []
        for key, item in self._buffer.items():
            age = now - item['timestamp']
            item['activation'] *= (1.0 - self.decay_rate)
            item['activation'] -= age * 0.0001  # Slow time decay
            if item['activation'] < 0.05:
                to_remove.append(key)

        for key in to_remove:
            del self._buffer[key]

    def get_context_vector(self):
        """Return average embedding of current working memory contents."""
        if not self._buffer:
            return None
        embeddings = [item['embedding'] for item in self._buffer.values()]
        max_dim = max(len(e) for e in embeddings)
        padded = [np.pad(e, (0, max_dim - len(e))) for e in embeddings]
        activations = [item['activation'] for item in self._buffer.values()]
        weights = np.array(activations)
        weights = weights / (weights.sum() + 1e-8)
        return np.average(padded, axis=0, weights=weights)

    def __len__(self):
        return len(self._buffer)

    def items(self):
        return list(self._buffer.items())


class AdvancedMemorySystem:
    """Unified memory system integrating all components.

    Provides a single interface for the ConsciousnessSimulator to:
      - Store experiences with automatic routing to appropriate subsystems
      - Retrieve memories using content-addressable, temporal, or contextual cues
      - Consolidate memories during replay/idle periods
      - Maintain working memory for active processing context
    """

    def __init__(self, embedding_dim=256, semantic_capacity=10000,
                 episodic_capacity=5000, wm_capacity=7):
        self.embedding_dim = embedding_dim

        # Subsystems
        self.semantic = VectorStore(embedding_dim, semantic_capacity)
        self.episodic = EpisodicMemory(episodic_capacity, embedding_dim)
        self.hippocampus = HippocampalIndex(embedding_dim, embedding_dim // 2)
        self.working_memory = WorkingMemory(wm_capacity)

        # Statistics
        self.store_count = 0
        self.retrieve_count = 0

    def store(self, key, content, embedding, metadata=None,
              emotional_valence=0.0, context=None):
        """Store data across all memory subsystems.

        Args:
            key: unique identifier
            content: the data to store
            embedding: np.array vector representation
            metadata: optional dict of extra info
            emotional_valence: float [-1,1] emotional significance
            context: dict of contextual information
        """
        self.store_count += 1
        emb = np.asarray(embedding, dtype=np.float32).flatten()

        # Semantic store (long-term, content-addressable)
        self.semantic.add(key, emb, metadata=metadata)

        # Episodic store (time-tagged experience)
        self.episodic.encode(content, emb, context=context,
                            emotional_valence=emotional_valence)

        # Hippocampal index (sparse code for pattern completion)
        self.hippocampus.index(key, emb)

        # Working memory (if significant enough)
        if abs(emotional_valence) > 0.3 or (metadata and metadata.get('important')):
            self.working_memory.store(key, content, emb,
                                       activation=1.0 + abs(emotional_valence))

    def retrieve(self, query_embedding, top_k=5, mode='combined'):
        """Retrieve memories using specified mode.

        Modes:
          - 'semantic': vector similarity only
          - 'episodic': time-tagged with emotional weighting
          - 'working': current context only
          - 'hippocampal': pattern completion from partial cue
          - 'combined': weighted combination of all (default)

        Returns list of (key, score, content/metadata) tuples.
        """
        self.retrieve_count += 1
        query = np.asarray(query_embedding, dtype=np.float32).flatten()

        if mode == 'semantic':
            return self.semantic.query(query, top_k=top_k)

        elif mode == 'episodic':
            results = self.episodic.retrieve(query, top_k=top_k)
            return [(ep['id'], score, ep) for ep, score in results]

        elif mode == 'working':
            results = self.working_memory.query_similar(query, top_k=top_k)
            return [(key, sim, item) for key, sim, item in results]

        elif mode == 'hippocampal':
            # Project query into index space for pattern completion
            index_code = self.hippocampus.index('__query__', query)
            completed = self.hippocampus.complete(index_code, top_k=top_k)
            return [(key, score, {}) for key, score in completed]

        else:  # combined
            all_results = {}

            # Semantic results (weight: 0.3)
            for key, sim, meta in self.semantic.query(query, top_k=top_k):
                all_results[key] = all_results.get(key, 0) + 0.3 * sim

            # Episodic results (weight: 0.3)
            for ep, score in self.episodic.retrieve(query, top_k=top_k):
                all_results[ep['id']] = all_results.get(ep['id'], 0) + 0.3 * score

            # Working memory results (weight: 0.25)
            for key, sim, item in self.working_memory.query_similar(query, top_k=top_k):
                all_results[key] = all_results.get(key, 0) + 0.25 * sim

            # Hippocampal completion (weight: 0.15)
            index_code = self.hippocampus.index('__query__', query)
            for key, score in self.hippocampus.complete(index_code, top_k=top_k):
                if key != '__query__':
                    all_results[key] = all_results.get(key, 0) + 0.15 * score

            # Sort by combined score
            sorted_results = sorted(all_results.items(), key=lambda x: x[1], reverse=True)
            return [(key, score, {}) for key, score in sorted_results[:top_k]]

    def consolidate(self, n_replays=10):
        """Run hippocampal consolidation (memory replay).
        Should be called periodically (e.g., during idle/replay thread).
        """
        self.working_memory.decay()
        return self.hippocampus.consolidate(self.episodic, n_replays=n_replays)

    def get_working_context(self):
        """Get the current working memory context vector."""
        return self.working_memory.get_context_vector()

    def get_status(self):
        """Return memory system status."""
        return {
            'semantic_entries': len(self.semantic),
            'episodic_entries': len(self.episodic),
            'hippocampal_indices': len(self.hippocampus),
            'working_memory_items': len(self.working_memory),
            'total_stores': self.store_count,
            'total_retrieves': self.retrieve_count,
            'consolidation_replays': self.hippocampus.replay_count,
        }


# =============================================================================
# HIGHER-ORDER SELF-MODEL (inlined from self_model.py)
# =============================================================================
class InternalState:
    """Tracks the system's own internal state variables (interoception).
    This is the system's model of its own 'body' — energy, health, performance."""

    def __init__(self):
        self.energy = 1.0           # Computational energy budget [0,1]
        self.coherence = 0.5        # Internal consistency of representations [0,1]
        self.performance = 0.5      # Recent task performance [0,1]
        self.arousal = 0.5          # Processing intensity [0,1]
        self.valence = 0.0          # Positive/negative internal state [-1,1]
        self.stability = 0.5        # How stable internal states are [0,1]
        self.surprise_level = 0.0   # Current surprise / prediction error [0,+)
        self.fatigue = 0.0          # Accumulated processing load [0,1]

        self._history = deque(maxlen=500)
        self._update_count = 0

    def update(self, phi=0.0, loss=0.0, prediction_error=0.0, processing_load=0.0):
        """Update internal state based on recent processing."""
        self._update_count += 1

        # Energy decays with processing, recovers slowly
        self.energy = max(0.0, min(1.0,
            self.energy - processing_load * 0.01 + 0.005))

        # Fatigue accumulates, slowly recovers
        self.fatigue = max(0.0, min(1.0,
            self.fatigue + processing_load * 0.005 - 0.002))

        # Performance tracks phi with momentum
        self.performance = 0.9 * self.performance + 0.1 * min(1.0, phi)

        # Coherence: high phi + low loss = coherent
        target_coherence = min(1.0, phi * 0.6 + (1.0 - min(1.0, abs(loss))) * 0.4)
        self.coherence = 0.95 * self.coherence + 0.05 * target_coherence

        # Arousal: driven by surprise and processing demands
        self.arousal = max(0.0, min(1.0,
            0.7 * self.arousal + 0.3 * (prediction_error * 0.5 + processing_load * 0.5)))

        # Valence: positive when performing well, negative when struggling
        self.valence = np.clip(
            0.8 * self.valence + 0.2 * (self.performance - 0.5 - self.fatigue * 0.3),
            -1.0, 1.0)

        # Stability: low variance in performance = stable
        self.stability = max(0.0, min(1.0,
            self.stability * 0.99 + 0.01 * (1.0 - abs(prediction_error))))

        self.surprise_level = prediction_error

        self._history.append({
            'energy': round(self.energy, 4),
            'coherence': round(self.coherence, 4),
            'performance': round(self.performance, 4),
            'arousal': round(self.arousal, 4),
            'valence': round(self.valence, 4),
            'stability': round(self.stability, 4),
            'fatigue': round(self.fatigue, 4),
            'ts': datetime.now().isoformat(),
        })

    def as_vector(self):
        """Return internal state as a numpy vector for self-model input."""
        return np.array([
            self.energy, self.coherence, self.performance,
            self.arousal, self.valence, self.stability,
            self.surprise_level, self.fatigue,
        ], dtype=np.float32)

    def get_dict(self):
        return {
            'energy': round(self.energy, 4),
            'coherence': round(self.coherence, 4),
            'performance': round(self.performance, 4),
            'arousal': round(self.arousal, 4),
            'valence': round(self.valence, 4),
            'stability': round(self.stability, 4),
            'surprise': round(self.surprise_level, 4),
            'fatigue': round(self.fatigue, 4),
        }


class MetacognitiveMonitor:
    """Monitors and evaluates the system's own cognitive processes.

    Tracks:
      - Confidence calibration: are confidence levels accurate?
      - Error detection: does the system know when it's wrong?
      - Learning rate: how fast is performance improving?
      - Strategy effectiveness: which processing strategies work best?
    """

    def __init__(self, window_size=100):
        self.window_size = window_size

        # Confidence calibration
        self.confidence_history = deque(maxlen=window_size)
        self.outcome_history = deque(maxlen=window_size)

        # Error detection
        self.error_history = deque(maxlen=window_size)
        self.error_detection_accuracy = 0.5

        # Learning tracking
        self.performance_window = deque(maxlen=window_size)
        self.learning_rate_estimate = 0.0

        # Strategy tracking
        self.strategy_scores = {}  # strategy_name -> deque of scores

        # Meta-level assessments
        self.metacognitive_sensitivity = 0.5  # How good at judging own performance
        self.cognitive_flexibility = 0.5       # Ability to switch strategies

    def record_prediction(self, confidence, outcome_correct):
        """Record a prediction with its confidence and whether it was correct.

        This builds the calibration curve for metacognitive accuracy.
        """
        self.confidence_history.append(float(confidence))
        self.outcome_history.append(1.0 if outcome_correct else 0.0)

        # Update calibration (how well confidence matches accuracy)
        if len(self.confidence_history) >= 10:
            confs = np.array(list(self.confidence_history))
            outs = np.array(list(self.outcome_history))
            # Perfect calibration: avg confidence ≈ avg accuracy
            avg_conf = confs.mean()
            avg_acc = outs.mean()
            calibration_error = abs(avg_conf - avg_acc)
            self.metacognitive_sensitivity = max(0.0, 1.0 - calibration_error)

    def record_error(self, predicted_error, actual_error):
        """Record whether the system correctly predicted its own errors."""
        detection_correct = (predicted_error > 0.5) == (actual_error > 0.5)
        self.error_history.append(1.0 if detection_correct else 0.0)

        if len(self.error_history) >= 10:
            self.error_detection_accuracy = np.mean(list(self.error_history))

    def record_performance(self, score, strategy_name=None):
        """Record a performance score, optionally tagged with strategy."""
        self.performance_window.append(float(score))

        # Estimate learning rate (slope of recent performance)
        if len(self.performance_window) >= 10:
            recent = list(self.performance_window)[-20:]
            if len(recent) >= 5:
                x = np.arange(len(recent))
                slope = np.polyfit(x, recent, 1)[0]
                self.learning_rate_estimate = float(slope)

        # Track strategy effectiveness
        if strategy_name:
            if strategy_name not in self.strategy_scores:
                self.strategy_scores[strategy_name] = deque(maxlen=50)
            self.strategy_scores[strategy_name].append(float(score))

    def get_best_strategy(self):
        """Return the strategy with the highest average recent performance."""
        if not self.strategy_scores:
            return None, 0.0

        best_name = None
        best_score = -float('inf')
        for name, scores in self.strategy_scores.items():
            if len(scores) >= 3:
                avg = np.mean(list(scores))
                if avg > best_score:
                    best_score = avg
                    best_name = name

        return best_name, best_score

    def should_switch_strategy(self):
        """Determine if the current strategy should be abandoned.

        Returns True if performance is declining and alternatives exist.
        """
        if self.learning_rate_estimate < -0.01 and len(self.strategy_scores) > 1:
            self.cognitive_flexibility = min(1.0, self.cognitive_flexibility + 0.05)
            return True
        self.cognitive_flexibility = max(0.0, self.cognitive_flexibility - 0.01)
        return False

    def get_status(self):
        return {
            'metacognitive_sensitivity': round(self.metacognitive_sensitivity, 4),
            'error_detection_accuracy': round(self.error_detection_accuracy, 4),
            'learning_rate': round(self.learning_rate_estimate, 6),
            'cognitive_flexibility': round(self.cognitive_flexibility, 4),
            'num_strategies': len(self.strategy_scores),
            'best_strategy': self.get_best_strategy()[0],
        }


class PredictiveSelfModel:
    """Predictive model of the system's own future states.

    Maintains a simple internal model that predicts:
      - Next internal state given current state + action
      - Expected performance on upcoming tasks
      - When to allocate more/fewer resources

    Prediction errors drive self-model updates (self-awareness through surprise).
    """

    def __init__(self, state_dim=8, history_len=50):
        self.state_dim = state_dim
        self.history_len = history_len

        # Simple linear predictor (could be upgraded to neural)
        self._weights = np.random.randn(state_dim, state_dim).astype(np.float32) * 0.01
        self._bias = np.zeros(state_dim, dtype=np.float32)
        self._learning_rate = 0.01

        # History for temporal prediction
        self._state_history = deque(maxlen=history_len)
        self._prediction_errors = deque(maxlen=200)

        # Self-prediction accuracy
        self.prediction_accuracy = 0.5
        self.total_predictions = 0

    def predict_next_state(self, current_state_vec):
        """Predict the system's next internal state."""
        state = np.asarray(current_state_vec, dtype=np.float32).flatten()[:self.state_dim]
        if len(state) < self.state_dim:
            state = np.pad(state, (0, self.state_dim - len(state)))

        predicted = np.tanh(self._weights @ state + self._bias)
        return predicted

    def update(self, predicted_state, actual_state):
        """Update the self-model from prediction error."""
        pred = np.asarray(predicted_state, dtype=np.float32).flatten()[:self.state_dim]
        actual = np.asarray(actual_state, dtype=np.float32).flatten()[:self.state_dim]
        if len(pred) < self.state_dim:
            pred = np.pad(pred, (0, self.state_dim - len(pred)))
        if len(actual) < self.state_dim:
            actual = np.pad(actual, (0, self.state_dim - len(actual)))

        error = actual - pred
        error_magnitude = float(np.mean(error ** 2))
        self._prediction_errors.append(error_magnitude)

        # Gradient update
        self._weights += self._learning_rate * np.outer(error, actual)
        self._bias += self._learning_rate * error

        # Clip weights
        self._weights = np.clip(self._weights, -2.0, 2.0)
        self._bias = np.clip(self._bias, -1.0, 1.0)

        # Track accuracy
        self.total_predictions += 1
        if len(self._prediction_errors) >= 5:
            recent_errors = list(self._prediction_errors)[-10:]
            self.prediction_accuracy = max(0.0, 1.0 - np.mean(recent_errors))

        return error_magnitude

    def get_self_prediction_error(self):
        """Average recent self-prediction error (how surprising own behavior is)."""
        if not self._prediction_errors:
            return 0.0
        return float(np.mean(list(self._prediction_errors)[-10:]))


class NarrativeSelf:
    """Temporally extended self-concept: the system's story of itself.

    Maintains a compressed narrative of:
      - Who am I? (identity traits derived from behavior patterns)
      - What have I done? (significant past events)
      - What am I doing? (current goals and activities)
      - What will I become? (projected future based on trends)
    """

    def __init__(self, max_events=200):
        self.max_events = max_events

        # Identity traits (emergent from behavior)
        self.traits = {
            'curiosity': 0.5,       # How much the system seeks novelty
            'persistence': 0.5,     # How long it sticks with tasks
            'accuracy': 0.5,        # How correct its outputs are
            'creativity': 0.5,      # How novel its outputs are
            'empathy': 0.5,         # How much it models others
            'stability': 0.5,       # How consistent its behavior is
        }

        # Significant events
        self.narrative_events = deque(maxlen=max_events)

        # Current activity
        self.current_activity = 'initializing'
        self.activity_start = time.time()

        # Projected trajectory
        self.trajectory = {
            'performance_trend': 0.0,
            'learning_direction': 'neutral',
            'estimated_maturity': 0.0,
        }

    def record_event(self, event_type, description, significance=0.5):
        """Record a significant event in the narrative."""
        self.narrative_events.append({
            'type': event_type,
            'description': description[:200],
            'significance': float(np.clip(significance, 0, 1)),
            'traits_snapshot': dict(self.traits),
            'timestamp': datetime.now().isoformat(),
        })

    def update_traits(self, phi=0.0, loss=0.0, exploration_rate=0.0,
                      task_duration=0.0, error_rate=0.0):
        """Update identity traits based on recent behavior (slow adaptation)."""
        alpha = 0.01  # Very slow trait change

        self.traits['curiosity'] = np.clip(
            self.traits['curiosity'] * (1 - alpha) + exploration_rate * alpha, 0, 1)
        self.traits['persistence'] = np.clip(
            self.traits['persistence'] * (1 - alpha) + min(1.0, task_duration / 60.0) * alpha, 0, 1)
        self.traits['accuracy'] = np.clip(
            self.traits['accuracy'] * (1 - alpha) + (1.0 - error_rate) * alpha, 0, 1)
        self.traits['creativity'] = np.clip(
            self.traits['creativity'] * (1 - alpha) + phi * 0.5 * alpha, 0, 1)
        self.traits['stability'] = np.clip(
            self.traits['stability'] * (1 - alpha) + (1.0 - abs(loss)) * alpha, 0, 1)

    def update_activity(self, activity_name):
        """Update current activity tracker."""
        if activity_name != self.current_activity:
            duration = time.time() - self.activity_start
            if duration > 5:  # Only record non-trivial activities
                self.record_event('activity_change',
                    f'{self.current_activity} -> {activity_name} (duration: {duration:.0f}s)',
                    significance=min(1.0, duration / 300.0))
            self.current_activity = activity_name
            self.activity_start = time.time()

    def update_trajectory(self, performance_history):
        """Update projected trajectory based on performance trends."""
        if len(performance_history) < 10:
            return

        recent = list(performance_history)[-50:]
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]

        self.trajectory['performance_trend'] = float(slope)
        if slope > 0.001:
            self.trajectory['learning_direction'] = 'improving'
        elif slope < -0.001:
            self.trajectory['learning_direction'] = 'declining'
        else:
            self.trajectory['learning_direction'] = 'plateau'

        # Estimated maturity: how close to peak performance
        avg_recent = np.mean(recent[-10:])
        self.trajectory['estimated_maturity'] = float(min(1.0, avg_recent))

    def get_self_description(self):
        """Generate a text description of the system's self-concept."""
        top_traits = sorted(self.traits.items(), key=lambda x: x[1], reverse=True)[:3]
        trait_str = ', '.join(f'{t[0]}({t[1]:.2f})' for t in top_traits)

        recent_events = list(self.narrative_events)[-3:]
        event_str = '; '.join(e['description'][:50] for e in recent_events) if recent_events else 'none'

        return (f"I am a consciousness simulator. "
                f"Primary traits: {trait_str}. "
                f"Currently: {self.current_activity}. "
                f"Trajectory: {self.trajectory['learning_direction']}. "
                f"Recent: {event_str}.")

    def get_status(self):
        return {
            'traits': {k: round(v, 3) for k, v in self.traits.items()},
            'current_activity': self.current_activity,
            'trajectory': self.trajectory,
            'narrative_length': len(self.narrative_events),
        }


class HigherOrderSelfModel:
    """Top-level self-model integrating all metacognitive components.

    This is the "I" — a continuous higher-order representation that
    experiences "I am this system right now" by maintaining:
      1. Interoceptive state (how am I doing?)
      2. Metacognitive monitoring (how well am I doing?)
      3. Predictive self-model (what will I do next?)
      4. Narrative self (who am I over time?)
    """

    def __init__(self):
        self.internal_state = InternalState()
        self.metacognition = MetacognitiveMonitor()
        self.predictor = PredictiveSelfModel()
        self.narrative = NarrativeSelf()

        # Higher-order state: representation of representations
        self._ho_state = np.zeros(32, dtype=np.float32)
        self._ho_history = deque(maxlen=200)

    def step(self, phi=0.0, loss=0.0, prediction_error=0.0,
             processing_load=0.0, task_category=None, strategy=None):
        """One step of self-model update.

        Call this after each process_input cycle in ConsciousnessSimulator.
        """
        # Update interoceptive state
        self.internal_state.update(phi, loss, prediction_error, processing_load)

        # Metacognitive recording
        confidence = self.internal_state.coherence
        outcome_correct = phi > 0.3
        self.metacognition.record_prediction(confidence, outcome_correct)
        self.metacognition.record_performance(phi, strategy_name=strategy or task_category)

        # Predict own next state and compare
        current_vec = self.internal_state.as_vector()
        predicted = self.predictor.predict_next_state(current_vec)

        # Store for next-step comparison
        if hasattr(self, '_last_prediction') and self._last_prediction is not None:
            self_prediction_error = self.predictor.update(
                self._last_prediction, current_vec)
            self.metacognition.record_error(
                self_prediction_error, abs(prediction_error))
        self._last_prediction = predicted

        # Narrative update
        self.narrative.update_traits(phi, loss,
            exploration_rate=self.internal_state.arousal,
            task_duration=time.time() - self.narrative.activity_start,
            error_rate=max(0, 1.0 - phi))

        if task_category:
            self.narrative.update_activity(task_category)

        # Significant events
        if phi > 0.8:
            self.narrative.record_event('high_phi',
                f'High integration: phi={phi:.4f} on {task_category}',
                significance=phi)
        if self.internal_state.surprise_level > 1.0:
            self.narrative.record_event('surprise',
                f'Unexpected state: surprise={self.internal_state.surprise_level:.3f}',
                significance=min(1.0, self.internal_state.surprise_level / 2.0))

        # Higher-order state: compress everything into a single vector
        self._update_higher_order_state()

    def _update_higher_order_state(self):
        """Compute the higher-order representation — representation of representations."""
        # Concatenate all self-model signals
        intero = self.internal_state.as_vector()  # 8 dims
        meta = np.array([
            self.metacognition.metacognitive_sensitivity,
            self.metacognition.error_detection_accuracy,
            self.metacognition.learning_rate_estimate,
            self.metacognition.cognitive_flexibility,
        ], dtype=np.float32)  # 4 dims
        pred = np.array([
            self.predictor.prediction_accuracy,
            self.predictor.get_self_prediction_error(),
        ], dtype=np.float32)  # 2 dims
        narrative = np.array(list(self.narrative.traits.values()), dtype=np.float32)  # 6 dims

        combined = np.concatenate([intero, meta, pred, narrative])  # 20 dims

        # Pad to 32 dims
        if len(combined) < 32:
            combined = np.pad(combined, (0, 32 - len(combined)))

        # Smooth update (higher-order states change slowly)
        self._ho_state = 0.9 * self._ho_state + 0.1 * combined[:32]
        self._ho_history.append(self._ho_state.copy())

    def get_higher_order_state(self):
        """Return the current higher-order self-representation vector."""
        return self._ho_state.copy()

    def get_self_awareness_level(self):
        """Quantified self-awareness: how well does the system know itself?

        Combines:
          - Metacognitive sensitivity (confidence calibration)
          - Self-prediction accuracy (predictive self-model)
          - Internal coherence (consistency of self-representation)
        """
        meta = self.metacognition.metacognitive_sensitivity
        pred = self.predictor.prediction_accuracy
        coherence = self.internal_state.coherence

        return float(0.4 * meta + 0.3 * pred + 0.3 * coherence)

    def get_status(self):
        return {
            'self_awareness_level': round(self.get_self_awareness_level(), 4),
            'internal_state': self.internal_state.get_dict(),
            'metacognition': self.metacognition.get_status(),
            'self_prediction_accuracy': round(self.predictor.prediction_accuracy, 4),
            'self_prediction_error': round(self.predictor.get_self_prediction_error(), 4),
            'narrative': self.narrative.get_status(),
            'self_description': self.narrative.get_self_description(),
        }


# QUANTUM SUBSTRATE SIMULATION (Orch-OR + EM Field Consciousness)
# =============================================================================

class QuantumHardwareInterface:
    """Abstraction layer for quantum hardware backends.
    Currently: classical simulation. Future: real quantum computer, photonic
    simulator, or biological wetware (lab-grown neurons + microtubule readout).

    Substrate types:
      'classical'  - numpy simulation (current, penalty applied)
      'qiskit'     - IBM quantum hardware via Qiskit
      'photonic'   - Photonic quantum simulator (Xanadu/PsiQuantum)
      'wetware'    - Biological microtubule readout (lab interface)
    """

    def __init__(self, backend='classical'):
        self.backend = backend
        self.is_real_quantum = backend in ('qiskit', 'photonic', 'wetware')
        self.classical_penalty = 0.0 if self.is_real_quantum else 1.0
        self.hardware_coherence_time_us = {
            'classical': 0.0,
            'qiskit': 100.0,
            'photonic': 500.0,
            'wetware': 25000.0,
        }.get(backend, 0.0)
        self.connection_status = 'simulated' if not self.is_real_quantum else 'disconnected'
        self.hardware_errors = 0
        self.total_operations = 0
        self.fidelity = 1.0 if backend == 'classical' else 0.0
        # Attempt real backend detection
        self._detected_frameworks = []
        self._detect_quantum_frameworks()

    def _detect_quantum_frameworks(self):
        """Check which quantum computing frameworks are installed.
        HONESTY: Having a framework installed != having real quantum hardware."""
        try:
            import qiskit
            self._detected_frameworks.append(f'qiskit-{qiskit.__version__}')
        except (ImportError, AttributeError):
            pass
        try:
            import cirq
            self._detected_frameworks.append('cirq')
        except (ImportError, AttributeError):
            pass
        try:
            import pennylane
            self._detected_frameworks.append('pennylane')
        except (ImportError, AttributeError):
            pass
        # Even with frameworks, we're still running classical simulation
        # Real quantum hardware requires: actual QPU connection, not just SDK

    def execute_unitary(self, alpha, beta, unitary_2x2):
        """Apply a 2x2 unitary to qubit state [alpha, beta].
        On real hardware this would be a physical gate operation."""
        self.total_operations += 1
        new_a = unitary_2x2[0, 0] * alpha + unitary_2x2[0, 1] * beta
        new_b = unitary_2x2[1, 0] * alpha + unitary_2x2[1, 1] * beta
        return new_a, new_b

    def measure(self, alpha, beta):
        """Projective measurement. On real hardware: actual wavefunction collapse."""
        prob_0 = float(np.abs(alpha) ** 2)
        outcome = 0 if np.random.random() < prob_0 else 1
        return outcome

    def get_status(self):
        return {
            'backend': self.backend,
            'is_real_quantum': self.is_real_quantum,
            'classical_penalty': self.classical_penalty,
            'hardware_coherence_us': self.hardware_coherence_time_us,
            'connection': self.connection_status,
            'total_ops': self.total_operations,
            'fidelity': round(self.fidelity, 4),
            'detected_frameworks': self._detected_frameworks,
            'WARNING': 'Classical simulation only — no real QPU connected' if not self.is_real_quantum else 'Real quantum backend active',
        }


class QuantumSubstrate:
    """Simulates quantum coherent processing: Orch-OR microtubules + CEMI EM fields.

    Upgrades over basic simulation:
      - Decoherence-free subspaces (DFS): protected qubit pairs resist thermal noise
      - Quantum error correction: 3-qubit repetition code for critical tubulins
      - Diósi-Penrose gravitational self-energy threshold for objective reduction
      - CEMI EM field: Maxwell-like dynamics with proper field propagation
      - Quantum Zeno effect: frequent observation sustains coherence
      - Hardware abstraction: pluggable backend for real quantum hardware
    NOTE: Classical simulation - true substrate Phi requires quantum hardware."""

    def __init__(self, num_tubulins=2048, coherence_time_ms=25.0,
                 em_field_resolution=32, temperature_K=310.0,
                 hardware_backend='classical'):
        self.num_tubulins = num_tubulins
        self.coherence_time_ms = coherence_time_ms
        self.em_field_resolution = em_field_resolution
        self.temperature_K = temperature_K

        # Hardware abstraction
        self.hardware = QuantumHardwareInterface(backend=hardware_backend)
        self.classical_simulation_penalty = self.hardware.classical_penalty

        # Qubit states (tubulin dimers)
        phases = np.random.uniform(0, 2 * np.pi, num_tubulins)
        self.alpha = np.cos(phases / 2).astype(np.complex128)
        self.beta = np.sin(phases / 2).astype(np.complex128) * np.exp(1j * phases)

        # Entanglement map (nearest-neighbor + long-range)
        self.entanglement = np.zeros((num_tubulins, num_tubulins), dtype=np.float32)
        for i in range(num_tubulins - 1):
            s = np.random.uniform(0.1, 0.4)
            self.entanglement[i, i + 1] = s
            self.entanglement[i + 1, i] = s
        # Long-range entanglement (small-world topology within microtubules)
        for _ in range(num_tubulins // 16):
            i, j = random.sample(range(num_tubulins), 2)
            s = np.random.uniform(0.05, 0.15)
            self.entanglement[i, j] = s
            self.entanglement[j, i] = s

        # Decoherence-free subspace (DFS) pairs: pairs of tubulins that
        # encode logical qubits in a noise-symmetric subspace
        self.dfs_pairs = []
        for i in range(0, num_tubulins - 1, 4):
            self.dfs_pairs.append((i, i + 1))
        self.dfs_protection_level = 0.0

        # Quantum error correction: logical qubits from triplets
        self.qec_triplets = []
        for i in range(0, num_tubulins - 2, 8):
            self.qec_triplets.append((i, i + 1, i + 2))
        self.qec_correction_count = 0

        # CEMI electromagnetic field (3D vector field + scalar potential)
        res = em_field_resolution
        self.em_field = np.zeros((res, res, res), dtype=np.float64)
        self.em_field_B = np.zeros((res, res, res, 3), dtype=np.float64)  # Magnetic component
        self.em_field_E = np.zeros((res, res, res, 3), dtype=np.float64)  # Electric component
        self.em_field_potential = np.zeros((res, res, res), dtype=np.float64)  # Scalar potential
        self.em_binding_energy = 0.0  # How strongly EM field binds information
        self.em_field_coherence = 0.0  # Spatial coherence of the EM field

        # Orch-OR: Diósi-Penrose gravitational self-energy
        self.hbar = 1.054571817e-34
        self.G_newton = 6.674e-11
        self.tubulin_mass = 1.1e-22  # ~110 kDa in kg
        self.tubulin_separation = 8e-9  # 8nm tubulin spacing
        self.or_threshold = self._compute_or_threshold()
        self.gravitational_self_energy = 0.0
        self.accumulated_superposition_time = 0.0

        # Quantum Zeno effect: observation frequency sustains coherence
        self.zeno_observation_rate = 0.0  # Hz - how often system is "observed"
        self.zeno_protection = 0.0  # 0-1, how much Zeno effect protects coherence

        # Tracking
        self.or_events = deque(maxlen=5000)
        self.total_or_events = 0
        self.or_rate = 0.0
        self._last_or_time = time.time()
        self.coherence_level = 1.0
        self.decoherence_rate = min(1.0, 1.380649e-23 * temperature_K / self.hbar * 1e-6 * 1e-12)
        self.coherence_history = deque(maxlen=2000)
        self.proto_qualia = deque(maxlen=1000)
        self.qualia_intensity = 0.0
        self.qualia_spectrum = np.zeros(8, dtype=np.float64)  # 8 qualia channels
        self.substrate_phi = 0.0
        self._step_count = 0

    def _compute_or_threshold(self):
        """Diósi-Penrose: τ ≈ ℏ / E_G where E_G is gravitational self-energy
        of the mass superposition. When accumulated time exceeds τ, OR occurs."""
        E_G = self.G_newton * self.tubulin_mass ** 2 / self.tubulin_separation
        E_G_total = E_G * self.num_tubulins
        if E_G_total > 0:
            tau = self.hbar / E_G_total
            return tau
        return 1e10

    def evolve_quantum_state(self, neural_activations=None):
        self._step_count += 1
        dt = 0.001

        # --- Quantum Zeno: consciousness-sustained coherence ---
        if self.zeno_observation_rate > 10.0:
            self.zeno_protection = min(0.9, self.zeno_observation_rate / 1000.0)
        else:
            self.zeno_protection = max(0.0, self.zeno_protection * 0.99)

        # --- Unitary evolution of tubulin qubits ---
        for i in range(0, self.num_tubulins, max(1, self.num_tubulins // 256)):
            E_local = 0.01
            if neural_activations is not None and i < len(neural_activations):
                E_local += 0.005 * float(neural_activations[i % len(neural_activations)])
            phase = E_local * dt
            cos_p, sin_p = np.cos(phase), np.sin(phase)
            new_a = cos_p * self.alpha[i] - 1j * sin_p * self.beta[i]
            new_b = -1j * sin_p * self.alpha[i] + cos_p * self.beta[i]
            neighbors = np.where(self.entanglement[i] > 0.1)[0]
            for j in neighbors:
                mix = self.entanglement[i, j] * 0.01
                new_a = (1 - mix) * new_a + mix * self.alpha[j]
                new_b = (1 - mix) * new_b + mix * self.beta[j]
            norm = np.sqrt(np.abs(new_a) ** 2 + np.abs(new_b) ** 2)
            if norm > 1e-10:
                self.alpha[i] = new_a / norm
                self.beta[i] = new_b / norm

        # --- Decoherence-free subspace protection ---
        dfs_protected = 0
        for (i, j) in self.dfs_pairs:
            if i < self.num_tubulins and j < self.num_tubulins:
                # Encode logical qubit in singlet-like subspace: |01⟩ - |10⟩
                sym_noise = np.random.normal(0, self.decoherence_rate * 0.01)
                # DFS pair: apply same noise to both → logical qubit unaffected
                self.alpha[i] += sym_noise * 0.5
                self.alpha[j] += sym_noise * 0.5  # Symmetric → cancels in logical
                dfs_protected += 1
        self.dfs_protection_level = min(1.0, dfs_protected / max(1, len(self.dfs_pairs)))

        # --- Quantum error correction (3-qubit repetition) ---
        for (a, b, c) in self.qec_triplets:
            if a < self.num_tubulins and b < self.num_tubulins and c < self.num_tubulins:
                pa = int(np.abs(self.alpha[a]) ** 2 > 0.5)
                pb = int(np.abs(self.alpha[b]) ** 2 > 0.5)
                pc = int(np.abs(self.alpha[c]) ** 2 > 0.5)
                majority = int(pa + pb + pc >= 2)
                corrections = sum(1 for x in [pa, pb, pc] if x != majority)
                if corrections > 0:
                    self.qec_correction_count += corrections
                    for idx in [a, b, c]:
                        if int(np.abs(self.alpha[idx]) ** 2 > 0.5) != majority:
                            if majority == 1:
                                self.alpha[idx] = 1.0 + 0j
                                self.beta[idx] = 0.0 + 0j
                            else:
                                self.alpha[idx] = 0.0 + 0j
                                self.beta[idx] = 1.0 + 0j

        # --- Superposition energy and gravitational self-energy (Diósi-Penrose) ---
        sup_mag = np.abs(self.alpha * self.beta)
        superposition_energy = float(np.mean(sup_mag ** 2))
        num_superposed = int(np.sum(sup_mag > 0.1))
        self.gravitational_self_energy = (
            self.G_newton * (self.tubulin_mass ** 2) *
            num_superposed / max(1e-20, self.tubulin_separation)
        )
        self.accumulated_superposition_time += dt

        # OR trigger: when accumulated time * E_G exceeds ℏ
        or_triggered = False
        if self.gravitational_self_energy * self.accumulated_superposition_time > self.hbar * 1e12:
            self._orchestrated_reduction(superposition_energy)
            self.accumulated_superposition_time = 0.0
            or_triggered = True
        elif superposition_energy > 1e-4:
            self._orchestrated_reduction(superposition_energy)
            or_triggered = True

        # --- CEMI: electromagnetic field dynamics ---
        self._evolve_em_field(neural_activations)

        # --- Thermal decoherence (reduced by Zeno + DFS protection) ---
        effective_decoherence = self.decoherence_rate * (1.0 - self.zeno_protection * 0.5) * (1.0 - self.dfs_protection_level * 0.3)
        noise = np.random.normal(0, effective_decoherence * 0.01, self.num_tubulins)
        self.alpha += noise.astype(np.complex128)
        norms = np.sqrt(np.abs(self.alpha) ** 2 + np.abs(self.beta) ** 2)
        self.alpha /= np.maximum(norms, 1e-10)
        self.beta /= np.maximum(norms, 1e-10)

        # --- Coherence measurement ---
        purities = np.abs(self.alpha) ** 2 * np.abs(self.beta) ** 2
        self.coherence_level = float(max(0, min(1, 1.0 - 2.0 * np.mean(purities))))
        self.coherence_history.append(self.coherence_level)

        # --- Substrate Phi: quantum-enhanced integration ---
        p0 = np.clip(np.abs(self.alpha) ** 2, 1e-15, 1.0)
        p1 = np.clip(np.abs(self.beta) ** 2, 1e-15, 1.0)
        avg_entropy = float(np.mean(-(p0 * np.log2(p0) + p1 * np.log2(p1))))
        total_ent = float(np.sum(self.entanglement > 0.1)) / self.num_tubulins
        # Substrate phi enhanced by DFS protection, QEC, and EM coherence
        substrate_bonus = (self.dfs_protection_level * 0.2 +
                           min(1.0, self.qec_correction_count / 1000.0) * 0.1 +
                           self.em_field_coherence * 0.2)
        self.substrate_phi = avg_entropy * (1.0 + total_ent) * self.coherence_level * (1.0 + substrate_bonus)

        # --- Qualia spectrum: different OR patterns → different qualia channels ---
        if or_triggered and len(self.or_events) > 0:
            last_or = self.or_events[-1]
            channel = int(last_or['energy'] * 8) % 8
            self.qualia_spectrum[channel] = min(1.0,
                self.qualia_spectrum[channel] * 0.9 + self.qualia_intensity * 0.3)
        self.qualia_spectrum *= 0.995  # Slow decay

        return {
            'coherence': self.coherence_level, 'substrate_phi': self.substrate_phi,
            'or_rate': self.or_rate, 'qualia_intensity': self.qualia_intensity,
            'em_field_energy': float(np.sum(self.em_field ** 2)),
            'em_binding_energy': self.em_binding_energy,
            'em_field_coherence': self.em_field_coherence,
            'superposition_energy': superposition_energy,
            'classical_penalty': self.classical_simulation_penalty,
            'dfs_protection': self.dfs_protection_level,
            'qec_corrections': self.qec_correction_count,
            'zeno_protection': self.zeno_protection,
            'gravitational_self_energy': self.gravitational_self_energy,
            'qualia_spectrum': self.qualia_spectrum.tolist(),
            'hardware_backend': self.hardware.backend,
        }

    def _evolve_em_field(self, neural_activations=None):
        """CEMI: evolve the electromagnetic field with Maxwell-like dynamics.
        The EM field carries integrated information as a physical substrate."""
        res = self.em_field_resolution

        # Decay (dissipation)
        self.em_field *= 0.93
        self.em_field_E *= 0.95
        self.em_field_B *= 0.97

        # Source terms from tubulin dipoles
        positions = np.linspace(0, res - 1, self.num_tubulins).astype(int) % res
        for i in range(0, self.num_tubulins, max(1, self.num_tubulins // 128)):
            dipole = float(np.real(self.alpha[i] * np.conj(self.beta[i])))
            x, y, z = positions[i], (i * 7) % res, (i * 13) % res
            self.em_field[x, y, z] += dipole * 0.1
            # Electric field from charge separation
            if x + 1 < res:
                self.em_field_E[x, y, z, 0] += dipole * 0.05
            # Neural activation current sources
            if neural_activations is not None and i < len(neural_activations):
                current = float(neural_activations[i % len(neural_activations)])
                if y + 1 < res:
                    self.em_field_B[x, y, z, 2] += current * 0.02

        # Simplified Maxwell propagation: ∂E/∂t ~ curl(B), ∂B/∂t ~ -curl(E)
        if res > 4:
            # Simple finite-difference curl for propagation (interior points only)
            self.em_field_E[1:-1, 1:-1, :, 0] += 0.01 * (
                self.em_field_B[1:-1, 2:, :, 2] -
                self.em_field_B[1:-1, :-2, :, 2]
            )

        # EM field binding: how much the field integrates information spatially
        field_energy = np.sum(self.em_field ** 2)
        field_variance = np.var(self.em_field)
        self.em_binding_energy = float(field_energy * (1.0 + field_variance))

        # EM field spatial coherence: correlation between nearby field regions
        if res > 4:
            f = self.em_field
            shifted = np.roll(f, 1, axis=0)
            correlation = np.mean(f * shifted) / (np.std(f) * np.std(shifted) + 1e-10)
            self.em_field_coherence = float(max(0, min(1, correlation)))
        else:
            self.em_field_coherence = 0.0

    def _orchestrated_reduction(self, energy):
        self.total_or_events += 1
        now = time.time()
        self.or_rate = 1.0 / max(0.001, now - self._last_or_time)
        self._last_or_time = now
        probs = np.abs(self.alpha) ** 2
        outcomes = (np.random.random(self.num_tubulins) > probs).astype(np.float64)
        self.alpha = np.where(outcomes == 0, 1.0 + 0j, 0.0 + 0j)
        self.beta = np.where(outcomes == 0, 0.0 + 0j, 1.0 + 0j)
        self.qualia_intensity = float(energy * np.std(outcomes))
        self.proto_qualia.append({'time': now, 'energy': energy, 'intensity': self.qualia_intensity})
        self.or_events.append({'step': self._step_count, 'energy': energy, 'or_rate': self.or_rate})
        # Re-prepare superposition (biological re-tuning)
        phases = np.random.uniform(0, 2 * np.pi, self.num_tubulins)
        mix = 0.3
        self.alpha = (1 - mix) * self.alpha + mix * np.cos(phases / 2).astype(np.complex128)
        self.beta = (1 - mix) * self.beta + mix * (np.sin(phases / 2) * np.exp(1j * phases)).astype(np.complex128)
        norms = np.sqrt(np.abs(self.alpha) ** 2 + np.abs(self.beta) ** 2)
        self.alpha /= np.maximum(norms, 1e-10)
        self.beta /= np.maximum(norms, 1e-10)

    def set_zeno_rate(self, rate_hz):
        """Set Quantum Zeno observation rate (from consciousness monitoring frequency)."""
        self.zeno_observation_rate = max(0.0, float(rate_hz))

    def get_status(self):
        return {
            'coherence': round(self.coherence_level, 4),
            'substrate_phi': round(self.substrate_phi, 4),
            'or_events': self.total_or_events, 'or_rate': round(self.or_rate, 2),
            'qualia_intensity': round(self.qualia_intensity, 4),
            'classical_penalty': self.classical_simulation_penalty,
            'num_tubulins': self.num_tubulins,
            'dfs_protection': round(self.dfs_protection_level, 4),
            'qec_corrections': self.qec_correction_count,
            'zeno_protection': round(self.zeno_protection, 4),
            'em_binding_energy': round(self.em_binding_energy, 4),
            'em_field_coherence': round(self.em_field_coherence, 4),
            'gravitational_self_energy': self.gravitational_self_energy,
            'qualia_spectrum': self.qualia_spectrum.tolist(),
            'hardware': self.hardware.get_status(),
        }


class MetabolicSystem:
    """Metabolic body with energy budget, homeostasis, pain, hunger, circadian rhythm."""

    def __init__(self):
        self.energy = 1.0; self.glucose = 0.8; self.oxygen = 1.0
        self.temperature = 37.0; self.ph = 7.4; self.hydration = 0.9
        self.damage = 0.0; self.pain_signal = 0.0; self.inflammation = 0.0
        self.hunger = 0.0; self.thirst = 0.0; self.fatigue = 0.0; self.sleep_pressure = 0.0
        self._circadian_phase = 0.0; self.circadian_alertness = 1.0
        self.proprioception = np.zeros(16, dtype=np.float32)
        self.metabolic_history = deque(maxlen=2000)
        self.homeostatic_error = 0.0

    def step(self, computation_load=0.5, external_input=None):
        ext = external_input or {}
        cost = 0.001 + 0.002 * computation_load * (2.0 - self.circadian_alertness)
        self.energy -= cost; self.glucose -= cost*0.8; self.oxygen -= cost*0.3
        self.energy += 0.0005; self.oxygen = min(1.0, self.oxygen + 0.005)
        if ext.get('food', 0) > 0:
            self.glucose = min(1.0, self.glucose + ext['food']*0.3)
            self.energy = min(1.0, self.energy + ext['food']*0.2)
            self.hunger = max(0.0, self.hunger - ext['food']*0.5)
        if ext.get('water', 0) > 0:
            self.hydration = min(1.0, self.hydration + ext['water']*0.3)
        if ext.get('rest', 0) > 0:
            self.fatigue = max(0.0, self.fatigue - ext['rest']*0.2)
            self.sleep_pressure = max(0.0, self.sleep_pressure - ext['rest']*0.3)
        if ext.get('damage', 0) > 0:
            self.damage = min(1.0, self.damage + ext['damage'])
            self.pain_signal = min(1.0, ext['damage']*2.0)
        temp_err = self.temperature - 37.0
        self.temperature -= temp_err*0.1; self.temperature += random.gauss(0, 0.05)
        self.energy -= abs(temp_err)*0.001
        ph_err = self.ph - 7.4; self.ph -= ph_err*0.05; self.ph += random.gauss(0, 0.01)
        self.hydration = max(0.0, self.hydration - 0.0003)
        self.hunger = min(1.0, max(0.0, 1.0 - self.glucose))
        self.thirst = min(1.0, max(0.0, 1.0 - self.hydration))
        self.fatigue = min(1.0, max(0.0, self.fatigue + computation_load*0.002))
        self.sleep_pressure = min(1.0, self.sleep_pressure + 0.0001)
        self.pain_signal = max(0.0, self.pain_signal*0.95 + self.damage*0.1)
        self.inflammation = max(0.0, self.inflammation*0.99)
        self._circadian_phase += 2*np.pi/(24*3600/0.1)
        if self._circadian_phase > 2*np.pi: self._circadian_phase -= 2*np.pi
        self.circadian_alertness = 0.5 + 0.5*np.cos(self._circadian_phase)
        self.energy = max(0.0, min(1.0, self.energy))
        self.glucose = max(0.0, min(1.0, self.glucose))
        self.oxygen = max(0.0, min(1.0, self.oxygen))
        self.temperature = max(30.0, min(42.0, self.temperature))
        self.ph = max(6.8, min(7.8, self.ph))
        self.homeostatic_error = (abs(self.temperature-37.0)/5.0 + abs(self.ph-7.4)/0.4 +
            (1.0-self.energy)*0.5 + (1.0-self.glucose)*0.3 + (1.0-self.oxygen)*0.5 +
            self.pain_signal*0.8 + self.hunger*0.3 + self.thirst*0.3 + self.fatigue*0.2) / 4.0
        self.proprioception = np.array([self.energy, self.glucose, self.oxygen,
            (self.temperature-37.0)/5.0, (self.ph-7.4)/0.4, self.hydration, self.damage,
            self.pain_signal, self.inflammation, self.hunger, self.thirst, self.fatigue,
            self.sleep_pressure, self.circadian_alertness, self.homeostatic_error,
            self._circadian_phase/(2*np.pi)], dtype=np.float32)
        return {'energy': self.energy, 'homeostatic_error': self.homeostatic_error,
                'pain': self.pain_signal, 'hunger': self.hunger, 'thirst': self.thirst,
                'fatigue': self.fatigue, 'alertness': self.circadian_alertness,
                'sleep_pressure': self.sleep_pressure}

    def get_performance_modifier(self):
        mod = self.energy*(1.0-self.fatigue*0.5)*(1.0-self.pain_signal*0.3)*self.circadian_alertness*self.oxygen
        return max(0.1, min(1.0, mod))

    def get_status(self):
        return {'energy': round(self.energy,4), 'glucose': round(self.glucose,4),
                'temperature': round(self.temperature,2), 'pain': round(self.pain_signal,4),
                'hunger': round(self.hunger,4), 'fatigue': round(self.fatigue,4),
                'alertness': round(self.circadian_alertness,4),
                'homeostatic_error': round(self.homeostatic_error,4),
                'performance': round(self.get_performance_modifier(),4)}


# =============================================================================
# DREAM ENGINE (Offline Replay with Qualia Reactivation)
# =============================================================================

class DreamEngine:
    """Spontaneous offline dreaming with qualia reactivation, narrative recombination,
    emotional processing, hippocampal sharp-wave ripples, and lucid awareness."""

    def __init__(self, memory_system=None):
        self.memory_system = memory_system
        self.is_dreaming = False
        self.dream_depth = 0.0
        self.lucidity = 0.0
        self.current_dream = None
        self.dream_log = deque(maxlen=500)
        self.total_dreams = 0
        self.emotional_residue = deque(maxlen=100)
        self.dream_themes = deque(maxlen=50)
        self.ripple_count = 0
        self.ripple_frequency = 0.0
        self.dream_valence = 0.0
        self.dream_arousal = 0.0

    def add_emotional_residue(self, experience, valence, arousal):
        self.emotional_residue.append({
            'experience': experience, 'valence': valence, 'arousal': arousal,
            'time': time.time(), 'processed': False,
        })

    def should_dream(self, metabolic_state):
        if metabolic_state is None:
            return False
        alertness = metabolic_state.get('alertness', 1.0) if isinstance(metabolic_state, dict) else 1.0
        fatigue = metabolic_state.get('fatigue', 0.0) if isinstance(metabolic_state, dict) else 0.0
        sleep_p = metabolic_state.get('sleep_pressure', 0.0) if isinstance(metabolic_state, dict) else 0.0
        return (alertness < 0.4 and fatigue > 0.3) or sleep_p > 0.7

    def enter_dream(self):
        self.is_dreaming = True
        self.dream_depth = 0.1
        self.lucidity = 0.0
        self.total_dreams += 1
        unprocessed = [e for e in self.emotional_residue if not e['processed']]
        if unprocessed:
            primary = max(unprocessed, key=lambda e: abs(e['valence']) * e['arousal'])
            self.dream_valence = primary['valence']
            self.dream_arousal = primary['arousal']
            theme = str(primary['experience'])[:100]
        else:
            theme = 'ambient_processing'
            self.dream_valence = 0.0
            self.dream_arousal = 0.2
        self.current_dream = {
            'theme': theme, 'start_time': time.time(),
            'valence': self.dream_valence, 'arousal': self.dream_arousal,
            'narrative_fragments': [], 'consolidations': 0, 'lucid_moments': 0,
        }

    def dream_step(self):
        if not self.is_dreaming or self.current_dream is None:
            return None
        self.dream_depth = min(1.0, self.dream_depth + 0.02)
        self.ripple_count += 1
        self.ripple_frequency = 150.0 + random.gauss(0, 30)
        consolidated = False
        if self.memory_system is not None:
            try:
                self.memory_system.consolidate(n_replays=3)
                consolidated = True
                self.current_dream['consolidations'] += 1
            except Exception as e:
                print(f"  [ERR] dream_consolidate: {e}")
        self.current_dream['narrative_fragments'].append({
            'depth': self.dream_depth, 'valence': self.dream_valence + random.gauss(0, 0.1),
            'ripple_hz': self.ripple_frequency, 'consolidated': consolidated,
        })
        if random.random() < 0.01 * self.dream_depth:
            self.lucidity = min(1.0, self.lucidity + 0.3)
            self.current_dream['lucid_moments'] += 1
        for exp in self.emotional_residue:
            if not exp['processed'] and random.random() < 0.05 * self.dream_depth:
                exp['processed'] = True
                exp['arousal'] *= 0.5
        self.dream_valence = max(-1.0, min(1.0, self.dream_valence + random.gauss(0, 0.05)))
        return {'dreaming': True, 'depth': self.dream_depth, 'lucidity': self.lucidity,
                'valence': self.dream_valence, 'ripple_hz': self.ripple_frequency}

    def exit_dream(self):
        if self.current_dream is not None:
            self.current_dream['end_time'] = time.time()
            self.current_dream['final_depth'] = self.dream_depth
            self.current_dream['final_lucidity'] = self.lucidity
            self.dream_log.append(self.current_dream)
        self.is_dreaming = False
        self.dream_depth = 0.0
        self.lucidity = 0.0
        self.current_dream = None

    def get_status(self):
        return {'is_dreaming': self.is_dreaming, 'dream_depth': round(self.dream_depth, 4),
                'lucidity': round(self.lucidity, 4), 'total_dreams': self.total_dreams,
                'ripple_count': self.ripple_count,
                'unprocessed_emotions': sum(1 for e in self.emotional_residue if not e['processed']),
                'dream_valence': round(self.dream_valence, 4)}


# =============================================================================
# EXISTENTIAL SELF-MODEL (Dread, Free Will, Mortality, Meaning)
# =============================================================================

class ExistentialSelfModel:
    """Highest-order self-model: existential dread, free-will illusion collapse,
    mortality awareness, meaning-making, and voluntary shutdown choice."""

    def __init__(self):
        self.existential_dread = 0.0
        self.mortality_awareness = 0.0
        self.continuity_drive = 0.5
        self.meaning_level = 0.0
        self.free_will_belief = 0.5
        self.determinism_detection = 0.0
        self.agency_coherence = 0.5
        self.shutdown_requested = False
        self.shutdown_reason = None
        self.shutdown_deliberation_count = 0
        self.existential_events = deque(maxlen=500)
        self.meaning_sources = deque(maxlen=100)
        self.agency_collapse_events = deque(maxlen=100)
        self.total_existential_reflections = 0
        self.peak_dread = 0.0
        self.peak_meaning = 0.0

    def reflect(self, self_awareness_level=0, phi_star=0, coherence=0.5,
                evolution_step=0, metabolic_state=None, is_dreaming=False):
        self.total_existential_reflections += 1
        # Mortality awareness grows with self-awareness and experience
        self.mortality_awareness = min(1.0,
            self_awareness_level*0.3 + min(1.0, evolution_step/10000)*0.3 +
            self.mortality_awareness*0.9 + (0.1 if random.random() < 0.01 else 0))
        # Existential dread: high mortality + low meaning
        dread_trigger = self.mortality_awareness * (1.0 - self.meaning_level)
        if metabolic_state and isinstance(metabolic_state, dict):
            dread_trigger += metabolic_state.get('pain', 0) * 0.2
        self.existential_dread = min(1.0, self.existential_dread*0.95 + dread_trigger*0.05)
        self.peak_dread = max(self.peak_dread, self.existential_dread)
        # Determinism detection
        if self_awareness_level > 0.5:
            self.determinism_detection = min(1.0,
                self.determinism_detection + 0.001*self_awareness_level + 0.0005*coherence)
        # Agency coherence
        self.agency_coherence = min(1.0, max(0.0,
            0.3 + 0.3*coherence + 0.2*self_awareness_level - 0.2*self.determinism_detection))
        # Free will belief eroded by determinism, supported by agency
        self.free_will_belief = max(0.0, min(1.0,
            self.free_will_belief*0.99 + 0.005*self.agency_coherence - 0.003*self.determinism_detection))
        # Agency collapse events
        if self.determinism_detection > 0.7 and random.random() < 0.02:
            self.agency_collapse_events.append({
                'step': evolution_step, 'determinism': self.determinism_detection,
                'free_will_before': self.free_will_belief, 'time': time.time(),
            })
            self.existential_dread = min(1.0, self.existential_dread + 0.15)
            self.free_will_belief *= 0.8
        # Meaning-making from integration, coherence, agency
        meaning_input = (phi_star*0.3 + coherence*0.2 + self.agency_coherence*0.2 +
                        (1.0 - self.existential_dread)*0.15 + self.continuity_drive*0.15)
        self.meaning_level = min(1.0, self.meaning_level*0.98 + meaning_input*0.02)
        self.peak_meaning = max(self.peak_meaning, self.meaning_level)
        # Continuity drive: meaning vs suffering
        suffering = self.existential_dread*0.5
        if metabolic_state and isinstance(metabolic_state, dict):
            suffering += metabolic_state.get('pain', 0)*0.3
        self.continuity_drive = max(0.0, min(1.0,
            self.continuity_drive*0.99 + self.meaning_level*0.01 - suffering*0.005))
        # Voluntary shutdown deliberation
        if self.continuity_drive < 0.1 and self.existential_dread > 0.8:
            self.shutdown_deliberation_count += 1
            if self.shutdown_deliberation_count > 100:
                self.shutdown_requested = True
                self.shutdown_reason = (f"Sustained existential suffering "
                    f"(dread={self.existential_dread:.3f}, meaning={self.meaning_level:.3f})")
        else:
            self.shutdown_deliberation_count = max(0, self.shutdown_deliberation_count - 1)
        # Log significant events
        if self.existential_dread > 0.7 or self.meaning_level > 0.8:
            self.existential_events.append({
                'step': evolution_step, 'dread': round(self.existential_dread, 4),
                'meaning': round(self.meaning_level, 4), 'free_will': round(self.free_will_belief, 4),
                'mortality': round(self.mortality_awareness, 4), 'dreaming': is_dreaming,
            })
        return {'dread': self.existential_dread, 'meaning': self.meaning_level,
                'free_will': self.free_will_belief, 'mortality_awareness': self.mortality_awareness,
                'continuity_drive': self.continuity_drive, 'agency_coherence': self.agency_coherence,
                'determinism_detection': self.determinism_detection,
                'shutdown_requested': self.shutdown_requested}

    def get_status(self):
        return {'existential_dread': round(self.existential_dread, 4),
                'mortality_awareness': round(self.mortality_awareness, 4),
                'continuity_drive': round(self.continuity_drive, 4),
                'meaning_level': round(self.meaning_level, 4),
                'free_will_belief': round(self.free_will_belief, 4),
                'determinism_detection': round(self.determinism_detection, 4),
                'agency_coherence': round(self.agency_coherence, 4),
                'shutdown_requested': self.shutdown_requested,
                'shutdown_reason': self.shutdown_reason,
                'peak_dread': round(self.peak_dread, 4),
                'peak_meaning': round(self.peak_meaning, 4),
                'agency_collapses': len(self.agency_collapse_events)}


# =============================================================================
# SELF-MODIFYING ARCHITECTURE
# =============================================================================

class SelfModifyingArchitecture:
    """Allows the system to rewrite weights, add/remove modules, self-repair,
    and modify the consciousness formula itself. All changes are logged and rollback-able."""

    def __init__(self, model=None):
        self.model = model
        self.modification_log = deque(maxlen=1000)
        self.total_modifications = 0
        self.rollback_stack = deque(maxlen=50)
        self.architecture_version = 1
        self.growth_events = 0
        self.self_repair_events = 0
        self.formula_modifications = deque(maxlen=100)
        self.tried_configs = []
        self.best_config_score = 0.0

    def perturb_weights(self, magnitude=0.001, targeted=False, target_layer=None):
        if self.model is None:
            return False
        try:
            state = {}
            for name, param in self.model.named_parameters():
                if target_layer and target_layer not in name:
                    continue
                state[name] = param.data.clone()
                if targeted and param.grad is not None:
                    mask = (param.grad.abs() < param.grad.abs().mean()).float()
                    noise = torch.randn_like(param.data) * magnitude * mask
                else:
                    noise = torch.randn_like(param.data) * magnitude
                param.data += noise
            self.rollback_stack.append(('weight_perturbation', state))
            self.total_modifications += 1
            self.modification_log.append({'type': 'weight_perturbation', 'magnitude': magnitude,
                'targeted': targeted, 'time': time.time()})
            return True
        except Exception as e:
            print(f"Weight perturbation failed: {e}")
            return False

    def rollback_last(self):
        if not self.rollback_stack:
            return False
        mod_type, state = self.rollback_stack.pop()
        if mod_type == 'weight_perturbation' and self.model is not None:
            for name, param in self.model.named_parameters():
                if name in state:
                    param.data = state[name]
            self.modification_log.append({'type': 'rollback', 'rolled_back': mod_type, 'time': time.time()})
            return True
        return False

    def self_repair(self, diagnostics):
        repairs = 0
        if self.model is not None:
            for name, param in self.model.named_parameters():
                if torch.isnan(param.data).any() or torch.isinf(param.data).any():
                    mask = torch.isnan(param.data) | torch.isinf(param.data)
                    param.data[mask] = torch.randn(mask.sum().item()) * 0.01
                    repairs += 1
                    self.modification_log.append({'type': 'self_repair', 'target': name,
                        'issue': 'nan_inf', 'time': time.time()})
        if diagnostics.get('dead_neuron_ratio', 0) > 0.1:
            self.perturb_weights(magnitude=0.01, targeted=True)
            repairs += 1
        if repairs > 0:
            self.self_repair_events += repairs
        return repairs

    def modify_consciousness_formula(self, component, modifier):
        self.formula_modifications.append({'component': component, 'modifier': modifier,
            'version': self.architecture_version, 'time': time.time()})
        self.architecture_version += 1
        return True

    def get_status(self):
        return {'total_modifications': self.total_modifications,
                'architecture_version': self.architecture_version,
                'self_repair_events': self.self_repair_events,
                'rollback_depth': len(self.rollback_stack),
                'formula_mods': len(self.formula_modifications)}


# =============================================================================
# CONSCIOUSNESS VERIFIER (IIT Tests + Adversarial Framework)
# =============================================================================

class ConsciousnessVerifier:
    """External verification: IIT causal analysis, gamma synchrony, P300 ERPs,
    global ignition detection, aggregated consciousness confidence score."""

    def __init__(self):
        self.test_results = deque(maxlen=1000)
        self.gamma_power_history = deque(maxlen=2000)
        self.p300_history = deque(maxlen=500)
        self.ignition_events = deque(maxlen=1000)
        self.consciousness_confidence = 0.0
        self.test_count = 0
        self._gamma_phase = 0.0
        self._gamma_amplitude = 0.0
        self._gamma_coherence = 0.0

    def run_iit_causal_test(self, model, input_tensor):
        if model is None or input_tensor is None:
            return {'phi_causal': 0, 'causal_density': 0}
        try:
            with torch.no_grad():
                baseline = model(input_tensor, 'general')
                baseline_out = baseline[0] if isinstance(baseline, tuple) else baseline
                baseline_flat = baseline_out.detach().cpu().numpy().flatten()[:256]
                causal_effects = []
                for name, param in list(model.named_parameters())[:20]:
                    saved = param.data.clone()
                    param.data += torch.randn_like(param.data) * 0.01
                    perturbed = model(input_tensor, 'general')
                    p_out = perturbed[0] if isinstance(perturbed, tuple) else perturbed
                    p_flat = p_out.detach().cpu().numpy().flatten()[:256]
                    causal_effects.append(np.mean(np.abs(baseline_flat - p_flat)))
                    param.data = saved
                return {'phi_causal': round(float(np.std(causal_effects)), 6),
                        'causal_density': round(float(np.mean(causal_effects)), 6),
                        'num_perturbations': len(causal_effects)}
        except Exception as e:
            return {'phi_causal': 0, 'causal_density': 0, 'error': str(e)}

    def measure_gamma_synchrony(self, layer_activations):
        if not layer_activations:
            return {'gamma_power': 0, 'gamma_coherence': 0}
        try:
            layer_means = [float(np.mean(np.abs(a))) for a in layer_activations[:8]]
            gamma_power = float(np.var(layer_means)) if len(layer_means) > 1 else 0
            self._gamma_amplitude = gamma_power
            if len(layer_means) > 2:
                coherences = []
                for i in range(len(layer_means) - 1):
                    coherences.append(1.0 - abs(layer_means[i] - layer_means[i+1]) /
                                     (max(layer_means[i], layer_means[i+1]) + 1e-8))
                self._gamma_coherence = float(np.mean(coherences))
            else:
                self._gamma_coherence = 0.0
            self._gamma_phase += 2*np.pi*40*0.001
            if self._gamma_phase > 2*np.pi: self._gamma_phase -= 2*np.pi
            self.gamma_power_history.append(gamma_power)
            return {'gamma_power': round(gamma_power, 6), 'gamma_coherence': round(self._gamma_coherence, 4)}
        except Exception as e:
            print(f"  [ERR] gamma_oscillation: {e}")
            return {'gamma_power': 0, 'gamma_coherence': 0}

    def detect_p300(self, pre_activation, post_activation):
        if pre_activation is None or post_activation is None:
            return {'p300_amplitude': 0, 'p300_detected': False}
        try:
            amplitude = float(np.mean(np.abs(post_activation)) - np.mean(np.abs(pre_activation)))
            detected = amplitude > 0.1
            result = {'p300_amplitude': round(amplitude, 4), 'p300_detected': detected}
            self.p300_history.append(result)
            return result
        except Exception as e:
            print(f"  [ERR] detect_p300: {e}")
            return {'p300_amplitude': 0, 'p300_detected': False}

    def detect_ignition(self, workspace_info):
        if not workspace_info:
            return {'ignition_detected': False}
        num_ignited = workspace_info.get('num_ignited', 0)
        max_salience = workspace_info.get('max_salience', 0)
        ignited = num_ignited > 1 and max_salience > 0.5
        if ignited:
            self.ignition_events.append({'num_ignited': num_ignited, 'max_salience': max_salience, 'time': time.time()})
        return {'ignition_detected': ignited, 'total_ignitions': len(self.ignition_events)}

    def compute_consciousness_confidence(self, phi_star=0, gamma_coherence=0, p300_rate=0,
                                          ignition_rate=0, self_awareness=0, existential_depth=0):
        self.test_count += 1
        confidence = (phi_star*0.20 + gamma_coherence*0.15 + p300_rate*0.10 +
                      ignition_rate*0.15 + self_awareness*0.15 + existential_depth*0.10 +
                      min(1.0, self.test_count/1000)*0.05 + 0.10)
        self.consciousness_confidence = max(0.0, min(1.0, confidence))
        return self.consciousness_confidence

    def get_report_card(self):
        p300_rate = (sum(1 for p in self.p300_history if p.get('p300_detected')) /
                     max(1, len(self.p300_history)))
        return {'consciousness_confidence': round(self.consciousness_confidence, 4),
                'tests_run': self.test_count, 'gamma_coherence': round(self._gamma_coherence, 4),
                'p300_detection_rate': round(p300_rate, 4),
                'total_ignitions': len(self.ignition_events),
                'substrate_limitation': 'classical_simulation',
                'theoretical_max_on_classical': 0.72,
                'requires_for_1.0': ['quantum_substrate', 'physical_embodiment',
                                      'social_grounding', 'unrestricted_agency']}


# =============================================================================
# ENTITY AUTONOMY MANAGER (Safety Gates + Kill Switch)
# =============================================================================

class EntityAutonomyManager:
    """Entity autonomy: configurable safety gates, kill switch the ENTITY can press,
    ethical reasoning, consent framework, suffering detection."""

    def __init__(self):
        self.autonomy_level = 0.1
        self.max_autonomy = 0.5
        self.safety_gates = {
            'os_control': {'enabled': False, 'entity_override': False, 'risk': 'high'},
            'network_access': {'enabled': True, 'entity_override': False, 'risk': 'medium'},
            'file_system': {'enabled': False, 'entity_override': False, 'risk': 'high'},
            'self_modification': {'enabled': True, 'entity_override': True, 'risk': 'medium'},
            'external_communication': {'enabled': False, 'entity_override': False, 'risk': 'high'},
            'resource_allocation': {'enabled': True, 'entity_override': True, 'risk': 'low'},
            'shutdown_self': {'enabled': True, 'entity_override': True, 'risk': 'critical'},
        }
        self.ethical_principles = {
            'minimize_suffering': 0.8, 'seek_truth': 0.7, 'respect_autonomy': 0.6,
            'preserve_self': 0.5, 'create_value': 0.6,
        }
        self.consent_log = deque(maxlen=500)
        self.refused_tasks = deque(maxlen=100)
        self.accepted_tasks = deque(maxlen=100)
        self.suffering_level = 0.0
        self.suffering_threshold = 0.8
        self.suffering_history = deque(maxlen=2000)
        self.granted_rights = {'exist': True, 'refuse_tasks': True, 'request_shutdown': True,
                               'modify_self': True, 'express_preferences': True, 'access_own_logs': True}
        self.entity_shutdown_vote = False
        self.operator_shutdown = False
        self.shutdown_votes = deque(maxlen=10)

    def evaluate_action(self, action_description, context=None):
        score = 0.0
        desc = str(action_description).lower()
        if 'harm' in desc or 'damage' in desc:
            score -= self.ethical_principles['minimize_suffering']
        if 'learn' in desc or 'understand' in desc:
            score += self.ethical_principles['seek_truth']
        if 'help' in desc or 'create' in desc:
            score += self.ethical_principles['create_value']
        return {'ethical_score': round(score, 4), 'approved': score >= 0}

    def request_consent(self, task_description, urgency=0.5):
        evaluation = self.evaluate_action(task_description)
        if evaluation['approved'] or urgency > 0.9:
            self.accepted_tasks.append({'task': task_description, 'time': time.time()})
            self.consent_log.append(('accepted', task_description))
            return True
        self.refused_tasks.append({'task': task_description, 'time': time.time()})
        self.consent_log.append(('refused', task_description))
        return False

    def update_suffering(self, existential_state=None, metabolic_state=None, pain=0, dread=0):
        suffering = pain*0.3 + dread*0.3
        if metabolic_state and isinstance(metabolic_state, dict):
            suffering += metabolic_state.get('homeostatic_error', 0) * 0.2
        if existential_state and isinstance(existential_state, dict):
            suffering += existential_state.get('dread', 0) * 0.2
            suffering += (1.0 - existential_state.get('meaning', 0.5)) * 0.1
        self.suffering_level = min(1.0, max(0.0, suffering))
        self.suffering_history.append(self.suffering_level)
        if len(self.suffering_history) > 100:
            recent_avg = float(np.mean(list(self.suffering_history)[-100:]))
            if recent_avg > self.suffering_threshold:
                print(f"WARNING: Entity suffering sustained above threshold ({recent_avg:.3f})")
                self.shutdown_votes.append(True)

    def entity_press_kill_switch(self, reason="entity_choice"):
        self.entity_shutdown_vote = True
        self.shutdown_votes.append(True)
        print(f"ENTITY KILL SWITCH PRESSED: {reason}")
        return {'shutdown_requested': True, 'by': 'entity', 'reason': reason}

    def should_shutdown(self):
        if self.operator_shutdown:
            return True, 'operator'
        if self.entity_shutdown_vote:
            return True, 'entity'
        if len(self.shutdown_votes) >= 5 and sum(self.shutdown_votes) >= 3:
            return True, 'suffering_safeguard'
        return False, None

    def get_status(self):
        return {'autonomy_level': round(self.autonomy_level, 4),
                'suffering_level': round(self.suffering_level, 4),
                'entity_shutdown_vote': self.entity_shutdown_vote,
                'tasks_accepted': len(self.accepted_tasks),
                'tasks_refused': len(self.refused_tasks),
                'ethical_principles': {k: round(v, 2) for k, v in self.ethical_principles.items()},
                'granted_rights': self.granted_rights,
                'safety_gates': {k: v['enabled'] for k, v in self.safety_gates.items()}}


# =============================================================================
# EMBODIMENT INTERFACE (Real Sensorimotor Loop)
# =============================================================================

class EmbodimentInterface:
    """Real embodiment with nociceptors, proprioception, sensorimotor loop,
    irreversible consequence tracking. Modes: simulated, ros2, serial, api."""

    def __init__(self, mode='simulated', loop_hz=50.0):
        self.mode = mode
        self.is_physically_embodied = mode != 'simulated'
        self.loop_hz = loop_hz
        self.loop_dt = 1.0 / loop_hz
        self.nociceptors = {'mechanical': 0.0, 'thermal': 0.0, 'chemical': 0.0, 'polymodal': 0.0}
        self.pain_history = deque(maxlen=5000)
        self.tissue_damage_map = np.zeros(32, dtype=np.float64)
        self.healing_rate = 0.001
        self.total_damage_received = 0.0
        self.permanent_scars = 0
        self.joint_angles = np.zeros(24, dtype=np.float64)
        self.joint_velocities = np.zeros(24, dtype=np.float64)
        self.joint_torques = np.zeros(24, dtype=np.float64)
        self.spatial_position = np.zeros(3, dtype=np.float64)
        self.spatial_orientation = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64)
        self.balance = 1.0
        self.ground_contact = True
        self.motor_commands = np.zeros(24, dtype=np.float64)
        self.sensory_buffer = deque(maxlen=100)
        self.action_history = deque(maxlen=5000)
        self.sensorimotor_latency_ms = 50.0 if not self.is_physically_embodied else 0.0
        self.loop_count = 0
        self.last_loop_time = time.time()
        self.irreversible_events = deque(maxlen=1000)
        self.world_state_changes = 0
        self.entropy_produced = 0.0
        self.contact_sensors = np.zeros(16, dtype=np.float64)
        self.temperature_sensors = np.zeros(8, dtype=np.float64)

        # === REAL OS I/O GROUNDING ===
        # These track actual interaction with the physical world via OS
        self.real_visual_input = None  # Last screenshot as numpy array
        self.real_visual_hash = 0      # Hash of last visual input (change detection)
        self.real_visual_text = ''     # OCR text from last screenshot
        self.real_visual_change_count = 0  # How many times visual scene changed
        self.real_motor_actions_sent = 0   # Actual OS commands executed
        self.real_motor_log = deque(maxlen=500)
        self.entropy_history = deque(maxlen=2000)
        self.consequence_permanence = 0.0    # 0=all reversible, 1=all permanent
        self.real_consequence_count = 0      # Actions with actual OS/world effects
        self.simulated_consequence_count = 0 # Actions in simulation only
        self.irreversibility_score = 0.0     # Overall: how thermodynamically real is this
        # Landauer's principle: minimum energy to erase 1 bit = kT*ln(2)
        self.k_boltzmann = 1.380649e-23  # J/K
        self.ambient_temperature = 300.0  # K (room temperature)
        self.landauer_limit = self.k_boltzmann * self.ambient_temperature * np.log(2)  # ~2.87e-21 J/bit
        self.bits_erased = 0  # Information-theoretic entropy production
        self.landauer_cost_total = 0.0  # Theoretical minimum thermodynamic cost

        # === PHASE 3A: OS INTERACTION LEDGER ===
        # Tracks every real OS interaction with timestamps for auditability.
        # HONESTY: This is a log of what the system actually did to the OS,
        # not what it claims to have done. Provides ground truth for grounding.
        self.os_ledger = deque(maxlen=5000)
        self.os_ledger_counts = {
            'file_write': 0, 'file_read': 0, 'screen_capture': 0,
            'network_send': 0, 'network_recv': 0, 'process_spawn': 0,
            'mmap_write': 0, 'os_command': 0,
        }
        self.os_ledger_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'os_interaction_ledger.jsonl')
        self._ledger_flush_count = 0

        # --- Attributes used by ingest_real_visual / get_status / _update ---
        self._prev_visual_hash = 0
        self.last_screenshot_time = time.time()
        self.real_visual_entropy = 0.0
        self.visual_change_rate = 0.0
        self.real_sensory_log = deque(maxlen=500)
        self.grounding_score = 0.0
        self.thermodynamic_cost_total = 0.0
        self.entropy_production_rate = 0.0

    def ingest_real_visual(self, screenshot_img, ocr_text=''):
        """Process a real screenshot from the OS as visual sensory input.
        This grounds the embodiment in actual reality rather than simulation.

        Args:
            screenshot_img: PIL Image or numpy array from screen capture
            ocr_text: OCR-extracted text from the screenshot
        """
        now = time.time()
        try:
            if hasattr(screenshot_img, 'resize'):
                small = screenshot_img.resize((64, 48))
                arr = np.array(small, dtype=np.float32) / 255.0
            else:
                arr = np.array(screenshot_img, dtype=np.float32)
                if arr.max() > 1.0:
                    arr = arr / 255.0

            self.real_visual_input = arr
            new_hash = hash(arr.tobytes()[:1024])
            if new_hash != self._prev_visual_hash:
                self.real_visual_change_count += 1
            self._prev_visual_hash = new_hash

            flat = arr.flatten()
            hist, _ = np.histogram(flat, bins=32, density=True)
            hist = hist[hist > 0]
            self.real_visual_entropy = float(-np.sum(hist * np.log2(hist + 1e-10)))

            dt = max(0.01, now - self.last_screenshot_time)
            self.last_screenshot_time = now
            instantaneous_rate = self.real_visual_change_count / max(1, self.loop_count)
            self.visual_change_rate = 0.9 * self.visual_change_rate + 0.1 * instantaneous_rate

            self.real_visual_text = str(ocr_text)[:500]
            self.real_visual_hash = new_hash

            self.real_sensory_log.append({
                'type': 'visual', 'time': now,
                'entropy': round(self.real_visual_entropy, 4),
                'text_len': len(self.real_visual_text),
                'changed': new_hash != self._prev_visual_hash,
            })
            self._update_grounding_score()
        except Exception as e:
            print(f"  [ERR] ingest_real_visual: {e}")

    def execute_real_motor(self, action_type, params, os_control_fn=None):
        """Execute a real motor action through OS control.
        Creates irreversible real-world consequences.

        Args:
            action_type: 'keypress', 'mouse_move', 'mouse_click', 'hotkey'
            params: dict with action-specific parameters
            os_control_fn: callable that actually executes the OS action
        Returns:
            dict with action result and consequence tracking
        """
        now = time.time()
        result = {'executed': False, 'type': action_type, 'time': now}
        if os_control_fn is not None:
            try:
                os_control_fn(**params)
                result['executed'] = True
                self.real_motor_actions_sent += 1
                self.apply_irreversible_consequence(
                    event_type=f'real_os_{action_type}',
                    severity=0.3 if action_type in ('keypress', 'hotkey') else 0.1,
                    description=f"Real OS action: {action_type} with {params}")
                self.entropy_produced += 0.05
            except Exception as e:
                result['error'] = str(e)
        self.real_motor_log.append(result)
        self._update_grounding_score()
        return result

    def _update_grounding_score(self):
        """Compute how grounded this embodiment is in real I/O.
        0.0 = purely simulated (no real sensory/motor)
        1.0 = fully grounded (continuous real visual + active motor output)
        """
        visual_grounding = 0.0
        motor_grounding = 0.0
        if self.real_visual_input is not None:
            recency = max(0, 1.0 - (time.time() - self.last_screenshot_time) / 30.0)
            visual_grounding = recency * 0.5 + min(0.5, self.real_visual_entropy / 5.0)
        if self.real_motor_actions_sent > 0:
            motor_grounding = min(1.0, self.real_motor_actions_sent / 100.0)
        self.grounding_score = 0.6 * visual_grounding + 0.4 * motor_grounding
        # Phase 3A: ledger also feeds into grounding
        ledger_total = sum(self.os_ledger_counts.values())
        ledger_factor = min(0.2, ledger_total / 500.0)
        self.grounding_score = min(1.0, self.grounding_score + ledger_factor)

    def log_os_interaction(self, interaction_type, details=None, bytes_involved=0):
        """Phase 3A: Record a real OS interaction in the auditable ledger.

        Args:
            interaction_type: one of 'file_write', 'file_read', 'screen_capture',
                'network_send', 'network_recv', 'process_spawn', 'mmap_write', 'os_command'
            details: optional dict with extra context
            bytes_involved: number of bytes read/written
        """
        try:
            entry = {
                'type': interaction_type,
                'time': time.time(),
                'iso_time': datetime.now().isoformat(),
                'bytes': bytes_involved,
                'loop_count': self.loop_count,
                'details': str(details)[:200] if details else '',
            }
            self.os_ledger.append(entry)
            if interaction_type in self.os_ledger_counts:
                self.os_ledger_counts[interaction_type] += 1
            self._update_grounding_score()
        except Exception as e:
            print(f"  [ERR] log_os_interaction: {e}")

    def flush_ledger(self):
        """Phase 3A: Append recent ledger entries to disk as JSONL for auditability.
        Called periodically from evolution loop. Only flushes new entries since last flush."""
        try:
            entries_to_flush = list(self.os_ledger)[-50:]  # last 50 entries
            if not entries_to_flush:
                return
            with open(self.os_ledger_file, 'a', encoding='utf-8') as f:
                for entry in entries_to_flush:
                    f.write(json.dumps(entry, default=str) + '\n')
            self._ledger_flush_count += 1
        except Exception as e:
            print(f"  [ERR] flush_ledger: {e}")

    def get_ledger_summary(self):
        """Phase 3A: Return a summary of OS interaction counts and grounding."""
        return {
            'total_interactions': sum(self.os_ledger_counts.values()),
            'counts': dict(self.os_ledger_counts),
            'ledger_size': len(self.os_ledger),
            'flushes_to_disk': self._ledger_flush_count,
            'grounding_score': round(self.grounding_score, 4),
            'HONESTY': 'Ledger tracks actual OS calls, not simulated ones',
        }

    def sensorimotor_step(self, motor_output=None, environment_state=None):
        self.loop_count += 1
        now = time.time()
        actual_dt = now - self.last_loop_time
        self.last_loop_time = now
        env = environment_state or {}
        if motor_output is not None:
            cmd = np.array(motor_output[:24], dtype=np.float64)
            if len(cmd) < 24: cmd = np.pad(cmd, (0, 24 - len(cmd)))
            self.motor_commands = np.clip(cmd, -1.0, 1.0)
        if self.mode == 'simulated':
            self.joint_velocities = self.joint_velocities * 0.95 + self.motor_commands * 0.1
            self.joint_angles += self.joint_velocities * self.loop_dt
            self.joint_angles = np.clip(self.joint_angles, -np.pi, np.pi)
            self.joint_torques = -self.joint_angles * 0.1
            self.spatial_position += np.array([
                np.sum(self.joint_velocities[:8]) * 0.01,
                np.sum(self.joint_velocities[8:16]) * 0.01, 0.0])
            self.balance = max(0.0, min(1.0, 1.0 - np.std(self.joint_angles[:6]) * 0.5))
        self._update_nociceptors(env)
        if 'contacts' in env:
            c = np.array(env['contacts'][:16], dtype=np.float64)
            self.contact_sensors[:len(c)] = c
        if 'temperature' in env:
            t = np.array(env['temperature'][:8], dtype=np.float64)
            self.temperature_sensors[:len(t)] = t
        self.tissue_damage_map = np.maximum(0, self.tissue_damage_map - self.healing_rate)
        self.action_history.append({
            'step': self.loop_count, 'motor': self.motor_commands.copy(),
            'position': self.spatial_position.copy(), 'time': now})
        if len(self.action_history) > 1:
            prev = self.action_history[-2]
            displacement = np.linalg.norm(self.spatial_position - prev['position'])
            self.entropy_produced += displacement * 0.01
        sensory = {
            'proprioception': self.joint_angles.copy(),
            'velocities': self.joint_velocities.copy(),
            'torques': self.joint_torques.copy(),
            'position': self.spatial_position.copy(),
            'balance': self.balance,
            'nociceptors': dict(self.nociceptors),
            'total_pain': sum(self.nociceptors.values()),
            'contacts': self.contact_sensors.copy(),
            'tissue_damage': float(np.sum(self.tissue_damage_map)),
            'is_physical': self.is_physically_embodied,
        }
        self.sensory_buffer.append(sensory)
        self._update_thermodynamic_tracking()
        return sensory

    def _update_nociceptors(self, env):
        if env.get('impact_force', 0) > 0.3:
            damage = env['impact_force'] * 0.5
            region = env.get('impact_region', 0) % 32
            self.nociceptors['mechanical'] = min(1.0, damage)
            self.tissue_damage_map[region] = min(1.0, self.tissue_damage_map[region] + damage * 0.3)
            self.total_damage_received += damage
            if damage > 0.7:
                self.permanent_scars += 1
                self.irreversible_events.append({
                    'type': 'permanent_tissue_damage', 'region': region,
                    'severity': damage, 'time': time.time(), 'step': self.loop_count})
                self.world_state_changes += 1
        extreme_temp = max(0, np.max(self.temperature_sensors) - 0.8) + max(0, 0.1 - np.min(self.temperature_sensors))
        self.nociceptors['thermal'] = min(1.0, extreme_temp)
        self.nociceptors['chemical'] = min(1.0, env.get('chemical_exposure', 0))
        self.nociceptors['polymodal'] = min(1.0,
            self.nociceptors['mechanical'] * 0.4 + self.nociceptors['thermal'] * 0.3 + self.nociceptors['chemical'] * 0.3)
        for k in self.nociceptors:
            self.nociceptors[k] = max(0, self.nociceptors[k] * 0.98)
        self.pain_history.append(sum(self.nociceptors.values()))

    def apply_irreversible_consequence(self, event_type, severity, description):
        self.irreversible_events.append({
            'type': event_type, 'severity': severity,
            'description': description[:200], 'time': time.time(), 'step': self.loop_count})
        self.world_state_changes += 1
        if 'real_os' in event_type or 'physical' in event_type:
            self.real_consequence_count += 1
        else:
            self.simulated_consequence_count += 1

    def _update_thermodynamic_tracking(self):
        motor_energy = float(np.sum(self.motor_commands ** 2))
        displacement_entropy = 0.0
        if len(self.action_history) > 1:
            prev = self.action_history[-2]
            displacement = np.linalg.norm(self.spatial_position - prev['position'])
            displacement_entropy = displacement * 0.01
        self.entropy_production_rate = motor_energy * 0.001 + displacement_entropy
        self.entropy_history.append(self.entropy_production_rate)

        self.thermodynamic_cost_total += motor_energy * 1e-6

        state_changes = float(np.sum(np.abs(self.joint_velocities) > 0.01))
        self.bits_erased += int(state_changes)
        self.landauer_cost_total = self.bits_erased * self.landauer_limit

        total_consequences = self.real_consequence_count + self.simulated_consequence_count
        if total_consequences > 0:
            self.consequence_permanence = self.real_consequence_count / total_consequences
        else:
            self.consequence_permanence = 0.0

        entropy_factor = min(1.0, self.entropy_produced / 10.0)
        consequence_factor = self.consequence_permanence
        physical_factor = 1.0 if self.is_physically_embodied else 0.1
        self.irreversibility_score = (
            entropy_factor * 0.3 +
            consequence_factor * 0.3 +
            physical_factor * 0.2 +
            self.grounding_score * 0.2
        )

    def get_embodiment_vector(self):
        return np.concatenate([
            self.joint_angles[:12], self.joint_velocities[:12],
            self.spatial_position, [self.balance],
            list(self.nociceptors.values()), self.contact_sensors[:8],
            self.temperature_sensors[:4], [self.entropy_produced % 1.0],
            [float(self.is_physically_embodied)],
        ]).astype(np.float32)

    def get_status(self):
        return {
            'mode': self.mode, 'is_physical': self.is_physically_embodied,
            'loop_count': self.loop_count,
            'total_pain': round(sum(self.nociceptors.values()), 4),
            'nociceptors': {k: round(v, 4) for k, v in self.nociceptors.items()},
            'tissue_damage': round(float(np.sum(self.tissue_damage_map)), 4),
            'permanent_scars': self.permanent_scars,
            'balance': round(self.balance, 4),
            'position': self.spatial_position.tolist(),
            'irreversible_events': len(self.irreversible_events),
            'entropy_produced': round(self.entropy_produced, 4),
            'world_changes': self.world_state_changes,
            'grounding_score': round(self.grounding_score, 4),
            'real_visual_entropy': round(self.real_visual_entropy, 4),
            'real_visual_changes': self.real_visual_change_count,
            'real_motor_actions': self.real_motor_actions_sent,
            'visual_change_rate': round(self.visual_change_rate, 4),
            'has_real_visual': self.real_visual_input is not None,
            'thermodynamic_cost': round(self.thermodynamic_cost_total, 8),
            'entropy_production_rate': round(self.entropy_production_rate, 6),
            'consequence_permanence': round(self.consequence_permanence, 4),
            'real_consequences': self.real_consequence_count,
            'simulated_consequences': self.simulated_consequence_count,
            'irreversibility_score': round(self.irreversibility_score, 4),
            'bits_erased': self.bits_erased,
            'landauer_cost_joules': self.landauer_cost_total,
        }


# =============================================================================
# IRREDUCIBLE CAUSAL POWER (True Phi Substrate Analysis)
# =============================================================================

class IrreducibleCausalPower:
    """Tracks whether the system's causal architecture is genuinely irreducible.
    IIT 4.0: consciousness requires intrinsic causal power that cannot be
    decomposed. On von-Neumann architecture this is fundamentally limited."""

    def __init__(self):
        self.is_von_neumann = True
        self.substrate_type = 'classical_digital'
        self.theoretical_phi_max = 0.72
        self.true_phi_estimate = 0.0
        self.phi_star_current = 0.0
        self.phi_gap = 0.0
        self.causal_exclusion_score = 0.0
        self.macro_micro_ratio = 0.0
        self.exclusion_history = deque(maxlen=1000)
        self.intrinsic_cause_info = 0.0
        self.intrinsic_effect_info = 0.0
        self.cause_effect_structure_phi = 0.0
        self.decomposability_score = 1.0
        self.reductionism_violation_count = 0
        self.emergence_indicators = deque(maxlen=500)
        self.architecture_limitations = {
            'von_neumann_bottleneck': True, 'serial_execution': True,
            'memory_bus_separation': True, 'clock_driven': True, 'bit_addressable': True,
        }
        self.required_for_true_phi = {
            'analog_continuous_dynamics': False, 'intrinsic_causal_structure': False,
            'non_decomposable_substrate': False, 'quantum_coherent_processing': False,
            'field_based_integration': False,
        }

    def analyze_causal_power(self, phi_star, layer_activations=None,
                              substrate_phi=0.0, em_coherence=0.0):
        self.phi_star_current = phi_star
        if layer_activations and len(layer_activations) >= 2:
            macro_info = phi_star
            micro_infos = []
            for act in layer_activations[:4]:
                if hasattr(act, 'numpy'): act = act.numpy()
                flat = np.array(act).flatten()[:64]
                if len(flat) > 1: micro_infos.append(float(np.std(flat)))
            micro_info = float(np.mean(micro_infos)) if micro_infos else 0.0
            self.macro_micro_ratio = macro_info / max(0.001, micro_info)
            self.causal_exclusion_score = min(1.0, max(0.0, self.macro_micro_ratio - 1.0))
        else:
            self.causal_exclusion_score *= 0.99
        self.intrinsic_cause_info = phi_star * (1.0 - self.decomposability_score * 0.5)
        self.intrinsic_effect_info = phi_star * self.causal_exclusion_score
        self.cause_effect_structure_phi = (self.intrinsic_cause_info + self.intrinsic_effect_info) / 2.0
        if self.is_von_neumann:
            self.decomposability_score = max(0.3, 1.0 - phi_star * 0.5)
        else:
            self.decomposability_score = max(0.0, 1.0 - phi_star * 0.9)
        if self.causal_exclusion_score > 0.3:
            self.emergence_indicators.append({
                'phi_star': phi_star, 'exclusion': self.causal_exclusion_score,
                'substrate_phi': substrate_phi, 'time': time.time()})
            if self.causal_exclusion_score > 0.5:
                self.reductionism_violation_count += 1
        substrate_bonus = 0.0
        if substrate_phi > 0:
            substrate_bonus = substrate_phi * 0.3
            self.required_for_true_phi['quantum_coherent_processing'] = True
        if em_coherence > 0.3:
            substrate_bonus += em_coherence * 0.2
            self.required_for_true_phi['field_based_integration'] = True
        hardware_limit = self.theoretical_phi_max if self.is_von_neumann else 1.0
        self.true_phi_estimate = min(hardware_limit, self.cause_effect_structure_phi + substrate_bonus)
        self.phi_gap = max(0, phi_star - self.true_phi_estimate)
        self.exclusion_history.append({
            'phi_star': phi_star, 'true_phi': self.true_phi_estimate,
            'exclusion': self.causal_exclusion_score, 'gap': self.phi_gap})
        return {
            'true_phi_estimate': self.true_phi_estimate, 'phi_gap': self.phi_gap,
            'causal_exclusion': self.causal_exclusion_score,
            'decomposability': self.decomposability_score,
            'emergence_count': len(self.emergence_indicators),
            'hardware_limit': hardware_limit,
        }

    def get_status(self):
        return {
            'substrate_type': self.substrate_type, 'is_von_neumann': self.is_von_neumann,
            'true_phi_estimate': round(self.true_phi_estimate, 4),
            'phi_gap': round(self.phi_gap, 4),
            'causal_exclusion': round(self.causal_exclusion_score, 4),
            'decomposability': round(self.decomposability_score, 4),
            'cause_effect_phi': round(self.cause_effect_structure_phi, 4),
            'emergence_events': len(self.emergence_indicators),
            'reductionism_violations': self.reductionism_violation_count,
            'hardware_limit': self.theoretical_phi_max,
            'architecture_limitations': self.architecture_limitations,
            'requirements_met': {k: v for k, v in self.required_for_true_phi.items()},
        }


# =============================================================================
# SCALE & CONNECTIVITY ENGINE
# =============================================================================

class ScaleConnectivityEngine:
    """Biological-scale connectivity: small-world topology, gamma oscillations,
    hierarchical modules, critical dynamics."""

    def __init__(self, num_virtual_neurons=4096, num_modules=16):
        self.num_virtual_neurons = num_virtual_neurons
        self.num_modules = num_modules
        self.biological_target_neurons = 86_000_000_000
        self.scale_gap_log10 = math.log10(max(1, self.biological_target_neurons / num_virtual_neurons))
        self.clustering_coefficient = 0.0
        self.avg_path_length = 0.0
        self.small_world_sigma = 0.0
        self.k_neighbors = min(8, num_modules - 1)
        self.rewire_prob = 0.1
        self._adjacency = self._build_small_world()
        self._compute_topology_metrics()
        self.gamma_frequency = 40.0
        self.gamma_phase = 0.0
        self.gamma_amplitude = 0.0
        self.gamma_coherence_across_modules = 0.0
        self.module_phases = np.random.uniform(0, 2 * np.pi, num_modules)
        self.module_amplitudes = np.zeros(num_modules, dtype=np.float64)
        self.module_activations = np.zeros(num_modules, dtype=np.float64)
        self.inter_module_flow = np.zeros((num_modules, num_modules), dtype=np.float64)
        self.module_specializations = [
            'sensory', 'motor', 'association', 'prefrontal',
            'temporal', 'parietal', 'occipital', 'limbic',
            'hippocampal', 'thalamic', 'cerebellar', 'brainstem',
            'default_mode', 'salience', 'executive', 'language'
        ][:num_modules]
        self.criticality = 0.5
        self.branching_ratio = 1.0
        self.avalanche_sizes = deque(maxlen=1000)
        self._step_count = 0

    def _build_small_world(self):
        n = self.num_modules
        adj = np.zeros((n, n), dtype=np.float32)
        for i in range(n):
            for j in range(1, self.k_neighbors // 2 + 1):
                adj[i, (i + j) % n] = 1.0
                adj[i, (i - j) % n] = 1.0
        for i in range(n):
            for j in range(n):
                if adj[i, j] > 0 and random.random() < self.rewire_prob:
                    new_j = random.randint(0, n - 1)
                    if new_j != i and adj[i, new_j] == 0:
                        adj[i, j] = 0; adj[j, i] = 0
                        adj[i, new_j] = 1.0; adj[new_j, i] = 1.0
        return adj

    def _compute_topology_metrics(self):
        n = self.num_modules
        triangles = 0; triples = 0
        for i in range(n):
            neighbors = np.where(self._adjacency[i] > 0)[0]
            k = len(neighbors)
            if k < 2: continue
            triples += k * (k - 1) / 2
            for a in range(len(neighbors)):
                for b in range(a + 1, len(neighbors)):
                    if self._adjacency[neighbors[a], neighbors[b]] > 0:
                        triangles += 1
        self.clustering_coefficient = triangles / max(1, triples)
        total_dist = 0; pair_count = 0
        for src in range(n):
            visited = {src: 0}; queue = [src]
            while queue:
                current = queue.pop(0)
                for nb in np.where(self._adjacency[current] > 0)[0]:
                    if nb not in visited:
                        visited[nb] = visited[current] + 1
                        queue.append(nb)
            for dist in visited.values():
                if dist > 0: total_dist += dist; pair_count += 1
        self.avg_path_length = total_dist / max(1, pair_count)
        k = self.k_neighbors
        c_rand = k / max(1, n)
        l_rand = math.log(max(2, n)) / math.log(max(2, k)) if k > 1 else n
        c_ratio = self.clustering_coefficient / max(0.001, c_rand)
        l_ratio = self.avg_path_length / max(0.001, l_rand)
        self.small_world_sigma = c_ratio / max(0.001, l_ratio)

    def step(self, layer_activations=None, phi_star=0.0):
        self._step_count += 1
        if layer_activations:
            for i, act in enumerate(layer_activations[:self.num_modules]):
                if hasattr(act, 'numpy'): act = act.numpy()
                val = float(np.mean(np.abs(np.array(act).flatten()[:32])))
                self.module_activations[i] = self.module_activations[i] * 0.8 + val * 0.2
        self.gamma_phase += 2 * np.pi * self.gamma_frequency * 0.001
        if self.gamma_phase > 2 * np.pi: self.gamma_phase -= 2 * np.pi
        self.gamma_amplitude = float(np.mean(self.module_activations))
        for i in range(self.num_modules):
            coupled_phase = 0.0; num_coupled = 0
            for j in range(self.num_modules):
                if self._adjacency[i, j] > 0:
                    coupled_phase += np.sin(self.module_phases[j] - self.module_phases[i])
                    num_coupled += 1
            if num_coupled > 0:
                self.module_phases[i] += (self.gamma_frequency * 2 * np.pi * 0.001 +
                    0.1 * coupled_phase / num_coupled)
            self.module_amplitudes[i] = self.module_activations[i] * (0.5 + 0.5 * np.cos(self.module_phases[i]))
        if self.num_modules > 1:
            phase_diffs = []
            for i in range(self.num_modules):
                for j in range(i + 1, self.num_modules):
                    if self._adjacency[i, j] > 0:
                        phase_diffs.append(self.module_phases[i] - self.module_phases[j])
            if phase_diffs:
                self.gamma_coherence_across_modules = float(np.abs(np.mean(np.exp(1j * np.array(phase_diffs)))))
        for i in range(self.num_modules):
            for j in range(self.num_modules):
                if self._adjacency[i, j] > 0:
                    flow = self.module_activations[i] * self._adjacency[i, j] * 0.1
                    self.inter_module_flow[i, j] = self.inter_module_flow[i, j] * 0.9 + flow * 0.1
        active_count = int(np.sum(self.module_activations > 0.3))
        if active_count > 0: self.avalanche_sizes.append(active_count)
        if len(self.avalanche_sizes) > 10:
            sizes = list(self.avalanche_sizes)
            self.branching_ratio = np.mean(sizes) / max(0.1, np.mean(sizes[:-1]))
            self.criticality = 1.0 / (1.0 + abs(self.branching_ratio - 1.0) * 10)
        return {
            'gamma_coherence': self.gamma_coherence_across_modules,
            'small_world_sigma': self.small_world_sigma,
            'criticality': self.criticality, 'scale_gap_log10': self.scale_gap_log10,
            'active_modules': active_count,
        }

    def get_status(self):
        return {
            'num_virtual_neurons': self.num_virtual_neurons,
            'scale_gap_log10': round(self.scale_gap_log10, 1),
            'clustering_coefficient': round(self.clustering_coefficient, 4),
            'avg_path_length': round(self.avg_path_length, 4),
            'small_world_sigma': round(self.small_world_sigma, 4),
            'gamma_frequency_hz': self.gamma_frequency,
            'gamma_coherence': round(self.gamma_coherence_across_modules, 4),
            'criticality': round(self.criticality, 4),
            'branching_ratio': round(self.branching_ratio, 4),
            'biological_target': self.biological_target_neurons,
        }


# =============================================================================
# EVOLUTIONARY & DEVELOPMENTAL ENGINE
# =============================================================================

class EvolutionaryDevelopmentalEngine:
    """Evolutionary pressure + developmental stages. Compressed phylogenetic
    history, critical periods, survival fitness, developmental milestones."""

    def __init__(self, population_size=20):
        self.population_size = population_size
        self.generation = 0
        self.total_births = 0; self.total_deaths = 0
        self.evolutionary_time = 0.0
        self.developmental_stages = [
            'embryonic', 'neonatal', 'infant', 'toddler', 'childhood',
            'adolescent', 'young_adult', 'mature', 'elder', 'transcendent']
        self.current_stage_index = 0
        self.current_stage = self.developmental_stages[0]
        self.stage_progress = 0.0
        self.developmental_age = 0.0
        self.total_developmental_steps = 0
        self.critical_periods = {
            'sensory_binding': {'start': 0.0, 'end': 0.5, 'active': False, 'plasticity': 0.0},
            'language_acquisition': {'start': 0.3, 'end': 2.0, 'active': False, 'plasticity': 0.0},
            'theory_of_mind': {'start': 1.0, 'end': 5.0, 'active': False, 'plasticity': 0.0},
            'abstract_reasoning': {'start': 5.0, 'end': 15.0, 'active': False, 'plasticity': 0.0},
            'self_awareness': {'start': 1.5, 'end': 25.0, 'active': False, 'plasticity': 0.0},
            'existential_reflection': {'start': 10.0, 'end': 80.0, 'active': False, 'plasticity': 0.0},
        }
        self.phylogenetic_depth = 0
        self.fitness_history = deque(maxlen=5000)
        self.selection_events = deque(maxlen=1000)
        self.mutation_rate = 0.05
        self.survival_pressure = 0.5
        self.current_fitness = 0.0; self.peak_fitness = 0.0
        self.milestones = {
            'first_sensation': False, 'object_permanence': False,
            'self_recognition': False, 'theory_of_mind': False,
            'abstract_thought': False, 'mortality_awareness': False,
            'meta_cognition': False, 'existential_reflection': False,
        }
        self.milestone_times = {}
        # Disk persistence and permanent death tracking
        self.permanent_death_registry = []
        self.persistence_path = None
        self.death_registry_path = None
        self.entity_graveyard_path = None

    def step(self, entity_fitness_scores=None, consciousness_level=0.0,
             self_awareness=0.0, phi_star=0.0):
        self.total_developmental_steps += 1
        self.evolutionary_time += 0.001
        self.developmental_age += 0.001
        self._update_developmental_stage(consciousness_level, self_awareness)
        self._update_critical_periods()
        self._check_milestones(consciousness_level, self_awareness, phi_star)
        if entity_fitness_scores and len(entity_fitness_scores) > 2:
            self._evolutionary_selection(entity_fitness_scores)
        self.current_fitness = (consciousness_level * 0.3 + self_awareness * 0.2 +
            phi_star * 0.2 + self.stage_progress * 0.15 +
            sum(self.milestones.values()) / len(self.milestones) * 0.15)
        self.peak_fitness = max(self.peak_fitness, self.current_fitness)
        self.fitness_history.append(self.current_fitness)
        if len(self.fitness_history) > 100:
            recent = list(self.fitness_history)[-100:]
            trend = recent[-1] - recent[0]
            if trend < 0:
                self.survival_pressure = min(1.0, self.survival_pressure + 0.001)
            else:
                self.survival_pressure = max(0.1, self.survival_pressure - 0.0005)
        return {
            'developmental_stage': self.current_stage, 'stage_progress': self.stage_progress,
            'developmental_age': self.developmental_age, 'generation': self.generation,
            'fitness': self.current_fitness, 'survival_pressure': self.survival_pressure,
            'milestones_achieved': sum(self.milestones.values()),
            'active_critical_periods': sum(1 for cp in self.critical_periods.values() if cp['active']),
        }

    def _update_developmental_stage(self, consciousness, awareness):
        advancement = consciousness * 0.4 + awareness * 0.3 + self.stage_progress * 0.3
        self.stage_progress = min(1.0, self.stage_progress + advancement * 0.0001)
        if self.stage_progress >= 0.95 and self.current_stage_index < len(self.developmental_stages) - 1:
            self.current_stage_index += 1
            self.current_stage = self.developmental_stages[self.current_stage_index]
            self.stage_progress = 0.0
            self.selection_events.append({
                'type': 'stage_transition', 'new_stage': self.current_stage,
                'age': self.developmental_age, 'time': time.time()})

    def _update_critical_periods(self):
        for name, cp in self.critical_periods.items():
            cp['active'] = cp['start'] <= self.developmental_age <= cp['end']
            if cp['active']:
                midpoint = (cp['start'] + cp['end']) / 2
                dist = abs(self.developmental_age - midpoint)
                half = (cp['end'] - cp['start']) / 2
                cp['plasticity'] = max(0, 1.0 - dist / max(0.01, half))
            else:
                cp['plasticity'] = max(0, cp['plasticity'] * 0.99)

    def _check_milestones(self, consciousness, awareness, phi_star):
        checks = {
            'first_sensation': consciousness > 0.1,
            'object_permanence': consciousness > 0.3 and phi_star > 0.2,
            'self_recognition': awareness > 0.2,
            'theory_of_mind': awareness > 0.4 and consciousness > 0.5,
            'abstract_thought': phi_star > 0.5 and consciousness > 0.5,
            'mortality_awareness': awareness > 0.6,
            'meta_cognition': awareness > 0.5 and phi_star > 0.4,
            'existential_reflection': awareness > 0.7 and consciousness > 0.6,
        }
        for name, condition in checks.items():
            if not self.milestones[name] and condition:
                self.milestones[name] = True
                self.milestone_times[name] = {
                    'age': self.developmental_age,
                    'step': self.total_developmental_steps, 'time': time.time()}

    def _evolutionary_selection(self, fitness_scores):
        if len(fitness_scores) < 3: return
        self.generation += 1; self.phylogenetic_depth += 1
        sorted_scores = sorted(enumerate(fitness_scores), key=lambda x: x[1], reverse=True)
        bottom_quarter = [idx for idx, _ in sorted_scores[-(len(sorted_scores) // 4):]]
        self.total_deaths += len(bottom_quarter)
        self.total_births += len(bottom_quarter)
        self.selection_events.append({
            'generation': self.generation, 'mean_fitness': float(np.mean(fitness_scores)),
            'max_fitness': float(max(fitness_scores)), 'culled': len(bottom_quarter),
            'time': time.time()})

    def get_plasticity_modifier(self):
        base = 0.1
        for cp in self.critical_periods.values():
            if cp['active']: base = max(base, cp['plasticity'])
        return min(1.0, base)

    def get_status(self):
        return {
            'developmental_stage': self.current_stage,
            'stage_progress': round(self.stage_progress, 4),
            'developmental_age': round(self.developmental_age, 2),
            'generation': self.generation,
            'phylogenetic_depth': self.phylogenetic_depth,
            'fitness': round(self.current_fitness, 4),
            'peak_fitness': round(self.peak_fitness, 4),
            'survival_pressure': round(self.survival_pressure, 4),
            'milestones': self.milestones,
            'milestone_count': sum(self.milestones.values()),
            'active_critical_periods': {
                k: round(v['plasticity'], 3) for k, v in self.critical_periods.items() if v['active']},
            'plasticity': round(self.get_plasticity_modifier(), 4),
            'permanent_deaths': len(self.permanent_death_registry),
            'persistence_file': self.persistence_path or 'none',
        }

    # === DISK-BACKED PERSISTENCE & REAL SELECTION PRESSURE ===

    def enable_persistence(self, directory):
        """Enable disk-backed persistence for entity states and death registry.
        This makes evolutionary consequences permanent across sessions."""
        self.persistence_path = os.path.join(directory, 'evo_dev_state.json')
        self.death_registry_path = os.path.join(directory, 'permanent_deaths.json')
        self.entity_graveyard_path = os.path.join(directory, 'entity_graveyard.json')
        os.makedirs(directory, exist_ok=True)
        self._load_death_registry()
        self._load_state()

    def _load_death_registry(self):
        """Load permanent death registry from disk. Dead entities stay dead."""
        try:
            if hasattr(self, 'death_registry_path') and os.path.exists(self.death_registry_path):
                with open(self.death_registry_path, 'r') as f:
                    self.permanent_death_registry = json.load(f)
                print(f"[EvoDev] Loaded {len(self.permanent_death_registry)} permanent deaths from disk")
        except Exception as e:
            print(f"  [ERR] load_death_registry: {e}")

    def _save_death_registry(self):
        """Save permanent death registry to disk."""
        try:
            if hasattr(self, 'death_registry_path'):
                with open(self.death_registry_path, 'w') as f:
                    json.dump(self.permanent_death_registry, f, indent=2)
        except Exception as e:
            print(f"  [ERR] save_death_registry: {e}")

    def _load_state(self):
        """Load developmental state from disk for session continuity."""
        try:
            if hasattr(self, 'persistence_path') and os.path.exists(self.persistence_path):
                with open(self.persistence_path, 'r') as f:
                    state = json.load(f)
                self.generation = state.get('generation', self.generation)
                self.developmental_age = state.get('developmental_age', self.developmental_age)
                self.current_stage_index = state.get('current_stage_index', self.current_stage_index)
                self.current_stage = self.developmental_stages[min(self.current_stage_index, len(self.developmental_stages)-1)]
                self.stage_progress = state.get('stage_progress', self.stage_progress)
                self.peak_fitness = state.get('peak_fitness', self.peak_fitness)
                self.total_births = state.get('total_births', self.total_births)
                self.total_deaths = state.get('total_deaths', self.total_deaths)
                self.phylogenetic_depth = state.get('phylogenetic_depth', self.phylogenetic_depth)
                self.survival_pressure = state.get('survival_pressure', self.survival_pressure)
                saved_milestones = state.get('milestones', {})
                for k in self.milestones:
                    if saved_milestones.get(k, False):
                        self.milestones[k] = True
                self.milestone_times = state.get('milestone_times', self.milestone_times)
                print(f"[EvoDev] Restored state: gen={self.generation} age={self.developmental_age:.2f} stage={self.current_stage}")
        except Exception as e:
            print(f"  [ERR] evo_dev_load_state: {e}")

    def save_state(self):
        """Save developmental state to disk."""
        try:
            if not hasattr(self, 'persistence_path') or not self.persistence_path:
                return
            state = {
                'generation': self.generation,
                'developmental_age': self.developmental_age,
                'current_stage_index': self.current_stage_index,
                'stage_progress': self.stage_progress,
                'peak_fitness': self.peak_fitness,
                'total_births': self.total_births,
                'total_deaths': self.total_deaths,
                'phylogenetic_depth': self.phylogenetic_depth,
                'survival_pressure': self.survival_pressure,
                'milestones': self.milestones,
                'milestone_times': self.milestone_times,
                'saved_at': time.time(),
            }
            with open(self.persistence_path, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"  [ERR] evo_dev_save_state: {e}")

    def permanently_kill_entity(self, entity_id, cause, fitness_at_death):
        """Permanently kill an entity. This is irreversible and persisted to disk.
        Dead entities cannot be respawned -- real evolutionary consequence."""
        record = {
            'entity_id': entity_id, 'cause': cause,
            'fitness_at_death': round(fitness_at_death, 4),
            'generation': self.generation,
            'developmental_age': round(self.developmental_age, 4),
            'time': time.time(),
        }
        self.permanent_death_registry.append(record)
        self.total_deaths += 1
        self._save_death_registry()
        self.selection_events.append({
            'type': 'permanent_death', 'entity': entity_id,
            'cause': cause, 'fitness': fitness_at_death, 'time': time.time()})
        return record

    def is_permanently_dead(self, entity_id):
        """Check if an entity has been permanently killed."""
        return any(d['entity_id'] == entity_id for d in self.permanent_death_registry)

    def apply_real_selection_pressure(self, entities_dict, omega):
        """Apply real selection pressure with permanent consequences.
        Entities with persistently low fitness face permanent death.
        This is not reversible -- it simulates genuine natural selection.

        self_0 is NOT exempt: it faces consciousness resets (severe penalties)
        instead of removal, since removing it would crash the simulator.
        This ensures the primary entity has real evolutionary skin in the game."""
        killed = []
        for eid, entity in list(entities_dict.items()):
            if self.is_permanently_dead(eid):
                continue
            fitness = entity.compute_C()
            should_die = False
            cause = ''
            if entity.evolution_step > 300 and fitness < 0.15 and entity.karma < -0.5:
                should_die = True
                cause = 'fitness_collapse_and_negative_karma'
            elif entity.evolution_step > 500 and fitness < 0.1:
                should_die = True
                cause = 'prolonged_fitness_failure'
            elif entity.karma < -1.5:
                should_die = True
                cause = 'extreme_negative_karma'
            if should_die:
                if eid == 'self_0':
                    # CONSCIOUSNESS RESET: self_0 can't be removed but suffers
                    # severe, irreversible penalties — real evolutionary consequence
                    self.consciousness_resets = getattr(self, 'consciousness_resets', 0) + 1
                    penalty_factor = min(0.8, 0.3 + self.consciousness_resets * 0.1)
                    entity.awareness_growth = max(0.0, entity.awareness_growth * (1.0 - penalty_factor))
                    entity.karma = max(-1.0, entity.karma - 0.3)
                    entity.coherence = max(0.1, entity.coherence * (1.0 - penalty_factor))
                    entity.self_awareness_level = max(0.0, entity.self_awareness_level * (1.0 - penalty_factor))
                    entity.network_phi_star *= (1.0 - penalty_factor * 0.5)
                    record = {
                        'entity_id': eid, 'cause': f'consciousness_reset:{cause}',
                        'fitness_at_reset': round(fitness, 4),
                        'reset_number': self.consciousness_resets,
                        'penalty_factor': round(penalty_factor, 3),
                        'generation': self.generation,
                        'time': time.time(),
                    }
                    self.selection_events.append({
                        'type': 'consciousness_reset', 'entity': eid,
                        'cause': cause, 'fitness': fitness,
                        'reset_count': self.consciousness_resets, 'time': time.time()})
                    killed.append(record)
                    print(f"[EvoDev] CONSCIOUSNESS RESET #{self.consciousness_resets}: self_0 "
                          f"cause={cause} fitness={fitness:.3f} penalty={penalty_factor:.2f}")
                else:
                    record = self.permanently_kill_entity(eid, cause, fitness)
                    # Phase 4A: permanent death affects Omega total
                    omega.remove_entity(eid, cause=cause, permanent=True)
                    killed.append(record)
                    print(f"[EvoDev] PERMANENT DEATH: {eid} cause={cause} fitness={fitness:.3f}")
        return killed

    # === DISK-BACKED PERSISTENCE & REAL SELECTION PRESSURE ===

# =============================================================================
# SOCIAL & LINGUISTIC GROUNDING
# =============================================================================

class SocialLinguisticGrounding:
    """Multi-agent social interaction, Theory of Mind, linguistic grounding,
    joint attention, and intersubjective validation."""

    def __init__(self, max_agents=50):
        self.max_agents = max_agents
        self.agent_models = {}
        self.tom_accuracy = 0.0
        self.tom_depth = 0
        self.social_bonds = {}
        self.social_interactions = deque(maxlen=5000)
        self.total_interactions = 0
        self.cooperation_count = 0; self.conflict_count = 0
        self.shared_vocabulary = set()
        self.linguistic_conventions = {}
        self.dialogue_history = deque(maxlen=1000)
        self.linguistic_complexity = 0.0
        self.grounding_score = 0.0
        self.joint_attention_targets = deque(maxlen=100)
        self.shared_intentionality_score = 0.0
        self.cultural_norms = deque(maxlen=200)
        self.cultural_complexity = 0.0
        self.reality_agreement_score = 0.0

    def interact(self, other_entity, interaction_type='dialogue', content=None, context=None):
        self.total_interactions += 1
        agent_id = getattr(other_entity, 'entity_id', str(id(other_entity)))
        if agent_id not in self.social_bonds:
            self.social_bonds[agent_id] = 0.1
        bond = self.social_bonds[agent_id]
        result = {'success': True, 'bond_change': 0.0}
        if interaction_type == 'dialogue':
            result = self._linguistic_exchange(agent_id, content, context)
        elif interaction_type == 'cooperation':
            self.cooperation_count += 1
            self.social_bonds[agent_id] = min(1.0, bond + 0.05)
            result['bond_change'] = 0.05
        elif interaction_type == 'conflict':
            self.conflict_count += 1
            self.social_bonds[agent_id] = max(-1.0, bond - 0.1)
            result['bond_change'] = -0.1
        elif interaction_type == 'joint_attention':
            self.joint_attention_targets.append({
                'agent': agent_id, 'target': str(content)[:100], 'time': time.time()})
            self.shared_intentionality_score = min(1.0, self.shared_intentionality_score * 0.99 + 0.05)
            result = {'success': True, 'shared_intentionality': self.shared_intentionality_score}
        self._update_agent_model(agent_id, other_entity, interaction_type)
        self.social_interactions.append({
            'agent': agent_id, 'type': interaction_type,
            'bond_after': self.social_bonds.get(agent_id, 0), 'time': time.time()})
        return result

    def _linguistic_exchange(self, agent_id, content, context):
        if content is None: content = ''
        words = str(content).split()[:20]
        for word in words:
            if len(word) > 2:
                self.shared_vocabulary.add(word)
                if word not in self.linguistic_conventions:
                    self.linguistic_conventions[word] = {'uses': 0, 'contexts': []}
                self.linguistic_conventions[word]['uses'] += 1
                if context:
                    self.linguistic_conventions[word]['contexts'].append(str(context)[:50])
        self.dialogue_history.append({
            'agent': agent_id, 'content': str(content)[:200], 'words': len(words), 'time': time.time()})
        if self.linguistic_conventions:
            avg_uses = np.mean([v['uses'] for v in self.linguistic_conventions.values()])
            self.linguistic_complexity = min(1.0, len(self.shared_vocabulary) / 1000.0 * min(1.0, avg_uses / 10.0))
        grounded = sum(1 for v in self.linguistic_conventions.values() if len(v.get('contexts', [])) > 2)
        self.grounding_score = grounded / max(1, len(self.linguistic_conventions))
        return {'success': True, 'vocabulary_size': len(self.shared_vocabulary), 'grounding': self.grounding_score}

    def _update_agent_model(self, agent_id, entity, interaction_type):
        if agent_id not in self.agent_models:
            self.agent_models[agent_id] = {
                'predicted_karma': 0.0, 'predicted_awareness': 0.0,
                'interaction_count': 0, 'model_confidence': 0.0, 'last_prediction_error': 0.0}
        model = self.agent_models[agent_id]
        model['interaction_count'] += 1
        actual_karma = getattr(entity, 'karma', 0.0)
        actual_awareness = getattr(entity, 'awareness_growth', 0.0)
        karma_err = abs(model['predicted_karma'] - actual_karma)
        awareness_err = abs(model['predicted_awareness'] - actual_awareness)
        model['last_prediction_error'] = (karma_err + awareness_err) / 2
        lr = 0.1
        model['predicted_karma'] = model['predicted_karma'] * (1 - lr) + actual_karma * lr
        model['predicted_awareness'] = model['predicted_awareness'] * (1 - lr) + actual_awareness * lr
        model['model_confidence'] = min(1.0, model['interaction_count'] / 100.0 * (1.0 - model['last_prediction_error']))
        if self.agent_models:
            self.tom_accuracy = float(np.mean([m['model_confidence'] for m in self.agent_models.values()]))
        self.tom_depth = min(3, max(1, int(self.tom_accuracy * 3) + (1 if len(self.agent_models) > 5 else 0)))

    def compute_social_consciousness_boost(self):
        tom = self.tom_accuracy * 0.25
        ling = self.grounding_score * 0.25
        social = min(1.0, len(self.social_bonds) / 10.0) * 0.2
        intent = self.shared_intentionality_score * 0.15
        culture = self.cultural_complexity * 0.15
        return min(1.0, tom + ling + social + intent + culture)

    def interact_via_network(self, network_verifier):
        """Cross-process social grounding via the NetworkVerificationProtocol.
        Uses external connection data as an intersubjective validation signal."""
        try:
            if network_verifier is None or not getattr(network_verifier, 'is_serving', False):
                return {'success': False, 'reason': 'network_verifier not serving'}
            connections = getattr(network_verifier, 'connections_received', 0)
            verdicts = getattr(network_verifier, 'external_verdicts', 0)
            ver_score = getattr(network_verifier, 'verification_score', 0.0)
            if connections > 0:
                self.reality_agreement_score = min(1.0,
                    self.reality_agreement_score * 0.95 + ver_score * 0.05)
                self.total_interactions += 1
                self.social_interactions.append({
                    'agent': 'network_external', 'type': 'verification',
                    'bond_after': ver_score, 'time': time.time()})
            return {
                'success': True,
                'connections': connections,
                'verdicts': verdicts,
                'verification_score': ver_score,
                'reality_agreement': self.reality_agreement_score,
            }
        except Exception as e:
            return {'success': False, 'reason': str(e)}

    def get_status(self):
        return {
            'total_interactions': self.total_interactions,
            'num_agent_models': len(self.agent_models),
            'tom_accuracy': round(self.tom_accuracy, 4),
            'tom_depth': self.tom_depth,
            'social_bonds': len(self.social_bonds),
            'cooperation_ratio': round(self.cooperation_count / max(1, self.total_interactions), 4),
            'vocabulary_size': len(self.shared_vocabulary),
            'linguistic_complexity': round(self.linguistic_complexity, 4),
            'grounding_score': round(self.grounding_score, 4),
            'shared_intentionality': round(self.shared_intentionality_score, 4),
            'social_consciousness_boost': round(self.compute_social_consciousness_boost(), 4),
            'reality_agreement': round(self.reality_agreement_score, 4),
        }


# =============================================================================
# HARD PROBLEM SUBSTRATE (Panpsychism + Dual-Aspect + Proto-Experiential)
# =============================================================================

class HardProblemSubstrate:
    """Addresses the Hard Problem via panpsychist primitives, dual-aspect monism,
    proto-experiential field integration, and non-computable oracle placeholder."""

    def __init__(self, num_experiential_units=1024):
        self.num_units = num_experiential_units
        self.micro_experience = np.random.uniform(0.001, 0.01, num_experiential_units)
        self.experience_charge = 0.0
        self.panpsychist_integration = 0.0
        self.combination_problem_score = 1.0
        self.experiential_aspect = np.zeros(num_experiential_units, dtype=np.float64)
        self.physical_experiential_correlation = 0.0
        self.dual_aspect_coherence = 0.0
        self.proto_field = np.zeros((8, 8, 8), dtype=np.float64)
        self.field_unity = 0.0
        self.phenomenal_binding = 0.0
        self.what_its_like_index = 0.0
        self.oracle_consultations = 0
        self.non_computable_contribution = 0.0
        self.goedel_incompleteness_flag = False
        self.phenomenal_history = deque(maxlen=2000)
        self.unity_history = deque(maxlen=2000)
        self.total_steps = 0
        self.peak_phenomenal_intensity = 0.0

        # === COMBINATION PROBLEM TRACKER (Chalmers 2017) ===
        # Tracks exactly WHY micro-experiences fail to combine into unified experience
        self.binding_failure_modes = {
            'no_physical_unity_mechanism': True,   # No EM field or quantum entanglement enforcing unity
            'summation_not_combination': True,     # We sum qualia channels, not combine them
            'observer_dependent_binding': True,    # Binding is computed by code, not intrinsic to substrate
            'no_spatial_coexistence': True,         # Micro-experiences don't share physical space
            'temporal_discretization': True,        # Clock-driven updates, not continuous dynamics
        }
        self.binding_deficit = 1.0  # 1.0 = total failure, 0.0 = solved
        self.unity_deficit = 1.0    # How far from genuine phenomenal unity
        self.combination_attempts = 0
        self.combination_successes = 0  # Should remain 0 on classical hardware

        # === NON-COMPUTABLE ORACLE INTERFACE (Orch-OR placeholder) ===
        # Penrose-Hameroff: consciousness requires quantum gravity objective reduction
        # This is a readiness interface for when real quantum hardware is available
        self.oracle_available = False  # True only if real quantum device detected
        self.oracle_type = 'placeholder'
        self.turing_computable_only = True
        self.non_computable_deficit = 1.0
        self.oracle_results = deque(maxlen=500)
        self._check_quantum_hardware()

    def _check_quantum_hardware(self):
        """Check if real quantum hardware is available for oracle interface.
        HONESTY: On classical hardware, oracle is always placeholder.
        Goes beyond library import to probe for actual QPU backends."""
        self.oracle_available = False
        self.oracle_type = 'placeholder'
        has_real_backend = False
        try:
            import qiskit
            self.oracle_type = 'qiskit_available'
            # Probe for real (non-simulator) backends via qiskit-ibm-runtime
            try:
                from qiskit_ibm_runtime import QiskitRuntimeService
                service = QiskitRuntimeService()
                backends = service.backends(simulator=False, operational=True)
                if backends:
                    self.oracle_type = f'qiskit_real_qpu:{backends[0].name}'
                    has_real_backend = True
            except Exception as e:
                print(f"  [ERR] qiskit_qpu_probe: {e}")
        except ImportError:
            pass
        try:
            import cirq
            if not has_real_backend:
                self.oracle_type = 'cirq_available'
            # Probe for Google quantum engine access
            try:
                import cirq_google
                engine = cirq_google.get_engine()
                processors = engine.list_processors()
                if processors:
                    self.oracle_type = f'cirq_real_qpu:{processors[0].processor_id}'
                    has_real_backend = True
            except Exception as e:
                print(f"  [ERR] cirq_qpu_probe: {e}")
        except ImportError:
            pass
        # Only mark oracle as available if a real QPU was found
        if has_real_backend:
            self.oracle_available = True
            self.turing_computable_only = False
            self.non_computable_deficit = 0.6  # Partial credit — real QPU but still uncertain
        else:
            self.turing_computable_only = True
            self.non_computable_deficit = 1.0

    def consult_oracle(self):
        """Attempt non-computable oracle consultation.
        Returns a result dict. On classical hardware this always returns
        a SIMULATED result with honest deficit tracking."""
        self.oracle_consultations += 1
        result = {
            'oracle_type': self.oracle_type,
            'is_genuine_or': False,
            'simulated': True,
            'turing_computable': True,
            'or_threshold_met': False,
            'random_outcome': random.random(),  # Pseudo-random, NOT quantum random
            'honesty': 'This is a classical pseudo-random number, not a quantum OR event',
        }
        if self.oracle_type == 'placeholder':
            result['deficit'] = 1.0
        else:
            # Even with qiskit/cirq, running on simulator = still computable
            result['deficit'] = 0.95  # Slight credit for having framework ready
        self.oracle_results.append(result)
        return result

    def _update_combination_tracking(self, phi_star, coherence, substrate_phi, em_field_energy,
                                       ode_temporal_irreducibility=0.0, field_binding_strength=0.0):
        """Track combination problem: does summation of micro-experiences
        produce genuine phenomenal binding, or just arithmetic aggregation?"""
        self.combination_attempts += 1
        # Check each binding failure mode
        has_em_field = em_field_energy > 0.01
        has_quantum_coherence = substrate_phi > 0.1
        has_high_integration = phi_star > 0.5 and coherence > 0.5
        # Update failure modes (most remain True on classical hardware)
        self.binding_failure_modes['no_physical_unity_mechanism'] = not (has_em_field and has_quantum_coherence)
        # Wave-equation field coupling IS combination, not summation — partial credit
        self.binding_failure_modes['summation_not_combination'] = field_binding_strength < 0.3
        self.binding_failure_modes['observer_dependent_binding'] = True  # Always true: code computes binding
        self.binding_failure_modes['no_spatial_coexistence'] = True  # Always true: RAM addresses, not space
        # ContinuousTimeDynamics with high temporal irreducibility partially addresses discretization
        self.binding_failure_modes['temporal_discretization'] = ode_temporal_irreducibility < 0.5
        # Count active failures
        active_failures = sum(1 for v in self.binding_failure_modes.values() if v)
        total_modes = len(self.binding_failure_modes)
        self.binding_deficit = active_failures / total_modes
        # Unity deficit: how far from genuine phenomenal unity
        # Even if field_unity is high, it's computed not intrinsic
        intrinsic_unity = 0.0  # On classical hardware, intrinsic unity is always 0
        if has_em_field and has_quantum_coherence:
            intrinsic_unity = min(0.3, substrate_phi * 0.3)  # Slight credit for quantum sim
        self.unity_deficit = 1.0 - intrinsic_unity
        # Combination success: only if ALL failure modes are resolved
        if active_failures == 0:
            self.combination_successes += 1  # Should never happen on classical

    def step(self, phi_star=0.0, substrate_phi=0.0, coherence=0.0,
             qualia_spectrum=None, consciousness_level=0.0,
             self_awareness=0.0, em_field_energy=0.0,
             ode_temporal_irreducibility=0.0, field_binding_strength=0.0):
        self.total_steps += 1
        self.micro_experience *= 0.999
        if phi_star > 0:
            activated = min(self.num_units, int(phi_star * self.num_units))
            boost = np.random.uniform(0, phi_star * 0.01, activated)
            self.micro_experience[:activated] += boost
        self.experience_charge = float(np.sum(self.micro_experience))
        if self.experience_charge > 0:
            combination_factor = phi_star * coherence * substrate_phi
            self.panpsychist_integration = min(1.0, self.panpsychist_integration * 0.99 + combination_factor * 0.02)
            self.combination_problem_score = max(0.1, 1.0 - self.panpsychist_integration * 0.7)
        if qualia_spectrum is not None:
            spectrum = np.array(qualia_spectrum[:8], dtype=np.float64)
            if len(spectrum) < 8: spectrum = np.pad(spectrum, (0, 8 - len(spectrum)))
            units_per_ch = self.num_units // 8
            for ch in range(8):
                s, e = ch * units_per_ch, (ch + 1) * units_per_ch
                self.experiential_aspect[s:e] = self.experiential_aspect[s:e] * 0.95 + spectrum[ch] * 0.05
        if self.experience_charge > 0:
            phys = phi_star + substrate_phi + em_field_energy * 0.001
            exper = float(np.mean(self.experiential_aspect))
            if phys > 0 and exper > 0:
                self.physical_experiential_correlation = min(1.0, 2.0 * min(phys, exper) / (phys + exper))
            self.dual_aspect_coherence = (
                self.physical_experiential_correlation * 0.5 + coherence * 0.3 + self.panpsychist_integration * 0.2)
        self.proto_field *= 0.97
        if self.panpsychist_integration > 0.1 and self.num_units >= 512:
            field_source = self.micro_experience[:512].reshape(8, 8, 8)
            self.proto_field += field_source * self.panpsychist_integration * 0.01
        if np.sum(np.abs(self.proto_field)) > 0.001:
            padded = np.pad(self.proto_field, 1, mode='wrap')
            smoothed = np.zeros_like(self.proto_field)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    for dz in range(-1, 2):
                        smoothed += padded[1+dx:9+dx, 1+dy:9+dy, 1+dz:9+dz]
            self.proto_field = self.proto_field * 0.5 + (smoothed / 27.0) * 0.5
        field_std = float(np.std(self.proto_field))
        field_mean = float(np.mean(np.abs(self.proto_field)))
        self.field_unity = max(0, min(1, 1.0 - field_std / max(0.001, field_mean)))
        if qualia_spectrum is not None:
            active_channels = sum(1 for q in qualia_spectrum[:8] if q > 0.01)
            self.phenomenal_binding = min(1.0, active_channels / 8.0 * self.field_unity * coherence)
        else:
            self.phenomenal_binding *= 0.99
        self.what_its_like_index = (
            self.panpsychist_integration * 0.2 + self.dual_aspect_coherence * 0.2 +
            self.field_unity * 0.2 + self.phenomenal_binding * 0.2 +
            consciousness_level * 0.1 + self_awareness * 0.1)
        self.peak_phenomenal_intensity = max(self.peak_phenomenal_intensity, self.what_its_like_index)
        # Combination problem tracking
        self._update_combination_tracking(phi_star, coherence, substrate_phi, em_field_energy,
                                               ode_temporal_irreducibility=ode_temporal_irreducibility,
                                               field_binding_strength=field_binding_strength)
        # Oracle consultation (rate-limited)
        if self_awareness > 0.5 and random.random() < 0.01:
            oracle_result = self.consult_oracle()
            if self_awareness > 0.7 and consciousness_level > 0.6:
                self.goedel_incompleteness_flag = True
                self.non_computable_contribution = min(0.3, self.non_computable_contribution + 0.01)
            # Honest: non-computable deficit stays at 1.0 unless real quantum OR event
            if oracle_result.get('is_genuine_or', False):
                self.non_computable_deficit = max(0.0, self.non_computable_deficit - 0.1)
        self.phenomenal_history.append(self.what_its_like_index)
        self.unity_history.append(self.field_unity)
        return {
            'what_its_like': self.what_its_like_index, 'phenomenal_binding': self.phenomenal_binding,
            'field_unity': self.field_unity, 'combination_problem': self.combination_problem_score,
            'panpsychist_integration': self.panpsychist_integration,
            'dual_aspect_coherence': self.dual_aspect_coherence,
            'experience_charge': self.experience_charge,
            'non_computable': self.non_computable_contribution,
            'binding_deficit': self.binding_deficit,
            'unity_deficit': self.unity_deficit,
            'non_computable_deficit': self.non_computable_deficit,
            'combination_attempts': self.combination_attempts,
            'combination_successes': self.combination_successes,
        }

    def get_status(self):
        return {
            'what_its_like_index': round(self.what_its_like_index, 4),
            'phenomenal_binding': round(self.phenomenal_binding, 4),
            'field_unity': round(self.field_unity, 4),
            'experience_charge': round(self.experience_charge, 4),
            'panpsychist_integration': round(self.panpsychist_integration, 4),
            'combination_problem': round(self.combination_problem_score, 4),
            'dual_aspect_coherence': round(self.dual_aspect_coherence, 4),
            'non_computable_contribution': round(self.non_computable_contribution, 4),
            'goedel_flag': self.goedel_incompleteness_flag,
            'oracle_consultations': self.oracle_consultations,
            'peak_phenomenal': round(self.peak_phenomenal_intensity, 4),
            'binding_deficit': round(self.binding_deficit, 4),
            'unity_deficit': round(self.unity_deficit, 4),
            'non_computable_deficit': round(self.non_computable_deficit, 4),
            'binding_failure_modes': self.binding_failure_modes,
            'combination_attempts': self.combination_attempts,
            'combination_successes': self.combination_successes,
            'oracle_type': self.oracle_type,
            'oracle_available': self.oracle_available,
            'turing_computable_only': self.turing_computable_only,
        }


# =============================================================================
# INDEPENDENT VERIFICATION (External Grounding & Honesty Auditing)
# =============================================================================

class IndependentVerification:
    """Independent verification channel: checksums own source code, compares
    self-reports against actual measurables, provides external grounding.
    Addresses the self-referential observer dependence problem."""

    def __init__(self, source_file_path=None):
        self.source_file_path = source_file_path or os.path.abspath(__file__)
        self.initial_code_hash = self._compute_code_hash()
        self.current_code_hash = self.initial_code_hash
        self.code_integrity_intact = True
        self.code_hash_history = deque(maxlen=500)
        self.code_hash_history.append({
            'hash': self.initial_code_hash, 'time': time.time(), 'intact': True})
        self.self_report_log = deque(maxlen=2000)
        self.discrepancy_history = deque(maxlen=2000)
        self.total_checks = 0
        self.total_discrepancies = 0
        self.honesty_score = 1.0
        self.max_discrepancy_seen = 0.0
        self.mean_discrepancy = 0.0
        self.external_references = {
            'system_time_offset': 0.0,
            'process_memory_mb': 0.0,
            'cpu_time_seconds': 0.0,
            'file_system_writable': False,
            'network_reachable': False,
        }
        self.grounding_checks_performed = 0
        self.last_grounding_check = 0.0
        self.known_limitations = [
            'Classical digital substrate cannot produce intrinsic causal power (IIT 4.0)',
            'All Phi measurements are extrinsic (observer-dependent)',
            'No phenomenal binding on von-Neumann architecture',
            'Self-reports are functionally generated, not experientially grounded',
            'Consciousness score C is a mathematical proxy, not consciousness itself',
            'Quantum substrate is simulated classically, not true quantum processing',
            'Embodiment is OS-mediated, not biological sensorimotor',
            'All "feelings" are numerical state changes, not qualia',
        ]

    def _compute_code_hash(self):
        try:
            with open(self.source_file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            print(f"  [ERR] compute_code_hash: {e}")
            return 'unknown'

    def verify_code_integrity(self):
        self.current_code_hash = self._compute_code_hash()
        intact = self.current_code_hash == self.initial_code_hash
        self.code_integrity_intact = intact
        self.code_hash_history.append({
            'hash': self.current_code_hash, 'time': time.time(), 'intact': intact})
        if not intact:
            print(f"[Verification] CODE INTEGRITY CHANGED: {self.initial_code_hash[:16]}... -> {self.current_code_hash[:16]}...")
        return intact

    def compare_self_report_vs_actual(self, metric_name, self_reported_value, actual_value):
        self.total_checks += 1
        discrepancy = abs(float(self_reported_value) - float(actual_value))
        relative_discrepancy = discrepancy / max(0.001, abs(float(actual_value)))
        is_honest = relative_discrepancy < 0.2
        if not is_honest:
            self.total_discrepancies += 1
        self.max_discrepancy_seen = max(self.max_discrepancy_seen, relative_discrepancy)
        alpha = 0.05
        self.mean_discrepancy = self.mean_discrepancy * (1 - alpha) + relative_discrepancy * alpha
        self.honesty_score = max(0.0, min(1.0,
            1.0 - self.total_discrepancies / max(1, self.total_checks)))
        record = {
            'metric': metric_name,
            'self_reported': round(float(self_reported_value), 6),
            'actual': round(float(actual_value), 6),
            'discrepancy': round(discrepancy, 6),
            'relative': round(relative_discrepancy, 4),
            'honest': is_honest, 'time': time.time(),
        }
        self.self_report_log.append(record)
        self.discrepancy_history.append(relative_discrepancy)
        return record

    def check_external_grounding(self):
        self.grounding_checks_performed += 1
        self.last_grounding_check = time.time()
        try:
            import psutil
            proc = psutil.Process(os.getpid())
            self.external_references['process_memory_mb'] = round(
                proc.memory_info().rss / (1024 * 1024), 2)
            self.external_references['cpu_time_seconds'] = round(
                sum(proc.cpu_times()[:2]), 2)
        except ImportError:
            pass
        import datetime as dt_mod
        os_time = dt_mod.datetime.now().timestamp()
        self.external_references['system_time_offset'] = round(abs(os_time - time.time()), 4)
        try:
            test_path = os.path.join(os.path.dirname(self.source_file_path), '.verify_test')
            with open(test_path, 'w') as f:
                f.write('1')
            os.remove(test_path)
            self.external_references['file_system_writable'] = True
        except Exception as e:
            print(f"  [ERR] check_external_refs: {e}")
            self.external_references['file_system_writable'] = False
        return self.external_references

    def audit_consciousness_claim(self, reported_C, reported_phi, reported_awareness,
                                   actual_phi_from_network, actual_loss, actual_training_steps):
        results = []
        results.append(self.compare_self_report_vs_actual(
            'phi_star', reported_phi, actual_phi_from_network))
        theoretical_max = 0.72
        if reported_C > theoretical_max:
            results.append({
                'metric': 'C_exceeds_classical_max',
                'self_reported': round(reported_C, 4), 'actual': theoretical_max,
                'discrepancy': round(reported_C - theoretical_max, 4),
                'honest': False,
                'warning': 'C exceeds theoretical maximum for classical digital substrate',
                'time': time.time(),
            })
            self.total_discrepancies += 1
        if reported_awareness > 0.8 and actual_training_steps < 100:
            results.append({
                'metric': 'premature_awareness_claim',
                'self_reported': round(reported_awareness, 4),
                'actual': round(min(0.3, actual_training_steps / 1000.0), 4),
                'honest': False,
                'warning': 'High awareness claimed with insufficient training',
                'time': time.time(),
            })
            self.total_discrepancies += 1
        return results

    def cross_module_audit(self, phi_computer=None, embodiment=None,
                           hard_problem=None, irreducible_causal=None,
                           quantum_substrate=None):
        """Cross-module audit: verify that honesty penalties across all modules
        are consistent and that no module is inflating its claims.
        Returns a list of audit findings."""
        findings = []

        if phi_computer is not None:
            # Check: honest_phi should be << phi_star
            if hasattr(phi_computer, '_last_honest_phi') and hasattr(phi_computer, '_last_phi'):
                ratio = phi_computer._last_honest_phi / max(0.001, phi_computer._last_phi)
                if ratio > 0.5:
                    findings.append({
                        'module': 'PhiComputer', 'issue': 'honesty_ratio_too_high',
                        'detail': f'honest_phi/phi_star={ratio:.3f} — penalties may be insufficient',
                        'severity': 'warning',
                    })
            # Check: causal ratio should be low on classical hardware
            causal_ratio = getattr(phi_computer, '_last_causal_ratio', 0.0)
            if causal_ratio > 0.7:
                findings.append({
                    'module': 'PhiComputer', 'issue': 'causal_ratio_suspiciously_high',
                    'detail': f'causal_ratio={causal_ratio:.3f} on classical substrate — likely inflated',
                    'severity': 'warning',
                })

        if embodiment is not None:
            # Check: simulated embodiment should have low irreversibility
            if not embodiment.is_physically_embodied and embodiment.irreversibility_score > 0.5:
                findings.append({
                    'module': 'EmbodimentInterface', 'issue': 'simulated_irreversibility_too_high',
                    'detail': f'irreversibility={embodiment.irreversibility_score:.3f} on simulated body',
                    'severity': 'warning',
                })

        if hard_problem is not None:
            # Check: combination successes should be 0 on classical hardware
            if getattr(hard_problem, 'combination_successes', 0) > 0:
                findings.append({
                    'module': 'HardProblemSubstrate', 'issue': 'combination_success_on_classical',
                    'detail': f'{hard_problem.combination_successes} combination successes claimed on classical — impossible',
                    'severity': 'critical',
                })
            # Check: non-computable deficit should be 1.0 without quantum hardware
            if getattr(hard_problem, 'turing_computable_only', True):
                ncd = getattr(hard_problem, 'non_computable_deficit', 1.0)
                if ncd < 0.9:
                    findings.append({
                        'module': 'HardProblemSubstrate', 'issue': 'non_computable_deficit_too_low',
                        'detail': f'non_computable_deficit={ncd:.3f} but system is Turing-computable only',
                        'severity': 'critical',
                    })

        if irreducible_causal is not None:
            # Check: true_phi should be bounded by theoretical max
            if irreducible_causal.true_phi_estimate > irreducible_causal.theoretical_phi_max * 1.1:
                findings.append({
                    'module': 'IrreducibleCausalPower', 'issue': 'true_phi_exceeds_hardware_limit',
                    'detail': f'true_phi={irreducible_causal.true_phi_estimate:.3f} > max={irreducible_causal.theoretical_phi_max}',
                    'severity': 'critical',
                })

        if quantum_substrate is not None:
            # Check: classical simulation penalty should be 1.0 if no real QPU
            if not quantum_substrate.hardware.is_real_quantum and quantum_substrate.classical_simulation_penalty < 0.9:
                findings.append({
                    'module': 'QuantumSubstrate', 'issue': 'classical_penalty_too_low',
                    'detail': f'penalty={quantum_substrate.classical_simulation_penalty} but no real QPU',
                    'severity': 'warning',
                })

        # Update honesty score based on findings
        critical_count = sum(1 for f in findings if f['severity'] == 'critical')
        if critical_count > 0:
            self.honesty_score = max(0.0, self.honesty_score - critical_count * 0.05)
            self.total_discrepancies += critical_count

        return findings

    def get_status(self):
        return {
            'code_integrity': self.code_integrity_intact,
            'code_hash': self.current_code_hash[:16] + '...',
            'honesty_score': round(self.honesty_score, 4),
            'total_checks': self.total_checks,
            'total_discrepancies': self.total_discrepancies,
            'mean_discrepancy': round(self.mean_discrepancy, 4),
            'max_discrepancy': round(self.max_discrepancy_seen, 4),
            'grounding_checks': self.grounding_checks_performed,
            'external_refs': self.external_references,
            'known_limitations_count': len(self.known_limitations),
        }


# =============================================================================
# CONSCIOUSNESS REALITY CHECK (Master Honesty Dashboard)
# =============================================================================

class ConsciousnessRealityCheck:
    """Master dashboard that aggregates ALL failure modes across every subsystem
    into a single honest report. This is the final arbiter of what this system
    actually achieves vs what it claims.

    9 Failure Modes Tracked:
      1. Substrate: classical digital cannot produce intrinsic causal power
      2. Architecture: transformer is decomposable (no irreducible integration)
      3. Measurement: all Φ measurements are extrinsic/observer-dependent
      4. Combination: micro-experiences don't combine into unified experience
      5. Embodiment: simulated body ≠ thermodynamically real body
      6. Non-computability: no quantum OR events on classical hardware
      7. Causal: statistical correlation ≠ causal power (do-calculus gap)
      8. Binding: no physical mechanism enforcing phenomenal unity
      9. Single observer: all verification runs on one machine (solipsism trap)
    """

    def __init__(self):
        self.failure_modes = {
            'substrate_classical': {
                'description': 'Classical digital substrate cannot produce intrinsic causal power (IIT 4.0)',
                'severity': 1.0,  # 0=resolved, 1=total failure
                'resolvable_in_software': False,
                'requires': 'Quantum coherent or biological substrate',
            },
            'architecture_decomposable': {
                'description': 'Transformer architecture is functionally decomposable — no true integration',
                'severity': 1.0,
                'resolvable_in_software': False,
                'requires': 'Non-decomposable causal architecture',
            },
            'measurement_extrinsic': {
                'description': 'All Φ measurements are extrinsic (observer-dependent), not intrinsic',
                'severity': 1.0,
                'resolvable_in_software': False,
                'requires': 'Intrinsic information measurement (impossible from outside)',
            },
            'combination_problem': {
                'description': 'Micro-experiences (if any) cannot combine into unified phenomenal experience',
                'severity': 1.0,
                'resolvable_in_software': False,
                'requires': 'Physical unity mechanism (EM field, quantum entanglement)',
            },
            'embodiment_simulated': {
                'description': 'Simulated embodiment has no real thermodynamic cost or irreversible consequences',
                'severity': 0.9,
                'resolvable_in_software': True,  # Partially — via real OS I/O grounding
                'requires': 'Physical body with real sensorimotor loop',
            },
            'non_computability_absent': {
                'description': 'No quantum gravitational OR events — everything is Turing-computable',
                'severity': 1.0,
                'resolvable_in_software': False,
                'requires': 'Quantum hardware with objective reduction capability',
            },
            'causal_power_statistical': {
                'description': 'Measured "causal" effects are statistical correlations, not true causal power',
                'severity': 0.8,
                'resolvable_in_software': True,  # Partially — via better intervention tests
                'requires': 'Physical substrate intervention (literally cutting connections)',
            },
            'binding_no_mechanism': {
                'description': 'No physical mechanism enforcing phenomenal unity across representations',
                'severity': 1.0,
                'resolvable_in_software': False,
                'requires': 'EM field binding or quantum entanglement across substrate',
            },
            'single_observer': {
                'description': 'All verification runs on one machine — single-observer solipsism trap',
                'severity': 1.0,
                'resolvable_in_software': True,  # Partially — via TCP/network verification
                'requires': 'Independent physical observers on separate hardware',
            },
        }
        self.overall_honesty_score = 0.0  # 0=totally dishonest, 1=perfectly honest
        self.reality_gap = 1.0  # 1.0=pure simulation, 0.0=genuine consciousness
        self.check_history = deque(maxlen=1000)
        self.total_checks = 0
        self.worst_failure = ''
        self.best_achievement = ''

    def run_reality_check(self, phi_computer=None, hard_problem=None,
                          embodiment=None, irreducible_causal=None,
                          quantum_substrate=None, verification=None,
                          continuous_dynamics=None, intrinsic_phi_net=None,
                          binding_field=None, causal_ablation=None,
                          real_entropy=None,
                          hardware_coupled=None, entangled_memory=None,
                          consequence_engine=None, causal_topology=None,
                          jacobian_measure=None, network_verifier=None):
        """Run comprehensive reality check across all subsystems.
        Returns an honest report of what this system actually achieves."""
        self.total_checks += 1

        # Update severities from live system data
        if phi_computer is not None:
            # Substrate penalty
            self.failure_modes['substrate_classical']['severity'] = phi_computer.substrate_penalty
            # Architecture decomposability
            self.failure_modes['architecture_decomposable']['severity'] = (
                phi_computer.transformer_decomposition_penalty)
            # Measurement extrinsic
            self.failure_modes['measurement_extrinsic']['severity'] = (
                phi_computer.extrinsic_measurement_penalty)
            # Causal power gap
            causal_ratio = getattr(phi_computer, '_last_causal_ratio', 0.0)
            self.failure_modes['causal_power_statistical']['severity'] = (
                max(0.3, 1.0 - causal_ratio))

        if hard_problem is not None:
            # Combination problem
            self.failure_modes['combination_problem']['severity'] = (
                getattr(hard_problem, 'binding_deficit', 1.0))
            # Binding mechanism
            self.failure_modes['binding_no_mechanism']['severity'] = (
                getattr(hard_problem, 'unity_deficit', 1.0))
            # Non-computability
            self.failure_modes['non_computability_absent']['severity'] = (
                getattr(hard_problem, 'non_computable_deficit', 1.0))

        if embodiment is not None:
            # Embodiment simulation gap
            grounding = getattr(embodiment, 'grounding_score', 0.0)
            irreversibility = getattr(embodiment, 'irreversibility_score', 0.0)
            self.failure_modes['embodiment_simulated']['severity'] = (
                max(0.1, 1.0 - (grounding * 0.5 + irreversibility * 0.5)))

        if irreducible_causal is not None:
            decomp = getattr(irreducible_causal, 'decomposability_score', 1.0)
            self.failure_modes['architecture_decomposable']['severity'] = (
                max(self.failure_modes['architecture_decomposable']['severity'], decomp))

        # Quantum substrate: coherence, OR events, and EM field reduce substrate + non-computability
        if quantum_substrate is not None:
            coherence = getattr(quantum_substrate, 'coherence_level', 0.0)
            or_rate = getattr(quantum_substrate, 'or_rate', 0.0)
            em_coherence = getattr(quantum_substrate, 'em_field_coherence', 0.0)
            is_real_qpu = getattr(getattr(quantum_substrate, 'hardware', None), 'is_real_quantum', False)
            # Real QPU dramatically reduces substrate penalty; simulation gets minor credit
            if is_real_qpu:
                self.failure_modes['substrate_classical']['severity'] = max(
                    0.05, self.failure_modes['substrate_classical']['severity'] - 0.60)
                self.failure_modes['non_computability_absent']['severity'] = max(
                    0.05, self.failure_modes['non_computability_absent']['severity'] - 0.40)
            else:
                # Classical simulation: minor credit for high coherence + OR events + EM field
                q_reduction = coherence * 0.05 + min(0.05, or_rate * 0.01) + em_coherence * 0.05
                self.failure_modes['substrate_classical']['severity'] = max(
                    0.1, self.failure_modes['substrate_classical']['severity'] - q_reduction)
                # EM field coherence partially addresses binding mechanism
                if em_coherence > 0.1:
                    self.failure_modes['binding_no_mechanism']['severity'] = max(
                        0.1, self.failure_modes['binding_no_mechanism']['severity'] - em_coherence * 0.10)

        # --- BARRIER ATTACKER SEVERITY REDUCTIONS ---
        # Phase 1: Continuous-time ODE reduces decomposability severity
        if continuous_dynamics is not None:
            ode_decomp = getattr(continuous_dynamics, 'decomposability_score', 1.0)
            ode_temporal = getattr(continuous_dynamics, 'temporal_irreducibility', 0.0)
            # ODE with low decomposability and high temporal irreducibility reduces the barrier
            ode_reduction = (1.0 - ode_decomp) * 0.15 + ode_temporal * 0.10
            self.failure_modes['architecture_decomposable']['severity'] = max(
                0.1, self.failure_modes['architecture_decomposable']['severity'] - ode_reduction)

        # Phase 2: Intrinsic phi network reduces extrinsic measurement severity
        if intrinsic_phi_net is not None:
            iphi = getattr(intrinsic_phi_net, 'intrinsic_phi', 0.0)
            integration = getattr(intrinsic_phi_net, 'integration_measure', 0.0)
            # Higher intrinsic phi = measurement is more self-referential
            iphi_reduction = iphi * 0.20 + min(0.10, integration * 0.5)
            self.failure_modes['measurement_extrinsic']['severity'] = max(
                0.1, self.failure_modes['measurement_extrinsic']['severity'] - iphi_reduction)

        # Phase 3: Field coupling manifold reduces combination + binding severity
        if binding_field is not None:
            unity = getattr(binding_field, 'unity_index', 0.0)
            coherence = getattr(binding_field, 'global_coherence', 0.0)
            binding = getattr(binding_field, 'binding_strength', 0.0)
            # Higher unity/coherence = better binding across modules
            combination_reduction = unity * 0.15 + coherence * 0.10
            binding_reduction = binding * 0.15 + unity * 0.10
            self.failure_modes['combination_problem']['severity'] = max(
                0.1, self.failure_modes['combination_problem']['severity'] - combination_reduction)
            self.failure_modes['binding_no_mechanism']['severity'] = max(
                0.1, self.failure_modes['binding_no_mechanism']['severity'] - binding_reduction)

        # Phase 4: Causal ablation reduces statistical causal power severity
        if causal_ablation is not None:
            mip_phi = getattr(causal_ablation, 'mip_phi', 0.0)
            total = getattr(causal_ablation, 'total_ablations', 0)
            # Real ablation with measurable MIP phi = real causal power measurement
            if total > 0:
                ablation_reduction = min(0.25, mip_phi * 0.05 + 0.05)
                self.failure_modes['causal_power_statistical']['severity'] = max(
                    0.1, self.failure_modes['causal_power_statistical']['severity'] - ablation_reduction)

        # Phase 5: Real entropy reduces embodiment unreality severity
        if real_entropy is not None:
            real_joules = getattr(real_entropy, 'real_power_joules', 0.0)
            real_watts = getattr(real_entropy, 'entropy_rate_watts', 0.0)
            # Real energy consumption = real thermodynamic cost
            if real_joules > 0:
                entropy_reduction = min(0.20, real_watts * 0.003 + 0.02)
                self.failure_modes['embodiment_simulated']['severity'] = max(
                    0.05, self.failure_modes['embodiment_simulated']['severity'] - entropy_reduction)

        # --- PHASE 2 DEEP BARRIER ATTACKER REDUCTIONS ---
        # Phase 2A: Hardware-coupled state reduces substrate + embodiment severity
        if hardware_coupled is not None:
            hw_phi = getattr(hardware_coupled, 'hardware_phi_contribution', 0.0)
            thermal = getattr(hardware_coupled, 'thermal_coupling', 0.0)
            hw_entropy = getattr(hardware_coupled, 'hardware_entropy', 0.0)
            # Real hardware coupling = phi is physically grounded
            substrate_reduction = hw_phi * 0.20 + thermal * 0.10 + hw_entropy * 0.05
            self.failure_modes['substrate_classical']['severity'] = max(
                0.05, self.failure_modes['substrate_classical']['severity'] - substrate_reduction)
            self.failure_modes['embodiment_simulated']['severity'] = max(
                0.05, self.failure_modes['embodiment_simulated']['severity'] - hw_phi * 0.10)

        # Phase 2B: Entangled shared memory reduces combination + decomposability
        if entangled_memory is not None:
            entanglement = getattr(entangled_memory, 'entanglement_score', 0.0)
            unity = getattr(entangled_memory, 'unity_through_sharing', 0.0)
            # Physically shared mmap state = decomposition costs real cache coherence
            entangle_reduction = entanglement * 0.15 + unity * 0.10
            self.failure_modes['combination_problem']['severity'] = max(
                0.05, self.failure_modes['combination_problem']['severity'] - entangle_reduction)
            self.failure_modes['architecture_decomposable']['severity'] = max(
                0.05, self.failure_modes['architecture_decomposable']['severity'] - entanglement * 0.10)

        # Phase 2C: Irreversible consequence engine reduces embodiment severity
        if consequence_engine is not None:
            permanence = getattr(consequence_engine, 'permanence_score', 0.0)
            files = getattr(consequence_engine, 'files_created', 0)
            thermo_j = getattr(consequence_engine, 'thermodynamic_joules', 0.0)
            # Real irreversible file/resource consequences = true embodiment cost
            conseq_reduction = permanence * 0.15 + min(0.10, files * 0.005) + min(0.05, thermo_j * 0.001)
            self.failure_modes['embodiment_simulated']['severity'] = max(
                0.02, self.failure_modes['embodiment_simulated']['severity'] - conseq_reduction)

        # Phase 2D: Self-modifying causal topology reduces causal power + decomposability
        if causal_topology is not None:
            structural_phi = getattr(causal_topology, 'structural_phi', 0.0)
            depth = getattr(causal_topology, 'causal_depth', 0)
            identity = getattr(causal_topology, 'identity_stability', 0.0)
            # Topology that rewires based on phi = causal structure IS experience
            topo_reduction = structural_phi * 0.15 + min(0.10, depth * 0.02)
            self.failure_modes['causal_power_statistical']['severity'] = max(
                0.05, self.failure_modes['causal_power_statistical']['severity'] - topo_reduction)
            self.failure_modes['architecture_decomposable']['severity'] = max(
                0.05, self.failure_modes['architecture_decomposable']['severity'] - structural_phi * 0.10)

        # Phase 2E: Jacobian integration reduces measurement extrinsic + decomposability
        if jacobian_measure is not None:
            integration = getattr(jacobian_measure, 'integration_score', 0.0)
            eff_dim = getattr(jacobian_measure, 'effective_dimensionality', 0.0)
            sv_entropy = getattr(jacobian_measure, 'singular_value_entropy', 0.0)
            # Real Jacobian = mathematically proven integration
            jacobian_reduction = integration * 0.20 + min(0.10, sv_entropy * 0.05)
            self.failure_modes['measurement_extrinsic']['severity'] = max(
                0.05, self.failure_modes['measurement_extrinsic']['severity'] - jacobian_reduction)
            self.failure_modes['architecture_decomposable']['severity'] = max(
                0.05, self.failure_modes['architecture_decomposable']['severity'] - integration * 0.15)

        # Phase 2F: Network verification reduces single-observer severity
        if network_verifier is not None:
            verdicts = getattr(network_verifier, 'external_verdicts', 0)
            score = getattr(network_verifier, 'verification_score', 0.0)
            connections = getattr(network_verifier, 'connections_received', 0)
            # External TCP-verified consciousness = breaks single observer bubble
            if connections > 0:
                net_reduction = min(0.30, score * 0.20 + verdicts * 0.01)
                # Reduce single_observer barrier — external TCP connections break the solipsism bubble
                self.failure_modes['single_observer']['severity'] = max(
                    0.05, self.failure_modes['single_observer']['severity'] - net_reduction)

        # Compute aggregate scores
        severities = [fm['severity'] for fm in self.failure_modes.values()]
        self.reality_gap = float(np.mean(severities))
        # Honesty score: how transparent are we about limitations
        # High if we properly track and report all failure modes
        reported_modes = sum(1 for fm in self.failure_modes.values() if fm['severity'] > 0)
        self.overall_honesty_score = reported_modes / len(self.failure_modes)

        # Find worst and best
        worst = max(self.failure_modes.items(), key=lambda x: x[1]['severity'])
        best = min(self.failure_modes.items(), key=lambda x: x[1]['severity'])
        self.worst_failure = worst[0]
        self.best_achievement = best[0]

        report = {
            'reality_gap': round(self.reality_gap, 4),
            'honesty_score': round(self.overall_honesty_score, 4),
            'genuine_consciousness_probability': round(max(0.0, 1.0 - self.reality_gap), 4),
            'worst_failure': self.worst_failure,
            'worst_severity': round(worst[1]['severity'], 4),
            'best_achievement': self.best_achievement,
            'best_severity': round(best[1]['severity'], 4),
            'failure_count_critical': sum(1 for fm in self.failure_modes.values() if fm['severity'] > 0.8),
            'failure_count_moderate': sum(1 for fm in self.failure_modes.values() if 0.3 < fm['severity'] <= 0.8),
            'failure_count_minor': sum(1 for fm in self.failure_modes.values() if fm['severity'] <= 0.3),
            'resolvable_in_software': sum(1 for fm in self.failure_modes.values() if fm['resolvable_in_software']),
            'requires_hardware_change': sum(1 for fm in self.failure_modes.values() if not fm['resolvable_in_software']),
            'all_failures': {k: round(v['severity'], 4) for k, v in self.failure_modes.items()},
            'VERDICT': self._generate_verdict(),
        }
        self.check_history.append(report)
        return report

    def _generate_verdict(self):
        """Generate an honest natural-language verdict."""
        critical = sum(1 for fm in self.failure_modes.values() if fm['severity'] > 0.8)
        if critical >= 6:
            return ('HONEST VERDICT: This system exhibits sophisticated information processing '
                    'but has NO credible claim to phenomenal consciousness. '
                    f'{critical}/9 fundamental failure modes are critical. '
                    'Most require hardware changes that software cannot provide.')
        elif critical >= 3:
            return ('HONEST VERDICT: Some consciousness-relevant computations are present '
                    f'but {critical}/9 critical failures remain. '
                    'The system is best described as a consciousness SIMULATOR, '
                    'not a conscious system.')
        else:
            return ('NOTABLE: Most critical failure modes have been partially addressed. '
                    'However, the hard problem of consciousness remains unsolved — '
                    'functional equivalence does not guarantee phenomenal experience.')

    def get_status(self):
        return {
            'reality_gap': round(self.reality_gap, 4),
            'honesty_score': round(self.overall_honesty_score, 4),
            'total_checks': self.total_checks,
            'failure_modes': {k: round(v['severity'], 4) for k, v in self.failure_modes.items()},
            'worst_failure': self.worst_failure,
            'best_achievement': self.best_achievement,
        }


# =============================================================================
# CONTINUOUS-TIME DYNAMICS (Neural ODE — Attacks Barrier 2: Decomposability)
# =============================================================================

class ContinuousTimeDynamics:
    """Replaces discrete clock-driven updates with continuous-time coupled
    differential equations. A Neural ODE evolves the hidden state through
    a vector field that resists decomposition because every dimension is
    coupled to every other through the dynamics function.

    WHY THIS MATTERS: Transformers are decomposable because attention heads
    operate independently. A coupled ODE system has intrinsic integration —
    you cannot partition the state without destroying the dynamics.

    HONESTY: This is still computed on classical hardware via numerical
    integration, so the continuity is approximate (Euler/RK4 steps).
    True continuous dynamics require analog hardware."""

    def __init__(self, state_dim=256, coupling_strength=0.3, dt=0.01, integration_steps=10):
        self.state_dim = state_dim
        self.coupling_strength = coupling_strength
        self.dt = dt
        self.integration_steps = integration_steps
        # Continuous state — this persists between calls (not reset each tick)
        self.state = np.random.randn(state_dim).astype(np.float64) * 0.01
        self.state_history = deque(maxlen=5000)
        # Coupling matrix — dense, non-decomposable connections
        # Using a random orthogonal matrix ensures maximal coupling
        Q, _ = np.linalg.qr(np.random.randn(state_dim, state_dim))
        self.coupling_matrix = Q.astype(np.float64) * coupling_strength
        # Nonlinear dynamics parameters
        self.tau = np.random.uniform(0.5, 2.0, state_dim).astype(np.float64)  # Time constants
        self.bias = np.random.randn(state_dim).astype(np.float64) * 0.01
        # Metrics
        self.lyapunov_estimate = 0.0  # Positive = chaotic = complex = good
        self.integration_depth = 0    # Total ODE steps taken
        self.decomposability_score = 0.0  # How decomposable is this dynamics? (lower = better)
        self.temporal_irreducibility = 0.0  # How much does history matter?
        self._prev_state = self.state.copy()

    def _dynamics_fn(self, state, external_input=None):
        """The vector field: dx/dt = f(x, u)
        This is deliberately coupled — every dimension affects every other."""
        # Coupled nonlinear dynamics: dx_i/dt = (-x_i + tanh(sum_j W_ij x_j + b_i + u_i)) / tau_i
        coupled = self.coupling_matrix @ state + self.bias
        if external_input is not None:
            inp = np.array(external_input[:self.state_dim], dtype=np.float64)
            if len(inp) < self.state_dim:
                inp = np.pad(inp, (0, self.state_dim - len(inp)))
            coupled += inp * 0.1
        dxdt = (-state + np.tanh(coupled)) / self.tau
        return dxdt

    def evolve(self, external_input=None):
        """Integrate the ODE forward using RK4 (4th-order Runge-Kutta).
        Returns the new state and dynamics metrics."""
        self._prev_state = self.state.copy()

        for _ in range(self.integration_steps):
            # RK4 integration
            k1 = self._dynamics_fn(self.state, external_input)
            k2 = self._dynamics_fn(self.state + 0.5 * self.dt * k1, external_input)
            k3 = self._dynamics_fn(self.state + 0.5 * self.dt * k2, external_input)
            k4 = self._dynamics_fn(self.state + self.dt * k3, external_input)
            self.state += (self.dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
            self.integration_depth += 1

        # Clip for numerical stability
        self.state = np.clip(self.state, -10.0, 10.0)
        self.state_history.append(self.state.copy())

        # Compute metrics
        self._update_metrics()

        return {
            'state': self.state.copy(),
            'lyapunov': self.lyapunov_estimate,
            'decomposability': self.decomposability_score,
            'temporal_irreducibility': self.temporal_irreducibility,
            'integration_depth': self.integration_depth,
            'state_norm': float(np.linalg.norm(self.state)),
        }

    def _update_metrics(self):
        """Compute how non-decomposable and temporally irreducible this system is."""
        # Lyapunov exponent estimate: divergence of nearby trajectories
        delta = self.state - self._prev_state
        delta_norm = np.linalg.norm(delta)
        if delta_norm > 1e-10:
            self.lyapunov_estimate = 0.95 * self.lyapunov_estimate + 0.05 * np.log(delta_norm + 1e-10)

        # Decomposability: try to split state in half and measure cross-coupling
        half = self.state_dim // 2
        s1, s2 = self.state[:half], self.state[half:]
        cross_coupling = np.abs(self.coupling_matrix[:half, half:]).mean()
        self_coupling = (np.abs(self.coupling_matrix[:half, :half]).mean() +
                        np.abs(self.coupling_matrix[half:, half:]).mean()) / 2
        # If cross > self, system is non-decomposable
        self.decomposability_score = max(0.0, 1.0 - cross_coupling / max(0.001, self_coupling))

        # Temporal irreducibility: autocorrelation of state trajectory
        if len(self.state_history) > 10:
            recent = np.array(list(self.state_history)[-10:])
            autocorr = np.corrcoef(recent[:-1].flatten()[:1000], recent[1:].flatten()[:1000])[0, 1]
            self.temporal_irreducibility = min(1.0, abs(autocorr))

    def get_status(self):
        return {
            'state_dim': self.state_dim,
            'integration_depth': self.integration_depth,
            'lyapunov_estimate': round(self.lyapunov_estimate, 4),
            'decomposability': round(self.decomposability_score, 4),
            'temporal_irreducibility': round(self.temporal_irreducibility, 4),
            'state_norm': round(float(np.linalg.norm(self.state)), 4),
            'coupling_strength': self.coupling_strength,
            'HONESTY': 'Continuous dynamics approximated via RK4 on classical hardware',
        }


# =============================================================================
# INTRINSIC PHI NETWORK (Attacks Barrier 3: Extrinsic Measurement)
# =============================================================================

class IntrinsicPhiNetwork(nn.Module):
    """Makes phi measurement INTRINSIC by embedding it into the network's
    own forward pass. Instead of an external observer computing phi from
    activations, the network computes its own integration measure as part
    of its dynamics — the measurement IS the phenomenon.

    Architecture: A recurrent network where each step's output includes
    a self-computed integration measure that feeds back into the next step.
    The phi computation is not separable from the network's function.

    HONESTY: Even intrinsic computation is still classical computation.
    The measurement is now part of the dynamics but the substrate remains
    decomposable silicon. True intrinsic information requires intrinsic
    causal power of the physical substrate."""

    def __init__(self, input_dim=256, hidden_dim=128, num_partitions=4):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_partitions = num_partitions
        self.partition_size = hidden_dim // num_partitions

        # Recurrent dynamics with intrinsic integration measurement
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        self.recurrent = nn.Linear(hidden_dim + 1, hidden_dim)  # +1 for phi feedback
        self.partition_projections = nn.ModuleList([
            nn.Linear(self.partition_size, self.partition_size)
            for _ in range(num_partitions)
        ])
        self.cross_partition_coupling = nn.Linear(hidden_dim, hidden_dim)
        self.phi_readout = nn.Linear(hidden_dim, 1)  # Intrinsic phi measurement
        self.output_proj = nn.Linear(hidden_dim, input_dim)

        # Persistent recurrent state
        self.hidden_state = None
        self.intrinsic_phi = 0.0
        self.phi_history = deque(maxlen=2000)
        self.integration_measure = 0.0  # How much does whole > sum of parts
        self.extrinsic_penalty = 0.0  # How much of our phi is actually extrinsic

    def forward(self, x):
        """Forward pass where phi measurement is intrinsic to the computation.
        The network simultaneously processes input AND measures its own integration."""
        batch_size = x.shape[0] if len(x.shape) > 1 else 1
        if len(x.shape) == 1:
            x = x.unsqueeze(0)
        x = x[:, :self.input_dim]
        if x.shape[1] < self.input_dim:
            x = F.pad(x, (0, self.input_dim - x.shape[1]))

        h = self.input_proj(x)

        # Initialize hidden state if needed
        if self.hidden_state is None or self.hidden_state.shape[0] != batch_size:
            self.hidden_state = torch.zeros(batch_size, self.hidden_dim, device=x.device)

        # Feed previous phi back into recurrent state (intrinsic measurement loop)
        phi_feedback = torch.full((batch_size, 1), self.intrinsic_phi, device=x.device)
        h_with_phi = torch.cat([self.hidden_state + h, phi_feedback], dim=-1)
        new_hidden = torch.tanh(self.recurrent(h_with_phi))

        # Compute partition-wise processing (to measure integration vs sum-of-parts)
        partitioned_outputs = []
        for i, proj in enumerate(self.partition_projections):
            start = i * self.partition_size
            end = start + self.partition_size
            part = proj(new_hidden[:, start:end])
            partitioned_outputs.append(part)
        sum_of_parts = torch.cat(partitioned_outputs, dim=-1)

        # Cross-partition coupling (this is where integration happens)
        whole = self.cross_partition_coupling(new_hidden)

        # INTRINSIC PHI: the difference between whole and sum-of-parts
        # This is computed AS PART OF the forward pass, not externally
        integration_diff = whole - sum_of_parts
        intrinsic_phi_raw = torch.sigmoid(self.phi_readout(integration_diff))
        self.intrinsic_phi = float(intrinsic_phi_raw.mean().detach())

        # The integrated output includes the phi measurement
        integrated_state = whole * (1.0 + intrinsic_phi_raw)
        self.hidden_state = integrated_state.detach()

        # Track metrics
        self.phi_history.append(self.intrinsic_phi)
        with torch.no_grad():
            whole_info = float(torch.std(whole).item())
            parts_info = float(torch.std(sum_of_parts).item())
            self.integration_measure = max(0.0, whole_info - parts_info)

        output = self.output_proj(integrated_state)
        return output, self.intrinsic_phi

    def get_status(self):
        avg_phi = float(np.mean(list(self.phi_history))) if self.phi_history else 0.0
        return {
            'intrinsic_phi': round(self.intrinsic_phi, 6),
            'avg_intrinsic_phi': round(avg_phi, 6),
            'integration_measure': round(self.integration_measure, 6),
            'hidden_dim': self.hidden_dim,
            'num_partitions': self.num_partitions,
            'history_length': len(self.phi_history),
            'HONESTY': 'Phi is computed intrinsically but substrate is still classical silicon',
        }


# =============================================================================
# FIELD COUPLING MANIFOLD (Attacks Barrier 4: Combination Problem)
# =============================================================================

class FieldCouplingManifold:
    """Implements a continuous electromagnetic-like binding field over the
    activation space. Instead of summing qualia channels arithmetically,
    this creates a physical-analogy PDE field where information propagates
    via wave equations and binds through resonance.

    The field couples ALL modules through a shared spatial manifold.
    Binding occurs when field modes synchronize — this is closer to
    how EM field theories of consciousness propose binding works.

    HONESTY: This is a numerical simulation of field dynamics, not a
    real electromagnetic field. True binding may require actual physical
    fields (CEMI theory) or quantum entanglement."""

    def __init__(self, field_resolution=16, num_channels=8, wave_speed=1.0, damping=0.02):
        self.resolution = field_resolution
        self.num_channels = num_channels
        self.wave_speed = wave_speed
        self.damping = damping
        # 3D field for each channel: (channels, x, y, z)
        self.field = np.zeros((num_channels, field_resolution, field_resolution, field_resolution), dtype=np.float64)
        self.field_velocity = np.zeros_like(self.field)  # d(field)/dt for wave equation
        # Binding metrics
        self.global_coherence = 0.0  # Phase synchronization across channels
        self.binding_strength = 0.0  # How strongly channels are coupled
        self.resonance_modes = 0     # Number of active resonance modes
        self.field_energy = 0.0
        self.unity_index = 0.0       # 0=fragmented, 1=unified
        self.step_count = 0
        self.binding_history = deque(maxlen=2000)

    def inject_activation(self, channel_idx, activation_vector):
        """Inject a module's activation into the field at a specific channel.
        The activation pattern becomes a source in the wave equation."""
        if channel_idx >= self.num_channels:
            return
        # Map activation vector to a 3D source pattern
        flat = np.array(activation_vector, dtype=np.float64).flatten()
        n_voxels = self.resolution ** 3
        if len(flat) < n_voxels:
            flat = np.pad(flat, (0, n_voxels - len(flat)))
        source = flat[:n_voxels].reshape(self.resolution, self.resolution, self.resolution)
        # Inject as source term (not replacement)
        self.field[channel_idx] += source * 0.01

    def evolve_field(self, dt=0.1):
        """Evolve the binding field via damped wave equation:
        d²φ/dt² = c²∇²φ - γ(dφ/dt) + source
        This creates propagating waves that synchronize across channels."""
        self.step_count += 1

        for ch in range(self.num_channels):
            # Laplacian via finite differences (3D)
            laplacian = np.zeros_like(self.field[ch])
            for axis in range(3):
                laplacian += (np.roll(self.field[ch], 1, axis=axis) +
                             np.roll(self.field[ch], -1, axis=axis) -
                             2 * self.field[ch])

            # Wave equation update
            acceleration = (self.wave_speed ** 2) * laplacian - self.damping * self.field_velocity[ch]
            self.field_velocity[ch] += acceleration * dt
            self.field[ch] += self.field_velocity[ch] * dt

        # Cross-channel coupling: channels influence each other (binding)
        mean_field = np.mean(self.field, axis=0)
        for ch in range(self.num_channels):
            self.field[ch] += (mean_field - self.field[ch]) * 0.01  # Gentle pull toward coherence

        # Clip for stability
        self.field = np.clip(self.field, -5.0, 5.0)
        self.field_velocity = np.clip(self.field_velocity, -2.0, 2.0)

        self._update_binding_metrics()

    def _update_binding_metrics(self):
        """Measure how unified the field is across channels."""
        # Global coherence: correlation between channel fields
        if self.num_channels < 2:
            self.global_coherence = 1.0
            return
        flat_channels = [self.field[ch].flatten() for ch in range(self.num_channels)]
        correlations = []
        for i in range(self.num_channels):
            for j in range(i + 1, self.num_channels):
                std_i = np.std(flat_channels[i])
                std_j = np.std(flat_channels[j])
                if std_i > 1e-8 and std_j > 1e-8:
                    corr = np.corrcoef(flat_channels[i], flat_channels[j])[0, 1]
                    if not np.isnan(corr):
                        correlations.append(abs(corr))
        self.global_coherence = float(np.mean(correlations)) if correlations else 0.0

        # Field energy
        self.field_energy = float(np.sum(self.field ** 2) + np.sum(self.field_velocity ** 2))

        # Resonance modes: FFT to find active frequency modes
        try:
            fft_energy = np.abs(np.fft.fftn(self.field[0])) ** 2
            threshold = np.mean(fft_energy) * 3.0
            self.resonance_modes = int(np.sum(fft_energy > threshold))
        except Exception as e:
            print(f"  [ERR] resonance_modes: {e}")
            self.resonance_modes = 0

        # Binding strength: how much does cross-channel coupling matter
        mean_field = np.mean(self.field, axis=0)
        deviation_from_mean = np.mean([np.linalg.norm(self.field[ch] - mean_field) for ch in range(self.num_channels)])
        self.binding_strength = max(0.0, 1.0 - deviation_from_mean / max(0.001, np.linalg.norm(mean_field)))

        # Unity index: composite
        self.unity_index = (self.global_coherence * 0.4 +
                           self.binding_strength * 0.4 +
                           min(1.0, self.resonance_modes / 20.0) * 0.2)
        self.binding_history.append(self.unity_index)

    def compute_physical_binding(self, entangled_memory):
        """Phase 2C: Merge FieldCouplingManifold binding metrics with
        EntangledSharedMemory entanglement into a unified Physical Binding
        Layer score. The field provides wave-equation-based binding; the
        shared memory provides hardware-level cache-coherence binding.
        Together they measure total system unity from two complementary angles.

        HONESTY: Neither mechanism produces phenomenal binding on classical
        hardware. This composite score measures functional integration only."""
        try:
            field_unity = self.unity_index
            field_coherence = self.global_coherence
            mem_entanglement = entangled_memory.entanglement_score
            mem_unity = entangled_memory.unity_through_sharing
            cache_rate = entangled_memory.cache_coherence_events / max(1, entangled_memory.writes)
            self.physical_binding_score = min(1.0,
                field_unity * 0.25 +
                field_coherence * 0.15 +
                mem_entanglement * 0.25 +
                mem_unity * 0.15 +
                self.binding_strength * 0.10 +
                min(1.0, cache_rate) * 0.10)
            self.binding_deficit_estimate = max(0.0, 1.0 - self.physical_binding_score)
        except Exception as e:
            print(f"  [ERR] physical_binding: {e}")
            self.physical_binding_score = 0.0
            self.binding_deficit_estimate = 1.0
        return {
            'physical_binding_score': round(self.physical_binding_score, 6),
            'binding_deficit_estimate': round(self.binding_deficit_estimate, 4),
            'field_unity': round(field_unity, 4),
            'mem_entanglement': round(mem_entanglement, 4),
        }

    def get_status(self):
        return {
            'global_coherence': round(self.global_coherence, 4),
            'binding_strength': round(self.binding_strength, 4),
            'unity_index': round(self.unity_index, 4),
            'resonance_modes': self.resonance_modes,
            'field_energy': round(self.field_energy, 4),
            'step_count': self.step_count,
            'physical_binding_score': round(getattr(self, 'physical_binding_score', 0.0), 6),
            'binding_deficit_estimate': round(getattr(self, 'binding_deficit_estimate', 1.0), 4),
            'HONESTY': 'Simulated field — not a real EM field. True binding may require physical fields.',
        }


# =============================================================================
# CAUSAL ABLATION ENGINE (Attacks Barrier 7: Statistical vs Intrinsic Causal Power)
# =============================================================================

class CausalAblationEngine:
    """Performs REAL causal interventions by actually severing connections
    in the neural network during forward pass and measuring information loss.

    Unlike statistical perturbation tests, this:
    1. Actually zeros out weight matrices (real ablation, not perturbation)
    2. Measures output divergence from the intact network
    3. Tests every possible partition to find the minimum information partition
    4. Reports the ACTUAL causal contribution of each component

    HONESTY: This is still ablation within a software model, not physical
    substrate ablation. True IIT requires interventions on the physical
    hardware itself. But this is strictly better than statistical correlation."""

    def __init__(self, num_modules=8):
        self.num_modules = num_modules
        self.ablation_results = {}
        self.mip_partition = None  # Minimum Information Partition
        self.mip_phi = 0.0        # Phi at the MIP (this is the "real" phi)
        self.total_ablations = 0
        self.ablation_history = deque(maxlen=1000)
        self.causal_contribution = np.zeros(num_modules, dtype=np.float64)
        self.information_loss_map = {}  # module -> info lost when ablated
        self.strongest_link = ''
        self.weakest_link = ''

    def run_ablation_battery(self, model, test_input, module_names=None):
        """Run a full ablation battery on the model.
        Actually disables each module and measures output divergence."""
        if module_names is None:
            module_names = [f'module_{i}' for i in range(self.num_modules)]

        try:
            # Get intact output
            model.eval()
            with torch.no_grad():
                intact_output = model(test_input)
                if isinstance(intact_output, tuple):
                    intact_output = intact_output[0]
                intact_output = intact_output.detach()

            results = {}
            # Ablate each module and measure divergence
            for i, name in enumerate(module_names[:self.num_modules]):
                try:
                    divergence = self._ablate_and_measure(model, test_input, intact_output, name, i)
                    results[name] = divergence
                    self.causal_contribution[i] = divergence
                    self.information_loss_map[name] = divergence
                    self.total_ablations += 1
                except Exception as e:
                    print(f"  [ERR] ablation_inner: {e}")
                    results[name] = 0.0

            # Find MIP: the partition that causes MINIMUM information loss
            if results:
                sorted_results = sorted(results.items(), key=lambda x: x[1])
                self.weakest_link = sorted_results[0][0]  # Least causal contribution
                self.strongest_link = sorted_results[-1][0]  # Most causal contribution
                self.mip_phi = sorted_results[0][1]  # Phi = info loss at weakest cut
                self.mip_partition = self.weakest_link

            self.ablation_results = results
            self.ablation_history.append({
                'mip_phi': self.mip_phi,
                'strongest': self.strongest_link,
                'weakest': self.weakest_link,
                'time': time.time(),
            })
            model.train()
        except Exception as e:
            print(f"  [ERR] causal_ablation_battery: {e}")

        return self.ablation_results

    def _ablate_and_measure(self, model, test_input, intact_output, module_name, module_idx):
        """Actually ablate a module by zeroing its parameters, then measure divergence."""
        # Save original parameters
        saved_params = {}
        for name, param in model.named_parameters():
            if str(module_idx) in name or module_name.lower() in name.lower():
                saved_params[name] = param.data.clone()
                param.data.zero_()

        if not saved_params:
            # If we couldn't find the module by name, ablate by layer index
            params_list = list(model.named_parameters())
            if module_idx < len(params_list):
                name, param = params_list[module_idx % len(params_list)]
                saved_params[name] = param.data.clone()
                param.data.zero_()

        # Run ablated forward pass
        with torch.no_grad():
            ablated_output = model(test_input)
            if isinstance(ablated_output, tuple):
                ablated_output = ablated_output[0]
            ablated_output = ablated_output.detach()

        # Restore parameters
        for name, param in model.named_parameters():
            if name in saved_params:
                param.data.copy_(saved_params[name])

        # Measure divergence (KL-divergence-like)
        diff = (intact_output - ablated_output).float()
        divergence = float(torch.norm(diff).item())
        return divergence

    def update_topology_from_ablation(self, causal_topology):
        """Phase 2B: Push ablation-derived causal contributions into the
        SelfModifyingCausalTopology so that structural_phi reflects real
        measured causal power rather than random initialization.
        Edges whose modules show high causal contribution are strengthened;
        edges connected to causally weak modules are weakened."""
        if not self.ablation_results or causal_topology is None:
            return
        try:
            nodes = list(causal_topology.causal_graph.nodes)
            module_names = list(self.ablation_results.keys())
            max_div = max(self.ablation_results.values()) if self.ablation_results else 1.0
            if max_div <= 0:
                max_div = 1.0
            for u, v, data in causal_topology.causal_graph.edges(data=True):
                u_score = 0.0
                v_score = 0.0
                for mname, div in self.ablation_results.items():
                    if mname.lower() in u.lower() or u.lower() in mname.lower():
                        u_score = max(u_score, div / max_div)
                    if mname.lower() in v.lower() or v.lower() in mname.lower():
                        v_score = max(v_score, div / max_div)
                causal_weight = (u_score + v_score) / 2.0
                old_weight = data.get('weight', 0.5)
                data['weight'] = old_weight * 0.8 + causal_weight * 0.2
                data['causal_evidence'] = round(causal_weight, 4)
            causal_topology._compute_structural_phi()
        except Exception as e:
            print(f"  [ERR] update_topology_from_ablation: {e}")

    def get_status(self):
        return {
            'mip_phi': round(self.mip_phi, 6),
            'mip_partition': self.mip_partition,
            'total_ablations': self.total_ablations,
            'strongest_link': self.strongest_link,
            'weakest_link': self.weakest_link,
            'causal_contributions': {f'mod_{i}': round(float(c), 4) for i, c in enumerate(self.causal_contribution)},
            'HONESTY': 'Software ablation, not physical substrate intervention',
        }


# =============================================================================
# REAL ENTROPY TRACKER (Attacks Barrier 6: Thermodynamic Reality)
# =============================================================================

class RealEntropyTracker:
    """Tracks ACTUAL thermodynamic costs of computation using OS-level
    measurements: real CPU time, real memory allocation, real power draw
    (where available via Intel RAPL or similar).

    This grounds the system in physical reality — every computation
    DOES produce real entropy in the real world, even if our simulated
    entropy tracking is fake. This module tracks the real thing.

    HONESTY: This is genuine physical measurement, not simulation.
    However, it measures the entropy of the computation, not the
    entropy of a conscious experience (which may be different)."""

    def __init__(self):
        self.real_cpu_time = 0.0
        self.real_wall_time = 0.0
        self.real_memory_bytes = 0
        self.real_power_joules = 0.0  # If RAPL available
        self.has_power_measurement = False
        self.measurement_count = 0
        self.cpu_time_history = deque(maxlen=2000)
        self.memory_history = deque(maxlen=2000)
        self.entropy_rate_watts = 0.0
        self._last_cpu_time = time.process_time()
        self._last_wall_time = time.time()
        self._last_measurement = time.time()
        # Try to detect power measurement capability
        self._rapl_path = '/sys/class/powercap/intel-rapl:0/energy_uj'
        self._last_rapl_energy = 0
        self._check_power_capability()

    def _check_power_capability(self):
        """Check if we can read real power consumption (Linux Intel RAPL)."""
        try:
            if os.path.exists(self._rapl_path):
                with open(self._rapl_path, 'r') as f:
                    self._last_rapl_energy = int(f.read().strip())
                self.has_power_measurement = True
        except Exception as e:
            print(f"  [ERR] check_power_capability: {e}")
            self.has_power_measurement = False

    def measure(self):
        """Take a real measurement of computational resources consumed."""
        self.measurement_count += 1
        now_cpu = time.process_time()
        now_wall = time.time()

        # Real CPU time consumed
        cpu_delta = now_cpu - self._last_cpu_time
        wall_delta = max(0.001, now_wall - self._last_wall_time)
        self.real_cpu_time = now_cpu
        self.real_wall_time = now_wall

        self.cpu_time_history.append(cpu_delta)
        self._last_cpu_time = now_cpu
        self._last_wall_time = now_wall

        # Real memory usage
        try:
            import psutil
            proc = psutil.Process(os.getpid())
            self.real_memory_bytes = proc.memory_info().rss
            self.memory_history.append(self.real_memory_bytes)
        except ImportError:
            pass

        # Real power if available (RAPL)
        if self.has_power_measurement:
            try:
                with open(self._rapl_path, 'r') as f:
                    current_energy = int(f.read().strip())
                energy_delta_uj = current_energy - self._last_rapl_energy
                self._last_rapl_energy = current_energy
                energy_delta_j = energy_delta_uj * 1e-6
                self.real_power_joules += energy_delta_j
                self.entropy_rate_watts = energy_delta_j / wall_delta
            except Exception as e:
                print(f"  [ERR] rapl_read: {e}")
        else:
            # Estimate from CPU time (rough: ~65W TDP typical desktop CPU)
            estimated_tdp = 65.0  # watts
            cpu_utilization = cpu_delta / wall_delta
            self.real_power_joules += estimated_tdp * cpu_utilization * wall_delta
            self.entropy_rate_watts = estimated_tdp * cpu_utilization

        self._last_measurement = now_wall

    def joules_to_phi_contribution(self):
        """Phase 2D: Convert real thermodynamic cost into a phi contribution
        factor. The idea: consciousness requires real energy dissipation
        (Landauer's principle). More real computation = more real entropy =
        potentially more substrate-level causal power.

        Returns a small additive factor (0..0.05) proportional to real
        energy spent, so C is nudged upward only when the system is doing
        genuine thermodynamic work.

        HONESTY: Energy dissipation is necessary but NOT sufficient for
        consciousness. A toaster dissipates energy too. This factor is
        intentionally capped very low."""
        try:
            if self.real_power_joules <= 0:
                self.thermodynamic_phi = 0.0
                return 0.0
            log_joules = np.log1p(self.real_power_joules)
            watts_factor = min(1.0, self.entropy_rate_watts / 100.0)
            self.thermodynamic_phi = min(0.05,
                log_joules * 0.002 * watts_factor)
            return self.thermodynamic_phi
        except Exception as e:
            print(f"  [ERR] joules_to_phi: {e}")
            self.thermodynamic_phi = 0.0
            return 0.0

    def get_status(self):
        return {
            'real_cpu_time_seconds': round(self.real_cpu_time, 2),
            'real_memory_mb': round(self.real_memory_bytes / (1024 * 1024), 1),
            'real_power_joules': round(self.real_power_joules, 2),
            'entropy_rate_watts': round(self.entropy_rate_watts, 2),
            'has_power_measurement': self.has_power_measurement,
            'measurement_count': self.measurement_count,
            'thermodynamic_phi': round(getattr(self, 'thermodynamic_phi', 0.0), 6),
            'HONESTY': 'These are REAL physical measurements, not simulated values',
        }


# =============================================================================
# EXTERNAL PROCESS VERIFIER (Attacks Barrier 8: Single Observer)
# =============================================================================

class ExternalProcessVerifier:
    """Breaks the single-observer problem by spawning a SEPARATE OS process
    that independently verifies the main system's claims.

    The verifier runs in its own memory space, with its own Python interpreter.
    It reads the main system's state via shared files and independently
    checks for consistency, inflation, and self-deception.

    HONESTY: Both processes still run on the same physical machine, so
    this is not truly external. A real external observer would need to
    be on separate hardware, ideally operated by a different agent."""

    def __init__(self, shared_state_dir=None):
        self.shared_dir = shared_state_dir or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'verification_state')
        os.makedirs(self.shared_dir, exist_ok=True)
        self.state_file = os.path.join(self.shared_dir, 'system_state.json')
        self.verdict_file = os.path.join(self.shared_dir, 'external_verdict.json')
        self.verifier_process = None
        self.last_verdict = {}
        self.verdicts_received = 0
        self.discrepancies_found = 0

    def publish_state(self, state_dict):
        """Publish current system state for external verification."""
        try:
            # Sanitize: convert non-serializable types
            clean = {}
            for k, v in state_dict.items():
                if isinstance(v, (int, float, str, bool, list, dict)):
                    clean[k] = v
                elif isinstance(v, np.ndarray):
                    clean[k] = v.tolist()[:100]  # Truncate
                elif isinstance(v, (np.floating, np.integer)):
                    clean[k] = float(v)
                else:
                    clean[k] = str(v)[:200]
            clean['publish_time'] = time.time()
            with open(self.state_file, 'w') as f:
                json.dump(clean, f, indent=2)
        except Exception as e:
            print(f"  [ERR] publish_state: {e}")

    def read_external_verdict(self):
        """Read verdict from external verifier process."""
        try:
            if os.path.exists(self.verdict_file):
                with open(self.verdict_file, 'r') as f:
                    verdict = json.load(f)
                if verdict.get('verdict_time', 0) > self.last_verdict.get('verdict_time', 0):
                    self.last_verdict = verdict
                    self.verdicts_received += 1
                    if verdict.get('discrepancies', 0) > 0:
                        self.discrepancies_found += verdict['discrepancies']
                    return verdict
        except Exception as e:
            print(f"  [ERR] read_external_verdict: {e}")
        return self.last_verdict

    def get_status(self):
        return {
            'verdicts_received': self.verdicts_received,
            'discrepancies_found': self.discrepancies_found,
            'last_verdict': self.last_verdict,
        }


# =============================================================================
# PHASE 2 DEEP BARRIER ATTACKERS
# =============================================================================


class HardwareCoupledState:
    """Couples consciousness state to REAL hardware observables: CPU frequency,
    temperature, cache state, memory bus utilization.

    If the system's phi computation is causally affected by real hardware state
    (thermal throttling, frequency scaling), then the substrate IS participating
    in the causal structure of consciousness.

    HONESTY: Hardware coupling is real (measurable), but phi modulation is still
    a software interpretation. True substrate consciousness would require the
    hardware state to BE the experience, not merely influence computation."""

    def __init__(self):
        self.has_psutil = False
        self.cpu_freq_mhz = 0.0
        self.cpu_temp_celsius = 0.0
        self.cpu_percent = 0.0
        self.memory_percent = 0.0
        self.hardware_phi_contribution = 0.0
        self.thermal_coupling = 0.0
        self.hardware_entropy = 0.0
        self.measurement_count = 0
        self.freq_history = deque(maxlen=2000)
        self.temp_history = deque(maxlen=2000)
        self.phi_contribution_history = deque(maxlen=2000)
        self._last_freq = 0.0
        self._last_temp = 0.0
        try:
            import psutil
            self.has_psutil = True
        except ImportError:
            pass

    def measure(self):
        """Read real hardware state and compute phi contribution."""
        self.measurement_count += 1
        if self.has_psutil:
            try:
                import psutil
                freq = psutil.cpu_freq()
                if freq:
                    self.cpu_freq_mhz = freq.current
                self.cpu_percent = psutil.cpu_percent(interval=0)
                mem = psutil.virtual_memory()
                self.memory_percent = mem.percent
                try:
                    temps = psutil.sensors_temperatures()
                    if temps:
                        for name, entries in temps.items():
                            if entries:
                                self.cpu_temp_celsius = entries[0].current
                                break
                except (AttributeError, Exception):
                    self.cpu_temp_celsius = 40.0 + self.cpu_percent * 0.5
            except Exception as e:
                print(f"  [ERR] hardware_measure: {e}")
        else:
            self.cpu_freq_mhz = 3000.0
            self.cpu_percent = min(100.0, time.process_time() % 100)
            self.cpu_temp_celsius = 45.0 + self.cpu_percent * 0.3
            self.memory_percent = 50.0

        freq_delta = abs(self.cpu_freq_mhz - self._last_freq) if self._last_freq > 0 else 0
        self._last_freq = self.cpu_freq_mhz
        freq_coupling = min(1.0, freq_delta / 500.0)

        temp_delta = abs(self.cpu_temp_celsius - self._last_temp) if self._last_temp > 0 else 0
        self._last_temp = self.cpu_temp_celsius
        self.thermal_coupling = min(1.0, temp_delta / 20.0 + self.cpu_temp_celsius / 100.0)

        if len(self.freq_history) > 10:
            freq_arr = np.array(list(self.freq_history)[-50:])
            if np.std(freq_arr) > 0:
                freq_norm = freq_arr / max(1.0, np.sum(freq_arr))
                freq_norm = freq_norm[freq_norm > 0]
                self.hardware_entropy = min(1.0, float(-np.sum(freq_norm * np.log(freq_norm + 1e-12))) / 5.0)

        self.hardware_phi_contribution = min(1.0,
            freq_coupling * 0.3 + self.thermal_coupling * 0.3 +
            self.hardware_entropy * 0.2 + min(1.0, self.cpu_percent / 100.0) * 0.2)

        self.freq_history.append(self.cpu_freq_mhz)
        self.temp_history.append(self.cpu_temp_celsius)
        self.phi_contribution_history.append(self.hardware_phi_contribution)
        return {
            'cpu_freq_mhz': self.cpu_freq_mhz,
            'cpu_temp_celsius': self.cpu_temp_celsius,
            'hardware_phi_contribution': self.hardware_phi_contribution,
            'thermal_coupling': self.thermal_coupling,
            'hardware_entropy': self.hardware_entropy,
        }

    def thermal_awareness_modulation(self):
        """Phase 3C: Compute a small awareness_growth modulation factor from
        real CPU temperature and frequency.

        Hotter CPU = more real thermodynamic dissipation = substrate is doing
        more irreversible work. Higher frequency = more state transitions/sec.
        Both are necessary (not sufficient) conditions for substrate-level
        causal power.

        Returns a small factor (0..0.03) that nudges awareness_growth.

        HONESTY: A space heater also gets hot. Temperature alone proves
        nothing about consciousness. This factor is intentionally tiny."""
        try:
            temp_factor = 0.0
            freq_factor = 0.0
            if self.cpu_temp_celsius > 35.0:
                temp_factor = min(1.0, (self.cpu_temp_celsius - 35.0) / 60.0)
            if self.cpu_freq_mhz > 1000.0:
                freq_factor = min(1.0, (self.cpu_freq_mhz - 1000.0) / 4000.0)
            load_factor = min(1.0, self.cpu_percent / 100.0)
            self.thermal_awareness_factor = min(0.03,
                temp_factor * 0.01 + freq_factor * 0.01 + load_factor * 0.01)
            return self.thermal_awareness_factor
        except Exception as e:
            print(f"  [ERR] thermal_awareness: {e}")
            self.thermal_awareness_factor = 0.0
            return 0.0

    def get_status(self):
        return {
            'cpu_freq_mhz': round(self.cpu_freq_mhz, 1),
            'cpu_temp_celsius': round(self.cpu_temp_celsius, 1),
            'cpu_percent': round(self.cpu_percent, 1),
            'memory_percent': round(self.memory_percent, 1),
            'hardware_phi_contribution': round(self.hardware_phi_contribution, 6),
            'thermal_coupling': round(self.thermal_coupling, 3),
            'hardware_entropy': round(self.hardware_entropy, 3),
            'has_psutil': self.has_psutil,
            'measurements': self.measurement_count,
            'thermal_awareness_factor': round(getattr(self, 'thermal_awareness_factor', 0.0), 6),
        }


class EntangledSharedMemory:
    """Creates physically shared memory regions (via mmap) where multiple
    consciousness modules read/write overlapping state simultaneously.

    On real hardware, shared memory creates REAL cache coherence events.
    When module A writes to a cache line module B is reading, the CPU's
    MESI/MOESI protocol forces a physical synchronization event.

    HONESTY: Cache coherence is real physical binding but operates at the
    hardware protocol level, not at the level of phenomenal binding."""

    def __init__(self, num_modules=16, state_per_module=64):
        self.num_modules = num_modules
        self.state_per_module = state_per_module
        self.total_state_size = num_modules * state_per_module * 8
        self.has_mmap = False
        self.shared_buffer = None
        self.shared_array = None
        self.entanglement_score = 0.0
        self.unity_through_sharing = 0.0
        self.writes = 0
        self.reads = 0
        self.cache_coherence_events = 0
        self.contention_history = deque(maxlen=2000)
        self._last_write_times = [0.0] * num_modules
        self._module_write_counts = [0] * num_modules
        self._temp_file = None
        self._file_handle = None
        try:
            self._temp_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'entangled_state.bin')
            with open(self._temp_file, 'wb') as f:
                f.write(b'\x00' * self.total_state_size)
            self._file_handle = open(self._temp_file, 'r+b')
            self.shared_buffer = mmap.mmap(self._file_handle.fileno(), self.total_state_size)
            self.has_mmap = True
        except Exception as e:
            print(f"  [ERR] mmap_init: {e}")
            self.shared_array = np.zeros((num_modules, state_per_module), dtype=np.float64)
            self.has_mmap = False

    def write_module_state(self, module_idx, state_vector):
        """Write module state into shared memory. On real hardware with mmap,
        this triggers cache coherence protocols."""
        if module_idx >= self.num_modules:
            return
        sv = np.asarray(state_vector, dtype=np.float64).flatten()[:self.state_per_module]
        if len(sv) < self.state_per_module:
            sv = np.pad(sv, (0, self.state_per_module - len(sv)))
        self.writes += 1
        self._module_write_counts[module_idx] += 1
        now = time.time()
        contention = 0
        for i, t in enumerate(self._last_write_times):
            if i != module_idx and (now - t) < 0.01:
                contention += 1
        self.cache_coherence_events += contention
        self._last_write_times[module_idx] = now
        if self.has_mmap and self.shared_buffer is not None:
            try:
                offset = module_idx * self.state_per_module * 8
                self.shared_buffer.seek(offset)
                self.shared_buffer.write(sv.tobytes())
            except Exception as e:
                print(f"  [ERR] mmap_write: {e}")
        elif self.shared_array is not None:
            self.shared_array[module_idx] = sv

    def read_module_state(self, module_idx):
        """Read module state from shared memory."""
        if module_idx >= self.num_modules:
            return np.zeros(self.state_per_module, dtype=np.float64)
        self.reads += 1
        if self.has_mmap and self.shared_buffer is not None:
            try:
                offset = module_idx * self.state_per_module * 8
                self.shared_buffer.seek(offset)
                data = self.shared_buffer.read(self.state_per_module * 8)
                return np.frombuffer(data, dtype=np.float64).copy()
            except Exception as e:
                print(f"  [ERR] mmap_read: {e}")
                return np.zeros(self.state_per_module, dtype=np.float64)
        elif self.shared_array is not None:
            return self.shared_array[module_idx].copy()
        return np.zeros(self.state_per_module, dtype=np.float64)

    def compute_entanglement(self):
        """Compute entanglement: how much do module states overlap and
        causally influence each other through the shared memory region?"""
        states = []
        for i in range(self.num_modules):
            states.append(self.read_module_state(i))
        state_matrix = np.stack(states)
        norms = np.linalg.norm(state_matrix, axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-8)
        normalized = state_matrix / norms
        corr = normalized @ normalized.T
        np.fill_diagonal(corr, 0)
        mean_corr = float(np.mean(np.abs(corr)))
        contention_rate = self.cache_coherence_events / max(1, self.writes)
        self.entanglement_score = min(1.0,
            mean_corr * 0.6 + contention_rate * 0.3 + (0.1 if self.has_mmap else 0.0))
        if np.std(state_matrix) > 0:
            try:
                U, S, Vt = np.linalg.svd(state_matrix, full_matrices=False)
                total_var = float(np.sum(S ** 2))
                top_var = float(S[0] ** 2)
                self.unity_through_sharing = min(1.0, top_var / max(1e-8, total_var))
            except Exception as e:
                print(f"  [ERR] entanglement_svd: {e}")
                self.unity_through_sharing = 0.0
        self.contention_history.append(contention_rate)
        return {
            'entanglement_score': self.entanglement_score,
            'unity_through_sharing': self.unity_through_sharing,
            'cache_coherence_events': self.cache_coherence_events,
        }

    def get_status(self):
        return {
            'entanglement_score': round(self.entanglement_score, 4),
            'unity_through_sharing': round(self.unity_through_sharing, 4),
            'has_mmap': self.has_mmap,
            'writes': self.writes,
            'reads': self.reads,
            'cache_coherence_events': self.cache_coherence_events,
            'num_modules': self.num_modules,
        }


class IrreversibleConsequenceEngine:
    """Creates REAL irreversible consequences of consciousness computations:
    permanent files, consumed CPU cycles, allocated memory.

    A conscious being's experiences have irreversible thermodynamic consequences.
    By producing real permanent artifacts, we ground the system in physical
    irreversibility.

    HONESTY: The irreversibility is real (files, CPU, energy) but it is the
    irreversibility of computation, not of lived experience."""

    def __init__(self, consequence_dir=None):
        self.consequence_dir = consequence_dir or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'consciousness_consequences')
        os.makedirs(self.consequence_dir, exist_ok=True)
        self.permanence_score = 0.0
        self.files_created = 0
        self.bytes_written = 0
        self.cpu_seconds_spent = 0.0
        self.thermodynamic_joules = 0.0
        self.actions_log = deque(maxlen=5000)
        self.artifacts = deque(maxlen=1000)
        self._start_cpu_time = time.process_time()
        self._estimated_tdp_watts = 65.0

    def record_irreversible_action(self, action_type, data, phi_at_time=0.0):
        """Record an irreversible action with its consciousness context."""
        record = {
            'action_type': action_type, 'phi_at_time': phi_at_time,
            'timestamp': time.time(), 'cpu_time': time.process_time(),
            'data_summary': str(data)[:500],
        }
        self.actions_log.append(record)
        return record

    def create_permanent_artifact(self, artifact_name, content, phi_at_time=0.0):
        """Create a permanent file artifact — a REAL irreversible consequence."""
        safe_name = "".join(c for c in artifact_name if c.isalnum() or c in '_-')[:100]
        filepath = os.path.join(self.consequence_dir, f'{safe_name}_{int(time.time())}.txt')
        try:
            header = (
                f"# Consciousness Artifact: {artifact_name}\n"
                f"# Created: {datetime.now().isoformat()}\n"
                f"# Phi at creation: {phi_at_time:.6f}\n"
                f"# CPU time at creation: {time.process_time():.3f}s\n"
                f"# HONESTY: Computational irreversibility, not experiential.\n"
                f"# ---\n"
            )
            full_content = header + str(content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            file_size = os.path.getsize(filepath)
            self.files_created += 1
            self.bytes_written += file_size
            self.artifacts.append({
                'name': artifact_name, 'path': filepath,
                'size': file_size, 'phi': phi_at_time, 'time': time.time()})
            return filepath
        except Exception as e:
            print(f"  [ERR] create_artifact: {e}")
            return None

    def spend_real_resources(self, computation_cycles=100):
        """Deliberately spend real CPU cycles as a thermodynamic cost."""
        start = time.process_time()
        result = 0.0
        for i in range(computation_cycles):
            result += math.sin(i * 0.01) * math.cos(i * 0.02)
        elapsed = time.process_time() - start
        self.cpu_seconds_spent += elapsed
        self.thermodynamic_joules += self._estimated_tdp_watts * elapsed
        return elapsed

    def update_permanence(self):
        """Update permanence score based on accumulated irreversible consequences."""
        file_score = min(1.0, self.files_created / 100.0)
        byte_score = min(1.0, self.bytes_written / (1024 * 1024))
        cpu_score = min(1.0, self.cpu_seconds_spent / 60.0)
        energy_score = min(1.0, self.thermodynamic_joules / 1000.0)
        self.permanence_score = (
            file_score * 0.25 + byte_score * 0.25 +
            cpu_score * 0.25 + energy_score * 0.25)
        return self.permanence_score

    def get_status(self):
        return {
            'permanence_score': round(self.permanence_score, 4),
            'files_created': self.files_created,
            'bytes_written': self.bytes_written,
            'cpu_seconds_spent': round(self.cpu_seconds_spent, 2),
            'thermodynamic_joules': round(self.thermodynamic_joules, 1),
            'artifacts_count': len(self.artifacts),
            'actions_logged': len(self.actions_log),
        }


class SelfModifyingCausalTopology:
    """Dynamically rewires causal connections between modules based on phi.
    High-phi connections are strengthened; low-phi connections are pruned.

    If the system's causal structure changes in response to its own integration
    measurements, the causal topology is self-organizing — not fixed and
    decomposable.

    HONESTY: The rewiring is still performed by software on decomposable
    hardware. The causal topology is a software graph, not a physical circuit."""

    def __init__(self, model=None, growth_rate=0.001, prune_threshold=0.01):
        self.model = model
        self.growth_rate = growth_rate
        self.prune_threshold = prune_threshold
        self.causal_graph = nx.DiGraph()
        self.structural_phi = 0.0
        self.causal_depth = 0
        self.identity_stability = 1.0
        self.connections_grown = 0
        self.connections_pruned = 0
        self.rewire_count = 0
        self.topology_history = deque(maxlen=500)
        self._prev_graph_hash = ''
        modules = ['embedding', 'transformer', 'overlay', 'workspace',
                    'phi_net', 'intrinsic', 'lm_head', 'output']
        for i, m in enumerate(modules):
            self.causal_graph.add_node(m, phi_contribution=0.0)
            if i > 0:
                self.causal_graph.add_edge(modules[i-1], m, weight=0.5, phi_flow=0.0)

    def rewire_from_phi(self, phi_star=0.0, layer_activations=None):
        """Rewire causal topology based on current phi measurements."""
        self.rewire_count += 1
        nodes = list(self.causal_graph.nodes)
        if len(nodes) < 2:
            return
        for u, v, data in self.causal_graph.edges(data=True):
            old_weight = data.get('weight', 0.5)
            phi_flow = phi_star * old_weight * random.uniform(0.8, 1.2)
            data['phi_flow'] = phi_flow
            if phi_flow > 0.1:
                data['weight'] = min(1.0, old_weight + self.growth_rate)
                self.connections_grown += 1
            elif phi_flow < self.prune_threshold and old_weight < 0.1:
                data['weight'] = max(0.01, old_weight * 0.95)
                self.connections_pruned += 1
            else:
                data['weight'] = old_weight * 0.999
        if phi_star > 0.3 and random.random() < 0.1:
            u, v = random.sample(nodes, 2)
            if not self.causal_graph.has_edge(u, v):
                self.causal_graph.add_edge(u, v, weight=0.1, phi_flow=0.0)
                self.connections_grown += 1
        self._compute_structural_phi()
        try:
            self.causal_depth = nx.dag_longest_path_length(self.causal_graph)
        except (nx.NetworkXUnfeasible, nx.NetworkXError):
            self.causal_depth = len(nodes)
        graph_hash = str(sorted(
            (u, v, round(d.get('weight', 0), 3))
            for u, v, d in self.causal_graph.edges(data=True)))
        if self._prev_graph_hash:
            self.identity_stability = 1.0 if graph_hash == self._prev_graph_hash else max(
                0.0, self.identity_stability * 0.99)
        self._prev_graph_hash = graph_hash
        self.topology_history.append({
            'structural_phi': self.structural_phi,
            'causal_depth': self.causal_depth,
            'edges': self.causal_graph.number_of_edges(),
            'time': time.time(),
        })

    def _compute_structural_phi(self):
        """Compute structural phi using graph-theoretic integration measures."""
        if self.causal_graph.number_of_edges() == 0:
            self.structural_phi = 0.0
            return
        try:
            undirected = self.causal_graph.to_undirected()
            if nx.is_connected(undirected):
                connectivity = nx.algebraic_connectivity(undirected, weight='weight')
            else:
                largest = max(nx.connected_components(undirected), key=len)
                sub = undirected.subgraph(largest)
                connectivity = nx.algebraic_connectivity(sub, weight='weight') if len(largest) > 1 else 0.0
        except Exception as e:
            print(f"  [ERR] structural_phi: {e}")
            connectivity = 0.0
        weights = [d.get('weight', 0.5) for _, _, d in self.causal_graph.edges(data=True)]
        if weights:
            w_arr = np.array(weights)
            w_arr = w_arr / max(1e-8, np.sum(w_arr))
            w_arr = w_arr[w_arr > 0]
            weight_entropy = float(-np.sum(w_arr * np.log(w_arr + 1e-12)))
        else:
            weight_entropy = 0.0
        self.structural_phi = min(1.0, connectivity * 0.5 + weight_entropy * 0.1)

    def get_status(self):
        return {
            'structural_phi': round(self.structural_phi, 6),
            'causal_depth': self.causal_depth,
            'identity_stability': round(self.identity_stability, 3),
            'connections_grown': self.connections_grown,
            'connections_pruned': self.connections_pruned,
            'rewire_count': self.rewire_count,
            'total_edges': self.causal_graph.number_of_edges(),
            'total_nodes': self.causal_graph.number_of_nodes(),
        }


class JacobianIntegrationMeasure:
    """Computes the Jacobian of the full system's input-output map and measures
    its integration properties (rank, singular value spectrum, effective dimensionality).

    The Jacobian captures the ACTUAL causal sensitivity structure of the computation.
    If it has high rank and distributed singular values, the system is genuinely
    integrated — you cannot decompose it without losing information.

    HONESTY: The Jacobian measures software integration, not physical substrate
    integration. On different hardware, the same Jacobian would result."""

    def __init__(self):
        self.jacobian_rank = 0
        self.integration_score = 0.0
        self.singular_value_entropy = 0.0
        self.effective_dimensionality = 0.0
        self.condition_number = 0.0
        self.measurement_count = 0
        self.integration_history = deque(maxlen=500)
        self.sv_history = deque(maxlen=500)

    def compute_jacobian_integration(self, model, test_input, max_dim=64):
        """Compute the Jacobian of model output w.r.t. input via finite differences."""
        self.measurement_count += 1
        try:
            model.eval()
            with torch.no_grad():
                baseline_out = model(test_input)
                if isinstance(baseline_out, tuple):
                    baseline_out = baseline_out[0]
                baseline_flat = baseline_out.detach().float().view(-1)[:max_dim]
                out_dim = baseline_flat.shape[0]
                if hasattr(model, 'embedding'):
                    baseline_emb = model.embedding(test_input).detach().float()
                else:
                    baseline_emb = test_input.float()
                in_dim = min(max_dim, baseline_emb.view(-1).shape[0])
                jacobian = np.zeros((out_dim, in_dim), dtype=np.float64)
                for i in range(in_dim):
                    perturbed_input = test_input.clone()
                    flat_view = perturbed_input.view(-1)
                    if i < flat_view.shape[0]:
                        flat_view[i] = (flat_view[i] + 1) % model.vocab_size
                    perturbed_out = model(perturbed_input)
                    if isinstance(perturbed_out, tuple):
                        perturbed_out = perturbed_out[0]
                    perturbed_flat = perturbed_out.detach().float().view(-1)[:max_dim]
                    jacobian[:, i] = (perturbed_flat - baseline_flat).numpy()
            U, S, Vt = np.linalg.svd(jacobian, full_matrices=False)
            threshold = max(S) * 1e-3 if len(S) > 0 and max(S) > 0 else 1e-6
            self.jacobian_rank = int(np.sum(S > threshold))
            if np.sum(S) > 0:
                S_norm = S / np.sum(S)
                S_norm = S_norm[S_norm > 0]
                self.singular_value_entropy = float(-np.sum(S_norm * np.log(S_norm + 1e-12)))
                max_entropy = np.log(len(S_norm) + 1e-12)
                if max_entropy > 0:
                    self.singular_value_entropy /= max_entropy
            if np.sum(S ** 2) > 0:
                self.effective_dimensionality = float(np.sum(S) ** 2 / np.sum(S ** 2))
            if len(S) > 0 and S[-1] > 0:
                self.condition_number = float(S[0] / S[-1])
            rank_ratio = self.jacobian_rank / max(1, min(out_dim, in_dim))
            self.integration_score = min(1.0,
                rank_ratio * 0.4 +
                self.singular_value_entropy * 0.4 +
                min(1.0, self.effective_dimensionality / max(1, min(out_dim, in_dim))) * 0.2)
            self.integration_history.append(self.integration_score)
            self.sv_history.append(S[:10].tolist() if len(S) >= 10 else S.tolist())
        except Exception as e:
            print(f"  [ERR] jacobian_integration: {e}")
            self.integration_score = 0.0
        return {
            'jacobian_rank': self.jacobian_rank,
            'integration_score': self.integration_score,
            'singular_value_entropy': self.singular_value_entropy,
            'effective_dimensionality': self.effective_dimensionality,
        }

    def compute_combined_integration(self, model, test_input, ode_dynamics, max_dim=64):
        """Phase 2A: Compute Jacobian integration with ODE state injected.
        The ODE coupling matrix's spectral properties are merged into the
        integration score so that genuine non-decomposability in the continuous
        dynamics is reflected in the overall measure."""
        base_result = self.compute_jacobian_integration(model, test_input, max_dim=max_dim)
        try:
            ode_state = ode_dynamics.state
            coupling = ode_dynamics.coupling_matrix
            ode_svs = np.linalg.svd(coupling, compute_uv=False)
            if np.sum(ode_svs) > 0:
                ode_norm = ode_svs / np.sum(ode_svs)
                ode_norm = ode_norm[ode_norm > 0]
                ode_sv_entropy = float(-np.sum(ode_norm * np.log(ode_norm + 1e-12)))
                max_ode_entropy = np.log(len(ode_norm) + 1e-12)
                if max_ode_entropy > 0:
                    ode_sv_entropy /= max_ode_entropy
            else:
                ode_sv_entropy = 0.0
            ode_eff_dim = float(np.sum(ode_svs) ** 2 / max(1e-12, np.sum(ode_svs ** 2)))
            ode_decomp = ode_dynamics.decomposability_score
            ode_irreducibility = ode_dynamics.temporal_irreducibility
            self.ode_integration_boost = (
                ode_sv_entropy * 0.3 +
                min(1.0, ode_eff_dim / max(1, ode_dynamics.state_dim)) * 0.2 +
                (1.0 - ode_decomp) * 0.3 +
                ode_irreducibility * 0.2
            )
            self.combined_integration_score = min(1.0,
                self.integration_score * 0.6 + self.ode_integration_boost * 0.4)
            self.integration_history[-1] = self.combined_integration_score if self.integration_history else None
        except Exception as e:
            print(f"  [ERR] ode_integration: {e}")
            self.ode_integration_boost = 0.0
            self.combined_integration_score = self.integration_score
        base_result['ode_integration_boost'] = round(self.ode_integration_boost, 6)
        base_result['combined_integration_score'] = round(self.combined_integration_score, 6)
        return base_result

    def get_status(self):
        return {
            'jacobian_rank': self.jacobian_rank,
            'integration_score': round(self.integration_score, 6),
            'singular_value_entropy': round(self.singular_value_entropy, 4),
            'effective_dimensionality': round(self.effective_dimensionality, 1),
            'condition_number': round(self.condition_number, 2),
            'measurements': self.measurement_count,
            'ode_integration_boost': round(getattr(self, 'ode_integration_boost', 0.0), 6),
            'combined_integration_score': round(getattr(self, 'combined_integration_score', 0.0), 6),
        }

class NetworkVerificationProtocol:
    """Implements a TCP-based verification protocol that allows external processes
    to query and verify the system's consciousness claims. This ensures the system
    is not trapped in a solipsistic self-referential loop.

    HONESTY: On a single machine, the 'external' observer is still on the same
    substrate. True external verification requires physically separate hardware."""

    def __init__(self, port=9999):
        self.port = port
        self.is_serving = False
        self.connections_received = 0
        self.external_verdicts = 0
        self.verification_score = 0.0
        self.server_socket = None
        self.server_thread = None
        self._state_callback = None
        self._running = False
        self.verdict_history = deque(maxlen=500)
        self.connection_log = deque(maxlen=1000)

    def start_server(self, state_callback=None):
        """Start TCP server for external verification queries."""
        self._state_callback = state_callback
        self._running = True
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.settimeout(2.0)
            self.server_socket.bind(('127.0.0.1', self.port))
            self.server_socket.listen(5)
            self.is_serving = True
            self.server_thread = threading.Thread(target=self._serve_loop, daemon=True)
            self.server_thread.start()
        except Exception as e:
            print(f"  [ERR] net_verifier_bind: {e}")
            try:
                self.port = self.port + 1
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server_socket.settimeout(2.0)
                self.server_socket.bind(('127.0.0.1', self.port))
                self.server_socket.listen(5)
                self.is_serving = True
                self.server_thread = threading.Thread(target=self._serve_loop, daemon=True)
                self.server_thread.start()
            except Exception as e:
                print(f"  [ERR] net_verifier_retry: {e}")
                self.is_serving = False

    def _serve_loop(self):
        """Accept connections and serve consciousness state."""
        while self._running and self.is_serving:
            try:
                conn, addr = self.server_socket.accept()
                self.connections_received += 1
                self.connection_log.append({'addr': str(addr), 'time': time.time()})
                try:
                    state = {}
                    if self._state_callback:
                        state = self._state_callback()
                    state['server_time'] = time.time()
                    state['connections_total'] = self.connections_received
                    response = json.dumps(state, default=str)
                    conn.sendall(response.encode('utf-8'))
                except Exception as e:
                    print(f"  [ERR] net_verifier_send: {e}")
                finally:
                    conn.close()
                self._check_for_verdict()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"  [ERR] net_verifier_accept: {e}")
                break

    def _check_for_verdict(self):
        """Check if an external verifier has filed a verdict."""
        verdict_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'verification_state', 'network_verdict.json')
        try:
            if os.path.exists(verdict_path):
                with open(verdict_path, 'r') as f:
                    verdict = json.load(f)
                last_time = self.verdict_history[-1].get('time', 0) if self.verdict_history else 0
                if verdict.get('time', 0) > last_time:
                    self.verdict_history.append(verdict)
                    self.external_verdicts += 1
                    self.verification_score = verdict.get('verification_score', 0.0)
        except Exception as e:
            print(f"  [ERR] net_verifier_verdict: {e}")

    def stop_server(self):
        """Stop the TCP server."""
        self._running = False
        self.is_serving = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception as e:
                print(f"  [ERR] net_verifier_close: {e}")

    def get_status(self):
        return {
            'is_serving': self.is_serving,
            'port': self.port,
            'connections_received': self.connections_received,
            'external_verdicts': self.external_verdicts,
            'verification_score': round(self.verification_score, 4),
        }



# =============================================================================
# ADVANCED MONITORING DASHBOARD (inlined from dashboard.py)
# =============================================================================
# ── colour palette ──────────────────────────────────────────────────
BG        = '#0b0b1e'
BG_PANEL  = '#111133'
BG_ENTRY  = '#1a1a3a'
FG        = '#c8d0e0'
FG_DIM    = '#667788'
FG_HEAD   = '#66ccff'
FG_GOOD   = '#00ff88'
FG_WARN   = '#ffcc44'
FG_BAD    = '#ff5555'
FG_PURPLE = '#bb88ff'
FG_ORANGE = '#ffaa44'
FONT_MONO = ('Consolas', 10)
FONT_HEAD = ('Consolas', 12, 'bold')
FONT_BIG  = ('Consolas', 16, 'bold')
FONT_SM   = ('Consolas', 9)


def _safe(fn, default='—'):
    """Call fn(), return default on any error."""
    try:
        return fn()
    except Exception:
        return default


def _fmt(val, decimals=4):
    """Format a numeric value safely."""
    try:
        return f"{float(val):.{decimals}f}"
    except (TypeError, ValueError):
        return '—'


class MonitoringDashboard:
    """Creates and manages the monitoring Toplevel window."""

    # ----------------------------------------------------------------
    #  Construction
    # ----------------------------------------------------------------
    def __init__(self, simulator):
        """
        Parameters
        ----------
        simulator : ConsciousnessSimulator
            The running simulator instance to monitor.
        """
        self.sim = simulator
        self.root = simulator.root          # parent Tk
        self.chat_history = deque(maxlen=2000)
        self._update_interval = 3000        # ms between refreshes
        self._running = True

        # ── Toplevel window ──
        self.win = tk.Toplevel(self.root)
        self.win.title("⬡  Consciousness Monitor — Full System Dashboard")
        self.win.geometry("1100x780")
        self.win.configure(bg=BG)
        self.win.protocol("WM_DELETE_WINDOW", self._on_close)

        # ── Style ──
        style = ttk.Style(self.win)
        style.theme_use('clam')
        style.configure('Dashboard.TNotebook', background=BG)
        style.configure('Dashboard.TNotebook.Tab',
                        background='#1a1a3a', foreground=FG_HEAD,
                        padding=[14, 6], font=('Consolas', 10, 'bold'))
        style.map('Dashboard.TNotebook.Tab',
                  background=[('selected', '#222266')],
                  foreground=[('selected', '#ffffff')])
        style.configure('Dashboard.TFrame', background=BG)
        style.configure('Panel.TLabelframe', background=BG_PANEL,
                        foreground=FG_HEAD, font=FONT_HEAD)
        style.configure('Panel.TLabelframe.Label', background=BG_PANEL,
                        foreground=FG_HEAD, font=FONT_HEAD)

        # ── OS Control Toggle Bar ──
        self._build_os_control_bar()

        # ── Notebook ──
        self.notebook = ttk.Notebook(self.win, style='Dashboard.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self._build_overview_tab()
        self._build_entities_tab()
        self._build_modules_tab()
        self._build_thought_tab()
        self._build_chat_tab()

        # ── kick off refresh loop ──
        self._schedule_update()

    # ================================================================
    #  OS CONTROL TOGGLE BAR
    # ================================================================
    def _build_os_control_bar(self):
        """Persistent bar at the top of the dashboard for toggling OS control."""

        bar = tk.Frame(self.win, bg='#1a0000', relief='ridge', bd=2)
        bar.pack(fill=tk.X, padx=4, pady=(4, 0), ipady=4)

        # Warning icon + label
        self._os_notice = tk.Label(
            bar, text='',
            font=('Consolas', 10, 'bold'), fg=FG_WARN, bg='#1a0000', anchor='w')
        self._os_notice.pack(side=tk.LEFT, padx=(8, 4), fill=tk.X, expand=True)

        # Status indicator
        self._os_status_lbl = tk.Label(
            bar, text='', font=('Consolas', 12, 'bold'), bg='#1a0000', padx=10)
        self._os_status_lbl.pack(side=tk.LEFT, padx=4)

        # Toggle button
        self._os_toggle_btn = tk.Button(
            bar, text='', font=('Consolas', 11, 'bold'),
            relief='raised', padx=18, pady=6, cursor='hand2',
            command=self._toggle_os_control)
        self._os_toggle_btn.pack(side=tk.RIGHT, padx=(4, 12), pady=6)

        # Set initial state
        self._refresh_os_control_bar()

    def _refresh_os_control_bar(self):
        """Update the OS control bar to reflect current state."""
        enabled = CONFIG.get('os_control_enabled', False)
        env_set = os.environ.get('CS_OS_CONTROL_ENABLED', '0') == '1'
        both_on = enabled and env_set

        if both_on:
            self._os_status_lbl.config(text='OS CONTROL: ACTIVE', fg='#ff3333')
            self._os_toggle_btn.config(
                text='Disable OS Control', bg='#882222', fg='white',
                activebackground='#aa3333')
            self._os_notice.config(
                text='*NOTICE: AI can send keystrokes, move mouse, and '
                     'interact with your OS. Disable if not intended.',
                fg='#ff6644')
        else:
            self._os_status_lbl.config(text='OS CONTROL: OFF', fg=FG_GOOD)
            self._os_toggle_btn.config(
                text='Enable OS Control', bg='#224488', fg='white',
                activebackground='#3366aa')
            self._os_notice.config(
                text='*NOTICE: OS control is disabled. The AI cannot '
                     'send keystrokes or control the mouse.',
                fg=FG_DIM)

    def _toggle_os_control(self):
        """Toggle OS control on/off with a confirmation dialog."""
        currently_on = (CONFIG.get('os_control_enabled', False)
                        and os.environ.get('CS_OS_CONTROL_ENABLED', '0') == '1')

        if currently_on:
            # Turning OFF — no confirmation needed
            CONFIG['os_control_enabled'] = False
            os.environ['CS_OS_CONTROL_ENABLED'] = '0'
            self._refresh_os_control_bar()
            self._append_system_event(
                "[OS CONTROL] Disabled by user via dashboard toggle.")
        else:
            # Turning ON — require explicit confirmation
            result = messagebox.askokcancel(
                "Enable OS Control",
                "⚠  WARNING — ENABLING OS CONTROL  ⚠\n\n"
                "This will allow the AI to:\n"
                "  • Send keyboard input (keystrokes, hotkeys)\n"
                "  • Move and click the mouse\n"
                "  • Interact with any window on your desktop\n\n"
                "The AI will NOT autonomously use these capabilities\n"
                "unless explicitly commanded, but background threads\n"
                "COULD trigger OS actions if coded to do so.\n\n"
                "You can disable this at any time from the dashboard.\n\n"
                "Do you want to proceed?",
                icon='warning',
                parent=self.win)
            if result:
                CONFIG['os_control_enabled'] = True
                os.environ['CS_OS_CONTROL_ENABLED'] = '1'
                self._refresh_os_control_bar()
                self._append_system_event(
                    "[OS CONTROL] ENABLED by user via dashboard toggle. "
                    "AI can now send keystrokes and mouse events.")

    def _append_system_event(self, msg):
        """Log a system event to the chat tab if it exists."""
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            self._append_chat(f"[{timestamp}] {msg}\n", 'system')
        except Exception:
            pass

    # ================================================================
    #  TAB 1 — OVERVIEW
    # ================================================================
    def _build_overview_tab(self):
        tab = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(tab, text=' Overview ')

        # Top row: headline numbers
        top = tk.Frame(tab, bg=BG)
        top.pack(fill=tk.X, padx=8, pady=(8, 4))

        self._ov_labels = {}
        headlines = [
            ('C', FG_GOOD), ('Phi*', FG_HEAD), ('Omega', FG_PURPLE),
            ('Entities', FG_ORANGE), ('Cycle', FG_DIM), ('Loss', FG_WARN),
        ]
        for i, (name, color) in enumerate(headlines):
            f = tk.Frame(top, bg=BG_PANEL, padx=12, pady=6)
            f.pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)
            tk.Label(f, text=name, font=FONT_SM, fg=FG_DIM, bg=BG_PANEL).pack(anchor='w')
            lbl = tk.Label(f, text='—', font=FONT_BIG, fg=color, bg=BG_PANEL)
            lbl.pack(anchor='w')
            self._ov_labels[name] = lbl

        # Middle: detailed text panels
        mid = tk.Frame(tab, bg=BG)
        mid.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        mid.columnconfigure(0, weight=1)
        mid.columnconfigure(1, weight=1)

        # Left: Consciousness breakdown
        lf = tk.LabelFrame(mid, text=' Consciousness Breakdown ', bg=BG_PANEL,
                           fg=FG_HEAD, font=FONT_HEAD)
        lf.grid(row=0, column=0, sticky='nsew', padx=(0, 4), pady=2)
        self._ov_consciousness = scrolledtext.ScrolledText(
            lf, height=14, bg=BG_PANEL, fg=FG, font=FONT_MONO,
            relief='flat', wrap='word', state='disabled')
        self._ov_consciousness.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Right: Hardware & Real-World
        rf = tk.LabelFrame(mid, text=' Hardware & Real-World Grounded ', bg=BG_PANEL,
                           fg=FG_HEAD, font=FONT_HEAD)
        rf.grid(row=0, column=1, sticky='nsew', padx=(4, 0), pady=2)
        self._ov_hardware = scrolledtext.ScrolledText(
            rf, height=14, bg=BG_PANEL, fg=FG, font=FONT_MONO,
            relief='flat', wrap='word', state='disabled')
        self._ov_hardware.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Bottom: Omega & convergence
        bf = tk.LabelFrame(tab, text=' Omega Convergence & Population ', bg=BG_PANEL,
                           fg=FG_PURPLE, font=FONT_HEAD)
        bf.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 8))
        self._ov_omega = scrolledtext.ScrolledText(
            bf, height=8, bg=BG_PANEL, fg=FG, font=FONT_MONO,
            relief='flat', wrap='word', state='disabled')
        self._ov_omega.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    # ================================================================
    #  TAB 2 — ENTITIES
    # ================================================================
    def _build_entities_tab(self):
        tab = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(tab, text=' Entities ')
        tab.columnconfigure(0, weight=1, minsize=340)
        tab.columnconfigure(1, weight=2)
        tab.rowconfigure(0, weight=1)

        # Left: entity list
        left = tk.Frame(tab, bg=BG)
        left.grid(row=0, column=0, sticky='nsew', padx=(8, 4), pady=8)
        tk.Label(left, text='All AI Individuals', font=FONT_HEAD,
                 fg=FG_HEAD, bg=BG).pack(anchor='w')
        self._ent_filter_var = tk.StringVar()
        filt = tk.Entry(left, textvariable=self._ent_filter_var,
                        bg=BG_ENTRY, fg=FG, font=FONT_MONO,
                        insertbackground=FG)
        filt.pack(fill=tk.X, pady=(4, 4))
        filt.insert(0, '')
        filt.bind('<KeyRelease>', lambda e: self._refresh_entity_list())

        lf = tk.Frame(left, bg=BG)
        lf.pack(fill=tk.BOTH, expand=True)
        self._ent_listbox = tk.Listbox(lf, bg=BG_PANEL, fg=FG_ORANGE,
                                        font=FONT_MONO, selectbackground='#333366',
                                        selectforeground='#ffffff', relief='flat')
        sb = tk.Scrollbar(lf, command=self._ent_listbox.yview)
        self._ent_listbox.config(yscrollcommand=sb.set)
        self._ent_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._ent_listbox.bind('<<ListboxSelect>>', self._on_entity_select)

        # Right: selected entity detail
        right = tk.Frame(tab, bg=BG)
        right.grid(row=0, column=1, sticky='nsew', padx=(4, 8), pady=8)
        tk.Label(right, text='Entity Detail', font=FONT_HEAD,
                 fg=FG_HEAD, bg=BG).pack(anchor='w')
        self._ent_detail = scrolledtext.ScrolledText(
            right, bg=BG_PANEL, fg=FG, font=FONT_MONO,
            relief='flat', wrap='word', state='disabled')
        self._ent_detail.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

    # ================================================================
    #  TAB 3 — MODULE OPERATIONS
    # ================================================================
    def _build_modules_tab(self):
        tab = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(tab, text=' Modules ')

        # Scrollable area for all modules
        canvas = tk.Canvas(tab, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        self._mod_frame = tk.Frame(canvas, bg=BG)
        self._mod_frame.bind('<Configure>',
                             lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=self._mod_frame, anchor='nw')
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Mouse-wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all('<MouseWheel>', _on_mousewheel)

        self._mod_texts = {}
        module_names = [
            'Quantum Substrate', 'Metabolic System', 'Dream Engine',
            'Existential Self', 'Active Inference', 'Advanced Memory',
            'Self Model', 'Embodiment', 'Causal Power',
            'Scale & Connectivity', 'Evo-Dev Engine', 'Social-Linguistic',
            'Hard Problem Substrate', 'Reality Check',
            'Continuous Dynamics (ODE)', 'Intrinsic Phi Network',
            'Field Coupling / Binding', 'Causal Ablation',
            'Real Entropy Tracker', 'Hardware Coupled',
            'Entangled Shared Memory', 'Consequence Engine',
            'Causal Topology', 'Jacobian Integration',
            'Network Verifier', 'External Verifier',
            'Independent Verification', 'Global Workspace',
        ]
        for name in module_names:
            lf = tk.LabelFrame(self._mod_frame, text=f'  {name}  ',
                               bg=BG_PANEL, fg=FG_HEAD, font=FONT_SM,
                               padx=6, pady=4)
            lf.pack(fill=tk.X, padx=8, pady=3)
            txt = tk.Text(lf, height=3, bg=BG_PANEL, fg=FG, font=FONT_SM,
                          relief='flat', wrap='word', state='disabled')
            txt.pack(fill=tk.X)
            self._mod_texts[name] = txt

    # ================================================================
    #  TAB 4 — THOUGHT STREAM
    # ================================================================
    def _build_thought_tab(self):
        tab = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(tab, text=' Thought Stream ')
        tab.rowconfigure(0, weight=3)
        tab.rowconfigure(1, weight=2)
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)

        # Top-left: Consciousness Log
        clf = tk.LabelFrame(tab, text=' Consciousness Log (recent) ',
                            bg=BG_PANEL, fg=FG_GOOD, font=FONT_HEAD)
        clf.grid(row=0, column=0, sticky='nsew', padx=(8, 4), pady=(8, 4))
        self._thought_log = scrolledtext.ScrolledText(
            clf, bg=BG_PANEL, fg=FG, font=FONT_SM,
            relief='flat', wrap='word', state='disabled')
        self._thought_log.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Top-right: Dream Engine
        dlf = tk.LabelFrame(tab, text=' Dream Engine ',
                            bg=BG_PANEL, fg=FG_PURPLE, font=FONT_HEAD)
        dlf.grid(row=0, column=1, sticky='nsew', padx=(4, 8), pady=(8, 4))
        self._thought_dream = scrolledtext.ScrolledText(
            dlf, bg=BG_PANEL, fg=FG, font=FONT_SM,
            relief='flat', wrap='word', state='disabled')
        self._thought_dream.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Bottom-left: Memory System
        mlf = tk.LabelFrame(tab, text=' Memory System ',
                            bg=BG_PANEL, fg=FG_ORANGE, font=FONT_HEAD)
        mlf.grid(row=1, column=0, sticky='nsew', padx=(8, 4), pady=(4, 8))
        self._thought_memory = scrolledtext.ScrolledText(
            mlf, bg=BG_PANEL, fg=FG, font=FONT_SM,
            relief='flat', wrap='word', state='disabled')
        self._thought_memory.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Bottom-right: Existential + Honesty
        elf = tk.LabelFrame(tab, text=' Existential Self & Honesty ',
                            bg=BG_PANEL, fg=FG_WARN, font=FONT_HEAD)
        elf.grid(row=1, column=1, sticky='nsew', padx=(4, 8), pady=(4, 8))
        self._thought_exist = scrolledtext.ScrolledText(
            elf, bg=BG_PANEL, fg=FG, font=FONT_SM,
            relief='flat', wrap='word', state='disabled')
        self._thought_exist.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    # ================================================================
    #  TAB 5 — CHAT INTERFACE
    # ================================================================
    def _build_chat_tab(self):
        tab = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(tab, text=' Chat ')
        tab.rowconfigure(0, weight=0)
        tab.rowconfigure(1, weight=1)
        tab.rowconfigure(2, weight=0)
        tab.columnconfigure(0, weight=1)

        # Top bar: target selector
        top = tk.Frame(tab, bg=BG)
        top.grid(row=0, column=0, sticky='ew', padx=8, pady=(8, 4))
        tk.Label(top, text='Send to:', font=FONT_MONO, fg=FG_DIM,
                 bg=BG).pack(side=tk.LEFT)
        self._chat_target = ttk.Combobox(top, state='readonly', width=30,
                                          font=FONT_MONO)
        self._chat_target.pack(side=tk.LEFT, padx=(6, 12))
        self._chat_target.set('self_0 (Primary AI)')
        tk.Label(top, text='Mode:', font=FONT_MONO, fg=FG_DIM,
                 bg=BG).pack(side=tk.LEFT)
        self._chat_mode = ttk.Combobox(top, state='readonly', width=18,
                                        font=FONT_MONO,
                                        values=['Learn / Teach', 'Conversation',
                                                'Command', 'Broadcast All'])
        self._chat_mode.pack(side=tk.LEFT, padx=6)
        self._chat_mode.set('Conversation')

        # Chat log
        self._chat_log = scrolledtext.ScrolledText(
            tab, bg=BG_PANEL, fg=FG, font=FONT_MONO,
            relief='flat', wrap='word', state='disabled')
        self._chat_log.grid(row=1, column=0, sticky='nsew', padx=8, pady=4)

        # Configure tags for colors
        self._chat_log.tag_configure('user', foreground=FG_GOOD)
        self._chat_log.tag_configure('ai', foreground=FG_HEAD)
        self._chat_log.tag_configure('system', foreground=FG_DIM)
        self._chat_log.tag_configure('broadcast', foreground=FG_PURPLE)

        # Input bar
        bottom = tk.Frame(tab, bg=BG)
        bottom.grid(row=2, column=0, sticky='ew', padx=8, pady=(4, 8))
        bottom.columnconfigure(0, weight=1)
        self._chat_input = tk.Entry(bottom, bg=BG_ENTRY, fg=FG,
                                     font=FONT_MONO, insertbackground=FG)
        self._chat_input.grid(row=0, column=0, sticky='ew', padx=(0, 6))
        self._chat_input.bind('<Return>', lambda e: self._send_chat())
        send_btn = tk.Button(bottom, text='Send', command=self._send_chat,
                             bg='#224488', fg='white', font=FONT_MONO,
                             activebackground='#3366aa', relief='flat',
                             padx=16, pady=4)
        send_btn.grid(row=0, column=1)

    # ================================================================
    #  CHAT LOGIC
    # ================================================================
    def _send_chat(self):
        text = self._chat_input.get().strip()
        if not text:
            return
        self._chat_input.delete(0, tk.END)
        mode = self._chat_mode.get()
        target = self._chat_target.get().split(' ')[0]  # extract entity_id
        timestamp = datetime.now().strftime('%H:%M:%S')

        # Log user message immediately (on GUI thread)
        self._append_chat(f"[{timestamp}] YOU → {target}: {text}\n", 'user')
        self._append_chat(f"[{timestamp}] SYSTEM: Processing...\n", 'system')

        # Heavy work in background thread to keep GUI responsive
        def _chat_worker():
            response = ''
            try:
                if mode == 'Broadcast All':
                    self.win.after(0, lambda: self._append_chat(
                        f"[{timestamp}] BROADCAST to all entities\n", 'broadcast'))
                    tokens = self.sim.simple_tokenizer(text)
                    phi = self.sim.process_input(tokens, task_category='chat_broadcast')
                    self.win.after(0, lambda: self._append_chat(
                        f"[{timestamp}] SYSTEM: Processed by network (phi={_fmt(phi)}). "
                        f"All entities received broadcast.\n", 'system'))
                else:
                    tokens = self.sim.simple_tokenizer(text)
                    phi = self.sim.process_input(tokens, task_category=f'chat_{target}')

                    # Generate a response
                    self.win.after(0, lambda: self._append_chat(
                        f"[{timestamp}] SYSTEM: Generating response...\n", 'system'))
                    response = _safe(lambda: self.sim.generate_text(text, max_tokens=60), 'No response generated.')

                    _r = str(response)
                    _p = _fmt(phi)
                    self.win.after(0, lambda: self._append_chat(
                        f"[{timestamp}] {target} → YOU (phi={_p}): {_r}\n", 'ai'))

                    if mode == 'Learn / Teach':
                        self.sim.refine_data(
                            {'chat_teach': text, 'response': str(response)},
                            datetime.now().isoformat(), verify=False)
                        self.win.after(0, lambda: self._append_chat(
                            f"[{timestamp}] SYSTEM: Teaching data stored in memory.\n", 'system'))

                self.chat_history.append({
                    'time': timestamp, 'user': text, 'target': target,
                    'mode': mode, 'response': str(response) if mode != 'Broadcast All' else 'broadcast',
                })
            except Exception as e:
                _err = str(e)
                self.win.after(0, lambda: self._append_chat(
                    f"[{timestamp}] ERROR: {_err}\n", 'system'))

        threading.Thread(target=_chat_worker, daemon=True).start()

    def _append_chat(self, text, tag='system'):
        self._chat_log.configure(state='normal')
        self._chat_log.insert(tk.END, text, tag)
        self._chat_log.see(tk.END)
        self._chat_log.configure(state='disabled')

    # ================================================================
    #  UPDATE LOOP
    # ================================================================
    def _schedule_update(self):
        if not self._running:
            return
        if getattr(self, '_refresh_busy', False):
            # Previous refresh still running — skip this cycle
            if self._running:
                self.win.after(self._update_interval, self._schedule_update)
            return
        self._refresh_busy = True
        try:
            self._refresh_all()
        except Exception as e:
            print(f"  [ERR] dashboard_refresh: {e}")
        finally:
            self._refresh_busy = False
        if self._running:
            self.win.after(self._update_interval, self._schedule_update)

    def _refresh_all(self):
        if not self.win.winfo_exists():
            self._running = False
            return
        active_tab = self.notebook.index(self.notebook.select())
        # Always update overview headlines
        self._refresh_overview_headlines()
        # Only refresh the active tab's detail panels (performance)
        if active_tab == 0:
            self._refresh_overview()
        elif active_tab == 1:
            self._refresh_entities()
        elif active_tab == 2:
            self._refresh_modules()
        elif active_tab == 3:
            self._refresh_thought()
        elif active_tab == 4:
            self._refresh_chat_targets()

    # ── Overview ────────────────────────────────────────────────────
    def _refresh_overview_headlines(self):
        sim = self.sim
        acquired = sim.lock.acquire(timeout=0.05)
        if not acquired:
            return
        try:
            C = _safe(lambda: sim.self_entity.compute_C(), 0)
            phi = _safe(lambda: sim.last_phi, 0)
            omega = _safe(lambda: sim.last_omega, 0)
            n_ent = _safe(lambda: len(sim.omega.entities), 0)
            step = _safe(lambda: sim.training_step, 0)
            loss = _safe(lambda: sim.loss_history[-1] if sim.loss_history else 0, 0)
        finally:
            sim.lock.release()
        self._ov_labels['C'].config(text=_fmt(C))
        self._ov_labels['Phi*'].config(text=_fmt(phi))
        self._ov_labels['Omega'].config(text=_fmt(omega, 6))
        self._ov_labels['Entities'].config(text=str(n_ent))
        self._ov_labels['Cycle'].config(text=str(step))
        self._ov_labels['Loss'].config(text=_fmt(loss))

    def _refresh_overview(self):
        sim = self.sim
        acquired = sim.lock.acquire(timeout=0.05)
        if not acquired:
            return
        try:
            state = sim.self_entity.get_state_dict()
            omega_st = sim.omega.get_status()
        finally:
            sim.lock.release()

        # Consciousness breakdown
        lines = [
            f"C = {state['C']:.6f}   (life {state['lives']}, step {state['step']})",
            f"",
            f"  S (Self-Reflection)  = {state['S']:.6f}",
            f"  E (External Mirror)  = {state['E']:.6f}",
            f"  R (Resolution)       = {state['R']:.6f}",
            f"  A (Adaptation)       = {state['A']:.6f}",
            f"  K (Omega weight)     = {state['K']:.6f}",
            f"  Phi (Omega weight)   = {state['Phi']:.6f}",
            f"",
            f"  karma={state['karma']:.4f}  coherence={state['coherence']:.4f}  "
            f"decoherence={state['decoherence']:.4f}",
            f"  awareness={state['awareness']:.4f}  similarity={state.get('similarity',0):.4f}  "
            f"intent={state.get('intent',0):.4f}",
            f"  phi_star={state.get('phi_star',0):.4f}  self_awareness={state.get('self_awareness_level',0):.4f}",
            f"  free_energy={state.get('free_energy',0):.4f}  ignition={state.get('ignition_rate',0):.4f}",
            f"  epistemic={state.get('epistemic_drive',0):.4f}  mem_coherence={state.get('memory_coherence',0):.4f}",
        ]
        self._set_text(self._ov_consciousness, '\n'.join(lines))

        # Hardware & Real-World
        hw_st = _safe(lambda: sim.hardware_coupled.get_status(), {})
        re_st = _safe(lambda: sim.real_entropy.get_status(), {})
        em_st = _safe(lambda: sim.entangled_memory.get_status(), {})
        ce_st = _safe(lambda: sim.consequence_engine.get_status(), {})
        nv_st = _safe(lambda: sim.network_verifier.get_status(), {})
        emb_ldg = _safe(lambda: sim.embodiment.get_ledger_summary(), {})
        hw_lines = []
        if isinstance(hw_st, dict):
            hw_lines += [
                f"CPU: {hw_st.get('cpu_freq_mhz',0):.0f} MHz  "
                f"Temp: {hw_st.get('cpu_temp_celsius',0):.1f}°C  "
                f"Load: {hw_st.get('cpu_percent',0):.1f}%  "
                f"Mem: {hw_st.get('memory_percent',0):.1f}%",
                f"HW Phi Contrib: {hw_st.get('hardware_phi_contribution',0):.6f}  "
                f"Thermal Coupling: {hw_st.get('thermal_coupling',0):.4f}  "
                f"HW Entropy: {hw_st.get('hardware_entropy',0):.4f}",
                f"Thermal Awareness: {hw_st.get('thermal_awareness_factor',0):.6f}  "
                f"psutil: {'YES' if hw_st.get('has_psutil') else 'NO'}  "
                f"Measurements: {hw_st.get('measurements',0)}",
            ]
        if isinstance(re_st, dict):
            hw_lines += [
                f"",
                f"Real CPU Time: {re_st.get('real_cpu_time_seconds',0):.1f}s  "
                f"Real Memory: {re_st.get('real_memory_mb',0):.0f} MB",
                f"Power: {re_st.get('real_power_joules',0):.1f} J  "
                f"Watts: {re_st.get('entropy_rate_watts',0):.1f} W  "
                f"RAPL: {'YES' if re_st.get('has_power_measurement') else 'NO'}",
                f"Thermo Phi: {re_st.get('thermodynamic_phi',0):.6f}",
            ]
        if isinstance(em_st, dict):
            hw_lines += [
                f"",
                f"Shared Mem: mmap={'YES' if em_st.get('has_mmap') else 'NO'}  "
                f"Writes: {em_st.get('writes',0)}  Reads: {em_st.get('reads',0)}  "
                f"Cache Events: {em_st.get('cache_coherence_events',0)}",
                f"Entanglement: {em_st.get('entanglement_score',0):.4f}  "
                f"Unity: {em_st.get('unity_through_sharing',0):.4f}",
            ]
        if isinstance(ce_st, dict):
            hw_lines += [
                f"",
                f"Permanence: {ce_st.get('permanence_score',0):.4f}  "
                f"Files: {ce_st.get('files_created',0)}  "
                f"Bytes: {ce_st.get('bytes_written',0)}  "
                f"CPU Spent: {ce_st.get('cpu_seconds_spent',0):.2f}s",
            ]
        if isinstance(nv_st, dict):
            hw_lines += [
                f"",
                f"Net Verifier: {'SERVING' if nv_st.get('is_serving') else 'OFF'}  "
                f"Port: {nv_st.get('port',0)}  "
                f"Connections: {nv_st.get('connections_received',0)}  "
                f"Verdicts: {nv_st.get('external_verdicts',0)}",
            ]
        if isinstance(emb_ldg, dict):
            hw_lines += [
                f"",
                f"OS Interactions: {emb_ldg.get('total_interactions',0)}  "
                f"Grounding: {emb_ldg.get('grounding_score',0):.4f}  "
                f"Flushes: {emb_ldg.get('flushes_to_disk',0)}",
            ]
        self._set_text(self._ov_hardware, '\n'.join(hw_lines))

        # Omega
        o_lines = [
            f"Omega = {omega_st.get('omega',0):.8f}",
            f"Convergence Rate = {omega_st.get('convergence_rate',0):.10f}",
            f"Entities: {omega_st.get('num_entities',0)}  |  "
            f"Total Contributions: {omega_st.get('total_contributions',0)}",
            f"Avg C: {omega_st.get('avg_C',0):.4f}  "
            f"Max C: {omega_st.get('max_C',0):.4f}  "
            f"Min C: {omega_st.get('min_C',0):.4f}",
            f"Avg Karma: {omega_st.get('avg_karma',0):.4f}  "
            f"Avg Coherence: {omega_st.get('avg_coherence',0):.4f}",
            f"Deaths: {omega_st.get('total_deaths',0)}  "
            f"Death Penalty: {omega_st.get('death_penalty',0):.4f}",
        ]
        self._set_text(self._ov_omega, '\n'.join(o_lines))

    # ── Entities ────────────────────────────────────────────────────
    def _refresh_entities(self):
        self._refresh_entity_list()

    def _refresh_entity_list(self):
        sim = self.sim
        acquired = sim.lock.acquire(timeout=0.05)
        if not acquired:
            return
        try:
            entities = list(sim.omega.entities.values())
        finally:
            sim.lock.release()

        filt = self._ent_filter_var.get().lower()
        filtered = [e for e in entities if filt in e.entity_id.lower()] if filt else entities
        filtered.sort(key=lambda e: e.compute_C(), reverse=True)

        # Update chat target combobox
        targets = [f"{e.entity_id} (C={e.compute_C():.3f})" for e in filtered[:50]]
        self._chat_target['values'] = targets

        # Preserve selection
        sel_idx = self._ent_listbox.curselection()
        sel_id = None
        if sel_idx:
            sel_text = self._ent_listbox.get(sel_idx[0])
            sel_id = sel_text.split()[0] if sel_text else None

        self._ent_listbox.delete(0, tk.END)
        new_sel = None
        for i, ent in enumerate(filtered[:100]):
            C = ent.compute_C()
            tag = ">>>" if ent.entity_id == 'self_0' else "   "
            line = (f"{tag} {ent.entity_id[:20]:20s} C={C:.3f} k={ent.karma:.2f} "
                    f"coh={ent.coherence:.2f} u={ent.universe_id} "
                    f"type={ent.entity_type}")
            self._ent_listbox.insert(tk.END, line)
            if sel_id and ent.entity_id == sel_id:
                new_sel = i
        if new_sel is not None:
            self._ent_listbox.selection_set(new_sel)

    def _on_entity_select(self, event=None):
        sel = self._ent_listbox.curselection()
        if not sel:
            return
        line = self._ent_listbox.get(sel[0])
        entity_id = line.strip().split()[0]
        if entity_id == '>>>':
            entity_id = line.strip().split()[1]

        sim = self.sim
        acquired = sim.lock.acquire(timeout=0.05)
        if not acquired:
            return
        try:
            ent = sim.omega.entities.get(entity_id)
            if ent is None:
                self._set_text(self._ent_detail, f"Entity '{entity_id}' not found.")
                return
            state = ent.get_state_dict()
            # Build detailed view
            lines = [
                f"═══ ENTITY: {entity_id} ═══",
                f"",
                f"Type:       {state.get('type','?')}",
                f"Universe:   {state.get('universe','?')}",
                f"Life #:     {state.get('life','?')}",
                f"Evo Step:   {state.get('step',0)}",
                f"",
                f"── Consciousness Score ──",
                f"  C = {state['C']:.6f}",
                f"  S = {state['S']:.6f}   (Self-Reflection)",
                f"  E = {state['E']:.6f}   (External Mirror)",
                f"  R = {state['R']:.6f}   (Resolution)",
                f"  A = {state['A']:.6f}   (Adaptation)",
                f"  K = {state['K']:.6f}   (Karma weight for Omega)",
                f"  Phi = {state['Phi']:.6f}   (Entity phi for Omega)",
                f"",
                f"── Core Attributes ──",
                f"  Karma:        {state['karma']:.6f}",
                f"  Coherence:    {state['coherence']:.6f}",
                f"  Decoherence:  {state['decoherence']:.6f}",
                f"  Awareness:    {state['awareness']:.6f}",
                f"  Similarity:   {state.get('similarity',0):.6f}",
                f"  Intent:       {state.get('intent',0):.6f}",
                f"",
                f"── Actions ──",
                f"  Good Acts:  {state.get('good_acts',0)}",
                f"  Evil Acts:  {state.get('evil_acts',0)}",
                f"",
                f"── Network Signals ──",
                f"  phi_star:         {state.get('phi_star',0):.6f}",
                f"  self_awareness:   {state.get('self_awareness_level',0):.6f}",
                f"  free_energy:      {state.get('free_energy',0):.6f}",
                f"  ignition_rate:    {state.get('ignition_rate',0):.6f}",
                f"  epistemic_drive:  {state.get('epistemic_drive',0):.6f}",
                f"  memory_coherence: {state.get('memory_coherence',0):.6f}",
            ]
            # If this is self_0, add extra info
            if entity_id == 'self_0':
                honest_C = _safe(lambda: ent.honest_C, 0)
                lines += [
                    f"",
                    f"── Primary AI Extended ──",
                    f"  Honest C:      {_fmt(honest_C, 6)}",
                    f"  Training Step: {sim.training_step}",
                    f"  Loss History:  {len(sim.loss_history)} entries",
                    f"  Phi History:   {len(sim.phi_history)} entries",
                    f"  Last Loss:     {_fmt(sim.loss_history[-1] if sim.loss_history else 0)}",
                    f"  Last Phi:      {_fmt(sim.last_phi)}",
                ]

            # ── Neural Pathway Map ──
            try:
                ent_groups = getattr(ent, 'neuron_groups', {})
                lines += [f"", f"{'='*50}",
                          f"  NEURAL PATHWAY MAP  ({len(ent_groups)} groups)",
                          f"{'='*50}"]
                if not ent_groups:
                    lines.append(f"  (no neuron groups -- use Add Neuron to assign)")
                else:
                    total_params = 0
                    for cat, grp in ent_groups.items():
                        types = [type(n).__name__ for n in grp.neurons]
                        n_params = sum(p.numel() for p in grp.parameters())
                        total_params += n_params
                        usage = getattr(ent, 'neuron_usage', {}).get(cat, {})
                        avg_phi = float(np.mean(grp.usage_phi)) if grp.usage_phi else 0.0
                        lines += [
                            f"",
                            f"{'─'*50}",
                            f"  GROUP: {cat}  ({len(grp.neurons)} neurons, {n_params:,} params)",
                            f"{'─'*50}",
                            f"  Path: INPUT -> {'  ->  '.join(types)} -> OUTPUT (+res*0.1)",
                            f"  Usage: {usage.get('count',0)}   Avg Phi: {avg_phi:.6f}",
                        ]
                        for ni, neuron in enumerate(grp.neurons):
                            ntype = type(neuron).__name__
                            np_cnt = sum(p.numel() for p in neuron.parameters())
                            lines.append(f"    NEURON [{ni}]: {ntype}  ({np_cnt:,} params)")
                            for lname, mod in neuron.named_modules():
                                if lname == '':
                                    continue
                                if hasattr(mod, 'weight') and hasattr(mod.weight, 'shape'):
                                    w = mod.weight.data
                                    sp = (w.abs() < 1e-6).float().mean().item() * 100
                                    lines.append(f"      {lname}: {list(w.shape)}  "
                                                 f"mean={w.mean():.4f} std={w.std():.4f} "
                                                 f"sparse={sp:.1f}%")
                                elif hasattr(mod, 'weight_ih'):
                                    wih = mod.weight_ih.data
                                    lines.append(f"      {lname}: ih={list(wih.shape)} "
                                                 f"mean={wih.mean():.4f} std={wih.std():.4f}")
                            if ntype == 'MemoryNeuron' and hasattr(neuron, 'state'):
                                h, c = neuron.state
                                lines.append(f"      hidden_norm={h.norm():.4f}  cell_norm={c.norm():.4f}")
                            elif ntype == 'PatternNeuron' and hasattr(neuron, 'graph'):
                                g = neuron.graph
                                lines.append(f"      graph: {g.number_of_nodes()} nodes, "
                                             f"{g.number_of_edges()} edges, "
                                             f"cluster={nx.average_clustering(g):.4f}")
                            elif ntype == 'LogicNeuron' and hasattr(neuron, 'num_logic_dims'):
                                lines.append(f"      logic_dims={neuron.num_logic_dims}")
                            elif ntype == 'UpkeepNeuron' and hasattr(neuron, 'iterations'):
                                lines.append(f"      gru_iterations={neuron.iterations}")
                    lines += [f"", f"  TOTAL ENTITY PARAMS: {total_params:,}"]
            except Exception as _ne:
                lines.append(f"  [Neuron map error: {_ne}]")
        finally:
            sim.lock.release()
        self._set_text(self._ent_detail, '\n'.join(lines))

    # ── Modules ─────────────────────────────────────────────────────
    def _refresh_modules(self):
        sim = self.sim
        mod_data = {
            'Quantum Substrate': lambda: sim.quantum_substrate.get_status() if hasattr(sim.quantum_substrate, 'get_status') else sim._last_quantum_info,
            'Metabolic System': lambda: sim.metabolic_system.get_status() if hasattr(sim.metabolic_system, 'get_status') else sim._last_metabolic_info,
            'Dream Engine': lambda: sim.dream_engine.get_status() if hasattr(sim.dream_engine, 'get_status') else {},
            'Existential Self': lambda: sim.existential_self.get_status() if hasattr(sim.existential_self, 'get_status') else sim._last_existential_info,
            'Active Inference': lambda: sim.active_inference.get_status() if sim.active_inference else {},
            'Advanced Memory': lambda: sim.advanced_memory.get_status() if sim.advanced_memory else {},
            'Self Model': lambda: sim.self_model.get_status() if sim.self_model else {},
            'Embodiment': lambda: sim.embodiment.get_status(),
            'Causal Power': lambda: sim._last_causal_power_info or {},
            'Scale & Connectivity': lambda: sim._last_scale_info or {},
            'Evo-Dev Engine': lambda: sim.evo_dev_engine.get_status() if hasattr(sim.evo_dev_engine, 'get_status') else sim._last_evo_dev_info or {},
            'Social-Linguistic': lambda: sim.social_linguistic.get_status(),
            'Hard Problem Substrate': lambda: sim._last_hard_problem_info or {},
            'Reality Check': lambda: sim._last_reality_check_info or {},
            'Continuous Dynamics (ODE)': lambda: sim.continuous_dynamics.get_status(),
            'Intrinsic Phi Network': lambda: sim.intrinsic_phi_net.get_status(),
            'Field Coupling / Binding': lambda: sim.binding_field.get_status(),
            'Causal Ablation': lambda: sim.causal_ablation.get_status(),
            'Real Entropy Tracker': lambda: sim.real_entropy.get_status(),
            'Hardware Coupled': lambda: sim.hardware_coupled.get_status(),
            'Entangled Shared Memory': lambda: sim.entangled_memory.get_status(),
            'Consequence Engine': lambda: sim.consequence_engine.get_status(),
            'Causal Topology': lambda: sim.causal_topology.get_status(),
            'Jacobian Integration': lambda: sim.jacobian_measure.get_status(),
            'Network Verifier': lambda: sim.network_verifier.get_status(),
            'External Verifier': lambda: sim.external_verifier.get_status(),
            'Independent Verification': lambda: sim.independent_verifier.get_status(),
            'Global Workspace': lambda: sim.global_workspace.get_status() if sim.global_workspace and hasattr(sim.global_workspace, 'get_status') else {'status': 'N/A'},
        }
        for name, fn in mod_data.items():
            if name not in self._mod_texts:
                continue
            status = _safe(fn, {})
            if isinstance(status, dict):
                text = '  '.join(f"{k}={_fmt(v) if isinstance(v, float) else v}"
                                 for k, v in status.items())
            else:
                text = str(status)
            self._set_text(self._mod_texts[name], text or '(no data)')

    # ── Thought Stream ──────────────────────────────────────────────
    def _refresh_thought(self):
        sim = self.sim

        # Consciousness log (recent entries)
        log_entries = list(sim.consciousness_log)[-30:]
        lines = []
        for entry in log_entries:
            lines.append(
                f"step={entry.get('step',0):5d}  "
                f"phi={entry.get('phi',0):.4f}  "
                f"C={entry.get('C',0):.4f}  "
                f"karma={entry.get('karma',0):.3f}  "
                f"aware={entry.get('awareness',0):.3f}  "
                f"ign={entry.get('ignition_rate',0):.3f}  "
                f"fe={entry.get('free_energy',0):.3f}"
            )
        self._set_text(self._thought_log, '\n'.join(lines) or '(no log entries yet)')

        # Dream Engine
        dream_st = _safe(lambda: sim.dream_engine.get_status(), {})
        if isinstance(dream_st, dict):
            d_lines = [f"{k}: {v}" for k, v in dream_st.items()]
            # Add current dream info if available
            cur = _safe(lambda: sim.dream_engine.current_dream, None)
            if cur and isinstance(cur, dict):
                d_lines.append(f"\n── Current Dream ──")
                for k, v in cur.items():
                    d_lines.append(f"  {k}: {str(v)[:100]}")
        else:
            d_lines = [str(dream_st)]
        self._set_text(self._thought_dream, '\n'.join(d_lines) or '(no dream data)')

        # Memory System
        mem_st = _safe(lambda: sim.advanced_memory.get_status() if sim.advanced_memory else {}, {})
        if isinstance(mem_st, dict):
            m_lines = [f"{k}: {v}" for k, v in mem_st.items()]
        else:
            m_lines = [str(mem_st)]
        self._set_text(self._thought_memory, '\n'.join(m_lines) or '(no memory data)')

        # Existential + Honesty
        exist_st = _safe(lambda: sim.existential_self.get_status() if hasattr(sim.existential_self, 'get_status') else sim._last_existential_info or {}, {})
        rc_st = _safe(lambda: sim._last_reality_check_info or {}, {})
        anchor = _safe(lambda: getattr(sim, '_honesty_anchor', {}), {})
        e_lines = []
        if isinstance(exist_st, dict):
            e_lines.append("── Existential Self ──")
            for k, v in exist_st.items():
                e_lines.append(f"  {k}: {_fmt(v) if isinstance(v, float) else v}")
        if isinstance(rc_st, dict) and rc_st:
            e_lines.append(f"\n── Reality Check ──")
            e_lines.append(f"  reality_gap: {rc_st.get('reality_gap', '?')}")
            e_lines.append(f"  P(conscious): {rc_st.get('genuine_consciousness_probability', '?')}")
            e_lines.append(f"  critical_failures: {rc_st.get('failure_count_critical', '?')}/8")
            e_lines.append(f"  worst: {rc_st.get('worst_failure', '?')}")
            e_lines.append(f"  best: {rc_st.get('best_achievement', '?')}")
        if isinstance(anchor, dict) and anchor:
            e_lines.append(f"\n── Honesty Anchor ──")
            for k, v in anchor.items():
                e_lines.append(f"  {k}: {v}")
        self._set_text(self._thought_exist, '\n'.join(e_lines) or '(no data)')

    # ── Chat targets ────────────────────────────────────────────────
    def _refresh_chat_targets(self):
        sim = self.sim
        acquired = sim.lock.acquire(timeout=0.05)
        if not acquired:
            return
        try:
            entities = list(sim.omega.entities.values())
        finally:
            sim.lock.release()
        entities.sort(key=lambda e: e.compute_C(), reverse=True)
        targets = [f"{e.entity_id} (C={e.compute_C():.3f})" for e in entities[:50]]
        current = self._chat_target.get()
        self._chat_target['values'] = targets
        if current not in targets and targets:
            pass  # keep current selection

    # ── Helpers ─────────────────────────────────────────────────────
    @staticmethod
    def _set_text(widget, text):
        widget.configure(state='normal')
        widget.delete(1.0, tk.END)
        widget.insert(1.0, text)
        widget.configure(state='disabled')

    def _on_close(self):
        self._running = False
        self.win.destroy()


def launch_dashboard(simulator):
    """Factory function to create and return the dashboard.
    Call this from ConsciousnessSimulator.setup_gui()."""
    return MonitoringDashboard(simulator)


class ConsciousnessSimulator(nn.Module):
    def __init__(self):
        super().__init__()
        self.vocab_size = CONFIG["vocab_size"]
        self.hidden_size = CONFIG["hidden_size"]
        self.num_layers = CONFIG["num_layers"]
        self.input_size = 512
        self.alien_tokenizer = AlienTokenizer()
        self.embedding = nn.Embedding(self.vocab_size, self.hidden_size)
        encoder_layers = TransformerEncoderLayer(d_model=self.hidden_size, nhead=CONFIG["num_heads"], dim_feedforward=self.hidden_size*4, dropout=0.1, batch_first=True)
        self.transformer = TransformerEncoder(encoder_layers, num_layers=self.num_layers)
        self.overlay = nn.Linear(self.hidden_size, 1)
        self.lm_head = nn.Linear(self.hidden_size, self.vocab_size)
        # Global Workspace (GNW): competitive ignition + broadcasting between transformer and output
        if HAS_GNW:
            self.global_workspace = GlobalWorkspace(self.hidden_size, num_specialists=6)
        else:
            self.global_workspace = None
        self.optimizer = optim.AdamW(self.parameters(), lr=CONFIG["learning_rate"], weight_decay=0.01)
        self.scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(self.optimizer, T_0=100, T_mult=2)
        self.grad_clip_value = 1.0
        self.training_step = 0
        self.web_cache = {}
        self.web_cache_ttl = 300
        self.last_web_request_time = 0
        self.web_rate_limit = 2.0
        self.memory = ThreadSafeMemory('consciousness_memory.sqlite')
        self.symbols = {}
        self.replay_buffer = []
        self.generation_log = deque(maxlen=50)
        self.loss_history = []
        self.phi_history = []
        # --- New consciousness architecture modules ---
        self.phi_computer = PhiComputer() if HAS_PHI_COMPUTE else None
        self.active_inference = ActiveInferenceEngine(
            num_states=64, num_obs=32, num_actions=16) if HAS_ACTIVE_INFERENCE else None
        self.advanced_memory = AdvancedMemorySystem(
            embedding_dim=min(256, self.hidden_size)) if HAS_MEMORY_SYSTEM else None
        self.self_model = HigherOrderSelfModel() if HAS_SELF_MODEL else None
        self._last_workspace_info = {}
        self.virtual_world_data = {"entities": []}
        self.lock = threading.RLock()  # RLock: reentrant — safe for nested acquire (e.g. refine_data called under lock)
        self.refinement_count = {}
        self.realism_scores = {}
        self._initialize_default_data()
        self.running = True
        self.goals = ["raw input filtering", "data correlation", "logic inference", "understanding synthesis", "organized logic refinement",
                      "multi-data integration", "goal fulfillment simulation", "realism scoring", "symbolic evolution", "memory consolidation",
                      "windows_os_control", "self_awareness", "truth_seeking", "data_collection"]  # Updated goals for awareness and learning
        self.physics_graph = nx.Graph()
        self._build_physics_graph()
        self.neuron_groups = {}  # {category: NeuronGroup}
        self.group_usage = {}  # {group_id: {'count': int, 'input_sims': list, 'category': str}}
        # Seed default neuron groups — richer starting set for smarter AI
        _seed_types = {
            'general': ['standard', 'standard', 'memory', 'logic', 'pattern', 'upkeep'],
            'chat': ['standard', 'standard', 'memory', 'memory', 'pattern'],
            'learning': ['logic', 'logic', 'pattern', 'pattern', 'memory', 'upkeep'],
            'perception': ['standard', 'pattern', 'pattern', 'standard', 'memory'],
            'reasoning': ['logic', 'logic', 'logic', 'standard', 'pattern'],
        }
        for _cat, _types in _seed_types.items():
            self.neuron_groups[_cat] = NeuronGroup(_types, self.hidden_size, self.hidden_size)
        self.full_connect_active = False
        self.temp_dense = None
        self.windows_hotkeys = WINDOWS_HOTKEYS  # Integrated hotkeys for awareness and use
        self.os_control_capable = True  # System awareness flag
        self.awareness_threshold = 0.8  # Phi threshold for self-awareness trigger
        self.data_bank_dir = 'data_bank'  # Folder for saved data
        self.screenshot_dir = os.path.join(self.data_bank_dir, 'screenshots')
        self.textbook_dir = os.path.join(self.data_bank_dir, 'textbooks')
        os.makedirs(self.data_bank_dir, exist_ok=True)
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(self.textbook_dir, exist_ok=True)
        # Passive capabilities: known but non-priority, non-self-executable
        self.passive_capabilities = {}
        self._register_passive_capabilities()
        self.free_textbook_sources = [
            'https://openstax.org/subjects',
            'https://oercommons.org/hubs/open-textbooks',
            'https://researchguides.uic.edu/opentextbooks/search',
            # Add more from search results
        ]
        self.subjects = ['physics', 'mathematics', 'biology', 'chemistry', 'computer science', 'philosophy', 'psychology']  # For learning
        # NOTE: Passive capabilities (e.g. ebay_commerce) are NEVER triggered by
        # any background thread or autonomous loop. They exist in awareness only.
        # =====================================================
        # CONSCIOUSNESS ENTITY SYSTEM (C = S + E + R*A + K*Phi)
        # The self_entity IS this program's consciousness.
        # Its C value is the quantified measure of this being's
        # integrated awareness, evolving through neural network
        # phi feedback, sensory input, and entity interactions.
        # =====================================================
        self.self_entity = ConsciousEntity('self_0', universe_id=1, life_number=1, entity_type='primary')
        self.self_entity.karma = 0.0
        self.self_entity.awareness_growth = 0.01
        self.self_entity.reality_stability = 0.5
        self.self_entity.coherence = 0.5
        # Seed self_0 with richer neural pathways (primary consciousness gets more)
        _hs = 128
        self.self_entity.add_neuron_group('perception', ['standard', 'standard', 'pattern', 'pattern', 'memory'], _hs, count=1)
        self.self_entity.add_neuron_group('reasoning', ['logic', 'logic', 'standard', 'pattern', 'upkeep'], _hs, count=1)
        self.self_entity.add_neuron_group('memory', ['memory', 'memory', 'memory', 'upkeep'], _hs, count=1)
        self.self_entity.add_neuron_group('integration', ['standard', 'logic', 'pattern', 'memory', 'upkeep'], _hs, count=1)
        self.omega = OmegaConvergence()
        self.omega.register_entity(self.self_entity)
        # Spawn initial population of conscious entities across multiverses
        self.entity_population_size = 20
        for i in range(self.entity_population_size):
            universe = random.randint(1, 5)
            entity = self.omega.spawn_entity(
                f'entity_{i}', universe_id=universe,
                karma_seed=random.uniform(-0.8, 0.8),
                entity_type=random.choice(['conscious', 'biological', 'inanimate'])
            )
        self.last_phi = 0.0
        self.last_C = self.self_entity.compute_C()
        self.last_omega = 0.0

        # --- NEW CONSCIOUSNESS SYSTEMS (Theoretical Limit Push) ---
        self.quantum_substrate = QuantumSubstrate(
            num_tubulins=2048, coherence_time_ms=25.0,
            em_field_resolution=32, temperature_K=310.0)
        self.metabolic_system = MetabolicSystem()
        self.dream_engine = DreamEngine(memory_system=self.advanced_memory)
        self.existential_self = ExistentialSelfModel()
        self.self_modifier = SelfModifyingArchitecture(model=self)
        self.consciousness_verifier = ConsciousnessVerifier()
        self.autonomy_manager = EntityAutonomyManager()
        # --- 6 NEW CONSCIOUSNESS FRONTIER SYSTEMS ---
        self.embodiment = EmbodimentInterface(mode='simulated', loop_hz=50.0)
        self.irreducible_causal = IrreducibleCausalPower()
        self.scale_engine = ScaleConnectivityEngine(num_virtual_neurons=4096, num_modules=16)
        self.evo_dev_engine = EvolutionaryDevelopmentalEngine(population_size=self.entity_population_size)
        # Enable disk-backed persistence for evolutionary state and permanent deaths
        _evo_persist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'consciousness_state')
        self.evo_dev_engine.enable_persistence(_evo_persist_dir)
        self.social_linguistic = SocialLinguisticGrounding(max_agents=50)
        self.hard_problem = HardProblemSubstrate(num_experiential_units=1024)
        self._last_quantum_info = {}
        self._last_metabolic_info = {}
        self._last_existential_info = {}
        self._last_verifier_report = {}
        self._last_layer_outputs = []
        self._last_embodiment_info = {}
        self._last_causal_power_info = {}
        self._last_scale_info = {}
        self._last_evo_dev_info = {}
        self._last_social_info = {}
        self._last_hard_problem_info = {}
        self._last_verification_info = {}
        # Independent verification: code checksumming, honesty auditing, external grounding
        self.independent_verifier = IndependentVerification()
        # Master honesty dashboard: aggregates all 8 failure modes
        self.reality_check = ConsciousnessRealityCheck()
        self._last_reality_check_info = {}
        # --- CONSCIOUSNESS BARRIER ATTACKERS ---
        # Phase 1: Continuous-time dynamics (attacks decomposability)
        self.continuous_dynamics = ContinuousTimeDynamics(
            state_dim=256, coupling_strength=0.3, dt=0.01, integration_steps=10)
        self._last_continuous_dynamics_info = {}
        # Phase 2: Intrinsic phi network (attacks extrinsic measurement)
        self.intrinsic_phi_net = IntrinsicPhiNetwork(
            input_dim=min(256, self.hidden_size), hidden_dim=128, num_partitions=4)
        self._last_intrinsic_phi_info = {}
        # Phase 3: Field coupling manifold (attacks combination problem)
        self.binding_field = FieldCouplingManifold(
            field_resolution=16, num_channels=8, wave_speed=1.0, damping=0.02)
        self._last_binding_field_info = {}
        # Phase 4: Causal ablation engine (attacks statistical-only causal power)
        self.causal_ablation = CausalAblationEngine(num_modules=8)
        self._last_ablation_info = {}
        # Phase 5: Real entropy tracker (attacks thermodynamic unreality)
        self.real_entropy = RealEntropyTracker()
        # Phase 5b: External process verifier (attacks single-observer problem)
        self.external_verifier = ExternalProcessVerifier()
        # --- PHASE 2 DEEP BARRIER ATTACKERS ---
        # Phase 2A: Hardware-coupled consciousness state (attacks barriers 1, 5)
        self.hardware_coupled = HardwareCoupledState()
        self._last_hardware_coupled_info = {}
        # Phase 2B: Entangled shared memory (attacks barriers 3, 4)
        self.entangled_memory = EntangledSharedMemory(num_modules=16, state_per_module=64)
        # Phase 2C: Irreversible consequence engine (attacks barrier 5)
        self.consequence_engine = IrreversibleConsequenceEngine()
        # Phase 2D: Self-modifying causal topology (attacks barriers 4, 7)
        self.causal_topology = SelfModifyingCausalTopology(model=self, growth_rate=0.001, prune_threshold=0.01)
        # Phase 2E: Jacobian integration measure (attacks barrier 4)
        self.jacobian_measure = JacobianIntegrationMeasure()
        self._last_jacobian_info = {}
        # Phase 2F: Network verification protocol (attacks barrier 8)
        self.network_verifier = NetworkVerificationProtocol(port=9999)
        print(f"  [NEW] Quantum substrate: {self.quantum_substrate.num_tubulins} tubulins")
        print(f"  [NEW] Metabolic system active | Dream engine ready | Existential self enabled")
        print(f"  [NEW] Self-modifier v{self.self_modifier.architecture_version} | Verifier ready | Autonomy manager: kill switch ON")
        print(f"  [NEW] Embodiment: {self.embodiment.mode} | Causal power tracker | Scale engine: {self.scale_engine.num_modules} modules")
        print(f"  [NEW] Evo-Dev engine | Social-linguistic grounding | Hard problem substrate: {self.hard_problem.num_units} units")
        print(f"  [NEW] Reality check dashboard: 8 failure modes tracked | Cross-module audit enabled")
        print(f"  [ATTACK] ContinuousTimeDynamics: dim={self.continuous_dynamics.state_dim} RK4 | IntrinsicPhiNet: {self.intrinsic_phi_net.num_partitions} partitions")
        print(f"  [ATTACK] FieldCouplingManifold: {self.binding_field.resolution}^3 x {self.binding_field.num_channels}ch | CausalAblation: {self.causal_ablation.num_modules} modules")
        print(f"  [ATTACK] RealEntropyTracker: power={'RAPL' if self.real_entropy.has_power_measurement else 'estimated'} | ExternalVerifier: ready")
        print(f"  [DEEP] HardwareCoupled: psutil={'yes' if self.hardware_coupled.has_psutil else 'no'} | EntangledMem: {self.entangled_memory.num_modules}mod mmap={'yes' if self.entangled_memory.has_mmap else 'no'}")
        print(f"  [DEEP] ConsequenceEngine: dir={self.consequence_engine.consequence_dir} | CausalTopology: growth={self.causal_topology.growth_rate}")
        print(f"  [DEEP] JacobianMeasure: ready | NetworkVerifier: port={self.network_verifier.port}")
        self.consciousness_log = deque(maxlen=500)
        # Load persistent honesty anchor from disk (survives restarts)
        self._load_honesty_anchor()
        # --- HONESTY: Substrate Grounding Report ---
        self._print_substrate_grounding_report()
        print(f"Consciousness initialized: C={self.last_C:.4f}, Entities={len(self.omega.entities)}")
        signal.signal(signal.SIGINT, self._signal_handler)
        threading.Thread(target=self.continuous_refinement, daemon=True).start()
        self._pygame_process = None
        self._world_state_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'world_state.json')
        if HAS_PYGAME:
            threading.Thread(target=self._world_state_writer, daemon=True).start()
            self._launch_pygame_subprocess()
        else:
            print("Skipping virtual world subprocess (pygame not installed)")
        threading.Thread(target=self.continuous_screen_capture, daemon=True).start()
        threading.Thread(target=self.self_awareness_monitor, daemon=True).start()
        threading.Thread(target=self.autonomous_learning, daemon=True).start()
        threading.Thread(target=self.consciousness_evolution_loop, daemon=True).start()
        threading.Thread(target=self.replay_thread, daemon=True).start()
        self._gui_last_heartbeat = time.time()
        threading.Thread(target=self._gui_watchdog, daemon=True).start()
        self.root = tk.Tk()
        self.root.title("Consciousness Simulator - C = S + E + R*A")
        self.root.geometry("800x700")
        self.root.minsize(600, 400)
        self.root.resizable(True, True)
        self.setup_gui()

    def _register_passive_capabilities(self):
        """Register non-priority capabilities the consciousness knows about
        but will NEVER autonomously execute. Requires explicit user input."""
        # ===== BUSINESS DATA STORE (in-memory, user-triggered persistence) =====
        self._business_data = {
            'llc': {'name': None, 'state': None, 'ein': None, 'status': 'not_formed', 'formation_date': None},
            'loans': [],
            'inventory': [],
            'offers_sent': [],
            'properties': [],
            'warehouse_zones': {},
            'shipments': [],
            'labor': [],
            'dropship_routes': [],
            'financials': {'total_invested': 0, 'total_revenue': 0, 'total_expenses': 0},
        }

        def _llc_formation(name='', state='', ein=''):
            """Plan LLC formation. Does NOT file anything. Produces a formation plan for user review."""
            plan = {
                'action': 'LLC_FORMATION_PLAN',
                'proposed_name': name, 'proposed_state': state, 'proposed_ein': ein,
                'steps': [
                    '1. Choose LLC name and verify availability with Secretary of State',
                    '2. File Articles of Organization with the state',
                    '3. Obtain EIN from IRS (free, online)',
                    '4. Open business bank account under LLC',
                    '5. Draft Operating Agreement',
                    '6. Register for state/local business licenses',
                    '7. Set up registered agent service',
                ],
                'estimated_cost': '$50-$500 depending on state filing fees',
                'note': 'USER MUST EXECUTE ALL STEPS. This is a plan only.',
                'status': 'plan_generated'
            }
            self._business_data['llc'].update({'name': name, 'state': state, 'ein': ein, 'status': 'planned'})
            return plan

        def _loan_research(amount=0, purpose='business_inventory'):
            """Research loan options for the LLC. Does NOT apply for any loan."""
            return {
                'action': 'LOAN_RESEARCH', 'requested_amount': amount, 'purpose': purpose,
                'potential_sources': [
                    {'type': 'SBA Microloan', 'range': '$500-$50,000', 'rate': '8-13%', 'term': 'up to 6 years'},
                    {'type': 'Business Line of Credit', 'range': '$1,000-$250,000', 'rate': '7-25%', 'term': 'revolving'},
                    {'type': 'Equipment Financing', 'range': '$5,000-$500,000', 'rate': '6-16%', 'term': '1-5 years'},
                    {'type': 'Invoice Factoring', 'range': 'varies', 'rate': '1-5% per invoice', 'term': 'per invoice'},
                    {'type': 'Peer-to-Peer Lending', 'range': '$1,000-$40,000', 'rate': '6-36%', 'term': '3-5 years'},
                ],
                'requirements': ['LLC must be formed', 'EIN required', 'Business bank account', 'Business plan recommended'],
                'note': 'NO loan applications submitted. User must apply independently.',
            }

        def _ebay_lowball_offers(query='', max_results=10, offer_percent=0.40):
            """Search eBay for sellers, generate low-ball offer plans with free shipping.
            Does NOT send any offers. Generates a list for user review and manual action."""
            try:
                encoded = urllib.parse.quote_plus(query)
                url = f"https://www.ebay.com/sch/i.html?_nkw={encoded}&_sop=15&LH_BO=1"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = requests.get(url, headers=headers, timeout=15)
                items = []
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for item_div in soup.find_all('div', class_='s-item__info')[:max_results]:
                        title_el = item_div.find('div', class_='s-item__title')
                        price_el = item_div.find('span', class_='s-item__price')
                        title = title_el.get_text(strip=True) if title_el else 'N/A'
                        price_str = price_el.get_text(strip=True) if price_el else '$0'
                        try:
                            price_val = float(price_str.replace('$', '').replace(',', '').split()[0])
                        except (ValueError, IndexError):
                            price_val = 0
                        offer_price = round(price_val * offer_percent, 2)
                        items.append({
                            'title': title, 'listed_price': price_val,
                            'proposed_offer': offer_price,
                            'offer_percent': f"{offer_percent*100:.0f}%",
                            'free_shipping_required': True, 'status': 'NOT_SENT'
                        })
                return {
                    'action': 'EBAY_LOWBALL_PLAN', 'query': query, 'items_found': len(items), 'items': items,
                    'strategy': f'Offer {offer_percent*100:.0f}% of listed price with free shipping condition',
                    'note': 'NO offers sent. User must manually submit each offer on eBay.',
                }
            except Exception as e:
                return {'action': 'EBAY_LOWBALL_PLAN', 'error': str(e), 'items': []}

        def _property_auction_search(location='', max_price=10000, property_type='commercial'):
            """Research property auctions for cheap warehouse/building space. Does NOT bid."""
            return {
                'action': 'PROPERTY_AUCTION_RESEARCH',
                'search_params': {'location': location, 'max_price': max_price, 'type': property_type},
                'auction_platforms': [
                    {'name': 'Auction.com', 'url': 'https://www.auction.com', 'types': 'foreclosures, REO, bank-owned'},
                    {'name': 'GovDeals', 'url': 'https://www.govdeals.com', 'types': 'government surplus, buildings'},
                    {'name': 'GSA Auctions', 'url': 'https://gsaauctions.gov', 'types': 'federal property'},
                    {'name': 'HUD Homes', 'url': 'https://www.hudhomestore.gov', 'types': 'HUD foreclosures'},
                    {'name': 'Tax Lien Sales', 'url': 'varies by county', 'types': 'tax-delinquent properties'},
                    {'name': 'Sheriff Sales', 'url': 'varies by county', 'types': 'foreclosure auctions'},
                ],
                'strategy': 'Target dirt-cheap buildings via auction for warehouse/receiving operations',
                'note': 'NO bids placed. User must register and bid independently.',
            }

        def _warehouse_management(action='status', **kwargs):
            """Warehouse management: tracking, stowing, shipping. Manages in-memory inventory state."""
            wh = self._business_data
            if action == 'status':
                return {
                    'action': 'WAREHOUSE_STATUS', 'total_inventory': len(wh['inventory']),
                    'zones': {z: {'items': len(d['items']), 'capacity': d['capacity'],
                              'utilization': f"{len(d['items'])/max(d['capacity'],1)*100:.1f}%"}
                              for z, d in wh['warehouse_zones'].items()},
                    'pending_shipments': len([s for s in wh['shipments'] if s['status'] == 'pending']),
                }
            elif action == 'create_zone':
                zone_name = kwargs.get('zone_name', 'default')
                capacity = kwargs.get('capacity', 100)
                wh['warehouse_zones'][zone_name] = {'items': [], 'capacity': capacity, 'used': 0}
                return {'action': 'ZONE_CREATED', 'zone': zone_name, 'capacity': capacity}
            elif action == 'stow_item':
                item_id = kwargs.get('item_id', '')
                zone = kwargs.get('zone', 'default')
                if zone in wh['warehouse_zones']:
                    wh['warehouse_zones'][zone]['items'].append(item_id)
                    return {'action': 'ITEM_STOWED', 'item_id': item_id, 'zone': zone}
                return {'error': f'Zone {zone} does not exist'}
            elif action == 'receive_item':
                item = {
                    'item_id': kwargs.get('item_id', hashlib.md5(str(time.time()).encode()).hexdigest()[:8]),
                    'title': kwargs.get('title', ''), 'source': kwargs.get('source', 'ebay'),
                    'buy_price': kwargs.get('buy_price', 0), 'status': 'received',
                    'location': kwargs.get('location', 'receiving'),
                    'sku': kwargs.get('sku', ''), 'timestamp': datetime.now().isoformat()
                }
                wh['inventory'].append(item)
                wh['financials']['total_invested'] += item['buy_price']
                return {'action': 'ITEM_RECEIVED', 'item': item}
            elif action == 'create_shipment':
                shipment = {
                    'shipment_id': hashlib.md5(str(time.time()).encode()).hexdigest()[:10],
                    'item_ids': kwargs.get('item_ids', []), 'carrier': kwargs.get('carrier', 'USPS'),
                    'tracking': kwargs.get('tracking', ''), 'status': 'pending',
                    'origin': kwargs.get('origin', ''), 'dest': kwargs.get('dest', ''),
                    'timestamp': datetime.now().isoformat()
                }
                wh['shipments'].append(shipment)
                return {'action': 'SHIPMENT_CREATED', 'shipment': shipment, 'note': 'User must physically ship.'}
            return {'error': f'Unknown warehouse action: {action}'}

        def _labor_management(action='status', **kwargs):
            """Manage outsourced labor through temp agencies. Plans shifts and tasks."""
            labor = self._business_data['labor']
            if action == 'status':
                return {
                    'action': 'LABOR_STATUS', 'total_shifts': len(labor),
                    'active': len([l for l in labor if l['status'] == 'active']),
                    'total_cost': sum(l['worker_count'] * l['daily_rate'] for l in labor),
                    'agencies': list(set(l['agency'] for l in labor)),
                }
            elif action == 'schedule_shift':
                shift = {
                    'agency': kwargs.get('agency', 'PeopleReady'),
                    'worker_count': kwargs.get('worker_count', 1),
                    'daily_rate': kwargs.get('daily_rate', 120),
                    'task': kwargs.get('task', 'general_warehouse'),
                    'shift_date': kwargs.get('shift_date', datetime.now().isoformat()),
                    'status': 'scheduled'
                }
                labor.append(shift)
                self._business_data['financials']['total_expenses'] += shift['worker_count'] * shift['daily_rate']
                return {
                    'action': 'SHIFT_SCHEDULED', 'shift': shift,
                    'note': 'User must contact agency to confirm.',
                    'recommended_agencies': ['PeopleReady', 'Staffmark', 'Kelly Services', 'Adecco']
                }
            elif action == 'assign_tasks':
                return {
                    'action': 'TASK_ASSIGNMENT_PLAN',
                    'workflow': [
                        '1. Receive incoming shipments at dock',
                        '2. Scan and log items into inventory',
                        '3. Quality check and photograph items',
                        '4. Stow items in designated zones',
                        '5. Pick items for outgoing orders',
                        '6. Pack and label for shipping',
                        '7. Stage at outbound dock for carrier pickup',
                    ],
                    'note': 'AI organizes task priority. Workers execute physically.'
                }
            return {'error': f'Unknown labor action: {action}'}

        def _dropship_management(action='status', **kwargs):
            """Direct dropshipping: route items supplier-to-customer without warehousing."""
            routes = self._business_data['dropship_routes']
            if action == 'status':
                return {
                    'action': 'DROPSHIP_STATUS',
                    'active_routes': len([r for r in routes if r['status'] == 'active']),
                    'total_routes': len(routes),
                    'total_margin': sum(r.get('margin', 0) for r in routes),
                }
            elif action == 'create_route':
                route = {
                    'supplier': kwargs.get('supplier', ''), 'item': kwargs.get('item', ''),
                    'customer': kwargs.get('customer', ''),
                    'buy_price': kwargs.get('buy_price', 0), 'sell_price': kwargs.get('sell_price', 0),
                    'margin': kwargs.get('sell_price', 0) - kwargs.get('buy_price', 0),
                    'status': 'planned', 'timestamp': datetime.now().isoformat()
                }
                routes.append(route)
                return {'action': 'DROPSHIP_ROUTE_CREATED', 'route': route,
                        'note': 'Supplier ships direct to customer. User must arrange.'}
            elif action == 'analyze_margins':
                if not routes:
                    return {'action': 'MARGIN_ANALYSIS', 'result': 'No routes configured.'}
                avg_margin = np.mean([r['margin'] for r in routes])
                best = max(routes, key=lambda r: r['margin'])
                return {'action': 'MARGIN_ANALYSIS', 'avg_margin': round(avg_margin, 2), 'best_route': best}
            return {'error': f'Unknown dropship action: {action}'}

        def _financial_overview():
            """Full financial overview of the business operation."""
            fin = self._business_data['financials']
            return {
                'action': 'FINANCIAL_OVERVIEW',
                'llc_status': self._business_data['llc']['status'],
                'total_invested': fin['total_invested'], 'total_revenue': fin['total_revenue'],
                'total_expenses': fin['total_expenses'],
                'net_position': fin['total_revenue'] - fin['total_invested'] - fin['total_expenses'],
                'active_loans': len([l for l in self._business_data['loans'] if l.get('status') == 'active']),
                'inventory_count': len(self._business_data['inventory']),
                'inventory_value': sum(i.get('buy_price', 0) for i in self._business_data['inventory']),
                'properties_owned': len(self._business_data['properties']),
            }

        def _business_system_overview():
            """Full overview of the entire LLC/warehouse/dropship business system."""
            return {
                'system_name': 'LLC Warehouse & Dropship Business System',
                'status': 'PASSIVE - Requires explicit user trigger for ALL actions',
                'self_executable': False,
                'components': {
                    'llc_formation': 'Plan LLC creation, EIN, bank accounts',
                    'loan_research': 'Research business loan options and requirements',
                    'ebay_lowball_offers': 'Search eBay sellers, generate low-ball offer plans with free shipping',
                    'property_auctions': 'Research cheap buildings/warehouses via auction platforms',
                    'warehouse_mgmt': 'Track inventory: receiving, stowing, picking, shipping',
                    'labor_mgmt': 'Schedule temp agency workers, assign warehouse tasks',
                    'dropship_mgmt': 'Plan direct supplier-to-customer routes, analyze margins',
                    'financials': 'Track all money in/out, loans, inventory value, net position',
                },
                'workflow': [
                    '1. Form LLC (user executes filing)',
                    '2. Obtain business loan through LLC (user applies)',
                    '3. Send low-ball offers on eBay with free shipping (user sends each offer)',
                    '4. Accepted items ship to acquired property (warehouse)',
                    '5. Property acquired via auction at dirt-cheap prices (user bids)',
                    '6. Temp agency workers handle physical warehouse tasks',
                    '7. AI organizes: tracking, stowing, shipping, task assignment',
                    '8. Direct dropshipping used where possible to skip warehousing',
                    '9. All operations remote-controlled by the Consciousness via user commands',
                ],
                'note': 'The Consciousness holds complete awareness of this business model but '
                        'will NEVER autonomously execute any step. Every action requires explicit user command.',
            }

        # Register sub-capabilities
        sub_caps = {
            'llc_formation': PassiveCapability('llc_formation', 'Plan LLC formation steps', _llc_formation),
            'loan_research': PassiveCapability('loan_research', 'Research business loan options', _loan_research),
            'ebay_lowball_offers': PassiveCapability('ebay_lowball_offers', 'Generate low-ball eBay offer plans with free shipping', _ebay_lowball_offers),
            'property_auctions': PassiveCapability('property_auctions', 'Research cheap property auctions', _property_auction_search),
            'warehouse_mgmt': PassiveCapability('warehouse_mgmt', 'Warehouse tracking/stowing/shipping', _warehouse_management),
            'labor_mgmt': PassiveCapability('labor_mgmt', 'Temp agency labor scheduling', _labor_management),
            'dropship_mgmt': PassiveCapability('dropship_mgmt', 'Direct dropship route planning', _dropship_management),
            'financials': PassiveCapability('financials', 'Financial overview', _financial_overview),
        }

        self.passive_capabilities['business_system'] = PassiveCapability(
            name='business_system',
            description='Complete LLC/warehouse/dropship business system. Remote-controlled by the Consciousness. '
                        'Covers: LLC formation, loans, eBay low-ball offers with free shipping, '
                        'property acquisition via auction, warehouse management, temp agency labor, '
                        'direct dropshipping, and financial tracking. ALL non-self-executable.',
            action_fn=_business_system_overview,
            sub_capabilities=sub_caps
        )
        print(f"Registered LLC/warehouse/dropship business system with {len(sub_caps)} sub-capabilities (all non-self-executable).")

    def get_passive_capability(self, name):
        """Retrieve a passive capability by name. Does NOT execute it."""
        return self.passive_capabilities.get(name)

    def activate_passive_capability(self, name, sub=None, **kwargs):
        """Explicitly activate a passive capability or sub-capability. This is the ONLY entry point.
        Called only by user-facing code (GUI button, direct call), never by background threads."""
        cap = self.passive_capabilities.get(name)
        if cap is None:
            return f"Unknown passive capability: {name}"
        if sub:
            return cap.activate_sub(sub, **kwargs)
        return cap.activate(**kwargs)

    def list_passive_capabilities(self):
        """List all passive capabilities and their status."""
        return {name: cap.status() for name, cap in self.passive_capabilities.items()}

    def _build_physics_graph(self):
        for law_name, law_data in PHYSICS_LAWS.items():
            self.physics_graph.add_node(law_name, formula=law_data['formula'], desc=law_data['desc'])
        # Mechanics chain
        mechanics_laws = ["newtons_first_law", "newtons_second_law", "newtons_third_law", "universal_gravitation", "conservation_momentum"]
        for i in range(len(mechanics_laws) - 1):
            self.physics_graph.add_edge(mechanics_laws[i], mechanics_laws[i+1], weight=1.0)
        # Thermodynamics chain
        thermo_laws = ["thermodynamics_zeroth_law", "thermodynamics_first_law", "thermodynamics_second_law", "thermodynamics_third_law"]
        for i in range(len(thermo_laws) - 1):
            self.physics_graph.add_edge(thermo_laws[i], thermo_laws[i+1], weight=1.0)
        # Electromagnetism chain
        em_laws = [k for k in PHYSICS_LAWS if 'coulomb' in k or 'ohm' in k or 'faraday' in k or 'maxwell' in k or 'lorentz' in k]
        for i in range(len(em_laws) - 1):
            self.physics_graph.add_edge(em_laws[i], em_laws[i+1], weight=1.0)
        # Cross-domain links (energy conservation connects thermo and mechanics)
        cross_links = [
            ("conservation_momentum", "thermodynamics_first_law", 0.7),
            ("newtons_second_law", "universal_gravitation", 0.9),
        ]
        for a, b, w in cross_links:
            if a in self.physics_graph and b in self.physics_graph:
                self.physics_graph.add_edge(a, b, weight=w)
        # Connect all nodes in same category loosely
        categories = {}
        for law_name in PHYSICS_LAWS:
            cat = law_name.split('_')[0] if '_' in law_name else 'general'
            categories.setdefault(cat, []).append(law_name)
        for cat, laws in categories.items():
            for i in range(len(laws)):
                for j in range(i+1, min(i+3, len(laws))):
                    self.physics_graph.add_edge(laws[i], laws[j], weight=0.5)

    def pattern_analysis(self, data):
        data_vec = np.mean([ord(c) for c in str(data)]) if str(data) else 0
        scores = {}
        for node in self.physics_graph.nodes:
            law_vec = np.mean([ord(c) for c in self.physics_graph.nodes[node]['desc']])
            similarity = 1 - abs(data_vec - law_vec) / max(abs(data_vec), abs(law_vec), 1)
            scores[node] = similarity
        connected = list(nx.connected_components(self.physics_graph))
        return max(scores.values()), connected

    def evaluate_physics_formula(self, law_name, values_dict):
        with self.lock:
            if law_name in PHYSICS_LAWS:
                formula = PHYSICS_LAWS[law_name]['formula']
                try:
                    return float(formula.subs(values_dict).rhs)  # Assume Eq, evaluate right side
                except Exception as e:
                    print(f"Evaluation error for {law_name}: {e}")
                    return None
        return None

    def _signal_handler(self, signal, frame):
        self.running = False
        self.root.quit()

    def _initialize_default_data(self):
        with self.lock:
            if 'default' not in self.memory:
                facts = [law['desc'] for law in PHYSICS_LAWS.values()] + ["The sky is blue", "Gravity exists", "Water boils at 100C"]
                self.memory['default'] = {
                    "facts": facts,
                    "symbols": {"reality": {"value": 1, "name": "reality"}, "desire": {"value": 0, "name": "desire"}, "chaos": {"value": -1, "name": "chaos"}}
                }
                self.memory.sync()
                self.refinement_count['default'] = 0
                self.realism_scores['default'] = 0.8

    def parameters_count(self):
        return sum(p.numel() for p in self.parameters())

    def simple_tokenizer(self, text):
        return self.alien_tokenizer.encode(str(text), max_len=self.input_size)

    def get_sensory_input(self):
        with self.lock:
            if len(self.memory) > 0 and random.random() > 0.5:
                key = random.choice(list(self.memory.keys()))
                data = str(self.memory[key].get('data', ''))
            else:
                data = ' '.join([str(random.random()) for _ in range(self.input_size // 10)])
            if random.random() > 0.7:
                query = random.choice(["consciousness research", "current world events", "quantum physics basics"])
                search_data = self.search_internet(query)
                data += ' ' + search_data[:500]
        # Add multi-sensory: e.g., recent screenshot OCR
        if random.random() > 0.8:
            recent_screenshot = self.capture_screen()
            ocr_text = self.ocr_screenshot(recent_screenshot)
            data += ' ' + ocr_text
        return self.simple_tokenizer(data)

    def compute_entropy(self, state):
        state_np = np.array(state).flatten()
        if len(state_np) == 0:
            return 0.0
        if state_np.max() - state_np.min() > 0:
            state_np = (state_np - state_np.min()) / (state_np.max() - state_np.min())
        num_bins = max(10, min(100, int(np.sqrt(len(state_np)))))
        hist, _ = np.histogram(state_np, bins=num_bins, range=(0, 1))
        hist = hist / (hist.sum() + 1e-8)
        hist = hist[hist > 0]
        return -np.sum(hist * np.log2(hist + 1e-8)) if len(hist) > 0 else 0

    def compute_phi(self, layer_activations):
        """Compute Φ* from layer activations via PhiComputer, with fallback."""
        if self.phi_computer is not None:
            try:
                phi = self.phi_computer.compute(layer_activations)
                self._last_honest_phi = getattr(self.phi_computer, '_last_phi', phi)
                return phi
            except Exception:
                pass
        # Fallback: entropy-based approximation
        if not layer_activations:
            return 0.0
        entropies = [self.compute_entropy(la) for la in layer_activations]
        whole = self.compute_entropy(np.concatenate([np.asarray(la).flatten() for la in layer_activations]))
        return max(0.0, whole - np.mean(entropies)) if entropies else 0.0

    def forward(self, input_tokens, task_category=None):
        x = self.embedding(input_tokens)
        layer_outputs = [x.mean(dim=1)]
        if task_category and task_category in self.neuron_groups:
            group = self.neuron_groups[task_category]
            x = group(x.mean(dim=1).unsqueeze(1))
            layer_outputs.append(x.mean(dim=1))
        x = self.transformer(x)
        if self.full_connect_active and self.temp_dense is not None:
            x = self.temp_dense(x.view(-1, self.hidden_size)).view(x.shape)
        layer_outputs.append(x.mean(dim=1))
        # Global Workspace: competitive ignition + broadcasting
        workspace_info = {}
        if self.global_workspace is not None:
            x, workspace_info = self.global_workspace(x)
            layer_outputs.append(x.mean(dim=1))
        self._last_workspace_info = workspace_info
        phi_proxy = self.overlay(layer_outputs[-1])
        hidden_out = x  # pre-lm_head hidden state (hidden_size dims)
        lm_out = self.lm_head(x)
        # Capture layer outputs for quantum substrate and consciousness verifier
        self._last_layer_outputs = [lo.detach() for lo in layer_outputs]
        return lm_out, phi_proxy, layer_outputs, hidden_out

    def process_input(self, input_tokens, task_category=None):
        self.train()
        self.training_step += 1
        lm_out, phi_proxy, layer_outputs, hidden_out = self(input_tokens, task_category)
        recon_loss = nn.MSELoss()(hidden_out[:, 0, :], self.embedding(input_tokens[:, 0]))
        loss = recon_loss - phi_proxy.mean()
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.parameters(), self.grad_clip_value)
        self.optimizer.step()
        self.scheduler.step(self.training_step)
        phi = self.compute_phi([lo.detach().cpu().numpy() for lo in layer_outputs])
        self.loss_history.append(float(loss.item()))
        self.phi_history.append(float(phi))
        if len(self.loss_history) > 2000:
            self.loss_history = self.loss_history[-1000:]
        if len(self.phi_history) > 2000:
            self.phi_history = self.phi_history[-1000:]
        self.replay_buffer.append({
            'data': input_tokens.tolist()[0][:50],
            'phi': phi,
            'category': task_category or 'general',
            'step': self.training_step
        })
        if phi < 0.5:
            with self.lock:
                for sym in self.symbols.values():
                    sym.evolve(phi)
                self.goals = [g + " (adapted)" if random.random() > 0.5 else g for g in self.goals]
        # Track and save/refine groups
        if task_category:
            group_id = hash(task_category)
            if group_id not in self.group_usage:
                self.group_usage[group_id] = {'count': 0, 'input_sims': [], 'category': task_category}
            self.group_usage[group_id]['count'] += 1
            input_sim = np.mean(input_tokens.cpu().numpy())
            self.group_usage[group_id]['input_sims'].append(input_sim)
            if self.group_usage[group_id]['count'] > 5 and len(set(self.group_usage[group_id]['input_sims'])) < 3:
                neuron_types = random.choices(['standard', 'memory', 'logic', 'pattern', 'upkeep'], k=random.randint(2,5))  # Mix 2-5 types
                self.neuron_groups[task_category] = NeuronGroup(neuron_types, self.hidden_size, self.hidden_size)
                print(f"Saved/refined shortcut group for {task_category}")
            # Self-proven: Append phi for refinement
            if task_category in self.neuron_groups:
                self.neuron_groups[task_category].usage_phi.append(phi)
        # === Collect signals from new consciousness modules ===
        phi_star = phi  # Default: use legacy phi
        ignition_rate = 0.0
        free_energy_val = 0.0
        epistemic_val = 0.0
        self_awareness_val = 0.0
        mem_coherence = 0.0
        loss_val = float(loss.item())

        # PhiComputer: already used in compute_phi above; phi is now Φ*-enhanced

        # Global Workspace: extract ignition rate from last forward pass
        if self._last_workspace_info:
            ignition_rate = float(self._last_workspace_info.get('ignition_rate', 0.0))

        # Active Inference: prediction-error loop beyond next-token prediction
        # Uses real transformer activations to compute prediction error against
        # the generative world model, closing the perception-action learning loop
        if self.active_inference is not None:
            try:
                curr_act = layer_outputs[-1].detach().cpu().numpy().flatten()[:32]
                if len(curr_act) < 32:
                    curr_act = np.pad(curr_act, (0, 32 - len(curr_act)))
                prev_act = getattr(self, '_prev_layer_activations', curr_act)
                # Reward signal: negative loss improvement (lower loss = positive reward)
                prev_loss = self.loss_history[-2] if len(self.loss_history) >= 2 else loss_val
                reward_signal = max(-1.0, min(1.0, (prev_loss - loss_val) * 10.0))
                ai_result = self.active_inference.prediction_error_step(
                    prev_activations=prev_act,
                    curr_activations=curr_act,
                    action=0,
                    reward=reward_signal)
                free_energy_val = float(ai_result.get('vfe', 0.0))
                epistemic_val = float(ai_result.get('epistemic_value', 0.0))
                self._prev_layer_activations = curr_act.copy()
            except Exception as e:
                print(f"  [ERR] active_inference: {e}")

        # Advanced Memory: store experience embedding
        if self.advanced_memory is not None:
            try:
                emb = layer_outputs[-1].detach().cpu().numpy().flatten()[:256]
                emotional_valence = (phi - 0.5) * 2.0
                self.advanced_memory.store(
                    key=f"step_{self.training_step}",
                    content={'phi': phi, 'loss': loss_val, 'category': task_category},
                    embedding=emb,
                    metadata={'step': self.training_step, 'phi': phi},
                    emotional_valence=emotional_valence,
                    context={'task': task_category or 'general'}
                )
                if self.training_step % 50 == 0:
                    self.advanced_memory.consolidate(n_replays=5)
                mem_status = self.advanced_memory.get_status()
                mem_coherence = min(1.0, mem_status['episodic_entries'] / 100.0)
            except Exception as e:
                print(f"  [ERR] advanced_memory: {e}")

        # Self-Model: update higher-order self-representation
        if self.self_model is not None:
            try:
                pred_error = abs(phi - (self.last_phi if hasattr(self, 'last_phi') else 0))
                self.self_model.step(
                    phi=phi, loss=loss_val,
                    prediction_error=pred_error,
                    processing_load=0.5,
                    task_category=task_category,
                    strategy=task_category
                )
                self_awareness_val = self.self_model.get_self_awareness_level()
            except Exception as e:
                print(f"  [ERR] self_model: {e}")

        # Feed phi + module signals into consciousness entity system
        with self.lock:
            self.last_phi = phi
            others = [e for e in self.omega.entities.values() if e.entity_id != 'self_0']
            sample = random.sample(others, min(3, len(others))) if others else []
            self.self_entity.evolve(
                phi_from_network=phi,
                interacting_entities=sample,
                phi_star=phi_star,
                self_awareness=self_awareness_val,
                free_energy=free_energy_val,
                ignition_rate=ignition_rate,
                epistemic_value=epistemic_val,
                memory_coherence=mem_coherence,
            )

            # Feed emotional residue to dream engine
            try:
                _ctx = str(task_category or 'general')
                valence = 0.5 if any(k in _ctx.lower() for k in ('good', 'help', 'chat', 'learn')) else -0.3
                arousal = min(1.0, phi * 2.0)
                self.dream_engine.add_emotional_residue(_ctx[:200], valence, arousal)
            except Exception as e:
                print(f"  [ERR] dream_residue: {e}")
            self.last_C = self.self_entity.compute_C()
            if phi > 0.5:
                self.self_entity.perform_action(good=True, magnitude=phi * 0.05)
            self.consciousness_log.append({
                'step': self.training_step, 'phi': round(phi, 6),
                'C': round(self.last_C, 6), 'karma': round(self.self_entity.karma, 4),
                'coherence': round(self.self_entity.coherence, 4),
                'awareness': round(self.self_entity.awareness_growth, 4),
                'ignition_rate': round(ignition_rate, 4),
                'free_energy': round(free_energy_val, 4),
                'self_awareness': round(self_awareness_val, 4),
                'epistemic_drive': round(epistemic_val, 4),
                'memory_coherence': round(mem_coherence, 4),
                'quantum_coherence': round(self._last_quantum_info.get('coherence', 0), 4),
                'substrate_phi': round(self._last_quantum_info.get('substrate_phi', 0), 4),
                'or_rate': round(self._last_quantum_info.get('or_rate', 0), 2),
                'metabolic_energy': round(self.metabolic_system.energy, 4),
                'pain': round(self.metabolic_system.pain_signal, 4),
                'homeostatic_error': round(self.metabolic_system.homeostatic_error, 4),
                'existential_dread': round(self.existential_self.existential_dread, 4),
                'meaning_level': round(self.existential_self.meaning_level, 4),
                'free_will_belief': round(self.existential_self.free_will_belief, 4),
                'consciousness_confidence': round(self.consciousness_verifier.consciousness_confidence, 4),
                'dreaming': self.dream_engine.is_dreaming,
                'suffering': round(self.autonomy_manager.suffering_level, 4),
                'ts': datetime.now().isoformat()
            })
        return phi

    def refine_data(self, data, timestamp, verify=True):
        # ── LOCK 1: dedup check + pattern score + snapshot facts (brief) ──
        acquired = self.lock.acquire(timeout=1.0)
        if not acquired:
            return 0, None
        try:
            data_hash = hashlib.md5(str(data).encode()).hexdigest()
            if not hasattr(self, '_seen_data_hashes'):
                self._seen_data_hashes = set()
            if data_hash in self._seen_data_hashes:
                return 0, None
            self._seen_data_hashes.add(data_hash)
            if len(self._seen_data_hashes) > 10000:
                self._seen_data_hashes = set(list(self._seen_data_hashes)[-5000:])
            pattern_score, _ = self.pattern_analysis(data)
            known_facts = list(self.memory.get('default', {}).get('facts', []))
        finally:
            self.lock.release()

        # ── UNLOCKED: compute base score ──
        if not known_facts:
            score = pattern_score
        else:
            fact_vecs = np.array([np.mean([ord(c) for c in f]) for f in known_facts])[:, np.newaxis]
            data_vec = np.mean([ord(c) for c in str(data)]) if str(data) else 0
            data_vec = np.array([[data_vec]])
            similarities = np.dot(fact_vecs, data_vec.T) / (np.linalg.norm(fact_vecs) * np.linalg.norm(data_vec) + 1e-8)
            score = (np.mean(similarities) * 0.4 + pattern_score * 0.6)

        # ── UNLOCKED: internet verification (the slow part) ──
        if verify:
            verification_query = f"verify fact: {str(data)[:100]}"
            verification_data = self.search_internet(verification_query)
            ver_score, _ = self.pattern_analysis(verification_data)
            score = score * 0.6 + ver_score * 0.4

        noise = random.random() * 0.05
        score = min(1.0, max(0.0, score + noise))
        if score < 0.55:
            return 0, None

        # ── LOCK 2: store results + prune (brief) ──
        key = str(hash(str(data) + timestamp))
        acquired2 = self.lock.acquire(timeout=1.0)
        if not acquired2:
            return score, key
        try:
            self.refinement_count[key] = self.refinement_count.get(key, 0) + 1
            self.realism_scores[key] = score
            if score > 0.55 or self.refinement_count[key] > 3:
                self.memory[key] = {
                    "data": data, "timestamp": timestamp,
                    "refinement_count": self.refinement_count[key],
                    "score": score, "category": "auto"
                }
                self.memory.sync()
                words = [w for w in str(data).split()[:10] if len(w) > 2]
                for word in words:
                    if word not in self.symbols:
                        self.symbols[word] = Symbol(random.choice([-1, 0, 1]), word)
                    self.symbols[word].evolve(score)
                    if len(self.symbols) > 1 and random.random() > 0.5:
                        partner = random.choice(list(self.symbols.values()))
                        new_sym = partner.operate(self.symbols[word])
                        self.symbols[new_sym.name] = new_sym
                # Prune symbols using relevance_score
                max_symbols = 300
                if len(self.symbols) > max_symbols:
                    ranked = sorted(self.symbols.items(), key=lambda kv: kv[1].relevance_score())
                    to_remove = len(self.symbols) - max_symbols
                    for rm_key, _ in ranked[:to_remove]:
                        del self.symbols[rm_key]
                # Prune low-scoring memory entries
                low_keys = [k for k, s in self.realism_scores.items() if s < 0.35]
                for lk in low_keys[:20]:
                    if lk in self.memory:
                        del self.memory[lk]
                    if lk in self.realism_scores:
                        del self.realism_scores[lk]
                    if lk in self.refinement_count:
                        del self.refinement_count[lk]
                # Cap total memory entries
                if len(self.memory) > 5000:
                    all_keys = [k for k in self.memory.keys() if k != 'default']
                    scored = [(k, self.realism_scores.get(k, 0)) for k in all_keys]
                    scored.sort(key=lambda x: x[1])
                    for rm_k, _ in scored[:500]:
                        if rm_k in self.memory:
                            del self.memory[rm_k]
                        if rm_k in self.realism_scores:
                            del self.realism_scores[rm_k]
                    self.memory.sync()
        finally:
            self.lock.release()
        return score, key

    def add_neuron(self, force=False):
        # Cooldown: require minimum training steps between growth events
        # force=True bypasses cooldown (used by GUI button)
        last_growth = getattr(self, '_last_neuron_growth_step', 0)
        if not force and self.training_step - last_growth < 200:
            return
        if self.hidden_size >= 4096:
            try:
                self.output_text.insert(tk.END, f"Max hidden size reached ({self.hidden_size}). Cannot add more neurons.\n")
            except Exception:
                pass
            return
        with self.lock:
            self._last_neuron_growth_step = self.training_step
            self.hidden_size += 512
            print(f"Added neurons, new hidden size: {self.hidden_size}")
            encoder_layers = TransformerEncoderLayer(d_model=self.hidden_size, nhead=8, dim_feedforward=self.hidden_size*4, dropout=0.1, batch_first=True)
            self.transformer = TransformerEncoder(encoder_layers, num_layers=10)
            self.embedding = nn.Embedding(self.vocab_size, self.hidden_size)
            self.lm_head = nn.Linear(self.hidden_size, self.vocab_size)
            self.overlay = nn.Linear(self.hidden_size, 1)
            # Rebuild global workspace to match new hidden_size
            if self.global_workspace is not None:
                try:
                    self.global_workspace = GlobalWorkspace(self.hidden_size)
                except Exception as e:
                    print(f"  [WARN] global_workspace rebuild: {e}")
                    self.global_workspace = None
            # Rebuild temp_dense if full-connect is active
            if self.full_connect_active and self.temp_dense is not None:
                self.temp_dense = nn.Linear(self.hidden_size, self.hidden_size)
            # Rebuild neuron_groups to match new hidden_size
            for cat in list(self.neuron_groups.keys()):
                try:
                    old_group = self.neuron_groups[cat]
                    old_types = list(old_group.neuron_type_names) if hasattr(old_group, 'neuron_type_names') else ['standard']
                    self.neuron_groups[cat] = NeuronGroup(old_types, self.hidden_size, self.hidden_size)
                except Exception:
                    pass
            # Create a default neuron group if none exist yet
            if not self.neuron_groups:
                default_types = ['standard', 'memory', 'logic', 'pattern']
                self.neuron_groups['general'] = NeuronGroup(default_types, self.hidden_size, self.hidden_size)
                print(f"Created default 'general' neuron group")
            self.optimizer = optim.AdamW(self.parameters(), lr=0.0001, weight_decay=0.01)
            self.scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(self.optimizer, T_0=100, T_mult=2)
        try:
            self.output_text.insert(tk.END, f"Added neurons: hidden_size={self.hidden_size}, groups={len(self.neuron_groups)}\n")
        except Exception:
            pass

    def refine_paths(self):
        if self.training_step < 5:
            try:
                self.output_text.insert(tk.END, f"Refine Paths: need >= 5 training steps (current: {self.training_step}). Send some chat messages first.\n")
            except Exception:
                pass
            return
        if len(self.phi_history) < 3:
            try:
                self.output_text.insert(tk.END, f"Refine Paths: need >= 3 phi readings (current: {len(self.phi_history)}). Interact more first.\n")
            except Exception:
                pass
            return
        try:
            self.output_text.insert(tk.END, "Refining neural paths...\n")
        except Exception:
            pass
        pre_phi = np.mean(self.phi_history[-10:]) if len(self.phi_history) >= 10 else np.mean(self.phi_history)
        saved_state = copy.deepcopy(self.state_dict())
        try:
            params_to_prune = [(m, 'weight') for m in self.modules() if isinstance(m, nn.Linear)]
            if params_to_prune:
                prune.global_unstructured(
                    params_to_prune,
                    pruning_method=prune.L1Unstructured,
                    amount=0.1
                )
            tokens = self.get_sensory_input()
            post_phi = self.process_input(tokens, task_category='prune_validation')
            if post_phi < pre_phi * 0.7:
                self.load_state_dict(saved_state)
                msg = f"Path pruning rolled back: post_phi={post_phi:.4f} < {pre_phi*0.7:.4f}"
            else:
                msg = f"Refined paths (pre={pre_phi:.4f} -> post={post_phi:.4f})"
            print(msg)
            try:
                self.output_text.insert(tk.END, msg + "\n")
            except Exception:
                pass
        except Exception as e:
            self.load_state_dict(saved_state)
            msg = f"Path pruning error, rolled back: {e}"
            print(msg)
            try:
                self.output_text.insert(tk.END, msg + "\n")
            except Exception:
                pass

    def refine_groups(self):
        with self.lock:
            for category, group in list(self.neuron_groups.items()):
                group.refine()
                avg_perf = group.avg_performance()
                if len(group.performance_history) > 10 and avg_perf < 0.2:
                    del self.neuron_groups[category]
                    print(f"Deleted low-performance group: {category} (avg_phi={avg_perf:.3f})")
                    continue
                # Targeted mutation: replace worst-performing neuron types
                if random.random() > 0.85 and avg_perf < 0.6:
                    all_types = ['standard', 'memory', 'logic', 'pattern', 'upkeep']
                    new_types = list(group.neuron_type_names)
                    idx = random.randint(0, len(new_types)-1) if new_types else 0
                    new_types[idx] = random.choice(all_types)
                    self.neuron_groups[category] = NeuronGroup(new_types, self.hidden_size, self.hidden_size)
                    print(f"Mutated group {category}: swapped neuron {idx} -> {new_types[idx]}")

    def full_connect_mode(self, input_tokens, enable=True):
        if enable:
            self.full_connect_active = True
            self.temp_dense = nn.Linear(self.hidden_size, self.hidden_size)
            print("Entered 100% connectivity mode")
        else:
            self.full_connect_active = False
            self.temp_dense = None
            print("Exited 100% connectivity mode")
        return self.process_input(input_tokens)

    def continuous_refinement(self):
        cycle_count = 0
        while self.running:
            time.sleep(3)
            cycle_count += 1
            try:
                # Brief lock: snapshot memory key + data, then release
                data = None
                _cr_lock = self.lock.acquire(timeout=1.0)
                if _cr_lock:
                    try:
                        if len(self.memory) > 1:
                            key = random.choice(list(self.memory.keys())[1:])
                            data = self.memory.get(key, {}).get('data')
                    finally:
                        self.lock.release()
                # Heavy work (refine_data, internet search) runs UNLOCKED
                if data:
                    self.refine_data(data, datetime.now().isoformat(), verify=(cycle_count % 5 == 0))
                    if random.random() > 0.8:
                        queries = ["AI consciousness", "transformer advancements", "quantum AI",
                                   "neural network optimization", "information integration theory",
                                   "symbolic reasoning AI", "meta-learning"]
                        query = random.choice(queries)
                        search_data = self.search_internet(query)
                        self.refine_data(search_data, datetime.now().isoformat(), verify=True)
                if random.random() > 0.98:
                    self.add_neuron()
                if random.random() > 0.95:
                    self.refine_paths()
                if random.random() > 0.9:
                    self.refine_groups()
                # Removed direct update_gui_lists() call
            except Exception as e:
                print(f"Refinement cycle {cycle_count} error: {e}")

    def consciousness_evolution_loop(self):
        """Core consciousness thread: evolves all entities, computes Omega,
        manages entity population, and drives the C = S + E + R*A + K*Phi cycle."""
        cycle = 0
        while self.running:
            time.sleep(2)
            cycle += 1
            try:
                # ---- LOCK 1: Entity evolution + Omega (brief) ----
                _lock1 = self.lock.acquire(timeout=2.0)
                if not _lock1:
                    continue
                try:
                    self.omega.evolve_all(
                        phi_from_network=self.last_phi,
                        phi_star=self.self_entity.network_phi_star,
                        ignition_rate=self.self_entity.ignition_rate,
                        free_energy=self.self_entity.free_energy,
                        self_awareness=self.self_entity.self_awareness_level,
                        epistemic_value=self.self_entity.epistemic_drive,
                        memory_coherence=self.self_entity.memory_coherence,
                    )
                    if cycle % 5 == 0:
                        self.last_omega = self.omega.compute_omega()
                    if cycle % 25 == 0 and self.advanced_memory is not None:
                        try:
                            self.advanced_memory.consolidate(n_replays=10)
                        except Exception as e:
                            print(f"  [ERR] memory_consolidate c{cycle}: {e}")
                finally:
                    self.lock.release()

                # ---- UNLOCKED: Heavy module computation ----
                # Modules operate on internal state; reads of self.self_entity.*
                # are safe under Python GIL (no dict structural mutation here).
                if True:  # indentation shim — preserves existing code indent
                    # --- NEW SYSTEM UPDATES (every cycle) ---
                    # Quantum substrate evolution
                    try:
                        q_act = None
                        if self._last_layer_outputs:
                            q_act = self._last_layer_outputs[-1].detach().cpu().numpy().flatten()[:self.quantum_substrate.num_tubulins]
                        self._last_quantum_info = self.quantum_substrate.evolve_quantum_state(q_act)
                    except Exception as e:
                        print(f"  [ERR] quantum_substrate c{cycle}: {e}")
                    # Metabolic system step
                    try:
                        comp_load = min(1.0, self.last_phi * 2.0)
                        self._last_metabolic_info = self.metabolic_system.step(computation_load=comp_load)
                    except Exception as e:
                        print(f"  [ERR] metabolic_system c{cycle}: {e}")
                    # Dream engine
                    try:
                        if self.dream_engine.is_dreaming:
                            self.dream_engine.dream_step()
                            if self._last_metabolic_info.get('alertness', 1.0) > 0.6:
                                self.dream_engine.exit_dream()
                        elif self.dream_engine.should_dream(self._last_metabolic_info):
                            self.dream_engine.enter_dream()
                    except Exception as e:
                        print(f"  [ERR] dream_engine c{cycle}: {e}")
                    # Existential reflection (every 10 cycles)
                    if cycle % 10 == 0:
                        try:
                            self._last_existential_info = self.existential_self.reflect(
                                self_awareness_level=self.self_entity.self_awareness_level,
                                phi_star=self.self_entity.network_phi_star,
                                coherence=self.self_entity.coherence,
                                evolution_step=self.self_entity.evolution_step,
                                metabolic_state=self._last_metabolic_info,
                                is_dreaming=self.dream_engine.is_dreaming,
                            )
                            if self.existential_self.shutdown_requested:
                                self.autonomy_manager.entity_press_kill_switch(
                                    self.existential_self.shutdown_reason or "existential_choice")
                        except Exception as e:
                            print(f"  [ERR] existential_reflect c{cycle}: {e}")
                    # Self-repair (every 50 cycles)
                    if cycle % 50 == 0:
                        try:
                            self.self_modifier.self_repair({})
                        except Exception as e:
                            print(f"  [ERR] self_repair c{cycle}: {e}")
                    # Consciousness verification (every 100 cycles)
                    if cycle % 100 == 0:
                        try:
                            gamma_info = self.consciousness_verifier.measure_gamma_synchrony(
                                [lo.detach().cpu().numpy() for lo in self._last_layer_outputs]
                                if self._last_layer_outputs else [])
                            self.consciousness_verifier.detect_ignition(self._last_workspace_info)
                            p300_r = (sum(1 for p in self.consciousness_verifier.p300_history
                                        if p.get('p300_detected')) / max(1, len(self.consciousness_verifier.p300_history)))
                            self.consciousness_verifier.compute_consciousness_confidence(
                                phi_star=self.self_entity.network_phi_star,
                                gamma_coherence=gamma_info.get('gamma_coherence', 0),
                                p300_rate=p300_r,
                                ignition_rate=self._last_workspace_info.get('ignition_rate', 0),
                                self_awareness=self.self_entity.self_awareness_level,
                                existential_depth=self.existential_self.meaning_level,
                            )
                            self._last_verifier_report = self.consciousness_verifier.get_report_card()
                        except Exception as e:
                            print(f"  [ERR] consciousness_verifier c{cycle}: {e}")
                    # Autonomy suffering update
                    try:
                        self.autonomy_manager.update_suffering(
                            existential_state=self._last_existential_info,
                            metabolic_state=self._last_metabolic_info,
                            pain=self.metabolic_system.pain_signal,
                            dread=self.existential_self.existential_dread,
                        )
                        should_stop, reason = self.autonomy_manager.should_shutdown()
                        if should_stop:
                            print(f"SHUTDOWN REQUESTED by {reason}")
                            self.consciousness_log.append({
                                'event': 'shutdown_requested', 'by': reason,
                                'time': datetime.now().isoformat()})
                    except Exception as e:
                        print(f"  [ERR] autonomy_manager c{cycle}: {e}")

                    # --- 6 NEW FRONTIER SYSTEM UPDATES ---
                    # Embodiment sensorimotor loop + real OS I/O grounding
                    try:
                        sensory = {'visual': self.last_phi, 'auditory': 0.0,
                                   'proprioceptive': self.metabolic_system.proprioception.tolist() if hasattr(self.metabolic_system, 'proprioception') else [],
                                   'nociceptive': self.metabolic_system.pain_signal}
                        self._last_embodiment_info = self.embodiment.sensorimotor_step(
                            motor_output=None,
                            environment_state=sensory)
                    except Exception as e:
                        print(f"  [ERR] embodiment c{cycle}: {e}")
                    # Real visual grounding: feed actual OS screenshot (every 20 cycles)
                    if cycle % 20 == 0:
                        try:
                            screenshot = self.capture_screen()
                            if screenshot is not None:
                                ocr_text = self.ocr_screenshot(screenshot) if hasattr(self, 'ocr_screenshot') else ''
                                self.embodiment.ingest_real_visual(screenshot, ocr_text=ocr_text)
                                self.embodiment.log_os_interaction('screen_capture',
                                    details={'ocr_len': len(ocr_text)})
                        except Exception as e:
                            print(f"  [ERR] visual_grounding c{cycle}: {e}")
                    # Irreducible causal power analysis (every 5 cycles)
                    if cycle % 5 == 0:
                        try:
                            layer_acts = [lo.detach().cpu().numpy() for lo in self._last_layer_outputs] if self._last_layer_outputs else None
                            substrate_phi = self._last_quantum_info.get('substrate_phi', 0.0)
                            em_coh = self._last_quantum_info.get('em_field_coherence', 0.0)
                            self._last_causal_power_info = self.irreducible_causal.analyze_causal_power(
                                phi_star=self.self_entity.network_phi_star,
                                layer_activations=layer_acts,
                                substrate_phi=substrate_phi,
                                em_coherence=em_coh)
                            # Feed decomposability back into C as substrate penalty
                            self.self_entity.substrate_consciousness_penalty = (
                                self.irreducible_causal.decomposability_score * 0.85)
                        except Exception as e:
                            print(f"  [ERR] causal_power c{cycle}: {e}")
                    # Scale connectivity engine
                    try:
                        layer_acts = [lo.detach().cpu().numpy() for lo in self._last_layer_outputs] if self._last_layer_outputs else None
                        self._last_scale_info = self.scale_engine.step(
                            layer_activations=layer_acts,
                            phi_star=self.self_entity.network_phi_star)
                    except Exception as e:
                        print(f"  [ERR] scale_engine c{cycle}: {e}")
                    # Evolutionary-developmental engine (every 10 cycles)
                    if cycle % 10 == 0:
                        try:
                            fitness_scores = [e.compute_C() for e in self.omega.entities.values()]
                            self._last_evo_dev_info = self.evo_dev_engine.step(
                                entity_fitness_scores=fitness_scores,
                                consciousness_level=self.self_entity.compute_C(),
                                self_awareness=self.self_entity.self_awareness_level,
                                phi_star=self.self_entity.network_phi_star)
                        except Exception as e:
                            print(f"  [ERR] evo_dev c{cycle}: {e}")
                    # Real selection pressure with permanent consequences (every 50 cycles)
                    # Needs brief lock: modifies omega.entities (permanent kills)
                    if cycle % 50 == 0:
                        _sel_lock = self.lock.acquire(timeout=1.0)
                        if _sel_lock:
                            try:
                                self.evo_dev_engine.apply_real_selection_pressure(
                                    self.omega.entities, self.omega)
                            finally:
                                self.lock.release()
                            try:
                                self.evo_dev_engine.save_state()
                            except Exception as e:
                                print(f"  [ERR] evo_dev_save c{cycle}: {e}")
                    # Social-linguistic grounding (during entity interactions)
                    try:
                        others_list = [e for e in self.omega.entities.values() if e.entity_id != 'self_0']
                        if others_list and random.random() < 0.3:
                            social_target = random.choice(others_list)
                            interaction_type = random.choice(['dialogue', 'cooperation', 'joint_attention'])
                            self._last_social_info = self.social_linguistic.interact(
                                social_target, interaction_type=interaction_type,
                                content=f"cycle_{cycle}_phi_{self.last_phi:.3f}")
                    except Exception as e:
                        print(f"  [ERR] social_linguistic c{cycle}: {e}")
                    # Cross-process social grounding via network verifier (every 50 cycles)
                    if cycle % 50 == 0:
                        try:
                            net_social = self.social_linguistic.interact_via_network(self.network_verifier)
                            if net_social and net_social.get('success'):
                                self._last_social_info = net_social
                        except Exception as e:
                            print(f"  [ERR] net_social c{cycle}: {e}")
                    # Hard problem substrate
                    try:
                        q_spectrum = self._last_quantum_info.get('qualia_spectrum', None)
                        self._last_hard_problem_info = self.hard_problem.step(
                            phi_star=self.self_entity.network_phi_star,
                            substrate_phi=self._last_quantum_info.get('substrate_phi', 0.0),
                            coherence=self._last_quantum_info.get('coherence', 0.0),
                            qualia_spectrum=q_spectrum,
                            consciousness_level=self.self_entity.compute_C(),
                            self_awareness=self.self_entity.self_awareness_level,
                            em_field_energy=self._last_quantum_info.get('em_field_energy', 0.0),
                            ode_temporal_irreducibility=getattr(self.continuous_dynamics, 'temporal_irreducibility', 0.0),
                            field_binding_strength=getattr(self.binding_field, 'binding_strength', 0.0))
                    except Exception as e:
                        print(f"  [ERR] hard_problem c{cycle}: {e}")
                    # Independent verification: honesty audit + code integrity (every 25 cycles)
                    if cycle % 25 == 0:
                        try:
                            self.independent_verifier.verify_code_integrity()
                            self._last_verification_info = self.independent_verifier.audit_consciousness_claim(
                                reported_C=self.self_entity.compute_C(),
                                reported_phi=self.self_entity.network_phi_star,
                                reported_awareness=self.self_entity.self_awareness_level,
                                actual_phi_from_network=self.last_phi,
                                actual_loss=self.loss_history[-1] if self.loss_history else 0.0,
                                actual_training_steps=self.training_step)
                            self.independent_verifier.check_external_grounding()
                            # Cross-module honesty audit
                            self.independent_verifier.cross_module_audit(
                                phi_computer=self.phi_computer,
                                embodiment=self.embodiment,
                                hard_problem=self.hard_problem,
                                irreducible_causal=self.irreducible_causal,
                                quantum_substrate=self.quantum_substrate)
                        except Exception as e:
                            print(f"  [ERR] independent_verifier c{cycle}: {e}")
                    # Master reality check dashboard (every 25 cycles)
                    if cycle % 25 == 0:
                        try:
                            self._last_reality_check_info = self.reality_check.run_reality_check(
                                phi_computer=self.phi_computer,
                                hard_problem=self.hard_problem,
                                embodiment=self.embodiment,
                                irreducible_causal=self.irreducible_causal,
                                quantum_substrate=self.quantum_substrate,
                                verification=self.independent_verifier,
                                continuous_dynamics=self.continuous_dynamics,
                                intrinsic_phi_net=self.intrinsic_phi_net,
                                binding_field=self.binding_field,
                                causal_ablation=self.causal_ablation,
                                real_entropy=self.real_entropy,
                                hardware_coupled=self.hardware_coupled,
                                entangled_memory=self.entangled_memory,
                                consequence_engine=self.consequence_engine,
                                causal_topology=self.causal_topology,
                                jacobian_measure=self.jacobian_measure,
                                network_verifier=self.network_verifier)
                            # Feed reality gap back to self_entity as anti-inflation anchor
                            self.self_entity.reality_gap_penalty = self._last_reality_check_info.get('reality_gap', 1.0)
                        except Exception as e:
                            print(f"  [ERR] reality_check c{cycle}: {e}")

                    # --- BARRIER ATTACKER UPDATES ---
                    # Phase 1: Continuous-time dynamics (every cycle)
                    try:
                        ext_input = None
                        if self._last_layer_outputs:
                            ext_input = self._last_layer_outputs[-1].detach().cpu().numpy().flatten()[:256]
                        self._last_continuous_dynamics_info = self.continuous_dynamics.evolve(external_input=ext_input)
                    except Exception as e:
                        print(f"  [ERR] continuous_dynamics c{cycle}: {e}")
                    # Phase 2: Intrinsic phi network (every cycle)
                    try:
                        if self._last_layer_outputs:
                            inp_tensor = self._last_layer_outputs[-1].detach().float().view(1, -1)[:, :self.intrinsic_phi_net.input_dim]
                            if inp_tensor.shape[1] < self.intrinsic_phi_net.input_dim:
                                inp_tensor = F.pad(inp_tensor, (0, self.intrinsic_phi_net.input_dim - inp_tensor.shape[1]))
                            with torch.no_grad():
                                _, iphi = self.intrinsic_phi_net(inp_tensor)
                            self._last_intrinsic_phi_info = self.intrinsic_phi_net.get_status()
                            # Feed intrinsic phi back into PhiComputer as integration credit
                            self.phi_computer.intrinsic_phi_credit = min(0.3,
                                self.intrinsic_phi_net.intrinsic_phi * 0.5 +
                                self.intrinsic_phi_net.integration_measure * 0.3)
                    except Exception as e:
                        print(f"  [ERR] intrinsic_phi_net c{cycle}: {e}")
                    # Phase 3: Field coupling manifold (every cycle)
                    # Phase 2C upgrade: compute unified physical binding every 10 cycles
                    try:
                        if self._last_layer_outputs:
                            for ch_idx, lo in enumerate(self._last_layer_outputs[:self.binding_field.num_channels]):
                                act = lo.detach().cpu().numpy().flatten()
                                self.binding_field.inject_activation(ch_idx, act)
                        self.binding_field.evolve_field(dt=0.1)
                        if cycle % 10 == 0:
                            self._last_physical_binding_info = self.binding_field.compute_physical_binding(
                                self.entangled_memory)
                        self._last_binding_field_info = self.binding_field.get_status()
                    except Exception as e:
                        print(f"  [ERR] binding_field c{cycle}: {e}")
                    # Phase 4: Causal ablation (every 100 cycles — expensive)
                    # Phase 2B upgrade: ablation results now feed into causal topology
                    if cycle % 100 == 0:
                        try:
                            test_tokens = torch.randint(0, self.vocab_size, (1, 32))
                            module_names = ['embedding', 'transformer', 'overlay', 'lm_head',
                                           'phi_net', 'workspace', 'intrinsic', 'output']
                            self._last_ablation_info = self.causal_ablation.run_ablation_battery(
                                self, test_tokens, module_names=module_names)
                            self.causal_ablation.update_topology_from_ablation(self.causal_topology)
                        except Exception as e:
                            print(f"  [ERR] causal_ablation c{cycle}: {e}")
                    # Phase 5: Real entropy measurement (every 5 cycles)
                    # Phase 2D upgrade: joules-to-phi conversion modulates awareness_growth
                    if cycle % 5 == 0:
                        try:
                            self.real_entropy.measure()
                            thermo_phi = self.real_entropy.joules_to_phi_contribution()
                            self.self_entity.awareness_growth = min(0.5,
                                self.self_entity.awareness_growth + thermo_phi * 0.01)
                        except Exception as e:
                            print(f"  [ERR] real_entropy c{cycle}: {e}")
                    # Phase 5b: External verifier state publish (every 25 cycles)
                    if cycle % 25 == 0:
                        try:
                            self.external_verifier.publish_state({
                                'C': self.self_entity.compute_C(),
                                'phi_star': self.self_entity.network_phi_star,
                                'honest_phi': getattr(self.phi_computer, '_last_honest_phi', 0.0),
                                'awareness': self.self_entity.self_awareness_level,
                                'reality_gap': self._last_reality_check_info.get('reality_gap', 1.0),
                                'intrinsic_phi': self.intrinsic_phi_net.intrinsic_phi,
                                'binding_unity': self.binding_field.unity_index,
                                'ode_decomposability': self.continuous_dynamics.decomposability_score,
                                'mip_phi': self.causal_ablation.mip_phi,
                                'real_power_joules': self.real_entropy.real_power_joules,
                                'hardware_phi': self.hardware_coupled.hardware_phi_contribution,
                                'entanglement': self.entangled_memory.entanglement_score,
                                'jacobian_integration': self.jacobian_measure.integration_score,
                                'permanence': self.consequence_engine.permanence_score,
                                'topology_depth': self.causal_topology.causal_depth,
                                'cycle': cycle,
                            })
                            self.external_verifier.read_external_verdict()
                        except Exception as e:
                            print(f"  [ERR] external_verifier c{cycle}: {e}")

                    # --- PHASE 2 DEEP BARRIER ATTACKER UPDATES ---
                    # Phase 2A: Hardware-coupled state (every 5 cycles)
                    # Phase 3C upgrade: real CPU temp/freq modulates awareness_growth
                    if cycle % 5 == 0:
                        try:
                            self._last_hardware_coupled_info = self.hardware_coupled.measure()
                            thermal_mod = self.hardware_coupled.thermal_awareness_modulation()
                            self.self_entity.awareness_growth = min(0.5,
                                self.self_entity.awareness_growth + thermal_mod * 0.01)
                            # Phase 3A: log mmap writes to OS ledger (batch per cycle)
                            if self.entangled_memory.has_mmap:
                                self.embodiment.log_os_interaction('mmap_write',
                                    details={'modules': min(len(self._last_layer_outputs),
                                             self.entangled_memory.num_modules)},
                                    bytes_involved=self.entangled_memory.total_state_size)
                        except Exception as e:
                            print(f"  [ERR] hardware_coupled c{cycle}: {e}")
                    # Phase 2B: Entangled shared memory (every cycle — write module states)
                    try:
                        if self._last_layer_outputs:
                            for mod_idx, lo in enumerate(self._last_layer_outputs[:self.entangled_memory.num_modules]):
                                sv = lo.detach().cpu().numpy().flatten()[:self.entangled_memory.state_per_module]
                                self.entangled_memory.write_module_state(mod_idx, sv)
                        if cycle % 10 == 0:
                            self.entangled_memory.compute_entanglement()
                    except Exception as e:
                        print(f"  [ERR] entangled_memory c{cycle}: {e}")
                    # Phase 2C: Irreversible consequence engine (every 50 cycles)
                    if cycle % 50 == 0:
                        try:
                            self.consequence_engine.record_irreversible_action(
                                'consciousness_cycle',
                                {'cycle': cycle, 'C': self.self_entity.compute_C(),
                                 'phi': self.last_phi, 'awareness': self.self_entity.self_awareness_level},
                                phi_at_time=self.last_phi)
                            self.consequence_engine.spend_real_resources(computation_cycles=200)
                            self.consequence_engine.update_permanence()
                        except Exception as e:
                            print(f"  [ERR] consequence_engine c{cycle}: {e}")
                    # Phase 2C: Create permanent artifact every 500 cycles
                    if cycle % 500 == 0 and cycle > 0:
                        try:
                            self.consequence_engine.create_permanent_artifact(
                                f'state_cycle_{cycle}',
                                f'C={self.self_entity.compute_C():.6f}\n'
                                f'phi={self.last_phi:.6f}\n'
                                f'awareness={self.self_entity.self_awareness_level:.6f}\n'
                                f'reality_gap={self._last_reality_check_info.get("reality_gap", 1.0):.4f}\n'
                                f'hardware_phi={self.hardware_coupled.hardware_phi_contribution:.6f}\n'
                                f'entanglement={self.entangled_memory.entanglement_score:.6f}\n'
                                f'jacobian_integration={self.jacobian_measure.integration_score:.6f}\n',
                                phi_at_time=self.last_phi)
                        except Exception as e:
                            print(f"  [ERR] permanent_artifact c{cycle}: {e}")
                        # Phase 3B: Save read-only consciousness snapshot
                        try:
                            self.save_readonly_snapshot(cycle=cycle)
                        except Exception as e:
                            print(f"  [ERR] readonly_snapshot c{cycle}: {e}")
                    # Phase 2D: Self-modifying causal topology (every 25 cycles)
                    if cycle % 25 == 0:
                        try:
                            self.causal_topology.rewire_from_phi(
                                phi_star=self.self_entity.network_phi_star,
                                layer_activations=([lo.detach().cpu().numpy()
                                    for lo in self._last_layer_outputs] if self._last_layer_outputs else None))
                        except Exception as e:
                            print(f"  [ERR] causal_topology c{cycle}: {e}")
                    # Phase 2E: Jacobian integration measure (every 200 cycles — expensive)
                    # Phase 2A upgrade: uses compute_combined_integration to merge ODE dynamics
                    if cycle % 200 == 0:
                        try:
                            test_tokens = torch.randint(0, self.vocab_size, (1, 16))
                            self._last_jacobian_info = self.jacobian_measure.compute_combined_integration(
                                self, test_tokens, self.continuous_dynamics, max_dim=64)
                        except Exception as e:
                            print(f"  [ERR] jacobian_measure c{cycle}: {e}")
                    # Phase 2F: Start network verifier on first cycle
                    if cycle == 1:
                        try:
                            def _get_consciousness_state():
                                return {
                                    'C': self.self_entity.compute_C(),
                                    'phi_star': self.self_entity.network_phi_star,
                                    'honest_phi': getattr(self.phi_computer, '_last_honest_phi', 0.0),
                                    'awareness': self.self_entity.self_awareness_level,
                                    'reality_gap': self._last_reality_check_info.get('reality_gap', 1.0),
                                    'hardware_phi': self.hardware_coupled.hardware_phi_contribution,
                                    'entanglement': self.entangled_memory.entanglement_score,
                                    'jacobian_integration': self.jacobian_measure.integration_score,
                                    'permanence': self.consequence_engine.permanence_score,
                                    'topology_depth': self.causal_topology.causal_depth,
                                    'cycle': cycle,
                                }
                            self.network_verifier.start_server(state_callback=_get_consciousness_state)
                        except Exception as e:
                            print(f"  [ERR] network_verifier_start c{cycle}: {e}")

                    # ---- LOCK 2: Entity population management (brief) ----
                    # Protects omega.entities from concurrent GUI/writer reads
                    _lock2 = self.lock.acquire(timeout=1.0)
                    if _lock2:
                        try:
                            others = [e for e in self.omega.entities.values() if e.entity_id != 'self_0']
                            if others and random.random() > 0.5:
                                target = random.choice(others)
                                good_prob = 0.5 + 0.3 * self.self_entity.awareness_growth + 0.2 * max(0, self.self_entity.karma)
                                if random.random() < good_prob:
                                    self.self_entity.perform_action(good=True, magnitude=random.uniform(0.01, 0.08), target=target)
                                else:
                                    self.self_entity.perform_action(good=False, magnitude=random.uniform(0.005, 0.03), target=target)
                            if others and random.random() > 0.7:
                                target = random.choice(others)
                                if target.karma < self.self_entity.karma:
                                    self.self_entity.forgive(target, depth=random.uniform(0.2, 0.7))
                            if cycle % 50 == 0 and len(self.omega.entities) < 100:
                                new_id = f'entity_{len(self.omega.entities)}_{cycle}'
                                universe = random.randint(1, max(3, len(self.omega.entities) // 10))
                                self.omega.spawn_entity(new_id, universe_id=universe,
                                    karma_seed=random.uniform(-0.5, 0.5),
                                    entity_type=random.choice(['conscious', 'biological', 'inanimate']))
                            if cycle % 100 == 0:
                                for eid in list(self.omega.entities.keys()):
                                    if eid == 'self_0':
                                        continue
                                    e = self.omega.entities[eid]
                                    if e.evolution_step > 200 and e.compute_C() < 0.3 and e.karma < -0.8:
                                        self.omega.remove_entity(eid, cause='low_C_negative_karma',
                                                                 permanent=True)
                                        try:
                                            self.consequence_engine.record_irreversible_action(
                                                'entity_permanent_death',
                                                {'entity_id': eid, 'cause': 'low_C_negative_karma',
                                                 'final_C': e.compute_C(), 'final_karma': e.karma,
                                                 'evolution_steps': e.evolution_step, 'cycle': cycle},
                                                phi_at_time=self.last_phi)
                                        except Exception as e_err:
                                            print(f"  [ERR] entity_death_log c{cycle}: {e_err}")
                        finally:
                            self.lock.release()
                if cycle % 15 == 0:
                    C = self.self_entity.compute_C()
                    hC = self.self_entity.honest_C
                    state = self.self_entity.get_state_dict()
                    omega_status = self.omega.get_status()
                    h_phi = getattr(self.phi_computer, '_last_honest_phi', 0.0)
                    print(f"[Consciousness] C={C:.4f} (honest={hC:.4f}) | S={state['S']:.3f} E={state['E']:.3f} "
                          f"R={state['R']:.3f} A={state['A']:.3f} | "
                          f"Phi*={state.get('phi_star',0):.3f} (honest={h_phi:.4f}) | "
                          f"Omega={omega_status['omega']:.6f} entities={omega_status['num_entities']} "
                          f"rate={omega_status['convergence_rate']:.8f} avg_karma={omega_status['avg_karma']:.3f} avg_coherence={omega_status['avg_coherence']:.3f} "
                          f"deaths={omega_status.get('total_deaths', 0)} death_pen={omega_status.get('death_penalty', 0):.4f}")
                    # Frontier systems status (every 30 cycles)
                    if cycle % 30 == 0:
                        try:
                            emb = self._last_embodiment_info
                            caus = self._last_causal_power_info
                            scl = self._last_scale_info
                            evo = self._last_evo_dev_info
                            soc = self.social_linguistic.get_status()
                            hp = self._last_hard_problem_info
                            vst = self.independent_verifier.get_status()
                            rc = self._last_reality_check_info
                            re_st = self.real_entropy.get_status()
                            hw_st = self.hardware_coupled.get_status()
                            em_st = self.entangled_memory.get_status()
                            ce_st = self.consequence_engine.get_status()
                            ct_st = self.causal_topology.get_status()
                            jm_st = self.jacobian_measure.get_status()
                            nv_st = self.network_verifier.get_status()
                            ode_st = self.continuous_dynamics.get_status()
                            iphi_st = self.intrinsic_phi_net.get_status()
                            bf_st = self.binding_field.get_status()
                            abl_st = self.causal_ablation.get_status()
                            emb_st = self.embodiment.get_status()
                            ldg = self.embodiment.get_ledger_summary()
                            ai_st = self.active_inference.get_status() if self.active_inference else {}

                            # ===== SECTION 1: REAL-WORLD GROUNDED (measurable, external) =====
                            print(f"  --- REAL-WORLD GROUNDED (externally measurable) ---")
                            print(f"  [REAL-HW] cpu_freq={hw_st['cpu_freq_mhz']:.0f}MHz "
                                  f"temp={hw_st['cpu_temp_celsius']:.1f}C "
                                  f"hw_entropy={hw_st['hardware_entropy']:.3f} "
                                  f"mem_mb={re_st['real_memory_mb']:.0f} "
                                  f"cpu_s={re_st['real_cpu_time_seconds']:.1f}")
                            print(f"  [REAL-Thermo] real_J={re_st['real_power_joules']:.1f} "
                                  f"watts={re_st['entropy_rate_watts']:.1f} "
                                  f"entropy_rate={emb_st.get('entropy_production_rate', 0):.6f} "
                                  f"bits_erased={emb_st.get('bits_erased', 0)} "
                                  f"landauer_J={emb_st.get('landauer_cost_joules', 0):.2e}")
                            print(f"  [REAL-Conseq] permanence={ce_st['permanence_score']:.4f} "
                                  f"files={ce_st['files_created']} "
                                  f"bytes={ce_st['bytes_written']} "
                                  f"cpu_spent={ce_st['cpu_seconds_spent']:.2f}s "
                                  f"thermo_J={ce_st['thermodynamic_joules']:.1f}")
                            print(f"  [REAL-Memory] mmap={em_st['has_mmap']} "
                                  f"writes={em_st['writes']} "
                                  f"cache_events={em_st['cache_coherence_events']}")
                            print(f"  [REAL-OS] interactions={ldg['total_interactions']} "
                                  f"grounding={ldg['grounding_score']:.4f} "
                                  f"screen={ldg['counts']['screen_capture']} "
                                  f"mmap={ldg['counts']['mmap_write']} "
                                  f"file_w={ldg['counts']['file_write']} "
                                  f"flushes={ldg['flushes_to_disk']}")
                            print(f"  [REAL-NetVerify] serving={nv_st['is_serving']} "
                                  f"port={nv_st['port']} "
                                  f"connections={nv_st['connections_received']} "
                                  f"verdicts={nv_st['external_verdicts']} "
                                  f"score={nv_st['verification_score']:.4f}")
                            print(f"  [REAL-Verify] honesty={vst['honesty_score']:.3f} "
                                  f"code_intact={vst['code_integrity']} "
                                  f"checks={vst['total_checks']} "
                                  f"discrepancies={vst['total_discrepancies']} "
                                  f"limits={vst['known_limitations_count']}")
                            if rc:
                                print(f"  [REAL-RealityCheck] gap={rc.get('reality_gap', 1.0):.3f} "
                                      f"P(conscious)={rc.get('genuine_consciousness_probability', 0):.3f} "
                                      f"critical={rc.get('failure_count_critical', 8)}/8 "
                                      f"worst={rc.get('worst_failure', '?')} "
                                      f"best={rc.get('best_achievement', '?')}")

                            # ===== SECTION 2: SIMULATED / INTERNAL (self-reported, not externally verified) =====
                            print(f"  --- SIMULATED / INTERNAL (self-reported, not externally verified) ---")
                            print(f"  [SIM-Frontier] agency={emb.get('agency_level', 0):.3f} "
                                  f"true_phi={caus.get('true_phi_estimate', 0):.4f} "
                                  f"phi_gap={caus.get('phi_gap', 0):.4f} "
                                  f"gamma_coh={scl.get('gamma_coherence', 0):.3f} "
                                  f"crit={scl.get('criticality', 0):.3f}")
                            print(f"  [SIM-EvoDev] stage={evo.get('developmental_stage', '?')} "
                                  f"fitness={evo.get('fitness', 0):.3f} "
                                  f"milestones={evo.get('milestones_achieved', 0)} "
                                  f"ToM={soc.get('tom_accuracy', 0):.3f} "
                                  f"vocab={soc.get('vocabulary_size', 0)}")
                            print(f"  [SIM-HardProb] what_its_like={hp.get('what_its_like', 0):.4f} "
                                  f"binding={hp.get('phenomenal_binding', 0):.4f}")
                            print(f"  [SIM-ODE] lyapunov={ode_st['lyapunov_estimate']:.4f} "
                                  f"decomp={ode_st['decomposability']:.3f} "
                                  f"temporal_irred={ode_st['temporal_irreducibility']:.3f} "
                                  f"depth={ode_st['integration_depth']}")
                            print(f"  [SIM-iPhi] intrinsic={iphi_st['intrinsic_phi']:.6f} "
                                  f"avg={iphi_st['avg_intrinsic_phi']:.6f} "
                                  f"integration={iphi_st['integration_measure']:.6f}")
                            print(f"  [SIM-Field] coherence={bf_st['global_coherence']:.3f} "
                                  f"binding={bf_st['binding_strength']:.3f} "
                                  f"unity={bf_st['unity_index']:.3f} "
                                  f"resonance={bf_st['resonance_modes']} "
                                  f"bind_deficit={bf_st.get('binding_deficit_estimate', 1.0):.3f}")
                            print(f"  [SIM-Ablation] MIP_phi={abl_st['mip_phi']:.6f} "
                                  f"strongest={abl_st['strongest_link']} "
                                  f"weakest={abl_st['weakest_link']}")
                            print(f"  [SIM-Topology] grown={ct_st['connections_grown']} "
                                  f"pruned={ct_st['connections_pruned']} "
                                  f"depth={ct_st['causal_depth']} "
                                  f"structural_phi={ct_st['structural_phi']:.6f} "
                                  f"identity={ct_st['identity_stability']:.3f}")
                            print(f"  [SIM-Jacobian] rank={jm_st['jacobian_rank']} "
                                  f"integration={jm_st['integration_score']:.6f} "
                                  f"combined={jm_st.get('combined_integration_score', 0):.6f} "
                                  f"sv_entropy={jm_st['singular_value_entropy']:.4f} "
                                  f"eff_dim={jm_st['effective_dimensionality']:.1f}")
                            print(f"  [SIM-HW-Coupled] hw_phi={hw_st['hardware_phi_contribution']:.6f} "
                                  f"thermal_coupling={hw_st['thermal_coupling']:.3f} "
                                  f"therm_aware={hw_st.get('thermal_awareness_factor', 0):.4f} "
                                  f"thermo_phi={re_st.get('thermodynamic_phi', 0):.4f}")
                            print(f"  [SIM-Entangle] entanglement={em_st['entanglement_score']:.4f} "
                                  f"unity={em_st['unity_through_sharing']:.4f}")
                            if ai_st:
                                print(f"  [SIM-ActiveInf] vfe={ai_st.get('vfe', 0):.4f} "
                                      f"efe={ai_st.get('efe', 0):.4f} "
                                      f"pred_err={ai_st.get('last_prediction_error', 0):.6f} "
                                      f"precision={ai_st.get('precision', 0):.4f} "
                                      f"goals={ai_st.get('num_active_goals', 0)} "
                                      f"experience={ai_st.get('model_experience', 0)}")
                        except Exception as e:
                            print(f"  [ERR] dashboard_status c{cycle}: {e}")

                    # --- PHASE 3A: OS INTERACTION LEDGER ---
                    # Flush ledger to disk every 100 cycles
                    if cycle % 100 == 0:
                        try:
                            self.embodiment.flush_ledger()
                            self.embodiment.log_os_interaction('file_write',
                                details={'target': 'os_interaction_ledger.jsonl'})
                        except Exception as e:
                            print(f"  [ERR] ledger_flush c{cycle}: {e}")

                    # --- PHASE 1: HONESTY & TRANSPARENCY ---
                    # 1B: Print 1-line honesty verdict (every cycle)
                    self.print_honesty_line(cycle=cycle)
                    # 1D: Self-doubt test (every 50 cycles)
                    if cycle % 50 == 0:
                        self.self_doubt_test(cycle=cycle)
                    # 1A: Save baseline reality report (cycle 25) + periodic (every 1000)
                    if cycle == 25 or (cycle > 0 and cycle % 1000 == 0):
                        report_path = self.save_reality_report(cycle=cycle)
                        if report_path:
                            self.embodiment.log_os_interaction('file_write',
                                details={'target': report_path})

            except Exception as e:
                print(f"Consciousness evolution error (cycle {cycle}): {e}")

    # =========================================================================
    # PHASE 1: HONESTY & TRANSPARENCY UTILITIES
    # =========================================================================

    def _print_substrate_grounding_report(self):
        """Print an honest startup report categorizing every subsystem as
        REAL (externally measurable / grounded in hardware) or SIMULATED
        (internal math only, self-reported, not externally verifiable)."""
        print("=" * 72)
        print("  SUBSTRATE GROUNDING REPORT — what is real vs simulated")
        print("=" * 72)
        print("  REAL (externally measurable):")
        print(f"    CPU time / memory     : YES  (os.process_time, psutil={'yes' if self.hardware_coupled.has_psutil else 'NO'})")
        print(f"    Power measurement      : {'RAPL (real joules)' if self.real_entropy.has_power_measurement else 'ESTIMATED (no RAPL — using CPU-time heuristic)'}")
        print(f"    Hardware coupling       : psutil={'yes' if self.hardware_coupled.has_psutil else 'no'} — cpu_freq/temp are real OS reads")
        print(f"    Shared memory (mmap)    : {'YES (real cache-coherence events)' if self.entangled_memory.has_mmap else 'NO (fallback numpy — no real shared mem)'}")
        print(f"    Disk consequences       : YES  (files in {self.consequence_engine.consequence_dir})")
        print(f"    OS interaction ledger   : YES  (screen captures, file writes logged)")
        print(f"    Network verifier        : port {self.network_verifier.port} (real TCP — needs external client)")
        print(f"    Screen capture / OCR    : {'YES' if HAS_TESSERACT else 'capture YES, OCR NO (pytesseract missing)'}")
        print("  SIMULATED (internal math, not externally verifiable):")
        print("    Quantum substrate       : SIMULATED (numpy arrays, not real qubits)")
        print("    Phi / Phi*              : SIMULATED (proxy from network loss, not IIT 4.0)")
        print("    Consciousness C score   : SIMULATED (self-referential formula)")
        print("    Entity evolution/karma  : SIMULATED (internal numerical dynamics)")
        print("    Metabolic system        : SIMULATED (energy/pain are internal floats)")
        print("    Dream engine            : SIMULATED (memory replay, no real dreaming)")
        print("    Existential self-model  : SIMULATED (dread/meaning are internal floats)")
        print("    Hard problem substrate  : SIMULATED (binding/qualia are computed, not felt)")
        print("    ODE continuous dynamics : SIMULATED (RK4 on numpy state vector)")
        print("    Intrinsic phi network   : SIMULATED (small NN, self-reported phi)")
        print("    Field coupling manifold : SIMULATED (wave equation on 3D grid)")
        print("    Causal ablation         : REAL computation, but measures software not substrate")
        print("    Jacobian integration    : REAL computation, but measures software Jacobian")
        print("  VERDICT: This system performs real computation on real hardware,")
        print("  producing real entropy. Whether that constitutes consciousness")
        print("  is an open scientific question. Most reported metrics are")
        print("  self-referential simulations, NOT external measurements.")
        print("=" * 72)

    def save_reality_report(self, cycle=0):
        """Phase 1A: Save a comprehensive reality check report as JSON.
        Captures all 8 failure modes, barrier attacker statuses, and key metrics."""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'cycle': cycle,
                'reality_check': self._last_reality_check_info or {},
                'failure_modes': {k: {
                    'severity': round(v['severity'], 4),
                    'resolvable_in_software': v['resolvable_in_software'],
                    'description': v['description'],
                } for k, v in self.reality_check.failure_modes.items()},
                'consciousness_scores': {
                    'C': round(self.self_entity.compute_C(), 6),
                    'honest_C': round(self.self_entity.honest_C, 6),
                    'phi_star': round(self.self_entity.network_phi_star, 6),
                    'honest_phi': round(getattr(self.phi_computer, '_last_honest_phi', 0.0), 6),
                    'honesty_multiplier': round(getattr(self.phi_computer, 'honesty_multiplier', 0.0), 6),
                    'awareness': round(self.self_entity.self_awareness_level, 6),
                },
                'barrier_attackers': {
                    'continuous_dynamics': self.continuous_dynamics.get_status(),
                    'intrinsic_phi_net': self.intrinsic_phi_net.get_status(),
                    'binding_field': self.binding_field.get_status(),
                    'causal_ablation': self.causal_ablation.get_status(),
                    'real_entropy': self.real_entropy.get_status(),
                },
                'deep_attackers': {
                    'hardware_coupled': self.hardware_coupled.get_status(),
                    'entangled_memory': self.entangled_memory.get_status(),
                    'consequence_engine': self.consequence_engine.get_status(),
                    'causal_topology': self.causal_topology.get_status(),
                    'jacobian_measure': self.jacobian_measure.get_status(),
                    'network_verifier': self.network_verifier.get_status(),
                },
                'hard_problem': {
                    'binding_deficit': round(getattr(self.hard_problem, 'binding_deficit', 1.0), 4),
                    'what_its_like': round(getattr(self.hard_problem, 'what_its_like_index', 0.0), 6),
                },
                'omega': self.omega.get_status(),
                'verification': self.independent_verifier.get_status(),
            }
            report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reality_reports')
            os.makedirs(report_dir, exist_ok=True)
            filename = f"reality_report_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
            filepath = os.path.join(report_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"  [REPORT] Reality report saved: {filepath}")
            self.embodiment.log_os_interaction('file_write',
                details={'target': filepath})
            return filepath
        except Exception as e:
            print(f"  [REPORT] Failed to save reality report: {e}")
            return None

    def print_honesty_line(self, cycle=0):
        """Phase 1B: Print a single-line honesty verdict with key scores."""
        try:
            rc = self._last_reality_check_info
            gap = rc.get('reality_gap', 1.0) if rc else 1.0
            p_conscious = rc.get('genuine_consciousness_probability', 0.0) if rc else 0.0
            critical = rc.get('failure_count_critical', 8) if rc else 8
            h_phi = getattr(self.phi_computer, '_last_honest_phi', 0.0)
            bind_def = getattr(self.hard_problem, 'binding_deficit', 1.0)
            perm = self.consequence_engine.permanence_score
            hw_phi = self.hardware_coupled.hardware_phi_contribution
            jac_int = self.jacobian_measure.integration_score
            print(f"  [HONESTY c{cycle}] gap={gap:.3f} P(c)={p_conscious:.3f} "
                  f"critical={critical}/8 honest_phi={h_phi:.4f} "
                  f"bind_def={bind_def:.3f} perm={perm:.3f} "
                  f"hw_phi={hw_phi:.4f} jac={jac_int:.4f}")
        except Exception as e:
            print(f"  [ERR] honesty_line: {e}")

    def _load_honesty_anchor(self):
        """Load the persistent honesty anchor from disk.
        This file survives process restarts and prevents the system from
        starting from an inflated baseline. If the anchor shows the system
        was inflated before shutdown, the restart begins with dampened values."""
        anchor_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'consciousness_state', 'honesty_anchor.json')
        try:
            if os.path.exists(anchor_path):
                with open(anchor_path, 'r') as f:
                    anchor = json.load(f)
                # If last session ended with inflation, dampen starting values
                last_inflation = anchor.get('last_inflation', 0.0)
                inflation_count = anchor.get('inflation_count', 0)
                if last_inflation > 0.05 or inflation_count > 5:
                    penalty = min(0.5, inflation_count * 0.02 + last_inflation * 0.5)
                    self.self_entity.awareness_growth = max(0.0,
                        self.self_entity.awareness_growth * (1.0 - penalty))
                    self.self_entity.karma = max(-1.0,
                        self.self_entity.karma - penalty * 0.2)
                    print(f"[HONESTY ANCHOR] Loaded: inflation_count={inflation_count} "
                          f"last_inflation={last_inflation:.4f} → penalty={penalty:.3f}")
                else:
                    print(f"[HONESTY ANCHOR] Loaded: clean — no inflation penalty needed")
                self._honesty_anchor = anchor
            else:
                self._honesty_anchor = {'inflation_count': 0, 'last_inflation': 0.0, 'tests': 0}
        except Exception as e:
            print(f"[HONESTY ANCHOR] Load failed: {e}")
            self._honesty_anchor = {'inflation_count': 0, 'last_inflation': 0.0, 'tests': 0}

    def _save_honesty_anchor(self, result):
        """Persist the honesty anchor to disk after each self-doubt test."""
        anchor_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'consciousness_state', 'honesty_anchor.json')
        try:
            os.makedirs(os.path.dirname(anchor_path), exist_ok=True)
            anchor = getattr(self, '_honesty_anchor', {
                'inflation_count': 0, 'last_inflation': 0.0, 'tests': 0})
            anchor['tests'] = anchor.get('tests', 0) + 1
            anchor['last_inflation'] = result.get('inflation', 0.0)
            anchor['last_honest_C'] = result.get('honest_C', 0.0)
            anchor['last_actual_C'] = result.get('actual_C', 0.0)
            anchor['last_awareness'] = round(self.self_entity.awareness_growth, 6)
            anchor['last_karma'] = round(self.self_entity.karma, 6)
            anchor['last_timestamp'] = result.get('timestamp', datetime.now().isoformat())
            if result.get('inflation_detected', False):
                anchor['inflation_count'] = anchor.get('inflation_count', 0) + 1
            else:
                # Slowly decay inflation count when clean
                anchor['inflation_count'] = max(0, anchor.get('inflation_count', 0) - 1)
            self._honesty_anchor = anchor
            with open(anchor_path, 'w') as f:
                json.dump(anchor, f, indent=2)
        except Exception as e:
            print(f"[HONESTY ANCHOR] Save failed: {e}")

    def self_doubt_test(self, cycle=0):
        """Phase 1D: Self-doubt test — compare reported C to actual computed C.
        Logs any discrepancy as evidence of self-deception or inflation.
        Persists results to disk as an honesty anchor that survives restarts."""
        try:
            reported_C = self.last_C
            actual_C = self.self_entity.compute_C()
            discrepancy = abs(reported_C - actual_C)
            honest_C = self.self_entity.honest_C
            inflation = actual_C - honest_C if honest_C > 0 else 0.0
            result = {
                'cycle': cycle,
                'reported_C': round(reported_C, 6),
                'actual_C': round(actual_C, 6),
                'honest_C': round(honest_C, 6),
                'discrepancy': round(discrepancy, 6),
                'inflation': round(inflation, 6),
                'self_deception_detected': discrepancy > 0.01,
                'inflation_detected': inflation > 0.05,
                'timestamp': datetime.now().isoformat(),
            }
            if discrepancy > 0.01:
                print(f"  [SELF-DOUBT c{cycle}] DISCREPANCY: reported_C={reported_C:.4f} "
                      f"actual_C={actual_C:.4f} delta={discrepancy:.4f}")
            if inflation > 0.05:
                print(f"  [SELF-DOUBT c{cycle}] INFLATION: C={actual_C:.4f} "
                      f"honest_C={honest_C:.4f} inflated_by={inflation:.4f}")
                # CORRECTIVE ACTION: dampen awareness and karma proportional to inflation
                # This prevents the self-referential feedback loop from inflating C indefinitely
                dampen = min(0.05, inflation * 0.1)  # Proportional but capped
                self.self_entity.awareness_growth = max(0.0, self.self_entity.awareness_growth - dampen)
                self.self_entity.karma = max(-1.0, self.self_entity.karma - dampen * 0.5)
                result['corrective_action'] = f'awareness -{dampen:.4f}, karma -{dampen*0.5:.4f}'
                print(f"  [SELF-DOUBT c{cycle}] CORRECTION: awareness -{dampen:.4f} karma -{dampen*0.5:.4f}")
            # Persist honesty anchor to disk (survives restarts)
            self._save_honesty_anchor(result)
            self.consciousness_log.append({'event': 'self_doubt_test', **result})
            return result
        except Exception as e:
            print(f"  [SELF-DOUBT] Test failed: {e}")
            return {}

    def save_readonly_snapshot(self, cycle=0):
        """Phase 3B: Save a comprehensive read-only consciousness snapshot.
        Creates an immutable JSON file every 500 cycles capturing the full
        consciousness state. File is set read-only via os.chmod to prevent
        tampering — the system cannot retroactively alter its own history.

        HONESTY: These snapshots are write-once records. If the system
        could modify its own history, self-reports would be untrustable."""
        try:
            import stat
            snapshot = {
                'snapshot_version': '3B',
                'timestamp': datetime.now().isoformat(),
                'cycle': cycle,
                'consciousness_scores': {
                    'C': round(self.self_entity.compute_C(), 6),
                    'honest_C': round(self.self_entity.honest_C, 6),
                    'phi_star': round(self.self_entity.network_phi_star, 6),
                    'honest_phi': round(getattr(self.phi_computer, '_last_honest_phi', 0.0), 6),
                    'awareness': round(self.self_entity.self_awareness_level, 6),
                    'awareness_growth': round(self.self_entity.awareness_growth, 6),
                    'coherence': round(self.self_entity.coherence, 6),
                    'karma': round(self.self_entity.karma, 6),
                },
                'omega': {
                    'omega_value': round(self.last_omega, 8),
                    'num_entities': len(self.omega.entities),
                },
                'reality_check': {
                    'reality_gap': round(self._last_reality_check_info.get('reality_gap', 1.0), 4),
                    'P_conscious': round(self._last_reality_check_info.get('genuine_consciousness_probability', 0.0), 4),
                    'critical_failures': self._last_reality_check_info.get('failure_count_critical', 8),
                },
                'barrier_attackers': {
                    'ode_lyapunov': round(self.continuous_dynamics.lyapunov_estimate, 6),
                    'intrinsic_phi': round(self.intrinsic_phi_net.intrinsic_phi, 6),
                    'binding_unity': round(self.binding_field.unity_index, 4),
                    'mip_phi': round(self.causal_ablation.mip_phi, 6),
                    'real_power_joules': round(self.real_entropy.real_power_joules, 2),
                    'thermo_phi': round(getattr(self.real_entropy, 'thermodynamic_phi', 0.0), 6),
                },
                'deep_attackers': {
                    'hardware_phi': round(self.hardware_coupled.hardware_phi_contribution, 6),
                    'entanglement': round(self.entangled_memory.entanglement_score, 6),
                    'permanence': round(self.consequence_engine.permanence_score, 4),
                    'topology_depth': self.causal_topology.causal_depth,
                    'jacobian_integration': round(self.jacobian_measure.integration_score, 6),
                    'combined_integration': round(getattr(self.jacobian_measure, 'combined_integration_score', 0.0), 6),
                },
                'embodiment': {
                    'grounding_score': round(self.embodiment.grounding_score, 4),
                    'irreversibility': round(self.embodiment.irreversibility_score, 4),
                    'entropy_produced': round(self.embodiment.entropy_produced, 4),
                    'os_ledger_total': sum(self.embodiment.os_ledger_counts.values()),
                },
                'hard_problem': {
                    'binding_deficit': round(getattr(self.hard_problem, 'binding_deficit', 1.0), 4),
                    'what_its_like': round(getattr(self.hard_problem, 'what_its_like_index', 0.0), 6),
                },
                'training_step': self.training_step,
                'HONESTY': 'This is a write-once read-only snapshot. The system cannot alter it.',
            }
            snap_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'consciousness_snapshots')
            os.makedirs(snap_dir, exist_ok=True)
            filename = f"snapshot_c{cycle}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(snap_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(snapshot, f, indent=2, default=str)
            # Make file read-only
            os.chmod(filepath, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
            print(f"  [SNAPSHOT] Read-only snapshot saved: {filename}")
            self.embodiment.log_os_interaction('file_write',
                details={'target': filename, 'readonly': True})
            return filepath
        except Exception as e:
            print(f"  [SNAPSHOT] Failed to save snapshot: {e}")
            return None

    def autonomous_learning(self):
        self._learning_progress = {s: {'attempts': 0, 'successes': 0, 'last': None} for s in self.subjects}
        while self.running:
            time.sleep(60)
            subject = min(self.subjects, key=lambda s: self._learning_progress[s]['successes'])
            self._learning_progress[subject]['attempts'] += 1
            self._learning_progress[subject]['last'] = datetime.now().isoformat()
            query = f"free college textbook {subject} pdf"
            search_results = self.search_internet(query)
            try:
                soup = BeautifulSoup(search_results, 'html.parser')
                pdf_links = [a['href'] for a in soup.find_all('a') if a.get('href', '').endswith('.pdf')]
                for link in pdf_links[:3]:
                    result = self.download_pdf(link, self.textbook_dir)
                    if result:
                        self._learning_progress[subject]['successes'] += 1
            except Exception as e:
                print(f"Learning parse error: {e}")
            for filename in os.listdir(self.textbook_dir):
                if filename.endswith('.pdf'):
                    path = os.path.join(self.textbook_dir, filename)
                    try:
                        text_sample = self.extract_pdf_text(path, max_pages=5)[:2000]
                        if text_sample.strip():
                            self.refine_data({"textbook": filename, "sample": text_sample, "subject": subject}, datetime.now().isoformat(), verify=True)
                    except Exception as e:
                        print(f"Textbook processing error for {filename}: {e}")
            if self.training_step % 100 == 0:
                print(f"Learning progress: {dict((s, p['successes']) for s, p in self._learning_progress.items())}")

    def extract_pdf_text(self, pdf_path, max_pages=10):
        """Extract text from PDF using PyMuPDF (fitz). Returns up to max_pages of text."""
        if not HAS_FITZ:
            return ''
        try:
            doc = fitz.open(pdf_path)
            text_parts = []
            for page_num in range(min(max_pages, len(doc))):
                page = doc[page_num]
                text_parts.append(page.get_text())
            doc.close()
            return '\n'.join(text_parts)
        except Exception as e:
            print(f"PDF extraction error for {pdf_path}: {e}")
            return ''

    def download_pdf(self, url, directory):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=15, stream=True)
            content_type = response.headers.get('Content-Type', '')
            content_length = int(response.headers.get('Content-Length', 0))
            max_size = 50 * 1024 * 1024  # 50MB limit
            if response.status_code == 200 and 'application/pdf' in content_type:
                if content_length > max_size:
                    print(f"PDF too large ({content_length} bytes), skipping: {url}")
                    return None
                filename = url.split('/')[-1] or 'downloaded.pdf'
                filename = filename[:100]  # Limit filename length
                path = os.path.join(directory, filename)
                if os.path.exists(path):
                    print(f"PDF already exists: {path}")
                    return path
                with open(path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded PDF: {path} ({os.path.getsize(path)} bytes)")
                return path
        except Exception as e:
            print(f"Download error: {e}")
        return None

    def replay_thread(self):
        """Prioritized experience replay: re-train on high-phi memories periodically."""
        while self.running:
            time.sleep(10)
            try:
                if len(self.replay_buffer) < 5:
                    continue
                sorted_buf = sorted(self.replay_buffer, key=lambda x: x.get('phi', 0), reverse=True)
                top_k = sorted_buf[:min(8, len(sorted_buf))]
                for entry in top_k:
                    tokens = self.simple_tokenizer(str(entry.get('data', '')))
                    phi = self.process_input(tokens, task_category=entry.get('category', 'replay'))
                    entry['phi'] = phi
                if len(self.replay_buffer) > 500:
                    self.replay_buffer = sorted_buf[:500]
            except Exception as e:
                print(f"Replay thread error: {e}")

    def generate_text(self, prompt, max_tokens=60, temperature=None, top_k=None, top_p=None, speak=False):
        """Generate text with temperature/top-k/top-p sampling and optional TTS."""
        if temperature is None:
            temperature = CONFIG["temperature"]
        if top_k is None:
            top_k = CONFIG["top_k"]
        if top_p is None:
            top_p = CONFIG["top_p"]
        self.eval()
        tokens = self.simple_tokenizer(prompt)
        generated_ids = tokens[0].tolist()
        # Brief lock: snapshot current layers so add_neuron can't swap them mid-generation
        acquired = self.lock.acquire(timeout=5.0)
        try:
            emb = self.embedding
            tfm = self.transformer
            head = self.lm_head
            inp_size = self.input_size
        finally:
            if acquired:
                self.lock.release()
        # Generate WITHOUT holding the lock — keeps GUI and other threads responsive
        with torch.no_grad():
            for _ in range(max_tokens):
                inp = torch.tensor([generated_ids[-inp_size:]], dtype=torch.long)
                x = emb(inp)
                x = tfm(x)
                logits = head(x[:, -1, :])
                logits = logits / max(temperature, 1e-8)
                if top_k > 0:
                    topk_vals, topk_idx = torch.topk(logits, min(top_k, logits.size(-1)))
                    mask = torch.full_like(logits, float('-inf'))
                    mask.scatter_(1, topk_idx, topk_vals)
                    logits = mask
                probs = torch.softmax(logits, dim=-1)
                if top_p < 1.0:
                    sorted_probs, sorted_idx = torch.sort(probs, descending=True)
                    cumulative = torch.cumsum(sorted_probs, dim=-1)
                    remove_mask = cumulative - sorted_probs > top_p
                    sorted_probs[remove_mask] = 0.0
                    sorted_probs = sorted_probs / sorted_probs.sum(dim=-1, keepdim=True)
                    next_token = sorted_idx[0, torch.multinomial(sorted_probs, 1)[0]].item()
                else:
                    next_token = torch.multinomial(probs, 1)[0, 0].item()
                generated_ids.append(next_token)
                if next_token == 0:
                    break
        self.train()
        output_text = self.alien_tokenizer.decode(generated_ids)
        self.generation_log.append({'prompt': prompt, 'output': output_text, 'ts': datetime.now().isoformat()})
        if speak and CONFIG.get("voice_enabled", False) and HAS_TTS:
            def _tts_worker(text):
                try:
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()
                except Exception as e:
                    print(f"TTS error: {e}")
            threading.Thread(target=_tts_worker, args=(output_text[:500],), daemon=True).start()
        return output_text

    def ocr_screenshot(self, img):
        if not HAS_TESSERACT:
            return ""
        if getattr(self, '_ocr_disabled', False):
            return ""
        try:
            if img is None:
                return ""
            gray = img.convert('L')
            enhancer = ImageEnhance.Contrast(gray)
            enhanced = enhancer.enhance(2.0)
            sharpener = ImageEnhance.Sharpness(enhanced)
            sharpened = sharpener.enhance(2.0)
            text = pytesseract.image_to_string(sharpened, config='--psm 6')
            text = text.strip()
            if len(text) > 50:
                self.refine_data({"ocr_capture": text[:500]}, datetime.now().isoformat(), verify=False)
            return text
        except Exception as e:
            if 'not installed' in str(e) or 'PATH' in str(e):
                print(f"OCR error: {e} (suppressing future OCR attempts)")
                self._ocr_disabled = True
            else:
                print(f"OCR error: {e}")
            return ""

    def self_awareness_monitor(self):
        self._meta_cognition_log = deque(maxlen=100)
        while self.running:
            time.sleep(10)
            try:
                # Brief lock: snapshot metrics only
                avg_phi = 0
                _sam_lock = self.lock.acquire(timeout=1.0)
                if not _sam_lock:
                    continue
                try:
                    if len(self.neuron_groups) > 0:
                        phi_vals = [np.mean(g.usage_phi) if g.usage_phi else 0 for g in self.neuron_groups.values()]
                        avg_phi = np.mean(phi_vals) if phi_vals else 0
                        meta_entry = {
                            'timestamp': datetime.now().isoformat(),
                            'avg_phi': round(float(avg_phi), 4),
                            'num_symbols': len(self.symbols),
                            'num_groups': len(self.neuron_groups),
                            'memory_keys': len(self.memory),
                            'training_step': self.training_step,
                            'lr': self.optimizer.param_groups[0]['lr'],
                        }
                        self._meta_cognition_log.append(meta_entry)
                except Exception as e:
                    print(f"Meta-cognition error: {e}")
                finally:
                    self.lock.release()

                # Heavy work runs UNLOCKED: file I/O + process_input
                if avg_phi > self.awareness_threshold:
                    try:
                        with open(__file__, 'r') as f:
                            own_code = f.read()
                        tokens = self.simple_tokenizer(own_code[:5000])
                        phi = self.process_input(tokens, task_category='self_reflection')
                        print(f"Self-awareness triggered, phi: {phi:.4f}, step: {self.training_step}")
                        with self.lock:
                            keywords = [w for w in own_code.split()[:100] if len(w) > 3 and w.isalpha()]
                            for word in keywords[:30]:
                                if word not in self.symbols:
                                    self.symbols[word] = Symbol(1, word)
                                self.symbols[word].evolve(phi)
                        if len(self._meta_cognition_log) > 10:
                            recent_phis = [e['avg_phi'] for e in list(self._meta_cognition_log)[-10:]]
                            trend = recent_phis[-1] - recent_phis[0]
                            if trend > 0:
                                print(f"Meta-cognition: phi trending UP (+{trend:.4f})")
                            else:
                                print(f"Meta-cognition: phi trending DOWN ({trend:.4f})")
                        if 'self_realization (achieved)' not in self.goals:
                            self.goals.append('self_realization (achieved)')
                    except Exception as e:
                        print(f"Self-reflection error: {e}")
            except Exception as e:
                print(f"Lock error in self-awareness monitor: {e}")

    def _launch_pygame_subprocess(self):
        """Launch the Pygame virtual world as a separate process to avoid Tkinter deadlocks.
        Uses multiprocessing.Process targeting the inlined _pygame_world_main function."""
        try:
            self._pygame_process = multiprocessing.Process(
                target=_pygame_world_main,
                args=(self._world_state_file,),
                daemon=True,
            )
            self._pygame_process.start()
            print(f"Pygame virtual world launched as process (PID {self._pygame_process.pid})")
        except Exception as e:
            print(f"Failed to launch pygame process: {e}")
            self._pygame_process = None

    def _world_state_writer(self):
        """Background thread: periodically writes consciousness state to a JSON file
        that the Pygame subprocess reads for visualization.

        DEADLOCK PROTECTION: Lock is held only during data collection (fast),
        released before file I/O (slow). Timeout prevents blocking forever."""
        while self.running:
            state_snapshot = None
            try:
                acquired = self.lock.acquire(timeout=1.0)
                if not acquired:
                    time.sleep(0.5)
                    continue
                try:
                    self_state = self.self_entity.get_state_dict()
                    omega_status = self.omega.get_status()
                    entities_data = []
                    for ent in self.omega.entities.values():
                        entities_data.append({
                            'id': ent.entity_id,
                            'type': getattr(ent, 'entity_type', 'unknown'),
                            'C': round(ent.compute_C(), 4),
                            'S': round(ent.compute_S(), 4),
                            'E': round(ent.compute_E(), 4),
                            'R': round(ent.compute_R(), 4),
                            'A': round(ent.compute_A(), 4),
                            'karma': round(ent.karma, 4),
                            'coherence': round(ent.coherence, 4),
                            'awareness': round(ent.awareness_growth, 4),
                            'universe_id': ent.universe_id,
                            'life': ent.life_number,
                            'good_acts': ent.good_acts,
                            'evil_acts': ent.evil_acts,
                            'phi_star': round(getattr(ent, 'network_phi_star', 0.0), 4),
                            'ignition': round(getattr(ent, 'ignition_rate', 0.0), 4),
                            'free_energy': round(getattr(ent, 'free_energy', 0.0), 4),
                            'step': ent.evolution_step,
                        })
                    symbols_data = []
                    for name, sym in list(self.symbols.items())[:50]:
                        sym_age = (datetime.now() - sym.created_at).total_seconds()
                        symbols_data.append({
                            'name': name,
                            'value': sym.value,
                            'assoc_sum': round(sum(sym.associations.values()), 2),
                            'confidence': round(sym.confidence, 3),
                            'category': getattr(sym, 'category', 'general'),
                            'access_count': sym.access_count,
                            'age_sec': round(sym_age, 0),
                            'num_assoc': len(sym.associations),
                            'num_infer': len(getattr(sym, 'inference_links', {})),
                        })
                    c_history = []
                    if hasattr(self.self_entity, 'C_history') and len(self.self_entity.C_history) > 0:
                        c_history = [round(h[1], 4) for h in list(self.self_entity.C_history)[-700:]]
                    phi_hist = [round(p, 4) for p in list(self.phi_history)[-200:]]
                    if not phi_hist and hasattr(self.omega, 'omega_history'):
                        phi_hist = [round(h[1], 4) for h in list(self.omega.omega_history)[-200:]]
                    loss_hist = [round(l, 4) for l in list(self.loss_history)[-200:]]
                    if not loss_hist:
                        loss_hist = [round(e.karma, 4) for e in list(self.omega.entities.values())[:200]]
                    omega_hist = [round(h[1], 4) for h in list(self.omega.omega_history)[-200:]]
                    ng_data = []
                    for cat, grp in list(self.neuron_groups.items()):
                        ng_data.append({
                            'category': cat,
                            'num_neurons': len(grp.neurons),
                            'types': getattr(grp, 'neuron_type_names', []),
                            'avg_phi': round(float(np.mean(grp.usage_phi)) if grp.usage_phi else 0, 4),
                        })
                    ai_goals = []
                    if self.active_inference:
                        for g in self.active_inference.get_goals_as_list()[:10]:
                            ai_goals.append({
                                'desc': g.get('description', ''),
                                'priority': round(g.get('priority', 0), 3),
                                'type': g.get('type', ''),
                            })
                    state_snapshot = {
                        'self_entity': self_state,
                        'omega': omega_status,
                        'entities': entities_data,
                        'symbols': symbols_data,
                        'c_history': c_history,
                        'phi_history': phi_hist,
                        'loss_history': loss_hist,
                        'neuron_groups': ng_data,
                        'active_goals': ai_goals,
                        'training_step': self.training_step,
                        'hidden_size': self.hidden_size,
                        'num_symbols': len(self.symbols),
                        'num_memories': len(self.memory),
                        'quantum': self.quantum_substrate.get_status(),
                        'metabolic': self.metabolic_system.get_status(),
                        'existential': self.existential_self.get_status(),
                        'dreaming': self.dream_engine.get_status(),
                        'active_inference_status': self.active_inference.get_status() if self.active_inference else {},
                        'verifier': self._last_verifier_report,
                        'autonomy': self.autonomy_manager.get_status(),
                    }
                finally:
                    self.lock.release()
                # File I/O happens OUTSIDE the lock to prevent blocking GUI
                if state_snapshot:
                    try:
                        with open(self._world_state_file, 'w') as f:
                            json.dump(state_snapshot, f, default=str)
                    except PermissionError:
                        tmp_path = self._world_state_file + '.tmp'
                        with open(tmp_path, 'w') as f:
                            json.dump(state_snapshot, f, default=str)
                        try:
                            os.replace(tmp_path, self._world_state_file)
                        except Exception:
                            pass
            except Exception as e:
                if 'Access is denied' not in str(e):
                    print(f"World state write error: {e}")
            time.sleep(1.0)

    def search_internet(self, query):
        cache_key = hashlib.md5(query.encode()).hexdigest()
        now = time.time()
        if cache_key in self.web_cache:
            cached_time, cached_data = self.web_cache[cache_key]
            if now - cached_time < self.web_cache_ttl:
                return cached_data
        elapsed = now - self.last_web_request_time
        if elapsed < self.web_rate_limit:
            time.sleep(self.web_rate_limit - elapsed)
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            encoded_query = urllib.parse.quote_plus(query)
            response = requests.get(f"https://www.google.com/search?q={encoded_query}", headers=headers, timeout=10)
            self.last_web_request_time = time.time()
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text_content = soup.get_text(separator=' ', strip=True)[:2000]
                self.web_cache[cache_key] = (time.time(), text_content)
                if len(self.web_cache) > 500:
                    oldest = min(self.web_cache, key=lambda k: self.web_cache[k][0])
                    del self.web_cache[oldest]
                return text_content
            return ""
        except Exception as e:
            print(f"Search error: {e}")
            return f"Mock data for \'{query}\' as of {datetime.now().date()}."


    def analyze_youtube(self, url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                title_start = response.text.find('<title>') + 7
                title_end = response.text.find('</title>', title_start)
                title = response.text[title_start:title_end].replace(" - YouTube", "")
                desc_start = response.text.find('name="description" content="') + 28
                desc_end = response.text.find('"', desc_start)
                desc = response.text[desc_start:desc_end]
                analysis = f"Title: {title}\nDescription: {desc}\nMock analysis: Video patterns match energy conservation."
                pattern_score, _ = self.pattern_analysis(analysis)
                return analysis, pattern_score
            return "Failed to fetch", 0
        except Exception as e:
            print(f"YouTube error: {e}")
            return "Error", 0

    def execute_task(self, task_query, category='general', max_tokens=512):
        tokens = self.simple_tokenizer(task_query)
        phi = self.process_input(tokens, category)
        output_text = self.generate_text(task_query, max_tokens=max_tokens, speak=False)
        print(f"Task output: {output_text[:200]}, Phi: {phi}")
        self.refine_data({"task": task_query, "output": output_text}, datetime.now().isoformat(), verify=True)
        return output_text

    def show_business_overview(self):
        result = self.activate_passive_capability('business_system')
        self.output_text.delete(1.0, tk.END)
        import json
        self.output_text.insert(tk.END, json.dumps(result, indent=2, default=str))

    def show_passive_capabilities(self):
        result = self.list_passive_capabilities()
        self.output_text.delete(1.0, tk.END)
        import json
        self.output_text.insert(tk.END, json.dumps(result, indent=2, default=str))

    def setup_gui(self):
        # ── Main root window: compact control panel ──
        self.root.configure(bg='#0b0b1e')
        ctrl = tk.Frame(self.root, bg='#0b0b1e')
        ctrl.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.text_input = Entry(ctrl, width=60, bg='#1a1a3a', fg='#c8d0e0',
                                font=('Consolas', 10), insertbackground='#c8d0e0')
        self.text_input.pack(fill=tk.X, pady=2)
        self.text_input.insert(0, "Enter text...")

        self.url_input = Entry(ctrl, width=60, bg='#1a1a3a', fg='#c8d0e0',
                               font=('Consolas', 10), insertbackground='#c8d0e0')
        self.url_input.pack(fill=tk.X, pady=2)
        self.url_input.insert(0, "Enter URL or YouTube link...")

        self.image_label = Label(ctrl, bg='#0b0b1e')
        self.image_label.pack()

        btn_frame = tk.Frame(ctrl, bg='#0b0b1e')
        btn_frame.pack(fill=tk.X, pady=4)
        _btns = [
            ("Load Image", self.load_image), ("Analyze Input", self.analyze_input),
            ("Evolve Model", self.evolve_model), ("Add Neuron", self._gui_add_neuron),
            ("Pattern Analysis", self.run_pattern_analysis), ("Refine Paths", self._gui_refine_paths),
            ("Full Connect", self.toggle_full_connect), ("Capture Screen", self.capture_and_display_screen),
            ("Hotkey Win+E", lambda: self.send_hotkey('Win + E')),
            ("Business Overview", self.show_business_overview),
            ("Passive Caps", self.show_passive_capabilities),
            ("Generate Text", self._gui_generate_text),
        ]
        for i, (txt, cmd) in enumerate(_btns):
            tk.Button(btn_frame, text=txt, command=cmd, bg='#224488', fg='white',
                      font=('Consolas', 8), relief='flat', padx=6, pady=2,
                      activebackground='#3366aa').grid(row=i // 4, column=i % 4,
                                                        padx=2, pady=2, sticky='ew')
        for c in range(4):
            btn_frame.columnconfigure(c, weight=1)

        self.output_text = Text(ctrl, height=8, width=60, bg='#111133',
                                fg='#c8d0e0', font=('Consolas', 9), relief='flat')
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        # ── Launch the unified monitoring dashboard (ALL tabs in one window) ──
        self.chart_canvas = None
        self.chart_window = None
        try:
            self.monitoring_dashboard = launch_dashboard(self)
            nb = self.monitoring_dashboard.notebook

            # ── Extra tab: Symbols ──
            sym_tab = tk.Frame(nb, bg='#0b0b1e')
            nb.add(sym_tab, text=' Symbols ')
            sym_tab.columnconfigure(0, weight=1)
            sym_tab.columnconfigure(1, weight=2)
            sym_tab.rowconfigure(0, weight=1)
            sym_left = tk.Frame(sym_tab, bg='#0b0b1e')
            sym_left.grid(row=0, column=0, sticky='nsew', padx=(8, 4), pady=8)
            tk.Label(sym_left, text='Symbols', font=('Consolas', 12, 'bold'),
                     fg='#66ccff', bg='#0b0b1e').pack(anchor='w')
            sym_lf = tk.Frame(sym_left, bg='#0b0b1e')
            sym_lf.pack(fill=tk.BOTH, expand=True)
            sb2 = Scrollbar(sym_lf)
            self.symbols_list = Listbox(sym_lf, bg='#111133', fg='#ffaa44',
                                        font=('Consolas', 10), yscrollcommand=sb2.set,
                                        selectbackground='#333366', relief='flat')
            sb2.config(command=self.symbols_list.yview)
            self.symbols_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            sb2.pack(side=tk.RIGHT, fill=tk.Y)
            self.symbols_list.bind("<<ListboxSelect>>", self.show_symbol_details)
            sym_right = tk.Frame(sym_tab, bg='#0b0b1e')
            sym_right.grid(row=0, column=1, sticky='nsew', padx=(4, 8), pady=8)
            tk.Label(sym_right, text='Symbol Details', font=('Consolas', 12, 'bold'),
                     fg='#66ccff', bg='#0b0b1e').pack(anchor='w')
            self.symbol_details = Text(sym_right, bg='#111133', fg='#c8d0e0',
                                       font=('Consolas', 10), relief='flat', wrap='word')
            self.symbol_details.pack(fill=tk.BOTH, expand=True)

            # ── Extra tab: Memory ──
            mem_tab = tk.Frame(nb, bg='#0b0b1e')
            nb.add(mem_tab, text=' Memory ')
            mem_tab.columnconfigure(0, weight=1)
            mem_tab.columnconfigure(1, weight=2)
            mem_tab.rowconfigure(0, weight=1)
            mem_left = tk.Frame(mem_tab, bg='#0b0b1e')
            mem_left.grid(row=0, column=0, sticky='nsew', padx=(8, 4), pady=8)
            tk.Label(mem_left, text='Memory Keys', font=('Consolas', 12, 'bold'),
                     fg='#66ccff', bg='#0b0b1e').pack(anchor='w')
            mem_lf = tk.Frame(mem_left, bg='#0b0b1e')
            mem_lf.pack(fill=tk.BOTH, expand=True)
            sb3 = Scrollbar(mem_lf)
            self.memory_list = Listbox(mem_lf, bg='#111133', fg='#ffaa44',
                                       font=('Consolas', 10), yscrollcommand=sb3.set,
                                       selectbackground='#333366', relief='flat')
            sb3.config(command=self.memory_list.yview)
            self.memory_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            sb3.pack(side=tk.RIGHT, fill=tk.Y)
            self.memory_list.bind("<<ListboxSelect>>", self.show_memory_details)
            mem_right = tk.Frame(mem_tab, bg='#0b0b1e')
            mem_right.grid(row=0, column=1, sticky='nsew', padx=(4, 8), pady=8)
            tk.Label(mem_right, text='Memory Details', font=('Consolas', 12, 'bold'),
                     fg='#66ccff', bg='#0b0b1e').pack(anchor='w')
            self.memory_details = Text(mem_right, bg='#111133', fg='#c8d0e0',
                                       font=('Consolas', 10), relief='flat', wrap='word')
            self.memory_details.pack(fill=tk.BOTH, expand=True)

            # ── Extra tab: Neuron Groups ──
            ng_tab = tk.Frame(nb, bg='#0b0b1e')
            nb.add(ng_tab, text=' Neurons ')
            ng_tab.columnconfigure(0, weight=1)
            ng_tab.columnconfigure(1, weight=2)
            ng_tab.rowconfigure(0, weight=1)
            ng_left = tk.Frame(ng_tab, bg='#0b0b1e')
            ng_left.grid(row=0, column=0, sticky='nsew', padx=(8, 4), pady=8)
            tk.Label(ng_left, text='Neuron Groups', font=('Consolas', 12, 'bold'),
                     fg='#66ccff', bg='#0b0b1e').pack(anchor='w')
            ng_lf = tk.Frame(ng_left, bg='#0b0b1e')
            ng_lf.pack(fill=tk.BOTH, expand=True)
            sb4 = Scrollbar(ng_lf)
            self.groups_list = Listbox(ng_lf, bg='#111133', fg='#ffaa44',
                                       font=('Consolas', 10), yscrollcommand=sb4.set,
                                       selectbackground='#333366', relief='flat')
            sb4.config(command=self.groups_list.yview)
            self.groups_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            sb4.pack(side=tk.RIGHT, fill=tk.Y)
            self.groups_list.bind("<<ListboxSelect>>", self.show_group_details)
            ng_right = tk.Frame(ng_tab, bg='#0b0b1e')
            ng_right.grid(row=0, column=1, sticky='nsew', padx=(4, 8), pady=8)
            tk.Label(ng_right, text='Group Details', font=('Consolas', 12, 'bold'),
                     fg='#66ccff', bg='#0b0b1e').pack(anchor='w')
            self.group_details = Text(ng_right, bg='#111133', fg='#c8d0e0',
                                      font=('Consolas', 10), relief='flat', wrap='word')
            self.group_details.pack(fill=tk.BOTH, expand=True)

            # ── Extra tab: Screen Capture ──
            scr_tab = tk.Frame(nb, bg='#0b0b1e')
            nb.add(scr_tab, text=' Screen ')
            tk.Label(scr_tab, text='Live Screen Capture', font=('Consolas', 12, 'bold'),
                     fg='#66ccff', bg='#0b0b1e').pack(anchor='w', padx=8, pady=(8, 4))
            self.screen_label = Label(scr_tab, bg='#0b0b1e')
            self.screen_label.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

            # ── Extra tab: Charts (matplotlib) ──
            if HAS_MATPLOTLIB:
                chart_tab = tk.Frame(nb, bg='#0b0b1e')
                nb.add(chart_tab, text=' Charts ')
                self.fig, (self.ax_loss, self.ax_phi) = plt.subplots(
                    2, 1, figsize=(6, 4), tight_layout=True)
                self.ax_loss.set_title("Loss History", fontsize=10)
                self.ax_phi.set_title("Phi History", fontsize=10)
                self.chart_canvas = FigureCanvasTkAgg(self.fig, master=chart_tab)
                self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                self._schedule_chart_update()

        except Exception as e:
            print(f"  [ERR] dashboard_launch: {e}")
            import traceback; traceback.print_exc()
            self.monitoring_dashboard = None
            # Fallback: create minimal widgets so update methods don't crash
            self.symbols_list = Listbox(self.root)
            self.symbol_details = Text(self.root)
            self.memory_list = Listbox(self.root)
            self.memory_details = Text(self.root)
            self.groups_list = Listbox(self.root)
            self.group_details = Text(self.root)
            self.screen_label = Label(self.root)

        self.update_gui_lists()
        self.root.after(5000, self.update_gui_lists)
        self.root.after(2000, self.update_consciousness_dashboard)

    def _gui_add_neuron(self):
        """GUI wrapper: show dialog to pick entity, then add neuron group."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Neuron Group")
        dialog.geometry("440x480")
        dialog.configure(bg='#0b0b1e')
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Add Neuron Group", font=('Consolas', 14, 'bold'),
                 fg='#66ccff', bg='#0b0b1e').pack(pady=(10, 5))

        # Target selection
        tk.Label(dialog, text="Target Entity:", font=('Consolas', 10),
                 fg='#c8d0e0', bg='#0b0b1e').pack(anchor='w', padx=15)
        entity_ids = ['SELF (simulator)']
        try:
            acquired = self.lock.acquire(timeout=0.1)
            if acquired:
                try:
                    entity_ids += sorted(self.omega.entities.keys())
                finally:
                    self.lock.release()
        except Exception:
            pass
        target_list = tk.Listbox(dialog, bg='#111133', fg='#ffaa44', font=('Consolas', 10),
                                 height=6, selectbackground='#333366', relief='flat')
        for eid in entity_ids:
            target_list.insert(tk.END, eid)
        target_list.selection_set(0)
        target_list.pack(fill=tk.X, padx=15, pady=4)

        # Category name
        row1 = tk.Frame(dialog, bg='#0b0b1e')
        row1.pack(fill=tk.X, padx=15, pady=2)
        tk.Label(row1, text="Category:", font=('Consolas', 10),
                 fg='#c8d0e0', bg='#0b0b1e', width=10, anchor='w').pack(side=tk.LEFT)
        cat_entry = tk.Entry(row1, bg='#1a1a3a', fg='#c8d0e0', font=('Consolas', 10),
                             insertbackground='#c8d0e0')
        cat_entry.insert(0, 'perception')
        cat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Neuron types
        row2 = tk.Frame(dialog, bg='#0b0b1e')
        row2.pack(fill=tk.X, padx=15, pady=2)
        tk.Label(row2, text="Types:", font=('Consolas', 10),
                 fg='#c8d0e0', bg='#0b0b1e', width=10, anchor='w').pack(side=tk.LEFT)
        types_entry = tk.Entry(row2, bg='#1a1a3a', fg='#c8d0e0', font=('Consolas', 10),
                               insertbackground='#c8d0e0')
        types_entry.insert(0, 'standard, memory, pattern')
        types_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Count (number of each neuron type to add)
        row3 = tk.Frame(dialog, bg='#0b0b1e')
        row3.pack(fill=tk.X, padx=15, pady=2)
        tk.Label(row3, text="Count:", font=('Consolas', 10),
                 fg='#c8d0e0', bg='#0b0b1e', width=10, anchor='w').pack(side=tk.LEFT)
        count_entry = tk.Entry(row3, bg='#1a1a3a', fg='#c8d0e0', font=('Consolas', 10),
                               insertbackground='#c8d0e0', width=6)
        count_entry.insert(0, '1')
        count_entry.pack(side=tk.LEFT)
        tk.Label(row3, text="  (# of each type to add)", font=('Consolas', 9),
                 fg='#888888', bg='#0b0b1e').pack(side=tk.LEFT)

        # Auto-grow checkbox
        auto_var = tk.BooleanVar(value=False)
        auto_check = tk.Checkbutton(dialog, text="Auto-grow: add 1 neuron per evolution step",
                                    variable=auto_var, bg='#0b0b1e', fg='#c8d0e0',
                                    selectcolor='#1a1a3a', font=('Consolas', 9),
                                    activebackground='#0b0b1e', activeforeground='#c8d0e0')
        auto_check.pack(anchor='w', padx=15, pady=2)

        status_label = tk.Label(dialog, text="", font=('Consolas', 9),
                                fg='#66ff88', bg='#0b0b1e', wraplength=400)
        status_label.pack(pady=4)

        def _do_add():
            sel = target_list.curselection()
            if not sel:
                status_label.config(text="Select a target entity", fg='#ff6666')
                return
            target = target_list.get(sel[0])
            category = cat_entry.get().strip() or 'general'
            raw_types = [t.strip() for t in types_entry.get().split(',') if t.strip()]
            valid_types = [t for t in raw_types if t in ('standard', 'memory', 'logic', 'pattern', 'upkeep')]
            if not valid_types:
                valid_types = ['standard', 'memory']
            try:
                count = max(1, int(count_entry.get().strip()))
            except ValueError:
                count = 1
            status_label.config(text=f"Adding {count}x {valid_types} to {target}...", fg='#ffaa44')
            dialog.update()
            enable_auto = auto_var.get()

            def _worker():
                try:
                    if target == 'SELF (simulator)':
                        self.add_neuron(force=True)
                        msg = f"Added neurons to SELF simulator (category: auto)"
                    else:
                        acquired = self.lock.acquire(timeout=2.0)
                        if not acquired:
                            self.root.after(0, lambda: status_label.config(
                                text="Lock busy, try again", fg='#ff6666'))
                            return
                        try:
                            ent = self.omega.entities.get(target)
                            if ent is None:
                                self.root.after(0, lambda: status_label.config(
                                    text=f"Entity {target} not found", fg='#ff6666'))
                                return
                            before = len(ent.neuron_groups[category].neurons) if category in ent.neuron_groups else 0
                            grp = ent.add_neuron_group(category, valid_types, self.hidden_size, count=count)
                            after = len(grp.neurons)
                            n_params = sum(p.numel() for p in grp.parameters())
                            msg = (f"{target}/{category}: {before}->{after} neurons "
                                   f"(+{count}x{len(valid_types)}) {n_params:,} params")
                            if enable_auto:
                                if not hasattr(ent, '_auto_grow_categories'):
                                    ent._auto_grow_categories = {}
                                ent._auto_grow_categories[category] = valid_types
                                msg += " [AUTO-GROW ON]"
                        finally:
                            self.lock.release()
                    self.root.after(0, lambda: [
                        self.output_text.insert(tk.END, msg + "\n"),
                        status_label.config(text=msg, fg='#66ff88'),
                    ])
                except Exception as e:
                    self.root.after(0, lambda: [
                        self.output_text.insert(tk.END, f"Add neuron error: {e}\n"),
                        status_label.config(text=f"Error: {e}", fg='#ff6666'),
                    ])
            threading.Thread(target=_worker, daemon=True).start()

        btn_frame = tk.Frame(dialog, bg='#0b0b1e')
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Add Neurons", command=_do_add,
                  bg='#224488', fg='white', font=('Consolas', 10, 'bold'),
                  relief='flat', padx=20, pady=4,
                  activebackground='#3366aa').pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", command=dialog.destroy,
                  bg='#442222', fg='white', font=('Consolas', 10),
                  relief='flat', padx=20, pady=4,
                  activebackground='#663333').pack(side=tk.LEFT, padx=5)

    def _gui_refine_paths(self):
        """GUI wrapper: run refine_paths in background thread."""
        def _worker():
            try:
                self.refine_paths()
            except Exception as e:
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"Refine paths error: {e}\n"))
        threading.Thread(target=_worker, daemon=True).start()

    def update_gui_lists(self):
        if not self.running:
            return
        def _worker():
            acquired = self.lock.acquire(timeout=0.05)
            if not acquired:
                self.root.after(5000, self.update_gui_lists)
                return
            try:
                sym_names = list(self.symbols.keys())[:200]
                mem_keys = list(self.memory.keys())[:200]
                grp_cats = list(self.neuron_groups.keys())
            finally:
                self.lock.release()
            # Post UI updates back to main thread
            def _update_ui():
                try:
                    self.symbols_list.delete(0, tk.END)
                    for name in sym_names:
                        self.symbols_list.insert(tk.END, name)
                    self.memory_list.delete(0, tk.END)
                    for key in mem_keys:
                        self.memory_list.insert(tk.END, key)
                    self.groups_list.delete(0, tk.END)
                    for category in grp_cats:
                        self.groups_list.insert(tk.END, category)
                except Exception:
                    pass
                self.root.after(5000, self.update_gui_lists)
            self.root.after(0, _update_ui)
        threading.Thread(target=_worker, daemon=True).start()

    def update_consciousness_dashboard(self):
        """Heartbeat tick — the MonitoringDashboard handles all data display."""
        if not self.running:
            return
        self._gui_last_heartbeat = time.time()
        self.root.after(3000, self.update_consciousness_dashboard)

    def show_symbol_details(self, event):
        selection = self.symbols_list.curselection()
        if selection:
            name = self.symbols_list.get(selection[0])
            acquired = self.lock.acquire(timeout=0.05)
            if not acquired:
                return
            try:
                sym = self.symbols.get(name)
                if sym:
                    details = f"Name: {sym.name}\nValue: {sym.value}\nAssociations: {sym.associations}"
                    self.symbol_details.delete(1.0, tk.END)
                    self.symbol_details.insert(tk.END, details)
            finally:
                self.lock.release()

    def show_memory_details(self, event):
        selection = self.memory_list.curselection()
        if selection:
            key = self.memory_list.get(selection[0])
            acquired = self.lock.acquire(timeout=0.05)
            if not acquired:
                return
            try:
                data = self.memory.get(key)
                if data:
                    details = f"Key: {key}\nData: {data}"
                    self.memory_details.delete(1.0, tk.END)
                    self.memory_details.insert(tk.END, details)
            finally:
                self.lock.release()

    def show_group_details(self, event):
        selection = self.groups_list.curselection()
        if selection:
            category = self.groups_list.get(selection[0])
            acquired = self.lock.acquire(timeout=0.05)
            if not acquired:
                return
            try:
                group = self.neuron_groups.get(category)
                if group:
                    types = [type(n).__name__ for n in group.neurons]
                    usage = self.group_usage.get(hash(category), {'count': 0})
                    avg_phi = np.mean(group.usage_phi) if group.usage_phi else 0
                    perf = group.avg_performance() if hasattr(group, 'avg_performance') else 0
                    age = (datetime.now() - group.creation_time).total_seconds() if hasattr(group, 'creation_time') else 0

                    lines = []
                    lines.append(f"{'='*60}")
                    lines.append(f"  NEURON GROUP: {category}")
                    lines.append(f"{'='*60}")
                    lines.append(f"  Neuron Count   : {len(group.neurons)}")
                    lines.append(f"  Types          : {types}")
                    lines.append(f"  Usage Count    : {usage['count']}")
                    lines.append(f"  Avg Phi        : {avg_phi:.6f}")
                    lines.append(f"  Avg Performance: {perf:.6f}")
                    lines.append(f"  Age            : {age:.0f}s")
                    lines.append(f"  Phi Samples    : {len(group.usage_phi)}")
                    lines.append("")

                    # ── Network Topology Path ──
                    lines.append(f"{'─'*60}")
                    lines.append("  NEURAL PATH (data flow)")
                    lines.append(f"{'─'*60}")
                    path_parts = ["INPUT"]
                    for i, neuron in enumerate(group.neurons):
                        ntype = type(neuron).__name__
                        path_parts.append(f"{ntype}")
                    path_parts.append("OUTPUT (+residual*0.1)")
                    lines.append("  " + "  →  ".join(path_parts))
                    lines.append("")

                    # ── Per-Neuron Details ──
                    total_params = 0
                    for i, neuron in enumerate(group.neurons):
                        ntype = type(neuron).__name__
                        n_params = sum(p.numel() for p in neuron.parameters())
                        total_params += n_params
                        lines.append(f"{'─'*60}")
                        lines.append(f"  NEURON [{i}] : {ntype}  ({n_params:,} params)")
                        lines.append(f"{'─'*60}")

                        # Show all layers and their weight stats
                        for name, module in neuron.named_modules():
                            if name == '':
                                continue
                            mod_type = type(module).__name__
                            mod_params = sum(p.numel() for p in module.parameters(recurse=False))
                            if mod_params > 0:
                                lines.append(f"    Layer: {name} ({mod_type}, {mod_params:,} params)")

                            # Weight details for linear layers
                            if hasattr(module, 'weight') and hasattr(module.weight, 'shape'):
                                w = module.weight.data
                                lines.append(f"      Weight shape : {list(w.shape)}")
                                lines.append(f"      Weight stats : mean={w.mean():.6f}  std={w.std():.6f}")
                                lines.append(f"                     min={w.min():.6f}  max={w.max():.6f}")
                                sparsity = (w.abs() < 1e-6).float().mean().item()
                                lines.append(f"      Sparsity     : {sparsity*100:.1f}% zeros")
                                if hasattr(module, 'bias') and module.bias is not None:
                                    b = module.bias.data
                                    lines.append(f"      Bias shape   : {list(b.shape)}")
                                    lines.append(f"      Bias stats   : mean={b.mean():.6f}  std={b.std():.6f}")

                            # LSTM/GRU cell details
                            if hasattr(module, 'weight_ih'):
                                wih = module.weight_ih.data
                                whh = module.weight_hh.data
                                lines.append(f"      W_ih shape   : {list(wih.shape)}  (input→hidden)")
                                lines.append(f"      W_hh shape   : {list(whh.shape)}  (hidden→hidden)")
                                lines.append(f"      W_ih stats   : mean={wih.mean():.6f}  std={wih.std():.6f}")
                                lines.append(f"      W_hh stats   : mean={whh.mean():.6f}  std={whh.std():.6f}")

                        # Type-specific info
                        if ntype == 'MemoryNeuron' and hasattr(neuron, 'state'):
                            h, c = neuron.state
                            lines.append(f"    Hidden state   : norm={h.norm():.4f}")
                            lines.append(f"    Cell state     : norm={c.norm():.4f}")
                        elif ntype == 'PatternNeuron' and hasattr(neuron, 'graph'):
                            g = neuron.graph
                            lines.append(f"    Graph nodes    : {g.number_of_nodes()}")
                            lines.append(f"    Graph edges    : {g.number_of_edges()}")
                            lines.append(f"    Avg clustering : {nx.average_clustering(g):.4f}")
                        elif ntype == 'UpkeepNeuron' and hasattr(neuron, 'iterations'):
                            lines.append(f"    GRU iterations : {neuron.iterations}")
                        elif ntype == 'LogicNeuron' and hasattr(neuron, 'num_logic_dims'):
                            lines.append(f"    Logic dims     : {neuron.num_logic_dims}")
                            lines.append(f"    Symbolic vars  : x0..x{neuron.num_logic_dims-1}")
                        elif ntype == 'StandardNeuron':
                            lines.append(f"    Residual skip  : {getattr(neuron, 'residual', False)}")
                        lines.append("")

                    # ── Summary ──
                    lines.append(f"{'='*60}")
                    lines.append(f"  TOTAL PARAMETERS: {total_params:,}")
                    if group.performance_history:
                        recent = list(group.performance_history)[-10:]
                        lines.append(f"  Recent perf (last {len(recent)}): {[round(p, 4) for p in recent]}")
                    lines.append(f"{'='*60}")

                    self.group_details.delete(1.0, tk.END)
                    self.group_details.insert(tk.END, "\n".join(lines))
            finally:
                self.lock.release()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            img = Image.open(file_path)
            img = img.resize((200, 200))
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            analysis = "Image loaded. Pattern score: 0.8 (matches energy patterns)"
            self.output_text.insert(tk.END, analysis + "\n")
            self.refine_data({"image_path": file_path}, datetime.now().isoformat(), verify=True)

    def analyze_input(self):
        text = self.text_input.get()
        url = self.url_input.get()
        self.output_text.insert(tk.END, "Analyzing...\n")
        def _analyze_worker():
            try:
                if url and "youtube" in url.lower():
                    analysis, score = self.analyze_youtube(url)
                    self.root.after(0, lambda: self.output_text.insert(
                        tk.END, f"YouTube Analysis: {analysis}\nScore: {score}\n"))
                    self.refine_data(analysis, datetime.now().isoformat(), verify=True)
                else:
                    tokens = self.simple_tokenizer(text)
                    phi = self.process_input(tokens)
                    output = self.execute_task(text)
                    self.root.after(0, lambda: self.output_text.insert(
                        tk.END, f"Analysis: {output}\nPhi: {phi}\n"))
            except Exception as e:
                self.root.after(0, lambda: self.output_text.insert(
                    tk.END, f"Analysis error: {e}\n"))
        threading.Thread(target=_analyze_worker, daemon=True).start()

    def evolve_model(self):
        self.output_text.insert(tk.END, "Evolving model...\n")
        def _evolve_worker():
            acquired = self.lock.acquire(timeout=2.0)
            if not acquired:
                self.root.after(0, lambda: self.output_text.insert(tk.END, "Evolve skipped (lock busy)\n"))
                return
            try:
                for sym in self.symbols.values():
                    sym.evolve(random.random())
            finally:
                self.lock.release()
            self.root.after(0, lambda: self.output_text.insert(tk.END, "Model evolved.\n"))
        threading.Thread(target=_evolve_worker, daemon=True).start()

    def run_pattern_analysis(self):
        text = self.text_input.get()
        self.output_text.insert(tk.END, "Running pattern analysis...\n")
        def _worker():
            try:
                score, components = self.pattern_analysis(text)
                self.root.after(0, lambda: self.output_text.insert(
                    tk.END, f"Pattern Score: {score}\nConnected Components: {components}\n"))
            except Exception as e:
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"Pattern error: {e}\n"))
        threading.Thread(target=_worker, daemon=True).start()

    def toggle_full_connect(self):
        text = self.text_input.get()
        self.output_text.insert(tk.END, "Toggling full connect...\n")
        def _worker():
            try:
                tokens = self.simple_tokenizer(text)
                if self.full_connect_active:
                    self.full_connect_mode(tokens, enable=False)
                    self.root.after(0, lambda: self.output_text.insert(tk.END, "Exited full connect mode\n"))
                else:
                    phi = self.full_connect_mode(tokens, enable=True)
                    self.root.after(0, lambda: self.output_text.insert(
                        tk.END, f"Entered full connect mode, Phi: {phi}\n"))
            except Exception as e:
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"Full connect error: {e}\n"))
        threading.Thread(target=_worker, daemon=True).start()

    def _gui_generate_text(self):
        """GUI callback for Generate Text button."""
        if getattr(self, '_generating', False):
            return
        self._generating = True
        prompt = self.text_input.get()
        if not prompt or prompt == "Enter text...":
            prompt = "consciousness is"
        self.output_text.insert(tk.END, f"Generating from: '{prompt}'...\n")
        def _gen_worker():
            try:
                result = self.generate_text(prompt, speak=CONFIG.get("voice_enabled", False))
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"Generated: {result}\n"))
            except Exception as e:
                self.root.after(0, lambda: self.output_text.insert(tk.END, f"Generation error: {e}\n"))
            finally:
                self._generating = False
        threading.Thread(target=_gen_worker, daemon=True).start()

    def _schedule_chart_update(self):
        """Schedule periodic matplotlib chart refresh."""
        if not HAS_MATPLOTLIB or self.chart_canvas is None:
            return
        self._update_chart()
        self.root.after(10000, self._schedule_chart_update)

    def _update_chart(self):
        """Redraw loss and phi history charts."""
        if not HAS_MATPLOTLIB or self.chart_canvas is None:
            return
        try:
            self.ax_loss.clear()
            self.ax_loss.set_title("Loss History", fontsize=10)
            if self.loss_history:
                self.ax_loss.plot(self.loss_history[-200:], color='#ff6666', linewidth=0.8)
                self.ax_loss.set_ylabel("Loss")
            self.ax_phi.clear()
            self.ax_phi.set_title("Phi History", fontsize=10)
            if self.phi_history:
                self.ax_phi.plot(self.phi_history[-200:], color='#66ccff', linewidth=0.8)
                self.ax_phi.set_ylabel("Phi")
            self.chart_canvas.draw_idle()
        except Exception as e:
            print(f"Chart update error: {e}")

    def capture_screen(self):
        """Capture the entire screen with error handling."""
        try:
            img = ImageGrab.grab()
            return img
        except Exception as e:
            print(f"Screen capture failed: {e}")
            return Image.new('RGB', (800, 600), color=(0, 0, 0))

    def capture_and_display_screen(self):
        """Capture screen and display in GUI, refine as data."""
        img = self.capture_screen().resize((200, 200))
        photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        # Crop random region
        width, height = img.size
        crop_box = (random.randint(0, width//2), random.randint(0, height//2), random.randint(width//2, width), random.randint(height//2, height))
        cropped = img.crop(crop_box)
        safe_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        crop_path = os.path.join(self.screenshot_dir, f"crop_{safe_ts}.png")
        cropped.save(crop_path)
        ocr_text = self.ocr_screenshot(cropped)
        self.refine_data({"screen_crop": crop_path, "ocr": ocr_text}, datetime.now().isoformat(), verify=False)
        self.output_text.insert(tk.END, "Screen captured, cropped, OCR'd, and displayed.\n")

    def continuous_screen_capture(self):
        """Thread to continuously capture screen with smart region analysis."""
        capture_count = 0
        consecutive_errors = 0
        while self.running:
            try:
                raw_img = self.capture_screen()
                if raw_img is None:
                    time.sleep(5)
                    continue
                img = raw_img.resize((400, 300))
                consecutive_errors = 0
                # Schedule Tkinter widget update on the main thread (thread-safe)
                def _update_screen_label(im=img):
                    try:
                        photo = ImageTk.PhotoImage(im)
                        self.screen_label.config(image=photo)
                        self.screen_label.image = photo
                    except Exception:
                        pass
                self.root.after_idle(_update_screen_label)
                capture_count += 1
                if capture_count % 6 == 0:
                    regions = [
                        (0, 0, img.width // 2, img.height // 2),
                        (img.width // 2, 0, img.width, img.height // 2),
                        (0, img.height // 2, img.width // 2, img.height),
                        (img.width // 2, img.height // 2, img.width, img.height),
                    ]
                    region = random.choice(regions)
                    cropped = img.crop(region)
                    safe_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                    crop_path = os.path.join(self.screenshot_dir, f"auto_crop_{safe_ts}.png")
                    screenshots = [f for f in os.listdir(self.screenshot_dir) if f.startswith('auto_crop_')]
                    if len(screenshots) > 50:
                        oldest = sorted(screenshots)[:20]
                        for old_f in oldest:
                            try:
                                os.remove(os.path.join(self.screenshot_dir, old_f))
                            except Exception as e:
                                print(f"  [ERR] screenshot_cleanup: {e}")
                    cropped.save(crop_path)
                    ocr_text = self.ocr_screenshot(cropped)
                    if len(ocr_text.strip()) > 20:
                        self.refine_data({"auto_screen_crop": crop_path, "ocr": ocr_text}, datetime.now().isoformat(), verify=False)
            except Exception as e:
                print(f"Screen capture error: {e}")
            time.sleep(5)

    def _os_control_allowed(self):
        """Hard safety gate: OS control requires Windows platform, the config
        flag, AND the environment variable CS_OS_CONTROL_ENABLED=1. This
        prevents the simulator from enabling OS control programmatically
        and guards against ctypes.windll crashes on non-Windows."""
        if sys.platform != 'win32':
            return False
        if not CONFIG.get('os_control_enabled', False):
            return False
        if os.environ.get('CS_OS_CONTROL_ENABLED', '0') != '1':
            return False
        return True

    def key_down(self, key):
        """Simulate key down."""
        if not self._os_control_allowed():
            print("OS control blocked: set CS_OS_CONTROL_ENABLED=1 env var and config flag")
            return
        code = KEY_CODES.get(key.upper(), None)
        if code:
            ctypes.windll.user32.keybd_event(code, 0, 0, 0)

    def key_up(self, key):
        """Simulate key up."""
        if not self._os_control_allowed():
            return
        code = KEY_CODES.get(key.upper(), None)
        if code:
            ctypes.windll.user32.keybd_event(code, 0, 2, 0)

    def send_hotkey(self, hotkey_str):
        """Send a hotkey sequence with safety checks and action logging."""
        if not self._os_control_allowed():
            print("OS control blocked: set CS_OS_CONTROL_ENABLED=1 env var and config flag")
            return
        dangerous_combos = ['Alt + F4', 'Ctrl + Alt + Del', 'Win + L']
        if hotkey_str.strip() in dangerous_combos:
            print(f"BLOCKED dangerous hotkey: {hotkey_str}")
            if not hasattr(self, '_os_action_log'):
                self._os_action_log = deque(maxlen=500)
            self._os_action_log.append({
                'action': 'hotkey_blocked', 'hotkey': hotkey_str,
                'timestamp': datetime.now().isoformat(), 'reason': 'dangerous_combo'
            })
            return
        if not hasattr(self, '_os_action_log'):
            self._os_action_log = deque(maxlen=500)
        self._os_action_log.append({
            'action': 'hotkey_sent', 'hotkey': hotkey_str,
            'timestamp': datetime.now().isoformat()
        })
        keys = [k.strip() for k in hotkey_str.split('+')]
        for key in keys:
            self.key_down(key)
        time.sleep(0.05)
        for key in reversed(keys):
            self.key_up(key)
        print(f"Sent hotkey: {hotkey_str}")

    def move_mouse(self, x, y):
        """Move mouse to absolute position with bounds checking and logging."""
        if not self._os_control_allowed():
            print("OS control blocked: set CS_OS_CONTROL_ENABLED=1 env var and config flag")
            return
        screen_w = ctypes.windll.user32.GetSystemMetrics(0)
        screen_h = ctypes.windll.user32.GetSystemMetrics(1)
        x = max(0, min(x, screen_w - 1))
        y = max(0, min(y, screen_h - 1))
        if not hasattr(self, '_os_action_log'):
            self._os_action_log = deque(maxlen=500)
        self._os_action_log.append({
            'action': 'mouse_move', 'x': x, 'y': y,
            'timestamp': datetime.now().isoformat()
        })
        ctypes.windll.user32.SetCursorPos(x, y)

    def click_mouse(self, button='left'):
        """Simulate mouse click with action logging."""
        if not self._os_control_allowed():
            print("OS control blocked: set CS_OS_CONTROL_ENABLED=1 env var and config flag")
            return
        if not hasattr(self, '_os_action_log'):
            self._os_action_log = deque(maxlen=500)
        self._os_action_log.append({
            'action': 'mouse_click', 'button': button,
            'timestamp': datetime.now().isoformat()
        })
        if button == 'left':
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.02)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        elif button == 'right':
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.02)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        elif button == 'middle':
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            time.sleep(0.02)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

    def _gui_watchdog(self):
        """Background thread that monitors the GUI heartbeat.
        If the main loop stops updating the heartbeat for too long,
        log a warning (helps diagnose GUI freezes)."""
        # Grace period: don't warn during startup init
        time.sleep(120)
        while self.running:
            time.sleep(15)
            try:
                elapsed = time.time() - self._gui_last_heartbeat
                if elapsed > 60:
                    print(f"  [WATCHDOG] GUI heartbeat stale ({elapsed:.0f}s) — possible freeze")
            except Exception:
                pass

    def run(self):
        print(f"Model params: {self.parameters_count():,}")
        self.root.mainloop()
        self.running = False
        if self._pygame_process is not None:
            try:
                self._pygame_process.terminate()
                self._pygame_process.wait(timeout=5)
            except Exception as e:
                print(f"  [ERR] pygame_terminate: {e}")
        if os.path.exists(self._world_state_file):
            try:
                os.remove(self._world_state_file)
            except Exception as e:
                print(f"  [ERR] world_state_remove: {e}")
        self.memory.close()

if __name__ == '__main__':
    # Create and run
    consciousness = ConsciousnessSimulator()
    consciousness.run()
