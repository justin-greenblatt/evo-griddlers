from Griddler import Griddler

GRIDDLER_DIRECTORY = "hurracain.txt"
GRIDDLER = Griddler(GRIDDLER_DIRECTORY)
GENERATIONS = 5
POP_SIZE = 25
POPULATIONS = 2
POPULATIONS_X = 5
MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.5
NO_MATCH_PENALTY = 7
MAX_LEVENSHTEIN_DIST_REWARD = 5
MIGRATION_RATE = 0.005
GENOME_PCT_FOR_CROSSOVER = 0.4
MAX_LEVENSHTEIN_DIST_SUBS = 5


RESOLVER_GENOME_PCT_FOR_CROSSOVER = 0.5
RESOLVER_POPULATION_SIZE = 10
RESOLVER_POPULATIONS = 1
RESOLVER_MIGRATION_RATE = 0
RESOLVER_HOST_SWAP_RATE = 0.05
RESOLVER_MUTATION_RATE = 0.2
RESOLVER_CROSSOVER_PCT = 0.5

LANGUAGE = ['0', '1']
RESOLVER_COLORS = ["\u2592\u2592","\u2593\u2593"]
COLORS = ["\u2588\u2588","\u2591\u2591","\u2592\u2592","\u2593\u2593","  "]
FLAG_COLORS = (chr(0x1f7e9),chr(0x1f7e5))


PARAM_DICT = {"resolverCrossoverPct"  : RESOLVER_GENOME_PCT_FOR_CROSSOVER,
              "resolverMigrationRate" : RESOLVER_MIGRATION_RATE,
              "resolverPopulations": RESOLVER_POPULATIONS,
              "resolverPopulationSize" : RESOLVER_POPULATION_SIZE,
              "resolverMutationRate" : RESOLVER_MUTATION_RATE,
              "resolverCrossover" : RESOLVER_CROSSOVER_PCT,
              "resolverHostSwap" : RESOLVER_HOST_SWAP_RATE,
              "griddler" : GRIDDLER,
              "populationSize": POP_SIZE,
              "populationsX": POPULATIONS_X,
              "language": LANGUAGE,
              "colors": COLORS,
              "flagColors" : FLAG_COLORS,
              "mutationRate": MUTATION_RATE,
              "crossOverRate": CROSSOVER_RATE,
              "generations": GENERATIONS,
              "noMatchPenalty": NO_MATCH_PENALTY,
              "rows": GRIDDLER.size[0],
              "cols": GRIDDLER.size[1],
              "migrationRate" : MIGRATION_RATE ,
              "populations" : POPULATIONS,
              "maxSubs" : MAX_LEVENSHTEIN_DIST_SUBS,
              "crossoverPct" : GENOME_PCT_FOR_CROSSOVER,
              "rowRules" : GRIDDLER.rows,
              "colRules" : GRIDDLER.cols,
              "resolverMutationRate" : RESOLVER_MUTATION_RATE,
              "resolverColors": RESOLVER_COLORS
              }