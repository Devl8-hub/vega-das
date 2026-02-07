# SPDX-FileCopyrightText: 2022-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

from bl_ui import node_add_menu
from bpy.app.translations import (
    contexts as i18n_contexts,
)


# only show input/output nodes when editing line style node trees
def line_style_shader_nodes_poll(context):
    snode = context.space_data
    return (snode.tree_type == 'ShaderNodeTree' and
            snode.shader_type == 'LINESTYLE')


# only show nodes working in world node trees
def world_shader_nodes_poll(context):
    snode = context.space_data
    return (snode.tree_type == 'ShaderNodeTree' and
            snode.shader_type == 'WORLD')


# only show nodes working in object node trees
def object_shader_nodes_poll(context):
    snode = context.space_data
    return (snode.tree_type == 'ShaderNodeTree' and
            snode.shader_type == 'OBJECT')


def cycles_shader_nodes_poll(context):
    return context.engine == 'CYCLES'


def eevee_shader_nodes_poll(context):
    return context.engine == 'BLENDER_EEVEE'


def object_not_eevee_shader_nodes_poll(context):
    return (object_shader_nodes_poll(context) and
            not eevee_shader_nodes_poll(context))


def object_eevee_shader_nodes_poll(context):
    return (object_shader_nodes_poll(context) and
            eevee_shader_nodes_poll(context))


class NODE_MT_shader_node_input_base(node_add_menu.NodeMenu):
    bl_label = "Input"

    def draw(self, context):
        layout = self.layout

        self.node_operator(layout, "ShaderNodeAttribute")
        self.node_operator(layout, "ShaderNodeVertexColor")
        self.node_operator(layout, "ShaderNodeUVMap")

        self.draw_assets_for_catalog(layout, self.bl_label)



class NODE_MT_shader_node_output_base(node_add_menu.NodeMenu):
    bl_label = "Output"

    def draw(self, context):
        layout = self.layout

        self.node_operator(
            layout,
            "ShaderNodeOutputMaterial",
            poll=object_shader_nodes_poll(context),
        )

        self.draw_assets_for_catalog(layout, self.bl_label)


class NODE_MT_shader_node_shader_base(node_add_menu.NodeMenu):
    bl_label = "Shader"

    def draw(self, context):
        layout = self.layout

        self.node_operator(
            layout,
            "ShaderNodeBsdfPrincipled",
            poll=object_shader_nodes_poll(context),
        )

        self.draw_assets_for_catalog(layout, self.bl_label)


class NODE_MT_shader_node_color_base(node_add_menu.NodeMenu):
    bl_label = "Color"

    def draw(self, context):
        layout = self.layout

        self.color_mix_node(context, layout)
        self.node_operator(layout, "ShaderNodeSeparateColor")

        self.draw_assets_for_catalog(layout, self.bl_label)


class NODE_MT_shader_node_texture_base(node_add_menu.NodeMenu):
    bl_label = "Texture"

    def draw(self, _context):
        layout = self.layout

        self.node_operator(layout, "ShaderNodeTexImage")

        self.draw_assets_for_catalog(layout, self.bl_label)




class NODE_MT_shader_node_all_base(node_add_menu.NodeMenu):
    bl_label = ""
    menu_path = "Root"
    bl_translation_context = i18n_contexts.operator_default

    # NOTE: Menus are looked up via their label, this is so that both the Add
    # & Swap menus can share the same layout while each using their
    # corresponding menus
    def draw(self, context):
        del context
        layout = self.layout
        self.draw_menu(layout, "Input")
        self.draw_menu(layout, "Output")
        layout.separator()
        # Do not order this alphabetically, we are matching the order in the output node.
        self.draw_menu(layout, "Shader")
        layout.separator()
        self.draw_menu(layout, "Color")
        self.draw_menu(layout, "Texture")
        layout.separator()
        self.draw_menu(layout, "Group")
        self.draw_menu(layout, "Layout")


add_menus = {
    # menu `bl_idname`: base-class.
    "NODE_MT_category_shader_input": NODE_MT_shader_node_input_base,
    "NODE_MT_category_shader_output": NODE_MT_shader_node_output_base,
    "NODE_MT_category_shader_color": NODE_MT_shader_node_color_base,
    "NODE_MT_category_shader_shader": NODE_MT_shader_node_shader_base,
    "NODE_MT_category_shader_texture": NODE_MT_shader_node_texture_base,
    "NODE_MT_shader_node_add_all": NODE_MT_shader_node_all_base,
}
add_menus = node_add_menu.generate_menus(
    add_menus,
    template=node_add_menu.AddNodeMenu,
    base_dict=node_add_menu.add_base_pathing_dict
)


swap_menus = {
    # menu `bl_idname`: base-class.
    "NODE_MT_shader_node_input_swap": NODE_MT_shader_node_input_base,
    "NODE_MT_shader_node_output_swap": NODE_MT_shader_node_output_base,
    "NODE_MT_shader_node_color_swap": NODE_MT_shader_node_color_base,
    "NODE_MT_shader_node_shader_swap": NODE_MT_shader_node_shader_base,
    "NODE_MT_shader_node_texture_swap": NODE_MT_shader_node_texture_base,
    "NODE_MT_shader_node_swap_all": NODE_MT_shader_node_all_base,
}
swap_menus = node_add_menu.generate_menus(
    swap_menus,
    template=node_add_menu.SwapNodeMenu,
    base_dict=node_add_menu.swap_base_pathing_dict
)


classes = (
    *add_menus,
    *swap_menus,
)


if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
