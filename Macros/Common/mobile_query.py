# Name: Mobile Query
# Description: Use as a background macro to refresh health bars
# Author: Reetus
# Shard: OSI

from ClassicAssist.UO.Commands import MobileQuery
from Assistant import Engine

def QueryAllMobiles():
	mobiles = Engine.Mobiles.GetMobiles()
	
	for x in range(len(mobiles)):
		mobile = mobiles[x]
		if (mobile != None and mobile.Distance < 5):
			MobileQuery(mobile.Serial)
			Pause(1000)

QueryAllMobiles()
Pause(2000)
