# Name: Evaluating Intelligence training to cap
# Description: Uses Reactive Armor to train Evaluating Intelligence to the cap
# Author: Mordor
# Era: Any

while not Dead('self') and Skill('Evaluating Intelligence') < SkillCap('Evaluating Intelligence'):
    if Mana('self') > 20:
        Cast('Reactive Armor')
        Pause(1000)
    else:
        while not BuffExists('Active Meditation') or not Mana('self') == MaxMana('self'):
            UseSkill('Meditation')
            Pause(4000)
        while Mana('self') < MaxMana('self'):
            Pause(1000)
