# Author: raveX
# Description: Smith BOD Filler

SetQuietMode(True)

if not FindAlias('smith bod source'):
  	PromptAlias('smith bod source')

if not FindAlias('smith bod destination'):
  	PromptAlias('smith bod destination')

if not FindAlias('smith bod filler restock'):
  	PromptAlias('smith bod filler restock')
  	
class SmithItem:
	def __init__(self, graphic, gumpResponse1, gumpResponse2):
		self.graphic = graphic
		self.gumpResponse1 = gumpResponse1
		self.gumpResponse2 = gumpResponse2


# *****MISC******
errorTextColor = 33

# *****GUMPS*****
smithGump 	= 0x38920abd
tinkerGump 	= 0x38920abd
BODGump 	= 0x5afbd742
BODBookGump 	= 0x54f555df

# *****Ingots******
ingots = 0x1bf2
ironIngotHue 	= 0
dullIngotHue 	= 2419
shadowIngotHue 	= 2406
copperIngotHue 	= 2413
bronzeIngotHue 	= 2418
goldIngotHue 	= 2213
agapiteIngotHue = 2425
veriteIngotHue 	= 2207
valoriteIngotHue = 2219

# *****BOD*******
BOD = 0x2258
SmithBODcolor = 0x44e

# *****Tools******
tongs = 0xfbb
tinkerTool = 0x1eb8
smithHammer = 0x13e3

# *************************
# ****** SMITH ITEMS ******
# *************************
# For your server, your gump responses may be different than those listed here.
# You can easily determine what they should be by creating a test macro,
# record crafting each item, and replacing the values below.  The itemGraphics should
# not need to change (unless you are on a very custom shard)
# *************************
# FORMAT: SmithItem(itemGraphic, GumpResponse1, GumpResponse2)
# *************************
# *****Bladed*****
Broadsword 	= SmithItem(0xf5e,  22, 9)
Cutlass 	= SmithItem(0x1441, 22, 23)
Dagger 		= SmithItem(0xf52,  22, 30)
Katana 		= SmithItem(0x13ff, 22, 37)
Kryss 		= SmithItem(0x1401, 22, 44)
Longsword 	= SmithItem(0xf61,  22, 51)
Scimitar 	= SmithItem(0x13b6, 22, 58)
Viking 		= SmithItem(0x13b9, 22, 65)
# *****Axes*****
Axe 		= SmithItem(0xf49,  29, 2)
BattleAxe 	= SmithItem(0xf47,  29, 9)
DoubleAxe 	= SmithItem(0xf4b,  29, 16)
ExecutionerAxe 	= SmithItem(0xf45,  29, 23)
LargeBattleAxe 	= SmithItem(0x13fb, 29, 30)
TwoHandedAxe 	= SmithItem(0x1443, 29, 37)
WarAxe 		= SmithItem(0x13b0, 29, 44)
# *****Polearms*****
Bardiche 	= SmithItem(0xf4d,  36, 2)
Halberd 	= SmithItem(0x143e, 36, 23)
ShortSpear 	= SmithItem(0x1403, 36, 44)
Spear 		= SmithItem(0xf62,  36, 58)
WarFork 	= SmithItem(0x1405, 36, 65)
# *****Bashing*****
HammerPick	= SmithItem(0x143d, 43, 2)
Mace 		= SmithItem(0xf5c,  43, 9)
Maul 		= SmithItem(0x143b, 43, 16)
WarMace 	= SmithItem(0x1407, 43, 30)
WarHammer 	= SmithItem(0x1439, 43, 37)
# *****Ringmail*****
RingmailGloves 		= SmithItem(0x13eb, 1, 2)
RingmailLeggings 	= SmithItem(0x13f0, 1, 9)
RingmailSleeves 	= SmithItem(0x13ee, 1, 16)
RingmailTunic 		= SmithItem(0x13ec, 1, 23)
# *****Chainmail*****
ChainmailCoif 		= SmithItem(0x13bb, 1, 30)
ChainmailLeggings 	= SmithItem(0x13be, 1, 37)
ChainmailTunic 		= SmithItem(0x13bf, 1, 44)
# *****Platemail*****
PlateArms 	= SmithItem(0x1410, 1, 51)
PlateGloves 	= SmithItem(0x1414, 1, 58)
PlateGorget 	= SmithItem(0x1413, 1, 65)
PlateLegs 	= SmithItem(0x1411, 1, 72)
PlateTunic 	= SmithItem(0x1415, 1, 79)
# *****Helms*****
Bascinet 	= SmithItem(0x140c, 8, 2)
CloseHelm 	= SmithItem(0x1408, 8, 9)
Helmet 		= SmithItem(0x140a, 8, 16)
NorseHelm 	= SmithItem(0x140e, 8, 23)
PlateHelm 	= SmithItem(0x1412, 8, 30)
# *****Shields*****
Buckler 		= SmithItem(0x1b73, 15, 2)
BronzeShield 		= SmithItem(0x1b72, 15, 9)
HeaterShield 		= SmithItem(0x1b76, 15, 16)
MetalShield 		= SmithItem(0x1b7b, 15, 23)
MetalKiteShield 	= SmithItem(0x1b74, 15, 30)
TearKiteShield 		= SmithItem(0x1b79, 15, 37)




def RefillIngots():
	container = GetAlias('smith bod filler restock')
	if CountType(ingots, "backpack") < 20:
		if CountType(ingots, container) == 0:
			SysMessage("OUT OF INGOTS!", errorTextColor)
			CancelTarget()
			Stop()
		else:
			MoveType(ingots, container, "backpack", -1, -1, -1, ironIngotHue, 1000)
			Pause(1500)


def CraftTinkerTool():
	RestockIngots()
	UseType(tinkerTool)
	WaitForGump(tinkerGump, 5000)
	ReplyGump(tinkerGump, 15)
	WaitForGump(tinkerGump, 5000)
	ReplyGump(tinkerGump, 23)
	Pause(1500)


def CraftTongs():
	if CountType(tinkerTool, "backpack") < 2:
		while CountType(tinkerTool, "backpack") < 2:
			CraftTinkerTool()
	while CountType(tongs, "backpack") < 5:
		UseType(tinkerTool)
		WaitForGump(tinkerGump, 5000)
		ReplyGump(tinkerGump, 15)
		WaitForGump(tinkerGump, 5000)
		ReplyGump(tinkerGump, 86)
		WaitForGump(tinkerGump, 5000)
		Pause(600)


def CheckForTongs():
	# Check for tongs
	if not FindType(tongs, 1, "backpack"):
		container = GetAlias('smith bod filler restock')
		if not FindType(tongs, 2, container):
			CraftTongs()
		else:
			MoveType(tongs, container, "backpack")
			Pause(1500)

	if FindType(tongs, 1, "backpack"):		
		currentTong = GetAlias("found")
		UseObject(currentTong)
		WaitForGump(smithGump, 5000)


def CraftItem(itemGraphic, gumpResponse1, gumpResponse2):
	ReplyGump(smithGump, gumpResponse1)
	WaitForGump(smithGump, 5000)
	ReplyGump(smithGump, gumpResponse2)
	WaitForGump(smithGump, 5000)
	Pause(500)
	while FindType(itemGraphic, 1, "backpack"):
		Target("found")
		WaitForTarget(2000)
		if not TargetExists() and InJournal("must be exceptional"):
			ReplyGump(smithGump, 14)
			WaitForTarget(5000)
			Target("found")
			Pause(1500)
			# Bring back the target cursor
			ReplyGump(BODGump, 2)
			WaitForGump(BODGump, 5000)
			WaitForTarget(5000)
			ClearJournal()


def BookDeedsRemaining():
	bodBook = GetAlias("smith bod source")
	remaining = PropertyValue[int](bodBook, "Deeds in Book:")
	return remaining



# Search for BOD to Fill
if FindType(BOD, 1, "backpack", SmithBODcolor):
	currentBOD = GetAlias("found")
	UseObject(currentBOD)
	WaitForGump(BODGump, 5000)
	# Select the combine option
	ReplyGump(BODGump, 2)
	WaitForGump(BODGump, 5000)
	WaitForTarget(5000)

	while TargetExists():
		RefillIngots()
		CheckForTongs()
		# ********** BLADED **********
		if InGump(BODGump, "broadsword"):
			CraftItem(Broadsword)
		elif InGump(BODGump, "cutlass"):
			CraftItem(Cutlass)
		elif InGump(BODGump, "dagger"):
			CraftItem(Dagger)
		elif InGump(BODGump, "katana"):
			CraftItem(Katana)
		elif InGump(BODGump, "kryss"):
			CraftItem(Kryss)
		elif InGump(BODGump, "longsword"):
			CraftItem(Longsword)
		elif InGump(BODGump, "scimitar"):
			CraftItem(Scimitar)
		elif InGump(BODGump, "viking"):
			CraftItem(Viking)
		# ********** AXES **********
		# NOTE: The order in which these are called matters here
		# ********** **** **********
		elif InGump(BODGump, "large battle axe"):
			CraftItem(LargeBattleAxe)
		elif InGump(BODGump, "battle axe"):
			CraftItem(BattleAxe)
		elif InGump(BODGump, "double axe"):
			CraftItem(DoubleAxe)
		elif InGump(BODGump, "executioner"):
			CraftItem(ExecutionerAxe)
		elif InGump(BODGump, "two handed axe"):
			CraftItem(TwoHandedAxe)
		elif InGump(BODGump, "war axe"):
			CraftItem(WarAxe)
		elif InGump(BODGump, "axe"):
			CraftItem(Axe)
		# ********** POLEARMS **********
		elif InGump(BODGump, "bardiche"):
			CraftItem(Bardiche)
		elif InGump(BODGump, "halberd"):
			CraftItem(Halberd)		
		elif InGump(BODGump, "short spear"):
			CraftItem(ShortSpear)
		elif InGump(BODGump, "spear"):
			CraftItem(Spear)
		elif InGump(BODGump, "war fork"):
			CraftItem(WarFork)
		# ********** BASHING **********
		# NOTE: War mace MUST be searched for before mace
		# ********** ******* **********
		elif InGump(BODGump, "hammer pick"):
			CraftItem(HammerPick)
		elif InGump(BODGump, "war mace"):
			CraftItem(WarMace)
		elif InGump(BODGump, "mace"):
			CraftItem(Mace)
		elif InGump(BODGump, "maul"):
			CraftItem(Maul)		
		elif InGump(BODGump, "war hammer"):
			CraftItem(WarHammer)
		# ********** HELMETS **********
		elif InGump(BODGump, "bascinet"):
			CraftItem(Bascinet)
		elif InGump(BODGump, "close helm"):
			CraftItem(CloseHelm)
		elif InGump(BODGump, "helmet"):
			CraftItem(Helmet)
		elif InGump(BODGump, "norse helm"):
			CraftItem(NorseHelm)
		elif InGump(BODGump, "plate helm"):
			CraftItem(PlateHelm)
		# ********** SHIELDS **********
		elif InGump(BODGump, "buckler"):
			CraftItem(Buckler)
		elif InGump(BODGump, "bronze shield"):
			CraftItem(BronzeShield)
		elif InGump(BODGump, "heater shield"):
			CraftItem(HeaterShield)
		elif InGump(BODGump, "metal shield"):
			CraftItem(MetalShield)
		elif InGump(BODGump, "metal kite shield"):
			CraftItem(MetalKitShield)
		elif InGump(BODGump, "tear kite shield"):
			CraftItem(TearKiteShield)
		# ********** RINGMAIL **********
		elif InGump(BODGump, "ringmail gloves"):
			CraftItem(RingmailGloves)
		elif InGump(BODGump, "ringmail leggings"):
			CraftItem(RingmailLeggings)
		elif InGump(BODGump, "ringmail sleeves"):
			CraftItem(RingmailSleeves)
		elif InGump(BODGump, "ringmail tunic"):
			CraftItem(RingmailTunic)
		# ********** CHAINMAIL **********
		elif InGump(BODGump, "chainmail coif"):
			CraftItem(ChainmailCoif)
		elif InGump(BODGump, "chainmail leggings"):
			CraftItem(ChainmailLeggings)
		elif InGump(BODGump, "chainmail tunic"):
			CraftItem(ChainmailTunic)
		# ********** PLATEMAIL **********
		elif InGump(BODGump, "platemail arms"):
			CraftItem(PlateArms)
		elif InGump(BODGump, "platemail gloves"):
			CraftItem(Plategloves)
		elif InGump(BODGump, "platemail gorget"):
			CraftItem(PlateGorget)
		elif InGump(BODGump, "platemail legs"):
			CraftItem(PlateLegs)
		elif InGump(BODGump, "platemail tunic"):
			CraftItem(PlateTunic)

	# BOD is complete, move to destination book
	if not TargetExists():
		destination = GetAlias('smith bod destination')
		MoveItem(currentBOD, destination)
		Pause(1500)

# Get A BOD out of the book
elif not BookDeedsRemaining() == 0:
	bodBook = GetAlias("smith bod source")
	UseObject(bodBook)
	WaitForGump(BODBookGump, 5000)
	ReplyGump(BODBookGump, 5)
	Pause(1500)

# All BODs filled / BOD book is empty
else:
	SysMessage("UNABLE TO FIND BODS TO FILL", errorTextColor)
	CancelTarget()
	Stop()
