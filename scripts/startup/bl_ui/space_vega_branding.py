
import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty
import bpy.utils.previews

# Global cache for icons
vega_icons = None

def load_icons():
    global vega_icons
    if vega_icons is None:
        vega_icons = bpy.utils.previews.new()
        
        # Try to find splash.png in standard paths
        # 1. Release datafiles (dev environment)
        # 2. Bundle resources (installed)
        
        icon_path = None
        candidates = [
            os.path.join(bpy.utils.resource_path('DATAFILES'), "splash.png"),
            os.path.join(os.path.dirname(bpy.app.binary_path), "..", "Resources", "datafiles", "splash.png"),
            # Fallback relative to this script for dev
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "release", "datafiles", "splash.png")
        ]
        
        for p in candidates:
            if os.path.exists(p):
                icon_path = p
                break
        
        if icon_path:
            vega_icons.load("splash", icon_path, 'IMAGE')
        else:
            print("WARNING: Could not find splash.png for Vega DAS")

def release_icons():
    global vega_icons
    if vega_icons:
        bpy.utils.previews.remove(vega_icons)
        vega_icons = None

class WM_OT_splash_vega(Operator):
    """Open the Vega DAS Splash Screen"""
    bl_idname = "wm.splash_vega"
    bl_label = ""
    
    def invoke(self, context, event):
        # Splash screen disabled by user request
        return {'FINISHED'}

    def draw(self, context):
        pass


class WM_OT_about_vega(Operator):
    """About Vega DAS"""
    bl_idname = "wm.about_vega"
    bl_label = "About Vega DAS"

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=400)

    def draw(self, context):
        layout = self.layout
        
        # Load icons if needed
        if vega_icons is None:
            load_icons()

        col = layout.column(align=True)
        col.alignment = 'CENTER'
        col.scale_y = 1.2
        
        if "splash" in vega_icons:
             # Draw Logo
            row = col.row()
            row.alignment = 'CENTER'
            row.scale_y = 3.0
            row.label(text="", icon_value=vega_icons["splash"].icon_id)
        
        col.separator()
        col.label(text="VEGA DAS", icon='NONE')
        col.separator()
        
        row = col.row()
        row.alignment = 'CENTER'
        row.label(text=f"Version: {bpy.app.version_string}")
        
        row = col.row()
        row.alignment = 'CENTER'
        row.label(text=f"Built: {bpy.app.build_date}")
        
        col.separator()
        row = col.row()
        row.alignment = 'CENTER'
        row.label(text="Powered by Blender Technology")
        
        row = col.row()
        row.alignment = 'CENTER'
        row.label(text="© 2026 Vega DAS System")

classes = (
    WM_OT_splash_vega,
    WM_OT_about_vega,
)

def register():
    load_icons()
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    release_icons()
