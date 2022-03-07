# Name: Leather gatherer
# Description: Gathers leather from corpses next to you. Read instructions.
# Author: Kakagriss
# Shard: UOG-Demise
# Date: Mon Mar 07 2022

# Instructions: You will need a blade and scissors, or a butcher's war cleaver in your backpack. Happy gathering!

blades = [0x13f6, 0xec3, 0xec4, 0x2d22, 0x2d21, 0x2d35, 0x2d33, 0xf52, 0x1441, 0x13b6, 0x1401, 0xf5e, 0xf61, 0x26bb, 0x13ff]
cleaver = None
blade = None
scissors = None

ClearIgnoreList()

if FindType(0x2d2f, -1, "backpack") and "butcher's war cleaver" in Name("found"):
	if cleaver == None:
		cleaver = GetAlias("found")
else:
	for item in blades:
		if blade == None and FindType(i, -1, "backpack"):
			blade = GetAlias("found")
		if FindType(0xf9f, -1, "backpack"):
			scissors = GetAlias("found")
		else:
			SysMessage("You fool! You don't have any scissors, get some first. Stopping")
			Stop()
			
if cleaver == None and blade == None:
	SysMessage("You fool! You don't have a proper blade, get one first. Stopping")
	Stop()

while not Dead():
	while FindType(0x2006, 2):
		if Weight() >= MaxWeight():
			HeadMsg("OVERWEIGHT! Stopping", "self", 33)
			Stop()
		else:
			if not TargetExists():
				if cleaver != None:
					UseObject(cleaver)
					WaitForTarget(5000)
					Target("found")
					IgnoreObject("found")
				elif blade != None:
					UseObject(blade)
					WaitForTarget(5000)
					Target("found")
					Pause(100)
					UseObject("found")
					WaitForContents("found", 5000)
					if FindType(0x1079, -1, "found"):
						MoveItem("found", "backpack")
						Pause(1000)
					while FindType(0x1079, -1, "backpack"):
						UseObject(scissors)
						WaitForTarget(5000)
						Target("found")
						Pause(100)
		IgnoreObject("found")