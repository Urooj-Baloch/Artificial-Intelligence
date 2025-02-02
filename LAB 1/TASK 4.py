import random
class System:
    def __init__(self):
        self.c = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        self.s = {comp: random.choice(['Safe', 'Low Risk Vulnerable', 'High Risk Vulnerable']) for comp in self.c}
    def display_state(self, msg):
        print(f"{msg}:")
        for comp, st in self.s.items():
            print(f"Comp {comp}: {st}")
    def get_vulns(self):
        return {comp: st for comp, st in self.s.items() if st != 'Safe'}
    def patch_low_risk(self):
        for comp, st in self.s.items():
            if st == 'Low Risk Vulnerable':
                self.s[comp] = 'Safe'
                print(f"PATCHED: Comp {comp} (Low Risk Vulnerable) has been patched.")
class Agent:
    def __init__(self, system):
        self.system = system
    def scan(self):
        print("Scanning the system for vulnerabilities.")
        for comp, st in self.system.s.items():
            if st == 'Safe':
                print(f"SUCCESS: Comp {comp} is safe.")
            else:
                print(f"WARNING: Comp {comp} is {st}.")
    def patch(self):
        print("Patching vulnerabilities...")
        self.system.patch_low_risk()
        for comp, st in self.system.s.items():
            if st == 'High Risk Vulnerable':
                print(f"ALERT: Comp {comp} (High Risk Vulnerable) requires premium service to patch.")
def run_security_simulation():
    system = System()
    system.display_state("Initial System State")
    agent = Agent(system)
    agent.scan()
    agent.patch()
    system.display_state("Final System State")
run_security_simulation()