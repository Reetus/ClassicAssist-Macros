# Name: JelweryBox Filter
# Description: open, load, scan, drop item from jelwery box based on props array setted on code (version with gui)
# Author: ... d0tsd0tsd0ts
# Shard: UOG-Demise
# Date: Fri Sep 06 2024

import json
import re
from datetime import *
import time

import wpf
import System
import clr
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine
from ClassicAssist.UO.Network import IncomingPacketHandlers
from ClassicAssist.UO.Objects.Gumps import Gump
from System import Uri, TimeSpan, Enum
from System.Windows import Application, Window, ResourceDictionary, SizeToContent
from System.Windows.Markup import XamlReader
from System.Windows.Threading import DispatcherTimer
from System.Threading import Thread, ThreadStart, ApartmentState

global props
props = ['damage increase']
#props = ['damage increase', 'faster casting', 'faster cast recovery'] 
#props = ['enhance potions', 'defense chance increase']

_json = False
_gump = 0x74d8915b

def loading():
    global _gump
    
    total = 0
    print '--- Loading ---'
    res, gump = Engine.Gumps.GetGump(_gump)
    if res:         
        for ele in gump.GumpElements.Where(lambda i: i.Type.ToString() == 'xmfhtmltok'):
            if ' of 500' in ele.Text:
                items = ele.Text.split(': ')
                total = int(items[1].split(' of ')[0])
        print total
    
    i = 1
    r = {}   
    c = 0    
    
    while 42:
        if c >= total:
            break
        res, gump = Engine.Gumps.GetGump(_gump)
        r[str(i)] = []
        if res:
            for ele in gump.GumpElements.Where(lambda i: i.Type.ToString() == 'itemproperty'):
                if IncomingPacketHandlers.PropertyCache.ContainsKey(ele.Serial):
                    tool = str(ele.Serial)
                    for p in IncomingPacketHandlers.PropertyCache[ele.Serial]:
                        tool += ';' + p.Text
                    #print tool
                    if tool not in r[str(i)]:
                        c = c + 1
                        r[str(i)].append(tool)
        ReplyGump(_gump, 2)
        WaitForGump(_gump, 1000)
        i = i + 1
        
    print 'Total: {}, Result: {}'.format(total,c)    
    ReplyGump(_gump, 0)   
    return r    

def check_props(v, ps):
    c = 0
    ss = v.replace(' ','').strip().split(';')
    for s in ss:                
        ms = re.match(r"([a-z]+)([0-9]+)", s, re.I)
        if ms:
            gs = ms.groups()
            for p in ps:
                p = p.replace(' ','').strip()
                for g in gs:                                                
                    if p.lower() == g.lower():                        
                        c += 1                                         
    return True if len(ps) == c else False                        

def scan(ps, os):
    print '--- Scaning ---'
    c = 0
    r = {}
    for k,vs in os.iteritems():
        for v in vs:            
            if check_props(v,ps):                
                if '{}'.format(k) not in r:
                    r['{}'.format(k)] = []
                r['{}'.format(k)].append(v)
                c += 1
    print 'Qty: {}'.format(c)
    ReplyGump(_gump, 0)            
    return c, r

def drops(fs):    
    print '--- Droping ---'
    c = 0    
    for k,vs in fs.iteritems():        
        for v in vs:
            print 'Drop: {}'.format(v)
            ps = v.split(';')
            b = int(ps[0])
            drop(b)
            c += 1
    ReplyGump(_gump, 0)            
    return c
    
def drop(b):
    global _gump    
    print 'button:{}'.format(b)
    ReplyGump(_gump, b)
    WaitForGump(_gump, 1000)            
    
def open(jelwerybox, timeout=25000):    
    global _gump       
    if not jelwerybox:
        return
    UseObject(jelwerybox)
    process_timer = datetime.now() + timedelta(milliseconds=timeout)
    while datetime.now() < process_timer and not GumpExists(_gump):
        Pause(1000)
    if not GumpExists(_gump):
        return        
    
            
def writeJsonFile(data, dump=_json):
    if not dump:
        return
    j = json.dumps(data)
    with open("jelwery_box.json", "w") as outfile:
        outfile.write(j)
        
################################################

xaml = """
<Grid xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
      xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">      
    <Grid.RowDefinitions>
        <RowDefinition Height="Auto"/>        
        <RowDefinition Height="*"/>
        <RowDefinition Height="Auto"/>       
    </Grid.RowDefinitions>
    <StackPanel  Margin="10, 10">
        <Rectangle HorizontalAlignment="Stretch" Fill="Gray" Height="1"/>
        <Label FontSize="15.0" FontWeight="Bold" Grid.Row="0" x:Name="propsLabel"></Label>
        <Rectangle HorizontalAlignment="Stretch" Fill="Gray" Height="1"/>
    </StackPanel>
    <ListView HorizontalAlignment="Left" Grid.Row="1" x:Name="listView">
        <ListView.View>
            <GridView>
                <GridViewColumn Header="Page" DisplayMemberBinding="{Binding Page}" Width="40"/>
                <GridViewColumn Header="Item" DisplayMemberBinding="{Binding Item}" Width="900"/>
                <GridViewColumn Header="Gump Button" DisplayMemberBinding="{Binding Button}" Width="100"/>                
            </GridView>
        </ListView.View>
    </ListView>       
    <Button Content="Got it" Grid.Row="2" x:Name="gotItButton"/>   
</Grid>
"""

class JelweryBoxItem:
    def __init__(self, page, item, button):
        self.Page = page
        self.Item = item
        self.Button = button

class XamlWindow(Window): 
    def __init__(self):
        try:
            rd = ResourceDictionary()
            rd.Source = Uri("pack://application:,,,/ClassicAssist.Shared;component/Resources/DarkTheme.xaml")
            self.Resources.MergedDictionaries.Add(rd)
            self.Background = self.Resources["ThemeWindowBackgroundBrush"]      
            
            self.Content = XamlReader.Parse(xaml)
            self.Title = "Jelwery Box"
            self.Topmost = True
            self.SizeToContent = SizeToContent.Width
            self.Height = 800
            self.Width = 700            
            self.refreshTime = TimeSpan.FromSeconds(30)
            
            self.propsLabel = self.Content.FindName('propsLabel') 
            self.propsLabel.Content = 'Looking for: [ {} ]'.format(', '.join(props).strip())
            
            self.listView = self.Content.FindName('listView')                        
            self.listView.Items.Clear()            
            items = Load()
            if not items:
                SysMessage("Properties are not found!!!!!!",34)              
                self.Close();                
            sorted = items.OrderBy(lambda i: i.Page)
            for item in sorted:                
                self.listView.Items.Add(item) 
            
            self.gotItButton = self.Content.FindName('gotItButton')
            self.gotItButton.Click += self.onGotItClick   
            
        except Exception as ex:
            print ex
            
    def onGotItClick(self, sender, event):   
        items = list(self.listView.SelectedItems)
        if items:
            GotIt(items)
            for i in items:
                self.listView.Items.Remove(i)          
                  
    
def GetItemProperty(v):
    ps = v.strip().split(';')
    return '{}'.format('; '.join(ps[1:]).strip())   
        
def GetJelweryBoxItem(fs):
    jelweryBoxItem = []
    for k,vs in fs.iteritems():
        for v in vs:              
            ps = v.split(';')            
            b = int(ps[0])     
            i = GetItemProperty(v)           
            jelweryBoxItem.append(JelweryBoxItem(k,i,b))
    return jelweryBoxItem       
    
def GotIt(items):
    global _gump
    open(GetAlias('Jelwry Box')) 
    for i in items:
        print 'Got It: {} | {}'.format(i.Item, i.Button)
        drop(i.Button)        
    ReplyGump(_gump, 0)             

def Load():     
    global _gump, props
    UnsetAlias('Jelwry Box')
    if PromptAlias('Jelwry Box') == 0:
        Stop()        
    open(GetAlias('Jelwry Box')) 
    loaded = loading()    
    open(GetAlias('Jelwry Box'))
    c, founds = scan(props, loaded)
    writeJsonFile(founds)
    return GetJelweryBoxItem(founds)    
    
def ShowWindow():
    try:
        c = XamlWindow()
        c.ShowDialog()
    except Exception as e:
        print e   

if GumpExists(_gump):
    ReplyGump(_gump, 0)  
WaitForContents("backpack", 600)

t = Thread(ThreadStart(ShowWindow))
t.SetApartmentState(ApartmentState.STA)
t.Start()
t.Join()    