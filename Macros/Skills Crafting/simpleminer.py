# Name: Simple Miner
# Description: A simple miner i have made that mines until a certain weight is met then just recalls to the blacksmith area in luna to smelt the ore and bank then the script stops and will start when i make it back the my mining area
# Author: HellForge
# Era: Any
# Date: Sun Mar 21 2021

UseType(0xf39)
WaitForTarget(5000)
TargetTileRelative("self", 1, False)

if Weight() >= 415:
	Cast("Recall")
	WaitForTarget(5000)
	Target(0x40047054)
	Stop()
