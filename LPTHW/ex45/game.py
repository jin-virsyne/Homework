from sys import path
path.append("/")
from scene import Map

class Engine(object):
    
    stage_limit = 3
    
    def __init__(self, scene_map):
        self.scene_map = scene_map
        
    def play(self, difficulty=stage_limit):
        current_scene = self.scene_map.opening_scene()
        final_scene = self.scene_map.ending_scene()
        stage_number = 0
        
        # safety check to not prolong the game stages
        if difficulty > Engine.stage_limit:
            difficulty = Engine.stage_limit
        
        while stage_number < difficulty:
            result = current_scene.enter()
            current_scene = self.scene_map.next_scene(result)
            stage_number += 1
        
        # to trigger the final scene   
        final_scene.enter()
        
a_map = Map()
a_game = Engine(a_map)
a_game.play()