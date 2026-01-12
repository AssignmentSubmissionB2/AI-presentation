import pygame
import itertools
import time

# Configuration
COLORS = [
    (255, 50, 50),   # Red
    (50, 255, 50),   # Green
    (50, 50, 255),   # Blue
    (255, 255, 50),  # Yellow
    (255, 150, 50),  # Orange
    (200, 50, 255)   # Purple
]
WIDTH, HEIGHT = 800, 700
FPS = 60

def get_feedback(guess, secret):
    """Calculates Black and White pegs."""
    blacks = sum(g == s for g, s in zip(guess, secret))
    g_list, s_list = list(guess), list(secret)
    # Remove blacks to count whites correctly
    for i in range(3, -1, -1):
        if g_list[i] == s_list[i]:
            g_list.pop(i)
            s_list.pop(i)
    whites = 0
    for color in g_list:
        if color in s_list:
            whites += 1
            s_list.remove(color)
    return blacks, whites

class SolverApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Mastermind: Exhaustive vs Knuth Minimax")
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        
        # Game State
        self.secret = (0, 1, 2, 3) # Fixed secret for comparison
        self.all_codes = list(itertools.product(range(6), repeat=4))
        
        # Exhaustive Stats
        self.exh_possibilities = list(self.all_codes)
        self.exh_guesses = []
        self.exh_done = False
        
        # Knuth Stats
        self.knu_possibilities = list(self.all_codes)
        self.knu_guesses = []
        self.knu_done = False

    def solve_step_exhaustive(self):
        if self.exh_done: return
        guess = self.exh_possibilities[0]
        fb = get_feedback(guess, self.secret)
        self.exh_guesses.append((guess, fb))
        if fb == (4, 0): self.exh_done = True
        else:
            self.exh_possibilities = [p for p in self.exh_possibilities if get_feedback(guess, p) == fb]

    def solve_step_knuth(self):
        if self.knu_done: return
        if not self.knu_guesses:
            guess = (0, 0, 1, 1) # Knuth's optimal first move
        else:
            # Minimax logic: find guess that minimizes the max remaining possibilities
            best_guess = None
            min_max_rem = float('inf')
            
            # To keep animation smooth, we sample or use a simplified minimax if set is large
            for potential_guess in self.all_codes:
                score_counts = {}
                for p in self.knu_possibilities:
                    fb = get_feedback(potential_guess, p)
                    score_counts[fb] = score_counts.get(fb, 0) + 1
                
                max_rem = max(score_counts.values())
                if max_rem < min_max_rem:
                    min_max_rem = max_rem
                    best_guess = potential_guess
            guess = best_guess

        fb = get_feedback(guess, self.secret)
        self.knu_guesses.append((guess, fb))
        if fb == (4, 0): self.knu_done = True
        else:
            self.knu_possibilities = [p for p in self.knu_possibilities if get_feedback(guess, p) == fb]

    def draw_board(self, x_offset, title, guesses, done, possibilities_count):
        # Draw Container
        rect = pygame.Rect(x_offset, 80, 350, 550)
        pygame.draw.rect(self.screen, (40, 40, 40), rect, border_radius=10)
        
        header = self.font.render(f"{title} (Remaining: {possibilities_count})", True, (255, 255, 255))
        self.screen.blit(header, (x_offset + 10, 50))

        for i, (guess, fb) in enumerate(guesses):
            y = 120 + (i * 50)
            # Draw Pegs
            for j, color_idx in enumerate(guess):
                pygame.draw.circle(self.screen, COLORS[color_idx], (x_offset + 50 + j*45, y), 18)
            
            # Draw Feedback Pegs
            for b in range(fb[0]): # Black
                pygame.draw.circle(self.screen, (0, 0, 0), (x_offset + 250 + b*20, y - 8), 6)
            for w in range(fb[1]): # White
                pygame.draw.circle(self.screen, (220, 220, 220), (x_offset + 250 + (fb[0]+w)*20, y + 8), 6)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Step solvers slowly so we can see them
            if not self.exh_done:
                self.solve_step_exhaustive()
                time.sleep(0.2)

            if not self.knu_done:
                self.solve_step_knuth()
                time.sleep(0.2)

            # Drawing
            self.screen.fill((25, 25, 25))

            self.draw_board(
                30,
                "Exhaustive Search",
                self.exh_guesses,
                self.exh_done,
                len(self.exh_possibilities),
            )

            self.draw_board(
                420,
                "Knuth Minimax",
                self.knu_guesses,
                self.knu_done,
                len(self.knu_possibilities),
            )

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    app = SolverApp()
    app.run()
