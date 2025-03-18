from car_simulation.cli import get_user_inputs

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_user_inputs()
    while True:
        print("Please choose from the following options:", end="\n")
        print("[1] Start over")
        print("[2] Exit", end="\n")
        new_choice = input()
        if new_choice == "1":
            get_user_inputs()
        elif new_choice == "2":
            print("Thank you for running the simulation. Goodbye!")
            break
