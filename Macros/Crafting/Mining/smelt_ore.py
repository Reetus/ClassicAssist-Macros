# Name: Smelt Ore
# Description: Smelt ore from a container and put ingots on ground back into container
# Author: Reetus
# Era: Any

from Assistant import Engine

if not FindObject('ore chest'):
	PromptAlias('ore chest')

if not FindObject('forge'):
	PromptAlias('forge')

oreTypes = [0x19b7, 0x19b8, 0x19b9, 0x19ba]

ClearIgnoreList()

for ore in oreTypes:
	while FindType(ore, -1, 'ore chest'):
		if Graphic('found') == 0x19b7:
			item = Engine.Items.GetItem(GetAlias('found'))
			if item.Count <= 1:
				IgnoreObject('found')
				continue
		UseObject('found')
		WaitForTarget(5000)
		Target('forge')
		Pause(1000)
		while FindType(0x1bf2, 3):
			MoveItem('found', 'ore chest')
			Pause(1000)
			IgnoreObject('found')
		while FindType(0x1bf2, -1, 'backpack'):
			MoveItem('found', 'ore chest')
			Pause(1000)
			IgnoreObject('found')
