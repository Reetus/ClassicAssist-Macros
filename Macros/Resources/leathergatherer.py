# Name: Leather Gatherer
# Description: Gathers leather from corpses next to you. Read instructions.
# Author: Kakagriss
# Shard: UOG-Demise
# Date: Mon Mar 07 2022

# Instructions: You will need a butcher's war cleaver in your backpack. Happy gathering!


if FindType(0x2d2f, -1, "backpack") and "butcher's war cleaver" in Name("found"):
	cleaver = GetAlias("found")
else:
	SysMessage("You fool! You don't have a proper blade. Stopping", 33)
	Stop()	
ClearIgnoreList()
while not Dead():
	while FindType(0x2006, 2):
		corpse = GetAlias("found")
		if Weight() >= MaxWeight():
			HeadMsg("OVERWEIGHT! Stopping", "self", 33)
			Stop()
		else:
			if not TargetExists():
				if FindObject(cleaver, -1, "backpack"):
					UseObject("found")
					WaitForTarget(5000)
					Target(corpse)
					IgnoreObject(corpse)
