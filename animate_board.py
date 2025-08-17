import pygame

# --- Player Class ---
class Player:
    def __init__(self, x, y, team, number):
        self.x = float(x)
        self.y = float(y)
        self.team = team
        self.number = number
        self.color = (0, 0, 255) if team == "offense" else (255, 0, 0)
        self.radius = 15
        self.target_x = float(x)
        self.target_y = float(y)

    def set_target(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y

    def move_towards_target(self, speed=2):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx**2 + dy**2) ** 0.5
        if dist > speed:  # normalize and step
            self.x += int(dx / dist * speed)
            self.y += int(dy / dist * speed)
        else:  # snap to target if close enough
            self.x, self.y = self.target_x, self.target_y


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        font = pygame.font.SysFont(None, 18)
        num_text = font.render(str(self.number), True, (255, 255, 255))
        text_rect = num_text.get_rect(center=(self.x, self.y))
        screen.blit(num_text, text_rect)


# --- Setup Pygame ---
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football Marker Board")
clock = pygame.time.Clock()

# --- Players: Shotgun formation vs. 2-high defense ---
players = [
    Player(250, 260, "offense", 12),    #OL 1-5
    Player(240, 240, "offense", 80),
    Player(230, 220, "offense", 81),
    Player(240, 280, "offense", 52),
    Player(230, 300, "offense", 24),

    Player(250, 450, "offense", 81),
    Player(250, 50, "offense", 52),   #WR 6-9
    Player(250, 150, "offense", 24),
    Player(250, 350, "offense", 25),

    Player(200, 260, "offense", 52),   #QB
    Player(200, 280, "offense", 24),   #RB


    # Defense
    Player(280, 300, "defense", 12),    #OL 1-5
    Player(280, 240, "defense", 80),
    Player(280, 220, "defense", 81),
    Player(280, 280, "defense", 52),

    Player(350, 250, "defense", 52),



    Player(280, 450, "defense", 81),
    Player(280, 50, "defense", 52),   #WR 6-9
    Player(280, 150, "defense", 24),
    Player(280, 350, "defense", 24),

    Player(450, 350, "defense", 35),   #safteys
    Player(450, 150, "defense", 15)
]


ol1 = players[0]
ol2 = players[1]
ol3 = players[2]
ol4 = players[3]
ol5 = players[4]

wr1 = players[5]
wr2 = players[6]
wr3 = players[7]
te = players[8]

qb = players[10]
rb = players[11]

for i in range(50, WIDTH, 50):
        pygame.draw.line(screen, (255, 255, 255), (i, 0), (i, HEIGHT), 1)

# --- Game Loop ---
movement_started = False
start_time = None
delay = 4000  # 4 seconds

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 128, 0))  # green field

    # Draw yard lines
    for i in range(50, WIDTH, 50):
        pygame.draw.line(screen, (255, 255, 255), (i, 0), (i, HEIGHT), 1)

    # Draw all players
    for player in players:
        player.draw(screen)

    # Start timer after first frame
    if start_time is None:
        start_time = pygame.time.get_ticks()

    current_time = pygame.time.get_ticks()
    if not movement_started and current_time - start_time >= delay:
        movement_started = True
        # Set targets for all moving players
        yards_to_pixels = 10
        back_distance = 3 * yards_to_pixels

        # OL moves back
        for i in range(5):
            players[i].set_target(players[i].x - back_distance, players[i].y)

        # WRs
        players[5].set_target(450, 450)
        players[6].set_target(450, 50)
        players[7].set_target(450, 150)
        # TE
        players[8].set_target(550, 300)
        # QB
        players[10].set_target(170, 260)
        # RB
        players[11].set_target(300, 300)

    # Move players if started
    if movement_started:
        for i in [0,1,2,3,4,5,6,7,8,10,11]:  # only offense
            players[i].move_towards_target(speed=1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
