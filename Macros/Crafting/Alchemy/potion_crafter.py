# Name: Potion Factory
# Description: Crafts the selected potion up to the selected maximum amount
# Author: Reetus
# Shard: UO Heritage

import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine

makeMax = 2500
makeCount = 0
craftGumpId = 0x38920abd

if not FindAlias('resChest'):
	resChest = PromptAlias('resChest')

def Tinker(category, button):
	UseType(0x1eb8)	
	ReplyGump(craftGumpId, category)
	WaitForGump(craftGumpId, 5000)
	ReplyGump(craftGumpId, button)
	WaitForGump(craftGumpId, 5000)

class PotionInfo:
	def __init__(self, name, itemid, hue, gumpButton1, gumpButton2, reagent):
		self.name = name
		self.itemid = itemid
		self.hue = hue
		self.gumpButton1 = gumpButton1
		self.gumpButton2 = gumpButton2
		self.reagent = reagent

potionInfo = [
	PotionInfo("Greater Cure", 0xf07, 0, 1, 51, 0xf84),
	PotionInfo("Greater Heal", 0xf0c, 0, 1, 30, 0xf85),
	PotionInfo("Greater Poison", 0xf0a, 0, 15, 16, 0xf88),
	PotionInfo("Greater Refreshment", 0xf0b, 0, 1, 9, 0xf7a)
]

(res, selection) = SelectionPrompt(potionInfo.Select(lambda i: i.name))

if not res:
	Stop()

info = potionInfo[selection]


(res, name) = MessagePrompt("Amount?", str(makeMax))

if not res:
	Stop()

makeMax = int(name)

makeCount = CountType(info.itemid, "backpack")
makeCount = makeCount + CountType(info.itemid, GetAlias('resChest'))

while makeCount < makeMax:
	
	print makeCount
	
	count = CountType(info.reagent, "backpack")
	
	# Reagent
	if count < 100:
		MoveType(info.reagent, GetAlias('resChest'), "backpack", -1, -1, -1, 0, 100)
	
	# Tinker Tools
	count = CountType(0x1eb8, 'backpack')
	
	if count < 3:
		Tinker(15, 23)
	
	# Mortar and pestal
	count = CountType(0xe9b, 'backpack')

	if count < 3:
		Tinker(15, 9)
		
	# Bottles
	count = CountType(0xf0e, 'backpack')
	
	if count < 20:
		MoveType(0xf0e, GetAlias('resChest'), 'backpack', -1, -1, -1, 0, 20)
		Pause(1000)
		
	UseType(0xe9b)
	WaitForGump(craftGumpId, 5000)
	ReplyGump(craftGumpId, info.gumpButton1)
	WaitForGump(craftGumpId, 5000)
	ReplyGump(craftGumpId, info.gumpButton2)
	WaitForGump(craftGumpId, 5000)
	
	res,gump = Engine.Gumps.GetGump(craftGumpId)
	
	if res:
		#X: 170, Y: 295, Type: xmfhtmlgumpcolor, Cliloc: 500279, Text: You pour the potion into a bottle...
		ele = gump.Pages[0].GetElementByXY(170, 295)
		
		if ele != None and ele.Cliloc == 500279:
			makeCount = makeCount + 1
			
	if Weight() > MaxWeight() - 100:
		MoveType(info.itemid, "backpack", resChest)
		Pause(2000)
		
print 'Finished'
