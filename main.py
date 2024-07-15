# main.py
import first_window
import second_window

if __name__ == '__main__':
    game_info = first_window.main()
    print(game_info)
    second_window.main(game_info)
