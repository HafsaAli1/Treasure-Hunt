import random
from collections import deque

# Initialises game with grid, treasure, powerups, traps
class TreasureHunt:
    def __init__(self, size=5, traps=2, powerups=2):
        self.size = size
        self.traps = traps
        self.powerups = powerups
        self.grid = []
        self.players = []
        self.treasure = None
        self.turn_index = 0
        self.create_grid()

# Initialises grid with treasure, powerups, traps
    def create_grid(self):
        self.grid = [["-" for _ in range(self.size)] for _ in range(self.size)]
# Randomly place treasure
        self.treasure = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        self.grid[self.treasure[0]][self.treasure[1]] = "T"

# Place traps and  power-ups
        def items(item, count):
            for _ in range(count):
                while True:
                    x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                    if self.grid[x][y] == "-":
                        self.grid[x][y] = item
                        break

        items("X", self.traps)
        items("P", self.powerups)

# Add 2 players to the game
    def addPlayer(self, name, start_x, start_y):
        if 0 <= start_x < self.size and 0 <= start_y < self.size:
            self.players.append({"name": name, "position": (start_x, start_y), "health": 100})
        else:
            print("Invalid position.")

# Allows players to move in different directions
    def movePlayer(self, player_index, direction):
        if not (0 <= player_index < len(self.players)):
            return "Invalid move."

        player = self.players[player_index]
        x, y = player["position"]
        direction_map = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

        if direction not in direction_map:
            return "Invalid direction."

        dx, dy = direction_map[direction]
        new_position = (x + dx, y + dy)

        if 0 <= new_position[0] < self.size and 0 <= new_position[1] < self.size:
            player["position"] = new_position
            self.effect(player)
        else:
            return "Try again."

# Tells you what happened depending on what cell you have landed on
    def effect(self, player):
        x, y = player["position"]
        cell = self.grid[x][y]

        if cell == "T":
            print(f"{player['name']} found the treasure! They win!")
            exit()
        elif cell == "X":
            player["health"] -= 20
            print(f"{player['name']} stepped on a trap! Health level: {player['health']}.")
            if player["health"] <= 0:
                print(f"{player['name']} is eliminated.")
                self.players.remove(player)
        elif cell == "P":
            player["health"] += 10
            print(f"{player['name']} collected a power-up! Health level: {player['health']}.")
            self.grid[x][y] = "-"

# Shows players position on grid
    def displayGrid(self):
        display = [row[:] for row in self.grid]
        for idx, player in enumerate(self.players):
            x, y = player["position"]
            display[x][y] = f"P{idx + 1}"
        for row in display:
            print(" ".join(row))

# Moves onto second players turnn
    def nextPlayer(self):
        self.turn_index = (self.turn_index + 1) % len(self.players)

# Performs binary search on the rows
    def binary(self, row, start, end, target):
        while start <= end:
            mid = (start + end) // 2
            if self.grid[row][mid] == target:
                return mid
            elif target < self.grid[row][mid]:
                end = mid - 1
            else:
                start = mid + 1
        return -1

# Performs BFS (Breadth-First Search) to find the shortest path to the treasure.
    def bfs(self, start):
        queue = deque([start])
        visited = set()
        parent_map = {}

        while queue:
            current = queue.popleft()
            if current in visited:
                continue

            visited.add(current)
            x, y = current

            if self.grid[x][y] == "T":
                path = []
                while current in parent_map:
                    path.append(current)
                    current = parent_map[current]
                path.reverse()
                return path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    parent_map[(nx, ny)] = current

        return []

# Performs DFS to explore paths to the treasure
    def dfs(self, current, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []

        x, y = current
        if self.grid[x][y] == "T":
            path.append(current)
            return path

        visited.add(current)
        path.append(current)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                result = self.dfs((nx, ny), visited, path)
                if result:
                    return result

        path.pop()
        return []

# Starts the game loop
    def play(self):
        while self.players:
            self.displayGrid()
            player = self.players[self.turn_index]
            print(f"{player['name']}'s turn. Current health: {player['health']}.")
            print("Choose an action:")
            print("1. Move (up/down/left/right)")
            print("2. Use BFS to find treasure")
            print("3. Use DFS to explore")
            print("4. Use Binary Search on a row")

            action = input("Enter action number: ").strip()
            if action == "1":
                direction = input("Enter direction (up/down/left/right): ").strip()
                self.movePlayer(self.turn_index, direction)
            elif action == "2":
                path = self.bfs(player["position"])
                print("Path to treasure:", path)
            elif action == "3":
                path = self.dfs(player["position"])
                print("Path to treasure:", path)
            elif action == "4":
                row = int(input("Enter row to search: "))
                target = input("Enter target: ")
                result = self.binary(row, 0, self.size - 1, target)
                if result != -1:
                    print(f"Target found at column {result}")
                else:
                    print("Target not found.")
            else:
                print("Invalid action.")

            self.nextPlayer()


# Runs the game
game = TreasureHunt()
game.addPlayer("Player 1", 0, 0)
game.addPlayer("Player 2", 4, 4)
game.play()

