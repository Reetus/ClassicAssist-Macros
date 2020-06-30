# Name: Provocation training
# Description: Uses the Provocation skill on the player to train Provocation to GM
# Author: Mordor
# Era: Any
from Assistant import Engine
import System
import clr

clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
# Script variables configuration
skill_cap = SkillCap('Provocation')


def train_provocation():
    '''
    Trains Provocation to GM
    '''
    # Script variables
    global skill_cap

    instruments = [0x2805, 0x0e9c, 0x0eb3, 0xeb2, 0x0eb1, 0x0e9e, 0x0e9d]

    if Skill('Provocation') == skill_cap:
        MessageBox("Done", 'You\'ve already maxed out Peacemaking!')
        return

    while not Dead('self') and Skill('Provocation') < skill_cap:
        found_targets = False
        first_target = None
        second_target = None
        ClearJournal()

        if DiffHits("self") > 2:
            UseSkill('Peacemaking')
            WaitForTarget(1000)
            Target('self')

        while not found_targets:
            enemies = Engine.Mobiles.Where(lambda m: m != None
                                           and m.Serial != GetAlias('self')
                                           and m.Distance <= 10
                                           and not InIgnoreList(m.Serial)
                                           ).OrderBy(lambda m: m.Distance)
            first_target = enemies.FirstOrDefault()
            second_target = enemies.Skip(1).FirstOrDefault()

            if first_target != None and second_target != None and first_target != second_target:
                found_targets = True

        UseSkill('Provocation')

        # Handle the Journal response
        if WaitForJournal('What instrument shall you play the music on?', 500):
            UnsetAlias('found')
            for i in instruments:
                if FindType(i, -1, "backpack"):
                    break

            if not FindAlias('found'):
                MessageBox("Error", "No instrument to playing with.")
                return

            WaitForTarget(2000)
            Target('found')

        WaitForTarget(5000)
        if TargetExists():
            Target(first_target)
            if InJournal('You can\'t incite that!') or InJournal('You cannot perform negative acts on your target.'):
                IgnoreObject(first_target)
                continue
            WaitForTarget(5000)
            if TargetExists():
                Target(second_target)
                if InJournal('You can\'t incite that!') or InJournal('You cannot perform negative acts on your target.'):
                    IgnoreObject(second_target)
                    continue
                Pause(8000)


# Start Provocation training
train_provocation()
