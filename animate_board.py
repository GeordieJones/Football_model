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

    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y

    def move_towards_target(self, speed=1):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist > 0:
            step_x = speed * dx / dist
            step_y = speed * dy / dist

            self.x += step_x
            self.y += step_y

    def run_route(self, speed=1.1):
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


    def track(self, speed=1):
        self.set_target(self.assignment.x, self.assignment.y)
        self.move_towards_target(speed=speed)
        





# --- Setup Pygame ---
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football Marker Board")
clock = pygame.time.Clock()


offensive_players = [
    Player(250, 260, [(250, 260)], "offense", 12),    #OL 1-5
    Player(240, 240, [(240, 240)], "offense", 80),
    Player(230, 220, [(230, 220)], "offense", 81),
    Player(240, 280, [(240, 280)], "offense", 52),
    Player(230, 300, [(230, 300)], "offense", 24),

    Player(250, 450, [(250, 450), (400, 450),(400, 80)], "offense", 81),  # WR route example
    Player(250, 50,  [(250, 50),  (400, 100),(500, 250)], "offense", 52),
    Player(250, 150, [(250, 150), (400, 200),(300, 180)], "offense", 24),
    Player(250, 350, [(250, 350), (400, 300),(600, 450)], "offense", 25),

    Player(200, 260, [(170, 260)], "offense", 52),   #QB (stationary for now)
    Player(200, 280, [(200, 280), (210, 30), (500, 30)], "offense", 24),   #RB small move


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
wr3 = offensive_players