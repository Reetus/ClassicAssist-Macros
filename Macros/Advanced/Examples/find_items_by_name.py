# Name: Find Items By Name
# Description: Find all items within a container containing the given text in it's name
# Author: Reetus
# Era: Any

from Assistant import Engine

def FindItemsByName(name, container):
	items = []
	
	cont = Engine.Items.GetItem(container)
	
	if cont == None:
		print 'Cannot find container'
		return
		
	if cont.Container == None:
		WaitForContents(container, 5000)
		
	for item in cont.Container.GetItems():
		if item.Name.ToLower().Contains(name.ToLower()):
			items.append(item.Serial)	
	
	return items
	
print FindItemsByName('Mythical', 0x418caa10)
