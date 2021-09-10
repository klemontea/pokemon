# Pokemon: Gotta Find Them All!
A text-based pokemon game which resembles Minesweeper game

## Introduction
Pokemon: Gotta Find Them All! is a single-player puzzle game where the goal is for the player to find all the Pokemon using 'flag' without scaring them away by stepping on them (click). This program is developed using Python language. This is one of my school projects, and some codes are already provided by school. However, almost 90% of contents in a1.py (main files) are my works. The other files such as a1_support.py, test_a1.py, and testrunner.py are provided by school to support and test the code so it could works fine. 

## How to Play
The objectives of this game is to find all pokemon locations (or bomb in Minesweeper) by put a flag on them. You have to execute a1.py in order to run this program. The other files are support and testing file.

Below is a list of valid actions:  
| Input | Action | Example |
------|--------|---------- |
| '-Upper Case Character--number-'| Select a cell | 'A1' |
| 'f -Upper Case Character--number-' | Place/remove a flag | 'f A1' |
| 'h' | Help text | 'h' |
| 'q' | Quit | 'q' |
| ':)' | Restart | ':)' |

If, say, 'C4' is entered, then the cell at position, C4, should be uncovered to reveal a number that indicates how many Pokemon are hidden in the neighbouring cells. If no Pokemon are present in any neighbouring cells then the number 0 should be displayed. For cells which have a zero value (i.e. no neighbouring pokemons) all the cell's neighbours are uncovered (i.e. they are made to display the number of pokemons in neighbouring cells). If one of those neighbouring cells is also zero then all of that cell's neighbours are also uncovered. This process repeats until there are no more 0's uncovered.  

If, say, 'f B1' is entered, then a flag will be placed on the cell at position, B1, provided there is no flag currently on that cell. Alternatively, if there is a flag on that cell, the flag will be removed.  

If you fail to flag the pokemon, and instead click on them (reveal), then game over. 
