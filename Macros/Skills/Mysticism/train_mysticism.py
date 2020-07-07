# Name: Mysticism training to cap
# Description: Train Mysticism to cap
# Author: Mordor
# Era: TOL

class SpellInfo:
    def __init__(self, name, mana_cost, min_skill, delay_in_ms, target=None):
        self.name = name
        self.mana_cost = mana_cost
        self.min_skill = min_skill
        self.delay_in_ms = delay_in_ms
        self.target = target


while not Dead('self') and Skill('Mysticism') < SkillCap('Mysticism'):
    # Set mana and spell cast according to your stats
    spells = [
        SpellInfo('Stone Form', 8, 40, 1500),
        SpellInfo('Cleansing Winds', 12, 63, 3000, GetAlias('self')),
        SpellInfo('Hail Storm', 30, 80, 4000, GetAlias('self')),
        SpellInfo('Nether Cyclone', 30, 95, 4000),
    ]

    current_spell = None

    for spell in spells:
        if spell.min_skill <= Skill('Mysticism'):
            current_spell = spell

    if Mana('self') > current_spell.mana_cost:
        Cast(current_spell.name, current_spell.target)
        Pause(current_spell.delay_in_ms)
    else:
        while not BuffExists('Active Meditation') or not Mana('self') == MaxMana('self'):
            UseSkill('Meditation')
            Pause(4000)
        while Mana('self') < MaxMana('self'):
            Pause(1000)
