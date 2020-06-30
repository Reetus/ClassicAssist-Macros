# Name: Durability check
# Description: Checks all items for durability and show alerts
# Author: Mordor
# Era: AOS

from Assistant import Engine
layers = [
    'OneHanded',
    'TwoHanded',
    'Shoes',
    'Pants',
    'Shirt',
    'Helm',
    'Gloves',
    'Ring',
    'Talisman',
    'Neck',
    'Waist',
    'InnerTorso',
    'Bracelet',
    'MiddleTorso',
    'Earrings',
    'Arms',
    'Cloak',
    'OuterTorso',
    'OuterLegs',
    'InnerLegs',
]

# Amount of durability to alert
minDurability = 20
# Checks every 5 secs
checkDelay = 1000 * 60  # every 1 min


def property_exists(serial, cliloc):
    item = Engine.Items.GetItem(serial)

    if (item == None or item.Properties == None):
        return False

    for x in item.Properties:
        if x.Cliloc == cliloc:
            return True

    return False


def check_durability():
    while not Dead('self'):
        for layer in layers:
            if FindLayer(layer) and property_exists(GetAlias('found'), 1060639):
                durability = PropertyValue[int]('found', 'durability')
                Pause(500)

                if durability < minDurability:
                    HeadMsg("ATTENTION!! \"" + layer + "\": " +
                            str(durability), 'self')

        Pause(checkDelay)


check_durability()
