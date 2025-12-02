import sys
import time
import random

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def type_print(text, speed=0.03, color=GREEN):
    """Simulates typing effect."""
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed * random.uniform(0.5, 1.5))
    sys.stdout.write(RESET + "\n")

def hacker_loader(label, duration=2):
    """Displays a retro progress bar."""
    sys.stdout.write(f"{CYAN}{label} [{RESET}")
    steps = 20
    for i in range(steps):
        time.sleep(duration / steps)
        sys.stdout.write(f"{GREEN}#{RESET}")
        sys.stdout.flush()
    sys.stdout.write(f"{CYAN}] DONE{RESET}\n")

def print_banner():
    """Prints the ZKputer ASCII Art."""
    banner = f"""{GREEN}
    ███████╗██╗  ██╗██████╗ ██╗   ██╗████████╗███████╗██████╗ 
    ╚══███╔╝██║ ██╔╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗
      ███╔╝ █████╔╝ ██████╔╝██║   ██║   ██║   █████╗  ██████╔╝
     ███╔╝  ██╔═██╗ ██╔═══╝ ██║   ██║   ██║   ██╔══╝  ██╔══██╗
    ███████╗██║  ██╗██║     ╚██████╔╝   ██║   ███████╗██║  ██║
    ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
    {RESET}{CYAN}   >>> THE SOVEREIGN SHADOW TRADER <<<{RESET}
    """
    print(banner)

def log(level, message):
    """Structured logging."""
    timestamp = time.strftime("%H:%M:%S")
    if level == "INFO":
        color = GREEN
    elif level == "WARN":
        color = YELLOW
    elif level == "ERROR":
        color = RED
    else:
        color = RESET
    
    print(f"{BOLD}[{timestamp}]{RESET} {color}[{level}]{RESET} {message}")
