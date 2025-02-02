import random
class BackupSystem:
    def __init__(self, num_tasks=10):
        self.tasks = [{'id': i + 1, 'status': random.choice(['Completed', 'Failed'])} for i in range(num_tasks)]
    def display_task_statuses(self, message):
        print(f"{message}:")
        for task in self.tasks:
            print(f"Task {task['id']}: {task['status']}")
    def get_failed_tasks(self):
        return [task for task in self.tasks if task['status'] == 'Failed']
    def retry_failed_tasks(self):
        failed_tasks = self.get_failed_tasks()
        for task in failed_tasks:
            if random.random() < 0.7:
                task['status'] = 'Completed'
                print(f"Task {task['id']} retry: Success")
            else:
                print(f"Task {task['id']} retry: Failed again")
class BackupManagementAgent:
    def __init__(self, system):
        self.system = system
    def scan_and_retry(self):
        print("Scanning for failed backup tasks.")
        self.system.retry_failed_tasks()
def backup_management_simulation():
    system = BackupSystem()
    system.display_task_statuses("Initial Task Statuses")
    agent = BackupManagementAgent(system)
    agent.scan_and_retry()
    system.display_task_statuses("Updated Task Statuses")
backup_management_simulation()
