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

class master_baixa(bpy.types.Operator):
    bl_idname = "master_blend.baixa"
    bl_label = "Configuração engines"
    
    def execute(self, context):
        if bpy.data.window_managers["WinMan"].Evee:        
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            bpy.context.scene.eevee.taa_render_samples = 64
            bpy.context.scene.eevee.taa_samples = 16
            bpy.context.scene.eevee.use_gtao = True
            bpy.context.scene.eevee.gtao_quality = 1
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.use_ssr_refraction = True
            bpy.context.scene.eevee.use_shadow_high_bitdepth = True
            bpy.context.scene.eevee.shadow_cube_size = '64'
            bpy.context.scene.eevee.shadow_cascade_size = '64'
            bpy.context.scene.eevee.gi_cubemap_resolution = '64'
            bpy.context.scene.eevee.gi_visibility_resolution = '8'
            bpy.context.scene.display_settings.display_device = 'sRGB'
            bpy.context.scene.view_settings.view_transform = 'AgX'
            bpy.context.scene.view_settings.look = 'AgX - Punchy'
            bpy.context.scene.view_settings.exposure = 0
            bpy.context.scene.view_settings.gamma = 1
            bpy.context.scene.view_settings.use_curve_mapping = False
            bpy.context.scene.sequencer_colorspace_settings.name = 'sRGB'
            bpy.context.scene.render.use_border = False
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'
            bpy.context.scene.render.image_settings.color_depth = '16'
            bpy.context.scene.render.image_settings.color_management = 'FOLLOW_SCENE'
            bpy.context.scene.use_nodes = False            
        if bpy.data.window_managers["WinMan"].Cycles:
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.use_preview_denoising = True
            bpy.context.scene.cycles.preview_denoising_start_sample = 1
            bpy.context.scene.cycles.preview_samples = 1
            bpy.context.scene.cycles.preview_adaptive_threshold = 0.1
            bpy.context.scene.cycles.preview_adaptive_min_samples = 0
            bpy.context.scene.cycles.adaptive_threshold = 0.01
            bpy.context.scene.cycles.samples = 5
            bpy.context.scene.cycles.adaptive_min_samples = 0
            bpy.context.scene.cycles.use_denoising = True
            bpy.context.scene.render.use_persistent_data = True
            bpy.context.scene.display_settings.display_device = 'sRGB'
            bpy.context.scene.view_settings.view_transform = 'AgX'
            bpy.context.scene.view_settings.look = 'AgX - Punchy'
            bpy.context.scene.view_settings.exposure = 0
            bpy.context.scene.view_settings.gamma = 1
            bpy.context.scene.sequencer_colorspace_settings.name = 'sRGB'
            bpy.context.scene.view_settings.use_curve_mapping = False
            bpy.context.scene.cycles.max_bounces = 3
            bpy.context.scene.cycles.diffuse_bounces = 1
            bpy.context.scene.cycles.glossy_bounces = 4
            bpy.context.scene.cycles.transmission_bounces = 3
            bpy.context.scene.cycles.volume_bounces = 2
            bpy.context.scene.cycles.transparent_max_bounces = 4
            bpy.context.scene.cycles.sample_clamp_direct = 0
            bpy.context.scene.cycles.sample_clamp_indirect = 5
            bpy.context.scene.cycles.blur_glossy = 1
            bpy.context.scene.cycles.caustics_reflective = False
            bpy.context.scene.cycles.caustics_refractive = False
            bpy.context.scene.cycles.use_fast_gi = True
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.color_depth = '16'
            bpy.context.scene.render.image_settings.color_management = 'FOLLOW_SCENE'
            bpy.context.scene.render.use_border = False
            bpy.context.scene.use_nodes = False
            bpy.context.view_layer.cycles.denoising_store_passes = False
            
        return {'FINISHED'}

class master_media(bpy.types.Operator):
    bl_idname = "master_blend.media"
    bl_label = "Configuração engines"
    
    def execute(self, context):
        if bpy.data.window_managers["WinMan"].Evee:        
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            bpy.context.scene.eevee.taa_render_samples = 64
            bpy.context.scene.eevee.taa_samples = 16
            bpy.context.scene.eevee.use_gtao = True
            bpy.context.scene.eevee.gtao_quality = 1
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.use_ssr_refraction = True
            bpy.context.scene.eevee.use_shadow_high_bitdepth = True
            bpy.context.scene.eevee.shadow_cube_size = '1024'
            bpy.context.scene.eevee.shadow_cascade_size = '1024'
            bpy.context.scene.eevee.gi_cubemap_resolution = '256'
            bpy.context.scene.eevee.gi_visibility_resolution = '16'
            bpy.context.scene.display_settings.display_device = 'sRGB'
            bpy.context.scene.view_settings.view_transform = 'AgX'
            bpy.context.scene.view_settings.look = 'AgX - Punchy'
            bpy.context.scene.view_settings.exposure = 0
            bpy.context.scene.view_settings.gamma = 1
            bpy.context.scene.view_settings.use_curve_mapping = False
            bpy.context.scene.sequencer_colorspace_settings.name = 'sRGB'
            bpy.context.scene.render.use_border = False
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'
            bpy.context.scene.render.image_settings.color_depth = '16'
            bpy.context.scene.render.image_settings.color_management = 'FOLLOW_SCENE'
            bpy.context.scene.use_nodes = False            
        if bpy.data.window_managers["WinMan"].Cycles:
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.use_preview_denoising = True
            bpy.context.scene.cycles.preview_denoising_start_sample = 499
            bpy.context.scene.cycles.preview_samples = 500
            bpy.context.scene.cycles.preview_adaptive_threshold = 0.1
            bpy.context.scene.cycles.preview_adaptive_min_samples = 0
            bpy.context.scene.cycles.adaptive_threshold = 0.01
            bpy.context.scene.cycles.samples = 2000
            bpy.context.scene.cycles.adaptive_min_samples = 0
            bpy.context.scene.cycles.use_denoising = False
            bpy.context.scene.render.use_persistent_data = True
            bpy.context.scene.display_settings.display_device = 'sRGB'
            bpy.context.scene.view_settings.view_transform = 'AgX'
            bpy.context.scene.view_settings.look = 'AgX - Punchy'
            bpy.context.scene.view_settings.exposure = 0
            bpy.context.scene.view_settings.gamma = 1
            bpy.context.scene.sequencer_colorspace_settings.name = 'sRGB'
            bpy.context.scene.view_settings.use_curve_mapping = False
            bpy.context.scene.cycles.max_bounces = 12
            bpy.context.scene.cycles.diffuse_bounces = 4
            bpy.context.scene.cycles.glossy_bounces = 4
            bpy.context.scene.cycles.transmission_bounces = 12
            bpy.context.scene.cycles.volume_bounces = 0
            bpy.context.scene.cycles.transparent_max_bounces = 8
            bpy.context.scene.cycles.sample_clamp_direct = 0
            bpy.context.scene.cycles.sample_clamp_indirect = 10
            bpy.context.scene.cycles.blur_glossy = 1
            bpy.context.scene.cycles.caustics_reflective = True
            bpy.context.scene.cycles.caustics_refractive = True
            bpy.context.scene.cycles.use_fast_gi = False
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.color_depth = '16'
            bpy.context.scene.render.image_settings.color_management = 'FOLLOW_SCENE'
            bpy.context.scene.render.use_border = False
            bpy.context.view_layer.cycles.denoising_store_passes = True
            bpy.context.scene.use_nodes = True        
            bpy.context.scene.node_tree.nodes.clear()       
            node_layers = bpy.context.scene.node_tree.nodes.new('CompositorNodeRLayers')
            node_layers.name = 'node_layers_mb'
            node_composite = bpy.context.scene.node_tree.nodes.new('CompositorNodeComposite')
            node_composite.name = 'composite_mb'
            node_denoiser = bpy.context.scene.node_tree.nodes.new('CompositorNodeDenoise')
            node_denoiser.name = 'denoiser_mb'
            tree = bpy.context.scene.node_tree 
            links = tree.links 
            link = links.new(node_layers.outputs["Image"], node_denoiser.inputs["Image"])
            link = links.new(node_denoiser.outputs["Image"], node_composite.inputs["Image"])
            link = links.new(node_layers.outputs["Denoising Normal"], node_denoiser.inputs["Normal"])
            link = links.new(node_layers.outputs["Denoising Albedo"], node_denoiser.inputs["Albedo"])

        
        return {'FINISHED'}

class master_alta(bpy.types.Operator):
    bl_idname = "master_blend.alta"
    bl_label = "Configuração engines"
    
    def execute(self, context):
        if bpy.data.window_managers["WinMan"].Evee:        
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            bpy.context.scene.eevee.taa_render_samples = 128
            bpy.context.scene.eevee.taa_samples = 32
            bpy.context.scene.eevee.use_gtao = True
            bpy.context.scene.eevee.gtao_quality = 1
            bpy.context.scene.eevee.use_ssr = True
            bpy.context.scene.eevee.use_ssr_refraction = True
            bpy.context.scene.eevee.use_ssr_halfres = False
            bpy.context.scene.eevee.ssr_quality = 1
            bpy.context.scene.eevee.ssr_max_roughness = 0.5
            bpy.context.scene.eevee.ssr_thickness = 0.1
            bpy.context.scene.eevee.ssr_border_fade = 0        
            bpy.context.scene.eevee.ssr_firefly_fac = 100
            bpy.context.scene.eevee.gi_diffuse_bounces = 10
            bpy.context.scene.eevee.gi_glossy_clamp = 100
            bpy.context.scene.eevee.gi_filter_quality = 8
            bpy.context.scene.eevee.use_shadow_high_bitdepth = True
            bpy.context.scene.eevee.shadow_cube_size = '4096'
            bpy.context.scene.eevee.shadow_cascade_size = '4096'
            bpy.context.scene.eevee.gi_cubemap_resolution = '4096'
            bpy.context.scene.eevee.gi_visibility_resolution = '64'
            bpy.context.scene.display_settings.display_device = 'sRGB'
            bpy.context.scene.view_settings.view_transform = 'AgX'
            bpy.context.scene.view_settings.look = 'AgX - Punchy'
            bpy.context.scene.view_settings.exposure = 0
            bpy.context.scene.view_settings.gamma = 1
            bpy.context.scene.view_settings.use_curve_mapping = False
            bpy.context.scene.sequencer_colorspace_settings.name = 'sRGB'
            bpy.context.scene.render.use_border = False
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'
            bpy.context.scene.render.image_settings.color_depth = '16'
            bpy.context.scene.render.image_settings.color_management = 'FOLLOW_SCENE'
            bpy.context.scene.use_nodes = False            
        if bpy.data.window_managers["WinMan"].Cycles:
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.use_preview_denoising = True
            bpy.context.scene.cycles.preview_denoising_start_sample = 4999
            bpy.context.scene.cycles.preview_samples = 5000
            bpy.context.scene.cycles.preview_adaptive_threshold = 0.1
            bpy.context.scene.cycles.preview_adaptive_min_samples = 0
            bpy.context.scene.cycles.adaptive_threshold = 0.01
            bpy.context.scene.cycles.samples = 5000
            bpy.context.scene.cycles.adaptive_min_samples = 0
            bpy.context.scene.cycles.use_denoising = False
            bpy.context.scene.render.use_persistent_data = True
            bpy.context.scene.display_settings.display_device = 'sRGB'
            bpy.context.scene.view_settings.view_transform = 'AgX'
            bpy.context.scene.view_settings.look = 'AgX - Punchy'
            bpy.context.scene.view_settings.exposure = 0
            bpy.context.scene.view_settings.gamma = 1
            bpy.context.scene.sequencer_colorspace_settings.name = 'sRGB'
            bpy.context.scene.view_settings.use_curve_mapping = False
            bpy.context.scene.cycles.max_bounces = 32
            bpy.context.scene.cycles.diffuse_bounces = 32
            bpy.context.scene.cycles.glossy_bounces = 32
            bpy.context.scene.cycles.transmission_bounces = 32
            bpy.context.scene.cycles.volume_bounces = 32
            bpy.context.scene.cycles.transparent_max_bounces = 32
            bpy.context.scene.cycles.sample_clamp_direct = 0
            bpy.context.scene.cycles.sample_clamp_indirect = 10
            bpy.context.scene.cycles.blur_glossy = 1
            bpy.context.scene.cycles.caustics_reflective = True
            bpy.context.scene.cycles.caustics_refractive = True
            bpy.context.scene.cycles.use_fast_gi = False
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.color_depth = '16'
            bpy.context.scene.render.image_settings.color_management = 'FOLLOW_SCENE'
            bpy.context.scene.render.use_border = False
            bpy.context.view_layer.cycles.denoising_store_passes = True
            bpy.context.scene.use_nodes = True
            bpy.context.scene.node_tree.nodes.clear()
            node_layers = bpy.context.scene.node_tree.nodes.new('CompositorNodeRLayers')
            node_layers.name = 'node_layers_mb'
            node_composite = bpy.context.scene.node_tree.nodes.new('CompositorNodeComposite')
            node_composite.name = 'composite_mb'
            node_denoiser = bpy.context.scene.node_tree.nodes.new('CompositorNodeDenoise')
            node_denoiser.name = 'denoiser_mb'
            tree = bpy.context.scene.node_tree 
            links = tree.links 
            link = links.new(node_layers.outputs["Image"], node_denoiser.inputs["Image"])
            link = links.new(node_denoiser.outputs["Image"], node_composite.inputs["Image"])
            link = links.new(node_layers.outputs["Denoising Normal"], node_denoiser.inputs["Normal"])
            link = links.new(node_layers.outputs["Denoising Albedo"], node_denoiser.inputs["Albedo"])
        
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
