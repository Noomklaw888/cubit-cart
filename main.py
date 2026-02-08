import asyncio # <--- ADD THIS
import pygame
import random

async def main():

    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cubit Cart")

    # Colors
    COLOR = (0, 255, 182)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)

    # Font
    font = pygame.font.Font(None, 36)

    # Game
    score = 0
    clock = pygame.time.Clock()
    running = True

    # Player
    player_width = 100
    player_height = 50
    player_x = 0
    player_y = HEIGHT - player_height - 40
    player_speed = 5

    y_velocity = 0
    on_ground = False

    # Physics
    gravity = 0.8

    # Ground
    ground = pygame.Rect(-50000000, HEIGHT - 40, 100000000, 40)

    # Hazards
    hazards = []
    HAZARD_WIDTH = 40
    HAZARD_HEIGHT = 40
    HAZARD_GAP = 250
    next_hazard_x = 400

    # Stars
    stars = []
    STAR_GAP = 250
    next_star_x = 400
    STAR_SIZE = 30

    # Track last hazard height to prevent stars from overlapping
    last_hazard_height = None

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # -------- PLAYER CONTROLS --------
        if keys[pygame.K_UP] and player_height < 200:
            player_height += player_speed
            player_y -= player_speed

        if keys[pygame.K_DOWN] and player_height > 50:
            player_height -= player_speed
            player_y += player_speed

        if keys[pygame.K_SPACE] and on_ground:
            y_velocity = -player_height / 10
            on_ground = False

        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # -------- PHYSICS --------
        y_velocity += gravity
        if y_velocity > 20:
            y_velocity = 20
        player_y += y_velocity

        # -------- SPAWN HAZARDS --------
        if player_x > next_hazard_x - 600:
            height_type = random.choice(["low", "mid", "high"])
            last_hazard_height = height_type  # save for star spawn

            if height_type == "low":
                y = ground.top - HAZARD_HEIGHT
            elif height_type == "mid":
                y = ground.top - 120
            else:
                y = ground.top - 220

            hazards.append(pygame.Rect(next_hazard_x, y, HAZARD_WIDTH, HAZARD_HEIGHT))
            next_hazard_x += HAZARD_GAP

        # -------- SPAWN STARS --------
        if player_x > next_star_x - 600:
            sheight_type = random.choice(["low", "mid", "high"])

            # ensure star height is different from last hazard
            while last_hazard_height and sheight_type == last_hazard_height:
                sheight_type = random.choice(["low", "mid", "high"])

            if sheight_type == "low":
                y = ground.top - 40
            elif sheight_type == "mid":
                y = ground.top - 120
            else:
                y = ground.top - 220

            stars.append(pygame.Rect(next_star_x, y, STAR_SIZE, STAR_SIZE))
            next_star_x += STAR_GAP * random.randint(1, 2)

        # -------- COLLISIONS --------
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        if player_rect.colliderect(ground) and y_velocity >= 0:
            player_y = ground.top - player_height
            y_velocity = 0
            on_ground = True

        for hazard in hazards:
            if player_rect.colliderect(hazard):
                print("Game Over! Resetting...")
                score = 0
                player_x = 0
                player_y = HEIGHT - player_height - 40
                hazards = []
                stars = []
                next_hazard_x = 400
                next_star_x = 400
                # Give the user a moment to realize they died
                await asyncio.sleep(1)

        for star in stars[:]:  # safe removal
            if player_rect.colliderect(star):
                score += 1
                stars.remove(star)

        # -------- CAMERA --------
        camera_x = player_x - WIDTH // 2
        draw_x = player_x - camera_x

        # -------- DRAW --------
        screen.fill(WHITE)

        # Ground
        pygame.draw.rect(screen, BLUE, (ground.x - camera_x, ground.y, ground.width, ground.height))

        # Player
        pygame.draw.rect(screen, COLOR, (draw_x, player_y, player_width, player_height))
        pygame.draw.rect(screen, BLACK, (draw_x, player_y, 20, 30))
        pygame.draw.rect(screen, BLACK, (draw_x + 80, player_y, 20, 30))
        pygame.draw.rect(screen, BLACK, (draw_x, player_y + player_height, 10, 10))
        pygame.draw.rect(screen, BLACK, (draw_x + 90, player_y + player_height, 10, 10))

        # Stars
        for star in stars:
            pygame.draw.rect(screen, YELLOW, (star.x - camera_x, star.y, star.width, star.height))

        # Hazards
        for hazard in hazards:
            pygame.draw.rect(screen, RED, (hazard.x - camera_x, hazard.y, hazard.width, hazard.height))

        # Score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        await asyncio.sleep(0) # <--- ADD THIS INSIDE THE LOOP

asyncio.run(main()) # <--- CALL THE FUNCTION
