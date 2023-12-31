from gothonweb.planisphere import *

def test_room():
    gold = Room("GoldRoom",
                """This room has gold in it you can grab. There's a
                door to the north.""")
    assert gold.name == "GoldRoom"
    assert gold.paths == {}
    
def test_room_paths():
    center = Room("Center", "Test room in the center.")
    north = Room("North", "Test room in the north.")
    south = Room("South", "Test room in the south.")
    
    center.add_paths({'north': north, 'south': south})
    assert center.go('north') == north
    assert center.go('south') == south
    
def test_map():
    start = Room("Start", "You can do west and down a hole.")
    west = Room("Trees", "There are trees here, you can go east")
    down = Room("Dungeon", "It's dark down here, you can go up.")
    
    start.add_paths({'west': west, 'down': down})
    west.add_paths({'east': start})
    down.add_paths({'up': start})
    
    assert start.go('west') == west
    assert start.go('west').go('east') == start
    assert start.go('down').go('up') == start
    
def test_gothon_game_map():
    start_room = load_room(START)
    assert start_room.go('shoot!') == central_corridor_shoot
    assert start_room.go('dodge!') == central_corridor_dodge
    
    room = start_room.go('tell a joke')
    assert room == laser_weapon_armory
    assert room.go('*') == laser_weapon_armory_lock
    
    room = room.go('0132')
    assert room == the_bridge
    assert room.go('throw the bomb') == the_bridge_throw
    
    room = room.go('slowly place the bomb')
    assert room == escape_pod
    assert room.go('*') == the_end_loser
    
    room = room.go('2')
    assert room == the_end_winner
    