"""
Pixel Runner - A fun endless runner game built with Pygame
Navigate your pixel character and jump over obstacles to achieve the highest score!
"""

import random
import sys
from enum import Enum

import pygame


class GameState(Enum):
    """Enum for different game states"""

    START_SCREEN = 1
    PLAYING = 2
    GAME_OVER = 3


class PixelRunner:
    """Main game class for Pixel Runner"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()

        # Constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 400
        self.GROUND_Y = 300
        self.GRAVITY = 1.1
        self.JUMP_STRENGTH = -22
        self.OBSTACLE_SPEED = 5
        self.FPS = 60

        # Colors
        self.SKY_COLOR = (94, 129, 162)
        self.TEXT_COLOR = (64, 64, 64)
        self.SCORE_BG_COLOR = "#c0e8ec"
        self.GAME_OVER_BG_COLOR = "Yellow"

        # Setup display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pixel Runner")
        self.clock = pygame.time.Clock()

        # Game state
        self.game_state = GameState.START_SCREEN
        self.score_start_time = 0
        self.final_score = 0  # Store final score when game ends
        self.player_gravity = 0

        # Load assets
        self._load_assets()

        # Initialize game objects
        self._init_game_objects()

        # Animation variables
        self.player_walk_index = 0
        self.player_walk_timer = 0
        self.snail_anim_index = 0
        self.snail_anim_timer = 0

    def _load_assets(self):
        """Load all game assets"""
        # Font
        self.font = pygame.font.Font("assets/font/Pixeltype.ttf", 50)

        # Background
        self.sky_surface = pygame.image.load("assets/graphics/Sky.png").convert()
        self.ground_surface = pygame.image.load("assets/graphics/ground.png").convert()

        # Player sprites
        self.player_walk_1 = pygame.image.load(
            "assets/graphics/player/player_walk_1.png"
        ).convert_alpha()
        self.player_walk_2 = pygame.image.load(
            "assets/graphics/player/player_walk_2.png"
        ).convert_alpha()
        self.player_jump = pygame.image.load(
            "assets/graphics/player/jump.png"
        ).convert_alpha()
        self.player_stand = pygame.image.load(
            "assets/graphics/player/player_stand.png"
        ).convert_alpha()
        self.player_walk_frames = [self.player_walk_1, self.player_walk_2]

        # Enemy sprites
        self.snail_1 = pygame.image.load(
            "assets/graphics/snail/snail1.png"
        ).convert_alpha()
        self.snail_2 = pygame.image.load(
            "assets/graphics/snail/snail2.png"
        ).convert_alpha()
        self.snail_frames = [self.snail_1, self.snail_2]

        # Fly sprites
        self.fly_1 = pygame.image.load("assets/graphics/fly/Fly1.png").convert_alpha()
        self.fly_frames = [self.fly_1]  # Can add more fly frames if available

    def _init_game_objects(self):
        """Initialize game object positions"""
        self.player_rect = self.player_walk_1.get_rect(midbottom=(80, self.GROUND_Y))
        self.obstacles = []
        self._spawn_obstacle()

    def _spawn_obstacle(self):
        """Spawn a new obstacle"""
        obstacle_type = random.choice(["snail", "fly"])
        if obstacle_type == "snail":
            obstacle_rect = self.snail_1.get_rect(
                midbottom=(self.SCREEN_WIDTH + 100, self.GROUND_Y)
            )
            self.obstacles.append(
                {"type": "snail", "rect": obstacle_rect, "frame": 0, "timer": 0}
            )
        else:
            obstacle_rect = self.fly_1.get_rect(
                midbottom=(self.SCREEN_WIDTH + 100, self.GROUND_Y - 100)
            )
            self.obstacles.append(
                {"type": "fly", "rect": obstacle_rect, "frame": 0, "timer": 0}
            )

    def _get_player_surface(self):
        """Get the current player sprite based on state"""
        if self.player_rect.bottom < self.GROUND_Y:
            return self.player_jump
        else:
            # Walking animation
            self.player_walk_timer += 1
            if self.player_walk_timer >= 5:  # Change frame every 5 ticks
                self.player_walk_index = (self.player_walk_index + 1) % len(
                    self.player_walk_frames
                )
                self.player_walk_timer = 0
            return self.player_walk_frames[self.player_walk_index]

    def _get_obstacle_surface(self, obstacle):
        """Get the current obstacle sprite based on type and animation"""
        if obstacle["type"] == "snail":
            obstacle["timer"] += 1
            if obstacle["timer"] >= 10:  # Change frame every 10 ticks
                obstacle["frame"] = (obstacle["frame"] + 1) % len(self.snail_frames)
                obstacle["timer"] = 0
            return self.snail_frames[obstacle["frame"]]
        else:  # fly
            return self.fly_1

    def _handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self._jump()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player_rect.collidepoint(event.pos):
                        self._jump()

            elif self.game_state == GameState.START_SCREEN:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self._start_game()

            elif self.game_state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y or event.key == pygame.K_SPACE:
                        self._restart_game()
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()

    def _jump(self):
        """Make the player jump"""
        if self.player_rect.bottom >= self.GROUND_Y:
            self.player_gravity = self.JUMP_STRENGTH

    def _start_game(self):
        """Start a new game"""
        self.game_state = GameState.PLAYING
        self.score_start_time = int(pygame.time.get_ticks() / 100)
        self._reset_game_objects()

    def _restart_game(self):
        """Restart the game after game over"""
        self._start_game()

    def _reset_game_objects(self):
        """Reset all game objects to initial state"""
        self.player_rect.midbottom = (80, self.GROUND_Y)
        self.player_gravity = 0
        self.obstacles.clear()
        self._spawn_obstacle()

    def _update_player(self):
        """Update player physics"""
        self.player_gravity += self.GRAVITY
        self.player_rect.y += self.player_gravity

        # Keep player on ground
        if self.player_rect.bottom >= self.GROUND_Y:
            self.player_rect.bottom = self.GROUND_Y
            self.player_gravity = 0

    def _update_obstacles(self):
        """Update obstacle positions and spawning"""
        # Move existing obstacles
        for obstacle in self.obstacles[
            :
        ]:  # Use slice to avoid modification during iteration
            obstacle["rect"].x -= self.OBSTACLE_SPEED
            if obstacle["rect"].right < 0:
                self.obstacles.remove(obstacle)

        # Spawn new obstacles
        if not self.obstacles or self.obstacles[-1]["rect"].x < self.SCREEN_WIDTH - 300:
            if random.randint(0, 100) < 2:  # 2% chance per frame to spawn
                self._spawn_obstacle()

    def _check_collisions(self):
        """Check for collisions between player and obstacles"""
        for obstacle in self.obstacles:
            if self.player_rect.colliderect(obstacle["rect"]):
                return True
        return False

    def _calculate_score(self):
        """Calculate current score"""
        if self.game_state == GameState.GAME_OVER:
            return self.final_score
        return int(pygame.time.get_ticks() / 100) - self.score_start_time

    def _draw_score(self):
        """Draw the current score"""
        current_score = self._calculate_score()
        score_surface = self.font.render(
            f"Score: {current_score}", True, self.TEXT_COLOR
        )
        score_rect = score_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 50))

        # Draw background for score
        pygame.draw.rect(self.screen, self.SCORE_BG_COLOR, score_rect)
        pygame.draw.rect(self.screen, self.SCORE_BG_COLOR, score_rect, 10)

        self.screen.blit(score_surface, score_rect)

    def _draw_start_screen(self):
        """Draw the start screen"""
        self.screen.fill(self.SKY_COLOR)

        # Title
        title_surface = self.font.render("PIXEL RUNNER", True, self.TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 80))

        # Player character
        player_surface = self.player_stand
        player_rect = player_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 200))

        # Instructions
        instruction_surface = self.font.render(
            "Press SPACE to Start", True, self.TEXT_COLOR
        )
        instruction_rect = instruction_surface.get_rect(
            center=(self.SCREEN_WIDTH // 2, 320)
        )

        self.screen.blit(title_surface, title_rect)
        self.screen.blit(player_surface, player_rect)
        self.screen.blit(instruction_surface, instruction_rect)

    def _draw_game_over_screen(self):
        """Draw the game over screen"""
        final_score = self._calculate_score()

        # Game Over text
        game_over_surface = self.font.render(
            f"Game Over! Score: {final_score}", True, self.TEXT_COLOR
        )
        game_over_rect = game_over_surface.get_rect(
            center=(self.SCREEN_WIDTH // 2, 150)
        )

        # Restart prompt
        restart_surface = self.font.render(
            "Restart? Press SPACE/Y or N", True, self.TEXT_COLOR
        )
        restart_rect = restart_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 250))

        # Draw backgrounds
        pygame.draw.rect(self.screen, self.GAME_OVER_BG_COLOR, game_over_rect)
        pygame.draw.rect(self.screen, self.GAME_OVER_BG_COLOR, restart_rect)

        self.screen.blit(game_over_surface, game_over_rect)
        self.screen.blit(restart_surface, restart_rect)

    def _draw_game(self):
        """Draw the main game"""
        # Background
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.ground_surface, (0, self.GROUND_Y))

        # Player
        player_surface = self._get_player_surface()
        self.screen.blit(player_surface, self.player_rect)

        # Obstacles
        for obstacle in self.obstacles:
            obstacle_surface = self._get_obstacle_surface(obstacle)
            self.screen.blit(obstacle_surface, obstacle["rect"])

        # Score
        self._draw_score()

    def run(self):
        """Main game loop"""
        while True:
            self._handle_events()

            if self.game_state == GameState.PLAYING:
                # Update game state
                self._update_player()
                self._update_obstacles()

                # Check collisions
                if self._check_collisions():
                    self.final_score = (
                        int(pygame.time.get_ticks() / 100) - self.score_start_time
                    )
                    self.game_state = GameState.GAME_OVER

                # Draw game
                self._draw_game()

            elif self.game_state == GameState.START_SCREEN:
                self._draw_start_screen()

            elif self.game_state == GameState.GAME_OVER:
                self._draw_game_over_screen()

            pygame.display.update()
            self.clock.tick(self.FPS)


def main():
    """Main function to run the game"""
    game = PixelRunner()
    game.run()


if __name__ == "__main__":
    main()
