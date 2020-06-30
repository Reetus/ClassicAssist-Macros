# Name: Discordance training
# Description: Uses the Discordance skill on the player to train Discordance to GM
# Author: Mordor
# Era: Any
from Assistant import Engine
import System
import clr

clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
# Script variables configuration
skill_cap = SkillCap('Discordance')


def train_discordance():
    '''
    Trains Discordance to GM
    '''
    # Script variables
    global skill_cap
    SetTimer('discord_timer', 0)

    instruments = [0x2805, 0x0e9c, 0x0eb3, 0xeb2, 0x0eb1, 0x0e9e, 0x0e9d]

    if Skill('Discordance') == skill_cap:
        MessageBox("Done", 'You\'ve already maxed out Discordance!')
        return

    while not Dead('self') and Skill('Discordance') < skill_cap:
        found_targets = False
        first_target = None
        ClearJournal()

        if Timer('discord_timer') > 1000 * 60 * 5:
            SetTimer('discord_timer', 0)
            ClearIgnoreList()

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

            if first_target != None:
                found_targets = True

        UseSkill('Discordance')

        # Handle the Journal response
        if WaitForJournal('What instrument shall you play?', 500):
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
            if WaitForJournal('That creature is already in discord.', 500) or InJournal('A song of discord would have no effect on that.'):
                IgnoreObject(first_target)
                continue

            Pause(8000)


# Start Discordance training
train_discordance()
