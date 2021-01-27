# Name: Combine Stacks
# Description: Combine multiple stacks of the same item id into one (or more) stacks of 60000
# Author: Reetus
# Era: Any
# Date: Wed Jan 27 2021

import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine
from ClassicAssist.UO.Data import TileData, TileFlags

if PromptAlias('container') == 0:
	Stop()

if not WaitForContents('container', 5000):
	print 'No contents'
	Stop()

container = Engine.Items.GetItem(GetAlias('container')).Container

while True:
	destStack = container.SelectEntity(lambda i: i.Count < 60000 and TileData.GetStaticTile(i.ID).Flags.HasFlag(TileFlags.Stackable) and not InIgnoreList(i.Serial))

	if destStack == None:
		Stop()

	print destStack

	needed = 60000 - destStack.Count

	sourceStack = container.SelectEntities( lambda i: i.ID == destStack.ID and i.Hue == destStack.Hue and i.Serial != destStack.Serial and i.Count != 60000 )
	
	if sourceStack == None:
		IgnoreObject(destStack.Serial)
		continue;
		
	sourceStack = sourceStack.OrderBy( lambda i: i.Count ).FirstOrDefault()
	
	print sourceStack

	MoveItem(sourceStack.Serial, destStack.Serial, sourceStack.Count if needed > sourceStack.Count else needed)
	Pause(1000)