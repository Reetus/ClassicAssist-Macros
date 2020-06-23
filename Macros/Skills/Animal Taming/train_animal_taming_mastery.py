# Name: Animal Taming training from 90 to cap
# Description: Uses Animal Taming master ability on target to train Animal Taming from 90 to cap
# Author: Mordor
# Era: Any

while not Dead('self') and Skill('Animal Taming') < SkillCap('Animal Taming'):
    target = 0x5eafbe3  # target for training
    spell_mana_cost = 32  # spell mana cost

    if Mana('self') > spell_mana_cost:
        Cast('Combat Training', target)
        Pause(1000)
    else:
        while not BuffExists('Active Meditation') or Mana('self') == MaxMana('self'):
            UseSkill('Meditation')
            Pause(4000)
        while Mana('self') < MaxMana('self'):
            Pause(1000)
