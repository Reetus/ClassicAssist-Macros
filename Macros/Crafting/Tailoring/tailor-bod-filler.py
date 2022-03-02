# Name: Tailor BOD Filler
# Description: This will fill all Tailor BODs from a Source BOD Book. Set your filter on this book to pull only the BODs you want filled.
# Author: raveX
# Era: Any

SetQuietMode(True)

# ****************************************
# To turn off/on the ingame help prompts *
# ****************************************
UseHelp = True
debug = True
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
      
if not FindAlias('tailor restock container'):
	if UseHelp: ConfirmPrompt(msg)
  	PromptAlias('tailor restock container')

msg = "Finally, this last choice is a book for BODs that cannot be filled. " \
	  "For instance, you may have run out of leather and " \
	  "still have plenty of cloth in your restock chest. " \
	  "The Macro could continue to complete the remaining cloth BODs, " \
	  "but would stash all the incompletable leather BODs in this book."
	  
if not FindAlias('tailor uncompletable bod book'):
	if UseHelp: ConfirmPrompt(msg)
  	PromptAlias('tailor uncompletable bod book')

msg = "Trash container for failed Bone armor attempts as they cannot be recycled"

if not FindAlias('TrashForBone'):
	if UseHelp: ConfirmPrompt(msg)
  	PromptAlias('TrashForBone')

msg = "You are all set! \nOne final note, if you prefer to not see these prompts " \
	  "anymore, set the 'UseHelp' variable at the top of the macro to 'False'" \

if UseHelp: ConfirmPrompt(msg)

class CraftableItem:
	def __init__(self, graphic, gumpResponse1, gumpResponse2):
		self.graphic = graphic
		self.gumpResponse1 = gumpResponse1
		self.gumpResponse2 = gumpResponse2
		self.defaultHue = 0
		
class Material:
	def __init__(self, graphic, name, hue, minPackAmt, restockAmt):
		self.graphic = graphic
		self.name = name
		self.hue = hue
		self.minPackAmt = minPackAmt
		self.restockAmt = restockAmt


# *****MISC******
textColor = 43
errorTextColor = 33
debugTextColor = 16
craftBoneArmor = True
craftStuddedArmor = True
stopOnOutOfResource = True

# *****GUMPS*****
tailorGump 	= 0x38920abd
tinkerGump 	= 0x38920abd
BODGump 	= 0x5afbd742
BODBookGump = 0x54f555df
BODGumpCombineResponse = 2
tailorMaterialResponse = 7
tailorLeatherResponse = 6
tailorSpinedResposne = 13
tailorHornedResponse = 20
tailorBarbedResponse = 27

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

def GetRestockContainer():
	if debug: SysMessage("[debug]:In GetRestockContainer", debugTextColor)
	container = GetAlias('tailor restock container')
	if container == 0:
		SysMessage("Looking for 'tailor restock container' alias and not found", errorTextColor)
		CancelTarget()
		Stop()
	elif not InRange(container, 2):
		SysMessage("Restock container is no longer in range", errorTextColor)
		CancelTarget()
		Stop()
	else: return container

def UnloadMaterials(skipIngots):
	if debug: print("In UnloadMaterials", debugTextColor)
	materials = [ingots, cloth, leather, spined, horned, barbed, bone]
	container = GetRestockContainer()
	for x in materials:
		if not (skipIngots and x == ingots):
			MoveType(x.graphic, "backpack", container, -1, -1, -1)

def RefillMaterial(type):
	if debug: SysMessage("[debug]:In RefillMaterial", debugTextColor)
	container = GetRestockContainer()
	if CountType(type.graphic, "backpack") < type.minPackAmt:
		if CountType(type.graphic, container) == 0:
			msg = "OUT OF " + type.name + "!"
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
			Pause(500)
			MoveType(type.graphic, container, "backpack", -1, -1, -1, type.hue, type.restockAmt)
			Pause(1500)


def SetLeatherType():
	if debug: SysMessage("[debug]:In SetLeatherType", debugTextColor)
	materialType = "cloth"
	if currentBOD == 0:
		SysMessage("Trying to set leather type but no current BOD", errorTextColor)
		return
		
	UseObject(currentBOD)
	WaitForGump(BODGump, 5000)
	for text in LeatherItems:
		if InGump(BODGump, text):
			materialType = "leather"			
			for type in LeatherTypes:
				if InGump(BODGump, type):
					materialType = type
					
	if materialType == "cloth": return
	
	kit = GetSewingKit()
	UseObject(kit)
	WaitForGump(tailorGump, 5000)
	ReplyGump(tailorGump, tailorMaterialResponse)
	WaitForGump(tailorGump, 5000)
	if materialType == "leather": ReplyGump(tailorGump, tailorLeatherResponse)
	elif materialType == "spined": ReplyGump(tailorGump, tailorSpinedResposne)
	elif materialType == "horned": ReplyGump(tailorGump, tailorHornedResponse)
	elif materialType == "barbed": ReplyGump(tailorGump, tailorBarbedResponse)

	

def CheckMaterials():
	if debug: SysMessage("[debug]:In CheckMaterials", debugTextColor)
	materialType = "cloth"
	requiresBone = False
	if currentBOD == 0:
		SysMessage("Looking for required BOD material but no current BOD", errorTextColor)
		return
	else:
		UseObject(currentBOD)
		WaitForGump(BODGump, 5000)
		for text in LeatherItems:
			if InGump(BODGump, text):
				materialType = "leather"
				if text == "bone":
					requiresBone = True
				for type in LeatherTypes:
					if InGump(BODGump, type):
						materialType = type

	print("Material type is: " + materialType)
	if materialType == "cloth": RefillMaterial(cloth)
	elif materialType == "leather": RefillMaterial(leather)
	elif materialType == "spined": RefillMaterial(spined)
	elif materialType == "horned": RefillMaterial(horned)
	elif materialType == "barbed": RefillMaterial(barbed)
		
	if requiresBone: RefillMaterial(bone)
	
							
		
		
def CraftTinkerItem(item):
	if debug: SysMessage("[debug]:In CraftTinkerItem", debugTextColor)
	# Careful of endless loop if we are crafting a tinker tool
	toolCheck = True
	if item.graphic == TinkerTool.graphic:
		toolCheck = False
		
	if toolCheck:	
		if CountType(TinkerTool.graphic, "backpack", TinkerTool.defaultHue) < 2:
			CraftTinkerItem(TinkerTool)
			
	RefillMaterial(ingots)
	UseType(TinkerTool.graphic)
	WaitForGump(tinkerGump, 5000)
	ReplyGump(tinkerGump, item.gumpResponse1)
	WaitForGump(tinkerGump, 5000)
	ReplyGump(tinkerGump, item.gumpResponse2)
	Pause(1500)		


def GetScissors():
	if debug: SysMessage("[debug]:In GetScissors", debugTextColor)
	while not FindType(Scissors.graphic, 1, "backpack"):
		CraftTinkerItem(Scissors)
	FindType(Scissors.graphic, 1, "backpack")
	return GetAlias("found")


def GetSewingKit():
	if debug: SysMessage("[debug]:In GetSewingKit", debugTextColor)
	while not FindType(SewingKit.graphic, 1, "backpack", SewingKit.defaultHue):
		container = GetRestockContainer()
		if not FindType(SewingKit.graphic, 2, container, SewingKit.defaultHue):
			CraftTinkerItem(SewingKit)
		else:
			MoveType(SewingKit.graphic, container, "backpack", -1, -1, -1, SewingKit.defaultHue)
			Pause(1500)
	if FindType(SewingKit.graphic, 1, "backpack", SewingKit.defaultHue):		
		return GetAlias("found")
	else:
		SysMessage("ERROR GETTING SEWING KIT", errorTextColor)
		Stop()


def CraftTailorItem(item):
	if debug: SysMessage("[debug]:In CraftTailorItem", debugTextColor)
	kit = GetSewingKit()
	UseObject(kit)
	WaitForGump(tailorGump, 5000)
	ReplyGump(tailorGump, item.gumpResponse1)
	WaitForGump(tailorGump, 5000)
	ReplyGump(tailorGump, item.gumpResponse2)
	WaitForGump(tailorGump, 5000)
	Pause(500)
	while FindType(item.graphic, 1, "backpack"):
		craftedItem = GetAlias("found")
		Target(craftedItem)
		WaitForTarget(2000)
		if not TargetExists() and InJournal("must be exceptional"):
			myScissors = GetScissors()
			Pause(500)
			UseObject(myScissors)
			WaitForTarget(5000)
			Target(craftedItem)
			Pause(300)
			if InJournal("Scissors cannot be used"):
				Pause(500)
				MoveItem(craftedItem, GetAlias("TrashForBone"))
				ClearJournal()
			# Bring back the target cursor
			Pause(500)
			ReplyGump(BODGump, BODGumpCombineResponse)
			WaitForGump(BODGump, 5000)
			WaitForTarget(5000)
			ClearJournal()


def BookDeedsRemaining():
	if debug:SysMessage("[debug]:In BookDeedsRemaining", debugTextColor)
	bodBook = GetAlias("smith bod source")
	
	if not bodBook == 0:
		remaining = PropertyValue[int](bodBook, "Deeds in Book:")
		return remaining
	else:
		SysMessage("Did not find the 'smith bod source' alias", errorTextColor)
		return 0


def GetBODItem():
	if debug: SysMessage("[debug]:In GetBODItem", debugTextColor)
	if not GumpExists(BODGump) and currentBOD == 0:
		SysMessage("Looking for BOD Gump and not found", errorTextColor)
		return None
	else:
		UseObject(currentBOD)
		WaitForGump(BODGump, 5000)
	
	# ********** Hats **********
	if InGump(BODGump, "skullcap"): return Skullcap
	elif InGump(BODGump, "bandana"): return Bandana
	elif InGump(BODGump, "floppy hat"): return FloppyHat
	elif InGump(BODGump, "cap"): return Cap
	elif InGump(BODGump, "wide-brim hat"): return WideBrimHat
	elif InGump(BODGump, "tall straw hat"): return TallStrawHat
	elif InGump(BODGump, "straw hat"): return StrawHat
	elif InGump(BODGump, "wizard's hat"): return WizardHat
	elif InGump(BODGump, "bonnet"): return Bonnet
	elif InGump(BODGump, "feathered hat"): return FeatheredHat
	elif InGump(BODGump, "tricorne hat"): return TricornHat
	elif InGump(BODGump, "jester hat"): return JesterHat
	# ********** Shirts and Pants **********
	elif InGump(BODGump, "doublet"): return Doublet
	elif InGump(BODGump, "fancy shirt"): return FancyShirt
	elif InGump(BODGump, "shirt"): return Shirt		
	elif InGump(BODGump, "surcoat"): return Surcoat
	elif InGump(BODGump, "plain dress"): return PlainDress
	elif InGump(BODGump, "fancy dress"): return FancyDress
	elif InGump(BODGump, "cloak"): return Cloak
	elif InGump(BODGump, "robe"): return Robe
	elif InGump(BODGump, "jester suit"): return JesterSuit
	elif InGump(BODGump, "short pants"): return ShortPants
	elif InGump(BODGump, "long pants"): return LongPants
	elif InGump(BODGump, "kilt"): return Kilt	
	# ********** MISCELLANEOUS **********
	elif InGump(BODGump, "body sash"): return BodySash
	elif InGump(BODGump, "half apron"): return HalfApron
	elif InGump(BODGump, "full apron"): return FullApron
	# ********** FOOTWEAR **********
	elif InGump(BODGump, "thigh boots"): return ThighBoots
	elif InGump(BODGump, "sandals"): return Sandals
	elif InGump(BODGump, "shoes"): return Shoes
	elif InGump(BODGump, "boots"): return Boots
	# ********** LEATHER ARMOR **********
	elif InGump(BODGump, "leather gorget"): return LeatherGorget
	elif InGump(BODGump, "leather cap"): return LeatherCap
	elif InGump(BODGump, "leather gloves"): return LeatherGloves
	elif InGump(BODGump, "leather leggings"): return LeatherLeggings
	elif InGump(BODGump, "leather sleeves"): return LeatherSleeves
	elif InGump(BODGump, "leather tunic"): return LeatherTunic
	# ********** STUDDED ARMOR **********
	elif InGump(BODGump, "studded gorget"): return StuddedGorget
	elif InGump(BODGump, "studded gloves"): return StuddedGloves
	elif InGump(BODGump, "studded leggings"): return StuddedLeggings
	elif InGump(BODGump, "studded sleeves"): return StuddedSleeves
	elif InGump(BODGump, "studded tunic"): return StuddedTunic
	# ********** FEMALE ARMOR **********
	elif InGump(BODGump, "leather shorts"): return LeatherShorts
	elif InGump(BODGump, "leather skirt"): return LeatherSkirt
	elif InGump(BODGump, "leather bustier"): return LeatherBustier
	elif InGump(BODGump, "studded bustier"): return StuddedBustier
	elif InGump(BODGump, "female leather armor"): return FemaleLeatherArmor
	elif InGump(BODGump, "studded armor"): return StuddedArmor
	# ********** BONE ARMOR **********
	elif InGump(BODGump, "bone helmet"): return BoneHelmet
	elif InGump(BODGump, "bone gloves"): return BoneGloves
	elif InGump(BODGump, "bone leggings"): return BoneLeggings
	elif InGump(BODGump, "bone arms"): return BoneArms
	elif InGump(BODGump, "bone armor"): return BoneArmor
	# ********** NEED THESE AT END ***********
	elif InGump(BODGump, "skirt"): return Skirt
	elif InGump(BODGump, "tunic"): return Tunic
	else:
		SysMessage("Did not find a supported item in the BOD Gump", errorTextColor)
		return None



# ******************************
# *****      MAIN          *****
# ******************************
def Main():
	while BookDeedsRemaining() > 0:
		# Search for BOD to Fill
		if FindType(BOD, 1, "backpack", TailorBODhue):
			global currentBOD
			currentBOD = GetAlias("found")
			UseObject(currentBOD)
			WaitForGump(BODGump, 5000)
			Pause(500)
			
			# Select the "combine" option
			ReplyGump(BODGump, BODGumpCombineResponse)
			WaitForGump(BODGump, 5000)
			WaitForTarget(5000)
			Pause(600)
			
			SetLeatherType()
			Pause(600)
			
			item = GetBODItem()
			
			while TargetExists() and item != None:
				CheckMaterials()
				CraftTailorItem(item)
		
			# BOD is complete, move to destination book
			if not TargetExists():
				
				destination = GetAlias('tailor bod destination')
				MoveItem(currentBOD, destination)
				currentBOD = 0
				Pause(500)
				UnloadMaterials(True)
				Pause(500)
		
		# Get A BOD out of the book
		else:
			bodBook = GetAlias("tailor bod source")
			UseObject(bodBook)
			WaitForGump(BODBookGump, 5000)
			ReplyGump(BODBookGump, 5)
			Pause(1500)
		
	UnloadMaterials(False)
	SysMessage("NO BODS TO FILL", textColor)
	CancelTarget()
	Stop()
	
	
# ******************************
# *****      BODY          *****
# ******************************
Main()
