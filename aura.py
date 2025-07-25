import os
import time
import shutil
from PIL import Image
import pygame
import subprocess

# === CONFIGURATION ===
VIDEO_PATH = "assets/video.mp4"
AUDIO_PATH = "assets/audio.mp3"
FPS = 30
WIDTH = 100
FRAMES_DIR = "frames"
ASCII_DIR = "ascii_frames"
FONT_SIZE = 10
FONT_NAME = "Courier New"  # Monospace font

# ASCII characters ordered by increasing brightness
ASCII_CHARS = " .,:;irsXA253hMHGS#9B&@"

# === STEP 1: SETUP DIRECTORIES ===
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(ASCII_DIR, exist_ok=True)

# === STEP 2: EXTRACT FRAMES FROM VIDEO ===
def extract_frames():
    print("Preping the land...")
    shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    os.makedirs(FRAMES_DIR)
    ffmpeg_cmd = [
        "C:/ffmpeg-7.1.1-essentials_build/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe",
        "-i", VIDEO_PATH,
        "-vf", f"fps={FPS}",
        f"{FRAMES_DIR}/frame_%04d.png",
        "-hide_banner", "-loglevel", "error"
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    print("Planting the seeds.")

# === STEP 3: CONVERT IMAGES TO ASCII ===
def pixel_to_char(pixel):
    gamma = 2.2
    brightness = pixel / 255.0
    corrected = brightness ** gamma
    index = int(corrected * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]

def image_to_ascii(path, width=WIDTH):
    img = Image.open(path).convert('L')
    wpercent = width / img.width
    hsize = int(img.height * wpercent * 0.55)
    img = img.resize((width, hsize))
    pixels = img.getdata()
    ascii_str = "".join([pixel_to_char(p) for p in pixels])
    return "\n".join([ascii_str[i:i+width] for i in range(0, len(ascii_str), width)])

def convert_frames_to_ascii():
    print("Watering seeds...")
    shutil.rmtree(ASCII_DIR, ignore_errors=True)
    os.makedirs(ASCII_DIR)
    for file in sorted(os.listdir(FRAMES_DIR)):
        if file.endswith(".png"):
            path = os.path.join(FRAMES_DIR, file)
            ascii_art = image_to_ascii(path)
            with open(os.path.join(ASCII_DIR, f"{file}.txt"), "w") as f:
                f.write(ascii_art)
    print("Harvest period incoming")

# === STEP 4: RENDER ON STATIC PYGAME CANVAS ===
def play_ascii_video_canvas():
    print("...")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_PATH)
    pygame.mixer.music.play()

    # Load all ASCII frames
    frames = []
    for file in sorted(os.listdir(ASCII_DIR)):
        with open(os.path.join(ASCII_DIR, file), "r") as f:
            frames.append(f.read())

    # Calculate window size from ASCII lines and characters
    lines = frames[0].splitlines()
    cols = len(lines[0])
    rows = len(lines)
    screen_width = cols * FONT_SIZE // 1.6
    screen_height = rows * FONT_SIZE

    screen = pygame.display.set_mode((int(screen_width), int(screen_height)))
    pygame.display.set_caption("🟩 ASCII Video Player")
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    green = (0, 255, 0)
    black = (0, 0, 0)

    print("😎Aura farm success!!😎...")

    clock = pygame.time.Clock()
    frame_time = 1.0 / FPS
    start_time = time.time()

    running = True
    try:
        for i, frame in enumerate(frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_time = time.time()
            target_time = start_time + i * frame_time
            if current_time < target_time:
                time.sleep(target_time - current_time)

            screen.fill(black)
            lines = frame.splitlines()
            for y, line in enumerate(lines):
                text_surface = font.render(line, True, green)
                screen.blit(text_surface, (5, y * FONT_SIZE))
            pygame.display.flip()

            clock.tick(FPS)

            if not running:
                break

    except KeyboardInterrupt:
        print("\n⏹ Stopped by user.")
    finally:
        pygame.quit()
        pygame.mixer.music.stop()

# === MAIN ===
if __name__ == "__main__":
    print("🎞 ASCII Video Terminal Player")
    print("==============================")
    extract_frames()
    convert_frames_to_ascii()
    play_ascii_video_canvas()
