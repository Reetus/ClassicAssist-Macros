# Name: Collect BS/Tailor Deeds
# Description: Collects Tailor and BS deeds from Luna NPCs, move them do BOD named BS and Tailor respectively  and logout.
# Author: MatheusPPfitscher
# Shard: UOG-Demise
# Date: Sat Oct 05 2024

BOD = 0x2259
TailorDeed = [0x2258,1155] #Graphic and Color
BSDeed = [0x2258,1102]

WaitForContext(0x9b52a, 1, 2000)
WaitForGump(0x9bade6ea, 2000)
ReplyGump(0x9bade6ea, 1)
Pause(500)

WaitForContext(0x9b4f7, 1, 2000)
WaitForGump(0x9bade6ea, 2000)
ReplyGump(0x9bade6ea, 1)
Pause(500)

ClearIgnoreList()  

while FindType(BOD,-1,"backpack"):
    WaitForProperties("found",5000)
    if Property("found","BS"):
        SetAlias("BS_BOD", "found")  
        IgnoreObject("found")
    if Property("found","Tailor"):
        SetAlias("Tailor_BOD","found")
        IgnoreObject("found")
    Pause(700)

while FindType(TailorDeed[0],-1,"backpack",TailorDeed[1]):
    MoveItem("found","Tailor_BOD")
    Pause(700)
    
while FindType(BSDeed[0],-1,"backpack",BSDeed[1]):
    MoveItem("found","BS_BOD")
    Pause(700)

ClearIgnoreList()  
Logout()