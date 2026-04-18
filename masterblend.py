bl_info = {
    "name": "MasterBlend",
    "author": "Jeferson Martins",
    "version": (1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Master Blend",
    "description": "Kit de ferramentas voltadas para a arquitetura e renderização.",
    "category": "Object",
}

import bpy
import bmesh
import math


def update_render_engine(self, context):
    if self.render_engine == 'CYCLES':
        context.scene.render.engine = 'CYCLES'
    elif self.render_engine == 'BLENDER_EEVEE':
        context.scene.render.engine = 'BLENDER_EEVEE'


class MB_Properties(bpy.types.PropertyGroup):
    render_engine: bpy.props.EnumProperty(
        name="Render Engine",
        items=[
            ('BLENDER_EEVEE', "Eevee", ""),
            ('CYCLES', "Cycles", "")
        ],
        update=update_render_engine
    )


class menu_principal(bpy.types.Panel):
    bl_label = "Master Blend"
    bl_idname = "MENU_PT_master_blend"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Master Blend"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        layout.label(text="Master Blend", icon='COLORSET_02_VEC')
        layout.prop(wm.mb_props, "render_engine", expand=True)



classes = (MB_Properties, menu_principal)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.mb_props = bpy.props.PointerProperty(type=MB_Properties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.mb_props


if __name__ == "__main__":
    register()
