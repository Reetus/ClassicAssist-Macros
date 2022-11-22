# Name: Train Necromancy
# Description: you need Wraith,Horrific and Lich form spells
# Author: merlottt
# Shard: uogames.org
# Date: Mon Nov 21 2022

#script to Train Necromancy
while Skill('Necromancy') < 100:
    if Skill('Necromancy') > 20 and Skill('Necromancy') <= 50:
        Cast("Wraith Form")
    if Skill('Necromancy') > 50 and Skill('Necromancy') <= 70:
        Cast("Horrific Beast")
    if Skill('Necromancy') > 70 and Skill('Necromancy') <= 100:
        Cast("Lich Form")      
    Pause(2000)