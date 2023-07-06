from sys import exit
from random import choice, randint
from textwrap import dedent

class Scene(object):
    
    input_str = "Number Choice >> "
    
    def enter(self):
        print("Scene not implemented.")
        exit(1)
        
        
class Death(Scene):
    
    quips = [
        "You died. You kinda suck at this.",
        "Your Mom would be proud...if she were smarter.",
        "Such a luser.",
        "I have a small puppy that's better at this.",
        "You're worse than your Dad's jokes."
    ]
    
    def enter(self):
        print(Death.quips[randint(0, len(self.quips)-1)])
        exit(1)
        
        
    
class TheBeginning(Scene):
    
    def enter(self):
        print(dedent("""
                     You woke up in a mysterious misty forest.
                     It looked ominous, and you felt the need to get out
                     of here immediately. You see two path in front of you,
                     which would you go?
                     
                     [1] - The darker path
                     [2] - The brighter path
                     """))
        
        action = input(Scene.input_str)
        
        if action == "1":
            print(dedent("""
                     You met a unicorn on your way.
                     That seems like a good sign!
                     """))
            return "the_beginning"
        else:
            print(dedent("""
                     A shadow crept behind you and slashed you into half!
                     """))
            return "death"

class TheEnd(Scene):
    
    def enter(self):
        print("You escaped the forest! Good job.")
        return 'the_end'
    
        
class LakeScene(Scene):
    
    def enter(self):
        print(dedent("""
                     You found a large lake! You're feeling very thirsty
                     suddenly, as though the lake is calling for you.
                     Should you be drinking the water?
                     
                     [1] - Drink
                     [2] - Don't drink
                     """))
        
        action = input(Scene.input_str)
        
        if action == "1":
            print(dedent("""
                     You felt super refreshed after drinking the lake water!
                     You heard a voice coming from your further right, and you
                     traced its direction.
                     """))
            return "lake"
        else:
            print(dedent("""
                     You left without drinking the water. You got lost in the
                     forest and eventually died from thirst.
                     """))
            return "death"
        
        
class CaveScene(Scene):
    
    def enter(self):
        print(dedent("""
                     It started raining suddenly. You ran and entered a cave for
                     shelter. There's hissing sound coming from inside...
                     
                     [1] - Exit the cave immediately
                     [2] - Stay in the cave regardless
                     """))
        
        action = input(Scene.input_str)
        
        if action == "2":
            print(dedent("""
                     You decided to rest inside. Being so exchausted,
                     you even fell asleep. By the time you woke up, the rain 
                     stopped and you're on your way once more.
                     """))
            return "cave"
        else:
            print(dedent("""
                     You exited the cave, fearing for your safety. Unfortunately,
                     a lightning flashed and struck you! 
                     """))
            return "death"


class TreeScene(Scene):
    def enter(self):
        print(dedent("""
                     You saw an abnormally large tree bearing golden fruits.
                     They looked tasty! Should you climb and pick one to try?
                     
                     [1] - Yes
                     [2] - No
                     """))
        
        action = input(Scene.input_str)
        
        if action == "2":
            print(dedent("""
                     Your mouth drooled but you shook your head, telling yourself
                     they could be poisonous. You moved on, hoping to find the exit.
                     """))
            return "tree"
        else:
            print(dedent("""
                     You climbed the tree. A flock of monkeys, their eyes beaming red,
                     glared at you. Protective of their home, they shred you apart!
                     """))
            return "death"


class DeerScene(Scene):
    def enter(self):
        print(dedent("""
                     A baby deer walked towards you slowly. It looked so adorable!
                     It seems hungry though. There's a berry bush nearby, should you
                     feed it?
                     
                     [1] - Pet its head instead
                     [2] - Feed it berries
                     """))
        
        action = input(Scene.input_str)
        
        if action == "1":
            print(dedent("""
                     It closed its eyes while being pet by you. Grateful for the
                     affection, it led you towards a hidden path.
                     """))
            return "deer"
        else:
            print(dedent("""
                     As you try to feed it, the deer evolved into a monster and
                     ate you alive. 
                     """))
            return "death"  


class Map(object):
    
    scenes = {
        'lake': LakeScene(),
        'cave': CaveScene(),
        'tree': TreeScene(),
        'deer': DeerScene(),
        'death': Death(),
        'the_beginning': TheBeginning(),
        'the_end': TheEnd()
    }
    
    scene_filter = ['death', 'the_beginning', 'the_end']
    
    def __init__(self):
        self.start_scene = "the_beginning"
        self.end_scene = "the_end"

        
    def next_scene(self, result, initial=False):
        scene_name = result

        if result != 'death' and result != 'the_end' and not initial:
            while scene_name in Map.scene_filter or scene_name == result:
                scene_name = choice(list(Map.scenes.keys()))

        val = Map.scenes.get(scene_name)
        return val
    
    def opening_scene(self):
        return self.next_scene(self.start_scene, True)
    
    def ending_scene(self):
        return self.next_scene(self.end_scene)