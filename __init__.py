import bpy

bl_info = {
    "name": "BRT Custom Shortcuts for Blender", "author": "Barrunterio",
    "version": (0, 2, 0), "blender": (4, 1, 0), "location": "Shortcuts",
    "description": "Custom shortcuts for Blender",
    "warning": "", "wiki_url": "", "category": "UI"}

#fac = 0.1

def tile_area(self):
    for area in bpy.context.screen.areas:
        if area == bpy.context.area: # 'VIEW_3D', 'CONSOLE', 'INFO' etc. 
            override = bpy.context.copy()
            override['area'] = area
            if area.width > area.height:
                direction = 'VERTICAL'
            else:
                direction = 'HORIZONTAL'
            bpy.ops.screen.area_split(direction=direction, factor=0.5, cursor=(self.x,self.y))
            break

def tile_area_type(self,area_type,direction,fac):

    saved_area = bpy.context.area.ui_type
    bpy.context.area.ui_type = area_type
    for area in bpy.context.screen.areas:
        if area == bpy.context.area: # 'VIEW_3D', 'CONSOLE', 'INFO' etc. 
            override = bpy.context.copy()
            override['area'] = area
            if direction not in ['HORIZONTAL', 'VERTICAL']:
                if area.width > area.height:
                    direction = 'VERTICAL'
                else:
                    direction = 'HORIZONTAL'
            if direction == 'VERTICAL' and bpy.context.area.width < 800:
                fac = 0.5
            if direction == 'HORIZONTAL' and bpy.context.area.height < 800:
                fac = 0.5              
            if direction!= 'NULL':
                bpy.ops.screen.area_split(direction, factor=fac, cursor=(self.x,self.y))
            break
    bpy.context.area.ui_type = saved_area

def area_close():
    bpy.ops.screen.area_close()
 

def window_show(area_type, area_ui_type, res_x, res_y):
    pref = bpy.context.preferences
    render = bpy.context.scene.render
    view = pref.view
    
    orgResX = render.resolution_x
    orgResY = render.resolution_y
    orgDispMode = view.render_display_type 
    
    render.resolution_x = res_x
    render.resolution_y = res_y
    view.render_display_type = "WINDOW"
    
    bpy.ops.render.view_show("INVOKE_DEFAULT")
    
    area = bpy.context.window_manager.windows[-1].screen.areas[0]
    area.type = area_type
    area.ui_type = area_ui_type
    
    view.render_display_type = orgDispMode
    render.resolution_x = orgResX
    render.resolution_y = orgResY
    #print(str(area.type))

 
def closer_pos(self):
    init_x = bpy.context.area.x
    init_y = bpy.context.area.y
    final_x = init_x + bpy.context.area.width
    final_y = init_y + bpy.context.area.height
    half_x = bpy.context.area.width/2
    half_y = bpy.context.area.height/2
    offset_x=half_x+init_x
    offset_y=half_y+init_y
    #DEFINE PROPORTIONS
    max_res = max(bpy.context.area.height,bpy.context.area.width)
    res_x=max_res/bpy.context.area.width
    res_y=max_res/bpy.context.area.height

    if offset_x-self.x >= 0: #ask for X
        if (abs(offset_x-self.x)*res_x) > (abs(offset_y-self.y)*res_y):
            cursor_pos=(init_x,self.y)
        else:
            if offset_y-self.y >= 0:
                    cursor_pos=(self.x,init_y)                    
            else:    
                cursor_pos=(self.x,final_y)                        
    else:
        if (abs(offset_x-self.x)*res_x) > (abs(offset_y-self.y)*res_y):
            cursor_pos=(final_x,self.y)
        else:
            if offset_y-self.y >= 0:
                    cursor_pos=(self.x,init_y)                    
            else:    
                cursor_pos=(self.x,final_y)  
    return(cursor_pos)

def area_swap(self):
    for area in bpy.context.screen.areas:
        if area == bpy.context.area: # 'VIEW_3D', 'CONSOLE', 'INFO' etc. 
            cursor_pos=(0,0)
            override = bpy.context.copy()
            override['area'] = area
            cursor_pos = closer_pos(self)
            bpy.ops.screen.area_swap(cursor=cursor_pos)
            break

def area_join(self):
    for area in bpy.context.screen.areas:
        if area == bpy.context.area: # 'VIEW_3D', 'CONSOLE', 'INFO' etc. 
            cursor_pos=(0,0)
            override = bpy.context.copy()
            override['area'] = area
            cursor_pos = closer_pos(self)
            bpy.ops.screen.area_join(cursor=cursor_pos)
            break        

class BRT_Area_Tile(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.brt_area_tile"
    bl_label = "Tile_Area"

    def invoke(self, context, event):
        self.x = event.mouse_x
        self.y = event.mouse_y
        return self.execute(context)

    def execute(self, context):
        tile_area(self)
        return {'FINISHED'}
    
class BRT_Area_Swap(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.brt_area_swap"
    bl_label = "Area_Swap"

    def invoke(self, context, event):
        self.x = event.mouse_x
        self.y = event.mouse_y
        return self.execute(context)

    def execute(self, context):
        area_swap(self)
        return {'FINISHED'}

class BRT_Area_Join(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.brt_area_join"
    bl_label = "Area_Join"

    def invoke(self, context, event):
        self.x = event.mouse_x
        self.y = event.mouse_y
        return self.execute(context)

    def execute(self, context):
        area_join(self)
        return {'FINISHED'}

class BRT_Area_Close(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.brt_area_close"
    bl_label = "Area_Close"
    def execute(self, context):
        area_close()
        return {'FINISHED'}
    
class BRT_Area_Tile_VIEW3D(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_view3d"
    bl_label = "Tile_Area_VIEW_3D"
    def execute(self, context):
        tile_area_type(self,'VIEW_3D','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_PROPERTIES(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_properties"
    bl_label = "Tile_Area_Properties"
    def execute(self, context):
        tile_area_type(self,'PROPERTIES','VERTICAL',0.7)
        return {'FINISHED'}
class BRT_Area_Tile_OUTLINER(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_outliner"
    bl_label = "Tile_Area_Properties"
    def execute(self, context):
        tile_area_type(self,'OUTLINER','VERTICAL',0.7)
        return {'FINISHED'}
class BRT_Area_Tile_IMAGE(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_image"
    bl_label = "Tile_Area_IMAGE"
    def execute(self, context):
        tile_area_type(self,'IMAGE_EDITOR','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_UV(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_uv"
    bl_label = "Tile_Area_UV"
    def execute(self, context):
        tile_area_type(self,'UV','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_FILE_BROWSER(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_filebrowser"
    bl_label = "Tile_Area_File_Browser"
    def execute(self, context):
        tile_area_type(self,'FILE_BROWSER','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_TEXT_EDITOR(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_text_editor"
    bl_label = "Tile_Area_Text_Editor"
    def execute(self, context):
        tile_area_type(self,'TEXT_EDITOR','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_SPREADSHEET(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_spreadsheet"
    bl_label = "Tile_Area_SpreadSheet"
    def execute(self, context):
        tile_area_type(self,'SPREADSHEET','NULL',0.5)
        return {'FINISHED'}

class BRT_Area_Tile_ASSET_BROWSER(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_asset_browser"
    bl_label = "Tile_Area_Asset_Browser"
    def execute(self, context):
        tile_area_type(self,'ASSETS','VERTICAL',0.7)
        return {'FINISHED'}
class BRT_Area_Tile_SHADER_EDITOR(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_shader_editor"
    bl_label = "Tile_Area_Shader"
    def execute(self, context):
        tile_area_type(self,'ShaderNodeTree','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_DRIVERS(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_driver"
    bl_label = "Tile_Area_Driver"
    def execute(self, context):
        tile_area_type(self,'DRIVERS','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_FCURVES(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_fcurves"
    bl_label = "Tile_Area_Fcurves"
    def execute(self, context):
        tile_area_type(self,'FCURVES','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_GEOMETRY_NODES(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_geo_nodes"
    bl_label = "Tile_Area_Text_Geometry_Node"
    def execute(self, context):
        tile_area_type(self,'GeometryNodeTree','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_INFO(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_info"
    bl_label = "Tile_Area_Text_Info"
    def execute(self, context):
        tile_area_type(self,'INFO','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_DOPESHEET(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_dopesheet"
    bl_label = "Tile_Area_Dopesheet"
    def execute(self, context):
        tile_area_type(self,'DOPESHEET','HORIZONTAL',0.7)
        return {'FINISHED'}
class BRT_Area_Tile_TIMELINE(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_timeline"
    bl_label = "Tile_Area_Timeline"
    def execute(self, context):
        tile_area_type(self,'TIMELINE','HORIZONTAL',0.7)
        return {'FINISHED'}
class BRT_Area_Tile_NLA(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_nla"
    bl_label = "Tile_Area_NLA"
    def execute(self, context):
        tile_area_type(self,'NLA_EDITOR','HORIZONTAL',0.6)
        return {'FINISHED'}

class BRT_Area_Tile_COMPOSITOR(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_compositor"
    bl_label = "Tile_Area_Compositor"
    def execute(self, context):
        tile_area_type(self,'CompositorNodeTree','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_CONSOLE(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_console"
    bl_label = "Tile_Area_Console"
    def execute(self, context):
        tile_area_type(self,'CONSOLE','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_CLIP_EDITOR(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_clip_editor"
    bl_label = "Tile_Area_Clip_Editor"
    def execute(self, context):
        tile_area_type(self,'CLIP_EDITOR','NULL',0.5)
        return {'FINISHED'}
class BRT_Area_Tile_SEQUENCER(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.tile_area_sequencer"
    bl_label = "Tile_Area_Sequencer"
    def execute(self, context):
        tile_area_type(self,'SEQUENCE_EDITOR','NULL',0.5)
        return {'FINISHED'}                

class BRT_Open_ASSETS(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "brtwm.open_window_asset_browser"
    bl_label = "Tile_Area_Sequencer"
    def execute(self, context):
        window_show("FILE_BROWSER", "ASSETS", 1000, 1000)
        return {'FINISHED'}      

addon_keymaps = []
classes = (BRT_Area_Tile,
BRT_Area_Close,
BRT_Area_Swap,
BRT_Area_Join,
BRT_Area_Tile_VIEW3D,
BRT_Area_Tile_FILE_BROWSER,
BRT_Area_Tile_TEXT_EDITOR,
BRT_Area_Tile_SPREADSHEET,
BRT_Area_Tile_UV,
BRT_Area_Tile_IMAGE,
BRT_Area_Tile_OUTLINER,
BRT_Area_Tile_PROPERTIES,
#BRT_Area_Tile_TEXTURE_NODES,
BRT_Area_Tile_ASSET_BROWSER,
BRT_Area_Tile_SHADER_EDITOR,
BRT_Area_Tile_DRIVERS,
BRT_Area_Tile_FCURVES,
BRT_Area_Tile_GEOMETRY_NODES,
BRT_Area_Tile_INFO,
BRT_Area_Tile_DOPESHEET,
BRT_Area_Tile_TIMELINE,
BRT_Area_Tile_NLA,
BRT_Area_Tile_COMPOSITOR,
BRT_Area_Tile_CONSOLE,
BRT_Area_Tile_CLIP_EDITOR,
BRT_Area_Tile_SEQUENCER,
BRT_Open_ASSETS,
)
def key(dfbool,km,kmi):
    kmi.active = dfbool
    addon_keymaps.append((km, kmi)) 

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
 #KEYMAP
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:    
        km = kc.keymaps.new(name='Screen', space_type='EMPTY')
        key(True,km,km.keymap_items.new("brtwm.brt_area_tile", 'E', 'PRESS', shift=True, alt=True))
        key(True,km,km.keymap_items.new("brtwm.brt_area_close", 'W', 'PRESS', shift=True, alt=True))
        key(True,km,km.keymap_items.new("brtwm.brt_area_swap", 'S', 'PRESS', shift=True, alt=True))
        key(True,km,km.keymap_items.new("brtwm.brt_area_join", 'Q', 'PRESS', shift=True, alt=True))
        
        #key(True,km,km.keymap_items.new("brtwm.tile_area_properties", 'P', 'PRESS', shift=True, oskey=True))
        #key(True,km,km.keymap_items.new("brtwm.tile_area_outliner", 'O', 'PRESS', shift=True, oskey=True))
        #key(True,km,km.keymap_items.new("brtwm.tile_area_view3d", 'V', 'PRESS', shift=True, oskey=True))   
        #key(True,km,km.keymap_items.new("brtwm.tile_area_image", 'I', 'PRESS', shift=True, oskey=True))
        #key(True,km,km.keymap_items.new("brtwm.tile_area_uv", 'U', 'PRESS', shift=True, oskey=True))  
        #key(True,km,km.keymap_items.new("brtwm.tile_area_text_editor", 'T', 'PRESS', shift=True, oskey=True))  
        #key(True,km,km.keymap_items.new("brtwm.tile_area_spreadsheet", 'Y', 'PRESS', shift=True, oskey=True))  
        #key(True,km,km.keymap_items.new("brtwm.tile_area_asset_browser", 'A', 'PRESS', shift=True, oskey=True))                
        #key(True,km,km.keymap_items.new("brtwm.tile_area_shader_editor", 'S', 'PRESS', shift=True, oskey=True))  
        #key(True,km,km.keymap_items.new("brtwm.tile_area_driver", 'D', 'PRESS', shift=True, oskey=True))                
        #key(True,km,km.keymap_items.new("brtwm.tile_area_fcurves", 'F', 'PRESS', shift=True, oskey=True))  
        #key(True,km,km.keymap_items.new("brtwm.tile_area_geo_nodes", 'G', 'PRESS', shift=True, oskey=True))                
        #key(True,km,km.keymap_items.new("brtwm.tile_area_info", 'H', 'PRESS', shift=True, oskey=True))  
        #key(True,km,km.keymap_items.new("brtwm.tile_area_dopesheet", 'J', 'PRESS', shift=True, oskey=True))                
        #key(True,km,km.keymap_items.new("brtwm.tile_area_timeline", 'K', 'PRESS', shift=True, oskey=True))  
        #key(True,km,km.keymap_items.new("brtwm.tile_area_nla", 'L', 'PRESS', shift=True, oskey=True))        
        #key(True,km,km.keymap_items.new("brtwm.tile_area_compositor", 'X', 'PRESS', shift=True, oskey=True))  
        #key(True,km,km.keymap_items.new("brtwm.tile_area_console", 'C', 'PRESS', shift=True, oskey=True))        
        #key(True,km,km.keymap_items.new("brtwm.tile_area_file_browser", 'Q', 'PRESS', shift=True, oskey=True))        

        key(True,km,km.keymap_items.new("brtwm.open_window_asset_browser", 'NUMPAD_7', 'PRESS', shift=True, oskey=True))  

        key(True,km,km.keymap_items.new("brtwm.tile_area_clip_editor", 'N', 'PRESS', shift=True, oskey=True))  
        key(True,km,km.keymap_items.new("brtwm.tile_area_sequencer", 'M', 'PRESS', shift=True, oskey=True))        
        km = kc.keymaps.new('Window', space_type='EMPTY', region_type='WINDOW', modal=False)

def unregister():
    for cls in classes:
        print(str(cls))
        bpy.utils.unregister_class(cls)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()   
if __name__ == "__main__":
    register()    
