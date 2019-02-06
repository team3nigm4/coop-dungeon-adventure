# Manage every game's event


# noinspection PyTypeChecker
class EventManager:
	toActive = [[]]
	event = []

	@staticmethod
	# Define how much events there are
	def setupEvent(number):
		EventManager.event = [0] * number
		EventManager.toActive = [[]] * number

	@staticmethod
	# Add a entity the to the list of entities to call when an event is true
	def addActive(event, id):
		EventManager.toActive[event].append(id)

	@staticmethod
	def activate(event):
		EventManager.event[event] -= 1
		if EventManager.event[event] == 0:
			for i in EventManager.toActive[event]:
				from game.game.entityclass.entitymanager import EntityManager
				EntityManager.entities[i].activate()


	@staticmethod
	def deactivate(event):
		if EventManager.event[event] == 0:
			for i in EventManager.toActive[event]:
				from game.game.entityclass.entitymanager import EntityManager
				EntityManager.entities[i].deactivate()

		EventManager.event[event] += 1
