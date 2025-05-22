# Name: Carpentry from 30 to 100
# Description: This macro is designed to help you level up your Carpentry skill.
#   Before starting, make sure you have the following:
#   *A container filled with boards
#   *A container holding your carpentry tools(default: nails)
#   *A destination container (can be a trash can or any other container for dumping crafted items)
#   When you run the macro, it will prompt you to select each of these containers. 
#   Once they're set and your supplies are in place, you're ready to begin.
# Author: angeloghiotto
# Shard: The crossroads 
# Date: Thu May 22 2025

SysMessage("SET RESOURCE CONTAINER(boards)")
PromptMacroAlias("resourceContainer") 
SysMessage("SET TOOL CONTAINER")
PromptMacroAlias("toolsContainer") 
SysMessage("SET FINAL GOODS CONTAINER")
PromptMacroAlias("finalGoodsContainer") #TRASH if you don't want to keep them


#---CONFIGURATION---#
carpenterTool = 0x102e; #nails
board = 0x1bd7;
woodColors = [0]; #normal wood -> 0, Oak -> 2010 - It will try to get the first item if not the second and so on(separeted by comma) ex [0,2010] it accepts all types of wood
waitingDelay = 600; #increase that if you ping is high
#----DON'T EDIT BELOW UNLESS NECESSARY---#
carpenterGump = 0x38920abd
itemStages = [
    [15, 2, 0x9aa],#container/woodem box
    [8, 37, 0xb53],#furniture/trinsic chair
    [43, 128, 0x14f0], #Misc. Add-ons/ballot box
    [22, 30, 0x27aa], #Weapons/fukiya
    [22, 23, 0x27a8], #Weapons/bokuto
    [22, 2, 0xe81], #Weapons/Sheppard Crook
    [22, 37, 0x27a6] #Weapons/Tetsubo
]


def grabTool():
    if not FindType(carpenterTool, -1, 'backpack'):
        UseObject("toolsContainer")  
        Pause(waitingDelay)
        if FindType(carpenterTool, -1, "toolsContainer"):
            MoveItem("found", "backpack")
            Pause(waitingDelay)
        else:
            SysMessage("No tools")
            Stop()

def grabWood():
    UseObject("resourceContainer")  
    Pause(waitingDelay)
    found = 0;
    freeSpace = MaxWeight() - Weight() - 50;
    for color in woodColors:
        if FindType(board, -1, "resourceContainer", color, freeSpace):
            MoveItem("found", "backpack", freeSpace);
            found = 1;
            break;
    if found == 0:
        SysMessage("Not enough wood");
        Stop();

def storeItem(itemStage):
    Pause(waitingDelay)
    if FindType(itemStages[itemStage][2], -1, "self"):
        MoveItem("found", "finalGoodsContainer")
        
def makeItem(itemStage):
    Pause(waitingDelay)
    grabTool()
    UseType(carpenterTool)
    WaitForGump(carpenterGump, 5000)
    ReplyGump(carpenterGump, itemStages[itemStage][0])
    WaitForGump(carpenterGump, 5000)
    ReplyGump(carpenterGump, itemStages[itemStage][1])
    WaitForGump(carpenterGump, 5000)
    if InGump(carpenterGump, "You do not have sufficient wood"):
        grabWood()
        makeItem(itemStage)
    storeItem(itemStage)
    return True

carpSkill = Skill("carpentry")
while carpSkill < 100:
    carpSkill = Skill("carpentry")
    if carpSkill < 43:
        makeItem(0)
    elif carpSkill < 48:
        makeItem(1)
    elif carpSkill < 65:
        makeItem(2)
    elif carpSkill < 72:
        makeItem(3)
    elif carpSkill < 79:
        makeItem(4)
    elif carpSkill < 95:
        makeItem(5)
    elif carpSkill < 100:
        makeItem(6)
    else:
        SysMessage("Macro ended, thank you")



