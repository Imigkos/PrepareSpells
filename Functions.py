import PySimpleGUI as sg
import json
import requests
import threading

level = 0
modif = 0


class Spell:
    def __init__(self, name, text, level, type):
        self.name = name
        self.text = text
        self.level = level
        self.type = type
        pass


class Item:
    def __init__(self, name, descr, quantity):
        self.name = name
        self.descr = descr
        self.quantity = quantity
        pass


def getPreset():
    spell_list = []
    item_list = []
    sg.theme('DarkBlue1')
    filename = sg.popup_get_file(
        "Open Preset(Click ok for empty)", save_as=False, file_types=(("JSON Files", "*.json"),))
    if filename:
        with open(filename, "r") as file:
            preset_dict = json.load(file)
    else:
        return spell_list, item_list

      # Parse spell information from the "Spells" key
    spell_dicts = preset_dict["Spells"]
    spell_list = [Spell(spell_dict["Name"], spell_dict["Text"],
                        spell_dict["Level"], spell_dict["Type"]) for spell_dict in spell_dicts]

    # Parse inventory item information from the "Inventory" key
    item_dicts = preset_dict["Inventory"]
    item_list = [Item(item_dict["Name"], item_dict["Description"],
                      item_dict["Quantity"]) for item_dict in item_dicts]

    return spell_list, item_list


def printSpell(spell):
    layout = [
        [sg.Text(f'Level:{spell.level} || Type:{spell.type}\n\n{spell.text}',
                 auto_size_text=True, size=(65, None))],
        
        [sg.Button('Cast at level:'),sg.Spin(values=[i for i in range(spell.level,10)], initial_value=spell.level, key='level'), sg.Button('Back')]
    ]
    popup_window = sg.Window(f'{spell.name}', layout, keep_on_top=True)
    button, values = popup_window.read()
    if button == 'Cast at level:':
        level = int(values['level']) 
        popup_window.close()
        return (level)
    else:
        popup_window.close()
        return (-1)


def apiJSONparse(spell):
    url = 'https://www.dnd5eapi.co/api/spells/'+spell

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        name = data['name']
        text = str(data['desc'])+'\n\n'+str(data['higher_level'])
        text = text.replace('[', '').replace(']', '').replace(
            '"', '').replace("'", '')
        level = data['level']
        if data['ritual'] == False:
            if data['concentration'] == False:
                type = data['duration']+','+data['casting_time']
            else:
                type = data['duration']+',' + \
                    'concetration'+','+data['casting_time']
        else:
            type = data['duration']+','+'ritual'+','+data['casting_time']
        parsed_spell = Spell(name, text, level, type)
        return parsed_spell
    else:
        sg.popup('Can not access api or spell not found')
        return None


def searchAPI(spell_list):
    layout = [
        [sg.Text('Enter the name of the spell you want to search:')],
        [sg.InputText(size=(15, 1), key='spell_search')],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Search', layout, keep_on_top=True)
    event, values = window.read()
    if event == 'Cancel':
        window.close()
    elif event == 'Submit':
        spell_search = values['spell_search']
        spell_search = spell_search.lower().replace(' ', '-')
        new_spell = apiJSONparse(spell_search)
        if new_spell:
            spell_list.append(new_spell)
        window.close()


def addSpell(spell_list):

    layout = [
        [sg.Text('Name:'), sg.InputText(size=(15, 1), key='name'), sg.Text('Type:'), sg.InputText(size=(
            10, 1), key='type'), sg.Text('Level'), sg.Spin([i for i in range(1, 11)], initial_value=1, key='level')],
        [sg.Multiline(default_text='Enter spell description here',
                      size=(50, 8), key='text')],
        [sg.Submit(), sg.Button('Search'), sg.Cancel()]
    ]

    window = sg.Window('Prepare Spells', layout, keep_on_top=True)
    event, values = window.read()
    if event == 'Submit':  # if user clicks submit store values
        spell_list.append(
            Spell(values['name'], values['text'], values['level'], values['type']))
        window.close()
    elif event == 'Search':
        searchAPI(spell_list)
        window.close()
    else:  # close window
        window.close()

    return (spell_list)


def addItem(item_list):
    layout = [
        [sg.Text('Name:'), sg.InputText(size=(15, 1), key='name'), sg.Text(
            'Quantity:'), sg.InputText(size=(5, 1), key='quantity')],
        [sg.Multiline(default_text='Enter item description here',
                      size=(50, 8), key='descr')],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('Add Item', layout, keep_on_top=True)
    event, values = window.read()
    if event == 'Submit':  # if user clicks submit store values
        item_list.append(
            Item(values['name'], values['descr'], int(values['quantity'])))
        window.close()
    else:  # close window
        window.close()
    return item_list


def removeSpell(spell_list):
    layout = [
        [sg.Text('Click on the spell you want to remove')],
        [sg.Column([[sg.Button(spell_list[i].name, key=spell_list[i].name)]for i in range(0, len(spell_list), 2)]),
         sg.Column([[sg.Button(spell_list[i].name, key=spell_list[i].name)]for i in range(1, len(spell_list), 2)])],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('Remove Spell', layout)
    default_color = sg.theme_button_color()
    selectedSpell = ''
    while True:
        event, values = window.read()
        if event != 'Submit' and event != 'Cancel':
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


def savePreset(spell_list, item_list):
    spell_dicts = []
    for spell in spell_list:
        spell_dict = {
            "Name": spell.name,
            "Text": spell.text,
            "Level": spell.level,
            "Type": spell.type
        }
        spell_dicts.append(spell_dict)
    inventory_dicts = []
    for item in item_list:
        inventory_dict = {
            "Name": item.name,
            "Description": item.descr,
            "Quantity": item.quantity
        }
        inventory_dicts.append(inventory_dict)
    filename = sg.popup_get_file("Save list as", save_as=True, file_types=(
        ("JSON Files", "*.json")), keep_on_top=True)
    with open(filename, "w") as file:
        # Write the list to the file using json.dump()
        json.dump({"Spells": spell_dicts,
                  "Inventory": inventory_dicts}, file, indent=4)


def openInventory(item_list):
    inventory = [[item.name, item.quantity] for item in item_list]
    layout = [
        [sg.Table(values=inventory, headings=['Item', 'Quantity',], display_row_numbers=False, enable_events=True, key='table', col_widths=[20, 10, 5],
                  row_height=30, tooltip='Click on an item to get its description',
                  selected_row_colors=(('white', sg.theme_background_color())),
                  auto_size_columns=True, justification='center')],
        [sg.Button('Add Item', key='add')]
    ]

    window = sg.Window('Inventory', layout, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif 'table' in values and values['table']:
            selected_row = values['table'][0]
            item = item_list[selected_row]
            layout = [
                [sg.Text(f"{item.descr}")],
                [sg.Input(key='quantity', default_text='1', size=5),
                 sg.Button('Increase'), sg.Button('Decrease'), sg.Button('Delete')]
            ]
            popup_window = sg.Window(f'{item.name}', layout, keep_on_top=True)
            button, values = popup_window.read()
            popup_window.close()
            if button == 'Increase':
                # increase the quantity of the selected item
                item.quantity += int(values['quantity'])
            elif button == 'Decrease':
                # decrease the quantity of the selected item
                if item.quantity >= int(values['quantity']):
                    item.quantity -= int(values['quantity'])
                else:
                    sg.popup('Cannot decrease quantity below zero.')
            elif button == 'Delete':
                item_list.remove(item)
        elif event == 'add':
            item_list = addItem(item_list)
        inventory = [[item.name, item.quantity] for item in item_list]
        window['table'].update(values=inventory)
    window.close()
    return (item_list)


def spellWindow(spell_list, item_list):
    sg.theme('DarkBlue1')
    spell_slots = []
    for i in range(10):
        spell_slots.append(0)

    layout = [
        [sg.Button('Add Spell'), sg.Button('Remove Spell', key='remove'), sg.Button(
            'Inventory', key='inventory'), sg.Button('Rest', key='rest')],
        [sg.Column([[sg.Button(spell_list[i].name, key=spell_list[i].name)]for i in range(0, len(spell_list), 2)]),
         sg.Column([[sg.Button(spell_list[i].name, key=spell_list[i].name)]for i in range(1, len(spell_list), 2)])],
        [sg.Text('Max HP:'), sg.Input(size=(3, 1), key='maxhp', default_text='0'), sg.Text('Current HP:'), sg.Input(size=(3, 1), key='currenthp', default_text='0'), sg.Text(
            'Temp:'), sg.Input(size=(3, 1), key='temphp', default_text='0'), sg.Button('Damage', key='dmg'), sg.Input(size=(3, 1), key='dmghp', default_text='0')],
        [sg.Text(f'Level 0:'), sg.Input('0', size=(3, 1), key='l0'), sg.Text(f'Level 1:'), sg.Input('0', size=(3, 1), key='l1'), sg.Text(f'Level 2:'), sg.Input(
            '0', size=(3, 1), key='l2'), sg.Text(f'Level 3:'), sg.Input('0', size=(3, 1), key='l3'), sg.Text(f'Level 4:'), sg.Input('0', size=(3, 1), key='l4')],
        [sg.Canvas(size=(500, 1), background_color='lightgray', key='canvas1')],
        [sg.Text(f'Level 5:'), sg.Input('0', size=(3, 1), key='l5'), sg.Text(f'Level 6:'), sg.Input('0', size=(3, 1), key='l6'), sg.Text(f'Level 7:'), sg.Input(
            '0', size=(3, 1), key='l7'), sg.Text(f'Level 8:'), sg.Input('0', size=(3, 1), key='l8'), sg.Text(f'Level 9:'), sg.Input('0', size=(3, 1), key='l9')],
        [sg.Canvas(size=(500, 1), background_color='lightgray', key='canvas2')],
        [sg.Exit(), sg.Button('Save As', key='save'),
         sg.Button('Store Max Spell Slots', key='store')],
    ]

    window = sg.Window('DND Manager', layout, keep_on_top=True)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            return (1)
        elif event == 'Add Spell':
            window.close()
            addSpell(spell_list)
            spellWindow(spell_list, item_list)
        elif event == 'save':
            savePreset(spell_list, item_list)
        elif event == 'remove':
            window.close()
            removeSpell(spell_list)
            spellWindow(spell_list, item_list)
        elif event == 'inventory':
            item_list = openInventory(item_list)
        elif event == 'dmg':
            maxHP = int(values['maxhp'])
            curHP = int(values['currenthp'])
            tempHP = int(values['temphp'])
            dmgHP = int(values['dmghp'])
            if dmgHP >= tempHP:
                dmgHP -= tempHP
                tempHP = 0
            else:
                tempHP -= dmgHP
                dmgHP = 0
            curHP -= dmgHP
            window['maxhp'].update(str(maxHP))
            window['currenthp'].update(str(curHP))
            window['temphp'].update(str(tempHP))
        elif event == 'store':
            for i in range(10):
                spell_slots[i] = int(values[f'l{i}'])
        elif event == 'rest':
            for i in range(10):
                window[f'l{i}'].update(str(spell_slots[i]))
        else:
            for i in range(len(spell_list)):
                if event == spell_list[i].name:
                    castLevel = printSpell(spell_list[i])
                    if castLevel >= 0:
                        window[f'l{castLevel}'].update(
                            str(int(values[f'l{castLevel}'])-1))
