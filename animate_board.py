import pygame

# --- Player Class ---
class Player:
    def __init__(self, x, y, target_list, team, number):
        self.x = float(x)
        self.y = float(y)
        self.team = team
        self.number = number
        self.color = (0, 0, 255) if team == "offense" else (255, 0, 0)
        self.radius = 15

        self.target_list = target_list  # keep the full route
        self.target_count = 0
        self.target_x, self.target_y = self.target_list[0]  # first route point
        self.finished = False

    def run_route(self, speed=1):
        if self.finished:
            return  # nothing left to do

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist <= speed:  # reached current target
            self.x, self.y = self.target_x, self.target_y
            self.target_count += 1
            if self.target_count < len(self.target_list):
                self.target_x, self.target_y = self.target_list[self.target_count]
            else:
                self.finished = True  # done with route
        else:
            # normalize movement and step
            self.x += (dx / dist) * speed
            self.y += (dy / dist) * speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        font = pygame.font.SysFont(None, 18)
        num_text = font.render(str(self.number), True, (255, 255, 255))
        text_rect = num_text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(num_text, text_rect)



class ManPlayer(Player):
    def __init__(self, x, y,route, team, number):
        super().__init__(x, y,route, team, number)
        self.assignment = None

    def assign(self, offensive_player):
        self.assignment = offensive_player

    def track(self):
        self.set_target(self.assignment.x, self.assignment.y)
        self.move_towards_target()
        





# --- Setup Pygame ---
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football Marker Board")
clock = pygame.time.Clock()

# --- Players: Shotgun formation vs. 2-high defense ---
'''offensive_players = [
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



    ManPlayer(280, 450, "defense", 81),
    ManPlayer(280, 50, "defense", 52),   #WR 6-9
    ManPlayer(280, 150, "defense", 24),
    ManPlayer(280, 350, "defense", 24),

    ManPlayer(450, 350, "defense", 35),   #safteys
    ManPlayer(450, 150, "defense", 15)
]'''

offensive_players = [
    Player(250, 260, [(250, 260)], "offense", 12),    #OL 1-5
    Player(240, 240, [(240, 240)], "offense", 80),
    Player(230, 220, [(230, 220)], "offense", 81),
    Player(240, 280, [(240, 280)], "offense", 52),
    Player(230, 300, [(230, 300)], "offense", 24),

    Player(250, 450, [(250, 450), (400, 450)], "offense", 81),  # WR route example
    Player(250, 50,  [(250, 50),  (400, 100)], "offense", 52),
    Player(250, 150, [(250, 150), (400, 200)], "offense", 24),
    Player(250, 350, [(250, 350), (400, 300)], "offense", 25),

    Player(200, 260, [(200, 260)], "offense", 52),   #QB (stationary for now)
    Player(200, 280, [(200, 280), (220, 280)], "offense", 24),   #RB small move


    # Defense
    Player(280, 300, [(280, 300)], "defense", 12),
    Player(280, 240, [(280, 240)], "defense", 80),
    Player(280, 220, [(280, 220)], "defense", 81),
    Player(280, 280, [(280, 280)], "defense", 52),

    Player(350, 250, [(350, 250)], "defense", 52),

    ManPlayer(280, 450, [(280, 450)], "defense", 81),
    ManPlayer(280, 50,  [(280, 50)],  "defense", 52),
    ManPlayer(280, 150, [(280, 150)], "defense", 24),
    ManPlayer(280, 350, [(280, 350)], "defense", 24),

    ManPlayer(450, 350, [(450, 350)], "defense", 35),   #safeties
    ManPlayer(450, 150, [(450, 150)], "defense", 15)
]



ol1 = offensive_players[0]
ol2 = offensive_players[1]
ol3 = offensive_players[2]
ol4 = offensive_players[3]
ol5 = offensive_players[4]

wr1 = offensive_players[5]
wr2 = offensive_players[6]
wr3 = offensive_players[7]
te = offensive_players[8]

qb = offensive_players[9]
rb = offensive_players[10]

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
    for player in offensive_players:
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

        # --- Assign Man Coverage ---
        offensive_WRs = [offensive_players[5], offensive_players[6], offensive_players[7], offensive_players[8]]
        defenders = [offensive_players[16], offensive_players[17], offensive_players[18], offensive_players[19]]

        for d, wr in zip(defenders, offensive_WRs):
            d.assign(wr)

            # Safeties follow WRs too (example: deep help)
        offensive_players[20].assign(offensive_players[5])  # safety on WR1
        offensive_players[21].assign(offensive_players[6])  # safety on WR2


        # OL moves back
        for i in range(5):
            offensive_players[i].set_target(offensive_players[i].x - back_distance, offensive_players[i].y)

        # WRs
        offensive_players[5].set_target(450, 450)
        offensive_players[6].set_target(450, 50)
        offensive_players[7].set_target(450, 150)
        # TE
        offensive_players[8].set_target(550, 300)
        # QB
        offensive_players[9].set_target(170, 260)
        # RB
        offensive_players[10].set_target(300, 300)

    # Move players if started
    if movement_started:
        for i in [0,1,2,3,4,5,6,7,8,9,10]:  # only offense
            offensive_players[i].move_towards_target(speed=1.1)


        for i in [16,17,18,19,20,21]:
            defensive_player = offensive_players[i]
            if isinstance(defensive_player, ManPlayer):
                defensive_player.track()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
