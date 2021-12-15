# Name: Set Z
# Description: An example showing sending a custom mobile update packet to the client with a specified Z level
# Author: Reetus
# Era: Any
# Date: Wed Dec 15 2021

from ClassicAssist.UO.Network.Packets import MobileUpdate
from Assistant import Engine

player = Engine.Player

mu = MobileUpdate(player.Serial, player.ID, player.Hue, player.Status, player.X, player.Y, 25, player.Direction)
Engine.SendPacketToClient(mu)