import heapq
layout = {
    "Storage": {"Corr1": 1},
    "Corr1": {"Storage": 1, "R101": 2, "NurseStat": 3},
    "R101": {"Corr1": 2},
    "NurseStat": {"Corr1": 3, "R205": 4},
    "R205": {"NurseStat": 4},
}
schedule = {
    "R101": {"time": "10:00 AM", "med": "Med A"},
    "R205": {"time": "11:00 AM", "med": "Med B"},
}
storage = {
    "Med A": 5,
    "Med B": 3,
}
def find_path(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path = path + [node]
            if node == end:
                return path
            for neighbor, weight in graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path))
    return None
class Robot:
    def __init__(self, layout, schedule, storage):
        self.layout = layout
        self.schedule = schedule
        self.storage = storage
        self.loc = "Storage"
        self.tasks = []
    def add_task(self, room, time, med):
        self.tasks.append({"room": room, "time": time, "med": med})
    def prioritize(self):
        self.tasks.sort(key=lambda x: x["time"])
    def pick_med(self, med):
        if self.storage.get(med, 0) > 0:
            self.storage[med] -= 1
            print(f"Picked up {med} from storage.")
            return True
        else:
            print(f"Error: {med} is out of stock.")
            return False
    def deliver_med(self, room, med):
        print(f"Delivering {med} to {room}.")
        print(f"Scanning patient ID in {room}.")
        print(f"Medicine {med} delivered to {room}.")
    def alert(self, msg):
        print(f"Alerting staff: {msg}")
    def execute(self):
        self.prioritize()
        for task in self.tasks:
            room = task["room"]
            med = task["med"]
            time = task["time"]
            print(f"\nProcessing task: Deliver {med} to {room} at {time}.")
            if self.loc != "Storage":
                path = find_path(self.layout, self.loc, "Storage")
                if path:
                    print(f"Moving from {self.loc} to Storage via {path}.")
                    self.loc = "Storage"
                else:
                    print("Error: Cannot reach Storage.")
                    continue
            if not self.pick_med(med):
                self.alert(f"{med} is out of stock. Please restock.")
                continue
            path = find_path(self.layout, self.loc, room)
            if path:
                print(f"Moving from {self.loc} to {room} via {path}.")
                self.loc = room
            else:
                print(f"Error: Cannot reach {room}.")
                continue
            self.deliver_med(room, med)
        print("\nAll tasks completed.")
if __name__ == "__main__":
    robot = Robot(layout, schedule, storage)
    for room, details in schedule.items():
        robot.add_task(room, details["time"], details["med"])
    robot.execute()
