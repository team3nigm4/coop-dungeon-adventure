# Manage every game's event


# noinspection PyTypeChecker
class EventManager:
	toActive = [[]]
	event = []

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
	def removeActive(eventIndex, id):
		if id in EventManager.toActive[eventIndex]:
			EventManager.toActive[eventIndex].remove(id)
			
		else:
			print("(EventManager - addActive()) Error want and unknown entity", eventIndex,", with id :", id)

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
