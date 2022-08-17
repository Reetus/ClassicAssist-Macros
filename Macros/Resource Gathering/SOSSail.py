# Name: SOS Sail
# Description: Sail to SOS Coordiate, in Felucca and Trammel
#               Sail use A* with 16 x 16 Tile but not perfect
#               Hunt monster with magery
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
from System.Windows import Window, ResourceDictionary, Point
from System.Windows.Markup import XamlReader
from System.Windows.Shapes import Ellipse, Line, Path
from System.Windows.Media import ImageBrush, Brushes, PolyLineSegment, PathFigure, PathGeometry, PixelFormats
from System.Windows.Controls import ToolTip, Canvas
from System.Threading import Thread, ThreadStart, ApartmentState
from System import Array, Byte
from System.Windows.Media.Imaging import BitmapSource
from System.Windows.Threading import DispatcherTimer


SetQuietMode(True)

global SOSType
global PoleType
global MonsterTypes
global SOSChestTypes

SOSType = 0x14EE
PoleType = 0x0DC0
MonsterTypes = [0x96,0x10,0x4D,0x97,0xb6, 0xb5]
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
		<Grid>
			<Canvas
				VerticalAlignment="Top"
				Name="canvas"
				Width="320"
				Height="256">
				<Canvas.Background>
					<ImageBrush x:Name="map"/>
				</Canvas.Background>
			</Canvas>
			<Canvas
				IsHitTestVisible="False"
				VerticalAlignment="Top"
				Name="lineCanvas"
				Width="320"
				Height="256">
			</Canvas>
			<Canvas
				IsHitTestVisible="False"
				VerticalAlignment="Top"
				Name="routeCanvas"
				Width="320"
				Height="256">
			</Canvas>
		</Grid>
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
				<CheckBox Name="CheckFishing" Content="Fishing when arrived" IsChecked="True" />
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
		e = Ellipse()
		e.Width = 5
		e.Height = 5
		if owner == "backpack":
			e.Fill = Brushes.Red
			e.Stroke = Brushes.Red
		else:
			e.Fill = Brushes.Yellow
			e.Stroke = Brushes.Yellow
		e.ToolTip = ToolTip()
		e.ToolTip.Content = "({}, {})".format(x, y)
		Canvas.SetLeft(e, self.MapX - e.Width / 2)
		Canvas.SetTop(e, self.MapY - e.Height / 2)
		self.ellipse = e
	def SetOwner(self, owner):
		self.Owner = owner
		if owner == "backpack":
			self.ellipse.Fill = Brushes.Red
			self.ellipse.Stroke = Brushes.Red
		else:
			self.ellipse.Fill = Brushes.Yellow
			self.ellipse.Stroke = Brushes.Yellow
		return

class Tile:
	def __init__(self, x, y, parent = None, cost = 0):
		self.X = x
		self.Y = y
		self.Cost = cost
		self.Parent = parent
		self.Distance = 0
	def SetDistance(self, targetX, targetY):
		self.Distance = (abs(self.X - targetX) + abs(self.Y - targetY)) * 10
		self.CostDistance = self.Cost + self.Distance

def SimplifySailRoute(CurrentRail):
	railLen = len(CurrentRail)
	if railLen < 3:
		return CurrentRail

	prevDir = ""
	simpleRoute = []
	#simpleRoute.append(CurrentRail[0])
	for index in range(1, railLen):
		dir = ""
		if CurrentRail[index - 1][1] > CurrentRail[index][1]:
			dir += "n"
		elif CurrentRail[index - 1][1] < CurrentRail[index][1]:
			dir += "s"
		if CurrentRail[index - 1][0] > CurrentRail[index][0]:
			dir += "w"
		elif CurrentRail[index - 1][0] < CurrentRail[index][0]:
			dir += "e"

		if (prevDir != dir):
			simpleRoute.append(CurrentRail[index - 1])
		#print("prev: {}, current({}) {} ".format(prevDir, index, dir))
		prevDir = dir
	#if simpleRoute[-1] != CurrentRail[-1]:
	simpleRoute.append(CurrentRail[-1])
	return simpleRoute


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
		Tile(currentTile.X - 1, currentTile.Y - 1, currentTile, currentTile.Cost + 14),
		Tile(currentTile.X - 1, currentTile.Y, currentTile, currentTile.Cost + 10),
		Tile(currentTile.X - 1, currentTile.Y + 1, currentTile, currentTile.Cost + 14),
		Tile(currentTile.X + 1, currentTile.Y - 1, currentTile, currentTile.Cost + 14),
		Tile(currentTile.X + 1, currentTile.Y, currentTile, currentTile.Cost + 10),
		Tile(currentTile.X + 1, currentTile.Y + 1, currentTile, currentTile.Cost + 14),
		Tile(currentTile.X, currentTile.Y - 1, currentTile, currentTile.Cost + 10),
		Tile(currentTile.X, currentTile.Y + 1, currentTile, currentTile.Cost + 10),
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

	ret = []
	ret.append((start[0] * 16 + 8, start[1] * 16 + 8))
	ret.append((end[1] * 16 + 8, end[1] * 16 + 8))

	if start[0] < 0 or width - 1 < start[0] or start[1] < 0 or height - 1 < start[1]:
		print("start position Error ({}, {})".format(start[0], start[1]))
		return ret
	if end[0] < 0 or width - 1 < end[0] or end[1] < 0 or height - 1 < end[1]:
		print("start position Error ({}, {})".format(end[0], end[1]))
		return ret
	if map[start[0]][start[1]] != 1 or map[end[0]][end[1]] != 1:
		print("start position Error ({}, {})".format(start[0], start[1]))
		print("end position Error ({}, {})".format(end[0], end[1]))
		print("failed SearchRoute start({}) end({})".format(map[start[0]][start[1]], map[end[0]][end[1]]))
		return ret
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
	loopCnt = 0
	UseObject(sos.Serial)
	while not WaitForGump(SOSGumpID, 5000):
		UseObject(sos.Serial)
		Pause(100)
		loopCnt += 1
		if loopCnt > 5:
			return None

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

		loopCnt = 0
		while GumpExists(SOSGumpID):
			ReplyGump(SOSGumpID, 0)
			Pause(100)
			loopCnt += 1
			if loopCnt > 5:
				return None

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
			tile1 = MapInfo.GetLandTile(map, x * 16 + 8, y * 16 + 8)
			tile2 = MapInfo.GetLandTile(map, x * 16 + 4, y * 16 + 4)
			tile3 = MapInfo.GetLandTile(map, x * 16 + 12, y * 16 + 4)
			tile4 = MapInfo.GetLandTile(map, x * 16 + 4, y * 16 + 12)
			tile5 = MapInfo.GetLandTile(map, x * 16 + 12, y * 16 + 12)
			if tile1.Name == "water" and tile2.Name == "water" and tile3.Name == "water" and tile4.Name == "water" and tile5.Name == "water":
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
			("DebugButton", self.ClickDebug),
		]

		for i in self.events:
			btn = self.Content.FindName(i[0])
			btn.Click += i[1]
		self.sailBtn = self.Content.FindName("MoveNext")

		self.map = self.Content.FindName("map")
		self.canvas = self.Content.FindName("canvas")
		self.lineCanvas = self.Content.FindName("lineCanvas")
		self.routeCanvas = self.Content.FindName("routeCanvas")
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

		self.TraBitmap = self.CreateBitmapSource(traTile)
		self.FelBitmap = self.CreateBitmapSource(felTile)
		self.ChangeBackgroudImage()

		self.CharHorizonLine = Line()
		self.CharHorizonLine.Stroke = Brushes.Black
		self.CharHorizonLine.StrokeThickness = 1
		self.lineCanvas.Children.Add(self.CharHorizonLine)
		self.CharVerticalLine = Line()
		self.CharVerticalLine.Stroke = Brushes.Black
		self.CharVerticalLine.StrokeThickness = 1
		self.lineCanvas.Children.Add(self.CharVerticalLine)
		self.SOSHorizonLine = Line()
		self.SOSHorizonLine.Stroke = Brushes.White
		self.SOSHorizonLine.StrokeThickness = 1
		self.lineCanvas.Children.Add(self.SOSHorizonLine)
		self.SOSVerticalLine = Line()
		self.SOSVerticalLine.Stroke = Brushes.White
		self.SOSVerticalLine.StrokeThickness = 1
		self.lineCanvas.Children.Add(self.SOSVerticalLine)
		return

	def CharMove(self):
		if Engine.Player.Map == Map.Felucca or Engine.Player.Map == Map.Trammel:
			self.CharHorizonLine.X1 = 0
			self.CharHorizonLine.Y1 = Y("self") / 16
			self.CharHorizonLine.X2 = width - 1
			self.CharHorizonLine.Y2 = Y("self") / 16
			self.CharVerticalLine.X1 = X("self") / 16
			self.CharVerticalLine.Y1 = 0
			self.CharVerticalLine.X2 = X("self") / 16
			self.CharVerticalLine.Y2 = height - 1
		else:
			self.CharHorizonLine.X1 = 0
			self.CharHorizonLine.Y1 = 0
			self.CharHorizonLine.X2 = 0
			self.CharHorizonLine.Y2 = 0
			self.CharVerticalLine.X1 = 0
			self.CharVerticalLine.Y1 = 0
			self.CharVerticalLine.X2 = 0
			self.CharVerticalLine.Y2 = 0
		return
	def ChangeCurrentSOS(self):
		if self.CurrentSOS == None:
			self.SOSHorizonLine.X1 = 0
			self.SOSHorizonLine.Y1 = 0
			self.SOSHorizonLine.X2 = 0
			self.SOSHorizonLine.Y2 = 0
			self.SOSVerticalLine.X1 = 0
			self.SOSVerticalLine.Y1 = 0
			self.SOSVerticalLine.X2 = 0
			self.SOSVerticalLine.Y2 = 0
		else:
			self.SOSHorizonLine.X1 = 0
			self.SOSHorizonLine.Y1 = self.CurrentSOS.MapY
			self.SOSHorizonLine.X2 = width - 1
			self.SOSHorizonLine.Y2 = self.CurrentSOS.MapY
			self.SOSVerticalLine.X1 = self.CurrentSOS.MapX
			self.SOSVerticalLine.Y1 = 0
			self.SOSVerticalLine.X2 = self.CurrentSOS.MapX
			self.SOSVerticalLine.Y2 = height - 1
		return
	def ChangeBackgroudImage(self):
		if Engine.Player.Map == Map.Felucca:
			self.map.ImageSource = self.FelBitmap
		else:
			self.map.ImageSource = self.TraBitmap

	def ResetCanvasChildren(self):
		self.canvas.Children.Clear()
		for sosInfo in self.SOSList:
			self.canvas.Children.Add(sosInfo.ellipse)

	def CreateBitmapSource(self, tiles):
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
		return BitmapSource.Create(width, height, 96, 96, pixelFormat, None, buffer, stride)

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
			self.DrawRoute(currentX, currentY)
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
	def DrawRoute(self, currentX, currentY):
		self.routeCanvas.Children.Clear()
		if (currentX == None or currentY == None):
			return

		lineSegment = PolyLineSegment()
		#lineSegment.Points.Add(Point(currentX / 16, currentY / 16))
		for rail in self.CurrentRail:
			lineSegment.Points.Add(Point(rail[0] / 16, rail[1] / 16))

		pathFigure = PathFigure()
		pathFigure.StartPoint = Point(currentX / 16, currentY / 16)
		pathFigure.Segments.Add(lineSegment)
		pathGeometry = PathGeometry()
		pathGeometry.Figures.Add(pathFigure)
		path = Path()
		path.Stroke = Brushes.Magenta
		path.StrokeThickness = 2.0
		path.Data = pathGeometry
		self.routeCanvas.Children.Add(path)

	def tickhandler(self, sender, args):
		if Engine.Player.Map != Map.Felucca and Engine.Player.Map != Map.Trammel:
			self.CurrentRail = []
			return
		#Resync()
		newTile = GetPlayerFacetTile()
		shipDir = FindShip()

		if self.State == "Fishing" or self.State == "Sail":
			if self.sailBtn.Content != "Stop":
				self.sailBtn.Content = "Stop"
		elif self.sailBtn.Content != "Sail to next SOS":
			self.sailBtn.Content = "Sail to next SOS"

		if shipDir != None:
			if KillMonster():
				self.MovingCnt = 0

		currentX = X("self")
		currentY = Y("self")
		moved = False
		needRedraw = False

		if (currentX != self.LastX or currentY != self.LastY):
			moved = True
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
			if self.CurrentSOS in self.SOSList:
				self.SOSList.remove(self.CurrentSOS)

			self.canvas.Children.Remove(self.CurrentSOS.ellipse)
			self.CurrentSOS = None
			self.ChangeCurrentSOS()
			self.CurrentRail = []
			if self.State == "Sail":
				Msg("stop")
			self.State = None

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
					if (closedSOS.X - currentX) ** 2 + (closedSOS.Y - currentY) ** 2 > (sosInfo.X - currentX) ** 2 + (sosInfo.Y - currentY) ** 2:
						closedSOS = sosInfo
				sosChanged = False
				if closedSOS.Owner == "backpack" and self.CurrentSOS != closedSOS:
					self.CurrentSOS = closedSOS
					self.ChangeCurrentSOS()
					sosChanged = True
				if len(self.CurrentRail) == 0 or sosChanged:
					self.CurrentRail = SearchRoute(self.FacetTile, ((currentX) / 16, (currentY) / 16), (closedSOS.MapX, closedSOS.MapY))
					if self.CurrentRail == None:
						self.CurrentRail = [(closedSOS.X, closedSOS.Y)]
						self.MsgBoxUpdate("route found failed. use Coord")
					else:
						self.CurrentRail = SimplifySailRoute(self.CurrentRail)
					self.DrawRoute(currentX, currentY)

		self.LastX = currentX
		self.LastY = currentY

		if needRedraw:
			self.ChangeBackgroudImage()
		if moved:
			self.CharMove()
		if self.State == None and InJournal("gogogo", Name()) and self.CurrentSOS != None:
			self.State = "Sail"
			ClearJournal()
		elif self.State == None:
			ClearJournal()

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
		if self.CurrentSOS == None:
			debugmsg += "self.CurrentSOS: {}\n".format(self.CurrentSOS)
		else:
			debugmsg += "self.CurrentSOS: ({}, {})\n".format(self.CurrentSOS.X, self.CurrentSOS.Y)
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
		self.ResetCanvasChildren()
		self.ButtonEnable()
		return
	def ClickLoadBackpack(self, sender, event):
		self.ButtonDisable()
		self.SOSList = []
		#self.BackpackSOSList = []
		FindSOS(self, GetAlias("backpack"))
		if FindShip() != None:
			self.LastX = None
		self.ResetCanvasChildren()
		self.ButtonEnable()
		return
	def ClickMoveSOS(self, sender, event):
		self.ButtonDisable()
		self.MsgBoxUpdate("Click Map")
		self.canvas.MouseDown += self.MapMouseDown
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
		if WaitForTargetOrFizzle(5000):
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
		if self.sailBtn.Content == "Sail to next SOS":
			self.State = "Sail"
			self.MovingCnt = 0
		else:
			self.State = None
			self.MovingCnt = 0
			Msg("Stop")
		return
	def MapMouseDown(self, sender, event):
		self.MsgBoxUpdate("")
		self.canvas.MouseDown -= self.MapMouseDown
		clicked = event.GetPosition(self.canvas)
		print("Click on ({}, {})".format(clicked.X, clicked.Y))
		moveCnt = (self.SOSMoveCount.SelectedIndex + 1 )* 10
		sortedSOS = sorted(self.SOSList, key=lambda sos: max(abs(sos.MapX - clicked.X), abs(sos.MapY - clicked.Y)))
		for i, sosInfo in enumerate(sortedSOS):
			if i == moveCnt:
				break
			print("Move SOS ({}, {}), map({}, {})".format(sosInfo.X, sosInfo.Y, sosInfo.MapX, sosInfo.MapY))
			MoveItem(sosInfo.Serial, "backpack")
			Pause(600)
			sosInfo.SetOwner("backpack")
		self.ButtonEnable()
		return

	def MsgBoxUpdate(self, message):
		msgBox = self.Content.FindName("MsgBox")
		msgBox.Text = message
		return

def ShowWindow():
	try:
		window = XamlWindow()
		print("Load done")
		window.ShowDialog()
	except Exception as e:
		print type(e)
		print e
	return

felTile = GetMapData(0)
traTile = GetMapData(1)


if FindObject("mount"):
	if not Property("mount", "guarding"):
		Msg("all guard me")

t = Thread(ThreadStart(ShowWindow))
t.SetApartmentState(ApartmentState.STA)
t.Start()
t.Join()

Stop()
