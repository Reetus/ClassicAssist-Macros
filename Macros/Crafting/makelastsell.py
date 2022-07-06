# Name: Make Last and Sell
# Description: This will use make last in a crafting gump, and attempt to sell to a nearby vendor
# Author: Bittiez
# Shard: Ruins and Riches

#You need to set up an auto sell agent before this will sell items

#This script does never ending Make Last, currently set for tinkering you may need to change it for
#    other crafts gumps
#The script will sell to the specified vendor every 10 items you craft

HeadMsg("What vendor would you like to sell to?", "self")
PromptAlias("vendor")

i = 0
while True:
    ReplyGump(0x38920abd, 21)
    WaitForGump(0x38920abd, 5000)
    i += 1
    if i > 10:
        WaitForContext("vendor", 3, 5000)
        i = 0
