# Name: Bandage Dual & Solo Pets
# Description: Auto bandage pets
# Author:  qk
# Era: Any
# Date: Mon Feb 01 2021

#// create pet list if not exist
RemoveList("petlist")
if not ListExists("petlist"):
	CreateList("petlist")
	#// add an entry for each pet you hunt with:
	PushList("petlist", 0x000001)  #// Meta
	PushList("petlist", 0x000001) #// Meta
	PushList("petlist", 0x000001)  #// Spider
	PushList("petlist", 0x000001) #// Spider

#// removes pets if mounted, stabled or you get too far away
if not FindAlias("pet1") or not FindObject("pet1", 30):
	UnsetAlias("pet1")
	HeadMsg("Cleared Pet1", "self", 33)
#if FindAlias("pet2") or not FindObject("pet2", 30):
#	UnsetAlias("pet2")
#	HeadMsg("Cleared Pet2", "self", 33)
	
#// makes sure the pets never equal each other
if FindAlias("pet1") and FindAlias("pet2"):
	if GetAlias("pet1") == GetAlias("pet2"):
		UnsetAlias("pet2")
    	
#// search pets
for i in GetList("petlist"): 
	if FindObject(i, 30):
		#if not FindObject("pet1"):
		#SysMessage("SetAlias pet1 " + hex(i))
			#SetAlias("pet1", i)
		SetAlias("pet1", i)
			
for i in GetList("petlist"): 
	SetAlias("petTemp", i)
	if (FindObject(i, 30) and GetAlias("petTemp") != GetAlias("pet1")):
		#if not FindObject("pet2"):
		#SysMessage("SetAlias pet2 " + hex(i))
			#SetAlias("pet2", i)
		SetAlias("pet2", i)	
				
#// clear target queue
#ClearTargetQueue()
#// clear journal
#ClearJournal()

#// check if player dead
if Dead("self"):
	Stop()
	
if not FindType(0xe21, -1, "backpack"):
	HeadMsg("Out of Bandages", "self", 33)
	Stop()

#// bandage timer
if not TimerExists("VetBandage"):
	CreateTimer("VetBandage")
	
#// Select timer timeout
if not TimerExists("SelectTimer"):
	CreateTimer("SelectTimer")
	
if not FindAlias("pet1"):
	HeadMsg("Select First Pet", "self", 33)
	PromptAlias("pet1")
	SetTimer("SelectTimer", 0)
	while WaitingForTarget() and Timer("SelectTimer") < 9999:
		Pause(100)
		
	if ((GetAlias("pet1") == GetAlias("self")) or (GetAlias("pet1") == False)):
		UnsetAlias("pet1")
		HeadMsg("No Valid Target", "self", 33)
		Stop()
	
if not GetAlias("pet2") == 0x40000001 and not FindAlias("pet2") :
	HeadMsg("Select Second Pet", "self", 33)
	PromptAlias("pet2")
	SetTimer("SelectTimer", 0)
	while WaitingForTarget() and Timer("SelectTimer") < 9999:
		Pause(100)
		
	if ((GetAlias("pet2") == GetAlias("self")) or (GetAlias("pet2") == False)):
		#UnsetAlias("pet2")
		HeadMsg("No Valid Target", "self", 33)
		SetAlias("pet2", 0x40000001) # solo pet
	
#if not FindAlias("pet1") or not FindAlias("pet2"):
#	HeadMsg("No Pets Found", "self", 33)
#	Stop()
	
if not FindObject(GetAlias("pet1")):
	HeadMsg("No Pet1 Found", "self", 33)
	Stop()
	
if GetAlias("pet2") == True and not FindObject(GetAlias("pet2")):
	HeadMsg("No Pet2 Found", "self", 33)
	Stop()

##// Bless self if overweight
#if ( Hits("pet1") == MaxHits("pet1") and Hits("pet2") == MaxHits("pet2") ) and ( Weight() > 390 ) and not ( BuffExists("Bless") ):
#	CancelTarget()
#	Cast("Bless", "self")
#	WaitForTarget(2000)
#	Target("self")

if (GetAlias("pet2") == 0x40000001):
	#// Bandage Solo Pet
	if Hits("pet1") > ( MaxHits("pet1") - 5 ):
		#HeadMsg("Full Healed - Stop", "self", 33)
		Stop()
		
	if InRange("pet1", 1) and Timer("VetBandage") >= 6100:
		if not InRange("pet1", 2): #and Timer("VetBandage") >= 6100:
			HeadMsg("Get Closer 1", "self", 33)
			#Stop()
			Pause(500)
		else:
			if Hits("pet1") < ( MaxHits("pet1") - 1 ):
				CancelTarget()
				UseType(0xe21, -1, "backpack")
				WaitForTarget(2000)
				Target("pet1")
				SetTimer("VetBandage", 0)
				#HeadMsg("Heal Start Pet1", "self", 80)
				HeadMsg("Healing " + Name("pet1"), "self", 33)
				PlayMacro("Client Timer Pet Bandage")
			else:
				Stop()
else:
	#// Bandage Dual Pets
	if Hits("pet1") > ( MaxHits("pet1") - 5 ) and Hits("pet2") > ( MaxHits("pet2") - 5 ):
		#HeadMsg("Full Healed - Stop", "self", 33)
		Stop()
	
	if Hits("pet1") != MaxHits("pet1") or Hits("pet2") != MaxHits("pet2"):
		#// Bandage Pet1
		if DiffHits("pet1") > DiffHits("pet2"):
			if not InRange("pet1", 2): #and Timer("VetBandage") >= 6100:
				HeadMsg("Get Closer 1", "self", 33)
				Pause(500)
			else:
				if Hits("pet1") < ( MaxHits("pet1") - 1 ):
					CancelTarget()
					UseType(0xe21, -1, "backpack")
					WaitForTarget(2000)
					Target("pet1")
					SetTimer("VetBandage", 0)
					HeadMsg("Healing " + Name("pet1"), "self", 33)
					PlayMacro("Client Timer Pet Bandage")
		else:
		#// Bandage Pet2
			if not InRange("pet2", 2): #and Timer("VetBandage") >= 6100:
				HeadMsg("Get Closer 2", "self", 33)
				Pause(500)
			else:
				if Hits("pet2") < ( MaxHits("pet2") - 1 ):
					CancelTarget()
					UseType(0xe21, -1, "backpack")
					WaitForTarget(2000)
					Target("pet2")
					SetTimer("VetBandage", 0)
					HeadMsg("Healing " + Name("pet2"), "self", 33)
					PlayMacro("Client Timer Pet Bandage")
				
#// Ress Pet
if GumpExists(0x4da72c0) and InGump(0x4da72c0, "Wilt thou sanctify the resurrection of"):
	ReplyGump(0x4da72c0, 1)
	HeadMsg("Pet Ressed", "self", 60)
	Pause(50)
	HeadMsg("Pet Ressed", "self", 70)
	Pause(50)
	HeadMsg("Pet Ressed", "self", 80)
	Pause(50)
	
#// Auto Protection Self
if not TimerExists("Protect"):
	CreateTimer("Protect")
	SetTimer("Protect", 250000)

if Timer("Protect") >= 250000:
	Cast("Protection", "self")
	SetTimer("Protect", 0)

#// Auto Bless Self
#if not BuffExists("Bless") and Timer("VetBandage") <= 6100:
#	CancelTarget()
#	Cast("Bless", "self")
#	#WaitForTarget(5000)
#    #WaitForTargetOrFizzle(5000):
    
ClearJournal()
if Timer("VetBandage") <= 6100:
	while Timer("VetBandage") <= 6100:
		if InJournal("finish applying the bandage", "system"):
			HeadMsg("Heal Complete", "self", 88)
			break
		if InJournal("too far away", "system"):
			HeadMsg("Too Far Away", "self", 33)
			break
		if InJournal("stay close enough", "system"):
			HeadMsg("Stay Close", "self", 33)
			break
		if InJournal("you are able to resurrect", "system"):
			HeadMsg("Ress Detected", "self", 33)
			break
		if InJournal("you fail to resurrect", "system"):
			HeadMsg("Ress Fail", "self", 33)
			break
			
SetTimer("VetBandage", 9999)
