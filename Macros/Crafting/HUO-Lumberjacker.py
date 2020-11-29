# Name: Lumberjacker 
# Description: Use 2 runic atlas with 48 runes on each, 1 hatchet, full LRC suit
# Author: ziox-b (inspired from "Cray" script)
# Era: UO Heritage

from Assistant import Engine
from ClassicAssist.UO.Commands import UO3DEquipItems
from System import Array

# settings
hand = 'TwoHanded'
axes = [0x0f43,0x1443]
logs = [0x1bdd,0x07da,0x04a7,0x04a8,0x04a9,0x04aa,0x047f] # colors
to_cont = [0x1bdd,0x1bd7,0x1bd7,0x2f5f,0x318f,0x3190,0x3191,0x3199,0x5738] # dump
cont_serial = 0x40159b2d # add your container serial to drop stuff
runebook1 = 0x400b631d # home rune must be the first one in this runic atlas
runebook2 = 0x4003a799 
runes = range(1, 48)
# end settings

def recall(runebook,r):
    ClearJournal()
    while Mana('self') < 10:
    	Pause(100)
    x = X('self')
    y = Y('self')
    rune_button = r + 100
    rune_recall = 4
    atlas_shit = r / 16
    UseObject(runebook)
    for i in range(atlas_shit):
        WaitForGump(0x1f2, 5000)
        ReplyGump(0x1f2, 1150)
    WaitForGump(0x1f2, 5000)
    ReplyGump(0x1f2, rune_button)
    WaitForGump(0x1f2, 5000)
    ReplyGump(0x1f2, rune_recall)
    while X('self') == x and Y('self') == y:
    	if InJournal("blocking", "system"):
    		recall(runebook,r)
        Pause(500)
    Pause(500)

def cut_logs():
	for log in logs:
		while FindType(log, -1, 'backpack'):
			Pause(500)
			UseLayer(hand)
			WaitForTarget(5000)
			Target('found')
			Pause(1000)

def	drop_to_home():
	if Weight() <= MaxWeight() - 200:
		Pause(100)
		return
	recall(runebook1,0)
	for items in to_cont:
		while FindType(items, -1, 'backpack'):
			MoveItem('found', cont_serial)
			Pause(1000)

def lumber(runebook):
	if InJournal("blocking", "system"):
		recall(runebook, r)
		lumber(runebook)
	if FindLayer(hand):
		SysMessage('axe in hand')
		return
	for axe in axes:
		if FindType(axe, -1, 'backpack'):
			UO3DEquipItems(Array[int]([GetAlias('found')]))
			Pause(750)
	ClearJournal()
	SetTimer("lumber", 8000)
	while Weight() <= MaxWeight():
		if not TimerExists("lumber"):
			break
		if InJournal("not enough", "system"):
			break
		CancelTarget()
		Pause(100)
		SetAlias('hatchet',0x40159b2a)
		TargetByResource('hatchet', 'Wood')
		Pause(1000)

while not Dead('self'):
	for r in runes:
		cut_logs()
		drop_to_home()
		recall(runebook1, r)
		lumber(runebook1)
	for r in runes:
		cut_logs()
		drop_to_home()
		recall(runebook2, r)
		lumber(runebook2)
	Pause(100)
