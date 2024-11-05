# Name: Training
# Description: Training inscription from 30 to 100
# Author: Lissandro
# Shard: UOG-Demise
# Date: Mon Nov 04 2024

# Macro de treino de Inscription para ClassicAssist baseado no guia https://www.uogdemise.com/community/viewtopic.php?f=10&t=108&start=15
# Para treinar tenha reagentes e blank scrols guardados. Usei aproximadamente 3000 blank scrols e entre 1000 e 2000 regs de cada. Usei um talismam 30 inscription bonus
# Preferi fazer um char novo com 50 inscription e deixei focus e medit upar ate 100, junto com 18mr, upou rapidinho. Depois transfira com soulstone, ou faça seu char começando por inscription  pois será bem melhor
# Só dar play e esperar gmzar :)

def check_tools_regs():
    # Verifica e restoca ingots
    if CountType(0x1bf2, 'backpack') < 20:
        MoveType(0x1bf2, 'restockScribe', 'backpack', -1, -1, 0, 0, 50)          
        Pause(1000)
    # Verifica e restoca blank scrols
    if CountType(0xef3, 'backpack') < 3:
        MoveType(0xef3, 'restockScribe', 'backpack', -1, -1, 0, 0, 30)         
        Pause(1000)
    # Fabrica Tinker Tools até ter pelo menos 2
    while CountType(0x1eb8, 'backpack') < 2:
        UseType(0x1eb8)
        WaitForGump(0x38920abd, 3000)
        ReplyGump(0x38920abd, 8)
        WaitForGump(0x38920abd, 3000)
        ReplyGump(0x38920abd, 23)
        Pause(1000)
    # Fabrica Scribe Pens até ter pelo menos 3
    while CountType(0xfbf, 'backpack') < 3:
        UseType(0x1eb8)
        WaitForGump(0x38920abd, 3000)
        ReplyGump(0x38920abd, 8)
        WaitForGump(0x38920abd, 3000)
        ReplyGump(0x38920abd, 156)
        WaitForGump(0x38920abd, 3000)
        Pause(1000)
    # Garante que tem reagentes na bag baseado no nvl
    RECALL_REGS = [0xf7a, 0xf7b, 0xf86] #blackpearl #bloodmoss #mandrake root
    MAGICREFLECTION_REGS = [0xf84, 0xf86, 0xf8d] #garlic #mandrake root #spidersilk
    MARK_REGS = [0xf7b, 0xf7a, 0xf86] #bloodmoss #blackpearl #mandrake root
    FLAMESTRIKE_REGS = [0xf8d, 0xf8c] #spidersilk #sulfurous ash
    RESSURRECTION_REGS = [0xf7b, 0xf84, 0xf85] #bloodmoss #garlic #ginseng
    if Skill('Inscription') < 30:
        HeadMsg('not enough skill!', 33)
        Stop()
    elif Skill('Inscription') < 55:        
        for regs in RECALL_REGS:        
            if CountType(regs, 'backpack') < 2:            
                MoveType(regs, 'restockScribe', 'backpack', -1, -1, 0, 0, 30)         
                Pause(1000)
    elif Skill('Inscription') < 65:        
        for regs in MAGICREFLECTION_REGS:        
            if CountType(regs, 'backpack') < 2:            
                MoveType(regs, 'restockScribe', 'backpack', -1, -1, 0, 0, 30)         
                Pause(1000)                
    elif Skill('Inscription') < 85:        
        for regs in MARK_REGS:        
            if CountType(regs, 'backpack') < 2:            
                MoveType(regs, 'restockScribe', 'backpack', -1, -1, 0, 0, 30)         
                Pause(1000)                
    elif Skill('Inscription') < 94:        
        for regs in FLAMESTRIKE_REGS:        
            if CountType(regs, 'backpack') < 2:            
                MoveType(regs, 'restockScribe', 'backpack', -1, -1, 0, 0, 30)         
                Pause(1000)    
    elif Skill('Inscription') < 100:        
        for regs in RESSURRECTION_REGS:        
            if CountType(regs, 'backpack') < 2:            
                MoveType(regs, 'restockScribe', 'backpack', -1, -1, 0, 0, 30)         
                Pause(1000)    
                

    
################  MACRO START

# Configuração inicial
if not FindAlias('restockScribe'):
    HeadMsg('Aponte a caixa com scrolls, reagentes e ingots', 33)
    PromptAlias('restockScribe')
    UseObject('restockScribe')


# Verifica e restoca scrolls
check_tools_regs()

#verifica mana e usa medit até ficar full
if Mana("self") < 20:  
    while Mana() < MaxMana("self"):
        if not BuffExists("Active Meditation"):
            UseSkill("Meditation")
            Pause(1000)

# Verifica o nível de skill e fabrica os itens de acordo com o nível

if Skill('Inscription') < 30:
    HeadMsg('Buy more skill!', 33)
    Stop()

elif Skill('Inscription') < 55: #RECALL_SCROLL
    UseType(0xfbf)
    WaitForGump(0x38920abd, 3000)
    ReplyGump(0x38920abd, 22)
    WaitForGump(0x38920abd, 3000)    
    ReplyGump(0x38920abd, 51)    
    Pause(1000)
    if CountType(0x1f4c, 'backpack') > 0: #RECALL_SCROLL
        MoveType(0x1f4c, 'backpack', 'restockScribe')        
        UseObject(0x42f8845a)
        
elif Skill('Inscription') < 65: #MAGIC REFLECTION SCROLL
    UseType(0xfbf)              
    WaitForGump(0x38920abd, 3000)
    ReplyGump(0x38920abd, 29)
    WaitForGump(0x38920abd, 3000)
    ReplyGump(0x38920abd, 23)
    WaitForGump(0x38920abd, 3000)    
    Pause(1000)  
    if CountType(0x1f50, 'backpack') > 0: #MAGIC REFLECTION SCROLL
        MoveType(0x1f50, 'backpack', 'restockScribe')
elif Skill('Inscription') < 85: #MARK SCROLL
    UseType(0xfbf)              
    WaitForGump(0x38920abd, 3000)             
    ReplyGump(0x38920abd, 36)
    WaitForGump(0x38920abd, 3000)
    ReplyGump(0x38920abd, 30)
    WaitForGump(0x38920abd, 3000)    
    Pause(1000)  
    if CountType(0x1f59, 'backpack') > 0: #MARK SCROLL
        MoveType(0x1f59, 'backpack', 'restockScribe')   
elif Skill('Inscription') < 94: #FLAMESTRIKE SCROLL
    UseType(0xfbf)              
    WaitForGump(0x38920abd, 3000)             
    ReplyGump(0x38920abd, 43)
    WaitForGump(0x38920abd, 5000)
    ReplyGump(0x38920abd, 16)
    WaitForGump(0x38920abd, 5000)
    Pause(1000)
    if CountType(0x1f5f, 'backpack') > 0: #FLAMESTRIKE SCROLL
        MoveType(0x1f5f, 'backpack', 'restockScribe')     
elif Skill('Inscription') < 100: #RESSURRECTION SCROLL
    UseType(0xfbf)              
    WaitForGump(0x38920abd, 3000)             
    ReplyGump(0x38920abd, 50)
    WaitForGump(0x38920abd, 3000)
    ReplyGump(0x38920abd, 16)
    WaitForGump(0x38920abd, 3000)
    Pause(1000)
    if CountType(0x1f67, 'backpack') > 0: #RESSURRECTION SCROLL
        MoveType(0x1f67, 'backpack', 'restockScribe')          
        ReplyGump(0x38920abd, 50)
elif Skill('Inscription') >= 100:
    Msg("CHEGA NÉ! AGORA VOCÊ É GM INSCRIPTION")
    stop()
