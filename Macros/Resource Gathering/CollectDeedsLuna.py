# Name: Collect BS/Tailor Deeds
# Description: Collects Tailor and BS deeds from Luna NPCs, move them do Bulk Order Book named BS and Tailor respectively  and logout.
# Author: MatheusPPfitscher
# Shard: UOG-Demise
# Date: Sat Oct 12 2024
BODBook = 0x2259  #Bulk Order Book Graphic
TailorDeed = [0x2258, 1155]  #Graphic and Color bulk order deed tailor
BSDeed = [0x2258, 1102]  #Graphic and Color bulk order deed blacksmith

#Gets Tailor Deed from NPC
WaitForContext(0x9b52a, 1, 2000)
WaitForGump(0x9bade6ea, 2000)
ReplyGump(0x9bade6ea, 1)
Pause(500)

#Gets BS Deed from NPC
WaitForContext(0x9b4f7, 1, 2000)
WaitForGump(0x9bade6ea, 2000)
ReplyGump(0x9bade6ea, 1)
Pause(500)

#Finds and set alias for each BOD book
while FindType(BODBook, -1, "backpack"):
    WaitForProperties("found", 3000)
    if Property("found", "BS"):
        SetAlias("BS_BODBook", "found")
        IgnoreObject("found")
    if Property("found", "Tailor"):
        SetAlias("Tailor_BODBook", "found")
        IgnoreObject("found")
    Pause(700)
#Find and move each Tailor Deed into the Tailor Book
while FindType(TailorDeed[0], -1, "backpack", TailorDeed[1]):
    MoveItem("found", "Tailor_BODBook")
    Pause(700)
#Find and move each BS Deed into the Tailor BS
while FindType(BSDeed[0], -1, "backpack", BSDeed[1]):
    MoveItem("found", "BS_BODBook")
    Pause(700)
ClearIgnoreList()
Logout()
