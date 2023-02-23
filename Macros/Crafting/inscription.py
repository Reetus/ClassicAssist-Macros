# Name: Inscription
# Description: Inscription até 100.0
# Author: matthewsmmatta
# Era: Any
# Date: Thu Feb 23 2023

FindType(0xfbf, 0, "backpack") #PEN AND INK
UseObject('found')
ReplyGump(0x484, 1) # PRIMEIRO CÍRCULO
WaitForGump(0x484, 5000)
ReplyGump(0x484, 10106) # MAGIC ARROW
WaitForGump(0x484, 5000)
Pause(3000)
