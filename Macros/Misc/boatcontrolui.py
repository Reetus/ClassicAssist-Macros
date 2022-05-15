# Name: Boat Control UI
# Description: Boat control UI like UO rudder for navigating around in a boat, with text commands
# Author: Reetus
# Era: Any
# Date: Wed Dec 01 2021

import wpf
import clr
from Assistant import Engine
from ClassicAssist.UO.Data import Layer
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from System import Uri, TimeSpan, Enum
from System.Windows import Window, ResourceDictionary
from System.Windows.Markup import XamlReader
from System.Threading import Thread, ThreadStart, ApartmentState

xaml = """
<Grid xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
	  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
	<Grid.RowDefinitions>
		<RowDefinition Height="*"/>
		<RowDefinition Height="*"/>
		<RowDefinition Height="*"/>
		<RowDefinition Height="*"/>
		<RowDefinition Height="*"/>
	</Grid.RowDefinitions>
	<Grid.ColumnDefinitions>
		<ColumnDefinition Width="*"/>
		<ColumnDefinition Width="*"/>
		<ColumnDefinition Width="*"/>	
	</Grid.ColumnDefinitions>
	<Button Content="↖" Grid.Row="0" Grid.Column="0" x:Name="forwardLeft"/>
	<Button Content="↑" Grid.Row="0" Grid.Column="1" x:Name="forward"/>
	<Button Content="↗" Grid.Row="0" Grid.Column="2" x:Name="forwardRight"/>
	<Button Content="←" Grid.Row="1" Grid.Column="0" x:Name="left"/>
	<Button Content="↻" Grid.Row="1" Grid.Column="1" x:Name="turnAround"/>
	<Button Content="→" Grid.Row="1" Grid.Column="2" x:Name="right"/>	
	<Button Content="↙" Grid.Row="2" Grid.Column="0" x:Name="backLeft"/>
	<Button Content="↓" Grid.Row="2" Grid.Column="1" x:Name="back"/>
	<Button Content="↘" Grid.Row="2" Grid.Column="2" x:Name="backRight"/>		
	<Button Content="Stop" Grid.Row="3" Grid.Column="0" x:Name="stop"/>		
	<Button Content="Raise" Grid.Row="3" Grid.Column="1" x:Name="raiseAnchor"/>		
	<Button Content="Drop" Grid.Row="3" Grid.Column="2" x:Name="dropAnchor"/>
	<Button Content="↶" Grid.Row="4" Grid.Column="0" x:Name="turnLeft"/>
	<Button Content="Start" Grid.Row="4" Grid.Column="1" x:Name="start"/>
	<Button Content="↷" Grid.Row="4" Grid.Column="2" x:Name="turnRight"/>		
</Grid>
"""

class XamlWindow(Window):
	def __init__(self):
		rd = ResourceDictionary()
		rd.Source = Uri("pack://application:,,,/ClassicAssist.Shared;component/Resources/DarkTheme.xaml")
		self.Resources.MergedDictionaries.Add(rd)
		self.Background = self.Resources["ThemeWindowBackgroundBrush"]		
		
		self.Content = XamlReader.Parse(xaml)
		self.Title = "Rudder"
		self.Topmost = True
		self.Height = 250
		self.Width = 250
		self.refreshTime = TimeSpan.FromSeconds(30)
		
		self.events = [ 
						('forwardLeft', 'Forward Left'),
					   	('forward', 'Forward'),
					   	('forwardRight', 'Forward Right'),
					   	('left', 'Left'),
					   	('turnAround', 'Turn Around'),
					   	('right', 'Right'),
					   	('backLeft', 'Back Left'),
					   	('back', 'Back'),
					   	('backRight', 'Back Right'),
					   	('stop', 'Stop'),
					   	('raiseAnchor', 'Raise Anchor'),
					   	('dropAnchor', 'Drop Anchor'),
					   	('turnLeft', 'Turn Left'),
					   	('turnRight', 'Turn Right'),
					   	('start', 'Start')
					  ]
		self.setEvents()

	def setEvents(self):
		for x in self.events:
			btn = self.Content.FindName(x[0])
			btn.Click += self.clickButton
			
	def clickButton(self, sender, event):
		for x in self.events:
			if x[0] == event.Source.Name:
				Msg(x[1])

def ShowWindow():
    try:
        c = XamlWindow()
        c.ShowDialog()
    except Exception as e:
    	# if you don't catch these, an exception will likely take down CUO/CA
        print e

t = Thread(ThreadStart(ShowWindow))
t.SetApartmentState(ApartmentState.STA)
t.Start()
t.Join()        
