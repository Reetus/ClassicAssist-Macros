# Name: Make Last Item
# Description: Asks you how many items you would like to make using make last
# Author: Bittiez
# Shard: Ruins and Riches

res, amt = MessagePrompt("How many times would you like to make last item?", "50")

if res:
    i = 0
    while i < int(amt):
        ReplyGump(0x38920abd, 21)
        WaitForGump(0x38920abd, 10000)
        i += 1
