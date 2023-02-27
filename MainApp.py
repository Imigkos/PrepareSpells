import PySimpleGUI as sg
import Functions as f

spell_list, item_list = f.getPreset();
exitapp = 0


while exitapp == 0:   
    exitapp = f.spellWindow(spell_list,item_list)
    


