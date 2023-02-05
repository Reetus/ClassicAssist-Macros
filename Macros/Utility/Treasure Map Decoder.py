# Name: Treasure Map Decoder 001
# Description: Decodes treasure maps and display runebook number
# Shard: Any 
# Author: qk
# Date: 3/2-2023

import clr
import System
from System import Array
from ClassicAssist.UO.Data import PacketWriter, PacketReader
from ClassicAssist.UO.Network.PacketFilter import PacketFilterInfo, PacketFilterCondition, PacketFilterConditions, PacketDirection
from Assistant import Engine
from ClassicAssist.UO import UOMath

import ClassicAssist 
clr.ImportExtensions(ClassicAssist.Misc)
from System.Threading.Tasks import Task

colorRed = 33
colorOrange = 43
colorGreen = 75
colorGrey = 990

tmaps = [0x14ec]

# based on player coords
tMapCoords = [
    '1 965 501',
    '2 1162 189',
    '3 1315 317',
    '4 1469 230',
    '5 1504 364',
    '6 2671 392',
    '7 2741 435',
    '8 2770 345',
    '9 2781 289',
    '10 2836 233',
    '11 3014 250',
    '12 3081 202',
    '13 1028 1181',
    '14 1318 889',
    '15 1413 771',
    '16 1529 753',
    '17 1554 806',
    '18 1509 968',
    '19 1561 1058',
    '20 1509 1071',
    '21 2338 645',
    '22 2349 689',
    '23 2395 723',
    '24 2432 767',
    '25 2642 851',
    '26 2457 1042',
    '27 2516 1066',
    '28 2337 1159',
    '29 2392 1153',
    '30 3245 246',
    '31 3402 238',
    '32 3375 458',
    '33 3369 638',
    '34 200 1454',
    '35 210 1440',
    '36 359 1337',
    '37 581 1453',
    '38 348 1565',
    '39 619 1706',
    '40 962 1859',
    '41 979 1850',
    '42 969 1894',
    '43 969 1884',
    '44 973 1878',
    '45 1017 1860',
    '46 1037 1879',
    '47 1039 1898',
    '48 1042 1960',
    '49 1038 1976',
    '50 1024 1991',
    '51 974 1992',
    '52 989 1993',
    '53 450 2053',
    '54 478 2043',
    '55 492 2027',
    '56 467 2087',
    '57 465 2100',
    '58 1657 2031',
    '59 1689 1993',
    '60 1709 1963',
    '61 1724 1999',
    '62 1731 2017',
    '63 1742 2029',
    '64 1754 2021',
    '65 2033 1942',
    '66 2053 1963',
    '67 2064 1979',
    '68 2057 1990',
    '69 2069 2007',
    '70 2061 1962',
    '71 2097 1976',
    '72 2088 1987',
    '73 2092 2006',
    '74 2187 1991',
    '75 1425 2405',
    '76 1433 2381',
    '77 1469 2340',
    '78 1450 2301',
    '79 1435 2294',
    '80 1437 2217',
    '81 1466 2181',
    '82 1463 2246',
    '83 1477 2273',
    '84 1561 2312',
    '85 1546 2222',
    '86 1517 2214',
    '87 1532 2189',
    '88 1521 2150',
    '89 1541 2114',
    '90 1593 2193',
    '91 1617 2236',
    '92 1653 2268',
    '93 1723 2288',
    '94 1772 2321',
    '95 1757 2333',
    '96 1764 2431',
    '97 1701 2318',
    '98 1653 2304',
    '99 2060 2144', #
    '100 2105 2124',
    '101 2097 2101',
    '102 2128 2108',
    '103 2153 2122',
    '104 2185 2143',
    '105 2177 2152',
    '106 2160 2149',
    '107 2129 2133',
    '108 2122 2121',
    '109 2646 2167',
    '110 2627 2221',
    '111 2641 2289',
    '112 2681 2291',
    '113 2727 2309',
    '114 2781 2294',
    '115 2804 2255',
    '116 2850 2252',
    '117 2957 2150',
    '118 2967 2171',
    '119 2952 2176', #
    '120 2955 2200',
    '121 2932 2240',
    '122 958 2505',
    '123 1025 2702',
    '124 1290 2735', #
    '125 1382 2840',
    '126 1390 2985',
    '127 1414 3059',
    '128 1647 2642',
    '129 1562 2705',
    '130 1670 2808',
    '131 1600 3013',
    '132 1664 3063',
    '133 1067 3182',
    '134 1074 3156',
    '135 1072 3133',
    '136 1089 3110',
    '137 1092 3132',
    '138 1096 3178',
    '139 1128 3403',
    '140 1161 3468',
    '141 1126 3499',
    '142 1135 3446',
    '143 2013 3269',
    '144 2039 3427',
    '145 2095 3384',
    '146 2148 3362',
    '147 2369 3428',
    '148 2341 3482',
    '149 2359 3507',
    '150 2386 3506',
    '151 2466 3580',
    '152 2480 3623',
    '153 2527 3584',
    '154 2533 3609',
    '155 2796 3452',
    '156 2802 3489',
    '157 2791 3520',
    '158 2830 3510',
    '159 2988 3606',
    '160 3034 3602',
    '161 2153 3983',
    '162 2143 3985',
    '163 2139 3941',
    '164 2156 3924',
    '165 2151 3951',
    '166 2161 3988',
    '167 2451 3942',
    '168 2421 3928',
    '169 2413 3920',
    '170 2421 3902',
    '171 2480 3908',
    '172 2511 3899',
    '173 2511 3919',
    '174 2511 3962',
    '175 2526 3982',
    '176 2515 3998',
    '177 4475 3282',
    '178 4476 3230',
    '179 4465 3211',
    '180 4424 3152',
    '181 4418 3117', #
    '182 4448 3130',
    '183 4453 3148',
    '184 4500 3108',
    '185 4512 3104',
    '186 4469 3188',
    '187 4506 3227',
    '188 4494 3242',
    '189 4641 3369',
    '190 4693 3486',
    '191 3476 2761',
    '192 3425 2723',
    '193 3417 2675',
    '194 3532 2471',
    '195 3510 2421',
    '196 3567 2402',
    '197 3701 2825',
    '198 3593 2826',
    '199 3556 2820',
    '200 3541 2785',
]

def GetValidMap(serial, id):
    item = Engine.Items.GetItem(serial)
    if (item != None and item.ID == id):
        return True
    return False

def getMapLocation(serial, timeout = 5000):
    pfiMapDetails = PacketFilterInfo(0x90, System.Array[PacketFilterCondition]([PacketFilterConditions.IntAtPositionCondition(serial, 1)]))
    pfiMapDetailsNew = PacketFilterInfo(0xF5, System.Array[PacketFilterCondition]([PacketFilterConditions.IntAtPositionCondition(serial, 1)]))
    
    pfiMapPlot = PacketFilterInfo(0x56, System.Array[PacketFilterCondition]([PacketFilterConditions.IntAtPositionCondition(serial, 1),PacketFilterConditions.ByteAtPositionCondition(1, 5)]))
    
    pweMapDetails = Engine.PacketWaitEntries.Add(pfiMapDetails, PacketDirection.Incoming, True)
    pweMapDetailsNew = Engine.PacketWaitEntries.Add(pfiMapDetailsNew, PacketDirection.Incoming, True) 
    
    pweMapPlot = Engine.PacketWaitEntries.Add(pfiMapPlot, PacketDirection.Incoming, True)
    
    t = Task.WhenAny(pweMapDetails.Lock.ToTask(), pweMapDetailsNew.Lock.ToTask())
    
    UseObject(serial)
    
    t.Wait()
    
    packet = None
    
    if pweMapDetails.Packet == None:
        packet = pweMapDetailsNew.Packet
    else:
        packet = pweMapDetails.Packet
    
    #if not pweMapDetails.Lock.WaitOne(timeout):
    #    return (-1, -1, -1)
    
    reader = PacketReader(packet, packet.Length, True)
    reader.ReadInt32()
    image = reader.ReadInt16()
    x1 = reader.ReadUInt16()
    y1 = reader.ReadUInt16()
    x2 = reader.ReadUInt16()
    y2 = reader.ReadUInt16()       
    width = reader.ReadUInt16()
    height = reader.ReadUInt16()               
    facet = reader.ReadUInt16()               
        
    if not pweMapPlot.Lock.WaitOne(timeout):
        return (-1, -1, -1)
    
    reader2 = PacketReader(pweMapPlot.Packet, pweMapPlot.Packet.Length, True)
    reader2.ReadInt32()
    reader2.ReadUInt16()
    x = reader2.ReadUInt16()
    y = reader2.ReadUInt16()
    
    calcX = (x1 + x) + x
    calcY = (y1 + y) + y
    
    return (calcX, calcY, x1, y1, x2, y2, width, height, facet, x, y)
    
UnsetAlias("map")
PromptAlias("map")

if not GetValidMap(GetAlias("map"), 0x14ec):
    SysMessage("No Valid Map Selected", colorRed)
    Stop()
    
cX, cY, x1, y1, x2, y2, width, height, facet, x, y = getMapLocation(GetAlias("map"))

#SysMessage('Player: X: {}, Y: {}'.format(Engine.Player.X, Engine.Player.Y), colorGreen)
#SysMessage('Map: cX: {}, cY: {}'.format(cX, cY), colorOrange)
#SysMessage('Map: X1: {}, Y1: {}'.format(x1, y1), colorRed)
#SysMessage('Map: X2: {}, Y2: {}'.format(x2, y2), colorRed)
#SysMessage('Map: width: {}, height: {}'.format(width, height), colorRed)
#SysMessage('Map: X: {}, Y: {}'.format(x, y), colorRed)
#SysMessage('-', colorRed)

mapNr = 0
for i in tMapCoords:
    _nr = i.split(" ")[0]
    _x = i.split(" ")[1]
    _y = i.split(" ")[-1]
    
    if _x != "":
        _distance = UOMath.Distance(cX, cY, int(_x), int(_y))
        if _distance <= 5:
            mapNr = _nr

if mapNr != 0:
    SysMessage('Decoded TMap #{}'.format(mapNr), colorGreen)
else:
    SysMessage('Unable To Decode TMap', colorRed)
