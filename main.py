import math
import networkx as nx
import cv2

d_val = math.sqrt(2)


def check_if_white(image, i, j):
    return len(image[1]) > i >= 0 and len(image) > j >= 0 and image[j][i][0] == 255


def add_edges(image, i, j):
    edges = list()
    neighbours = [(i, j + 1), (i, j - 1), (i - 1, j), (i + 1, j)]
    for n in neighbours:
        if check_if_white(image, n[0], n[1]):
            edges.append(((i, j), (n[0], n[1]), 1.0))
    return edges


def add_edges_diagonal(image, i, j):
    edges = add_edges(image, i, j)
    neighbours = [(i + 1, j + 1), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1)]
    for n in neighbours:
        if check_if_white(image, n[0], n[1]):
            edges.append(((i, j), (n[0], n[1]), 1.0))
    return edges


def euclides(a1, a2):
    return math.sqrt(math.pow((a1[0] - a2[0]), 2) + math.pow((a1[1] - a2[1]), 2))


def solve_maze(input_file, output_file, start, end, diagonal=True):
    image = cv2.imread(input_file)
    gray_image = cv2.cvtColor(image, cv2.IMREAD_GRAYSCALE)
    (thresh, bw_image) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    col, rows = bw_image.shape[1], bw_image.shape[0]
    cv2.imwrite(output_file, bw_image)
    edges = list()
    for i in range(0, rows):
        for j in range(0, col):
            if check_if_white(bw_image, i, j):
                if diagonal:
                    edges += add_edges_diagonal(bw_image, i, j)
                else:
                    edges += add_edges(bw_image, i, j)
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    path = nx.astar_path(G, start, end, heuristic=euclides)
    output_image = cv2.cvtColor(image, cv2.IMREAD_COLOR)
    for coords in path:
        cv2.circle(output_image, coords, 1, (255, 0, 0), -1)
    cv2.imwrite(output_file, output_image)


if __name__ == '__main__':
    # diagonal
    solve_maze("maze.png", "solved_maze_diagonal.png", (270, 15), (368, 519))
    # no-diagonal
    solve_maze("maze.png", "solved_maze_no_diagonal.png", (270, 15), (368, 519), diagonal=False)
    # diagonal maze2
    solve_maze("maze2.png", "solved_maze_2.png", (5, 5), (362, 362))
