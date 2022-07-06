# Name: Smelt Items
# Description: Smelts all items of a specified type
# Author: Bittiez
# Shard: Ruins and Riches

# You should already have your blacksmith crafting window open before you run this
# The macro will ask you what item type to smelt
#   The macro will attempt to smelt all items of that type in your inventory
#       Be careful if you have items of that type you wish to keep!

PromptAlias("smeltItem")
type = Graphic(GetAlias("smeltItem"))

ClearIgnoreList()
for item in type:
    while FindType(item, -1, "backpack"):
        ReplyGump(0x38920abd, 14)
        WaitForTarget(5000)
        Target("found")
        WaitForGump(0x38920abd, 5000)