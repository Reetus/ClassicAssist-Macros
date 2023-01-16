# Name: Pet Skills Window
# Description: Pet skills window similiar to skills tab showing value / cap / delta, useful when training pets
# Author: Reetus
# Shard: Margo
# Date: Mon Jan 16 2023

import wpf
import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine
from ClassicAssist.UO.Data import Layer
from System import Uri, TimeSpan, Enum
from System.Windows import Window, ResourceDictionary, SizeToContent
from System.Windows.Markup import XamlReader
from System.Windows.Threading import DispatcherTimer, Dispatcher
from System.Threading import Thread, ThreadStart, ApartmentState
import re

gumpId = 0xd937d1db
pet = GetAlias('lorePet')

if not FindAlias('lorePet'):
    pet = PromptAlias('lorePet')
    
class SkillInfo:
    def __init__(self, name, value, cap, delta):
        self.Name = name
        self.Value = value
        self.Cap = cap
        self.Delta = delta

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
                <GridViewColumn Header="Name" DisplayMemberBinding="{Binding Name}" Width="120"/>
                <GridViewColumn Header="Value" DisplayMemberBinding="{Binding Value}" Width="80"/>
                <GridViewColumn Header="+/-" DisplayMemberBinding="{Binding Delta}" Width="80"/>
                <GridViewColumn Header="Cap" DisplayMemberBinding="{Binding Cap}" Width="80"/>
            </GridView>
        </ListView.View>
    </ListView>
    <Button Content="Stop" Grid.Row="1" Margin="10, 10" x:Name="startButton"/>
</Grid>
"""

skills = []

def getSkills():
    UseSkill("Animal Lore")
    WaitForTarget(5000)
    Target(pet)
    WaitForGump(gumpId, 5000)
    
    loyalty = ""

    [res, gump] = Engine.Gumps.GetGump(gumpId)
    if res:
        loyaltyEle = gump.Pages[1].GetElementByXY(53, 236)
        
        loyalty = loyaltyEle.Text
    
        for page in range(5, 8):
            gumpPage = gump.Pages[page]
            
            for y in range(92, 236+18, 18):
                skillEle = gumpPage.GetElementByXY(53, y)
                amountEle = gumpPage.GetElementByXY(180, y)
                
                skillAmount = 0
                skillCap = 0
                
                if amountEle:
                    matches = re.search("<div align=right>(.*)/(.*)</div>", amountEle.Text)
                    if matches:
                        skillAmount = float(matches.groups()[0])
                        skillCap = float(matches.groups()[1])
                        
                existing = None
                
                                                       
                if skillEle and skillCap > 0:
                    for x in skills:
                        if x.Name == skillEle.Text:
                            existing = x
                            
                    if existing:
                        delta = (skillAmount - existing.Value)
                        existing.Value = skillAmount
                        existing.Cap = skillCap
                        existing.Delta += float(delta)
                    else:
                        skills.append(SkillInfo(skillEle.Text, skillAmount, skillCap, 0))
        ReplyGump(gumpId, 0)                     
    return loyalty

class XamlWindow(Window):
    def __init__(self):
        rd = ResourceDictionary()
        rd.Source = Uri("pack://application:,,,/ClassicAssist.Shared;component/Resources/DarkTheme.xaml")
        self.Resources.MergedDictionaries.Add(rd)
        self.Background = self.Resources["ThemeWindowBackgroundBrush"]      
        
        self.Content = XamlReader.Parse(xaml)
        self.Title = "Pet Skills"
        self.Topmost = True
        self.SizeToContent = SizeToContent.WidthAndHeight
        self.MinHeight = 400
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
        self.dispatcher = Dispatcher.CurrentDispatcher
        
        Events.Shutdown += self.onShutdown
        
    def onShutdown(self, sender, event):
        self.dispatcher.Invoke(lambda: self.Close())
                        
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
    
    def onTick(self, sender, event):    
        loyalty = getSkills()
        self.listView.Items.Clear()
        sorted = skills.OrderByDescending(lambda i: i.Delta)
        
        for x in sorted:
            self.listView.Items.Add(x)
            
        self.Title = "Pet Skills ({}) - {}".format(Name(pet), loyalty)

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