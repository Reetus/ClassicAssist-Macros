# Name: Healing Trainer
# Description: A simple to use healing trainer that uses magic arrow to damage yourself then heal use bandages
# Author: vertex101
# Era: Any
# Date: Thu Apr 01 2021

SetQuietMode(True) # this is so the chat in-game is not spammed with Object found updated
while not Dead("self"):
	if not FindType(0xe21, -1, "backpack"):
		HeadMsg("Out of Bandages", "self", 33)
		Stop()
	if Skill("Healing") == SkillCap("Healing"):
		HeadMsg("Heal training finished !!!", "self", 1194)
		Stop()
	if Hits("self") <= 20: #adjust this based of your HP
		while Hits('self') < MaxHits("self"):
			BandageSelf()
			Pause(7000) # adjust this based on your character stats
	else:
		Cast("Magic Arrow")
		WaitForTarget(5000)
		Target("self")
		Pause(2000) # adjust this based on your FC/FCR
