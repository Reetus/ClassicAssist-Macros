# Name: Hide All Multis
# Description: Issues a remove object on all multis in range, useful for looking inside the walls of houses
# Author: Reetus
# Era: Any

import clr
import System
clr.AddReference('System.Core')
clr.ImportExtensions(System.Linq)
from Assistant import Engine
from ClassicAssist.UO.Commands import RemoveObject

multis = Engine.Items.Where(lambda i: i.ArtDataID == 2)

for x in multis:
	RemoveObject(x.Serial)
