import bpy
import bmesh
from bpy.types import Operator


class MeshSelectNext(Operator):
    """Select the next element (using selection order)"""
    bl_idname = "mesh.select_next_item"
    bl_label = "Select Next Element"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        from .bmesh import find_adjacent

        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        if find_adjacent.select_next(bm, self.report):
            bm.select_flush_mode()
            bmesh.update_edit_mesh(me, loop_triangles=False)

        return {'FINISHED'}


class MeshSelectPrev(Operator):
    """Select the previous element (using selection order)"""
    bl_idname = "mesh.select_prev_item"
    bl_label = "Select Previous Element"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        from .bmesh import find_adjacent

        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        if find_adjacent.select_prev(bm, self.report):
            bm.select_flush_mode()
            bmesh.update_edit_mesh(me, loop_triangles=False)

        return {'FINISHED'}


class MeshSelectBoxSeam(Operator):
    """Select edges marked as seams within a box"""
    bl_idname = "mesh.select_box_seam"
    bl_label = "Select Seam Box"
    bl_options = {'UNDO'}

    mode: bpy.props.EnumProperty(
        items=(
            ('SET', "Set", "Set a new selection"),
            ('ADD', "Add", "Extend existing selection"),
            ('SUB', "Subtract", "Subtract existing selection"),
            ('XOR', "Xor", "Invert existing selection"),
        ),
        default='SET',
    )
    wait_for_input: bpy.props.BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def modal(self, context, event):
        if event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'ESC', 'ENTER'} and event.value == 'RELEASE':
            self.filter_seams(context)
            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def filter_seams(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            return
        bm = bmesh.from_edit_mesh(obj.data)
        for edge in bm.edges:
            if edge.select and not edge.use_seam:
                edge.select = False
        bm.select_flush_mode()
        bmesh.update_edit_mesh(obj.data)

    def invoke(self, context, event):
        bpy.ops.view3d.select_box('INVOKE_DEFAULT', mode=self.mode, wait_for_input=self.wait_for_input)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


classes = (
    MeshSelectNext,
    MeshSelectPrev,
    MeshSelectBoxSeam,
)
