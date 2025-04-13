# Name: Macro UI Customize
# Description: 매크로 사용자 UI 를 만듭니다
# Author: yangpa
# Shard: Margo
# Date: 2025.04.13

from ClassicAssist.UO.Objects.Gumps import Gump
from ClassicAssist.UO.Objects.Gumps import GumpButtonType
from collections import OrderedDict
from ClassicAssist.Data.Macros import MacroManager

class MacroUI(Gump):
    def __init__(self, x=0, y=0, page=0, gumpId=987654):
        pass
        
    def _add_option_button(self, x, y, button_id, option):
        uncheck = 2151
        check = 2153
        # Add checkbox button to the gump
        if option:
            self.AddButton(x, y, check, uncheck, button_id, GumpButtonType.Reply, 0)  # checked
        else:
            self.AddButton(x, y, uncheck, check, button_id, GumpButtonType.Reply, 0)  # unchecked
    
    def OnResponse(self, buttonID, switches, textEntries=None):
        if buttonID == 100:
            self.running = False
        else:
          for idx, (key, value) in enumerate(self.options.items()):
              if buttonID == idx:
                  self.options[key] = 1 - value  # Toggle option
                  break
    def OnClosing(self):
        if self.running and Playing(self.ownerMacro):
            self.Show(self.options, self.labels, self.ownerMacro)
        elif not self.running:
            Stop(self.ownerMacro)
            
    def Show(self, options, labels, ownerMacro):
        # UI setup
        self.options = options
        self.labels = labels
        self.ownerMacro = ownerMacro
        self.Movable = True
        self.AddPage(0)
        self.AddBackground(0, 0, 150, 30 * len(self.options) + 20, 30546)  # window 1
        self.AddAlphaRegion(0, 0, 150, 30 * len(self.options) + 20)  # alpha black window
        self.AddButton(135, 0, 2117, 2123, 100, GumpButtonType.Reply, 0)  # macro stop button

        # Displaying button labels
        for i in range(len(self.labels)):
            self.AddLabel(40, 15 + 30 * i, 55, self.labels[i])

        for idx, (key, value) in enumerate(self.options.items()):
            self._add_option_button(5, 10 + 30 * idx, idx, value)
        
        self.running = True
        self.SendGump()
        

# Example usage:
options = OrderedDict()
options["useEnemyOfOne"] = 0  # 0 False / 1 True
options["useConsecrateWeapon"] = 1  # 0 False / 1 True
options["useRemoveCurse"] = 0  # 0 False / 1 True
options["useCounterAttack"] = 0  # 0 False / 1 True

labels = [
 "Enemy Of One"
,"ConsecrateWeapon"
,"Remove Curse"
,"Counter Attack"
]

# Initialize the custom Gump
UI = MacroUI(0, 0, 0, 987654)
UI.Show(options, labels, MacroManager.GetInstance().CurrentMacro.Name)

# TestCode
while True:
  for i in options:
      print(i, options[i])
  Pause(1000)
