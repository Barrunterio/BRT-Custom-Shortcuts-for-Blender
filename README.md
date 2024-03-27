Set of Personal Shorcuts for Navigation

<kbd>Alt + Shift + E</kbd> Divide Window by Half

<kbd>Alt + Shift + S</kbd> Swap Areas by Cursor Coordinate Context

<kbd>System Key + Shift + NUMPAD 7</kbd> New Window File Browser

This convination is recomended to be used with:

```python
import bpy
wm = bpy.context.window_manager
kc = wm.keyconfigs.user
km = kc.keymaps['Screen']
kmi = km.keymap_items.new('screen.area_close', 'W', 'PRESS', shift=True, alt=True)

kmi = km.keymap_items.new('screen.area_split', 'LEFTMOUSE', 'PRESS', ctrl=True, oskey=True)
kmi.properties.direction='VERTICAL'
kmi = km.keymap_items.new('screen.area_split', 'RIGHTMOUSE', 'PRESS', ctrl=True, oskey=True)
kmi.properties.direction='HORIZONTAL'
´´´
