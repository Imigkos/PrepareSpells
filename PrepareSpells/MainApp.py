import PySimpleGUI as sg
import Functions as f

spell_list = f.getCharInfo();
print(f.level+f.modif)
exitapp = 0


while exitapp == 0:   
    exitapp = f.spellWindow(spell_list)
    


