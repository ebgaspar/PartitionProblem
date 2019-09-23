import numpy as np
import random as rd


class Chromosome:
    """
        Create the chromosome based on the data size
    """

    @staticmethod
    def generate_cromossome( size ):
        l = [ ]
        for _ in range( size ):
            l.append( 1 if rd.random( ) > 0.5 else 0 )
        return l


class Individual:
    """
        Class individual
         It encapsulates the genetic functions of a specimen
         Constains the data itself (can be optimized), the generation, the fitness and the chormosome
    """

    def __init__( self , dataset , generation = 0 ):
        """
        Initialize a individual
        :param dataset: data
        :param generation: the generation of the individual
        """
        self.data = dataset
        self.generation = generation
        self.fitness = 0
        self.chromosome = Chromosome.generate_cromossome( len( dataset ) )

    def evaluate( self ):
        """
        Evaluates the fitness of the specimen
        counts the 0s and 1s and add them into variables
        :return: the absolute value of the diference between the number of 0s and 1s
        """
        c1 = 0
        c2 = 0
        size = len( self.chromosome )
        for _ in range( size ):
            if self.chromosome[ _ ] == 0:
                c1 += self.data[ _ ]
            else:
                c2 += self.data[ _ ]
        result = abs( c1 - c2 )
        self.fitness = result

    def crossover( self , other ):
        """
        Executes the crossover operation generating two new individuals.
        Exchange the first and last quarter among.
        :param other: second individual
        :return: return the children, two new individuals with mixed genes
        """
        first_cut_point = round( len( self.chromosome ) * 0.25 )
        second_cut_point = round( len( self.chromosome ) * 0.75 )

        first_son = other.chromosome[ 0:first_cut_point ] + \
                    self.chromosome[ first_cut_point:second_cut_point ] + \
                    other.chromosome[ second_cut_point:: ]

        second_son = self.chromosome[ 0:first_cut_point ] + \
                     other.chromosome[ first_cut_point:second_cut_point ] + \
                     self.chromosome[ second_cut_point:: ]

        offspring = [ Individual( self.data , self.generation + 1 ) , Individual( self.data , self.generation + 1 ) ]
        offspring[ 0 ].chromosome = first_son
        offspring[ 1 ].chromosome = second_son
        return offspring

    #
    # def func( self, factor ):
    #     if rd.random( ) < factor:
    #         if self.chromosome[ i ] == 1:
    #             self.chromosome[ i ] = 0
    #         else:
    #             self.chromosome[ i ] = 1

    def mutation( self , factor ):
        """
        Executes the mutations on the genes by randomly changing it at random based on a factor
        :param factor: the mutation factor
        :return: returns the mutated individual
        """
        for _ in range( len( self.chromosome ) ):
            if rd.random( ) < factor:
                self.chromosome[ _ ] = 1 if self.chromosome[ _ ] == 0 else 0
        return self


class Population:
    """
    Collection of individuals
    """

    def __init__( self , size ):
        """
        Initialize an individual in the population
        :param size: the size of the population
        """
        self.size = size
        self.population = [ ]
        self.best_solution = 0

    def create_population( self , dataset ):
        """
        Initialize the population create N individuals
        and sets the initial best solutions
        :param dataset: data of an individual
        :return:
        """
        for _ in range( self.size ):
            self.population.append( Individual( dataset ) )
        self.best_solution = self.population[ 0 ]

    def sort_population( self ):
        self.population = sorted( self.population ,
                                  key = lambda population: population.fitness )

    def evaluate_population( self ):
        for individual in self.population:
            individual.evaluate( )

    def select_parents( self ):
        i = rd.randint( 0 , self.size - 1 )
        j = rd.randint( 0 , self.size - 1 )
        contestant1 = self.population[ i ]
        contestant2 = self.population[ j ]
        return i if contestant1.fitness < contestant2.fitness else j

    def best_individual( self , individual ):
        if individual.fitness < self.best_solution.fitness:
            self.best_solution = individual

    def new_population( self , mutation_factor ):
        new_individuals = [ ]
        for _ in range( 0 , self.size , 2 ):
            parent1 = self.select_parents( )
            parent2 = self.select_parents( )

            offspring = self.population[ parent1 ].crossover( self.population[ parent2 ] )

            new_individuals.append( offspring[ 0 ].mutation( mutation_factor ) )
            new_individuals.append( offspring[ 1 ].mutation( mutation_factor ) )

        self.population = list( new_individuals )


def gera_dados( ):
    return np.arange( 1 , 40001 , 1 )
    # return np.random.randint( low = 1 , high = 1000001 , size = 1000000 )


def print_fitness( ):
    fitness = [ ]
    for i in pop.population:
        fitness.append( i.fitness )
    print( "Fitness: " , fitness )


def print_result( npop ):
    print( "\nGeneration: " , npop.population[ 0 ].generation )
    print( "Best fit: " , npop.best_solution.fitness )
    # print( "Chromosome: " , pop.best_solution.chromosome )
    # print( "Data: " , pop.population[ 0 ].data )


data = gera_dados( )

pop = Population( 30 )
pop.create_population( data )
pop.evaluate_population( )
pop.sort_population( )
pop.best_individual( pop.population[ 0 ] )
print_result( pop )
print_fitness( )

generations = 20
for _ in range( generations ):
    pop.new_population( 0.1 )
    pop.evaluate_population( )
    pop.sort_population( )
    pop.best_individual( pop.population[ 0 ] )
    print_result( pop )
    print_fitness( )

print( len( data ) / 4 )
print( "Fim" )
