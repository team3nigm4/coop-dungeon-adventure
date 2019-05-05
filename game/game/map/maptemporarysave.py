from game.game.map.maploading import MapLoading as ml
from game.game.map import mapmanager as mam
from game.game.map.eventmanager import EventManager as ev
from game.game.entityclass import entitymanager as em
from game.game.map.maprender import MapRender as mr
from game.game.entityclass import loadentity


class MapTemporarySave:
	DATA_MAP_INFO = 0
	DATA_INTERACTIONS = 1
	DATA_ENTRIES = 2
	DATA_ENTITIES = 3
	DATA_MAP_DISPLAY = 4
	DATA_TILESET = 5

	zone = "Null"
	mapNumbers = 0
	currentMap = "None"
	oldMap = ""

	mapsName = []
	mapsLoad = {}

	# Event manager
	toActive_instances = {}
	event_instances = {}

	# Entity Manager
	entities_instances = {}
	entitiesCol_instances = {}
	displayLayer_instances = {}

	# Map Manager
	entryPos_instances = {}
	interaction_instances = {}
	defaultEntry_instances = {}

	# Map Render
	currentTileSet_instances = {}
	mapValues_instances = {}
	tilesPosition_instances = {}
	vbo_instances = {}
	ebo_instances = {}
	vboCount_instances = {}
	eboCount_instances = {}

	@staticmethod
	def newZone(zone):
		mts = MapTemporarySave

		import os
		path = "game/resources/map/" + zone + "/"
		files = os.listdir(path)
		for name in files:
			if name[-5:] == ".json":
				MapTemporarySave.unloadAll()

				name = name[0:-5]
				mts.mapNumbers += 1
				mts.mapsName.append(name)
				mts.mapsLoad[name] = False

				# Event manager
				mts.toActive_instances[name] = [[]]
				mts.event_instances[name] = []

				# Entity Manager
				mts.entities_instances[name] = []
				mts.entitiesCol_instances[name] = []
				mts.displayLayer_instances[name] = [[], [], [], []]

				# Map Manager
				mts.entryPos_instances[name] = []
				mts.interaction_instances[name] = [[]]
				mts.defaultEntry_instances[name] = 0

				# Map Render
				mts.currentTileSet_instances[name] = "tuto"
				mts.mapValues_instances[name] = []
				mts.tilesPosition_instances[name] = []
				mts.vbo_instances[name] = []
				mts.ebo_instances[name] = []
				mts.vboCount_instances[name] = []
				mts.eboCount_instances[name] = []

		mts.zone = zone
		mts.currentMap = "Null"

	@staticmethod
	def changeRoom(map, entry, reset=False):
		mts = MapTemporarySave
		mts.oldMap = mts.currentMap
		mts.currentMap = map

		if reset:
			mts.unload(map, True)
			loadentity.LoadEntity.setReset(True)

		if not mts.oldMap == "Null" and not reset:
			MapTemporarySave.saveValue(mts.oldMap)

		# Load the current Map
		if not mts.mapsLoad[map]:

			# Init the values of map
			mts.mapsLoad[map] = True

			values = ml.loadMap(mts.zone, map)

			ev.setupEvent(values[MapTemporarySave.DATA_MAP_INFO][1])

			if not reset:
				em.EntityManager.clear()
			else:
				em.EntityManager.checkId()

			mts.defaultEntry_instances[map] = values[MapTemporarySave.DATA_MAP_INFO][0]
			mts.entryPos_instances[map] = values[MapTemporarySave.DATA_ENTRIES]
			mam.MapManager.setupMapValues(values[MapTemporarySave.DATA_INTERACTIONS],
										  mts.defaultEntry_instances[map],
										  mts.entryPos_instances[map][str(mts.defaultEntry_instances[map])])

			mr.mapValues = values[MapTemporarySave.DATA_MAP_DISPLAY]
			mr.currentTileSet = values[MapTemporarySave.DATA_TILESET]
			mts.currentTileSet_instances[map] = values[MapTemporarySave.DATA_TILESET]
			mr.constructMap()
			for i in range(0, len(values[MapTemporarySave.DATA_ENTITIES])):
				args = values[MapTemporarySave.DATA_ENTITIES][i][1]
				args.insert(0, (values[MapTemporarySave.DATA_ENTITIES][i][0]))
				em.EntityManager.addA(args)

			ev.endInit()
			#
			MapTemporarySave.saveValue(map)
			loadentity.LoadEntity.setReset(False)

		# Apply all data to managers
		em.EntityManager.setValues(mts.entities_instances[map], mts.entitiesCol_instances[map],
								   mts.displayLayer_instances[map])
		em.EntityManager.checkId()

		mam.MapManager.setupMapValues(mts.interaction_instances[map],
									  mts.defaultEntry_instances[map],
									  mts.entryPos_instances[map][str(entry)])

		mr.setMapValues(mts.vbo_instances[map], mts.ebo_instances[map], mts.mapValues_instances[map],
						mts.tilesPosition_instances[map], mts.vboCount_instances[map], mts.eboCount_instances[map],
						mts.currentTileSet_instances[map])

		ev.event = mts.event_instances[map]
		ev.toActive = mts.toActive_instances[map]

		if reset:
			em.EntityManager.entityEffectAfterReset()

	@staticmethod
	def saveValue(map):
		mts = MapTemporarySave
		# Save values
		# Entity manager
		mts.entities_instances[map] = em.EntityManager.entities
		mts.entitiesCol_instances[map] = em.EntityManager.entitiesCol
		mts.displayLayer_instances[map] = em.EntityManager.displayLayer

		# Event manager
		mts.event_instances[map] = ev.event
		mts.toActive_instances[map] = ev.toActive

		# Map manager
		mts.interaction_instances[map] = mam.MapManager.interaction

		# Map render
		mts.currentTileSet_instances[map] = mr.currentTileSet
		mts.vbo_instances[map] = mr.vbo
		mts.ebo_instances[map] = mr.ebo
		mts.mapValues_instances[map] = mr.mapValues
		mts.tilesPosition_instances[map] = mr.tilesPosition
		mts.vboCount_instances[map] = mr.vboCount
		mts.eboCount_instances[map] = mr.eboCount

	@staticmethod
	def unload(map, reset=False):
		mts = MapTemporarySave

		if mts.mapsLoad[map]:
			mts.mapsLoad[map] = False
			em.EntityManager.setValues(mts.entities_instances[map], mts.entitiesCol_instances[map],
									   mts.displayLayer_instances[map])
			em.EntityManager.discharge(reset)

	@staticmethod
	def unloadAll():
		for e in MapTemporarySave.mapsName:
			MapTemporarySave.unload(e)
