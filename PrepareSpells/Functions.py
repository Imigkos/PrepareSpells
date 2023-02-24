import PySimpleGUI as sg
import json

level = 0
modif = 0

class Spell:
    def __init__(self, name, level, text, type):
        self.name = name
        self.level = level
        self.text = text
        self.type = type
        pass


def getCharInfo():  # create window that asks for character level and spellcasting modifier
    spell_list = []
    sg.theme('DarkPurple4')
    layout = [
        [sg.Text('Please enter your Character Name,Spellcasting Modifier and preset file')],
        [sg.Text('Character Level', size=(15, 1)), sg.InputText(key='level')],
        [sg.Text('Spellcasting Modifier', size=(15, 1)),sg.InputText(key='modif')],
        [sg.Submit(), sg.Cancel(),sg.Button('Open Preset',key='open')]
    ]

    window = sg.Window('Prepare Spells', layout)
    event, values = window.read()
    while True:
        if event == 'open':
            spell_list = getPreset()
            didopen = 1
        if event == 'Submit':  # if user clicks submit store values
            level = int(values['level'])
            modif = int(values['modif'])
            break;
        else:  # close window
            break;

    window.close()
    return (spell_list)  # returns how many spellslots the character can have


def getPreset():
    filename = sg.popup_get_file("Open Preset", save_as=False, file_types=(("JSON Files", "*.json"),))
    with open(filename, "r") as file:
        spell_dicts = json.load(file)

# Convert each dictionary back into a Spell object
    spell_list = []
    for spell_dict in spell_dicts:
        spell = Spell(spell_dict["Name"], spell_dict["Text"], spell_dict["Level"], spell_dict["Type"])
        spell_list.append(spell)
    return spell_list


def printSpell(spell):

    sg.Print(f'Level:{spell.level} || Type:{spell.type}\n{spell.text} ')


def addSpell(spell_list):

    layout = [
        [sg.Text('Name:'), sg.InputText(size=(15, 1), key='name'), sg.Text('Type:'), sg.InputText(size=(
            10, 1), key='type'), sg.Text('Level'), sg.Spin([i for i in range(10)], initial_value=0, key='level')],
        [sg.Multiline(default_text='Enter spell description here',
                      size=(50, 8), key='text')],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Prepare Spells', layout)
    event, values = window.read()
    if event == 'Submit':  # if user clicks submit store values
        spell_list.append(
            Spell(values['name'], values['level'], values['text'], values['type']))
        printSpell(spell_list[len(spell_list)-1])
        window.close()
    else:  # close window
        window.close()

    return (spell_list)


def savePreset(spell_list):
    spell_dicts = []
    for spell in spell_list:
        spell_dict = {
        "Name": spell.name,
        "Text": spell.text,
        "Level": spell.level,
        "Type": spell.type
        }
        spell_dicts.append(spell_dict)
    filename = sg.popup_get_file("Save list as", save_as=True, file_types=(("JSON Files", "*.json"),))
    with open(filename, "w") as file:
        # Write the list to the file using json.dump()
        json.dump(spell_dicts, file,indent=4)


def spellWindow(spell_list):
    sg.theme('DarkPurple4')

    layout = [
        [sg.Text('Spells'), sg.Button('Add Spell'), sg.Button(
            'Remove Spell'), sg.Button('Long Rest')],
        [sg.Column([[sg.Button(spell_list[i].name, key=spell_list[i].name)]for i in range(0, len(spell_list), 2)]),
         sg.Column([[sg.Button(spell_list[i].name, key=spell_list[i].name)]for i in range(1, len(spell_list), 2)])],
        [sg.Exit(), sg.Button('Save As', key='save')]
    ]

    window = sg.Window('Spells', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            return (1)
        elif event == 'Add Spell':
            addSpell(spell_list)
        elif event == 'save':
            savePreset(spell_list)
        else:
            for i in range(len(spell_list)):
                if event == spell_list[i].name:
                    printSpell(spell_list[i])

    
