import PySimpleGUI as sg
import json
import requests

level = 0
modif = 0

class Spell:
    def __init__(self, name,text, level, type):
        self.name = name
        self.text = text
        self.level = level
        self.type = type
        pass


def getCharInfo():  # create window that asks for character level and spellcasting modifier
    global level,modif
    spell_list = []
    sg.theme('DarkBlue1')
    layout = [
        [sg.Text('Please enter your Character Name,Spellcasting Modifier and preset file')],
        [sg.Text('Character Level', size=(15, 1)), sg.InputText(key='level')],
        [sg.Text('Spellcasting Modifier', size=(15, 1)),sg.InputText(key='modif')],
        [sg.Submit(), sg.Cancel(),sg.Button('Open Preset',key='open')]
    ]

    window = sg.Window('Prepare Spells', layout)
    while True:
        event, values = window.read()
        if event == 'open':
            spell_list = getPreset()
        elif event == 'Submit':  # if user clicks submit store values
            if values['level'] and values['modif']:
                level = int(values['level'])
                modif = int(values['modif'])
            break;
        else:  # close window
            exit(0)

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

    sg.popup(f'Level:{spell.level} || Type:{spell.type}\n\n{spell.text} ',title=spell.name)

def apiJSONparse(spell):
    url = 'https://www.dnd5eapi.co/api/spells/'+spell
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        name = data['name']
        text = str(data['desc'])+'\n\n'+str(data['higher_level'])
        text = text.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
        level = data['level']
        if data['ritual'] == False:
            if data['concentration'] == False:
                type = data['duration']+','+data['casting_time']
            else:
                type = data['duration']+','+'concetration'+','+data['casting_time']
        else:        
            type = data['duration']+','+'ritual'+','+data['casting_time']
        parsed_spell = Spell(name,text,level,type)
        return parsed_spell          
    else:
        sg.popup('Can not access api or spell not found')
        return None
          

def searchAPI(spell_list):
    layout = [
        [sg.Text('Enter the name of the spell you want to search:')],
        [sg.InputText(size=(15, 1), key='spell_search')],
        [sg.Submit(),sg.Cancel()]
    ]
    
    window = sg.Window('Search',layout)
    event,values = window.read()
    if event == 'Cancel':
        window.close()
    elif event == 'Submit':
        spell_search = values['spell_search']
        spell_search =spell_search.lower().replace(' ','-')
        new_spell = apiJSONparse(spell_search)
        if new_spell:
            spell_list.append(new_spell)
        window.close()

        

def addSpell(spell_list):

    layout = [
        [sg.Text('Name:'), sg.InputText(size=(15, 1), key='name'), sg.Text('Type:'), sg.InputText(size=(
            10, 1), key='type'), sg.Text('Level'), sg.Spin([i for i in range(1,11)], initial_value=1, key='level')],
        [sg.Multiline(default_text='Enter spell description here',
                      size=(50, 8), key='text')],
        [sg.Submit(),sg.Button('Search'), sg.Cancel()]
    ]

    window = sg.Window('Prepare Spells', layout)
    event, values = window.read()
    if event == 'Submit':  # if user clicks submit store values
        spell_list.append(Spell(values['name'], values['text'], values['level'], values['type']))
        printSpell(spell_list[len(spell_list)-1])
        window.close()
    elif event == 'Search':
        searchAPI(spell_list)
        window.close()
    else:  # close window
        window.close()

    return (spell_list)

def removeSpell(spell_list):
    layout = [
        [sg.Text('Click on the spell you want to remove')],
        [sg.Column([[sg.Button(spell_list[i].name, key=spell_list[i].name)]for i in range(0, len(spell_list), 2)]),
         sg.Column([[sg.Button(spell_list[i].name, key=spell_list[i].name)]for i in range(1, len(spell_list), 2)])],
        [sg.Submit(),sg.Cancel()]
    ]
    window = sg.Window('Remove Spell',layout)
    default_color = sg.theme_button_color()
    selectedSpell=''
    while True:
        event, values = window.read()
        if event != 'Submit' and event!='Cancel':
            if selectedSpell:
                window[selectedSpell].update(button_color=default_color)
            selectedSpell = event
            window[selectedSpell].update(button_color=('white', '#00008B'))
        if event == 'Submit':
            for spell in spell_list:
                if spell.name == selectedSpell:
                    spell_list.remove(spell)
            break
        elif event == 'Cancel':
            break
    window.close()
    


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
    sg.theme('DarkBlue1')
    
    layout = [
        [sg.Text('Spells'), sg.Button('Add Spell'), sg.Button(
            'Remove Spell',key='remove'), sg.Button('Long Rest')],
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
            window.close()
            addSpell(spell_list)
            spellWindow(spell_list)
        elif event == 'save':
            savePreset(spell_list)
        elif event == 'remove':
            window.close()
            removeSpell(spell_list)
            spellWindow(spell_list)
        else:
            for i in range(len(spell_list)):
                if event == spell_list[i].name:
                    printSpell(spell_list[i])

    
