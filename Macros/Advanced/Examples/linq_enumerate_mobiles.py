# Name: Linq Enumerate Mobiles
# Description: Using Linq with Python to get mobiles with a bunch of conditions...
# Author: Reetus
# Era: Any

import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine

# Possible notorieties
# Innocent, Ally, Attackable, Criminal, Enemy, Murderer, Invulnerable

humans = [0x190, 0x191]

def GetMobiles(ids = None, notorieties = None, includeFriends = False, includeIgnored = False, maxDistance = 32, orderBy = lambda m: m.Distance):
	mobiles = Engine.Mobiles.Where(lambda m: (ids == None or ids.Contains(m.ID))
                                             	and m.Distance < maxDistance
                                             	and m.Serial != Engine.Player.Serial
                                             	and (notorieties == None or notorieties.Contains(m.Notoriety.ToString()))
						and (includeFriends or not InFriendList(m.Serial))
						and (includeIgnored or not InIgnoreList(m.Serial))).OrderBy(orderBy)
	return mobiles

# Get 1 
mobile = GetMobiles(ids = humans, notorieties = ['Murderer'], maxDistance = 10).First()
HeadMsg(mobile.Name, 'self')

# Get 2
mobiles = GetMobiles(ids = humans, notorieties = ['Murderer', 'Innocent'], maxDistance = 10, includeFriends = True).Take(2)

for m in mobiles:
	HeadMsg(m.Name, 'self')

# Order by Hits
mobile = GetMobiles(orderBy = lambda m: m.Hits, notorieties = ['Innocent']).First()
HeadMsg(mobile.Name + ' - ' + str(mobile.Hits), 'self')

# Order by Hits, ThenBy alphabetical
mobile = GetMobiles(orderBy = lambda m: m.Hits).ThenBy(lambda m: m.Name).First()
HeadMsg(mobile.Name + ' - ' + str(mobile.Hits), 'self')

# Get all less than 5, and select just the serials
mobiles = GetMobiles(maxDistance = 5, includeFriends = True).Select(lambda m: m.Serial)

for m in mobiles:
	HeadMsg(hex(m), 'self')

# Only friends
mobiles = GetMobiles(maxDistance = 15, includeFriends = True).Where(lambda m: InFriendList(m.Serial))

for m in mobiles:
	HeadMsg(m.Name, 'self')


