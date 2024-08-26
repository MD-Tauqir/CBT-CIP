import random

def winner(player_choice,comp_choice):
    if player_choice==comp_choice:
        print("It's a tie!!")
    elif((player_choice=="rock"and comp_choice=="scissor")
        or (player_choice=="paper"and comp_choice=="rock")
        or (player_choice=="scissor"and comp_choice=="paper")):
        print("Congrulations You Won !!!!")
    else:
        print("Oops you lost!!!\nComputer Won")

def play():
    options=["rock", "paper", "scissor"]
    comp_choice=random.choice(options)
    player_choice=input("\n\nEnter your choice (Rock, Paper, Scissor) : ").lower()
    if player_choice not in options:
        print("Please choose a correct option")
        play()
    else:
        print("\nYour choice :", player_choice)
        print("Computer choice :", comp_choice)
        print()
        winner(player_choice,comp_choice)

print("\t\t\tWelcome to Rock Paper Scissor Game ")
print("\t\t\t-----------------------------------")
print()
start=input("Want to start the game ? (yes,no) : ").lower()
if (start!="no"):
    while(start!="no"):
        play()
        start=input("\nDo you want to play again ? (yes/no) : ").lower()
    print("\nThank you for playing the game :) ")