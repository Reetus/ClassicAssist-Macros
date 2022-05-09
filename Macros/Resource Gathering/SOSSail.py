# Name: SOS Sail
# Description: Sail to SOS Coordiate, in Felucca and Trammel
#				Sail use A* with 16 x 16 Tile but not perfect
#				Hunt monster with magery
# Author: ad960009
# Era: AOS

from Assistant import Engine
from ClassicAssist.UO.Data import MapInfo
from ClassicAssist.UO.Data import Map
import System
import clr
import re
from time import time
clr.AddReference("System.Core")
clr.AddReference('PresentationFramework')
clr.AddReference('PresentationCore')
clr.AddReference('WindowsBase')
clr.ImportExtensions(System.Linq)
from System import Uri, TimeSpan, Enum
from System.Windows import Window, ResourceDictionary
from System.Windows.Markup import XamlReader
from System.Threading import Thread, ThreadStart, ApartmentState
from System import Array, Byte
from System.Windows.Media import PixelFormats
from System.Windows.Media.Imaging import BitmapSource
from System.Windows.Threading import DispatcherTimer

SetQuietMode(True)

global SOSType
global PoleType
global MonsterTypes
global SOSContainerTypes

SOSType = 0x14EE
PoleType = 0x0DC0
MonsterTypes = [0x96,0x10,0x4D,0x97,]
SOSChestTypes = [0xE43, 0xE41, 0xA30A]

global North
global South
global East
global West
West = [0x3E93,0x90E9]
East = [0x3E65,0x91F7]
South = [0x3EB9,0x944C]
North = [0x3EAE,0x9170]

global width
global height
width = 320
height = 256

global SOSGumpID
SOSGumpID = 0x550a461b

global sosReg
sosReg = re.compile("([0-9]+)o ([0-9]+)'([N|S]), ([0-9]+)o ([0-9]+)'([W|E])")

global felTile
global traTile

global SuccessMessage
SuccessMessage = ["You pull out", "odd tangled", "Your fishing pole", "but fail to catch", "You pull up", "it into your back"]

global ShipKeyTypes
RuneTypes = [0x1F14,0x100F]
global ShipRuneNames
ShipRuneNames = ["Ship Recall Rune", "a ship key"]


xaml ="""
	<StackPanel Orientation="Horizontal"
	xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
	  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
	>
		<Image
			VerticalAlignment="Top"
			Name="map"
			Width="320"
			Height="256" />
		<DockPanel LastChildFill="True">
			<StackPanel DockPanel.Dock="Top">
				<Button Content="Load SOS from all container" Name="LoadAll"/>
				<Button Content="Load SOS from backpack" Name="LoadBackpack"/>
				<Button Content="Move SOS to backpack" Name="MoveSOS"/>
				<ComboBox HorizontalAlignment="Stretch" HorizontalContentAlignment="Center" Name="MoveCount">
					<ComboBoxItem Content="10" HorizontalAlignment="Center" />
					<ComboBoxItem Content="20" HorizontalAlignment="Center" />
					<ComboBoxItem Content="30" HorizontalAlignment="Center" />
					<ComboBoxItem Content="40" HorizontalAlignment="Center" />
					<ComboBoxItem Content="50" Selector.IsSelected="True" HorizontalAlignment="Center" />
				</ComboBox>
				<Button Content="Goto ship" Name="Recall"/>
				<Button Content="Recalc route" Name="Recalc"/>
				<Button Content="Sail to next SOS" Name="MoveNext"/>
				<Button Content="Stop sail" Name="StopSail"/>
				<CheckBox Name="CheckFishing" Content="Fishing when arrived" IsChecked="True" />
				<!--<Button Content="Debug" Name="DebugButton" Visibility="Collapsed" />-->
				<Button Content="Debug" Name="DebugButton" />
			</StackPanel>
			<TextBlock Name="MsgBox" Background="White" />
		</DockPanel>
	</StackPanel>
"""

class SOS:
	def __init__(self, x, y, serial, owner):
		self.X = x
		self.Y = y
		self.Serial = serial
		self.Owner = owner
		self.MapX = x / 16
		self.MapY = y / 16

class Tile:
	def __init__(self, x, y, parent = None, cost = 0):
		self.X = x
		self.Y = y
		self.Cost = cost
		self.Parent = parent
		self.Distance = 0
	def SetDistance(self, targetX, targetY):
		self.Distance = (self.X - targetX) ** 2 + (self.Y - targetY) ** 2
		self.CostDistance = self.Cost + self.Distance

def Recall(target):
	Cast("Recall")
	if WaitForTargetOrFizzle(5000):
		Target(target)
		fcr = FasterCastRecovery()
		Pause((6 - fcr) / 4 * 1000)
		return True
	return False

def KillMonsterWithMagery():
	find = False
	for mob in MonsterTypes:
		if FindType(mob, 10):
			find = True
			fcr = FasterCastRecovery()
			if Cast("Lightning", "found"):
				Pause((6 - fcr) / 4 * 1000)
		if DiffHits() > 50:
			fcr = FasterCastRecovery()
			if Poisoned("self"):
				Cast("Cure", "self")
			else:
				Cast("Heal", "self")
			Pause((6 - fcr) / 4 * 1000)
	return find

def KillMonster():
	if Skill("magery") > 80:
		return KillMonsterWithMagery()
	else:
		pass
	return False

def FindShip():
	if Engine.Player.Map != Map.Felucca and Engine.Player.Map != Map.Trammel:
		return None
	mapTile = GetPlayerFacetTile()
	if mapTile[X("self") / 16][Y("self") / 16] == 0:
		return None
	Resync()		
	for i in North:
		if FindType(i):
			return North

	for i in South:
		if FindType(i):
			return South

	for i in East:
		if FindType(i):
			return East

	for i in West:
		if FindType(i):
			return West
	return None

def GetWalkableTiles(map, currentTile, targetTile):
	possibleTiles = [
		Tile(currentTile.X - 1, currentTile.Y - 1, currentTile, currentTile.Cost + 1),
		Tile(currentTile.X - 1, currentTile.Y, currentTile, currentTile.Cost + 1),
		Tile(currentTile.X - 1, currentTile.Y + 1, currentTile, currentTile.Cost + 1),
		Tile(currentTile.X + 1, currentTile.Y - 1, currentTile, currentTile.Cost + 1),
		Tile(currentTile.X + 1, currentTile.Y, currentTile, currentTile.Cost + 1),
		Tile(currentTile.X + 1, currentTile.Y + 1, currentTile, currentTile.Cost + 1),
		Tile(currentTile.X, currentTile.Y - 1, currentTile, currentTile.Cost + 1),
		Tile(currentTile.X, currentTile.Y + 1, currentTile, currentTile.Cost + 1),
	]

	ret = []
	
	for possibleTile in possibleTiles:
		if possibleTile.X >= 0 and possibleTile.Y >= 0 and possibleTile.X < width and possibleTile.Y < height and map[possibleTile.X][possibleTile.Y] == 1:
			possibleTile.SetDistance(targetTile.X, targetTile.Y)
			ret.append(possibleTile)
	return ret
	
def SearchRoute(map, start, end):
	print("start SearchRoute")
	timeStart = time()
	if start[0] < 0 or width - 1 < start[0] or start[1] < 0 or height - 1 < start[1]:
		print("start position Error ({}, {})".format(start[0], start[1]))
		return None
	if end[0] < 0 or width - 1 < end[0] or end[1] < 0 or height - 1 < end[1]:
		print("start position Error ({}, {})".format(end[0], end[1]))
		return None
	if map[start[0]][start[1]] != 1 or map[end[0]][end[1]] != 1:
		print("start position Error ({}, {})".format(start[0], start[1]))
		print("end position Error ({}, {})".format(end[0], end[1]))
		print("failed SearchRoute start({}) end({})".format(map[start[0]][start[1]], map[end[0]][end[1]]))
		return None
	startTile = Tile(start[0], start[1])
	endTile = Tile(end[0], end[1])
	
	startTile.SetDistance(end[0], end[1])
	
	activeTiles = []
	visitedTiles = []
	activeTiles.append(startTile)
	
	while activeTiles:
		checkTile = activeTiles[0]
		for tile in activeTiles:
			if tile.CostDistance < checkTile.CostDistance:
				checkTile = tile
		#checkTile = activeTiles.OrderBy(lambda x: x.GetCostDistance()).First()
		
		if checkTile.X == end[0] and checkTile.Y == end[1]:
			ret = []
			rail = checkTile
			while rail != None:
				ret.append((rail.X * 16 + 8, rail.Y * 16 + 8))
				rail = rail.Parent
			timeEnd = time()
			print("end SearchRoute :" + str(timeEnd - timeStart))
			return ret[::-1]

		visitedTiles.append(checkTile)
		activeTiles.remove(checkTile)

		walkAbleTiles = GetWalkableTiles(map, checkTile, endTile)
		for walkTile in walkAbleTiles:
			find = False
			for visitedTile in visitedTiles:
				if walkTile.X == visitedTile.X and walkTile.Y == visitedTile.Y:
					find = True
					break
			if find:
				continue

			#if visitedTiles.Any(lambda x: x.X == walkTile.X and x.Y == walkTile.Y):
			#	continue

			existingTile = None
			for activeTile in activeTiles:
				if walkTile.X == activeTile.X and walkTile.Y == activeTile.Y:
					existingTile = activeTile
					break

			#existingTile = activeTiles.FirstOrDefault(lambda x: x.X == walkTile.X and x.Y == walkTile.Y)

			if existingTile == None:
				activeTiles.append(walkTile)
				continue
			if existingTile.CostDistance > checkTile.CostDistance:
				activeTiles.append(walkTile)
				activeTiles.remove(existingTile)
	print("failed SearchRoute")
	return None

def ParseSOS(sos):
	UseObject(sos.Serial)
	while not WaitForGump(SOSGumpID, 5000):
		UseObject(sos.Serial)
		Pause(100)
	x = None
	y = None
	(find, sosGump) = Engine.Gumps.GetGump(SOSGumpID)
	if find:
		sosCoord = sosGump.GumpElements[1].Args
		m = sosReg.search(sosCoord)
		xLong = int(m.group(4))
		xMins = int(m.group(5))
		xEast = m.group(6) == "E"
		yLat = int(m.group(1))
		yMins = int(m.group(2))
		ySouth = m.group(3) == "S"
	
		xCenter = 1323
		yCenter = 1624
		xWidth = 5120
		yHeight = 4096
		absLong = xLong + xMins / 60
		absLat = yLat + yMins / 60
		if not xEast:
			absLong = 360 - absLong
		if not ySouth:
			absLat = 360 - absLat
		
		x = xCenter + absLong * xWidth / 360
		y = yCenter + absLat * yHeight / 360
	
		if x < 0:
			x += xWidth
		if y < 0:
			y += yHeight
		if x > xWidth:
			x -= xWidth
		if y > yHeight:
			y -= yHeight
		
		while GumpExists(SOSGumpID):
			ReplyGump(SOSGumpID, 0)
			Pause(100)
		print("Parse SOS: {} -> ({}, {})".format(sosCoord, x, y))
		return (x, y)
	print("Parse SOS failed")
	return None

def FindSOS(window, container):
	if container == None:
		soses = Engine.Items.SelectEntities(lambda i: i.ID == SOSType)
	else:
		soses = Engine.Items.SelectEntities(lambda i: i.ID == SOSType and i.Owner == container)
	if soses == None:
		return
	print("SOS Count: {0}".format(len(soses)))
	window.MsgBoxUpdate("SOS Count: {0}".format(len(soses)))
	backpack = GetAlias("backpack")
	for sos in soses:
		sosItem = Engine.Items.GetItem(sos.Serial)
		if sosItem.Owner != backpack:
			container = sos.Owner
			while FindObject(sos.Serial, -1, container):
				MoveItem(sos.Serial, "backpack")
				Pause(600)
			sosCoord = ParseSOS(sos)
			if sosCoord != None:
				window.SOSList.append(SOS(sosCoord[0], sosCoord[1], sos.Serial, sos.Owner))
				print("SOS Count: {0}".format(len(window.SOSList)))
			while FindObject(sos.Serial, -1, "backpack"):
				MoveItem(sos.Serial, container)
				Pause(600)
		else:
			sosCoord = ParseSOS(sos)
			if sosCoord != None:
				sosInfo = SOS(sosCoord[0], sosCoord[1], sos.Serial, "backpack")
				window.SOSList.append(sosInfo)
				#window.BackpackSOSList.append(sosInfo)
				print("SOS Count: {0}".format(len(window.SOSList)))
	return

def GetMapData(map):
	tiles = [[0 for x in range(height)] for y in range(width)]

	for y in range(height):
		for x in range(width):
			tile = MapInfo.GetLandTile(map, x * 16 + 8, y * 16 + 8)
			if (tile.Name == "water"):
				tiles[x][y] = 1
	return tiles

def GetPlayerFacetTile():
	if Engine.Player.Map == Map.Felucca:
		return felTile
	else:
		return traTile

class XamlWindow(Window):
	def __init__(self):
		rd = ResourceDictionary()
		rd.Source = Uri("pack://application:,,,/ClassicAssist.Shared;component/Resources/DarkTheme.xaml")
		self.Resources.MergedDictionaries.Add(rd)
		self.Background = self.Resources["ThemeWindowBackgroundBrush"]
		
		self.Content = XamlReader.Parse(xaml)
		self.Title = "SOS Sail ad960009 in Margo"
		self.Width = 500
		self.Height = 300
		self.refreshTime = TimeSpan.FromSeconds(1)
		self.SOSList = []
		#self.BackpackSOSList = []
		
		self.events = [
			("LoadAll", self.ClickLoadAll),
			("LoadBackpack", self.ClickLoadBackpack),
			("MoveSOS", self.ClickMoveSOS),
			("Recall", self.ClickRecall),
			("Recalc", self.ClickRecalc),
			("MoveNext", self.ClickMoveNext),
			("StopSail", self.ClickStop),
			("DebugButton", self.ClickDebug),
		]
		
		for i in self.events:
			btn = self.Content.FindName(i[0])
			btn.Click += i[1]
		self.map = self.Content.FindName("map")
		self.SOSMoveCount = self.Content.FindName("MoveCount")
		self.CheckFishing = self.Content.FindName("CheckFishing")
		self.timer = DispatcherTimer()
		self.timer.Interval = TimeSpan(0, 0, 1)
		self.timer.Tick += self.tickhandler
		self.timer.Start()
		self.FacetTile = GetPlayerFacetTile()
		
		self.CurrentSOS = None
		self.CurrentRail = []
		self.LastX = None
		self.LastY = None
		self.State = None
		self.SailDir = ""
		
		self.MovingCnt = 0

		return
	
	def Sailing(self, shipDir, currentX, currentY):
		if len(self.CurrentRail) == 0 or ( self.CurrentRail[0][0] == currentX / 16 and self.CurrentRail[0][0] == currentY / 16):
			Msg("Stop")
			self.State = None
			if self.CheckFishing.IsChecked:
				ClearJournal()
				self.State = "Fishing"
			return True
		if shipDir == None:
			self.State = None
			return True

		self.SailDir = ""
		if currentX < self.LastX:
			self.SailDir += "west "
		elif currentX > self.LastX:
			self.SailDir += "east "
		else:
			pass
		if currentY < self.LastY:
			self.SailDir += "north "
		elif currentY > self.LastY:
			self.SailDir += "south "
		else:
			pass

		targetDir = ""
		if abs(self.CurrentRail[0][0] - currentX) > 2:
			if (self.CurrentRail[0][0] < currentX):
				targetDir += "west "
			elif (self.CurrentRail[0][0] > currentX):
				targetDir += "east "
			else:
				pass
		
		if abs(self.CurrentRail[0][1] - currentY) > 2:
			if (self.CurrentRail[0][1] < currentY):
				targetDir += "north "
			elif (self.CurrentRail[0][1] > currentY):
				targetDir += "south "
			else:
				pass
		
		if len(targetDir) == 0:
			self.CurrentRail.pop(0)
			return False
		#print("target {} : sailDir {}".format(targetDir, self.SailDir))
		if targetDir == self.SailDir:
			return
		
		if shipDir == North and not "north" in targetDir:
			if not "south" in targetDir:
				if "west" in targetDir:
					Msg("Turn left")
					return
				if "east" in targetDir:
					Msg("Turn right")
					return
			Msg("Turn around")
			return
		if shipDir == South and not "south" in targetDir:
			if not "north" in targetDir:
				if "west" in targetDir:
					Msg("Turn right")
					return
				if "east" in targetDir:
					Msg("Turn left")
					return
			Msg("Turn around")
			return
		if shipDir == East and not "east" in targetDir:
			if not "west" in targetDir:
				if "north" in targetDir:
					Msg("Turn left")
					return
				if "south" in targetDir:
					Msg("Turn right")
					return
			Msg("Turn around")
			return		
		if shipDir == West and not "west" in targetDir:
			if not "east" in targetDir:
				if "north" in targetDir:
					Msg("Turn right")
					return
				if "south" in targetDir:
					Msg("Turn left")
					return		
			Msg("Turn around")
			return
		
		if shipDir == North:
			if "west" in targetDir:
				Msg("forward left")
			elif "east" in targetDir:
				Msg("forward right")
			else:
				Msg("forward")
			return
		if shipDir == South:
			if "west" in targetDir:
				Msg("forward right")
			elif "east" in targetDir:
				Msg("forward left")
			else:
				Msg("forward")
			return			
		if shipDir == West:
			if "north" in targetDir:
				Msg("forward right")
			elif "south" in targetDir:
				Msg("forward left")
			else:
				Msg("forward")
			return
		if shipDir == East:
			if "north" in targetDir:
				Msg("forward left")
			elif "south" in targetDir:
				Msg("forward right")
			else:
				Msg("forward")
			return
		print("Sail Noop targetDir: {}".format(targetDir))
		return
	def Fishing(self):
		#print("in fishing")
		for chestType in SOSChestTypes:
			if FindType(chestType, 2):
				return False
			if FindType(chestType, 0, "backpack"):
				return False
		
		if not TimerExists("FishingTimer"):
			CreateTimer("FishingTimer")
			SetTimer("FishingTimer", 9000)
		if InJournal("biting here", "system") or InJournal("need to be closer", "system"):
			return False
		if not InJournal("You pull out", "system") and not InJournal("but fail to catch", "system") and Timer("FishingTimer") < 9000:
			return
		ClearJournal()
		for mob in MonsterTypes:
			if FindType(mob, 10):
				print("found mob")
				return

		Pole = None
		if not FindType(PoleType, 0, "self"):
			if not FindType(PoleType, 0, "backpack"):
				Msg("Can't found pole")
				return False
		Pole = GetAlias("found")
		
		UseObject(Pole)
		#print("use Pole")
		if WaitForTarget(5000):
			TargetTileOffsetResource(0, 0, 0)
		SetTimer("FishingTimer", 0)
		return

	def tickhandler(self, sender, args):
		if Engine.Player.Map != Map.Felucca and Engine.Player.Map != Map.Trammel:
			self.CurrentRail = []
			return
		#Resync()
		newTile = GetPlayerFacetTile()
		shipDir = FindShip()

		if shipDir != None:
			if KillMonster():
				self.MovingCnt = 0

		currentX = X("self")
		currentY = Y("self")
		moved = False
		moveCnt = False
		needRedraw = False
		
		if (currentX != self.LastX or currentY != self.LastY):
			moved = True
			needRedraw = True
			self.MovingCnt = 0
		elif self.State == "Sail":
			self.MovingCnt += 1
			if self.MovingCnt > 10:
				self.MsgBoxUpdate("Stopped")
				self.State = None
		if (self.FacetTile != newTile):
			self.FacetTile = newTile
			needRedraw = True

		
		if self.CurrentSOS != None and not FindObject(self.CurrentSOS.Serial, 0, "backpack"):
			self.CurrentSOS = None
		
		if self.State == "Fishing":
			if self.Fishing() == False:
				self.State = None

		elif self.State == "Sail":
			self.Sailing(shipDir, currentX, currentY)	
		else:
			if len(self.SOSList) > 0 and (( moved and shipDir != None ) or len(self.CurrentRail) == 0):
				closedSOS = self.SOSList[0]
				for sosInfo in self.SOSList:
					if sosInfo.Owner != "backpack":
						continue
					if max(abs(closedSOS.X - currentX), abs(closedSOS.Y - currentY)) > max(abs(sosInfo.X - currentX), abs(sosInfo.Y - currentY)):
						closedSOS = sosInfo
				sosChanged = False
				if closedSOS.Owner == "backpack" and self.CurrentSOS != closedSOS:
					self.CurrentSOS = closedSOS
					needRedraw = True
					sosChanged = True
				if len(self.CurrentRail) == 0 or sosChanged:
					self.CurrentRail = SearchRoute(self.FacetTile, ((currentX) / 16, (currentY) / 16), (closedSOS.MapX, closedSOS.MapY))
					if self.CurrentRail == None:
						self.CurrentRail = []
						if self.FacetTile[(currentX) / 16][(currentY) / 16] == 0:
							self.MsgBoxUpdate("Goto deep sea")
						else:
							self.MsgBoxUpdate("can't find route")

		self.LastX = currentX
		self.LastY = currentY
				
		if needRedraw:
			self.UpdateBitmap()
		return
		
	def ButtonDisable(self):
		for i in self.events:
			btn = self.Content.FindName(i[0])
			btn.IsEnabled = False
		return
	def ButtonEnable(self):
		for i in self.events:
			btn = self.Content.FindName(i[0])
			btn.IsEnabled = True		
		return
	def ClickDebug(self, sender, event):
		debugmsg = ""
		debugmsg += "CharXY ({}, {}) : State {}\n".format(X("self"), Y("self"), self.State)
		debugmsg += "ShipDir {}, SailDir {}\n".format(FindShip(), self.SailDir)
		debugmsg += "self.CurrentSOS: {}\n".format(self.CurrentSOS)
		debugmsg += "self.CurrentRail: {}\n".format(len(self.CurrentRail))
		debugmsg += "self.MovingCnt: {}\n".format(self.MovingCnt)
		if len(self.CurrentRail) > 0:
			debugmsg += "self.CurrentRail[0]: ({}, {})\n".format(self.CurrentRail[0][0], self.CurrentRail[0][1])
			debugmsg += "self.CurrentRail[-1]: ({}, {})\n".format(self.CurrentRail[-1][0], self.CurrentRail[-1][1])
		self.MsgBoxUpdate(debugmsg)
		
	def ClickLoadAll(self, sender, event):
		self.ButtonDisable()
		self.SOSList = []
		#self.BackpackSOSList = []
		FindSOS(self, None)
		if FindShip() != None:
			self.LastX = None
		self.UpdateBitmap()
		self.ButtonEnable()
		return
	def ClickLoadBackpack(self, sender, event):
		self.ButtonDisable()
		self.SOSList = []
		#self.BackpackSOSList = []
		FindSOS(self, GetAlias("backpack"))
		if FindShip() != None:
			self.LastX = None
		self.UpdateBitmap()
		self.ButtonEnable()
		return
	def ClickMoveSOS(self, sender, event):
		self.ButtonDisable()
		self.MsgBoxUpdate("Click Map")
		self.map.MouseDown += self.MapMouseDown
		return
	def ClickRecall(self, sender, event):
		rune = None
		ClearIgnoreList()
		for i, runeType in enumerate(RuneTypes):
			while FindType(runeType, 0, "backpack"):
				if Name('found') == ShipRuneNames[i]:
					rune = GetAlias('found')
					break
				else:
					IgnoreObject("found")
			if rune != None:
				break
		ClearIgnoreList()
		if rune == None:
			self.MsgBoxUpdate("Can't find Key or Rune")
			return
		# TODO any other skill's spell
		Cast("Recall")
		if WaitForTarget(5000):
			Target(rune)
			fcr = FasterCastRecovery()
			Pause((6 - fcr) / 4 * 1000)
		else:
			HeadMsg("Target Failed", "self")
		return
	def ClickRecalc(self, sender, event):
		if FindShip() != None:
			self.LastX = None
			self.State = None
			self.CurrentRail = []
		return
	def ClickMoveNext(self, sender, event):
		self.State = "Sail"
		self.MovingCnt = 0
		return
	def ClickStop(self, sender, event):
		self.State = None
		self.MovingCnt = 0
		Msg("Stop")
		return	
	def MapMouseDown(self, sender, event):
		self.MsgBoxUpdate("")
		self.map.MouseDown -= self.MapMouseDown
		clicked = event.GetPosition(self.map)
		print("Click on ({}, {})".format(clicked.X, clicked.Y))
		moveCnt = (self.SOSMoveCount.SelectedIndex + 1 )* 10
		sortedSOS = sorted(self.SOSList, key=lambda sos: max(abs(sos.MapX - clicked.X), abs(sos.MapY - clicked.Y)))
		for i, sosInfo in enumerate(sortedSOS):
			if i == moveCnt:
				break
			print("Move SOS ({}, {}), map({}, {})".format(sosInfo.X, sosInfo.Y, sosInfo.MapX, sosInfo.MapY))
			MoveItem(sosInfo.Serial, "backpack")
			Pause(600)
			sosInfo.Owner = "backpack"
		self.UpdateBitmap()
		self.ButtonEnable()
		return
		
	def MsgBoxUpdate(self, message):
		msgBox = self.Content.FindName("MsgBox")
		msgBox.Text = message
		return
		
	def UpdateBitmap(self):
		#print("start UpdateBitmap SOSList: {0}".format(len(self.SOSList)))
		tiles = self.FacetTile
		pixelFormat = PixelFormats.Bgr24
		bitsPerPixel = 24
		bytesPerPixel = (bitsPerPixel + 7) / 8
		stride = bytesPerPixel * width
		buffer = Array.CreateInstance(Byte, width * height * bytesPerPixel)
		for y in range(height):
			for x in range(width):
				bufferIndex = (y * width + x) * bytesPerPixel
				if tiles[x][y] == 1: #blue
					buffer[bufferIndex + 0] = 255
					buffer[bufferIndex + 1] = 0
					buffer[bufferIndex + 2] = 0
				else: #green
					buffer[bufferIndex + 0] = 0
					buffer[bufferIndex + 1] = 255
					buffer[bufferIndex + 2] = 0

		if len(self.SOSList) > 0:
			for sosInfo in self.SOSList:
				x = sosInfo.MapX
				y = sosInfo.MapY
				xStart = max(x - 1, 0)
				xEnd = min(width - 1, x + 1)
				yStart = max(y - 1, 0)
				yEnd = min(height - 1, y + 1)
				for yi in range(yStart, yEnd):
					for xi in range(xStart, xEnd):
						bufferIndex = (yi * width + xi) * bytesPerPixel
						if sosInfo.Owner == "backpack": #backpack red
							buffer[bufferIndex + 0] = 0
							buffer[bufferIndex + 1] = 0
							buffer[bufferIndex + 2] = 255
						else: #other yellow
							buffer[bufferIndex + 0] = 0
							buffer[bufferIndex + 1] = 255
							buffer[bufferIndex + 2] = 255
		
		if self.CurrentRail != None and len(self.CurrentRail) > 0:
			for rail in self.CurrentRail: # route white
				bufferIndex = (rail[1] / 16 * width + rail[0] / 16) * bytesPerPixel
				buffer[bufferIndex + 0] = 255
				buffer[bufferIndex + 1] = 255
				buffer[bufferIndex + 2] = 255

		if self.CurrentSOS != None:
			x = self.CurrentSOS.MapX
			y = self.CurrentSOS.MapY
			
			for i in range(height):
				bufferIndex = (i * width + x) * bytesPerPixel
				buffer[bufferIndex + 0] = 0
				buffer[bufferIndex + 1] = 255
				buffer[bufferIndex + 2] = 255
				
			for i in range(width):
				bufferIndex = (y * width + i) * bytesPerPixel
				buffer[bufferIndex + 0] = 0
				buffer[bufferIndex + 1] = 255
				buffer[bufferIndex + 2] = 255
			
		if self.LastX != None and self.LastY != None:
			x = (self.LastX) / 16
			y = (self.LastY) / 16
			for i in range(height):
				bufferIndex = (i * width + x) * bytesPerPixel
				buffer[bufferIndex + 0] = 0
				buffer[bufferIndex + 1] = 0
				buffer[bufferIndex + 2] = 0
				
			for i in range(width):
				bufferIndex = (y * width + i) * bytesPerPixel
				buffer[bufferIndex + 0] = 0
				buffer[bufferIndex + 1] = 0
				buffer[bufferIndex + 2] = 0
		
		bitmap = BitmapSource.Create(width, height, 96, 96, pixelFormat, None, buffer, stride)
		map = self.Content.FindName("map")
		map.Source = bitmap
		#print("end UpdateBitmap SOSList: {0}".format(len(self.SOSList)))
		return

def ShowWindow():
	try:
		window = XamlWindow()
		window.UpdateBitmap()
		window.ShowDialog()
	except Exception as e:
		print e
	return

felTile = GetMapData(0)
traTile = GetMapData(1)

t = Thread(ThreadStart(ShowWindow))
t.SetApartmentState(ApartmentState.STA)
t.Start()
t.Join()

Stop()
