import pygame
import random
import math
import os
import urllib.request
import tkinter as tk
from tkinter import messagebox, simpledialog

# Default settings
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
DEFAULT_FPS = 60
DEFAULT_OBJECT_COUNT = 60
DEFAULT_OBJECT_SIZE = 35  
DEFAULT_SPEED_MIN = 1
DEFAULT_SPEED_MAX = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Object types
ROCK = 0
PAPER = 1
SCISSORS = 2

# Unicode emojis
EMOJIS = {
    ROCK: "🪨",
    PAPER: "📄",
    SCISSORS: "✂️"
}

# Text labels
OBJECT_NAMES = {
    ROCK: "ROCK",
    PAPER: "PAPER", 
    SCISSORS: "SCISSORS"
}

def download_emoji_font():
    """Download Noto Color Emoji font if not exists"""
    font_path = "NotoColorEmoji.ttf"
    
    if not os.path.exists(font_path):
        print("Downloading emoji font...")
        try:
            url = "https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoColorEmoji.ttf"
            urllib.request.urlretrieve(url, font_path)
            print("Font downloaded successfully!")
        except Exception as e:
            print(f"Could not download font: {e}")
            return None
    
    return font_path

def get_emoji_font(size=30): 
    """Get emoji font, trying multiple fallback options"""
    # Try to download/use Noto Color Emoji
    font_path = download_emoji_font()
    if font_path and os.path.exists(font_path):
        try:
            return pygame.font.Font(font_path, size)
        except:
            pass
    
    # Fallback to system fonts that might support emoji
    emoji_fonts = [
        "seguiemj.ttf",  # Windows emoji font
        "Apple Color Emoji.ttc",  # macOS
        "NotoColorEmoji.ttf",  # Linux
        "Segoe UI Emoji",  # Windows
        "Apple Color Emoji",  # macOS
        "Noto Color Emoji",  # Linux
    ]
    
    for font_name in emoji_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            # Test if font can render emoji
            test_surface = font.render("🪨", True, BLACK)
            if test_surface.get_width() > size // 3:  
                return font
        except:
            continue
    
    # Last fallback - default font
    return pygame.font.Font(None, size)

def load_font(size):
    """
    Loads the font directly from the local file.
    Exits with a clear error message if the font is missing.
    This is the most reliable, offline, and cross-platform method.
    """
    # Note: This requires 'os' and 'sys' to be imported at the top of your script.
    font_path = "NotoColorEmoji.ttf"
    
    if not os.path.exists(font_path):
        print("---------------------------------------------------------")
        print(f"FATAL ERROR: Font file not found!")
        print(f"Please make sure '{font_path}' is in the same folder as the script.")
        print("---------------------------------------------------------")
        sys.exit(1) # Stop the program
        
    try:
        return pygame.font.Font(font_path, size)
    except pygame.error as e:
        print("---------------------------------------------------------")
        print(f"FATAL ERROR: The font file '{font_path}' could not be loaded. It may be corrupt.")
        print(f"Pygame Error: {e}")
        print("---------------------------------------------------------")
        sys.exit(1) # Stop the program

class SettingsDialog:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game Settings")
        self.root.geometry("450x950")
        self.root.resizable(False, False)
        
        # Force window to front and make it stay on top temporarily
        self.root.wm_attributes("-topmost", 1)
        self.root.focus_force()
        self.root.grab_set()  
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.root.winfo_screenheight() // 2) - (950 // 2)
        self.root.geometry(f"450x950+{x}+{y}")
        
        # Set background color
        self.root.configure(bg='#f0f0f0')
        
        self.settings = {}
        self.create_widgets()
        
    def create_widgets(self):        
        # Title with background
        title_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.pack_propagate(False)
        
        title = tk.Label(title_frame, text="🎮 ROCK PAPER SCISSORS 🎮", 
                        font=("Arial", 16, "bold"), fg='white', bg='#2196F3')
        title.pack(expand=True)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Screen dimensions
        screen_frame = tk.LabelFrame(main_frame, text="Screen Dimensions", 
                                   font=("Arial", 12, "bold"), padx=15, pady=15, bg='#f0f0f0')
        screen_frame.pack(pady=10, fill="x")
        
        tk.Label(screen_frame, text="Width:", font=("Arial", 11), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.width_var = tk.IntVar(value=DEFAULT_SCREEN_WIDTH)
        width_spin = tk.Spinbox(screen_frame, from_=600, to=1920, width=12, 
                               textvariable=self.width_var, font=("Arial", 11))
        width_spin.grid(row=0, column=1, padx=10, pady=8)
        
        tk.Label(screen_frame, text="Height:", font=("Arial", 11), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.height_var = tk.IntVar(value=DEFAULT_SCREEN_HEIGHT)
        height_spin = tk.Spinbox(screen_frame, from_=400, to=1080, width=12, 
                                textvariable=self.height_var, font=("Arial", 11))
        height_spin.grid(row=1, column=1, padx=10, pady=8)
        
        # Object settings
        object_frame = tk.LabelFrame(main_frame, text="Object Settings", 
                                   font=("Arial", 12, "bold"), padx=15, pady=15, bg='#f0f0f0')
        object_frame.pack(pady=10, fill="x")
        
        tk.Label(object_frame, text="Total Objects:", font=("Arial", 11), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.count_var = tk.IntVar(value=DEFAULT_OBJECT_COUNT)
        count_spin = tk.Spinbox(object_frame, from_=12, to=300, width=12, 
                               textvariable=self.count_var, font=("Arial", 11))
        count_spin.grid(row=0, column=1, padx=10, pady=8)
        
        tk.Label(object_frame, text="Object Size:", font=("Arial", 11), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.size_var = tk.IntVar(value=DEFAULT_OBJECT_SIZE)
        size_spin = tk.Spinbox(object_frame, from_=15, to=80, width=12, 
                              textvariable=self.size_var, font=("Arial", 11))
        size_spin.grid(row=1, column=1, padx=10, pady=8)
        
        # Collision settings
        collision_frame = tk.LabelFrame(main_frame, text="Collision Settings", 
                                      font=("Arial", 12, "bold"), padx=15, pady=15, bg='#f0f0f0')
        collision_frame.pack(pady=10, fill="x")
        
        tk.Label(collision_frame, text="Collision Coverage %:", font=("Arial", 11), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.coverage_var = tk.IntVar(value=100)
        coverage_spin = tk.Spinbox(collision_frame, from_=10, to=100, width=12, 
                                  textvariable=self.coverage_var, font=("Arial", 11))
        coverage_spin.grid(row=0, column=1, padx=10, pady=8)
        
        coverage_help = tk.Label(collision_frame, text="(Lower values = objects must overlap more to collide)", 
                               font=("Arial", 9), fg="gray", bg='#f0f0f0')
        coverage_help.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        # Speed settings
        speed_frame = tk.LabelFrame(main_frame, text="Speed Settings", 
                                  font=("Arial", 12, "bold"), padx=15, pady=15, bg='#f0f0f0')
        speed_frame.pack(pady=10, fill="x")
        
        tk.Label(speed_frame, text="Min Speed:", font=("Arial", 11), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.speed_min_var = tk.DoubleVar(value=DEFAULT_SPEED_MIN)
        speed_min_spin = tk.Spinbox(speed_frame, from_=0.5, to=5.0, increment=0.1, 
                                   width=12, textvariable=self.speed_min_var, format="%.1f", font=("Arial", 11))
        speed_min_spin.grid(row=0, column=1, padx=10, pady=8)
        
        tk.Label(speed_frame, text="Max Speed:", font=("Arial", 11), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.speed_max_var = tk.DoubleVar(value=DEFAULT_SPEED_MAX)
        speed_max_spin = tk.Spinbox(speed_frame, from_=1.0, to=10.0, increment=0.1, 
                                   width=12, textvariable=self.speed_max_var, format="%.1f", font=("Arial", 11))
        speed_max_spin.grid(row=1, column=1, padx=10, pady=8)
        
        # Info
        info_frame = tk.Frame(main_frame, bg='#f0f0f0')
        info_frame.pack(pady=15, fill="x")
        
        info_text = ("Objects will be divided equally among\nRock, Paper, and Scissors")
        tk.Label(info_frame, text=info_text, font=("Arial", 10), 
                fg="gray", justify="center", bg='#f0f0f0').pack()
        
        # Buttons - Very large and prominent
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=30)
        
        # START button - extra large and prominent
        start_btn = tk.Button(button_frame, text="🚀 START GAME 🚀", 
                             font=("Arial", 16, "bold"),
                             bg="#4CAF50", fg="white", 
                             padx=40, pady=20,
                             relief="raised", bd=5,
                             command=self.start_game, 
                             cursor="hand2",
                             activebackground="#45a049")
        start_btn.pack(pady=10)
        
        quit_btn = tk.Button(button_frame, text="❌ QUIT", 
                            font=("Arial", 12, "bold"),
                            bg="#f44336", fg="white", 
                            padx=25, pady=12,
                            relief="raised", bd=3,
                            command=self.quit_app, 
                            cursor="hand2",
                            activebackground="#da190b")
        quit_btn.pack(pady=5)
        
        # Set focus and bind Enter key
        start_btn.focus_set()
        self.root.bind('<Return>', lambda e: self.start_game())
        self.root.bind('<Escape>', lambda e: self.quit_app())
        
        # Remove topmost after window is fully loaded
        self.root.after(1000, lambda: self.root.wm_attributes("-topmost", 0))
    
    def validate_settings(self):
        """Validate user inputs"""
        if self.speed_min_var.get() >= self.speed_max_var.get():
            messagebox.showerror("Error", "Min speed must be less than max speed!")
            return False
        
        if self.count_var.get() % 3 != 0:
            # Adjust to nearest multiple of 3
            adjusted = (self.count_var.get() // 3) * 3
            if adjusted < 3:
                adjusted = 3
            result = messagebox.askyesno("Adjust Object Count", 
                                       f"Object count must be divisible by 3.\n"
                                       f"Adjust from {self.count_var.get()} to {adjusted}?")
            if result:
                self.count_var.set(adjusted)
            else:
                return False
        
        return True
    
    def start_game(self):
        if self.validate_settings():
            self.settings = {
                'screen_width': self.width_var.get(),
                'screen_height': self.height_var.get(),
                'object_count': self.count_var.get(),
                'object_size': self.size_var.get(),
                'speed_min': self.speed_min_var.get(),
                'speed_max': self.speed_max_var.get(),
                'collision_coverage': self.coverage_var.get() / 100.0
            }
            self.root.quit()
            self.root.destroy()
    
    def quit_app(self):
        self.settings = None
        self.root.quit()
        self.root.destroy()
    
    def get_settings(self):
        self.root.mainloop()
        return self.settings

class GameObject:
    def __init__(self, x, y, obj_type, speed_min, speed_max):
        self.x = x
        self.y = y
        self.type = obj_type
        self.speed_x = random.uniform(speed_min, speed_max) * random.choice([-1, 1])
        self.speed_y = random.uniform(speed_min, speed_max) * random.choice([-1, 1])
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)
        
    def update(self, screen_width, screen_height, object_size):
        # Update position
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Rotation
        self.rotation += self.rotation_speed
        
        # Wall collision
        if self.x <= object_size // 2:
            self.x = object_size // 2
            self.speed_x = abs(self.speed_x)
        elif self.x >= screen_width - object_size // 2:
            self.x = screen_width - object_size // 2
            self.speed_x = -abs(self.speed_x)
            
        if self.y <= object_size // 2:
            self.y = object_size // 2
            self.speed_y = abs(self.speed_y)
        elif self.y >= screen_height - object_size // 2:
            self.y = screen_height - object_size // 2
            self.speed_y = -abs(self.speed_y)
    
    def get_distance(self, other):
        """Calculate distance between two objects"""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def collides_with(self, other, object_size, coverage):
        """Check collision with another object based on coverage percentage"""
        distance = self.get_distance(other)
        collision_threshold = object_size * coverage  
        return distance < collision_threshold
    
    def battle(self, other):
        """Battle between two objects based on rock-paper-scissors rules"""
        if self.type == other.type:
            return None  
        
        # Game rules
        if (self.type == ROCK and other.type == SCISSORS) or \
           (self.type == SCISSORS and other.type == PAPER) or \
           (self.type == PAPER and other.type == ROCK):
            return self  
        else:
            return other 

class Game:
    def __init__(self, settings):
        pygame.init()
        
        self.screen_width = settings['screen_width']
        self.screen_height = settings['screen_height']
        self.object_count = settings['object_count']
        self.object_size = settings['object_size']
        self.speed_min = settings['speed_min']
        self.speed_max = settings['speed_max']
        self.collision_coverage = settings['collision_coverage']
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Rock Paper Scissors Simulation")
        self.clock = pygame.time.Clock()
        
        # --- START OF FINAL FIX ---
        print("Loading local emoji font...")
        self.big_font = load_font(48)
        self.ui_emoji_font = load_font(16)
        MASTER_FONT_SIZE = 128 
        master_emoji_font = load_font(MASTER_FONT_SIZE)
        
        self.master_surfaces = {
            ROCK: master_emoji_font.render(EMOJIS[ROCK], True, BLACK),
            PAPER: master_emoji_font.render(EMOJIS[PAPER], True, BLACK),
            SCISSORS: master_emoji_font.render(EMOJIS[SCISSORS], True, BLACK)
        }
        
        # 2. Define standard text fonts (no longer used for emojis)
        self.text_font = pygame.font.Font(None, 20)
        self.big_font = pygame.font.Font(None, 48)
        # --- END OF FINAL FIX ---
        
        self.objects = []
        self.create_objects()
        
        self.running = True
        self.game_over = False
        self.winner_type = None
        
    def test_emoji_support(self):
        # This function is no longer needed with the new method
        pass
        
    def create_objects(self):
        objects_per_type = self.object_count // 3
        
        for obj_type in [ROCK, PAPER, SCISSORS]:
            for _ in range(objects_per_type):
                attempts = 0
                while attempts < 100:
                    x = random.randint(self.object_size, self.screen_width - self.object_size)
                    y = random.randint(self.object_size, self.screen_height - self.object_size)
                    
                    new_obj = GameObject(x, y, obj_type, self.speed_min, self.speed_max)
                    collision = False
                    for existing_obj in self.objects:
                        if new_obj.collides_with(existing_obj, self.object_size, 1.0):
                            collision = True
                            break
                    
                    if not collision:
                        self.objects.append(new_obj)
                        break
                    attempts += 1
                
                if attempts >= 100:
                    self.objects.append(GameObject(x, y, obj_type, self.speed_min, self.speed_max))
    
    def handle_collisions(self):
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                obj1 = self.objects[i]
                obj2 = self.objects[j]
                
                if obj1.collides_with(obj2, self.object_size, self.collision_coverage):
                    if obj1.type == obj2.type:
                        obj1.speed_x, obj2.speed_x = obj2.speed_x, obj1.speed_x
                        obj1.speed_y, obj2.speed_y = obj2.speed_y, obj1.speed_y
                    else:
                        winner = obj1.battle(obj2)
                        if winner:
                            if winner == obj1:
                                obj2.type = obj1.type
                            else:
                                obj1.type = obj2.type
                        
                        dx = obj2.x - obj1.x
                        dy = obj2.y - obj1.y
                        distance = math.sqrt(dx * dx + dy * dy)
                        if distance > 0:
                            overlap = (self.object_size * self.collision_coverage) - distance
                            dx_normalized = dx / distance
                            dy_normalized = dy / distance
                            obj1.x -= dx_normalized * (overlap / 2)
                            obj1.y -= dy_normalized * (overlap / 2)
                            obj2.x += dx_normalized * (overlap / 2)
                            obj2.y += dy_normalized * (overlap / 2)
    
    def check_game_over(self):
        if len(self.objects) == 0:
            return
        first_type = self.objects[0].type
        if all(obj.type == first_type for obj in self.objects):
            self.game_over = True
            self.winner_type = first_type
    
    def draw_object(self, obj):
        master_surface = self.master_surfaces[obj.type]
        desired_size = (self.object_size, self.object_size)
        scaled_surface = pygame.transform.smoothscale(master_surface, desired_size)
        rotated_surface = pygame.transform.rotate(scaled_surface, obj.rotation)
        rect = rotated_surface.get_rect(center=(int(obj.x), int(obj.y)))
        self.screen.blit(rotated_surface, rect)
    
    def draw(self):
        self.screen.fill(WHITE)
        
        for obj in self.objects:
            self.draw_object(obj)
        
        # --- START OF STATS COUNTER FIX ---
        counts = {ROCK: 0, PAPER: 0, SCISSORS: 0}
        for obj in self.objects:
            counts[obj.type] += 1
        
        y_offset = 10
        UI_EMOJI_SIZE = (18, 18) # Define a fixed size for UI emojis
        for obj_type, count in counts.items():
            # Scale master surface for the UI emoji
            master_surface = self.master_surfaces[obj_type]
            emoji_surface = pygame.transform.smoothscale(master_surface, UI_EMOJI_SIZE)
            
            # Render text part
            name = OBJECT_NAMES[obj_type]
            text_surface = self.text_font.render(f" {name}: {count}", True, BLACK)
            
            self.screen.blit(emoji_surface, (10, y_offset))
            self.screen.blit(text_surface, (10 + UI_EMOJI_SIZE[0], y_offset))
            y_offset += 25
        # --- END OF STATS COUNTER FIX ---

        if self.game_over:
            # --- START OF WINNER MESSAGE FIX ---
            winner_name = OBJECT_NAMES[self.winner_type]
            
            # 1. Render text part
            text_surface = self.big_font.render(f"WINNER: {winner_name}", True, BLACK)
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

            # 2. Scale master surface for the winner emoji
            WINNER_EMOJI_SIZE = (48, 48)
            master_emoji_surface = self.master_surfaces[self.winner_type]
            winner_emoji_surface = pygame.transform.smoothscale(master_emoji_surface, WINNER_EMOJI_SIZE)
            
            # Position the emoji next to the text
            emoji_rect = winner_emoji_surface.get_rect(midleft=(text_rect.right + 10, text_rect.centery))

            # Background for both
            combined_rect = text_rect.union(emoji_rect)
            background_rect = combined_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, WHITE, background_rect)
            pygame.draw.rect(self.screen, BLACK, background_rect, 3)

            # Draw text and emoji
            self.screen.blit(text_surface, text_rect)
            self.screen.blit(winner_emoji_surface, emoji_rect)
            # --- END OF WINNER MESSAGE FIX ---
            
            restart_text = "Press R to restart, ESC to exit"
            restart_surface = self.text_font.render(restart_text, True, BLACK)
            restart_rect = restart_surface.get_rect(center=(self.screen_width // 2, background_rect.bottom + 30))
            self.screen.blit(restart_surface, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.objects = []
                        self.create_objects()
                        self.game_over = False
                        self.winner_type = None
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
            
            if not self.game_over:
                for obj in self.objects:
                    obj.update(self.screen_width, self.screen_height, self.object_size)
                self.handle_collisions()
                self.check_game_over()
            
            self.draw()
            self.clock.tick(DEFAULT_FPS)
        
        pygame.quit()
def main():
    print("Rock Paper Scissors Simulation")
    print("===============================")
    
    # Get settings from user
    dialog = SettingsDialog()
    settings = dialog.get_settings()
    
    if settings is None:
        print("Game cancelled by user.")
        return
    
    print(f"Starting game with settings:")
    print(f"Screen: {settings['screen_width']}x{settings['screen_height']}")
    print(f"Objects: {settings['object_count']} (size: {settings['object_size']})")
    print(f"Speed: {settings['speed_min']} - {settings['speed_max']}")
    print(f"Collision Coverage: {int(settings['collision_coverage'] * 100)}%")
    print("\nControls:")
    print("R - Restart game")
    print("ESC - Exit game")
    print()
    
    # Start game
    game = Game(settings)
    game.run()

if __name__ == "__main__":
    main()