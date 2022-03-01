# Name: Tailor BOD Filler
# Description: This will fill all Tailor BODs from a Source BOD Book. Set your filter on this book to pull only the BODs you want filled.
# Author: raveX
# Era: Any

SetQuietMode(True)

# ****************************************
# To turn off/on the ingame help prompts *
# ****************************************
UseHelp = True
# ****************************************
# ****************************************


msg = "Welcome to the Tailor BOD Filler macro.  This macro " \
	  "will take BODs from a BOD book and fill them.  It " \
	  "supports making any Tailor BOD, cloth, leather, bone, and " \
	  "of any leather type.  Let's get started!"
if UseHelp: ConfirmPrompt(msg)

msg = "First we will want to know what BOD book you want to pull BODs " \
      "out of to fill.  Be sure to set the filter on the book to the " \
      "specific type of BODs you want to fill here. At a minimum, you will " \
      "want to ensure you have selected Tailoring and Small BODs."
      
if not FindAlias('tailor bod source'):
	if UseHelp: ConfirmPrompt(msg)
  	PromptAlias('tailor bod source')

msg = "Second, you will need to select a different book to hold the completed " \
      "BODs you fill.  Make sure the book has plenty of room to hold all the " \
      "BODs. I'm not handling you screwing that up in the macro." 
      
if not FindAlias('tailor bod destination'):
	if UseHelp: ConfirmPrompt(msg)
  	PromptAlias('tailor bod destination')

msg = "Next, you need to select a container that will serve as your restock " \
      "target.  In this container, you will want plenty of materials, such as cut cloth, " \
      "leathers, and bone.  This all obviously depends on what BODs you are planning to fill " \
      "Additionally, if you are going to tinker sewing kits, have plenty of ingots in this " \
      "container as well. If you are not going to use tinkering, be sure to have scissors in " \
      "your pack (for non-exceptional items when exceptional is required) and lots of sewing kits in " \
      "there as well.  Material searches are set to a second level search."
      
if not FindAlias('tailor bod filler restock'):
	if UseHelp: ConfirmPrompt(msg)
  	PromptAlias('tailor bod filler restock')

msg = "Finally, this last choice is a book for BODs that cannot be filled. " \
	  "For instance, you may have run out of leather and " \
	  "still have plenty of cloth in your restock chest. " \
	  "The Macro could continue to complete the remaining cloth BODs, " \
	  "but would stash all the incompletable leather BODs in this book."
	  
if not FindAlias('tailor uncompletable bod book'):
	if UseHelp: ConfirmPrompt(msg)
  	PromptAlias('tailor uncompletable bod book')

msg = "You are all set! \nOne final note, if you prefer to not see these prompts " \
	  "anymore, set the 'UseHelp' variable at the top of the macro to 'False'" \

if UseHelp: ConfirmPrompt(msg)

class CraftableItem:
	def __init__(self, graphic, gumpResponse1, gumpResponse2):
		self.graphic = graphic
		self.gumpResponse1 = gumpResponse1
		self.gumpResponse2 = gumpResponse2
		
class Material:
	def __init__(self, graphic, name, hue, minPackAmt, restockAmt):
		self.graphic = graphic
		self.name = name
		self.hue = hue
		self.minPackAmt = minPackAmt
		self.restockAmt = restockAmt


# *****MISC******
errorTextColor = 33
craftBoneArmor = True
craftStuddedArmor = True
stopOnOutOfResource = True

# *****GUMPS*****
tailorGump 	= 0x38920abd
tinkerGump 	= 0x38920abd
BODGump 	= 0x5afbd742
BODBookGump = 0x54f555df

# *****BOD*******
BOD = 0x2258
TailorBODhue = 1155
currentBOD = 0

# *************************
# ******  MATERIALS  ******
# *************************
# FORMAT: Material(graphic, name, hue, minPackAmt, restockAmt)
# *************************
ingots 	= Material(0x1bf2, "INGOTS", 0, 2, 50)
cloth 	= Material(0x1766, "CLOTH", -1, 20, 500)
leather = Material(0x1081, "LEATHER", 0, 20, 500)
spined 	= Material(0x1081, "SPINED LEATHER", 2220, 20, 500)
horned 	= Material(0x1081, "HORNED LEATHER", 2117, 20, 500)
barbed 	= Material(0x1081, "BARBED LEATHER", 2129, 20, 500)
bone 	= Material(0xf7e,  "BONE", 0, 10, 200)

LeatherItems = ["shoes", "sandals", "boots", "leather", "studded", "bone"]
LeatherTypes = ["spined", "horned", "barbed"]

currentItemMaterials = []

# *****TRACK MATERIALS******
outOfCloth   = False
outOfLeather = False
outOfSpined  = False
outOfHorned  = False
outOfBarbed  = False
outOfBone    = False


# *************************
# ****** CRAFT ITEMS ******
# *************************
# For your server, your gump responses may be different than those listed here.
# You can easily determine what they should be by creating a test macro,
# record crafting each item, and replacing the values below.  The itemGraphics should
# not need to change (unless you are on a very custom shard)
# *************************
# FORMAT: CraftableItem(graphic, gumpResponse1, gumpResponse2)
# *************************
# *****Tools******
SewingKit 		= CraftableItem(0xf9d,  15, 44)
Scissors 		= CraftableItem(0xf9f,  15, 2)
TinkerTool 		= CraftableItem(0x1eb8, 15, 23)
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
Doublet 		= CraftableItem(0x1f7b, 15, 2)
Shirt 			= CraftableItem(0x1517, 15, 9)
FancyShirt 		= CraftableItem(0x1efd, 15, 16)
Tunic 			= CraftableItem(0x1fa1, 15, 23)
Surcoat 		= CraftableItem(0x1ffd, 15, 30)
PlainDress 		= CraftableItem(0x1f01, 15, 37)
FancyDress 		= CraftableItem(0x1f00, 15, 44)
Cloak 			= CraftableItem(0x1515, 15, 51)
Robe			= CraftableItem(0x1f03, 15, 58)
JesterSuit 		= CraftableItem(0x1f9f, 15, 65)
ShortPants 		= CraftableItem(0x152e, 15, 128)
LongPants 		= CraftableItem(0x1539, 15, 135)
Kilt 			= CraftableItem(0x1537, 15, 142)
Skirt 			= CraftableItem(0x1516, 15, 149)
# *****Miscellaneous*****
BodySash 		= CraftableItem(0x1541, 22, 2)
HalfApron 		= CraftableItem(0x153b, 22, 9)
FullApron 		= CraftableItem(0x153d, 22, 16)
# *****Footwear*****
Sandals 		= CraftableItem(0x170d, 29, 30)
Shoes 			= CraftableItem(0x170f, 29, 37)
Boots 			= CraftableItem(0x170b, 29, 44)
ThighBoots 		= CraftableItem(0x1711, 29, 51)
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


# *************************
# ******  FUNCTIONS  ******
# *************************

def RefillMaterial(type):
	container = GetAlias('tailor bod filler restock')
	if CountType(type.graphic, "backpack") < type.minPackAmt:
		if CountType(type.graphic, container) == 0:
			msg = "OUT OF " + name + "!"
			SysMessage(msg, errorTextColor)
			if stopOnOutOfResource:
				CancelTarget()
				Stop()
			else:
				if type == cloth: outOfCloth = True
				elif type == leather: outOfLeather = True
				elif type == spined: outOfSpined = True
				elif type == horned: outOfHorned = True
				elif type == barbed: outOfBarbed = True
				elif type == bone: outOfBone = True
		else:
			MoveType(type.graphic, container, "backpack", -1, -1, -1, hue, type.restockAmt)
			Pause(1500)


def UnloadMaterials():
	materials = [ingots, cloth, leather, spined, horned, barbed, bone]
	container = GetAlias('tailor bod filler restock')
	for x in materials:
		MoveType(x.graphic, "backpack", container, -1, -1, -1)


def CheckMaterials():
	materialType = "cloth"
	requiresBone = False
	if not GumpExists(BODGump):
		return
	else:
		for text in LeatherItems:
			if InGump(BODGump, text):
				materialType = "leather"
				if text == "bone":
					requiresBone = True
				for type in LeatherTypes:
					if InGump(BODGump, type):
						materialType = type

	if materialType == "cloth": RefillMaterial(cloth)
	elif materialType == "leather": RefillMaterial(leather)
	elif materialType == "spined": RefillMaterial(spined)
	elif materialType == "horned": RefillMaterial(horned)
	elif materialType == "barbed": RefillMaterial(barbed)
		
	if requiresBone: RefillMaterial(bone)
							
		
		
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


def CraftKits():
	if CountType(TinkerTool.graphic, "backpack") < 2:
		while CountType(TinkerTool.graphic, "backpack") < 2:
			CraftTinkerItem(TinkerTool)
	while CountType(SewingKit.graphic, "backpack") < 5:
		CraftTinkerItem(SewingKit)


def CheckForSewingKits():
	if not FindType(SewingKit.graphic, 1, "backpack"):
		container = GetAlias('tailor bod filler restock')
		if not FindType(SewingKit.graphic, 2, container):
			CraftKits()
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
if FindType(BOD, 1, "backpack", TailorBODhue):
	currentBOD = GetAlias("found")
	UseObject(currentBOD)
	WaitForGump(BODGump, 5000)
	
	# Select the "combine" option
	ReplyGump(BODGump, 2)
	WaitForGump(BODGump, 5000)
	WaitForTarget(5000)

	CheckMaterials()
	
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
