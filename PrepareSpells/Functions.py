import PySimpleGUI as sg

class Spell:
    def __init__(self,name,level,text,type):
        self.name = name
        self.level = level
        self.text = text
        self.type = type
        pass

def getCharInfo():
    
    sg.theme('DarkPurple4') 
    layout = [
    [sg.Text('Please enter your Character Name and his Spellcasting Modifier')],
    [sg.Text('Character Level', size =(15, 1)), sg.InputText(key='level')],
    [sg.Text('Spellcasting Modifier', size =(15, 1)), sg.InputText(key='modif')],
    [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Prepare Spells', layout)
    event, values = window.read()
    if event =='Submit':
        level = int(values['level'])
        modif = int(values['modif'])
        window.close()
    else:
        window.close()
    
    return(level+modif)

def getPreset():
    f = open("Healboi.txt","r")
    data = f.read()
    f.writelines