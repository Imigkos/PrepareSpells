import PySimpleGUI as sg

class Spell:
    def __init__(self,name,level,text,type):
        self.name = name
        self.level = level
        self.text = text
        self.type = type
        pass

def getCharInfo(): #create window that asks for character level and spellcasting modifier
    
    sg.theme('DarkPurple4') 
    layout = [
    [sg.Text('Please enter your Character Name and his Spellcasting Modifier')],
    [sg.Text('Character Level', size =(15, 1)), sg.InputText(key='level')],
    [sg.Text('Spellcasting Modifier', size =(15, 1)), sg.InputText(key='modif')],
    [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Prepare Spells', layout)
    event, values = window.read()
    if event =='Submit': #if user clicks submit store values 
        level = int(values['level'])
        modif = int(values['modif'])
        window.close()
    else:#close window 
        window.close()
    
    return(level+modif) #returns how many spellslots the character can have

def getPreset():
    spell_list = []
    f = open("Healboi.txt","r") #open file
    line = f.readline()#read first line
    line = line[:-1] #remove trailing newline
    while line: #read until eof
        split_line =line.split('#') #split with this delimiter
        spell_list.append(Spell(split_line[0], split_line[1], split_line[2], split_line[3]))
        line = f.readline() #read next line
        line = line[:-1] #remove trailing newline
    f.close
    return spell_list

def spellWindow(spell_list):
    sg.theme =('DarkPurple4')

    layout = [
    [sg.Text('Spells')],
    [sg.Button(spell_list[0].name),sg.Button(spell_list[1].name)]
    ]
    window = sg.Window('Spells', layout)