
# SPDX-License-Identifier: GPL-2.0-or-later

# "High Performance" Minimal Blender.
# Focused on Layout, Shading, and Rendering with GPU acceleration.

# --- DISABLE ---

set(WITH_ALEMBIC             OFF CACHE BOOL "" FORCE) # Huge
set(WITH_USD                 OFF CACHE BOOL "" FORCE) # Huge

set(WITH_AUDASPACE           OFF CACHE BOOL "" FORCE) # Audio engine
set(WITH_OPENAL              OFF CACHE BOOL "" FORCE)
set(WITH_JACK                OFF CACHE BOOL "" FORCE)
set(WITH_PULSEAUDIO          OFF CACHE BOOL "" FORCE)
set(WITH_COREAUDIO           OFF CACHE BOOL "" FORCE)
set(WITH_WASAPI              OFF CACHE BOOL "" FORCE)
set(WITH_SDL                 OFF CACHE BOOL "" FORCE)

set(WITH_MOD_FLUID           OFF CACHE BOOL "" FORCE) # Physics
set(WITH_MOD_OCEANSIM        OFF CACHE BOOL "" FORCE)
set(WITH_MOD_REMESH          OFF CACHE BOOL "" FORCE)
# set(WITH_OPENVDB             OFF CACHE BOOL "" FORCE) # Keep OpenVDB for better volume shading support if needed? User said "and all". Let's enable it.

set(WITH_FREESTYLE           OFF CACHE BOOL "" FORCE) # Line rendering (CPU based usually)

set(WITH_INPUT_NDOF          OFF CACHE BOOL "" FORCE)
set(WITH_GHOST_XDND          OFF CACHE BOOL "" FORCE)

# --- ENABLE (Explicitly) ---

# GPU & Rendering
set(WITH_CYCLES              ON  CACHE BOOL "" FORCE) # Core Render Engine
set(WITH_CYCLES_OSL          ON  CACHE BOOL "" FORCE) # Advanced Shading
set(WITH_CYCLES_DEVICE_METAL ON  CACHE BOOL "" FORCE) # macOS GPU Support
set(WITH_CYCLES_DEVICE_CUDA  OFF CACHE BOOL "" FORCE)
set(WITH_CYCLES_DEVICE_OPTIX OFF CACHE BOOL "" FORCE)
set(WITH_CYCLES_DEVICE_HIP   OFF CACHE BOOL "" FORCE)
set(WITH_CYCLES_DEVICE_ONEAPI OFF CACHE BOOL "" FORCE)

set(WITH_COMPOSITOR          ON  CACHE BOOL "" FORCE) # Realtime Compositor
set(WITH_OPENVDB             ON  CACHE BOOL "" FORCE) # Volume support

# Modeling needs
set(WITH_OPENSUBDIV          ON  CACHE BOOL "" FORCE)
set(WITH_GMP                 ON  CACHE BOOL "" FORCE)
set(WITH_MANIFOLD            ON  CACHE BOOL "" FORCE)

# Shading needs
set(WITH_OPENCOLORIO         ON  CACHE BOOL "" FORCE)
set(WITH_OPENIMAGEIO         ON  CACHE BOOL "" FORCE)
set(WITH_IMAGE_OPENEXR       ON  CACHE BOOL "" FORCE)
set(WITH_IMAGE_OPENJPEG      ON  CACHE BOOL "" FORCE)
set(WITH_IMAGE_TIFF          ON  CACHE BOOL "" FORCE)
set(WITH_IMAGE_WEBP          ON  CACHE BOOL "" FORCE)

# IO needs
set(WITH_IO_WAVEFRONT_OBJ    ON  CACHE BOOL "" FORCE)
set(WITH_IO_STL              ON  CACHE BOOL "" FORCE)
set(WITH_IO_PLY              ON  CACHE BOOL "" FORCE)
set(WITH_IO_FBX              ON  CACHE BOOL "" FORCE)
set(WITH_IO_GREASE_PENCIL    OFF CACHE BOOL "" FORCE)

# Core
set(WITH_PYTHON              ON  CACHE BOOL "" FORCE)
set(WITH_PYTHON_INSTALL      ON  CACHE BOOL "" FORCE)
set(WITH_BULLET              ON  CACHE BOOL "" FORCE)
