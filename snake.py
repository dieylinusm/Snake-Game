import asyncio
import platform
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width = 400
height = 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Set up the grid
grid_size = 20
grid_width = width // grid_size
grid_height = height // grid_size

# Set up the snake and food
snake = [(10, 10)]  # Initial snake position
direction = "right"  # Initial direction
food = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))  # Initial food position
score = 0  # Initial score

# Function to generate new food position not on the snake
def generate_food():
    while True:
        new_food = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
        if new_food not in snake:
            return new_food

# Setup function for initialization
def setup():
    global snake, direction, food, score
    snake = [(10, 10)]
    direction = "right"
    food = generate_food()
    score = 0
    window.fill(black)
    pygame.display.update()

# Update loop for game logic
async def update_loop():
    global snake, direction, food, score, running

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "down":
                direction = "up"
            elif event.key == pygame.K_DOWN and direction != "up":
                direction = "down"
            elif event.key == pygame.K_LEFT and direction != "right":
                direction = "left"
            elif event.key == pygame.K_RIGHT and direction != "left":
                direction = "right"

    # Move the snake
    head = snake[0]
    if direction == "up":
        new_head = (head[0], head[1] - 1)
    elif direction == "down":
        new_head = (head[0], head[1] + 1)
    elif direction == "left":
        new_head = (head[0] - 1, head[1])
    elif direction == "right":
        new_head = (head[0] + 1, head[1])
    snake.insert(0, new_head)

    # Check if snake ate the food
    if snake[0] == food:
        score += 1
        food = generate_food()  # Generate new food
    else:
        snake.pop()  # Remove the last segment

    # Check for collisions with walls or itself
    if (snake[0][0] < 0 or snake[0][0] >= grid_width or
        snake[0][1] < 0 or snake[0][1] >= grid_height or
        snake[0] in snake[1:]):
        return False

    # Draw the screen
    window.fill(black)
    for segment in snake:
        pygame.draw.rect(window, green, (segment[0] * grid_size, segment[1] * grid_size, grid_size, grid_size))
    pygame.draw.rect(window, red, (food[0] * grid_size, food[1] * grid_size, grid_size, grid_size))
    pygame.display.set_caption(f"Snake Game - Score: {score}")
    pygame.display.update()

    return True

# Main game loop
FPS = 10
running = True

async def main():
    setup()
    global running
    while running:
        running = await update_loop()
        await asyncio.sleep(1.0 / FPS)

    # Game over message
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, (255, 255, 255))
    window.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.update()
    await asyncio.sleep(2)  # Wait 2 seconds
    pygame.quit()

# Run the game based on platform
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
