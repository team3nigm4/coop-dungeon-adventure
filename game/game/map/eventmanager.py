# Manage every game's event


# noinspection PyTypeChecker
class EventManager:
	toActive = [[]]
	event = []
	wantRemove = []

	@staticmethod
	# Define how much events there are
	def setupEvent(number):
		EventManager.event = [0] * number
		EventManager.toActive = [[] for i in range(number)]

	@staticmethod
	# Add a entity the to the list of entities to call when an event is true
	def addActive(eventIndex, id):
		if not id in EventManager.toActive[eventIndex]:
			EventManager.toActive[eventIndex].append(id)
		else:
			print("(EventManager - addActive()) Error two entities with same id want to be place on table", eventIndex,", with id :", id)

	@staticmethod
	def rem(eventIndex, id):
		if id in EventManager.toActive[eventIndex]:
			EventManager.toActive[eventIndex].remove(id)
		else:
			print("(EventManager - addActive()) Error want and unknown entity", eventIndex,", with id :", id)

	@staticmethod
	def remove(eventIndex, id):
		if id in EventManager.toActive[eventIndex]:
			EventManager.wantRemove.append([id, eventIndex])

	@staticmethod
	def dispose():
		if not EventManager.wantRemove == []:
			for i in EventManager.wantRemove:
				EventManager.toActive[i[1]].remove(i[0])
			EventManager.wantRemove = []

	@staticmethod
	def activate(eventIndex):
		EventManager.event[eventIndex] -= 1
		if EventManager.event[eventIndex] == 0:
			from game.game.entityclass.entitymanager import EntityManager
			for i in EventManager.toActive[eventIndex]:
				EntityManager.entities[i].activate()

	@staticmethod
	def deactivate(eventIndex):
		if EventManager.event[eventIndex] == 0:
			from game.game.entityclass.entitymanager import EntityManager
			for i in EventManager.toActive[eventIndex]:
				EntityManager.entities[i].deactivate()
		
		EventManager.event[eventIndex] += 1
