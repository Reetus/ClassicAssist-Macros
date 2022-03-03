from Assistant import Engine

SetQuietMode(True)

# ****************************************
# To turn off/on the ingame help prompts *
# ****************************************
UseHelp = False
DEBUG = False
# ****************************************
# ****************************************
#                  GLOBALS                
# ****************************************
currentBOD 	 = None
craftBoneArmor 	  = True
craftStuddedArmor = True


textColor = 43
errorTextColor = 33
debugTextColor = 16


msg = "Welcome to the Tailor BOD Filler macro.  This macro " \
	  "will take BODs from a BOD book and fill them.  It " \
	  "supports making any Tailor BOD, cloth, leather, bone, and " \
	  "of any leather type.  Let's get started!"
if UseHelp: ConfirmPrompt(msg)

msg = "First we will want to know what BOD book you want to pull BODs " \
      "out of to fill.\n\nBe sure to set the filter on the book to the " \
      "specific type of BODs you want to fill here. AT A MINIMUM, you will " \
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

# *************************
# ******  MATERIALS  ******
# *************************		
class Material:
	outOfCloth   = True
	outOfLeather = False
	outOfSpined  = False
	outOfHorned  = True
	outOfBarbed  = True
	outOfBone    = False
	
	def __init__(self, graphic, name, hue, minPackAmt, restockAmt):
		self.graphic = graphic
		self.name = name
		self.hue = hue
		self.minPackAmt = minPackAmt
		self.restockAmt = restockAmt
		
	def __str__(self):
		return self.name

# *************************
# FYI - Cloth will be Cut Cloth only, but of any color unless you change the hue setting below
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



# *************************
# ****** CRAFT ITEMS ******
# *************************
class CraftableItem:
	def __init__(self, graphic, gumpResponse1, gumpResponse2, name):
		self.graphic = graphic
		self.gumpResponse1 = gumpResponse1
		self.gumpResponse2 = gumpResponse2
		self.name = name
		self.defaultHue = 0
		
	def __str__(self):
		return self.name
		
# *************************
# For your server, YOUR GUMP RESPONSES MAY BE DIFFERENT than those listed here.
# You can easily determine what they should be by creating a test macro,
# record crafting each item, and replacing the values below.  The itemGraphics should
# not need to change (unless you are on a very custom shard)
# *************************
# FORMAT: CraftableItem(graphic, gumpResponse1, gumpResponse2, name)
# *************************
# *****Tools******
Scissors 		= CraftableItem(0xf9f,  15, 2, "scissors")
TinkerTool 		= CraftableItem(0x1eb8, 15, 23, "tinker tool")
SewingKit 		= CraftableItem(0xf9d,  15, 44, "sewing kit")
# *****Hats*****
Skullcap 		= CraftableItem(0x1544, 8, 2, "skullcap")
Bandana 		= CraftableItem(0x1540, 8, 9, "bandana")
FloppyHat 		= CraftableItem(0x1713, 8, 16, "floppy hat")
Cap 			= CraftableItem(0x1715, 8, 23, "cap")
WideBrimHat 	= CraftableItem(0x1714, 8, 30, "wide-brim hat")
StrawHat 		= CraftableItem(0x1717, 8, 37, "straw hat")
TallStrawHat 	= CraftableItem(0x1716, 8, 44, "tall straw hat")
WizardHat 		= CraftableItem(0x1718, 8, 51, "wizard's hat")
Bonnet 			= CraftableItem(0x1719, 8, 58, "bonnet")
FeatheredHat	= CraftableItem(0x171a, 8, 65, "feathered hat")
TricornHat 		= CraftableItem(0x171b, 8, 72, "tricorne hat")
JesterHat 		= CraftableItem(0x171c, 8, 79, "jester hat")
# *****Shirts and Pants*****
Doublet 		= CraftableItem(0x1f7b, 15, 2, "doublet")
Shirt 			= CraftableItem(0x1517, 15, 9, "shirt")
FancyShirt 		= CraftableItem(0x1efd, 15, 16, "fancy shirt")
Tunic 			= CraftableItem(0x1fa1, 15, 23, "tunic")
Surcoat 		= CraftableItem(0x1ffd, 15, 30, "surcoat")
PlainDress 		= CraftableItem(0x1f01, 15, 37, "plain dress")
FancyDress 		= CraftableItem(0x1f00, 15, 44, "fancy dress")
Cloak 			= CraftableItem(0x1515, 15, 51, "cloak")
Robe			= CraftableItem(0x1f03, 15, 58, "robe")
JesterSuit 		= CraftableItem(0x1f9f, 15, 65, "jester suit")
ShortPants 		= CraftableItem(0x152e, 15, 128, "short pants")
LongPants 		= CraftableItem(0x1539, 15, 135, "long pants")
Kilt 			= CraftableItem(0x1537, 15, 142, "kilt")
Skirt 			= CraftableItem(0x1516, 15, 149, "skirt")
# *****Miscellaneous*****
BodySash 		= CraftableItem(0x1541, 22, 2, "body sash")
HalfApron 		= CraftableItem(0x153b, 22, 9, "half apron")
FullApron 		= CraftableItem(0x153d, 22, 16, "full apron")
# *****Footwear*****
Sandals 		= CraftableItem(0x170d, 29, 30, "sandals")
Shoes 			= CraftableItem(0x170f, 29, 37, "shoes")
Boots 			= CraftableItem(0x170b, 29, 44, "boots")
ThighBoots 		= CraftableItem(0x1711, 29, 51, "thigh boots")
# *****Leather Armor*****
LeatherGorget 	= CraftableItem(0x13c7, 36, 23, "leather gorget")
LeatherCap 		= CraftableItem(0x1db9, 36, 30, "leather cap")
LeatherGloves 	= CraftableItem(0x13c6, 36, 37, "leather gloves")
LeatherSleeves 	= CraftableItem(0x13cd, 36, 44, "leather leggings")
LeatherLeggings = CraftableItem(0x13cb, 36, 51, "leather sleeves")
LeatherTunic 	= CraftableItem(0x13cc, 36, 58, "leather tunic")
# *****Studded Armor*****
StuddedGorget 	= CraftableItem(0x13d6, 50, 2, "studded gorget")
StuddedGloves 	= CraftableItem(0x13d5, 50, 9, "studded gloves")
StuddedSleeves 	= CraftableItem(0x13dc, 50, 16, "studded leggings")
StuddedLeggings = CraftableItem(0x13da, 50, 23, "studded sleeves")
StuddedTunic 	= CraftableItem(0x13db, 50, 30, "studded tunic")
# *****Female Armor*****
LeatherShorts 		= CraftableItem(0x1c00, 57, 2, "leather shorts")
LeatherSkirt 		= CraftableItem(0x1c08, 57, 9, "leather skirt")
LeatherBustier 		= CraftableItem(0x1c0a, 57, 16, "leather bustier")
StuddedBustier 		= CraftableItem(0x1c0c, 57, 23, "studded bustier")
FemaleLeatherArmor 	= CraftableItem(0x1c06, 57, 30, "female leather armor")
StuddedArmor 		= CraftableItem(0x1c02, 57, 37, "studded armor")
# *****Bone Armor*****
BoneHelmet 		= CraftableItem(0x1451, 64, 2, "bone helmet")
BoneGloves 		= CraftableItem(0x1450, 64, 9, "bone gloves")
BoneArms 		= CraftableItem(0x144e, 64, 16, "bone leggings")
BoneLeggings 	= CraftableItem(0x1452, 64, 23, "bone arms")
BoneArmor 		= CraftableItem(0x144f, 64, 30, "bone armor")

class BOD:
	Gump = 0x5afbd742
	GumpCombineResponse = 2
	LeatherItems = ["shoes", "sandals", "boots", "leather", "studded", "bone"]
	LeatherTypes = ["spined", "horned", "barbed"]

	def __init__(self, id):
		self.id = id
		self.item = self.GetItem()
		self.amount = self.GetAmount()
		self.completed = self.GetCompleted()
		self.material = self.GetMaterial()
		self.isBone = self.CheckIfBone()
		self.isCompletable = self.CheckIfCompletable()


	def GetItem(self):
		if DEBUG: SysMessage("[debug]:In BOD.GetItem", debugTextColor)
		UseObject(self.id)
		WaitForGump(BOD.Gump, 5000)
		if not GumpExists(BOD.Gump):
			SysMessage("Looking for BOD Gump and not found", errorTextColor)
			return None
			
		items = [Skullcap, Bandana, FloppyHat, WideBrimHat, TallStrawHat, StrawHat, WizardHat, Bonnet, FeatheredHat,
				TricornHat, JesterHat, Doublet, FancyShirt, Shirt, Surcoat, PlainDress, FancyDress, Cloak, Robe,
				JesterSuit, ShortPants, LongPants, Kilt, BodySash, HalfApron, FullApron, ThighBoots, Sandals, Shoes,
				Boots, LeatherGorget, LeatherCap, LeatherGloves, LeatherLeggings, LeatherSleeves, LeatherTunic, 
				StuddedGorget, StuddedGloves, StuddedLeggings, StuddedSleeves, StuddedTunic, LeatherShorts, 
				LeatherSkirt, LeatherBustier, StuddedBustier, FemaleLeatherArmor, StuddedArmor, BoneHelmet, BoneGloves,
				BoneLeggings, BoneArms, BoneArmor, Skirt, Tunic, Cap]
		
		
		for i in items:
			if InGump(BOD.Gump, i.name): 
				return i

		SysMessage("Did not find a supported item in the BOD Gump", errorTextColor)
		self.isCompletable = False
		return None


	def GetMaterial(self):
		if DEBUG: SysMessage("[debug]:In BOD.GetMaterials", debugTextColor)
		materialType = "cloth"
		UseObject(self.id)
		WaitForGump(BOD.Gump, 5000)
		if not GumpExists(BOD.Gump):
			SysMessage("Looking for BOD Gump and not found", errorTextColor)
			return None

		for text in BOD.LeatherItems:
			if InGump(BOD.Gump, text):
				materialType = "leather"
				for type in BOD.LeatherTypes:
					if InGump(BOD.Gump, type):
						materialType = type

		SysMessage("[debug]:Material type is: " + materialType, debugTextColor)
		return materialType


	def CheckIfBone(self):
		if DEBUG: SysMessage("[debug]:In BOD.CheckIfBone", debugTextColor)
		
		UseObject(self.id)
		WaitForGump(BOD.Gump, 5000)
		if not GumpExists(BOD.Gump):
			SysMessage("Looking for BOD Gump and not found", errorTextColor)
			return False
		
		return InGump(BOD.Gump, "bone")


	def CheckIfCompletable(self):
		completable = True
		if self.material == "cloth":
			completable = not(Material.outOfCloth)
		elif self.material == "leather":
			completable = not(Material.outOfLeather)
		elif self.material == "spined":
			completable = not(Material.outOfSpined)
		elif self.material == "horned":
			completable = not(Material.outOfHorned)
		elif self.material == "barbed":
			completable = not(Material.outOfBarbed)
			
		if self.isBone:
			completable = completable and not(Material.outOfBone)
			
		return completable

	def GetAmount(self):
		if DEBUG: SysMessage("[debug]:In BOD.GetAmount", debugTextColor)
		amount = 0
		amount = PropertyValue[int](self.id, "Amount to make:")
		return amount


	def GetCompleted(self):
		if DEBUG: SysMessage("[debug]:In BOD.GetCompleted", debugTextColor)
		completed = 0
		bod = Engine.Items.GetItem(self.id)
		for property in bod.Properties:
			if DEBUG: SysMessage("[debug]:property: " + property.Text, debugTextColor)
			if self.item.name in property.Text:
				for arg in property.Arguments:
					if DEBUG: SysMessage("[debug]:argument: " + arg, debugTextColor)
				completed = int(property.Arguments[1])
		
		return completed
		
		
bod = BOD(0x40023709)
#bod = BOD(0x4003abe1)
#bod = BOD(0x40023541)

print("ID: " + str(bod.id))
print("Graphic: " + str(bod.item.graphic))
print("Amount to make: " + str(bod.amount))
print("Material: " + bod.material)
print("Amount completed: " + str(bod.completed))
print("Is Bone: " + str(bod.isBone))
print("Is completable: " + str(bod.isCompletable))




# *****MISC******
textColor = 43
errorTextColor = 33
debugTextColor = 16
stopOnOutOfResource = True

# *****GUMPS*****
tailorGump 	= 0x38920abd
tinkerGump 	= 0x38920abd
BODBookGump = 0x54f555df
tailorMaterialResponse = 7
tailorLeatherResponse = 6
tailorSpinedResposne = 13
tailorHornedResponse = 20
tailorBarbedResponse = 27

# *****BOD*******
BOD = 0x2258
TailorBODhue = 1155

# *************************
# ******  FUNCTIONS  ******
# *************************

def GetRestockContainer():
	if DEBUG: SysMessage("[debug]:In GetRestockContainer", debugTextColor)
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
	if DEBUG: SysMessage("[debug]:In UnloadMaterials", debugTextColor)
	materials = [ingots, cloth, leather, spined, horned, barbed, bone]
	container = GetRestockContainer()
	for x in materials:
		if not (skipIngots and x == ingots):
			MoveType(x.graphic, "backpack", container, -1, -1, -1)

def RefillMaterial(type):
	if DEBUG: SysMessage("[debug]:In RefillMaterial", debugTextColor)
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
	if DEBUG: SysMessage("[debug]:In SetLeatherType", debugTextColor)
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

	
		
def CraftTinkerItem(item):
	if DEBUG: SysMessage("[debug]:In CraftTinkerItem", debugTextColor)
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
	if DEBUG: SysMessage("[debug]:In GetScissors", debugTextColor)
	while not FindType(Scissors.graphic, 1, "backpack"):
		CraftTinkerItem(Scissors)
	FindType(Scissors.graphic, 1, "backpack")
	return GetAlias("found")


def GetSewingKit():
	if DEBUG: SysMessage("[debug]:In GetSewingKit", debugTextColor)
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
	if DEBUG: SysMessage("[debug]:In CraftTailorItem", debugTextColor)
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
	if DEBUG:SysMessage("[debug]:In BookDeedsRemaining", debugTextColor)
	bodBook = GetAlias("smith bod source")
	
	if not bodBook == 0:
		remaining = PropertyValue[int](bodBook, "Deeds in Book:")
		return remaining
	else:
		SysMessage("Did not find the 'smith bod source' alias", errorTextColor)
		return 0


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
			CloseGump(BODGump)
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
