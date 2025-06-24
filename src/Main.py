import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque
import numpy as np
import time
import os
import tracemalloc 
import logging     
from typing import Optional, List, Tuple, Set, Dict, Any


class BFS:
    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.start = None
        self._find_start()
        
    def _find_start(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'S':
                    self.start = (r, c)
    
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
        if not self.start:
            return None, set(), {}
        
        tracemalloc.start()
        start_time = time.time()
        
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        
        max_queue_size = 1
        total_branching_factor = 0
        nodes_with_neighbors = 0
        
        while queue:
            max_queue_size = max(max_queue_size, len(queue))
            
            current_node, path = queue.popleft()
            
            # cek apakah sudah sampai exit 'E'
            if self.grid[current_node[0]][current_node[1]] == 'E':
                end_time = time.time()
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                execution_time = (end_time - start_time) * 1000  # dalam ms
                avg_branching_factor = total_branching_factor / nodes_with_neighbors if nodes_with_neighbors > 0 else 0

                stats: Dict[str, Any] = {
                    'nodes_explored': len(visited),
                    'execution_time': execution_time,
                    'path_length': len(path),
                    'peak_memory_kb': peak / 1024, # konversi ke KB
                    'max_queue_size': max_queue_size,
                    'avg_branching_factor': avg_branching_factor
                }
                
                return path, visited, stats
            
            neighbors = self.get_neighbors(current_node, visited)
            
            if len(neighbors) > 0:
                total_branching_factor += len(neighbors)
                nodes_with_neighbors += 1

            for neighbor in neighbors:
                visited.add(neighbor)
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
        
        end_time = time.time()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        execution_time = (end_time - start_time) * 1000
        avg_branching_factor = total_branching_factor / nodes_with_neighbors if nodes_with_neighbors > 0 else 0

        stats: Dict[str, Any] = {
            'nodes_explored': len(visited),
            'execution_time': execution_time,
            'path_length': 0,
            'peak_memory_kb': peak / 1024,
            'max_queue_size': max_queue_size,
            'avg_branching_factor': avg_branching_factor
        }
        
        return None, visited, stats

class Visualizer:
    def __init__(self):
        self.colors = {
            '#': 'darkblue',      # Dinding
            '.': 'white',         # Jalur kosong
            'S': 'darkgreen',     # Start
            'E': 'red',           # Exit
            'visited': 'yellow',  # Node yang dikunjungi
            'path': 'lightblue'   # Jalur terpendek
        }
    
    def visualize_result(self, grid: list[list[str]], path: Optional[List[Tuple[int, int]]], visited: Set[Tuple[int, int]], title: str = "BFS Pathfinding Result"):
        rows, cols = len(grid), len(grid[0])
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        for r in range(rows):
            for c in range(cols):
                color = self.colors.get(grid[r][c], 'white')
                if (r, c) in visited and grid[r][c] not in ['S', 'E']:
                    color = self.colors['visited']
                if path and (r, c) in path and grid[r][c] not in ['S', 'E']:
                    color = self.colors['path']
                rect = patches.Rectangle((c, rows-1-r), 1, 1, linewidth=0.5, edgecolor='gray', facecolor=color)
                ax.add_patch(rect)
        
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        
        legend_elements = [
            patches.Patch(facecolor=self.colors['#'], label='Dinding', edgecolor='black'),
            patches.Patch(facecolor=self.colors['.'], label='Jalur Kosong', edgecolor='black'),
            patches.Patch(facecolor=self.colors['S'], label='Start', edgecolor='black'),
            patches.Patch(facecolor=self.colors['E'], label='Exit', edgecolor='black'),
            patches.Patch(facecolor=self.colors['visited'], label='Node Dikunjungi', edgecolor='black'),
            patches.Patch(facecolor=self.colors['path'], label='Jalur Terpendek', edgecolor='black')
        ]
        ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        return fig

def create_scenario_grids():
    scenario1: list[list[str]] = []
    size = 25
    for r in range(size):
        row: list[str] = []
        for c in range(size):
            if r == 0 or r == size-1 or c == 0 or c == size-1:
                row.append('#')
            else:
                row.append('.')
        scenario1.append(row)
    obstacles = [(5, 8), (6, 8), (7, 8), (15, 12), (16, 12), (17, 12)]
    for r, c in obstacles:
        if 0 < r < size-1 and 0 < c < size-1:
            scenario1[r][c] = '#'
    scenario1[2][2] = 'S'
    scenario1[size-3][size-3] = 'E'
    
    scenario2_str = """
#########################
#S....#.................#
#.###.#.#############.#.#
#.....#.............#.#.#
#.#####.###########.#.#.#
#.#...#.#.........#.#.#.#
#.#.#.#.#.#######.#.#.#.#
#.#.#.#.#.......#.#.#.#.#
#.#.#.#.#######.#.#.#.#.#
#.#.#.#.........#.#.#.#.#
#.#.#.###########.#.#.#.#
#.#.#.............#.#.#.#
#.#.#################.#.#
#.#...................#.#
#.#####################.#
#.......................#
#######################E#
#########################
    """.strip()
    scenario2 = [list(line) for line in scenario2_str.split('\n')]
    
    scenario3_str = """
#########################
#S......................#
#.##...##...##...##..#..#
#.##...##...##...##..#..#
#....................#..#
#.##...##...##...##..#..#
#.##...##...##...##..#..#
#....................#..#
#.##...##...##...##..#..#
#.##...##...##...##..#..#
#....................#..#
#.##...##...##...##..#..#
#.##...##...##...##..#..#
#....................#..#
#.##...##...##...##..#..#
#.##...##...##...##..#..#
#....................#..#
#.##...##...##...##..#..#
#.##...##...##...##..#..#
#....................##.#
#.....................#E#
#########################
    """.strip()
    scenario3 = [list(line) for line in scenario3_str.split('\n')]
    
    return scenario1, scenario2, scenario3

def run_simulation():
    scenarios = create_scenario_grids()
    scenario_names = [
        "Skenario 1: Denah Ruang Terbuka",
        "Skenario 2: Denah Labirin Kompleks", 
        "Skenario 3: Denah Jalur Menyesatkan"
    ]
    
    visualizer = Visualizer()
    results: List[Dict[str, Any]] = []
    
    print("=" * 60)
    print("MEMULAI SIMULASI BFS PATHFINDING PADA DENAH PAMERan")
    print("=" * 60)
    
    for i, (grid, name) in enumerate(zip(scenarios, scenario_names)):
        print(f"\nMenjalankan: {name}")
        
        pathfinder = BFS(grid)
        path, visited, stats = pathfinder.bfs_search()
        
        result: Dict[str, Any] = {
            'scenario': name,
            'grid_size': f"{len(grid)}x{len(grid[0])}",
            'path_length': stats.get('path_length', 0),
            'nodes_explored': stats.get('nodes_explored', 0),
            'execution_time': stats.get('execution_time', 0),
            'path_found': path is not None,
            'peak_memory_kb': stats.get('peak_memory_kb', 0),
            'max_queue_size': stats.get('max_queue_size', 0),
            'avg_branching_factor': stats.get('avg_branching_factor', 0)
        }
        results.append(result)
        
        if path:
            print(f"  Jalur ditemukan!")
            print(f"  Panjang jalur: {stats['path_length']} langkah")
            print(f"  Node dieksplorasi: {stats['nodes_explored']}")
            print(f"  Waktu eksekusi: {stats['execution_time']:.2f} ms")
            print(f"  Memori puncak: {stats['peak_memory_kb']:.2f} KB")
            print(f"  Ukuran antrian maks: {stats['max_queue_size']}")
            print(f"  Branching factor rata-rata: {stats['avg_branching_factor']:.2f}")

        else:
            logging.warning(f"  Tidak ada jalur yang ditemukan")
        
        fig = visualizer.visualize_result(grid, path, visited, name)
        filename = f"scenario_{i+1}_result.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"  Visualisasi disimpan: {filename}")
        
        plt.show()
        
    
    print("\n" + "=" * 120)
    print("TABEL PERBANDINGAN KINERJA BFS")
    print("=" * 120)
    header = f"{'Skenario':<25} {'Ukuran':<10} {'P. Jalur':<10} {'Node Eksplor.':<15} {'Waktu (ms)':<12} {'Memori (KB)':<12} {'Max Queue':<10} {'Avg B-Factor':<15}"
    print(header)
    print("-" * 120)
    
    for res in results:
        scenario_short = res['scenario'].split(':')[0]
        row = (f"{scenario_short:<25} {res['grid_size']:<10} {res['path_length']:<10} "
               f"{res['nodes_explored']:<15} {res['execution_time']:<12.2f} "
               f"{res['peak_memory_kb']:<12.2f} {res['max_queue_size']:<10} "
               f"{res['avg_branching_factor']:<15.2f}")
        print(row)
    return results

def save_grid_to_file(grid: List[List[str]], filename: str):
    with open(filename, 'w') as f:
        for row in grid:
            f.write(''.join(row) + '\n')

def load_grid_from_file(filename: str):
    grid: List[List[str]]= []
    try:
        with open(filename, 'r') as f:
            for line in f:
                grid.append(list(line.strip()))
        return grid
    except FileNotFoundError:
        logging.error(f"File {filename} tidak ditemukan")
        return None

def main():
    print("BFS Pathfinding Simulator")
    print("Simulasi Pencarian Jalan Keluar Terpendek pada Denah Pameran menggunakan Breadth-First Search (BFS)")
    
    while True:
        print("\nPilihan:")
        print("1. Jalankan simulasi lengkap (3 skenario)")
        print("2. Load grid dari file")
        print("3. Simpan grid skenario ke file")
        print("4. Keluar")
        
        choice = input("\nPilih opsi (1-4): ").strip()
        
        if choice == '1':
            run_simulation()
        elif choice == '2':
            filename = input("Masukkan nama file: ").strip()
            grid = load_grid_from_file(filename)
            if grid:
                pathfinder = BFS(grid)
                path, visited, stats = pathfinder.bfs_search()
                if path:
                    print(f"Jalur ditemukan dengan panjang {stats['path_length']} langkah")
                    print(f"  Jalur ditemukan!")
                    print(f"  Panjang jalur: {stats['path_length']} langkah")
                    print(f"  Node dieksplorasi: {stats['nodes_explored']}")
                    print(f"  Waktu eksekusi: {stats['execution_time']:.2f} ms")
                    print(f"  Memori puncak: {stats['peak_memory_kb']:.2f} KB")
                    print(f"  Ukuran antrian maks: {stats['max_queue_size']}")
                    print(f"  Branching factor rata-rata: {stats['avg_branching_factor']:.2f}")
                else:
                    logging.warning(f"  Tidak ada jalur yang ditemukan")
                visualizer = Visualizer()
                fig = visualizer.visualize_result(grid, path, visited, f"Custom Grid: {filename}")
                output_dir = "test"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                base_name = os.path.basename(filename)
                file_stem = os.path.splitext(base_name)[0]

                savefile = os.path.join(output_dir, f"scenario_{file_stem}.png")
                
                print(f"  Menyimpan visualisasi ke: {savefile}")
                plt.savefig(savefile, dpi=300, bbox_inches='tight')
                print(f"  Visualisasi berhasil disimpan.")
                plt.show()
        elif choice == '3':
            scenarios = create_scenario_grids()
            scenario_names = ["scenario1.txt", "scenario2.txt", "scenario3.txt"]
            for grid, filename in zip(scenarios, scenario_names):
                save_grid_to_file(grid, filename)
                print(f"Grid disimpan ke {filename}")
        elif choice == '4':
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
