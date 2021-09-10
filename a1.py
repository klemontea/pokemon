from a1_support import *


def main():
	"""Initialize the game.

	Parameters:
		None

	Returns:
		None
	"""
	
	while True:																
		prompt_grid = int(input("Please input the size of the grid: "))
		if prompt_grid > 26 or prompt_grid < 2:
			print("INVALID INPUT!(Number cannot be more than 26 or less than "
				"two!)")
			continue

		prompt_pokemon = int(input("Please input the number of pokemons: "))
		if prompt_pokemon < 1 or prompt_pokemon >= prompt_grid**2:
			print("INVALID INPUT! (Number cannot be more than number of cells "
				"or less than 1!)")
			continue
		else:
			break

	pokemon_location = generate_pokemons(prompt_grid, prompt_pokemon)
	game_string = UNEXPOSED*(prompt_grid**2)
	display_game(game_string, prompt_grid)

	flag = True 	# As a condition holder for main loop below

	while flag:
		prompt_action = input("\nPlease input action: ")

		if prompt_action == 'h':		# Help input
			print(HELP_TEXT)
			display_game(game_string, prompt_grid)

		elif prompt_action == ':)':		# Restart input
			print("It's rewind time.")
			pokemon_location = generate_pokemons(prompt_grid, prompt_pokemon)
			game_string = UNEXPOSED*(prompt_grid**2)
			display_game(game_string, prompt_grid)

		elif prompt_action == 'q':		# Quit input
			final_prompt = input("You sure about that buddy? (y/n): ")

			if final_prompt == 'y':
				print("Catch you on the flip side.")
				flag = False

			elif final_prompt == 'n':
				print("Let's keep going.")
				display_game(game_string, prompt_grid)

			else:
				print(INVALID)
				display_game(game_string, prompt_grid)

		elif prompt_action[0:2] == 'f ':	# Flag input
			input_checker = parse_position(prompt_action[2:], prompt_grid)

			if input_checker:
				selected_index = position_to_index(input_checker, prompt_grid)

				if game_string[selected_index].isnumeric():
					print("INVALID INPUT! Cell has already exposed.")
					display_game(game_string, prompt_grid)
				else:
					game_string = flag_cell(game_string, selected_index)
					display_game(game_string, prompt_grid)

			else:
				print(INVALID)
				display_game(game_string, prompt_grid)

		elif prompt_action.isalnum():		# Cell selection input
			input_checker = parse_position(prompt_action, prompt_grid)

			if input_checker:
				selected_index = position_to_index(input_checker, prompt_grid)

				if game_string[selected_index] == FLAG:
					display_game(game_string, prompt_grid)

				elif selected_index in pokemon_location:
					for pokemon in pokemon_location:
						game_string = replace_character_at_index(game_string, 
									pokemon, POKEMON)

					display_game(game_string, prompt_grid)
					print("You have scared away all the pokemons.")
					flag = check_win(game_string, prompt_grid)

				else:		# Cell that has only numeric
					visible_cell = big_fun_search(game_string, prompt_grid, 
								pokemon_location, selected_index)
					game_string = replace_character_at_index(game_string, 
								selected_index, EXPOSED)

					for visible in visible_cell:
						label = str(number_at_cell(game_string, 
								pokemon_location, prompt_grid, visible))

						if game_string[visible] == FLAG:
							continue
						else:	
							game_string = replace_character_at_index(
										game_string, visible, label)

					display_game(game_string, prompt_grid)

			else:
				display_game(game_string, prompt_grid)

		else:
			print(INVALID)
			display_game(game_string, prompt_grid)

		endgame = check_win(game_string, pokemon_location)

		if endgame:
			print("You win.")
			flag = False
		else:
			continue


def display_game(game, grid_size):
	"""Print out a grid-shaped representation of the game.
	
	Display a grid-shaped representing the game for users where each element in 
	game string parameter is correspond to a particular cell index in order. 
	Each cell has a similar index with each string of game parameter in 
	ascending order.

	The first column has a title consists of capitalize alphabet (from A to Z) 
	which start from the second row while the first row has a numerical title
	(from 1 to grid_size) which start from the second column.

	Parameters:
		game (str): A string in each cell of the game
		grid_size (int): The size of the grid

	Returns:
		(str): Print out grid-shaped display
	"""

	game_list = list(game)
	# Group horizontal by one column width
	horizontal_unit = WALL_HORIZONTAL*4
	alpha_list = list(ALPHA)

	for row in range(grid_size + 1):	# Iteration by row
		if row == 0:					# First row iteration

			for col in range(grid_size + 1):	# Iteration by column
				if col == 0:
					print('  ' + WALL_VERTICAL, end = '')

				elif col == grid_size and col < 10:
					col_convert = str(col)
					print(' ' + col_convert + ' ' + WALL_VERTICAL)

				# 'col < 10' means that single digit (1 to 9) occupy one spaces 
				# while double digit (>=10) will occupy two spaces in cell

				elif col == grid_size and col >= 10:
					col_convert = str(col)
					print(' ' + col_convert + WALL_VERTICAL)

				elif col > 0 and col < grid_size and col < 10:
					col_convert = str(col)
					print(' ' + col_convert + ' ' + WALL_VERTICAL, end = '')

				else:
					col_convert = str(col)
					print(' ' + col_convert + WALL_VERTICAL, end = '')

			print(horizontal_unit * (grid_size + 1))

		else:		# Second row and after
			for col in range(grid_size + 1):	# Iteration by column

				if col == 0:
					alpha_extract = alpha_list.pop(0)
					print(alpha_extract + ' ' + WALL_VERTICAL, end = '')

				elif col == grid_size:
					game_extract = game_list.pop(0)
					print(' ' + game_extract + ' ' + WALL_VERTICAL)

				else:
					game_extract = game_list.pop(0)
					print(' ' + game_extract + ' ' + WALL_VERTICAL, end = '')

			print(horizontal_unit * (grid_size + 1))


def parse_position(action, grid_size):
	"""Verify the input format when a cell is chosen.

	Check if the input satisfy a particular format by using iterable to the 
	action parameter. The iterable check if the character in action parameter is 
	an alphabet and add it to alpha variable or num variable if it is a numeric. 

	Both alpha and num variable are checked again each with different 
	conditional statement. Alpha checker to avoid two alphabet occur side by 
	side and num checker to limit maximum number. Each True condition then add 
	the element to result tuple.

	Parameters:
		action (str): Input from user
		grid_size (int): The size of the grid

	Results:
		(tuple<int>): Coordinate of selected cell
	"""

	action_list = list(action)
	alpha = []
	num = ''
	result = ()

	for element in action_list:
		if element.isalpha():
			alpha.append(element)
		elif element.isnumeric():
			num += element
		else:
			continue

	if num:
		num = int(num)
	else:
		return None

	if len(alpha) == 1:		# Alpha checker
		if alpha[0] in ALPHA:
			result += (ALPHA.index(alpha[0]),)
		else:
			return None

	else:
		return None

	if num <= grid_size:	# Numeric checker
		result += (num-1,)
	else:
		return None

	return result


def position_to_index(position, grid_size):
	"""Convert row and column of the cell into index.

	Convert cell coordinate (column and row) in position parameter into index 
	using some calculations that depend on the grid size.

	Parameters:
		position (tuple<int>): Cell coordinate (column, row)
		grid_size (int): The size of the grid

	Returns:
		(int): Index of the cell from coordinate conversion
	"""

	index = 0

	if position[0] == 0:
		index = position[1]

	else:
		index = position[1] + (grid_size * position[0])

	return index


def replace_character_at_index(game, index, character):
	"""Produce an updated game string after a cell is replaced by other 
	character.

	The game parameter is turned into list to be mutable. Then, a cell is 
	selected using list slicing and change with some character symbols.

	The modified game is returned as a string.

	Parameters:
		game (str): A string in each cell of the game
		index (int): Cell whose context will be replaced by another symbol
		character (str): A symbol that will be input into selected index

	Returns:
		(str): A new updated game string
	"""

	game = list(game)
	game[index] = character

	return ''.join(game)


def flag_cell(game, index):
	"""Produce an updated game string after the flag is put or revoked on 
	specific cell.

	The game parameter is turned into list so it is mutable. If a selected cell 
	already has a FLAG symbol ('♥') in it then it is revoked and replaced with 
	an UNEXPOSED symbol ('~'). Otherwise, the FLAG symbol is put in it.

	The updated game string is turned again into string and returned.

	Parameters:
		game (str): A string in each cell of the game
		index (int): A cell which will be put FLAG or its FLAG revoked

	Returns:
		(str): A new updated game string
	"""

	game = list(game)

	if game[index] == FLAG:
		game[index] = UNEXPOSED
	else:
		game[index] = FLAG
					
	return ''.join(game)


def index_in_direction(index, grid_size, direction):
	"""Find neighbour index adjacent to the subject cell in a particular 
	direction.

	Search neighbour cells in specific direction adjacent to the cell and return 
	its index if there is one. It will not return index in some directions if 
	the subject cell is located on the edges of grid.

	Parameters:
		index (int): A cell position/index which is a subject to its 
					neighbouring cells
		grid_size (int): The size of the grid
		direction (str): Direction from the subject cell where the neighbour 
						will be searched

	Returns:
		(int): Neighbour index adjacent to subject cell in specific direction
	"""

	if direction == DIRECTIONS[0] and index >= grid_size:
		index -= grid_size
		return index

	elif direction == DIRECTIONS[1] and index < (grid_size**2 - grid_size):
		index += grid_size
		return index

	elif direction == DIRECTIONS[2] and index % grid_size != 0:
		index -= 1
		return index

	elif direction == DIRECTIONS[3] and (index + 1) % grid_size != 0:
		index += 1
		return index

	elif direction == DIRECTIONS[4] and (index >= grid_size) and (
					index % grid_size != 0):
		index -= grid_size+1
		return index

	elif direction == DIRECTIONS[5] and (index >= grid_size) and (
					(index + 1) % grid_size != 0):
		index -= grid_size-1
		return index

	elif direction == DIRECTIONS[6] and ((index < (grid_size**2 - grid_size)) 
					and (index % grid_size != 0)):
		index += grid_size - 1
		return index

	elif direction == DIRECTIONS[7] and ((index < (grid_size**2 - grid_size)) 
					and ((index + 1) % grid_size != 0)):
		index += grid_size + 1
		return index

	return None


def neighbour_directions(index, grid_size):
	"""Find all neighbour cells around a particular cell.
	
	Search neighbour cells, extract its index, and store it in neighbour_index. 
	The function use another method, index_in_direction, to search neighbour 
	cells. It will return neighbour index except for cells at the edges of the 
	grid because they don't have all possible directions.

	The index will be checked for each possible direction around it and assigned 
	to neighbour_list if it has neighbour cell. If not, then it will be ignored 
	and go to the next iteration.

	Parameters:
		index (int): A cell position/index which is a subject to its 
					neighbouring cells
		grid_size (int): The size of the grid

	Returns:
		(list<int>): List of neighbour indexes
	"""

	neighbour_list = []

	for direction in DIRECTIONS:
		neighbour_index = index_in_direction(index, grid_size, direction)
		
		if neighbour_index == None:
			continue
		else:
			neighbour_list.append(neighbour_index)

	return neighbour_list


def number_at_cell(game, pokemon_locations, grid_size, index):
	"""Gives the number of pokemon in neighbouring cells.

	It uses another function called neighbour_directions to search neighbour 
	cell in every directions around a particular cell or index and store them 
	to list_of_neighbour variable. Each time a pokemon is found in 
	list_of_neighbour, it will be counted as one toward total_pokemon until 
	there is no longer neighbour in the list.

	Parameters:
		game (str): A string in each cell of the game
		pokemon_locations (tuple<int>): Tuple that show all pokemon location 
										indexes
		grid_size (int): The size of the grid
		index (int): A cell position/index which is a subject to its 
					neighbouring cells

	Returns:
		(int): Total number of pokemon around the cell
	"""

	total_pokemon = 0
	list_of_neighbour = neighbour_directions(index, grid_size)

	for pokemon in pokemon_locations:
		if pokemon in list_of_neighbour:
			total_pokemon += 1

	return total_pokemon


def check_win(game, pokemon_locations):
	"""Check for win or lose condition of the game.

	Game is declared as win if all cells are exposed except the cell with the 
	pokemon inside and all pokemon cells are flagged. It will return True as a 
	result.

	Game is declared as lose or in progress if either a pokemon is exposed or 
	there is a cell that has not been exposed. It will return False as a result.

	The function will check every elements in game string if they satisfy 
	certain conditions to be True. It is True if the element is exposed and show 
	a number and it is not a pokemon and if the element has pokemon then it is 
	flagged. Each True will be counted toward count_true variable as one. A 
	False value will be ignored and not counted.

	The function will return True if the number in total_cell equal to 
	count_true or False otherwise. Also, False will be returned immediately
	whenever a pokemon cell is exposed.

	Parameters:
		game (str): Game string
		pokemon_locations (int): A tuple consisting of all indexes which are 
							representation of pokemon locations for each index

	Returns:
		(bool): True if win or False if lose
	"""

	total_cell = len(game)
	count_true = 0			# As a comparison variable with total_cell

	for cell in game:		# Filter cell with numeric and pokemon element
		if cell.isnumeric():
			count_true += 1
		elif cell == POKEMON:
			return False
		else:
			continue

	for index in pokemon_locations:		# Filter pokemon cell with flag element
		if game[index] == FLAG:
			count_true += 1

	if total_cell == count_true:
		return True

	return False


def big_fun_search(game, grid_size, pokemon_locations, index):
	"""Searching adjacent cells to see if there are any Pokemon"s present.

	Using some sick algorithms.

	Find all cells which should be revealed when a cell is selected.

	For cells which have a zero value (i.e. no neighbouring pokemons) all the 
	cell"s neighbours are revealed. If one of the neighbouring cells is also 
	zero then all of that cell"s neighbours are also revealed. This repeats 
	until no zero value neighbours exist.

	For cells which have a non-zero value (i.e. cells with neightbour pokemons), 
	only the cell itself is revealed.

	Parameters:
		game (str): Game string.
		grid_size (int): Size of game.
		pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
		index (int): Index of the currently selected cell

	Returns:
		(list<int>): List of cells to turn visible.
	"""

	queue = [index]
	discovered = [index]
	visible = []

	if game[index] == FLAG:
		return queue

	number = number_at_cell(game, pokemon_locations, grid_size, index)
	if number != 0:
		return queue

	while queue:
		node = queue.pop()
		for neighbour in neighbour_directions(node, grid_size):
			if neighbour in discovered or neighbour is None:
				continue

			discovered.append(neighbour)
			if game[neighbour] != FLAG:
				number = number_at_cell(game, pokemon_locations, grid_size, 
					neighbour)
				if number == 0:
					queue.append(neighbour)
			visible.append(neighbour)
	return visible


if __name__ == "__main__":
    main()
