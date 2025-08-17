import matplotlib.pyplot as plt

class Player:
    def __init__(self, x, y, team, number,label=""):
        self.x = x
        self.y = y
        self.team = team
        self.number = number
        self.label = label
        self.route = []

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_route(self, route_points):
        """Route is a list of (x, y) tuples"""
        self.route = route_points

class Field:
    def __init__(self, length=120, width=53.3):
        self.length = length
        self.width = width

    def draw(self, players):
        plt.figure(figsize=(12,6))
        # Field outline
        plt.plot([0, self.length, self.length, 0, 0],
                [0, 0, self.width, self.width, 0], 'g-')
        
        for x in range(0, self.length+1, 10):
            plt.axvline(x, color="lightgray", linestyle="--", linewidth=0.5)
        
        # Draw players
        for p in players:
            color = 'blue' if p.team == "offense" else 'red'
            plt.scatter(p.x, p.y, c=color, s=200)
            plt.text(p.x, p.y+1, str(p.number), ha='center')
            if p.route:
                rx, ry = zip(*([(p.x, p.y)] + p.route))  # start at player position
                plt.plot(rx, ry, color=color, linestyle="--")

        plt.xlim(0, self.length)
        plt.ylim(0, self.width)
        plt.show()

# Example usage
players = [
    # Offense
    Player(25, 26, "offense", 12, "C"),    #OL 1-5
    Player(24, 24, "offense", 80, "OL"),
    Player(23, 22, "offense", 81, "OL"),
    Player(24, 28, "offense", 52, "OL"),
    Player(23, 30, "offense", 24, "OL"),

    Player(25, 45, "offense", 81, "WR"),
    Player(25, 5, "offense", 52, "WR"),   #WR 6-9
    Player(25, 15, "offense", 24, "WR"),
    Player(25, 35, "offense", 24, "WR"),

    Player(20, 26, "offense", 52, "WR"),   #QB
    Player(20, 28, "offense", 24, "WR"),   #RB


    # Defense
    Player(28, 30, "defense", 12, "DT"),    #OL 1-5
    Player(28, 24, "defense", 80, "DT"),
    Player(28, 22, "defense", 81, "DT"),
    Player(28, 28, "defense", 52, "DE"),

    Player(35, 25, "defense", 52, "LB"),



    Player(28, 45, "defense", 81, "WR"),
    Player(28, 5, "defense", 52, "WR"),   #WR 6-9
    Player(28, 15, "defense", 24, "WR"),
    Player(28, 35, "defense", 24, "WR"),

    Player(45, 35, "defense", 35, "WR"),   #safteys
    Player(45, 15, "defense", 15, "WR")
]

players[5].set_route([(35, 45), (45, 45)])   # WR go route
players[6].set_route([(30, 20), (35, 25)])   # WR slant
players[9].set_route([(18, 26)])   

field = Field()
field.draw(players)
