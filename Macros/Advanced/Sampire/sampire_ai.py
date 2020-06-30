# Name: Sampire AI 0.1.2
# Description: Automate Sampire build to cast proper abilities, move, loot and e.t.c
# Author: Mordor
# Era: TOL

from ClassicAssist.UO.Data import Direction
from ClassicAssist.UO import UOMath
import System
from Assistant import Engine
import clr

clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)

WAITING = 500  # Set depending on your ping
HEAL_AT = 90  # HP
ONE_ENEMY_FARM = False  # Set to True if you fight with one type on enemies
PUNCH_RANGE = 1
PLAYER_STUCK_TIMER_MILLISECONDS = 5000


class SpellFn:
    BUSHIDO = Cast
    VIRTUE = InvokeVirtue
    CHIVALRY = Cast
    ATTACK = 'ATTACK'
    CLICKING = 'CLICKING'
    MOVE = 'MOVE'
    CLEAR_TARGET = 'CLEAR_TARGET'
    SECONDARY_ATTACK = 'SECONDARY_ATTACK'


class SpellInfo:
    def __init__(self, name, mana_cost, min_skill, delay_in_ms, priority, when_to_cast, spell_fn, targeting=None):
        self._name = name
        self._mana_cost = mana_cost
        self.min_skill = min_skill
        self._delay_in_ms = delay_in_ms
        self.priority = priority
        self.when_to_cast = when_to_cast
        self._spell_fn = spell_fn
        self._targeting = targeting

    def cast(self, target=None):
        if self._spell_fn == SpellFn.ATTACK:
            attack(target)
        elif self._spell_fn == SpellFn.SECONDARY_ATTACK:
            secondary_ability()
        elif self._spell_fn == SpellFn.CLEAR_TARGET:
            clear_target()
        elif self._spell_fn == SpellFn.CLICKING:
            UseObject(target)
        elif self._spell_fn == SpellFn.MOVE:
            go_to_target(target)
        else:
            self._spell_fn(self._name)
        if self._targeting != None:
            WaitForTarget(WAITING)
            Target(self._targeting)
        Pause(WAITING + self._delay_in_ms)

    def has_mana(self, current_mana):
        return int(self._mana_cost) <= int(current_mana)


class Enemies:
    def __init__(self):
        IgnoreObject("self")
        self.refresh()

    def refresh(self, search_distance=1):
        self._mobiles = self._find_enemies(search_distance)

    def are_amount_eq(self, number):
        return self._mobiles.Count() == number

    def are_amount_more(self, number):
        return self._mobiles.Count() > number

    def boss_here(self):
        for mob in self._mobiles:
            if Enemy(mob).is_boss:
                return True
        return False

    def current_target(self):
        if self.are_amount_eq(0):
            return None

        target = self._mobiles.First().Serial
        if target == GetAlias('self'):
            return None
        else:
            return target

    def _find_enemies(self, distance=1):
        return Engine.Mobiles.Where(lambda m: m != None
                                    and (str(m.Notoriety) == 'Attackable' or str(m.Notoriety) == 'Murderer')
                                    and m.Distance <= distance
                                    and not InIgnoreList(m.Serial)
                                    ).OrderBy(lambda m: m.Distance)


class Enemy:
    def __init__(self, mobile):
        self._mobile = mobile
        self.is_boss = MaxHits(mobile) > 10000

    def is_low_hp(self):
        return Hits(self._mobile) < (MaxHits(self._mobile) * 0.01)

    def is_full_hp(self):
        return DiffHits(self._mobile) == 0


class Sampire_AI:
    def __init__(self, enemies):
        self._enemies = enemies
        self._target = None
        self._query = []
        self.search_distance = 1
        self._rotation = sorted([
            SpellInfo('Confidence', 10, 25, WAITING, 1,
                      self._cast_confidence_heal,
                      SpellFn.BUSHIDO),
            SpellInfo('Close Wounds', 10, 0, 1000, 1,
                      self._cast_heal,
                      SpellFn.CHIVALRY, GetAlias('self')),
            SpellInfo('Honor', 0, 0, WAITING, 2,
                      self._cast_honor,
                      SpellFn.VIRTUE, self._target),
            SpellInfo('Enemy Of One', 20, 45, WAITING, 4,
                      self._cast_enemy_of_one,
                      SpellFn.CHIVALRY),
            SpellInfo('Consecrate Weapon', 10, 15, 1000, 5,
                      self._cast_consecrate_weapon,
                      SpellFn.CHIVALRY),
            SpellInfo('Whirlwind', 30, 90, WAITING, 6,
                      self._cast_whirlwind,
                      SpellFn.SECONDARY_ATTACK),
            SpellInfo('Lightning Strike', 10, 50, WAITING, 6,
                      self._cast_lighting_strike,
                      SpellFn.BUSHIDO),
            SpellInfo('Momentum Strike', 10, 70, WAITING, 6,
                      self._cast_momentum_strike,
                      SpellFn.BUSHIDO),
            SpellInfo('Clicking', 0, 0, WAITING, 98,
                      self._clicking,
                      SpellFn.CLICKING),
            SpellInfo('Attack', 0, 0, WAITING, 3,
                      self._attack,
                      SpellFn.ATTACK),
            SpellInfo('Move', 0, 0, WAITING, 3,
                      self._move,
                      SpellFn.MOVE),
            SpellInfo('Clear Target', 0, 0, WAITING, 0,
                      self._clear_target,
                      SpellFn.CLEAR_TARGET),
        ], key=lambda spell: spell.priority)

    def tick(self):
        self._enemies.refresh(self.search_distance)
        self._target = self._enemies.current_target()
        self._build_query()
        self._run_query()
        self._search_for_enemies()
        Pause(WAITING)

    def _search_for_enemies(self):
        if self._enemies.are_amount_eq(0):
            if self.search_distance < 10:
                self.search_distance += 1
        else:
            self.search_distance = 1

    def _build_query(self):
        self._query = []
        for item in self._rotation:
            if item.when_to_cast():
                self._query.append(item)

    def _run_query(self):
        for item in self._query:
            if not item.has_mana(Mana('self')):
                return

            item.cast(self._target)

    def _clear_target(self):
        return Dead(self._target)

    def _move(self):
        return not InRange(self._target, PUNCH_RANGE)

    def _attack(self):
        return not self._enemies.are_amount_eq(0) and not Dead(self._target)

    def _clicking(self):
        return self._target is not None and not self._enemies.are_amount_eq(0) and Enemy(self._target).is_low_hp()

    def _cast_heal(self):
        return Hits('self') <= HEAL_AT and self._enemies.are_amount_eq(0)

    def _cast_confidence_heal(self):
        return Hits('self') <= HEAL_AT and self._enemies.are_amount_more(0) and not BuffExists('Confidence')

    def _cast_honor(self):
        return self._enemies.are_amount_more(0) and Enemy(self._target).is_full_hp() and not BuffExists('Honored')

    def _cast_enemy_of_one(self):
        return self._target is not None and (ONE_ENEMY_FARM or (self._enemies.are_amount_eq(1) and Enemy(self._target).is_boss)) and not BuffExists('Enemy Of One')

    def _cast_consecrate_weapon(self):
        return not BuffExists('Consecrate Weapon') and not self._enemies.are_amount_eq(0)

    def _cast_lighting_strike(self):
        return self._enemies.are_amount_eq(1) and (not BuffExists('Lightning Strike') or not BuffExists('Momentum Strike'))

    def _cast_momentum_strike(self):
        return self._enemies.are_amount_eq(2) and (not BuffExists('Momentum Strike') or not BuffExists('Lightning Strike'))

    def _cast_whirlwind(self):
        return self._enemies.are_amount_more(2)


# Helper functions


def direction_to(mobile, shift_x=0, shift_y=0):
    mobile = Engine.Mobiles.GetMobile(mobile)

    if mobile == None:
        return Direction.Invalid

    return UOMath.MapDirection(Engine.Player.X, Engine.Player.Y, mobile.X + shift_x, mobile.Y + shift_y)


def fast_run(dir):
    if dir == Direction.Invalid:
        return
    Engine.Move(dir, True)


def go_to_target(mobile, max_distance_to_target=2):
    fast_run(direction_to(mobile))
    Pause(50)

    return True


def attack(target):
    if not War('self'):
        WarMode('on')

    Target(target)
    Attack(target)


def clear_target():
    CancelTarget()
    ClearTargetQueue()


def secondary_ability():
    SetAbility("secondary")


# MAIN function


def main():
    enemies = Enemies()
    sampire_ai = Sampire_AI(enemies)

    while not Dead('self'):
        sampire_ai.tick()


main()
