import domain as dom
import state as st
import os
from heapq import heappush
from heapq import heappop
import time

import cProfile, pstats, StringIO

def a_star_solve(initial_state):

	heap = []

	heappush(heap,initial_state)
	visited_states = {tuple(initial_state.state):True}

	i = 0
	new_states_inserted = 0
	lowest_dist = float('inf')
	deepest = 0
	while heap:# and i < 1000 :

		#Get the state with the lowest cost from the heap
		possible_solution = heappop(heap)

		if possible_solution.estimated_dist_to_goal < lowest_dist:
			lowest_dist = possible_solution.estimated_dist_to_goal
		if possible_solution.depth > deepest:
			deepest = possible_solution.depth

		print 'Visited:',i,' len queue:',len(heap),' depth:',possible_solution.depth,deepest,\
		' New states:',new_states_inserted,' State cost: ',possible_solution.cost,\
		' Dist goal: ',possible_solution.estimated_dist_to_goal,lowest_dist#,len(possible_solution.state)

		if possible_solution.is_goal_state():
			print '\n\n----------Solution found!---------------\n'
			print 'The goal state is:\n',possible_solution.state
			print '\nLength of solution: ',len(possible_solution.actions)
			print '\nThe solution is: '
			for action in possible_solution.actions:
				print action

			return


		else:
			possible_solution.create_child_states()
			new_states = possible_solution.get_child_states()
			new_states_inserted = 0
			for new_state in new_states:

				#check if the state already has been visited using hash table
				if not tuple(new_state.state) in visited_states:
					new_state.set_state_cost()
					#Add the new state to visited states
					visited_states[tuple(new_state.state)] = True
					new_states_inserted = new_states_inserted + 1

					#Add the new state to the queue using a heap sorted based on
					#the state cost
					heappush(heap,new_state)



		i = i + 1


	print '---NOT SOLVABLE---'
	print 'Nodes visited = ',i


def main():

	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = dir_path[:-3]

	debug = False
	# debug = True



	#satellite problem.
	# domain_file_name = dir_path+'probs/satellite/domain.pddl'
	# problem_file_name = dir_path+'probs/satellite/problem01.pddl'
	#
	# #
	# #Block world problem quick enough
	# problem_file_name = dir_path+'probs/blocks/problem.pddl'
	# domain_file_name = dir_path+'probs/blocks/domain.pddl'
	#
	#
	# # # #aircargo problem
	# problem_file_name = dir_path+'probs/aircargo/problem.pddl'
	# domain_file_name = dir_path+'probs/aircargo/domain.pddl'
	#
	#
	# # # #
	# problem_file_name = dir_path+'probs/shakey/problem1.pddl'
	# domain_file_name = dir_path+'probs/shakey/domain.pddl'
	# # # #
 	# # # # # #Rover
	problem_file_name = dir_path+'probs/rover/problem.pddl'
	domain_file_name = dir_path+'probs/rover/domain.pddl'


	domain_file = open(domain_file_name,'r')
	problem_file = open(problem_file_name,'r')

	try:
		domain = dom.Domain(domain_file)
		init_state = st.State(domainclass = domain,problem_file=problem_file)

		start_time = time.time()

		profiling = False
		# profiling = True
		if profiling:
			pr = cProfile.Profile()
			pr.enable()

		a_star_solve(init_state)

		if profiling:
			pr.disable()
			s = StringIO.StringIO()
			sortby = 'cumulative'
			ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
			ps.print_stats()
			print s.getvalue()



		print("--- %s seconds ---" % (time.time() - start_time))


		if debug:
			print "\n\nDomain name: ",domain.domain_name
			for predicate in domain.predicates:
				print "\n------------------------------"
				print "Predicate name: ",predicate.name
				print "Predicate params: ",predicate.parameters
				print "------------------------------\n"

			for action in domain.actions:
				print "\n\n------Action name: ",action.name,"-------------"
				print "Parameters:", action.parameters
				for precondition in action.preconditions:
					print "------------------------------"
					print "Precondition name: ",precondition.name
					print "Precondition param: ",precondition.parameters
					print "------------------------------\n"
				for effect in action.effects:
					print "------------------------------"
					print "Effect name: ",effect.name
					print "Effect params: ", effect.parameters
					print "------------------------------\n"
				for delete_effect in action.delete_effects:
					print "------------------------------"
					print "Delete effect name: ",delete_effect.name
					print "Delete effect params: ", delete_effect.parameters
					print "------------------------------\n"

			print '\n----------Objects-----------------'
			for obj in init_state.objects:
				print obj
			print '\n-------INIT STATE-----------'
			for state in init_state.state:
				print state

			print '\n-------Goal-----------'
			for goal in init_state.goal:
				print goal

	except ValueError as err:
		print '------------------'
		for arg in err.args:
			print arg
		print '------------------'

	domain_file.close()
	problem_file.close()

if __name__=='__main__':
	main()

#https://github.com/primaryobjects/strips/tree/master/strips
#Fix naar action bare har en effect. Det blir rart
