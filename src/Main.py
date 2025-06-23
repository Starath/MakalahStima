from collections import deque
import time
from typing import Optional, List, Tuple, Set, Dict, Any

class BFS:
    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.start = None
        self.exit = None
        self._find_start_and_exit()
        
    def _find_start_and_exit(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'S':
                    self.start = (r, c)
                elif self.grid[r][c] == 'E':
                    self.exit = (r, c)
    
    def get_neighbors(self, node: Tuple[int, int], visited: set[Tuple[int, int]]) -> list[Tuple[int, int]]:
        neighbors: list[Tuple[int, int]] = []
        r, c = node
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] != '#' and (nr, nc) not in visited:
                    neighbors.append((nr, nc))
        
        return neighbors

    def bfs_search(self) -> Tuple[Optional[List[Tuple[int, int]]], Set[Tuple[int, int]], Dict[str, Any]]:
        if not self.start or not self.exit:
            return None, set(), {'nodes_explored': 0, 'execution_time': 0}
        
        start_time = time.time()
        
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        
        while queue:
            current_node, path = queue.popleft()
            
            if current_node == self.exit:
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000  # dalam ms
                
                stats: Dict[str, Any] = {
                    'nodes_explored': len(visited),
                    'execution_time': execution_time,
                    'path_length': len(path)
                }
                
                return path, visited, stats
            
            neighbors = self.get_neighbors(current_node, visited)
            for neighbor in neighbors:
                visited.add(neighbor)
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        
        stats: Dict[str, Any] = {
            'nodes_explored': len(visited),
            'execution_time': execution_time,
            'path_length': 0
        }
        
        return None, visited, stats
