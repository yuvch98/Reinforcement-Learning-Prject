import pygame
import q_learning_agent
import sarsa_agent
import display_animation
# Initialize Pygame
pygame.init()
import first_window

if __name__ == '__main__':
    game_info = first_window.main()
    print(game_info)
    if len(game_info) < 9:
        exit(-10)
    game_info['grid_size'] = int(game_info['grid_size'])
    game_info['alpha'] = float(game_info['alpha'])
    game_info['gamma'] = float(game_info['gamma'])
    game_info['epsilon'] = float(game_info['epsilon'])
    game_info['max_steps_per_episode'] = int(game_info['max_steps_per_episode'])
    game_info['training_phase'] = int(game_info['training_phase'])
    game_info['play_phase'] = int(game_info['play_phase'])
    if game_info['algorithm'] == "Q_Learning":
        game_info = q_learning_agent.main(game_info)
    else:
        game_info = sarsa_agent.main(game_info)
    display_animation.main(game_info, play_phase=True)