# Name: Animal Taming training
# Description: Tames nearby animals to train Animal Taming to GM (to 90 by default) with healing, killing and basic pathfinding
# Author: Mordor
# Era: Any

from ClassicAssist.UO.Data import Direction
from ClassicAssist.UO import UOMath
import System
from Assistant import Engine
from System.Collections.Generic import List

## Script options ##
# Change to the name that you want to rename the tamed animals to
rename_tamed_animals_to = 'M'
# Add any name of pets to ignore
pets_to_ignore = [
    rename_tamed_animals_to,
]
# Change to the number of followers you'd like to keep.
# The script will auto-kill the most recently tamed animal
# Set to the maximum number of times to attempt to tame a single animal. 0 == attempt until tamed
maximum_tame_attempts = 10
# Set the minimum taming difficulty to use when finding animals to tame
minimum_taming_difficulty = 30
# Set this to how you would like to heal your character if they take damage
# Options are:
# 'Magery' = uses the Heal and Greater Heal ability depending on how much health is missing
# 'None' = do not auto-heal
heal_using = 'Magery'
# True or False to track the animal being tamed
enable_follow_animal = True
# Distance to animal before start
max_distance_to_target = 3
max_search_distance = 30
# Set your skill cap
taming_cap = 90  # SkillCap('Animal Taming')
# Change depending on the latency to your UO shard
journal_entry_delay_milliseconds = 500
player_stuck_timer_milliseconds = 15000
taming_attemp_timer_milliseconds = 20000
need_to_recall = 300000


class Animal:
    def __init__(self, name, mobile_id, color, min_taming_skill, max_taming_skill):
        self.name = name
        self.mobile_id = mobile_id
        self.color = color
        self.min_taming_skill = min_taming_skill
        self.max_taming_skill = max_taming_skill


animals = {
    # Organized based on taming difficulty with no previous owners according to uo.com, then alphabetically by and within species
    # https://uo.com/wiki/ultima-online-wiki/skills/animal-taming/tameable-creatures/#mobs

    ### Min skill 0, Max skill 10 ###
    'dog': Animal('dog', 0x00D9, 0x0000, 0, 10),
    'gorilla': Animal('gorilla', 0x001D, 0x0000, 0, 10),
    'parrot': Animal('parrot', 0x033F, 0x0000, 0, 10),

    # Rabbits
    'rabbit (brown)': Animal('rabbit', 0x00CD, 0x0000, 0, 10),
    'rabbit (black)': Animal('rabbit', 0x00CD, 0x090E, 0, 10),
    'jack rabbit': Animal('jack rabbit', 0x00CD, 0x01BB, 0, 10),

    'skittering hopper': Animal('skittering hopper', 0x012E, 0x0000, 0, 10),
    'squirrel': Animal('squirrel', 0x0116, 0x0000, 0, 10),

    ### Min skill 0, Max skill 20 ###
    'mongbat': Animal('mongbat', 0x0027, 0x0000, 0, 20),

    ### Min skill 10, Max skill 20 ###
    # Birds
    # Note: the following share a color code:
    # 0x0835: Finch, hawk
    # 0x0847: Tern, Towhee
    # 0x0851: Nuthatch, woodpecker
    # 0x0901: Crow, Magpie, raven
    'chickadee': Animal('chickadee', 0x0006, 0x0840, 10, 20),
    'crossbill': Animal('crossbill', 0x0006, 0x083A, 10, 20),
    'crow': Animal('crow', 0x0006, 0x0901, 10, 20),
    'finch': Animal('finch', 0x0006, 0x0835, 10, 20),
    'hawk': Animal('hawk', 0x0006, 0x0835, 10, 20),
    'kingfisher': Animal('kingfisher', 0x0006, 0x083F, 10, 20),
    'lapwing': Animal('lapwing', 0x0006, 0x0837, 10, 20),
    'magpie': Animal('magpie', 0x0006, 0x0901, 10, 20),
    'nuthatch': Animal('nuthatch', 0x0006, 0x0851, 10, 20),
    'plover': Animal('plover', 0x0006, 0x0847, 10, 20),
    'raven': Animal('raven', 0x0006, 0x0901, 10, 20),
    'skylark': Animal('skylark', 0x0006, 0x083C, 10, 20),
    'starling': Animal('starling', 0x083E, 0x0845, 10, 20),
    'swift': Animal('swift', 0x0006, 0x0845, 10, 20),
    'tern': Animal('tern', 0x0006, 0x0847, 10, 20),
    'towhee': Animal('towhee', 0x0006, 0x0847, 10, 20),
    'woodpecker': Animal('woodpecker', 0x0006, 0x0851, 10, 20),
    'wren': Animal('wren', 0x0006, 0x0850, 10, 20),
    'cat': Animal('cat', 0x00C9, 0x0000, 10, 20),
    'chicken': Animal('chicken', 0x00D0, 0x0000, 10, 20),
    'mountain goat': Animal('mountain goat', 0x0058, 0x0000, 10, 20),
    'rat': Animal('rat', 0x00EE, 0x0000, 10, 20),
    'sewer rat': Animal('sewer rat', 0x00EE, 0x0000, 10, 20),

    ### Min skill 20, Max skill 30 ###
    'cow (brown)': Animal('cow', 0x00E7, 0x0000, 20, 30),
    'cow (black)': Animal('cow', 0x00D8, 0x0000, 20, 30),
    'goat': Animal('goat', 0x00D1, 0x0000, 20, 30),
    'pig': Animal('pig', 0x00CB, 0x0000, 20, 30),
    'sheep': Animal('sheep', 0x00CF, 0x0000, 20, 30),

    ### Min skill 20, Max skill 50 ###
    'giant beetle': Animal('giant beetle', 0x0317, 0x0000, 20, 50),
    'slime': Animal('slime', 0x0033, 0x0000, 20, 50),

    ### Min skill 30, Max skill 40 ###
    'eagle': Animal('eagle', 0x0005, 0x0000, 30, 40),
    'bouraRuddy': None,

    ### Min skill 40, Max skill 50 ###
    'boar': Animal('boar', 0x0122, 0x0000, 40, 50),
    'bullfrog': Animal('bullfrog', 0x0051, 0x0000, 40, 50),
    'lowland boura': None,
    'ferret': Animal('ferret', 0x0117, 0x0000, 40, 50),
    'giant rat': Animal('giant rat', 0x00D7, 0x0000, 40, 50),
    'hind': Animal('hind', 0x00ED, 0x0000, 40, 50),

    # Horses
    'horse': Animal('horse', 0x00C8, 0x0000, 40, 50),
    'horse2': Animal('horse', 0x00E2, 0x0000, 40, 50),
    'horse3': Animal('horse', 0x00CC, 0x0000, 40, 50),
    'horse4': Animal('horse', 0x00E4, 0x0000, 40, 50),
    'horsePack': Animal('pack horse', 0x0123, 0x0000, 40, 50),
    'horsePalomino': None,
    'horseWar': None,

    # Llamas
    'pack llama': Animal('pack llama', 0x0124, 0x0000, 40, 50),
    'llamaRideable': None,

    # Ostards
    'ostard': Animal('desert ostard', 0x00D2, 0x0000, 40, 50),
    'forest ostard (green)': Animal('forest ostard', 0x00DB, 0x88A0, 40, 50),
    'forest ostard (red)': Animal('forest ostard', 0x00DB, 0x889D, 40, 50),

    'timber wolf': Animal('timber wolf', 0x00E1, 0x0000, 40, 50),
    'rideable wolf': Animal('rideable wolf', 0x0115, 0x0000, 40, 50),

    ### Min skill 50, Max skill 60 ###
    'black bear': Animal('black bear', 0x00D3, 0x0000, 50, 60),
    'polar bear': Animal('polar bear', 0x00D5, 0x0000, 50, 60),
    'deathwatch beetle': None,
    'llama': Animal('llama', 0x00DC, 0x0000, 50, 60),
    'walrus': Animal('walrus', 0x00DD, 0x0000, 50, 60),

    ### Min skill 60, Max skill 70 ###
    'alligator': Animal('alligator', 0x00CA, 0x0000, 60, 70),
    'brown bear': Animal('brown bear', 0x00A7, 0x0000, 60, 70),
    'high plains boura': None,
    'cougar': Animal('cougar', 0x003F, 0x0000, 60, 70),
    'paralithode': None,
    'scorpion': Animal('scorpion', 0x0030, 0x0000, 60, 70),

    ### Min skill 70, Max skill 80 ###
    'rideable polar bear': Animal('rideable polar bear', 0x00D5, 0x0000, 70, 80),
    'grizzly bear': Animal('grizzly bear', 0x00D4, 0x0000, 70, 80),
    'young dragon': Animal('young dragon', 0x003C, 0x0000, 70, 80),

    'great hart': Animal('great hart', 0xea, 0x0000, 70, 80),

    'snow leopard': Animal('snow leopard', 0x0040, 0x0000, 70, 80),
    'snow leopard2': Animal('snow leopard', 0x0041, 0x0000, 70, 80),
    'panther': Animal('panther', 0x00D6, 0x0000, 70, 80),
    'snake': Animal('snake', 0x0034, 0x0000, 70, 80),
    'giant spider': Animal('giant spider', 0x001C, 0x0000, 70, 80),
    'grey wolf (light grey)': Animal('grey wolf', 0x0019, 0x0000, 70, 80),
    'grey wolf (dark grey)': Animal('grey wolf', 0x001B, 0x0000, 70, 80),

    ### Min skill 80, Max skill 90 ###
    'gaman': None,
    'slithStone': None,
    'white wolf (dark grey)': Animal('white wolf', 0x0022, 0x0000, 80, 90),
    'white wolf (light grey)': Animal('white wolf', 0x0025, 0x0000, 80, 90),

    ### Min skill 90, Max skill 100 ###
    'bull (solid, brown)': Animal('bull', 0x00E8, 0x0000, 90, 100),
    'bull (solid, black)': Animal('bull', 0x00E8, 0x0901, 90, 100),
    'bull (spotted, brown)': Animal('bull', 0x00E9, 0x0000, 90, 100),
    'bull (spotted, black)': Animal('bull', 0x00E9, 0x0901, 90, 100),
    'foxBlood': None,
    'hellcat (small)': Animal('hellcat', 0x00C9, 0x0647, 90, 100),
    'mongbatGreater': None,
    'frenzied ostard': Animal('frenzied ostard', 0x00DA, 0x0000, 90, 100),
    'osseinRam': None,
    'frost spider': Animal('frost spider', 0x0014, 0x0000, 90, 100),
    'giant toad': Animal('giant toad', 0x0050, 0x0000, 90, 100),
    'giant ice worm': Animal('giant ice worm', 0x0050, 0x0000, 90, 100),

    ### Min skill 100, Max skill 110 ###
    # Drakes
    # pathaleo drake: 0x003C
    'drake (brown)': Animal('drake', 0x003C, 0x0000, 100, 110),
    'drake (red)': Animal('drake', 0x003D, 0x0000, 100, 110),
    'drakeCrimson': None,
    'drakePlatinum': None,
    'drakeStygian': None,

    'hellcat (large)': Animal('hellcat', 0x007F, 0x0000, 100, 110),
    'hellhound': Animal('hellhound', 0x0062, 0x0000, 100, 110),
    'imp': Animal('imp', 0x004A, 0x0000, 100, 110),
    'kitsuneBake': None,
    'lava lizard': Animal('lava lizard', 0x00CE, 0x0000, 100, 110),

    # ridgebacks
    'ridgeback': Animal('ridgeback', 0x00BB, 0x0000, 100, 110),
    'savage ridgeback': Animal('savage ridgeback', 0x00BC, 0x0000, 100, 110),

    'slith': None,
    'dire wolf': Animal('dire wolf', 0x0017, 0x0000, 100, 110),

    ### Min skill 110, Max skill 120 ###
    'beetleDeath': None,
    'beetleFire': None,
    'rune beetle': Animal('rune beetle', 0x00F4, 0x0000, 110, 120),
    'dragon': Animal('dragon', 0x003B, 0x0000, 110, 120),
    'dragonSwamp': None,
    'dragonWater': None,
    'dragonDeepWater': None,
    'drakeCold': None,
    'hiryu': None,
    'hiryuLesser': None,
    'lion': None,
    'kiRin': None,
    'nightbear': None,
    'nightdragon': None,
    'nightfrenzy': None,
    'nightmare': None,
    'nightllama': None,
    'nightridge': None,
    'nightwolf': None,
    'skree': None,
    'dread spider': Animal('dread spider', 0x000B, 0x0000, 110, 120),
    'unicorn': None,
    'wolfTsuki': None,
    'white wyrm': Animal('white wyrm', 0x00B4, 0x0000, 110, 120),

    ### Challenging ###
    'cuSidhe': None,
    'dimetrosaur': None,

    # Dragons
    'dragonBane': None,
    'dragonFrost': None,
    'a greater dragon': None,
    'dragonSerpentine': None,
    'gallusaurus': None,

    # Horses
    'steedFire': None,
    'steedSkeletal': None,
    'horseDreadWar': None,

    'miteFrost': None,
    'najasaurus': None,
    'phoenix': None,
    'raptor': None,
    'reptalon': None,
    'saurosurus': None,

    # Tigers
    'tigerWild': None,
    'tigerSabreToothed': None,

    'triceratops': None,
    'turtleHatchlingDragon': None,
    'wolfDragon': None,
    'shadow wyrm': Animal('shadow wyrm', 0x006A, 0x0000, 120, 120)
}


def get_animal_ids_at_or_over_taming_difficulty(minimumTamingDifficulty):
    '''
    Looks through the list of tameables for animals at or over the minimum taming level
    '''
    global animals

    animal_list = List[int]()
    for animal in animals:
        if (not animals[animal] == None and
                not animal_list.Contains(animals[animal].mobile_id) and
                animals[animal].min_taming_skill >= minimumTamingDifficulty):
            animal_list.Add(animals[animal].mobile_id)

    return animal_list


def find_animal_to_tame():
    '''
    Finds the nearest tameable animal nearby
    '''
    global rename_tamed_animals_to
    global minimum_taming_difficulty
    global max_search_distance
    global pets_to_ignore

    import clr

    clr.AddReference("System.Core")
    clr.ImportExtensions(System.Linq)

    animal_ids = get_animal_ids_at_or_over_taming_difficulty(
        minimum_taming_difficulty)

    Pause(50)

    tameable_mobile = Engine.Mobiles.Where(lambda m: m != None
                                           and animal_ids.Contains(m.ID)
                                           and m.Distance <= max_search_distance
                                           and not InIgnoreList(m.Serial)
                                           and not pets_to_ignore.Contains(m.Name)
                                           ).OrderBy(lambda m: m.Distance).FirstOrDefault()

    if tameable_mobile == None:
        return None

    return tameable_mobile.Serial


def direction_to(mobile, shift_x=0, shift_y=0):
    mobile = Engine.Mobiles.GetMobile(mobile)

    if mobile == None:
        return Direction.Invalid

    return UOMath.MapDirection(Engine.Player.X, Engine.Player.Y, mobile.X + shift_x, mobile.Y + shift_y)


def fast_run(dir):
    if dir == Direction.Invalid:
        return
    Engine.Move(dir, True)


def follow_mobile(mobile, max_distance_to_target=2):
    '''
    Uses the X and Y coordinates of the animal and player to follow the animal around the map
    Returns True if player is not stuck, False if player is stuck
    '''

    global player_stuck_timer_milliseconds

    SetTimer('player_stuck_timer', 0)
    stuck_counter = 0

    while not InRange(mobile, max_distance_to_target):
        if stuck_counter > 5:
            return False

        fast_run(direction_to(mobile))
        Pause(50)

        if Timer('player_stuck_timer') > player_stuck_timer_milliseconds:
            stuck_counter += 1
            shift_x = -15
            shift_y = -15
            fast_run(direction_to(mobile, shift_x, shift_y))
            SetTimer('player_stuck_timer', 0)

    return True


def train_animal_taming():
    '''
    Trains Animal Taming to GM
    '''
    # User variables
    global rename_tamed_animals_to
    global maximum_tame_attempts
    global enable_follow_animal
    global journal_entry_delay_milliseconds
    global max_distance_to_target
    global max_search_distance
    global heal_using
    global taming_cap
    global need_to_recall

    if Skill('Animal Taming') == taming_cap:
        MessageBox("Done", 'You\'ve already maxed out Animal Taming!')
        return

    # Initialize variables
    animal_being_tamed = None
    tame_handled = False
    tame_ongoing = False
    times_tried = 0
    current_followers = Followers()

    # Initialize the journal and ignore object list
    ClearJournal()
    ClearIgnoreList()

    # Toggle war mode to make sure the player isn't going to kill the animal being tamed
    if War('self'):
        WarMode('off')

    while not Dead('self') and Skill('Animal Taming') < taming_cap:
        # Cast heal
        if heal_using == 'Magery' and DiffHits('self') > 30:
            Cast('Greater Heal', 'self')
            Pause(1000)
        # If there is no animal being tamed, try to find an animal to tame
        SetTimer('need_to_recall', 0)
        while animal_being_tamed == None:
            animal_being_tamed = find_animal_to_tame()
            Pause(1000)
            if Timer('need_to_recall') > need_to_recall:
                SetTimer('need_to_recall', 0)
                # recall to rune logic
                Pause(100)

        if animal_being_tamed > 0 and not tame_ongoing:
            SetTimer('need_to_recall', 0)
            HeadMsg('Found animal to tame', animal_being_tamed)

        if enable_follow_animal and animal_being_tamed > 0 and Distance(animal_being_tamed) <= max_search_distance:
            stuck = not follow_mobile(
                animal_being_tamed, max_distance_to_target)
            if stuck:
                IgnoreObject(animal_being_tamed)
                animal_being_tamed = None

        elif animal_being_tamed > 0 and Distance(animal_being_tamed) > max_search_distance:
            HeadMsg('Animal moved too far away, ignoring for now',
                    animal_being_tamed)
            animal_being_tamed = None
            continue

        if not maximum_tame_attempts == 0 and times_tried > maximum_tame_attempts:
            HeadMsg('Tried more than %i times to tame. Ignoring animal' %
                    maximum_tame_attempts, animal_being_tamed)
            IgnoreObject(animal_being_tamed)
            animal_being_tamed = None
            times_tried = 0

        # Tame the animal if a tame is not currently being attempted and enough time has passed since last using Animal Taming
        if not tame_ongoing:
            # Clear any previously selected target and the target queue
            CancelTarget()
            ClearTargetQueue()
            ClearJournal()

            # Hey, were finally using the Animal Taming skill! 'bout time!
            UseSkill('Animal Taming')
            WaitForTarget(1000)
            Target(animal_being_tamed)
            Pause(journal_entry_delay_milliseconds)

            # Check if Animal Taming was successfully triggered
            if InJournal('Tame which animal?'):
                times_tried += 1

                # Set tame_ongoing to true to start the journal checks that will handle the result of the taming
                if InJournal('*You start to tame the creature.*'):
                    tame_ongoing = True
                    SetTimer('taming_attemp_timer', 0)

                if InJournal('You have no chance of taming this creature'):
                    # Ignore the object and set to None so that another animal can be found
                    IgnoreObject(animal_being_tamed)

                    ClearJournal()
                    tame_handled = False
                    tame_ongoing = False
                    times_tried = 0
                    animal_being_tamed = None

                if Followers() > current_followers or (not maximum_tame_attempts == 0 and times_tried > maximum_tame_attempts):
                    follow_rename_and_kill(animal_being_tamed)

                    ClearJournal()
                    tame_handled = False
                    tame_ongoing = False
                    times_tried = 0
                    animal_being_tamed = None
                    SetTimer('taming_attemp_timer', 0)

            else:
                continue

        if tame_ongoing:
            Pause(journal_entry_delay_milliseconds)

            if (InJournal('It seems to accept you as master.') or
                InJournal('That wasn\'t even challenging.') or
                    Followers() > current_followers):
                # Animal was successfully tamed
                tame_handled = True
            elif (InJournal('You fail to tame the creature.') or
                    InJournal('You must wait a few moments to use another skill.') or
                    InJournal('That is too far away.') or
                    InJournal('You are too far away to continue taming.') or
                    InJournal('Someone else is already taming this') or
                    InJournal('You have no chance of taming this creature') or
                    InJournal('Target cannot be seen') or
                    InJournal('You can\'t see that.') or
                    InJournal('This animal has had too many owners and is too upset for you to tame.') or
                    InJournal('That animal looks tame already.') or
                    InJournal(
                    'You do not have a clear path to the animal you are taming, and must cease your attempt.') or
                    Timer(
                        'taming_attemp_timer') > taming_attemp_timer_milliseconds
                  ):
                tame_ongoing = False
                SetTimer('taming_attemp_timer', 0)

            if tame_handled:
                follow_rename_and_kill(animal_being_tamed)

                ClearJournal()
                tame_handled = False
                tame_ongoing = False
                times_tried = 0
                animal_being_tamed = None
                SetTimer('taming_attemp_timer', 0)

        # Wait a little bit so that the while loop doesn't consume as much CPU
        Pause(50)


def follow_rename_and_kill(animal_being_tamed):
    Msg('all follow me')
    Pause(1000)
    Rename(animal_being_tamed, rename_tamed_animals_to)
    Pause(1000)
    # Release pet
    WaitForContext(animal_being_tamed, 8, 15000)
    WaitForGump(0x909cc741, 5000)
    ReplyGump(0x909cc741, 2)
    Pause(1000)

    while Mana('self') < 40:
        Pause(1000)

    while Hits(animal_being_tamed) > 0 and Cast('Flame Strike', animal_being_tamed):
        Pause(3000)

    IgnoreObject(animal_being_tamed)


# Start Animal Taming
train_animal_taming()
