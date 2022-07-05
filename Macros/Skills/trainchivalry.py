# Name: Train Chivalry
# Description: This will train your Chivalry to 120.
# Author: OnlyAware
# Shard: UO Dreams World
# Date: Mon Jul 04 2022

while not Skill('Chivalry') == 120:
    if Skill('Chivalry') < 40 and Mana('self') > 15:
        Cast("Consecrate Weapon")
        Pause(7000)
    elif Skill('Chivalry') < 55 and Mana('self') > 25:
        Cast("Divine Fury")
        Pause(7000)#
    elif Skill('Chivalry') < 69 and Mana('self') > 20:
        Cast("Enemy of One")
        Pause(7000)
    elif Skill('Chivalry') < 88 and Mana('self') > 20:
        Cast("Holy Light")
        Pause(7000)
    elif Skill('Chivalry') < 100 and Mana('self') > 20:
        Cast("Noble Sacrifice")
        Pause(7000)
