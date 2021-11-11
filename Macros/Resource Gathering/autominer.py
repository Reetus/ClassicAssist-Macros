# Name: Auto Miner
# Description: Unattended cave mining
# Author: Batt11
# Shard: Dark Forest
# Date: Tue Nov 09 2021

from Assistant import Engine
from System import Random

dir = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']

SetQuietMode(True)

if not FindAlias('forge'):
	PromptAlias('forge')
	
#Roomba Walk, turn a random directions and contiue
def Roomba():
	int = Random().Next(8) # 0-7
	if not Walk(Direction('self')):
		Turn(dir[int])
	return

#Did you walk out of the cave?
def OutofCave():
	if (Direction('self') == "North"):
		Turn("South")
		BackinCave()
	elif (Direction('self') == "Northeast"):
		Turn("Southwest")
		BackinCave()
	elif (Direction('self') == "East"):
		Turn("West")
		BackinCave()
	elif (Direction('self') == "Southeast"):
		Turn("Northwest")
		BackinCave()
	elif (Direction('self') == "South"):
		Turn("North")
		BackinCave()
	elif (Direction('self') == "Southwest"):
		Turn("Northeast")
		BackinCave()
	elif (Direction('self') == "West"):
		Turn("East")
		BackinCave()
	elif (Direction('self') == "Northwest"):
		Turn("Southeast")
		BackinCave()
	return

#walk 6 steps to get back into the cave
def BackinCave():	
	for x in range(6):
		Walk(Direction('self'))
	return

#Make a shovel when none are left
def MakeShovel ():
	if FindType(0x1eb8, 0, 'backpack'):
		UseObject('Found')				#Tinker Tools
		WaitForGump(0x38920abd, 5000)
		ReplyGump(0x38920abd, 22)		#Tools Option
		WaitForGump(0x38920abd, 5000)
		ReplyGump(0x38920abd, 72)		#Shovel option
		WaitForGump(0x38920abd, 5000)
		ReplyGump(0x38920abd, 0)		#Close tools
	else:
		HeadMsg("Out of Tinker Tools", "self")
		Stop()
	return

#Smelt ore in mobile forge
def smelt():
	while FindType(0x19b9, 0, 'backpack'):
		Pause(1000)
		UseObject("found")
		WaitForPrompt(2000)
		Target("forge")
	return	
	
#Main loop
while not Dead('self'):
	#Look for Shovel or Pickaxe
	if FindType(0xf39, 0, 'backpack') or FindType(0xe85, 0, 'backpack'):
		UseObject('Found')
	else:
		MakeShovel()
	WaitForTarget(5000)

	#dig in front of you
	if (Direction('self') == "North"):
		TargetTileOffsetResource(0, -1, 0)
	elif (Direction('self') == "Northeast"):
		TargetTileOffsetResource(1, -1, 0)
	elif (Direction('self') == "East"):
		TargetTileOffsetResource(1, 0, 0)
	elif (Direction('self') == "Southeast"):
		TargetTileOffsetResource(1, 1, 0)
	elif (Direction('self') == "South"):
		TargetTileOffsetResource(0, 1, 0)
	elif (Direction('self') == "Southwest"):
		TargetTileOffsetResource(-1, 1, 0)
	elif (Direction('self') == "West"):
		TargetTileOffsetResource(-1, 0, 0)
	elif (Direction('self') == "Northwest"):
		TargetTileOffsetResource(-1, -1, 0)
	Pause(2000)

	#Move when there is nothing to mine or when a wall is hit
	if InJournal("There is no metal here to mine", "system") or InJournal("Target cannot be seen", "system")  or InJournal("You can't mine that", "system"):
		ClearJournal()   
		Roomba()
	#Turn around if you try to mine something other than cave floor
	if InJournal("You can't mine there"):
		ClearJournal()
		OutofCave()
	#Smelt when it gets to heavy	
	if DiffWeight() < 10:
		Smelt()