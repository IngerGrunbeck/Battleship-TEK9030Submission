# -*- coding: utf-8 -*-
"""
Created on Tue May 18 2021

@author: Inger Grünbeck (inger.gruenbeck@gmail.com)
Project: TEK9030 - Implementing Battleship
"""
import copy
from grid_read import Grid
import random
import matplotlib.pyplot as plt


def computer_grid(coordinates, ships):
    temp_coor = copy.deepcopy(coordinates)
    computer_sol = []
    for ship in ships:
        if ship == 2:
            i = random.randint(0, 1)
            o = random.choice(temp_coor)
            if i == 0:
                if (o[0]+1, o[1]) in temp_coor:
                    computer_sol.append(o)
                    temp_coor.remove(o)
                    computer_sol.append((o[0]+1, o[1]))
                    temp_coor.remove((o[0]+1, o[1]))
                else:
                    computer_sol.append(o)
                    temp_coor.remove(o)
                    computer_sol.append((o[0] - 1, o[1]))
                    temp_coor.remove((o[0] - 1, o[1]))
            else:
                if (o[0], o[1] + 1) in temp_coor:
                    computer_sol.append(o)
                    temp_coor.remove(o)
                    computer_sol.append((o[0], o[1] + 1))
                    temp_coor.remove((o[0], o[1] + 1))
                else:
                    computer_sol.append(o)
                    temp_coor.remove(o)
                    computer_sol.append((o[0], o[1] - 1))
                    temp_coor.remove((o[0], o[1] - 1))

        elif ship == 1:
            o = random.choice(temp_coor)
            computer_sol.append(o)
            temp_coor.remove(o)
    if sum(ships) != 4:
        print("Not all ships registered in computer grid")

    return computer_sol


def main():
    # Generate the grid's coordinates
    coordinates = []
    for i in range(3):
        for j in range(3):
            coordinates.append((i, j))

    # Pass the ships (number and size: 1 2-sized ship, 2 1-sized ships) to the computer
    # Generate the computers ships
    ships = [2, 1, 1]
    computer_sol = computer_grid(coordinates=coordinates, ships=ships)

    # Initialize the grid and calculate homography/transformation matrix
    print("----------------")
    print("Draw a 3 by 3 grid with a black marker.\nMark the axes in the grid with their corresponsing numbers from 0 to 2, starting in the upper-left corner."
          "\nPlace the grid in the view of the camera.\n"
          "It is important that the grid is not moved relative to the camera while playing.")
    input("Press enter when you are ready to read in the grid:")
    grid_check = True
    while grid_check:
        grid = Grid()
        print("----------------")
        char = input("Does the grid in the image look correctly cropped? \nIf yes, please press y. "
                     "\nIf no, press another key in order to take a new image of the grid.")
        plt.close('all')
        if char == 'y':
            break

    # Create the players solution
    print("----------------")
    print("Place squares made out of cardboard, your markers, \non the grid to symbolize were your ships are placed. "
          "\nPlace two ships consisting of on marker each,"
          " \nand one ship made out of two markers next to each other on the grid.")
    input("Are you ready to read in your solution? \nIf yes, press enter:")
    player_sol = grid.update(sol=True)

    # Start the game. The while loop runs until all ships in either the player or the computers grid are hit
    print("----------------")
    print("Ok, the game is set up and ready to play. \nRemove your markers from the grid.")
    input("Press enter when you are ready to play:")
    while computer_sol and player_sol:
        # Player's turn
        print("----------------")
        input("Place a new marker on your guess. \nPress enter when ready:")
        guess_p = grid.update()
        if guess_p in computer_sol:
            print("----------------")
            print("You hit")
            computer_sol.remove(guess_p)
        else:
            print("----------------")
            print("You missed")
        if not computer_sol:
            break

        # Computer's turn
        guess_c = random.choice(coordinates)
        print("----------------")
        print(f"The computer guessed {guess_c}")
        coordinates.remove(guess_c)
        if guess_c in player_sol:
            print("The computer hit")
            player_sol.remove(guess_c)
        else:
            print("The computer missed")

    # Evaluate who won the game and release the camera-link
    grid.end(computer_sol=computer_sol, player_sol=player_sol)


if __name__ == "__main__":
    main()
