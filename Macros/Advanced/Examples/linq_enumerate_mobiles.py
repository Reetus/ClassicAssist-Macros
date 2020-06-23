# Name: Linq Enumerate Mobiles
# Description: Using Linq with Python to cycle through mobiles with a bunch of conditions...
# Author: Reetus
# Era: Any

import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine

mounts = [0x115, 0xb3]

mount = Engine.Mobiles.Where(lambda m: mounts.Contains(m.ID) 
                                        and m.Distance < 10 
					and not InFriendList(m.Serial) 
					and not InIgnoreList(m.Serial)).FirstOrDefault()

if (mount == None):
	ClearIgnoreList()
	SysMessage('No mount found')
	Stop()

SetEnemy(mount.Serial)
IgnoreObject(mount.Serial)
