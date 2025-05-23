import pytest
import numpy as np
import matplotlib.pyplot as plt
from structural import Room, FloorPlan, WallType
from MEP import AirHandlingUnit
import routing as routing
from core import Point
from visualization import save_figure, visualize_layout

@pytest.fixture(autouse=True)
def mpl_test_settings():
	import matplotlib
	matplotlib.use('TkAgg')
	plt.ion()
	yield
	plt.close('all')

class TestFourRooms:
	@pytest.fixture
	def four_room_floor_plan(self):
		"""Create a 2x2 grid of rooms with outer walls and an AHU."""
		floor_plan = FloorPlan()
		rooms = []
		
		# Bottom-left room
		room = Room([Point(0, 0), Point(5, 0), Point(5, 5), Point(0, 5)])
		room.walls[0].wallType = WallType.OUTER_WALL  # Bottom wall
		room.walls[3].wallType = WallType.OUTER_WALL  # Left wall
		rooms.append(room)
		
		# Bottom-right room
		room = Room([Point(5, 0), Point(10, 0), Point(10, 5), Point(5, 5)])
		room.walls[0].wallType = WallType.OUTER_WALL  # Bottom wall
		room.walls[1].wallType = WallType.OUTER_WALL  # Right wall
		rooms.append(room)
		
		# Top-left room
		room = Room([Point(0, 5), Point(5, 5), Point(5, 10), Point(0, 10)])
		room.walls[2].wallType = WallType.OUTER_WALL  # Top wall
		room.walls[3].wallType = WallType.OUTER_WALL  # Left wall
		rooms.append(room)
		
		# Top-right room
		room = Room([Point(5, 5), Point(10, 5), Point(10, 10), Point(5, 10)])
		room.walls[1].wallType = WallType.OUTER_WALL  # Right wall
		room.walls[2].wallType = WallType.OUTER_WALL  # Top wall
		rooms.append(room)
		
		floor_plan.add_rooms(rooms)
		floor_plan.ahu = AirHandlingUnit(Point(2.5, 2.5))  # AHU in bottom-left room
		return floor_plan

class Test11Rooms:
	def test_complex_rooms(self,complex_floor_plan_fixture):
		floorPlan = complex_floor_plan_fixture
		start = floorPlan.ahu.position
		cm = 1/2.54  # centimeters in inches
		fig, ax = plt.subplots(figsize=(20*cm, 20*cm))
		visualize_layout(floorPlan, ax)
		network = routing.Network(floorPlan, start, ax)
		network.generate()
		save_figure(ax, "integration_test_11-room-layout")
		assert(isinstance(network.mainBranch, routing.Branch2D))
		assert(isinstance(network.branches, list))
		assert isinstance(ax, plt.Axes)
		assert isinstance(fig, plt.Figure)
		plt.show(block=True)

	def test_complex_rooms_with_concrete_walls(self,room_plan_11_rooms_random_concrete_fixture):
		floorPlan = room_plan_11_rooms_random_concrete_fixture
		assert isinstance(floorPlan, FloorPlan)
		start = floorPlan.ahu.position
		cm = 1/2.54  # centimeters in inches
		fig, ax = plt.subplots(figsize=(20*cm, 20*cm))
		visualize_layout(floorPlan, ax)
		network = routing.Network(floorPlan, start, ax)
		network.generate()
		save_figure(ax, "First concrete wall attempt")
		assert(isinstance(network.mainBranch, routing.Branch2D))
		assert(isinstance(network.branches, list))
		assert isinstance(ax, plt.Axes)
		assert isinstance(fig, plt.Figure)
		plt.show(block=True)
