# Name: Tailor BOD Filler
# Description: This will fill all Tailor BODs from a Source BOD Book. Set your filter on this book to pull only the BODs you want filled.
# Author: raveX
# Era: Any

SetQuietMode(True)

if not FindAlias('tailor bod source'):
  	PromptAlias('tailor bod source')

if not FindAlias('tailor bod destination'):
  	PromptAlias('tailor bod destination')

if not FindAlias('tailor bod filler restock'):
  	PromptAlias('tailor bod filler restock')
  	
class CraftableItem:
	def __init__(self, graphic, gumpResponse1, gumpResponse2):
		self.graphic = graphic
		self.gumpResponse1 = gumpResponse1
		self.gumpResponse2 = gumpResponse2


# *****MISC******
errorTextColor = 33
craftBoneArmor = True
craftStuddedArmor = True

# *****GUMPS*****
tailorGump 	= 0x38920abd
tinkerGump 	= 0x38920abd
BODGump 	= 0x5afbd742
BODBookGump = 0x54f555df

# *****Materials******
ingots = 0x1bf2
ironIngotHue = 0
cutCloth = 0x1766
leather = 0x1081
leatherHue 	= 0
spinedHue 	= 2220
hornedHue 	= 2117
barbedHue 	= 2129

# *****BOD*******
BOD = 0x2258
TailorBODcolor = 1155



# *************************
# ****** CRAFT ITEMS ******
# *************************
# For your server, your gump responses may be different than those listed here.
# You can easily determine what they should be by creating a test macro,
# record crafting each item, and replacing the values below.  The itemGraphics should
# not need to change (unless you are on a very custom shard)
# *************************
# FORMAT: CraftableItem(itemGraphic, GumpResponse1, GumpResponse2)
# *************************
# *****Tools******
SewingKit 	= CraftableItem(0xf9d,  15, 44)
Scissors 	= CraftableItem(0xf9f,  15, 2)
TinkerTool 	= CraftableItem(0x1eb8, 15, 23)
# *****Hats*****
Skullcap 		= CraftableItem(0x1544, 8, 2)
Bandana 		= CraftableItem(0x1540, 8, 9)
FloppyHat 		= CraftableItem(0x1713, 8, 16)
Cap 			= CraftableItem(0x1715, 8, 23)
WideBrimHat 	= CraftableItem(0x1714, 8, 30)
StrawHat 		= CraftableItem(0x1717, 8, 37)
TallStrawHat 	= CraftableItem(0x1716, 8, 44)
WizardHat 		= CraftableItem(0x1718, 8, 51)
Bonnet 			= CraftableItem(0x1719, 8, 58)
FeatheredHat	= CraftableItem(0x171a, 8, 65)
TricornHat 		= CraftableItem(0x171b, 8, 72)
JesterHat 		= CraftableItem(0x171c, 8, 79)
# *****Shirts and Pants*****
Doublet 	= CraftableItem(0x1f7b, 15, 2)
Shirt 		= CraftableItem(0x1517, 15, 9)
FancyShirt 	= CraftableItem(0x1efd, 15, 16)
Tunic 		= CraftableItem(0x1fa1, 15, 23)
Surcoat 	= CraftableItem(0x1ffd, 15, 30)
PlainDress 	= CraftableItem(0x1f01, 15, 37)
FancyDress 	= CraftableItem(0x1f00, 15, 44)
Cloak 		= CraftableItem(0x1515, 15, 51)
Robe		= CraftableItem(0x1f03, 15, 58)
JesterSuit 	= CraftableItem(0x1f9f, 15, 65)
ShortPants 	= CraftableItem(0x152e, 15, 128)
LongPants 	= CraftableItem(0x1539, 15, 135)
Kilt 		= CraftableItem(0x1537, 15, 142)
Skirt 		= CraftableItem(0x1516, 15, 149)
# *****Miscellaneous*****
BodySash 	= CraftableItem(0x1541, 22, 2)
HalfApron 	= CraftableItem(0x153b, 22, 9)
FullApron 	= CraftableItem(0x153d, 22, 16)
# *****Footwear*****
Sandals 	= CraftableItem(0x170d, 29, 30)
Shoes 		= CraftableItem(0x170f, 29, 37)
Boots 		= CraftableItem(0x170b, 29, 44)
ThighBoots 	= CraftableItem(0x1711, 29, 51)
# *****Leather Armor*****
LeatherGorget 	= CraftableItem(0x13c7, 36, 23)
LeatherCap 		= CraftableItem(0x1db9, 36, 30)
LeatherGloves 	= CraftableItem(0x13c6, 36, 37)
LeatherSleeves 	= CraftableItem(0x13cd, 36, 44)
LeatherLeggings = CraftableItem(0x13cb, 36, 51)
LeatherTunic 	= CraftableItem(0x13cc, 36, 58)
# *****Studded Armor*****
StuddedGorget 	= CraftableItem(0x13d6, 50, 2)
StuddedGloves 	= CraftableItem(0x13d5, 50, 9)
StuddedSleeves 	= CraftableItem(0x13dc, 50, 16)
StuddedLeggings = CraftableItem(0x13da, 50, 23)
StuddedTunic 	= CraftableItem(0x13db, 50, 30)
# *****Female Armor*****
LeatherShorts 		= CraftableItem(0x1c00, 57, 2)
LeatherSkirt 		= CraftableItem(0x1c08, 57, 9)
LeatherBustier 		= CraftableItem(0x1c0a, 57, 16)
StuddedBustier 		= CraftableItem(0x1c0c, 57, 23)
FemaleLeatherArmor 	= CraftableItem(0x1c06, 57, 30)
StuddedArmor 		= CraftableItem(0x1c02, 57, 37)
# *****Bone Armor*****
BoneHelmet 		= CraftableItem(0x1451, 64, 2)
BoneGloves 		= CraftableItem(0x1450, 64, 9)
BoneArms 		= CraftableItem(0x144e, 64, 16)
BoneLeggings 	= CraftableItem(0x1452, 64, 23)
BoneArmor 		= CraftableItem(0x144f, 64, 30)


ClothItems 	 = ["skullcap", "bandana", "hat", "cap", "bonnet", "doublet", "shirt", "tunic", "surcoat", 
			    "dress", "cloak", "robe", "jester", "pants", "kilt", "skirt", "apron", "sash"]
LeatherItems = ["shoes", "sandals", "boots", "leather", "studded"]
BoneItems 	 = ["Bone"]

def RefillIngots():
	container = GetAlias('tailor bod filler restock')
	if CountType(ingots, "backpack") < 2:
		if CountType(ingots, container) == 0:
			SysMessage("OUT OF INGOTS!", errorTextColor)
			CancelTarget()
			Stop()
		else:
			MoveType(ingots, container, "backpack", -1, -1, -1, ironIngotHue, 50)
			Pause(1500)

def RefillCloth():
	pass
	

def RefillLeather(leatherHue):
	pass
	

def UnloadMaterials():
	pass

def CheckMaterials():
	if not GumpExists(BODGump):
		return
	else:
		pass
		
def CraftTinkerItem(item):
	RestockIngots()
	UseType(TinkerTool.graphic)
	WaitForGump(tinkerGump, 5000)
	ReplyGump(tinkerGump, item.gumpResponse1)
	WaitForGump(tinkerGump, 5000)
	ReplyGump(tinkerGump, item.gumpResponse2)
	Pause(1500)	


def GetScissors():
	while not FindType(Scissors.graphic, 1, "backpack"):
		CraftTinkerItem(Scissors)
	FindType(Scissors.graphic, 1, "backpack")
	return GetAlias("found")


def CraftSewingKits():
	if CountType(TinkerTool.graphic, "backpack") < 2:
		while CountType(TinkerTool.graphic, "backpack") < 2:
			CraftTinkerItem(TinkerTool)
	while CountType(SewingKit.graphic, "backpack") < 5:
		CraftTinkerItem(SewingKit)


def CheckForSewingKits():
	if not FindType(SewingKit.graphic, 1, "backpack"):
		container = GetAlias('tailor bod filler restock')
		if not FindType(SewingKit.graphic, 2, container):
			CraftSewingKits()
		else:
			MoveType(SewingKit.graphic, container, "backpack")
			Pause(1500)

	if FindType(SewingKit.graphic, 1, "backpack"):		
		return GetAlias("found")
	else:
		SysMessage("ERROR GETTING SEWING KIT", errorTextColor)
		Stop()


def CraftTailorItem(item):
	ReplyGump(tailorGump, item.gumpResponse1)
	WaitForGump(tailorGump, 5000)
	ReplyGump(tailorGump, item.gumpResponse2)
	WaitForGump(tailorGump, 5000)
	Pause(500)
	while FindType(item.graphic, 1, "backpack"):
		item = GetAlias("found")
		Target(item)
		WaitForTarget(2000)
		if not TargetExists() and InJournal("must be exceptional"):
			myScissors = GetScissors()
			UseObject(myScissors)
			WaitForTarget(5000)
			Target(item)
			# Bring back the target cursor
			ReplyGump(BODGump, 2)
			WaitForGump(BODGump, 5000)
			WaitForTarget(5000)
			ClearJournal()


def BookDeedsRemaining():
	bodBook = GetAlias("smith bod source")
	remaining = PropertyValue[int](bodBook, "Deeds in Book:")
	return remaining

def ProcessBOD():
	CheckMaterials()
	kit = CheckForSewingKits()
	UseObject(kit)
	WaitForGump(tailorGump, 5000)
	# ********** Hats **********
	if InGump(BODGump, "skullcap"):
		CraftTailorItem(Skullcap)
	elif InGump(BODGump, "bandana"):
		CraftTailorItem(Bandana)
	elif InGump(BODGump, "floppy hat"):
		CraftTailorItem(FloppyHat)
	elif InGump(BODGump, "cap"):
		CraftTailorItem(Cap)
	elif InGump(BODGump, "wide-brim hat"):
		CraftTailorItem(WideBrimHat)
	elif InGump(BODGump, "tall straw hat"):
		CraftTailorItem(TallStrawHat)
	elif InGump(BODGump, "straw hat"):
		CraftTailorItem(StrawHat)
	elif InGump(BODGump, "wizard's hat"):
		CraftTailorItem(WizardHat)
	elif InGump(BODGump, "bonnet"):
		CraftTailorItem(Bonnet)
	elif InGump(BODGump, "feathered hat"):
		CraftTailorItem(FeatheredHat)
	elif InGump(BODGump, "tricorne hat"):
		CraftTailorItem(TricornHat)
	elif InGump(BODGump, "jester hat"):
		CraftTailorItem(JesterHat)
	# ********** Shirts and Pants **********
	elif InGump(BODGump, "doublet"):
		CraftTailorItem(Doublet)
	elif InGump(BODGump, "fancy shirt"):
		CraftTailorItem(FancyShirt)
	elif InGump(BODGump, "shirt"):
		CraftTailorItem(Shirt)
	elif InGump(BODGump, "tunic"):
		CraftTailorItem(Tunic)		
	elif InGump(BODGump, "surcoat"):
		CraftTailorItem(Surcoat)
	elif InGump(BODGump, "plain dress"):
		CraftTailorItem(PlainDress)
	elif InGump(BODGump, "fancy dress"):
		CraftTailorItem(FancyDress)
	elif InGump(BODGump, "cloak"):
		CraftTailorItem(Cloak)
	elif InGump(BODGump, "robe"):
		CraftTailorItem(Robe)
	elif InGump(BODGump, "jester suit"):
		CraftTailorItem(JesterSuit)
	elif InGump(BODGump, "short pants"):
		CraftTailorItem(ShortPants)		
	elif InGump(BODGump, "long pants"):
		CraftTailorItem(LongPants)
	elif InGump(BODGump, "kilt"):
		CraftTailorItem(Kilt)
	elif InGump(BODGump, "skirt"):
		CraftTailorItem(Skirt)
	# ********** MISCELLANEOUS **********
	elif InGump(BODGump, "body sash"):
		CraftTailorItem(BodySash)
	elif InGump(BODGump, "half apron"):
		CraftTailorItem(HalfApron)
	elif InGump(BODGump, "full apron"):
		CraftTailorItem(FullApron)
	# ********** FOOTWEAR **********
	elif InGump(BODGump, "thigh boots"):
		CraftTailorItem(ThighBoots)
	elif InGump(BODGump, "sandals"):
		CraftTailorItem(Sandals)
	elif InGump(BODGump, "shoes"):
		CraftTailorItem(Shoes)
	elif InGump(BODGump, "boots"):
		CraftTailorItem(Boots)
	# ********** LEATHER ARMOR **********
	elif InGump(BODGump, "leather gorget"):
		CraftTailorItem(LeatherGorget)
	elif InGump(BODGump, "leather cap"):
		CraftTailorItem(LeatherCap)	
	elif InGump(BODGump, "leather gloves"):
		CraftTailorItem(LeatherGloves)
	elif InGump(BODGump, "leather leggings"):
		CraftTailorItem(LeatherLeggings)
	elif InGump(BODGump, "leather sleeves"):
		CraftTailorItem(LeatherSleeves)
	elif InGump(BODGump, "leather tunic"):
		CraftTailorItem(LeatherTunic)
	# ********** STUDDED ARMOR **********
	elif InGump(BODGump, "studded gorget"):
		CraftTailorItem(StuddedGorget)	
	elif InGump(BODGump, "studded gloves"):
		CraftTailorItem(StuddedGloves)
	elif InGump(BODGump, "studded leggings"):
		CraftTailorItem(StuddedLeggings)
	elif InGump(BODGump, "studded sleeves"):
		CraftTailorItem(StuddedSleeves)
	elif InGump(BODGump, "studded tunic"):
		CraftTailorItem(StuddedTunic)
	# ********** FEMALE ARMOR **********
	elif InGump(BODGump, "leather shorts"):
		CraftTailorItem(LeatherShorts)
	elif InGump(BODGump, "leather skirt"):
		CraftTailorItem(LeatherSkirt)
	elif InGump(BODGump, "leather bustier"):
		CraftTailorItem(LeatherBustier)
	elif InGump(BODGump, "studded bustier"):
		CraftTailorItem(StuddedBustier)
	elif InGump(BODGump, "female leather armor"):
		CraftTailorItem(FemaleLeatherArmor)
	elif InGump(BODGump, "studded armorr"):
		CraftTailorItem(StuddedArmor)
	# ********** BONE ARMOR **********
	elif InGump(BODGump, "bone helmet"):
		CraftTailorItem(BoneHelmet)	
	elif InGump(BODGump, "bone gloves"):
		CraftTailorItem(BoneGloves)
	elif InGump(BODGump, "bone leggings"):
		CraftTailorItem(BoneLeggings)
	elif InGump(BODGump, "bone arms"):
		CraftTailorItem(BoneArms)
	elif InGump(BODGump, "bone armor"):
		CraftTailorItem(BoneArmor)


# ******************************
# *****      MAIN          *****
# ******************************

# Search for BOD to Fill
if FindType(BOD, 1, "backpack", TailorBODcolor):
	currentBOD = GetAlias("found")
	UseObject(currentBOD)
	WaitForGump(BODGump, 5000)
	# Select the combine option
	ReplyGump(BODGump, 2)
	WaitForGump(BODGump, 5000)
	WaitForTarget(5000)

	while TargetExists():
		ProcessBOD()

	# BOD is complete, move to destination book
	if not TargetExists():
		destination = GetAlias('tailor bod destination')
		MoveItem(currentBOD, destination)
		Pause(1500)

# Get A BOD out of the book
elif not BookDeedsRemaining() == 0:
	bodBook = GetAlias("tailor bod source")
	UseObject(bodBook)
	WaitForGump(BODBookGump, 5000)
	ReplyGump(BODBookGump, 5)
	Pause(1500)

# All BODs filled / BOD book is empty
else:
	SysMessage("UNABLE TO FIND BODS TO FILL", errorTextColor)
	CancelTarget()
	Stop()
