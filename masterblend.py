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
        motor = bpy.context.scene.render.engine
        if motor in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):        
            bpy.context.scene.eevee.taa_render_samples = 64
            bpy.context.scene.eevee.taa_samples = 16
            #bpy.context.scene.eevee.use_gtao = True
            #bpy.context.scene.eevee.gtao_quality = 1
            #bpy.context.scene.eevee.use_ssr = True
            #bpy.context.scene.eevee.use_ssr_refraction = True
            #bpy.context.scene.eevee.use_shadow_high_bitdepth = True
            #bpy.context.scene.eevee.shadow_cube_size = '64'
            #bpy.context.scene.eevee.shadow_cascade_size = '64'
            bpy.context.scene.eevee.gi_cubemap_resolution = '128'
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
        elif motor == "CYCLES":
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
        motor = bpy.context.scene.render.engine
        
        if motor in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):        
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            bpy.context.scene.eevee.taa_render_samples = 64
            bpy.context.scene.eevee.taa_samples = 16
            #bpy.context.scene.eevee.use_gtao = True
            #bpy.context.scene.eevee.gtao_quality = 1
            #bpy.context.scene.eevee.use_ssr = True
            #bpy.context.scene.eevee.use_ssr_refraction = True
            #bpy.context.scene.eevee.use_shadow_high_bitdepth = True
            #bpy.context.scene.eevee.shadow_cube_size = '1024'
            #bpy.context.scene.eevee.shadow_cascade_size = '1024'
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
        elif motor == "CYCLES":
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
            #bpy.context.scene.use_nodes = True        
            #bpy.context.scene.node_tree.nodes.clear()       
            #node_layers = bpy.context.scene.node_tree.nodes.new('CompositorNodeRLayers')
            #node_layers.name = 'node_layers_mb'
            #node_composite = bpy.context.scene.node_tree.nodes.new('CompositorNodeComposite')
            #node_composite.name = 'composite_mb'
            #node_denoiser = bpy.context.scene.node_tree.nodes.new('CompositorNodeDenoise')
            #node_denoiser.name = 'denoiser_mb'
            #tree = bpy.context.scene.node_tree 
            #links = tree.links 
            #link = links.new(node_layers.outputs["Image"], node_denoiser.inputs["Image"])
            #link = links.new(node_denoiser.outputs["Image"], node_composite.inputs["Image"])
            #link = links.new(node_layers.outputs["Denoising Normal"], node_denoiser.inputs["Normal"])
            #link = links.new(node_layers.outputs["Denoising Albedo"], node_denoiser.inputs["Albedo"])
          
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
 
class resete(bpy.types.Operator):
    bl_idname = "master_blend.resete"
    bl_label = "Configuração engines"
    
    def execute(self, context):        
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        bpy.context.scene.eevee.taa_render_samples = 64
        bpy.context.scene.eevee.taa_samples = 16
        bpy.context.scene.eevee.use_taa_reprojection = False
        bpy.context.scene.eevee.use_taa_reprojection = True
        bpy.context.scene.eevee.use_gtao = True
        bpy.context.scene.eevee.gtao_distance = 0.2
        bpy.context.scene.eevee.gtao_factor = 1
        bpy.context.scene.eevee.gtao_quality = 0.25
        bpy.context.scene.eevee.use_gtao_bent_normals = False
        bpy.context.scene.eevee.use_gtao_bent_normals = True
        bpy.context.scene.eevee.use_gtao_bounce = False
        bpy.context.scene.eevee.use_gtao_bounce = True
        bpy.context.scene.eevee.use_bloom = True
        bpy.context.scene.eevee.bloom_threshold = 0.8
        bpy.context.scene.eevee.bloom_knee = 0.5
        bpy.context.scene.eevee.bloom_radius = 6.5
        bpy.context.scene.eevee.bloom_color = (1.00017, 1.00017, 1.00017)
        bpy.context.scene.eevee.bloom_intensity = 0.05
        bpy.context.scene.eevee.bloom_clamp = 0
        bpy.context.scene.eevee.bokeh_max_size = 100
        bpy.context.scene.eevee.bokeh_threshold = 1
        bpy.context.scene.eevee.bokeh_neighbor_max = 10
        bpy.context.scene.eevee.bokeh_denoise_fac = 0.75
        bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = True
        bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = False
        bpy.context.scene.eevee.use_bokeh_jittered = True
        bpy.context.scene.eevee.use_bokeh_jittered = False
        bpy.context.scene.eevee.sss_samples = 7
        bpy.context.scene.eevee.sss_jitter_threshold = 0.3
        bpy.context.scene.eevee.use_ssr = True
        bpy.context.scene.eevee.use_ssr_refraction = True
        bpy.context.scene.eevee.use_ssr_halfres = False
        bpy.context.scene.eevee.use_ssr_halfres = True
        bpy.context.scene.eevee.ssr_quality = 0.25
        bpy.context.scene.eevee.ssr_max_roughness = 0.5
        bpy.context.scene.eevee.ssr_thickness = 0.2
        bpy.context.scene.eevee.ssr_border_fade = 0.075
        bpy.context.scene.eevee.ssr_firefly_fac = 10
        bpy.context.scene.eevee.use_motion_blur = True
        bpy.context.scene.eevee.motion_blur_position = 'CENTER'
        bpy.context.scene.eevee.motion_blur_shutter = 0.5
        bpy.context.scene.eevee.motion_blur_depth_scale = 99.99
        bpy.context.scene.eevee.motion_blur_depth_scale = 100
        bpy.context.scene.eevee.motion_blur_max = 32
        bpy.context.scene.eevee.motion_blur_steps = 1
        bpy.context.scene.eevee.use_motion_blur = False
        bpy.context.scene.eevee.use_bloom = False
        bpy.context.scene.eevee.volumetric_start = 0.1
        bpy.context.scene.eevee.volumetric_end = 100
        bpy.context.scene.eevee.volumetric_tile_size = '8'
        bpy.context.scene.eevee.volumetric_samples = 64
        bpy.context.scene.eevee.volumetric_sample_distribution = 0.8
        bpy.context.scene.eevee.use_volumetric_lights = False
        bpy.context.scene.eevee.use_volumetric_lights = True
        bpy.context.scene.eevee.volumetric_light_clamp = 0
        bpy.context.scene.eevee.use_volumetric_shadows = True
        bpy.context.scene.eevee.volumetric_shadow_samples = 16
        bpy.context.scene.eevee.use_volumetric_shadows = False
        bpy.context.scene.render.use_high_quality_normals = True
        bpy.context.scene.render.use_high_quality_normals = False
        bpy.context.scene.render.hair_type = 'STRAND'
        bpy.context.scene.render.hair_subdiv = 0
        bpy.context.scene.eevee.shadow_cube_size = '512'
        bpy.context.scene.eevee.shadow_cascade_size = '1024'
        bpy.context.scene.eevee.use_shadow_high_bitdepth = True
        bpy.context.scene.eevee.use_shadow_high_bitdepth = False
        bpy.context.scene.eevee.use_soft_shadows = False
        bpy.context.scene.eevee.use_soft_shadows = True
        bpy.context.scene.eevee.light_threshold = 0.01
        bpy.context.scene.eevee.gi_auto_bake = True
        bpy.context.scene.eevee.gi_auto_bake = False
        bpy.context.scene.eevee.gi_diffuse_bounces = 3
        bpy.context.scene.eevee.gi_cubemap_resolution = '512'
        bpy.context.scene.eevee.gi_visibility_resolution = '32'
        bpy.context.scene.eevee.gi_irradiance_smoothing = 0.1
        bpy.context.scene.eevee.gi_glossy_clamp = 0
        bpy.context.scene.eevee.gi_filter_quality = 3
        bpy.context.scene.eevee.gi_cubemap_display_size = 0.3
        bpy.context.scene.eevee.gi_irradiance_display_size = 0.1
        bpy.context.scene.render.filter_size = 1.5
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.render.film_transparent = False
        bpy.context.scene.eevee.use_overscan = True
        bpy.context.scene.eevee.use_overscan = False
        bpy.context.scene.eevee.use_overscan = True
        bpy.context.scene.eevee.overscan_size = 3
        bpy.context.scene.eevee.use_overscan = False
        bpy.context.scene.render.use_simplify = True
        bpy.context.scene.render.simplify_subdivision = 6
        bpy.context.scene.render.simplify_child_particles = 1
        bpy.context.scene.render.simplify_volumes = 1
        bpy.context.scene.render.simplify_shadows = 1
        bpy.context.scene.render.simplify_subdivision_render = 6
        bpy.context.scene.render.simplify_child_particles_render = 1
        bpy.context.scene.render.simplify_shadows_render = 1
        bpy.context.scene.render.use_simplify = False
        bpy.context.scene.grease_pencil_settings.antialias_threshold = 1
        bpy.context.scene.render.use_freestyle = True
        bpy.context.scene.render.line_thickness_mode = 'ABSOLUTE'
        bpy.context.scene.render.line_thickness_mode = 'ABSOLUTE'
        bpy.context.scene.render.line_thickness = 1
        bpy.context.scene.render.use_freestyle = False
        bpy.context.scene.display_settings.display_device = 'sRGB'
        bpy.context.scene.view_settings.view_transform = 'AgX'
        bpy.context.scene.view_settings.look = 'None'
        bpy.context.scene.view_settings.exposure = 0
        bpy.context.scene.view_settings.gamma = 1
        bpy.context.scene.sequencer_colorspace_settings.name = 'sRGB'
        bpy.context.scene.view_settings.use_curve_mapping = True
        bpy.context.scene.view_settings.use_curve_mapping = False
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.feature_set = 'SUPPORTED'
        bpy.context.scene.cycles.device = 'CPU'
        bpy.context.scene.cycles.shading_system = True
        bpy.context.scene.cycles.shading_system = False
        bpy.context.scene.cycles.use_preview_adaptive_sampling = False
        bpy.context.scene.cycles.use_preview_adaptive_sampling = True
        bpy.context.scene.cycles.preview_adaptive_threshold = 0.1
        bpy.context.scene.cycles.preview_samples = 1024
        bpy.context.scene.cycles.preview_adaptive_min_samples = 0
        bpy.context.scene.cycles.use_preview_denoising = True
        bpy.context.scene.cycles.preview_denoiser = 'AUTO'
        bpy.context.scene.cycles.preview_denoising_input_passes = 'RGB_ALBEDO'
        bpy.context.scene.cycles.preview_denoising_start_sample = 1
        bpy.context.scene.cycles.use_preview_denoising = False
        bpy.context.scene.cycles.use_adaptive_sampling = False
        bpy.context.scene.cycles.use_adaptive_sampling = True
        bpy.context.scene.cycles.adaptive_threshold = 0.01
        bpy.context.scene.cycles.samples = 4096
        bpy.context.scene.cycles.adaptive_min_samples = 0
        bpy.context.scene.cycles.time_limit = 0
        bpy.context.scene.cycles.use_denoising = False
        bpy.context.scene.cycles.use_denoising = True
        bpy.context.scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        bpy.context.scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
        bpy.context.scene.cycles.denoising_prefilter = 'ACCURATE'
        bpy.context.scene.cycles.use_guiding = True
        bpy.context.scene.cycles.use_guiding = False
        bpy.context.scene.cycles.use_guiding = True
        bpy.context.scene.cycles.guiding_training_samples = 128
        bpy.context.scene.cycles.use_surface_guiding = False
        bpy.context.scene.cycles.use_surface_guiding = True
        bpy.context.scene.cycles.use_volume_guiding = False
        bpy.context.scene.cycles.use_volume_guiding = True
        bpy.context.scene.cycles.use_guiding = False
        bpy.context.scene.cycles.use_light_tree = False
        bpy.context.scene.cycles.light_sampling_threshold = 0.01
        bpy.context.scene.cycles.use_light_tree = True
        bpy.context.scene.cycles.light_sampling_threshold = 0.01
        bpy.context.scene.cycles.seed = 0
        bpy.context.scene.cycles.sample_offset = 0
        bpy.context.scene.cycles.auto_scrambling_distance = True
        bpy.context.scene.cycles.auto_scrambling_distance = False
        bpy.context.scene.cycles.preview_scrambling_distance = True
        bpy.context.scene.cycles.preview_scrambling_distance = False
        bpy.context.scene.cycles.scrambling_distance = 1
        bpy.context.scene.cycles.min_light_bounces = 0
        bpy.context.scene.cycles.min_transparent_bounces = 0
        bpy.context.scene.cycles.max_bounces = 12
        bpy.context.scene.cycles.diffuse_bounces = 4
        bpy.context.scene.cycles.glossy_bounces = 4
        bpy.context.scene.cycles.transmission_bounces = 12
        bpy.context.scene.cycles.volume_bounces = 0
        bpy.context.scene.cycles.transparent_max_bounces = 8
        bpy.context.scene.cycles.sample_clamp_direct = 0
        bpy.context.scene.cycles.sample_clamp_indirect = 10
        bpy.context.scene.cycles.blur_glossy = 1
        bpy.context.scene.cycles.blur_glossy = 1
        bpy.context.scene.cycles.caustics_reflective = False
        bpy.context.scene.cycles.caustics_reflective = True
        bpy.context.scene.cycles.caustics_refractive = False
        bpy.context.scene.cycles.caustics_refractive = True
        bpy.context.scene.cycles.use_fast_gi = True
        bpy.context.scene.cycles.fast_gi_method = 'REPLACE'
        bpy.context.scene.world.light_settings.ao_factor = 1
        bpy.context.scene.world.light_settings.distance = 10
        bpy.context.scene.cycles.ao_bounces = 1
        bpy.context.scene.cycles.ao_bounces_render = 1
        bpy.context.scene.cycles.use_fast_gi = False
        bpy.context.scene.cycles.volume_step_rate = 1
        bpy.context.scene.cycles.volume_preview_step_rate = 1
        bpy.context.scene.cycles.volume_max_steps = 1024
        bpy.context.scene.cycles_curves.shape = 'RIBBONS'
        bpy.context.scene.cycles_curves.subdivisions = 1
        bpy.context.scene.cycles_curves.subdivisions = 2
        bpy.context.scene.render.hair_type = 'STRAND'
        bpy.context.scene.render.hair_subdiv = 0
        bpy.context.scene.render.use_simplify = True
        bpy.context.scene.render.simplify_subdivision = 5
        bpy.context.scene.render.simplify_subdivision = 6
        bpy.context.scene.render.simplify_child_particles = 1
        bpy.context.scene.cycles.texture_limit = 'OFF'
        bpy.context.scene.render.simplify_volumes = 1
        bpy.context.scene.render.simplify_subdivision_render = 6
        bpy.context.scene.render.simplify_child_particles_render = 1
        bpy.context.scene.cycles.texture_limit_render = 'OFF'
        bpy.context.scene.cycles.use_camera_cull = True
        bpy.context.scene.cycles.use_camera_cull = False
        bpy.context.scene.cycles.use_distance_cull = True
        bpy.context.scene.cycles.use_distance_cull = False
        bpy.context.scene.cycles.use_distance_cull = True
        bpy.context.scene.cycles.use_camera_cull = True
        bpy.context.scene.cycles.camera_cull_margin = 0.1
        bpy.context.scene.cycles.distance_cull_margin = 50
        bpy.context.scene.cycles.use_distance_cull = False
        bpy.context.scene.cycles.use_camera_cull = False
        bpy.context.scene.render.simplify_gpencil = True
        bpy.context.scene.render.simplify_gpencil_onplay = True
        bpy.context.scene.render.simplify_gpencil_onplay = False
        bpy.context.scene.render.simplify_gpencil_view_fill = False
        bpy.context.scene.render.simplify_gpencil_view_fill = True
        bpy.context.scene.render.simplify_gpencil_modifier = False
        bpy.context.scene.render.simplify_gpencil_modifier = True
        bpy.context.scene.render.simplify_gpencil_shader_fx = False
        bpy.context.scene.render.simplify_gpencil_shader_fx = True
        bpy.context.scene.render.simplify_gpencil_tint = False
        bpy.context.scene.render.simplify_gpencil_tint = True
        bpy.context.scene.render.simplify_gpencil_antialiasing = False
        bpy.context.scene.render.simplify_gpencil_antialiasing = True
        bpy.context.scene.render.use_motion_blur = True
        bpy.context.scene.cycles.motion_blur_position = 'CENTER'
        bpy.context.scene.render.motion_blur_shutter = 0.5
        bpy.context.scene.cycles.rolling_shutter_type = 'NONE'
        bpy.context.scene.cycles.rolling_shutter_duration = 0.1
        bpy.context.scene.render.use_motion_blur = False
        bpy.context.scene.render.simplify_gpencil = False
        bpy.context.scene.render.use_simplify = False
        bpy.context.scene.cycles.film_exposure = 1
        bpy.context.scene.cycles.pixel_filter_type = 'BLACKMAN_HARRIS'
        bpy.context.scene.cycles.filter_width = 1.5
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.cycles.film_transparent_glass = True
        bpy.context.scene.cycles.film_transparent_glass = False
        bpy.context.scene.cycles.film_transparent_roughness = 0.1
        bpy.context.scene.render.film_transparent = False
        bpy.context.scene.render.threads_mode = 'AUTO'
        bpy.context.scene.cycles.use_auto_tile = False
        bpy.context.scene.cycles.use_auto_tile = True
        bpy.context.scene.cycles.tile_size = 2048
        bpy.context.scene.cycles.debug_use_spatial_splits = True
        bpy.context.scene.cycles.debug_use_spatial_splits = False
        bpy.context.scene.cycles.debug_use_compact_bvh = True
        bpy.context.scene.cycles.debug_use_compact_bvh = False
        bpy.context.scene.render.use_persistent_data = True
        bpy.context.scene.render.use_persistent_data = False
        bpy.context.scene.render.preview_pixel_size = 'AUTO'
        bpy.context.scene.render.use_bake_multires = True
        bpy.context.scene.render.use_bake_multires = False
        bpy.context.scene.cycles.bake_type = 'COMBINED'
        bpy.context.scene.render.bake.view_from = 'ABOVE_SURFACE'
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_direct = True
        bpy.context.scene.render.bake.use_pass_indirect = False
        bpy.context.scene.render.bake.use_pass_indirect = True
        bpy.context.scene.render.bake.use_pass_diffuse = False
        bpy.context.scene.render.bake.use_pass_diffuse = True
        bpy.context.scene.render.bake.use_pass_glossy = False
        bpy.context.scene.render.bake.use_pass_glossy = True
        bpy.context.scene.render.bake.use_pass_transmission = False
        bpy.context.scene.render.bake.use_pass_transmission = True
        bpy.context.scene.render.bake.use_pass_emit = False
        bpy.context.scene.render.bake.use_pass_emit = True
        bpy.context.scene.render.bake.use_selected_to_active = True
        bpy.context.scene.render.bake.use_cage = True
        bpy.context.scene.render.bake.cage_extrusion = 0
        bpy.context.scene.render.bake.max_ray_distance = 0
        bpy.context.scene.render.bake.use_cage = False
        bpy.context.scene.render.bake.use_selected_to_active = False
        bpy.context.scene.render.bake.target = 'IMAGE_TEXTURES'
        bpy.context.scene.render.bake.use_clear = False
        bpy.context.scene.render.bake.use_clear = True
        bpy.context.scene.render.bake.margin_type = 'ADJACENT_FACES'
        bpy.context.scene.render.bake.margin = 16
        bpy.context.scene.grease_pencil_settings.antialias_threshold = 1
        bpy.context.scene.render.use_freestyle = True
        bpy.context.scene.render.line_thickness_mode = 'ABSOLUTE'
        bpy.context.scene.render.line_thickness = 0.9
        bpy.context.scene.render.line_thickness = 1
        bpy.context.scene.render.use_freestyle = False
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        bpy.context.scene.render.resolution_percentage = 100
        bpy.context.scene.render.pixel_aspect_x = 1
        bpy.context.scene.render.pixel_aspect_y = 1
        bpy.context.scene.render.use_border = True
        bpy.context.scene.render.use_border = False
        bpy.context.scene.render.use_crop_to_border = True
        bpy.context.scene.render.use_crop_to_border = False
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 250
        bpy.context.scene.frame_step = 1
        bpy.context.scene.render.frame_map_old = 100
        bpy.context.scene.render.frame_map_new = 100
        bpy.context.scene.render.use_multiview = True
        bpy.context.scene.render.views_format = 'STEREO_3D'
        bpy.context.scene.render.use_multiview = False
        bpy.context.scene.render.filepath = "/tmp\\"
        bpy.context.scene.render.use_file_extension = False
        bpy.context.scene.render.use_file_extension = True
        bpy.context.scene.render.use_render_cache = True
        bpy.context.scene.render.use_render_cache = False
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        bpy.context.scene.render.image_settings.color_depth = '8'
        bpy.context.scene.render.image_settings.compression = 15
        bpy.context.scene.render.use_overwrite = False
        bpy.context.scene.render.use_overwrite = True
        bpy.context.scene.render.use_placeholder = True
        bpy.context.scene.render.use_placeholder = False
        bpy.context.scene.render.image_settings.color_management = 'FOLLOW_SCENE'
        bpy.context.scene.render.metadata_input = 'SCENE'
        bpy.context.scene.render.use_stamp_date = False
        bpy.context.scene.render.use_stamp_date = True
        bpy.context.scene.render.use_stamp_time = False
        bpy.context.scene.render.use_stamp_time = True
        bpy.context.scene.render.use_stamp_render_time = False
        bpy.context.scene.render.use_stamp_render_time = True
        bpy.context.scene.render.use_stamp_frame = False
        bpy.context.scene.render.use_stamp_frame = True
        bpy.context.scene.render.use_stamp_frame_range = True
        bpy.context.scene.render.use_stamp_frame_range = False
        bpy.context.scene.render.use_stamp_memory = True
        bpy.context.scene.render.use_stamp_memory = False
        bpy.context.scene.render.use_stamp_hostname = True
        bpy.context.scene.render.use_stamp_hostname = False
        bpy.context.scene.render.use_stamp_camera = False
        bpy.context.scene.render.use_stamp_camera = True
        bpy.context.scene.render.use_stamp_lens = True
        bpy.context.scene.render.use_stamp_lens = False
        bpy.context.scene.render.use_stamp_scene = False
        bpy.context.scene.render.use_stamp_scene = True
        bpy.context.scene.render.use_stamp_marker = True
        bpy.context.scene.render.use_stamp_marker = False
        bpy.context.scene.render.use_stamp_filename = False
        bpy.context.scene.render.use_stamp_filename = True
        bpy.context.scene.render.use_stamp_sequencer_strip = True
        bpy.context.scene.render.use_stamp_sequencer_strip = False
        bpy.context.scene.render.use_stamp_note = True
        bpy.context.scene.render.use_stamp_note = False
        bpy.context.scene.render.use_stamp = True
        bpy.context.scene.render.stamp_font_size = 12
        bpy.context.scene.render.stamp_foreground = (0.8, 0.8, 0.8, 1)
        bpy.context.scene.render.stamp_background = (0, 0, 0, 0.25)
        bpy.context.scene.render.use_stamp_labels = False
        bpy.context.scene.render.use_stamp_labels = True
        bpy.context.scene.render.use_stamp = False
        bpy.context.scene.render.use_compositing = False
        bpy.context.scene.render.use_compositing = True
        bpy.context.scene.render.use_sequencer = False
        bpy.context.scene.render.use_sequencer = True
        bpy.context.scene.render.dither_intensity = 1
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        bpy.context.scene.eevee.use_gtao = False
        bpy.context.scene.eevee.use_ssr = False

                
        return {'FINISHED'}

class resete(bpy.types.Operator):
    bl_idname = "master_blend.resete"
    bl_label = "Configuração engines"
    
    def execute(self, context):        
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        bpy.context.scene.eevee.taa_render_samples = 64
        bpy.context.scene.eevee.taa_samples = 16
        bpy.context.scene.eevee.use_taa_reprojection = False
        bpy.context.scene.eevee.use_taa_reprojection = True
        bpy.context.scene.eevee.use_gtao = True
        bpy.context.scene.eevee.gtao_distance = 0.2
        bpy.context.scene.eevee.gtao_factor = 1
        bpy.context.scene.eevee.gtao_quality = 0.25
        bpy.context.scene.eevee.use_gtao_bent_normals = False
        bpy.context.scene.eevee.use_gtao_bent_normals = True
        bpy.context.scene.eevee.use_gtao_bounce = False
        bpy.context.scene.eevee.use_gtao_bounce = True
        bpy.context.scene.eevee.use_bloom = True
        bpy.context.scene.eevee.bloom_threshold = 0.8
        bpy.context.scene.eevee.bloom_knee = 0.5
        bpy.context.scene.eevee.bloom_radius = 6.5
        bpy.context.scene.eevee.bloom_color = (1.00017, 1.00017, 1.00017)
        bpy.context.scene.eevee.bloom_intensity = 0.05
        bpy.context.scene.eevee.bloom_clamp = 0
        bpy.context.scene.eevee.bokeh_max_size = 100
        bpy.context.scene.eevee.bokeh_threshold = 1
        bpy.context.scene.eevee.bokeh_neighbor_max = 10
        bpy.context.scene.eevee.bokeh_denoise_fac = 0.75
        bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = True
        bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = False
        bpy.context.scene.eevee.use_bokeh_jittered = True
        bpy.context.scene.eevee.use_bokeh_jittered = False
        bpy.context.scene.eevee.sss_samples = 7
        bpy.context.scene.eevee.sss_jitter_threshold = 0.3
        bpy.context.scene.eevee.use_ssr = True
        bpy.context.scene.eevee.use_ssr_refraction = True
        bpy.context.scene.eevee.use_ssr_halfres = False
        bpy.context.scene.eevee.use_ssr_halfres = True
        bpy.context.scene.eevee.ssr_quality = 0.25
        bpy.context.scene.eevee.ssr_max_roughness = 0.5
        bpy.context.scene.eevee.ssr_thickness = 0.2
        bpy.context.scene.eevee.ssr_border_fade = 0.075
        bpy.context.scene.eevee.ssr_firefly_fac = 10
        bpy.context.scene.eevee.use_motion_blur = True
        bpy.context.scene.eevee.motion_blur_position = 'CENTER'
        bpy.context.scene.eevee.motion_blur_shutter = 0.5
        bpy.context.scene.eevee.motion_blur_depth_scale = 99.99
        bpy.context.scene.eevee.motion_blur_depth_scale = 100
        bpy.context.scene.eevee.motion_blur_max = 32
        bpy.context.scene.eevee.motion_blur_steps = 1
        bpy.context.scene.eevee.use_motion_blur = False
        bpy.context.scene.eevee.use_bloom = False
        bpy.context.scene.eevee.volumetric_start = 0.1
        bpy.context.scene.eevee.volumetric_end = 100
        bpy.context.scene.eevee.volumetric_tile_size = '8'
        bpy.context.scene.eevee.volumetric_samples = 64
        bpy.context.scene.eevee.volumetric_sample_distribution = 0.8
        bpy.context.scene.eevee.use_volumetric_lights = False
        bpy.context.scene.eevee.use_volumetric_lights = True
        bpy.context.scene.eevee.volumetric_light_clamp = 0
        bpy.context.scene.eevee.use_volumetric_shadows = True
        bpy.context.scene.eevee.volumetric_shadow_samples = 16
        bpy.context.scene.eevee.use_volumetric_shadows = False
        bpy.context.scene.render.use_high_quality_normals = True
        bpy.context.scene.render.use_high_quality_normals = False
        bpy.context.scene.render.hair_type = 'STRAND'
        bpy.context.scene.render.hair_subdiv = 0
        bpy.context.scene.eevee.shadow_cube_size = '512'
        bpy.context.scene.eevee.shadow_cascade_size = '1024'
        bpy.context.scene.eevee.use_shadow_high_bitdepth = True
        bpy.context.scene.eevee.use_shadow_high_bitdepth = False
        bpy.context.scene.eevee.use_soft_shadows = False
        bpy.context.scene.eevee.use_soft_shadows = True
        bpy.context.scene.eevee.light_threshold = 0.01
        bpy.context.scene.eevee.gi_auto_bake = True
        bpy.context.scene.eevee.gi_auto_bake = False
        bpy.context.scene.eevee.gi_diffuse_bounces = 3
        bpy.context.scene.eevee.gi_cubemap_resolution = '512'
        bpy.context.scene.eevee.gi_visibility_resolution = '32'
        bpy.context.scene.eevee.gi_irradiance_smoothing = 0.1
        bpy.context.scene.eevee.gi_glossy_clamp = 0
        bpy.context.scene.eevee.gi_filter_quality = 3
        bpy.context.scene.eevee.gi_cubemap_display_size = 0.3
        bpy.context.scene.eevee.gi_irradiance_display_size = 0.1
        bpy.context.scene.render.filter_size = 1.5
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.render.film_transparent = False
        bpy.context.scene.eevee.use_overscan = True
        bpy.context.scene.eevee.use_overscan = False
        bpy.context.scene.eevee.use_overscan = True
        bpy.context.scene.eevee.overscan_size = 3
        bpy.context.scene.eevee.use_overscan = False
        bpy.context.scene.render.use_simplify = True
        bpy.context.scene.render.simplify_subdivision = 6
        bpy.context.scene.render.simplify_child_particles = 1
        bpy.context.scene.render.simplify_volumes = 1
        bpy.context.scene.render.simplify_shadows = 1
        bpy.context.scene.render.simplify_subdivision_render = 6
        bpy.context.scene.render.simplify_child_particles_render = 1
        bpy.context.scene.render.simplify_shadows_render = 1
        bpy.context.scene.render.use_simplify = False
        bpy.context.scene.grease_pencil_settings.antialias_threshold = 1
        bpy.context.scene.render.use_freestyle = True
        bpy.context.scene.render.line_thickness_mode = 'ABSOLUTE'
        bpy.context.scene.render.line_thickness_mode = 'ABSOLUTE'
        bpy.context.scene.render.line_thickness = 1
        bpy.context.scene.render.use_freestyle = False
        bpy.context.scene.display_settings.display_device = 'sRGB'
        bpy.context.scene.view_settings.view_transform = 'AgX'
        bpy.context.scene.view_settings.look = 'None'
        bpy.context.scene.view_settings.exposure = 0
        bpy.context.scene.view_settings.gamma = 1
        bpy.context.scene.sequencer_colorspace_settings.name = 'sRGB'
        bpy.context.scene.view_settings.use_curve_mapping = True
        bpy.context.scene.view_settings.use_curve_mapping = False
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.feature_set = 'SUPPORTED'
        bpy.context.scene.cycles.device = 'CPU'
        bpy.context.scene.cycles.shading_system = True
        bpy.context.scene.cycles.shading_system = False
        bpy.context.scene.cycles.use_preview_adaptive_sampling = False
        bpy.context.scene.cycles.use_preview_adaptive_sampling = True
        bpy.context.scene.cycles.preview_adaptive_threshold = 0.1
        bpy.context.scene.cycles.preview_samples = 1024
        bpy.context.scene.cycles.preview_adaptive_min_samples = 0
        bpy.context.scene.cycles.use_preview_denoising = True
        bpy.context.scene.cycles.preview_denoiser = 'AUTO'
        bpy.context.scene.cycles.preview_denoising_input_passes = 'RGB_ALBEDO'
        bpy.context.scene.cycles.preview_denoising_start_sample = 1
        bpy.context.scene.cycles.use_preview_denoising = False
        bpy.context.scene.cycles.use_adaptive_sampling = False
        bpy.context.scene.cycles.use_adaptive_sampling = True
        bpy.context.scene.cycles.adaptive_threshold = 0.01
        bpy.context.scene.cycles.samples = 4096
        bpy.context.scene.cycles.adaptive_min_samples = 0
        bpy.context.scene.cycles.time_limit = 0
        bpy.context.scene.cycles.use_denoising = False
        bpy.context.scene.cycles.use_denoising = True
        bpy.context.scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        bpy.context.scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
        bpy.context.scene.cycles.denoising_prefilter = 'ACCURATE'
        bpy.context.scene.cycles.use_guiding = True
        bpy.context.scene.cycles.use_guiding = False
        bpy.context.scene.cycles.use_guiding = True
        bpy.context.scene.cycles.guiding_training_samples = 128
        bpy.context.scene.cycles.use_surface_guiding = False
        bpy.context.scene.cycles.use_surface_guiding = True
        bpy.context.scene.cycles.use_volume_guiding = False
        bpy.context.scene.cycles.use_volume_guiding = True
        bpy.context.scene.cycles.use_guiding = False
        bpy.context.scene.cycles.use_light_tree = False
        bpy.context.scene.cycles.light_sampling_threshold = 0.01
        bpy.context.scene.cycles.use_light_tree = True
        bpy.context.scene.cycles.light_sampling_threshold = 0.01
        bpy.context.scene.cycles.seed = 0
        bpy.context.scene.cycles.sample_offset = 0
        bpy.context.scene.cycles.auto_scrambling_distance = True
        bpy.context.scene.cycles.auto_scrambling_distance = False
        bpy.context.scene.cycles.preview_scrambling_distance = True
        bpy.context.scene.cycles.preview_scrambling_distance = False
        bpy.context.scene.cycles.scrambling_distance = 1
        bpy.context.scene.cycles.min_light_bounces = 0
        bpy.context.scene.cycles.min_transparent_bounces = 0
        bpy.context.scene.cycles.max_bounces = 12
        bpy.context.scene.cycles.diffuse_bounces = 4
        bpy.context.scene.cycles.glossy_bounces = 4
        bpy.context.scene.cycles.transmission_bounces = 12
        bpy.context.scene.cycles.volume_bounces = 0
        bpy.context.scene.cycles.transparent_max_bounces = 8
        bpy.context.scene.cycles.sample_clamp_direct = 0
        bpy.context.scene.cycles.sample_clamp_indirect = 10
        bpy.context.scene.cycles.blur_glossy = 1
        bpy.context.scene.cycles.blur_glossy = 1
        bpy.context.scene.cycles.caustics_reflective = False
        bpy.context.scene.cycles.caustics_reflective = True
        bpy.context.scene.cycles.caustics_refractive = False
        bpy.context.scene.cycles.caustics_refractive = True
        bpy.context.scene.cycles.use_fast_gi = True
        bpy.context.scene.cycles.fast_gi_method = 'REPLACE'
        bpy.context.scene.world.light_settings.ao_factor = 1
        bpy.context.scene.world.light_settings.distance = 10
        bpy.context.scene.cycles.ao_bounces = 1
        bpy.context.scene.cycles.ao_bounces_render = 1
        bpy.context.scene.cycles.use_fast_gi = False
        bpy.context.scene.cycles.volume_step_rate = 1
        bpy.context.scene.cycles.volume_preview_step_rate = 1
        bpy.context.scene.cycles.volume_max_steps = 1024
        bpy.context.scene.cycles_curves.shape = 'RIBBONS'
        bpy.context.scene.cycles_curves.subdivisions = 1
        bpy.context.scene.cycles_curves.subdivisions = 2
        bpy.context.scene.render.hair_type = 'STRAND'
        bpy.context.scene.render.hair_subdiv = 0
        bpy.context.scene.render.use_simplify = True
        bpy.context.scene.render.simplify_subdivision = 5
        bpy.context.scene.render.simplify_subdivision = 6
        bpy.context.scene.render.simplify_child_particles = 1
        bpy.context.scene.cycles.texture_limit = 'OFF'
        bpy.context.scene.render.simplify_volumes = 1
        bpy.context.scene.render.simplify_subdivision_render = 6
        bpy.context.scene.render.simplify_child_particles_render = 1
        bpy.context.scene.cycles.texture_limit_render = 'OFF'
        bpy.context.scene.cycles.use_camera_cull = True
        bpy.context.scene.cycles.use_camera_cull = False
        bpy.context.scene.cycles.use_distance_cull = True
        bpy.context.scene.cycles.use_distance_cull = False
        bpy.context.scene.cycles.use_distance_cull = True
        bpy.context.scene.cycles.use_camera_cull = True
        bpy.context.scene.cycles.camera_cull_margin = 0.1
        bpy.context.scene.cycles.distance_cull_margin = 50
        bpy.context.scene.cycles.use_distance_cull = False
        bpy.context.scene.cycles.use_camera_cull = False
        bpy.context.scene.render.simplify_gpencil = True
        bpy.context.scene.render.simplify_gpencil_onplay = True
        bpy.context.scene.render.simplify_gpencil_onplay = False
        bpy.context.scene.render.simplify_gpencil_view_fill = False
        bpy.context.scene.render.simplify_gpencil_view_fill = True
        bpy.context.scene.render.simplify_gpencil_modifier = False
        bpy.context.scene.render.simplify_gpencil_modifier = True
        bpy.context.scene.render.simplify_gpencil_shader_fx = False
        bpy.context.scene.render.simplify_gpencil_shader_fx = True
        bpy.context.scene.render.simplify_gpencil_tint = False
        bpy.context.scene.render.simplify_gpencil_tint = True
        bpy.context.scene.render.simplify_gpencil_antialiasing = False
        bpy.context.scene.render.simplify_gpencil_antialiasing = True
        bpy.context.scene.render.use_motion_blur = True
        bpy.context.scene.cycles.motion_blur_position = 'CENTER'
        bpy.context.scene.render.motion_blur_shutter = 0.5
        bpy.context.scene.cycles.rolling_shutter_type = 'NONE'
        bpy.context.scene.cycles.rolling_shutter_duration = 0.1
        bpy.context.scene.render.use_motion_blur = False
        bpy.context.scene.render.simplify_gpencil = False
        bpy.context.scene.render.use_simplify = False
        bpy.context.scene.cycles.film_exposure = 1
        bpy.context.scene.cycles.pixel_filter_type = 'BLACKMAN_HARRIS'
        bpy.context.scene.cycles.filter_width = 1.5
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.cycles.film_transparent_glass = True
        bpy.context.scene.cycles.film_transparent_glass = False
        bpy.context.scene.cycles.film_transparent_roughness = 0.1
        bpy.context.scene.render.film_transparent = False
        bpy.context.scene.render.threads_mode = 'AUTO'
        bpy.context.scene.cycles.use_auto_tile = False
        bpy.context.scene.cycles.use_auto_tile = True
        bpy.context.scene.cycles.tile_size = 2048
        bpy.context.scene.cycles.debug_use_spatial_splits = True
        bpy.context.scene.cycles.debug_use_spatial_splits = False
        bpy.context.scene.cycles.debug_use_compact_bvh = True
        bpy.context.scene.cycles.debug_use_compact_bvh = False
        bpy.context.scene.render.use_persistent_data = True
        bpy.context.scene.render.use_persistent_data = False
        bpy.context.scene.render.preview_pixel_size = 'AUTO'
        bpy.context.scene.render.use_bake_multires = True
        bpy.context.scene.render.use_bake_multires = False
        bpy.context.scene.cycles.bake_type = 'COMBINED'
        bpy.context.scene.render.bake.view_from = 'ABOVE_SURFACE'
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_direct = True
        bpy.context.scene.render.bake.use_pass_indirect = False
        bpy.context.scene.render.bake.use_pass_indirect = True
        bpy.context.scene.render.bake.use_pass_diffuse = False
        bpy.context.scene.render.bake.use_pass_diffuse = True
        bpy.context.scene.render.bake.use_pass_glossy = False
        bpy.context.scene.render.bake.use_pass_glossy = True
        bpy.context.scene.render.bake.use_pass_transmission = False
        bpy.context.scene.render.bake.use_pass_transmission = True
        bpy.context.scene.render.bake.use_pass_emit = False
        bpy.context.scene.render.bake.use_pass_emit = True
        bpy.context.scene.render.bake.use_selected_to_active = True
        bpy.context.scene.render.bake.use_cage = True
        bpy.context.scene.render.bake.cage_extrusion = 0
        bpy.context.scene.render.bake.max_ray_distance = 0
        bpy.context.scene.render.bake.use_cage = False
        bpy.context.scene.render.bake.use_selected_to_active = False
        bpy.context.scene.render.bake.target = 'IMAGE_TEXTURES'
        bpy.context.scene.render.bake.use_clear = False
        bpy.context.scene.render.bake.use_clear = True
        bpy.context.scene.render.bake.margin_type = 'ADJACENT_FACES'
        bpy.context.scene.render.bake.margin = 16
        bpy.context.scene.grease_pencil_settings.antialias_threshold = 1
        bpy.context.scene.render.use_freestyle = True
        bpy.context.scene.render.line_thickness_mode = 'ABSOLUTE'
        bpy.context.scene.render.line_thickness = 0.9
        bpy.context.scene.render.line_thickness = 1
        bpy.context.scene.render.use_freestyle = False
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        bpy.context.scene.render.resolution_percentage = 100
        bpy.context.scene.render.pixel_aspect_x = 1
        bpy.context.scene.render.pixel_aspect_y = 1
        bpy.context.scene.render.use_border = True
        bpy.context.scene.render.use_border = False
        bpy.context.scene.render.use_crop_to_border = True
        bpy.context.scene.render.use_crop_to_border = False
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 250
        bpy.context.scene.frame_step = 1
        bpy.context.scene.render.frame_map_old = 100
        bpy.context.scene.render.frame_map_new = 100
        bpy.context.scene.render.use_multiview = True
        bpy.context.scene.render.views_format = 'STEREO_3D'
        bpy.context.scene.render.use_multiview = False
        bpy.context.scene.render.filepath = "/tmp\\"
        bpy.context.scene.render.use_file_extension = False
        bpy.context.scene.render.use_file_extension = True
        bpy.context.scene.render.use_render_cache = True
        bpy.context.scene.render.use_render_cache = False
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        bpy.context.scene.render.image_settings.color_depth = '8'
        bpy.context.scene.render.image_settings.compression = 15
        bpy.context.scene.render.use_overwrite = False
        bpy.context.scene.render.use_overwrite = True
        bpy.context.scene.render.use_placeholder = True
        bpy.context.scene.render.use_placeholder = False
        bpy.context.scene.render.image_settings.color_management = 'FOLLOW_SCENE'
        bpy.context.scene.render.metadata_input = 'SCENE'
        bpy.context.scene.render.use_stamp_date = False
        bpy.context.scene.render.use_stamp_date = True
        bpy.context.scene.render.use_stamp_time = False
        bpy.context.scene.render.use_stamp_time = True
        bpy.context.scene.render.use_stamp_render_time = False
        bpy.context.scene.render.use_stamp_render_time = True
        bpy.context.scene.render.use_stamp_frame = False
        bpy.context.scene.render.use_stamp_frame = True
        bpy.context.scene.render.use_stamp_frame_range = True
        bpy.context.scene.render.use_stamp_frame_range = False
        bpy.context.scene.render.use_stamp_memory = True
        bpy.context.scene.render.use_stamp_memory = False
        bpy.context.scene.render.use_stamp_hostname = True
        bpy.context.scene.render.use_stamp_hostname = False
        bpy.context.scene.render.use_stamp_camera = False
        bpy.context.scene.render.use_stamp_camera = True
        bpy.context.scene.render.use_stamp_lens = True
        bpy.context.scene.render.use_stamp_lens = False
        bpy.context.scene.render.use_stamp_scene = False
        bpy.context.scene.render.use_stamp_scene = True
        bpy.context.scene.render.use_stamp_marker = True
        bpy.context.scene.render.use_stamp_marker = False
        bpy.context.scene.render.use_stamp_filename = False
        bpy.context.scene.render.use_stamp_filename = True
        bpy.context.scene.render.use_stamp_sequencer_strip = True
        bpy.context.scene.render.use_stamp_sequencer_strip = False
        bpy.context.scene.render.use_stamp_note = True
        bpy.context.scene.render.use_stamp_note = False
        bpy.context.scene.render.use_stamp = True
        bpy.context.scene.render.stamp_font_size = 12
        bpy.context.scene.render.stamp_foreground = (0.8, 0.8, 0.8, 1)
        bpy.context.scene.render.stamp_background = (0, 0, 0, 0.25)
        bpy.context.scene.render.use_stamp_labels = False
        bpy.context.scene.render.use_stamp_labels = True
        bpy.context.scene.render.use_stamp = False
        bpy.context.scene.render.use_compositing = False
        bpy.context.scene.render.use_compositing = True
        bpy.context.scene.render.use_sequencer = False
        bpy.context.scene.render.use_sequencer = True
        bpy.context.scene.render.dither_intensity = 1
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        bpy.context.scene.eevee.use_gtao = False
        bpy.context.scene.eevee.use_ssr = False

                
        return {'FINISHED'}

class submenu_0(bpy.types.Menu):
    bl_idname = "submenu_0.name"
    bl_label = ""
    def draw(self, context):
        layout = self.layout             
        layout.operator("master_blend.material_override", text='Aplicar')         
        layout.operator("master_blend.remove_material_override", text='Remover')

class submenu_1(bpy.types.Menu):
    bl_idname = "submenu_1.name"
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        layout.separator() 
        self.layout.label(text="Qualidade")             
        layout.operator("master_blend.baixa", text='Baixa')         
        layout.operator("master_blend.media", text='Média')
        layout.operator("master_blend.alta", text='Alta')        
        layout.separator()
        self.layout.label(text="Configuração padrão")             
        layout.operator("master_blend.resete", text='Reset')   

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
        self.layout.label(text="Configuração da Engine")
        layout.menu(submenu_1.bl_idname)          

classes = (MB_Properties, submenu_0, resete, master_alta, master_media, master_baixa, remove_override, material_override, menu_principal, submenu_1)

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
