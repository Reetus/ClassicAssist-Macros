# Author: raveX
# Description: Smith BOD Filler

SetQuietMode(True)

if not FindAlias('smith bod source'):
  	PromptAlias('smith bod source')

if not FindAlias('smith bod destination'):
  	PromptAlias('smith bod destination')

if not FindAlias('smith bod filler restock'):
  	PromptAlias('smith bod filler restock')


# *****MISC******
smithGump = 0x38920abd
tinkerGump = 0x38920abd
errorTextColor = 33
# *****Ingots******
ingots = 0x1bf2
ironIngotHue = 0
dullIngotHue = 2419
shadowIngotHue = 2406
copperIngotHue = 2413
bronzeIngotHue = 2418
goldIngotHue = 2213
agapiteIngotHue = 2425
veriteIngotHue = 2207
valoriteIngotHue = 2219
# *****BOD*******
BOD = 0x2258
SmithBODcolor = 0x44e
BODGump = 0x5afbd742
BODBookGump = 0x54f555df
# *****Tools******
tongs = 0xfbb
tinkerTool = 0x1eb8
smithHammer = 0x13e3
# *****Swords*****
Katana = 0x13ff
Viking = 0x13b9
Broadsword = 0xf5e
Longsword = 0xf61
Cutlass = 0x1441
Scimitar = 0x13b6
# *****Axes*****
Executioner = 0xf45
DoubleAxe = 0xf4b
TwoHandedAxe = 0x1443
LargeBattleAxe = 0x13fb
BattleAxe = 0xf47
Axe = 0xf49
Bardiche = 0xf4d
Halberd = 0x143e
# *****Mace*****
WarAxe = 0x13b0
Maul = 0x143b
WarMace = 0x1407
HammerPick = 0x143d
WarHammer = 0x1439
Mace = 0xf5c
# *****Fencing*****
Kryss = 0x1401
Dagger = 0xf52
WarFork = 0x1405
ShortSpear = 0x1403
Spear = 0xf62
# *****Ringmail*****
RingmailGloves = 0x13eb
RingmailSleeves = 0x13ee
RingmailTunic = 0x13ec
RingmailLeggings = 0x13f0
# *****Chainmail*****
ChainmailCoif = 0x13bb
ChainmailLeggings = 0x13be
ChainmailTunic = 0x13bf
# *****Platemail*****
PlateArms = 0x1410
PlateLegs = 0x1411
PlateGorget = 0x1413
PlateGloves = 0x1414
PlateTunic = 0x1415
# *****Helms*****
PlateHelm = 0x1412
Helmet = 0x140a
CloseHelm = 0x1408
Bascinet = 0x140c
NorseHelm = 0x140e
# *****Shields*****
Metal = 0x1b7b
Buckler = 0x1b73
Bronze = 0x1b72
TearKite = 0x1b79
MetalKite = 0x1b74
Heater = 0x1b76


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


def CraftItem(itemType, gumpOption1, gumpOption2):
	ReplyGump(smithGump, gumpOption1)
	WaitForGump(smithGump, 5000)
	ReplyGump(smithGump, gumpOption2)
	WaitForGump(smithGump, 5000)
	Pause(500)
	while FindType(itemType, 1, "backpack"):
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
		# Craft
		if InGump(BODGump, "dagger"):
			CraftItem(Dagger, 22, 30)
		elif InGump(BODGump, "buckler"):
			CraftItem(Buckler, 15, 2)
		elif InGump(BODGump, "mace"):
			CraftItem(Mace, 43, 9)

	# BOD is complete, move to destination book
	if not TargetExists():
		destination = GetAlias('smith bod destination')
		MoveItem(currentBOD, destination)
		Pause(1500)

elif not BookDeedsRemaining() == 0:
	bodBook = GetAlias("smith bod source")
	UseObject(bodBook)
	WaitForGump(BODBookGump, 5000)
	ReplyGump(BODBookGump, 5)
	Pause(1500)
else:
	SysMessage("UNABLE TO FIND BODS TO FILL", errorTextColor)
	CancelTarget()
	Stop()
		
				
			
			
