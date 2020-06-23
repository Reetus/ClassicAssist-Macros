# Name: Faster Run
# Description: Run without waiting for movement accepted packets to speed up movement
# Author: Reetus
# Era: Any

from Assistant import Engine
from ClassicAssist.UO import UOMath
from ClassicAssist.UO.Data import Direction

def DirectionTo(alias):
    mobile = Engine.Mobiles.GetMobile(GetAlias(alias))
    
    if mobile == None:
        return Direction.Invalid

    return UOMath.MapDirection( Engine.Player.X, Engine.Player.Y, mobile.X, mobile.Y )
    
def FRun(dir):
    if dir == Direction.Invalid:
        return
    Engine.Move(dir, True)    
    
while Distance('enemy') > 1:    
    FRun(DirectionTo('enemy'))
    Pause(100)