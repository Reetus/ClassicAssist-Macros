# Name: WPF Window Xaml Layout Example
# Description: An example of creating WPF windows with Xaml layouts in ClassicAssist
# Uses a ListView to display Layer and Durability of items worn, refreshing on a WPF DispatcherTimer
# Uses ResourceDictionary from CA to display UI components in dark mode (why not?)
# Author: Reetus
# Era: AOS
# Date: Fri Aug 27 2021

import wpf
import clr
from Assistant import Engine
from ClassicAssist.UO.Data import Layer
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from System import Uri, TimeSpan, Enum
from System.Windows import Window, ResourceDictionary, SizeToContent
from System.Windows.Markup import XamlReader
from System.Windows.Threading import DispatcherTimer
from System.Threading import Thread, ThreadStart, ApartmentState

layers = [
    Layer.OneHanded,
    Layer.TwoHanded,
    Layer.Shoes,
    Layer.Pants,
    Layer.Shirt,
    Layer.Helm,
    Layer.Gloves,
    Layer.Ring,
    Layer.Talisman,
    Layer.Neck,
    Layer.Waist,
    Layer.InnerTorso,
    Layer.Bracelet,
    Layer.MiddleTorso,
    Layer.Earrings,
    Layer.Arms,
    Layer.Cloak,
    Layer.OuterTorso,
    Layer.OuterLegs,
    Layer.InnerLegs,
]

xaml = """
<Grid xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
	  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
	<Grid.RowDefinitions>
		<RowDefinition Height="*"/>
		<RowDefinition Height="Auto"/>
	</Grid.RowDefinitions>
	<ListView Grid.Row="0" x:Name="listView">
		<ListView.View>
        	<GridView>
        		<GridViewColumn Header="Layer" DisplayMemberBinding="{Binding Layer}" Width="120"/>
            	<GridViewColumn Header="Durability" DisplayMemberBinding="{Binding Durability}" Width="80"/>
        	</GridView>
    	</ListView.View>
	</ListView>
	<Button Content="Stop" Grid.Row="1" Margin="10, 10" x:Name="startButton"/>
</Grid>
"""

class LayerDurability:
	def __init__(self, layer, durability):
		self.Layer = layer
		self.Durability = durability
		
def GetDurability(layer):
	serial = Engine.Player.GetLayer(layer)
	if serial != 0:
		item = Engine.Items.GetItem(serial)
		if item != None and item.Properties != None and item.Properties.Any(lambda i: i.Cliloc == 1060639):
			property = item.Properties.FirstOrDefault(lambda i: i.Cliloc == 1060639)
			if property != None and property.Arguments != None:
				return (True, property.Arguments[0])
	return (False, None)

class XamlWindow(Window):
	def __init__(self):
		rd = ResourceDictionary()
		rd.Source = Uri("pack://application:,,,/ClassicAssist.Shared;component/Resources/DarkTheme.xaml")
		self.Resources.MergedDictionaries.Add(rd)
		self.Background = self.Resources["ThemeWindowBackgroundBrush"]		
		
		self.Content = XamlReader.Parse(xaml)
		self.Title = "Durability"
		self.Topmost = True
		self.SizeToContent = SizeToContent.Width
		self.Height = 400
		self.refreshTime = TimeSpan.FromSeconds(30)
		
		self.listView = self.Content.FindName('listView')
		self.startButton = self.Content.FindName('startButton')
		self.startButton.Click += self.onClick
		
		self.timer = DispatcherTimer()
		self.timer.Tick += self.onTick
		self.timer.Interval = TimeSpan().FromSeconds(0)
		self.timer.Start()
		self.timer.Interval = self.refreshTime
		self.Running = True
						
	def onClick(self, sender, event):
		self.Running = not self.Running
		self.startButton.Content = "Start" if not self.Running else 'Stop'
		
		if self.Running:
			print 'Starting timer...'
			self.timer.Interval = TimeSpan().FromSeconds(0)
			self.timer.Start()
			self.timer.Interval = self.refreshTime
		else:
			print 'Stopping timer...'
			self.timer.Stop()
			self.listView.Items.Clear()
	
	def onTick(self, sender, event):
		print 'Updating durabilities'
		self.listView.Items.Clear()
		durabilities = []
		for layer in layers:
			(res, durability) = GetDurability(layer)
			if res:
				durabilities.append(LayerDurability(layer, durability))
		sorted = durabilities.OrderBy(lambda i: int(i.Durability))
		for item in sorted:
			self.listView.Items.Add(item)

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

print 'Window Opening'

t.Join()        

print 'Window Closing'