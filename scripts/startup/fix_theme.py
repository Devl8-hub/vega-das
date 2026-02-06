
import bpy
from bpy.app.handlers import persistent

@persistent
def fix_theme_and_overlays(dummy):
    # Force enable Overlays and Outline in all 3D Views
    # We iterate through all screens and areas effectively
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.overlay.show_overlays = True
                        space.overlay.show_outline_selected = True

    # Reset Theme Colors for 3D View to standard Blender Orange
    # Typically theme[0] is the active one
    for theme in bpy.context.preferences.themes:
        view3d = theme.view_3d
        
        # Active Object (Bright Orange)
        view3d.object_active = (1.0, 0.4, 0.0)
        # Selected Object (Darker Orange)
        view3d.object_selected = (1.0, 0.2, 0.0)
        # Outline Width (Make it slightly thicker to be visible)
        view3d.outline_width = 2
        
        # Also ensure vertex/edge/face select colors are visible
        view3d.vertex_select = (1.0, 0.4, 0.0)
        view3d.edge_select = (1.0, 0.4, 0.0)
        view3d.face_select = (1.0, 0.4, 0.0, 0.3) # RGBA

    print("Vega DAS: Theme and Overlays fixed via Handler.")

def register():
    # Register the handler to run after file load
    bpy.app.handlers.load_post.append(fix_theme_and_overlays)
    # Also run immediately in case we are reloading scripts or just started
    # Note: context might not be fully ready on immediate run during initial startup,
    # but the handler covers the startup.blend load.
    try:
        fix_theme_and_overlays(None)
    except:
        pass

def unregister():
    if fix_theme_and_overlays in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(fix_theme_and_overlays)

if __name__ == "__main__":
    register()
