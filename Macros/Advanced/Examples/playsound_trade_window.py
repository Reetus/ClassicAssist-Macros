# Name: Packet wait play sound
# Description: Add a packet wait entry to play a sound when trade window is opened
# Author: Reetus
# Era: Any

from Assistant import Engine
from ClassicAssist.UO.Network.PacketFilter import *
           
pwe = Engine.PacketWaitEntries.Add(PacketFilterInfo(0x6F), PacketDirection.Incoming, True)

pwe.Lock.WaitOne()

while True:
    PlaySound("Bike Horn.wav")
    Pause(1000)
