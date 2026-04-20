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

class material_override(bpy.types.Operator):
    bl_idname = "master_blend.material_override"
    bl_label = "Material Override"
    
    def execute(self, context):
        
        for material in bpy.data.materials:          
            if material.use_nodes is False:
                material.use_nodes = True
            principled_node = material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
            principled_node.name = 'principled_node_OVERRIDE'
            principled_node.inputs['Roughness'].default_value = 0.2
            Output_node = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
            Output_node.name = 'Output_node_OVERRIDE'
            material.node_tree.links.new(principled_node.outputs['BSDF'], Output_node.inputs['Surface'])
            
            if material.node_tree and "Output_node_OVERRIDE" in material.node_tree.nodes:
                node_to_active = material.node_tree.nodes["Output_node_OVERRIDE"]
                material.node_tree.nodes.active = node_to_active
                
        return {'FINISHED'}

class remove_override(bpy.types.Operator):
    bl_idname = "master_blend.remove_material_override"
    bl_label = "Material Override"
    
    def execute(self, context):
                        
        for material in bpy.data.materials:          
                        
            if material.node_tree and "Output_node_OVERRIDE" in material.node_tree.nodes:
                node_to_delete = material.node_tree.nodes["Output_node_OVERRIDE"]
                material.node_tree.nodes.remove(node_to_delete)
                
            if material.node_tree and "principled_node_OVERRIDE" in material.node_tree.nodes:
                node_to_delete = material.node_tree.nodes["principled_node_OVERRIDE"]
                material.node_tree.nodes.remove(node_to_delete)
                
            if material.node_tree and "Material Output" in material.node_tree.nodes:
                    node_to_active = material.node_tree.nodes["Material Output"]
                    material.node_tree.nodes.active = node_to_active
                
        return {'FINISHED'}

class submenu_0(bpy.types.Menu):
    bl_idname = "submenu_0.name"
    bl_label = ""
    def draw(self, context):
        layout = self.layout             
        layout.operator("master_blend.material_override", text='Aplicar')         
        layout.operator("master_blend.remove_material_override", text='Remover')

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
        layout.label(text="Material Override")
        layout.menu(submenu_0.bl_idname)      

classes = (MB_Properties, submenu_0, remove_override, material_override, menu_principal)

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
