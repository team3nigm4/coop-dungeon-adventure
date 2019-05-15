# Static class to manage every game's event

from game.util.logger import Logger
from game.game.entityclass import entitymanager

# noinspection PyTypeChecker
class EventManager:
	# Functioning:
	# Each entity when their state is deactivate add one to the event and remove one when they are activated	<- activator entity
	# When the sum of the event pass from 0 to 1, all of entity linked to the event is deactivate				<- activated entity
	# When the sum of the event pass from 1 to 0, all of entity linked to the event is activate					<- activated entity

	toActive = [[]]
	event = []
	wantRemove = []
	init = True

	@staticmethod
	# Define how much events there are
	def setupEvent(number):
		EventManager.init = True
		EventManager.event = [0] * number
		EventManager.toActive = [[] for i in range(number)]

	# During the init, entities should not be activate
	# After the init, this method check avery event state to activate or deactivate entity
	@staticmethod
	def endInit():
		EventManager.init = False
		for i in range(len(EventManager.event)):
			if EventManager.event[i] == 0:
				EventManager.activeAllEntities(i)
			else:
				EventManager.deactiveAllEntities(i)

	# Add entity to the list of entities to call when an event is true
	@staticmethod
	def addActive(eventIndex, entityId):
		if not entityId in EventManager.toActive[eventIndex]:
			EventManager.toActive[eventIndex].append(entityId)
		else:
			Logger.error("EvManager", "Tow entities have the same ID " + str(eventIndex) + ", with id : " + str(entityId.id))

	# Remove entity from a list
	@staticmethod
	def rem(eventIndex, entityId):
		if entityId in EventManager.toActive[eventIndex]:
			EventManager.toActive[eventIndex].remove(entityId)
		else:
			Logger.error("EvManager", "Unknown entity " + str(eventIndex) + ", with id : " + str(entityId.id))

	# Entity should not be removed during the loop, so class register that
	@staticmethod
	def remove(eventIndex, entityId):
		if entityId in EventManager.toActive[eventIndex]:
			EventManager.wantRemove.append([entityId, eventIndex])

	# After the loop remove entity which want to be removed from a list
	@staticmethod
	def dispose():
		if not EventManager.wantRemove == []:
			for i in EventManager.wantRemove:
				EventManager.toActive[i[1]].remove(i[0])
			EventManager.wantRemove = []

	@staticmethod
	def activate(eventIndex):
		EventManager.event[eventIndex] -= 1
		# Security
		if EventManager.event[eventIndex] == 0 and not EventManager.init:
			EventManager.activeAllEntities(eventIndex)

	@staticmethod
	def activeAllEntities(eventIndex):
		for i in EventManager.toActive[eventIndex]:
			entitymanager.EntityManager.entities[i.id].activate()

	@staticmethod
	def deactivate(eventIndex):
		# Security
		if EventManager.event[eventIndex] == 0 and not EventManager.init:
			EventManager.deactiveAllEntities(eventIndex)
		EventManager.event[eventIndex] += 1

	@staticmethod
	def deactiveAllEntities(eventIndex):
		for i in EventManager.toActive[eventIndex]:
			entitymanager.EntityManager.entities[i.id].deactivate()
