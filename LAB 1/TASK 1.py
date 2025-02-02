import random
class Sys:
    def __init__(self, comps):
        self.comps = comps
        self.state = {comp: random.choice(['safe', 'vulnerable']) for comp in comps}
    def show_state(self, msg):
        print(f"{msg}:")
        for comp, status in self.state.items():
            print(f"Comp {comp}: {status}")
    def vuln_comps(self):
        return [comp for comp, status in self.state.items() if status == 'vulnerable']
    def patch(self, comp):
        self.state[comp] = 'safe'
        print(f"PATCHED: Comp {comp} is now safe.")
class Agent:
    def __init__(self, name):
        self.name = name

    def scan(self, sys):
        print(f"{self.name} is scanning the system.")
        vuln = sys.vuln_comps()
        for comp in sys.state:
            if comp in vuln:
                print(f"WARNING: Comp {comp} is vulnerable!")
            else:
                print(f"SUCCESS: Comp {comp} is secure.")
        return vuln

    def patch_system(self, sys, vuln):
        if vuln:
            print(f"{self.name} is patching...")
            for comp in vuln:
                sys.patch(comp)
        else:
            print("No vulnerabilities found. System is secure.")
def run_simulation():
    comps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    sys = Sys(comps)
    agent = Agent("Agent X")

    sys.show_state("Initial System State")
    vuln_comps = agent.scan(sys)
    agent.patch_system(sys, vuln_comps)
    sys.show_state("Final System State")
run_simulation()
