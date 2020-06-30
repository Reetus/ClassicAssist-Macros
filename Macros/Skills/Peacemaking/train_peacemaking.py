# Name: Peacemaking training
# Description: Uses the Peacemaking skill on the player to train Peacemaking to GM
# Author: Mordor
# Era: Any

# Script variables configuration
peacemaking_timer_milliseconds = 10000
journal_entry_delay_milliseconds = 1000
skill_cap = SkillCap('Peacemaking')


def train_peacemaking():
    '''
    Trains Peacemaking to GM
    '''
    # Script variables
    global peacemaking_timer_milliseconds
    global journal_entry_delay_milliseconds
    global skill_cap

    instruments = [0x2805, 0x0e9c, 0x0eb3, 0xeb2, 0x0eb1, 0x0e9e, 0x0e9d]

    if Skill('Peacemaking') == skill_cap:
        MessageBox("Done", 'You\'ve already maxed out Peacemaking!')
        return

    # Initialize skill timers
    SetTimer('peacemaking_timer', peacemaking_timer_milliseconds)

    # Initialize the journal
    ClearJournal()

    while not Dead('self') and Skill('Peacemaking') < skill_cap:
        if Timer('peacemaking_timer') >= peacemaking_timer_milliseconds:
            # Clean skill timers and jornal
            SetTimer('peacemaking_timer', 0)
            ClearJournal()

            UseSkill('Peacemaking')

            Pause(journal_entry_delay_milliseconds)

            # Handle the Journal response
            if InJournal('What instrument shall you play?'):
                for i in instruments:
                    if FindType(i, -1, "backpack"):
                        break

                if not FindAlias('found'):
                    MessageBox("Error", "No instrument to peacemake with.")
                    return

                WaitForTarget(1000)
                Target('found')

            WaitForTarget(1000)
            Target('self')

            # Wait for the journal entry to come up
            while Timer('peacemaking_timer') < peacemaking_timer_milliseconds:

                if (InJournal('You play hypnotic music, calming your target.', 'regular') or
                    InJournal('You play your hypnotic music, stopping the battle.', 'regular') or
                    InJournal('You attempt to calm everyone, but fail.', 'regular') or
                    InJournal('You play hypnotic music, but there is nothing in range for you to calm.', 'regular') or
                    InJournal('You attempt to calm your target, but fail.', 'regular') or
                    InJournal('You have no chance of calming that creature', 'regular') or
                    InJournal(
                    'You play poorly, and there is no effect.', 'regular')
                    ):
                    # Skill was used successfully, even if the enemy was not successfully put to peace
                    SetTimer('peacemaking_timer',
                             peacemaking_timer_milliseconds)

                Pause(journal_entry_delay_milliseconds)

            ClearJournal()

        # Wait a little bit so that the while loop doesn't consume as much CPU
        Pause(50)


# Start Peacemaking training
train_peacemaking()
