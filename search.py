# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    # python pacman.py -l tinyMaze -p SearchAgent
    # python pacman.py -l mediumMaze -z .7 -p SearchAgent
    # python pacman.py -l bigMaze -z .5 -p SearchAgent
    # python pacman.py -l openMaze -z .8 -p SearchAgent
    """criacao da pilha"""
    pilha = util.Stack()
    'Array que contem todos os nos explorados pelo pacman'
    nosVisitados = []
    'Colocando a cordenada inicial na pilha'
    pilha.push((problem.getStartState(), []))
    while not pilha.isEmpty():
        """
        Recebe tudo que foi excluido da pilha
        Uma cordenada e um comando
        """
        pacman = pilha.pop()
        coordenada = pacman[0]
        sequenciaPassos = pacman[1]

        'Verifica se a cordenada atual e o destino'
        'Se for retorna a sequencia de passos'
        if problem.isGoalState(coordenada):
            return sequenciaPassos

        if coordenada not in nosVisitados:
            nosVisitados.append(coordenada)

            for aux in problem.getSuccessors(coordenada):
                if aux[0] not in nosVisitados:
                    pilha.push((aux[0], (sequenciaPassos + [aux[1]])))
    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    # python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
    # python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
    # python pacman.py -l openMaze -z .8 -p SearchAgent -a fn=bfs
    """
    Mesmo funcionamento do codigo anterior so que utilizando uma lista
    """
    fila = util.Queue()
    nosVisitados = []
    fila.push((problem.getStartState(), []))

    while not fila.isEmpty():
        pacman = fila.pop()
        coordenada = pacman[0]
        sequenciaPassos = pacman[1]

        if problem.isGoalState(coordenada):
            return sequenciaPassos
        if coordenada not in nosVisitados:
            nosVisitados.append(coordenada)
            for aux in problem.getSuccessors(coordenada):
                if aux[0] not in nosVisitados:
                    fila.push((aux[0], (sequenciaPassos + [aux[1]])))
    # util.raiseNotDefined()



def uniformCostSearch(problem):
  "*** YOUR CODE HERE ***"
  """A busca por custo uniforme utiliza a funcao PriorityQueue para auxiliar nossa busca"""
  fila = util.PriorityQueue()
  nosExplorados = []
  """Nessa busca e necessario adicionar o custo, o custo inicial e zero"""
  fila.push((problem.getStartState(), []), 0)

  while not fila.isEmpty():
      pacman = fila.pop()
      coordenada = pacman[0]
      sequenciaPassos = pacman[1]

      if problem.isGoalState(coordenada):
          return sequenciaPassos

      if coordenada not in nosExplorados:
          nosExplorados.append(coordenada)
          for aux in problem.getSuccessors(coordenada):
              """A diferenca entre esse codigo e os outros dois acima esta no custo...
              O custo e calculado pela funcao problem.getCostOfActions, que eh o tamanho 
              de sequenciaPassos... poderia ser len(sequenciaPassos)... 
              eh importante lembrar que no pop... o retorno e do menor custo da fila...
              E assim que funciona o heapq.heappop"""
              if aux[0] not in nosExplorados:
                  """Calculando o custo uniforme dos estados anteriores + estado atual"""
                  custo = problem.getCostOfActions(sequenciaPassos + [aux[1]])
                  fila.push((aux[0], sequenciaPassos + [aux[1]]), custo)
  #util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    # python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
    # python pacman.py -l openMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

    """Mesmo funcionamento da busca anterior so que e acresentado o custo heuristico"""
    fila = util.PriorityQueue()
    nosVisitados = []
    fila.push((problem.getStartState(), []), 0)

    while not fila.isEmpty():
        pacman = fila.pop()
        coordenada = pacman[0]
        sequenciaPassos = pacman[1]

        if problem.isGoalState(coordenada):
            # print sequenciaPassos
            return sequenciaPassos
        if coordenada not in nosVisitados:
            nosVisitados.append(coordenada)
            for aux in problem.getSuccessors(coordenada):
                if aux[0] not in nosVisitados:
                    custoUniforme = problem.getCostOfActions(sequenciaPassos + [aux[1]])
                    custoHeuristico = heuristic(aux[0], problem)
                    custo = custoUniforme + custoHeuristico
                    fila.push((aux[0], sequenciaPassos + [aux[1]]), custo)
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch