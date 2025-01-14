import pygame
import App
import Graph
import multiprocessing

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
    app = App.App(screen)
    graph = Graph.Graph()
    processes = []
    process = multiprocessing.Process(target=graph.start_graph_thread)
    processes.append(process)
    process.start()
    app.run()
    graph.stop_graph_thread()