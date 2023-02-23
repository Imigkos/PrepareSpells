import PySimpleGUI as sg
import Functions as f
import json
  

Slots = f.getCharInfo();
print(Slots);
spell_list = []
spell_list = f.getPreset();
for i in range(len(spell_list)):
    print(f'Spell Name:{spell_list[i].name}')
    print(f'Spell Level:{spell_list[i].level}')
    print(f'Spell Text:{spell_list[i].text}')
    print(f'Spell Type:{spell_list[i].type}')
    
f.spellWindow(spell_list)


