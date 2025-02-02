import random
class ServerSystem:
    def __init__(self, num_servers=5):
        self.servers = {f"Server {i+1}": random.choice(['Underloaded', 'Balanced', 'Overloaded']) for i in range(num_servers)}
    def display_load_status(self, message):
        print(f"{message}:")
        for server, load in self.servers.items():
            print(f"{server}: {load}")
    def get_overloaded_servers(self):
        return [server for server, load in self.servers.items() if load == 'Overloaded']
    def get_underloaded_servers(self):
        return [server for server, load in self.servers.items() if load == 'Underloaded']
    def balance_load(self):
        overloaded_servers = self.get_overloaded_servers()
        underloaded_servers = self.get_underloaded_servers()
        for overloaded in overloaded_servers:
            if underloaded_servers:
                underloaded = underloaded_servers.pop(0)
                self.servers[overloaded] = 'Balanced'
                self.servers[underloaded] = 'Balanced'
                print(f"Moved tasks from {overloaded} to {underloaded}.")
            else:
                print(f"No underloaded servers available to balance {overloaded}.")
class LoadBalancerAgent:
    def __init__(self, system):
        self.system = system
    def scan_and_balance(self):
        print("Scanning the system for load imbalances.")
        self.system.balance_load()
def load_balancing_simulation():
    system = ServerSystem()
    system.display_load_status("Initial Load Status")
    agent = LoadBalancerAgent(system)
    agent.scan_and_balance()
    system.display_load_status("Updated Load Status")
load_balancing_simulation()
