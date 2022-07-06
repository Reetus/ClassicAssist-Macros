# Name: Arms Lore Training
# Description: Used for training arms lore on as many items as you wish
# Author: bittiez
# Shard: Ruins and Riches
# Date: Tue Jul 05 2022

# Play the macro, select the type of item you want to use arms lore on
# The macro will use arms lore on each item of that type, so if you have 10 scimitars for example
#   it will use the skill 30 times in total.
# I reccomend using this while training blacksmithy
# And yes for some reason Ruins and Riches reports skill names without the last letter

PromptAlias("itemType")
type = GetAlias("itemType")
trys = 3

i=0
ClearIgnoreList()
while FindType(Graphic(type), -1, "backpack"):
    UseSkill("arms lor")
    WaitForTarget(5000)
    Target("found")
    if i >= trys:
        IgnoreObject("found")
        i = 0
    i += 1
    Pause(1000)