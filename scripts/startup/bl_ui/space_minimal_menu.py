import bpy
from bpy.types import Menu

# Custom minimal editor type menu with only Layout, UV Editing, and Shading editors
class MINIMAL_MT_editor_types(Menu):
    bl_idname = "MINIMAL_MT_editor_types"
    bl_label = "Editor Type"
    
    def draw(self, context):
        layout = self.layout

        def ui_type_entry(text, icon, value):
            props = layout.operator("wm.context_set_enum", text=text, icon=icon)
            props.data_path = "area.ui_type"
            props.value = value

        # Layout workspace editors
        layout.label(text="Layout")
        ui_type_entry("3D Viewport", 'VIEW3D', 'VIEW_3D')
        ui_type_entry("Properties", 'PROPERTIES', 'PROPERTIES')
        
        layout.separator()
        
        # UV Editing workspace editors
        layout.label(text="UV Editing")
        ui_type_entry("UV Editor", 'UV', 'UV')
        ui_type_entry("Image Editor", 'IMAGE', 'IMAGE_EDITOR')
        
        layout.separator()
        
        # Shading workspace editors
        layout.label(text="Shading")
        ui_type_entry("Shader Editor", 'NODE_MATERIAL', 'ShaderNodeTree')
        
        layout.separator()
        
        # Helper to set render settings and switch to properties
        op = layout.operator("minimal.setup_render", text="Render", icon='RENDER_RESULT')



class MINIMAL_OT_setup_render(bpy.types.Operator):
    """Setup render settings (Cycles, 1 sample) and switch to Properties"""
    bl_idname = "minimal.setup_render"
    bl_label = "Setup Render"
    
    def execute(self, context):
        # Switch to Properties editor
        context.area.ui_type = 'PROPERTIES'
        
        # Set render engine to Cycles
        context.scene.render.engine = 'CYCLES'
        
        # Set Cycles samples to 1
        # We use try/except just in case Cycles isn't available, though it should be.
        try:
            context.scene.cycles.samples = 1
            context.scene.cycles.preview_samples = 1
        except AttributeError:
            self.report({'WARNING'}, "Cycles engine not found or properties not available")
            
        return {'FINISHED'}


# Helper function to draw minimal header (editor type button only)
def draw_minimal_editor_type(layout, context):
    """Draws just the editor type selector button with minimal menu"""
    row = layout.row(align=True)
    row.menu("MINIMAL_MT_editor_types", text="", icon=context.area.spaces.active.type_icon)


classes = (
    MINIMAL_MT_editor_types,
    MINIMAL_OT_setup_render,
)


def register():
    import addon_utils
    print("DEBUG: Enabling Cycles addon...")
    try:
        mod = addon_utils.enable("cycles", default_set=True)
        print(f"DEBUG: Cycles enable result: {mod}")
    except Exception as e:
        print(f"DEBUG: Cycles enable FAILED: {e}")
        import traceback
        traceback.print_exc()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
