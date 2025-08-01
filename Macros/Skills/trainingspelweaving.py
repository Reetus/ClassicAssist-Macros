# Name: Training Spelweaving
# Description: Insert your goal skill and press play to start training spelweaving
# Author: Lissandro
# Shard: The Crossroads
# Date: Fri Aug 01 2025

#Stand on an Arcane Circle, Pentagram, or Abattoir. Better if you have one in your house to cast AOE spells (essence of wind and wildfire) 
#Make sure you are wearing 40% Lower Mana Cost and as much Mana Regeneration as possible. 
#Lower Reagent Cost is not needed for Spellweaving 
#---- YOU WILL NEED TO HEAL YOURSELF from 90-120 -----
#Equip any melee weapon to cast. Immolating Weapon casts faster than Thunderstorm. Boomstick is what you need       


GOAL = 120

while Skill("Spellweaving") < GOAL:    
    if Mana("self") < 20 and Skill("meditation") > 80:  
        while Mana() < MaxMana("self"):
            if not BuffExists("Active Meditation"):
                UseSkill("Meditation")
                Pause(6000)
    

    if DiffHits("self") > 40:
        Cast("Greater Heal", "Self")
        Pause(3400)
    if Skill("Spellweaving") < 25:
        Cast("arcane circle")            
        Pause(2000)        
    if Skill("Spellweaving") >= 25 and Skill("Spellweaving") < 33:
        Cast("Immolating Weapon")    
        Pause(2100)        
    if Skill("Spellweaving") >= 33 and Skill("Spellweaving") < 52:        
        Cast("Reaper Form")        
        Pause(2400)                
    if Skill("Spellweaving") >= 52 and Skill("Spellweaving") < 74:        
        Cast("Essence of Wind")        
        Pause(3000)    
    if Skill("Spellweaving") >= 74 and Skill("Spellweaving") < 100:        
        Cast("Wildfire", "self")        
        Pause(3000)            
    if Skill("Spellweaving") >= 100 and Skill("Spellweaving") < 120:        
        if DiffHits("self") > 40:
            Cast("Greater Heal", "Self")
            Pause(3400)
        if DiffHits("self") > 40: #Yes, double check
            Cast("Greater Heal", "Self")
            Pause(3400)         
        Cast("Word of Death", "self")   
        Pause(2000)
