# Name: test
# Description: Test
# Author: Reetus
# Shard: Demise
# Date: Sat Dec 23 2023

Cast('Energy Vortex')
if not WaitForTargetOrFizzle(30000):
	HeadMsg('fizzled', 'self')
	Stop()
TargetTileRelative("self", 1, False)
