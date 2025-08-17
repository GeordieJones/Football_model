import matplotlib.pyplot as plt

class Player:
    def __init__(self, x, y, team, number,label=""):
        self.x = x
        self.y = y
        self.team = team
        self.number = number
        self.label = label

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

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

        plt.xlim(0, self.length)
        plt.ylim(0, self.width)
        plt.show()

# Example usage
players = [
    # Offense
    Player(10, 26, "offense", 12, "C"),    #OL 1-5
    Player(9, 24, "offense", 80, "OL"),
    Player(8, 22, "offense", 81, "OL"),
    Player(9, 28, "offense", 52, "OL"),
    Player(8, 30, "offense", 24, "OL"),

    Player(10, 45, "offense", 81, "WR"),
    Player(10, 5, "offense", 52, "WR"),   #WR 6-8
    Player(10, 15, "offense", 24, "WR"),

    # Defense
    Player(12, 26, "defense", 52, "LB"),   # LB in the box
    Player(20, 15, "defense", 24, "CB"),   # CB covering WR bottom
    Player(20, 37, "defense", 25, "CB"),   # CB covering WR top
    Player(25, 20, "defense", 30, "S"),    # Safety bottom
    Player(25, 32, "defense", 31, "S"),    # Safety top
]

field = Field()
field.draw(players)
