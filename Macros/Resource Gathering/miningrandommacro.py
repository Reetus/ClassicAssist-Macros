# Name: Mining Random Macro
# Description: #MACRO MINER RANDOM ULTIMA MEMENTO/ODYSSEY/RNR
#Feito por WillxD
#Adaptado por Matayos
# Author: Matayosl
# Shard: Memento/Odyssey/RnR
# Date: Sat Sep 27 2025

#MACRO MINER RANDOM ULTIMA MEMENTO/ODYSSEY/RNR
#Feito por WillxD
#Adaptado por Matayos

import clr
import System
from Assistant import Engine
from ClassicAssist.UO.Data import Statics
from ClassicAssist.UO import UOMath
from System import Convert
from System import Random

# Se precisar que o usuário selecione o packlhama, descomente a linha abaixo
# PromptAlias('Packlhama') 
SetAlias('Packlhama', 0x1d3e) # Se o ID do packlhama for fixo, pode manter assim

def guardar():
    HeadMsg("Peso alto! Guardando minérios...")
    # Loop para encontrar e mover todo o minério para o packlhama
    while FindType(0x19b9, -1, 'backpack'):
        ore = GetAlias('found')
        MoveItem(ore, GetAlias('Packlhama'))
        Pause(600) # Pausa para evitar sobrecarregar o servidor
    # A função termina quando não há mais minério na mochila
    return

def Mine():
    HeadMsg("Minerando...")
    ClearJournal()
    while not InJournal('There is no metal here to mine.'):
        # Verifica se a ferramenta se desgastou
        if InJournal('You have worn out your tool!'):
            ClearJournal() # Limpa o journal para a próxima verificação
            HeadMsg("Equipando nova picareta...")
            # Adicione aqui a lógica para equipar uma nova picareta, se necessário
            # Ex: UseType(0x0E85, 0x0000, 'backpack')
            Pause(1000)

        UseType(0xf39) # Usa a picareta
        WaitForTarget(2000)
        TargetTileOffsetResource(0, 0, 0)
        Pause(1200) # Pausa para o ciclo de mineração
        
        # >>> INÍCIO DA MODIFICAÇÃO <<<
        # Verifica se o peso atual é 300 ou mais
        if Weight() >= 300:
            guardar() # Se for, chama a função para guardar os itens
        # >>> FIM DA MODIFICAÇÃO <<<

    HeadMsg("Movendo para proximo local...")
    
    return

# --- Início do Script ---

# Lista de direções para movimento aleatório
rand = [ 'East', 'West', 'North', 'South', 'Northeast', 'Southeast', 'Southwest', 'Northwest' ]
rando = Random()

ClearIgnoreList()

while True:
    Mine()
    # Move-se uma vez em uma direção aleatória
    Run(rand[rando.Next(8)])
    # Anda 3 passos na mesma direção para se afastar mais
    Run(Direction('self'))
    Run(Direction('self'))
    Run(Direction('self'))
    