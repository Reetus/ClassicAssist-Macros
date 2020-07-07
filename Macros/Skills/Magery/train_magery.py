# Name: Magery training to cap
# Description: Train Magery to cap
# Author: Mordor
# Era: Any

class SpellInfo:
    def __init__(self, name, mana_cost, min_skill, delay_in_ms, target=None):
        self.name = name
        self.mana_cost = mana_cost
        self.min_skill = min_skill
        self.delay_in_ms = delay_in_ms
        self.target = target


# When training, target an inanimate object such as anything on the ground or in your backpack to avoid causing damage.
PromptAlias('spell_target')
magery_cap = SkillCap('Magery')
ping = 800

while not Dead('self') and Skill('Magery') < magery_cap:
    # Set mana and spell cast according to your stats
    spells = [
        SpellInfo('Fireball', 7, 30, 1000, GetAlias('spell_target')),
        SpellInfo('Lightning', 10, 45, 1250, GetAlias('spell_target')),
        SpellInfo('Paralyze', 12, 55, 1500, GetAlias('spell_target')),
        SpellInfo('Invisibility', 18, 65, 1750, GetAlias('self')),
        SpellInfo('Flame Strike', 30, 75, 2000, GetAlias('spell_target')),
        SpellInfo('Earthquake', 40, 90, 2250, GetAlias('spell_target')),
    ]

    current_spell = None

    for spell in spells:
        if spell.min_skill <= Skill('Magery'):
            current_spell = spell

    if Mana('self') > current_spell.mana_cost:
        Cast(current_spell.name, current_spell.target)
        Pause(current_spell.delay_in_ms + ping)
    else:
        while not BuffExists('Active Meditation') or not Mana('self') == MaxMana('self'):
            UseSkill('Meditation')
            Pause(4000)
        while Mana('self') < MaxMana('self'):
            Pause(1000)
