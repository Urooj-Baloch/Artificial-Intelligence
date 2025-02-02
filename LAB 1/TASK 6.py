class FirefightingRobot:
    def __init__(self):
        self.rooms = {
            'a': 'safe', 'b': 'safe', 'c': 'fire', 'd': 'safe', 'e': 'fire'
        }
        self.path = ['a', 'b', 'c', 'd', 'e']
    def display_grid(self):
        for room in self.rooms:
            status = ' ' if self.rooms[room] == 'safe' else '🔥'
            print(f"Room {room.upper()}: {status}")
    def move(self):
        for room in self.path:
            print(f"Moving to Room {room.upper()}.")
            if self.rooms[room] == 'fire':
                print(f"Fire detected in Room {room.upper()}. Extinguishing fire.")
                self.rooms[room] = 'safe'
            self.display_grid()
robot = FirefightingRobot()
robot.move()