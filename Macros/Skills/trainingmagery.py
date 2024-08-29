# Name: Training Magery
# Description: Train magery skill until the goal you want.
# Author: Lissandro
# Shard: UOG-Demise
# Date: Wed Aug 28 2024


GOAL = 100

while Skill("Magery") < GOAL:
    if Mana("self") < 50:  
        while Mana() < MaxMana("self"):
            if not BuffExists("Active Meditation"):
                UseSkill("Meditation")         
    
    if Skill("Magery") < 45:
        Cast("Bless", "self")    
        Pause(1800)        
    if Skill("Magery") >= 45 and Skill("Magery") < 55:
        Cast("greater heal", "self")    
        Pause(2100)
    if Skill("Magery") >= 55 and Skill("Magery") < 65:        
        Cast("Magic Reflection")        
        Pause(2400)      
    if Skill("Magery") >= 65 and Skill("Magery") < 75:        
        Cast("Invisibility", "Self")        
        Pause(2700)        
    if Skill("Magery") >= 75 and Skill("Magery") < 90:        
        Cast("Mass Dispel", "Self")        
        Pause(3000)    
    if Skill("Magery") >= 90 and Skill("Magery") < 120:        
        Cast("earthquake")   
        Pause(3300)

