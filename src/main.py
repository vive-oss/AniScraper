from __future__ import annotations
import random
import time
from scraper import get_anime_by_rank
from display import clear_screen, print_single_anime

def main() -> None:
   
    MAX_RANK = 30150
  
    while True:
        clear_screen()
        print("------------------------------AniScraper------------------------------")
        user_input = input(f"Pick a random anime from the top how many (1-{MAX_RANK})? Type 'q' to quit. ")
        
        if user_input.lower() == "q":
            clear_screen()
            print("Goodbye!")
            time.sleep(1)
            clear_screen()
            break

        try:
            user_max = int(user_input)
        except ValueError:
            clear_screen()
            print("(!) Please enter a valid number.")
            continue
        
        if user_max < 1 or user_max > MAX_RANK:
            clear_screen()
            print(f"(!) Please enter a number between 1 and {MAX_RANK}.")
            continue

        random_rank = random.randint(1, user_max)
        chosen = get_anime_by_rank(random_rank)
        clear_screen()
    
        if chosen is None: 
            print("(!) Could not fetch that anime. Try again.")
            continue
    
        print_single_anime(chosen) 
 
if __name__ == "__main__":
    main()
