import heapq
import itertools

class PriorityQueue:
    def __init__(self):
        self.pq = []  # min-heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = '<removed-task>'  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def add_task(self, task, priority=0):
        """Add a new task or update the priority of an existing task."""
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task):
        """Mark an existing task as REMOVED."""
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        """Remove and return the lowest priority task."""
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def change_priority(self, task, priority):
        """Change the priority of an existing task."""
        self.add_task(task, priority)

    def __str__(self):
        # Only show valid tasks (exclude removed ones)
        return str([entry for entry in self.pq if entry[-1] != self.REMOVED])

def test_priority_queue():
    pq = PriorityQueue()

    # Adicionando tarefas com diferentes prioridades
    pq.add_task("task1", 2)
    pq.add_task("task2", 1)
    pq.add_task("task3", 5)
    print("After adding tasks:", pq)

    # Inserindo novas tarefas
    pq.add_task("task4", 3)
    print("After adding task4:", pq)

    # Removendo a tarefa com menor prioridade
    pq.pop_task()
    print("After removing task with lowest priority:", pq)

    # Alterando a prioridade de uma tarefa
    pq.change_priority("task4", 0)
    print("After changing priority of task4:", pq)

    # Removendo novamente
    pq.pop_task()
    print("After removing another task:", pq)

test_priority_queue()
