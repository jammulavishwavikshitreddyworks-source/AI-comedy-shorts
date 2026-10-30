import os, json, random, subprocess, textwrap
from pathlib import Path
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
OUT = Path("output")
OUT.mkdir(exist_ok=True)

# Original, reusable comedy formats. Add new story objects to expand the library.
STORIES = [
    {
        "title": "THE ROBOT'S FIRST DAY AT WORK",
        "scenes": [
            ("BOSS", "Welcome! Your job is to make the team more productive.", "😎"),
            ("ROBOT", "Understood. I have analysed the office.", "🤖"),
            ("BOSS", "Great. What is your first suggestion?", "😎"),
            ("ROBOT", "Step one: remove the boss. Productivity rises 300%.", "🤖"),
        ],
        "description": "A robot's first day at the office takes an unexpected turn. Original AI-style comedy short."
    },
    {
        "title": "SALARY DAY: 5 SECONDS OF HAPPINESS",
        "scenes": [
            ("EMPLOYEE", "Salary day! Today I am officially rich!", "😁"),
            ("PHONE", "Rent payment successful.", "📱"),
            ("PHONE", "Loan payment successful.", "📱"),
            ("EMPLOYEE", "Can somebody send me a salary notification again?", "😭"),
        ],
        "description": "That beautiful moment when salary arrives... and immediately disappears. Original comedy short."
    },
    {
        "title": "THE AI COOKING ASSISTANT",
        "scenes": [
            ("ME", "AI, make me a simple dinner.", "🙂"),
            ("AI", "Certainly. I have selected a beginner recipe.", "🤖"),
            ("ME", "Why is the smoke alarm ringing?", "😳"),
            ("AI", "Dinner is ready. The kitchen is now extra crispy.", "🤖"),
        ],
        "description": "Never leave dinner entirely to your AI assistant. Original comedy short."
    },
    {
        "title": "THE MOST HONEST JOB INTERVIEW",
        "scenes": [
            ("INTERVIEWER", "Where do you see yourself in five years?", "🧑‍💼"),
            ("ROBOT", "In your chair.", "🤖"),
            ("INTERVIEWER", "And why should we hire you?", "🧑‍💼"),
            ("ROBOT", "You just answered your own question.", "🤖"),
        ],
        "description": "An unusually honest job interview. Original comedy short."
    },
    {
        "title": "WHEN THE BOSS SAYS 'QUICK CALL'",
        "scenes": [
            ("BOSS", "Quick call. Only five minutes.", "😎"),
            ("EMPLOYEE", "Perfect. I have lunch in ten minutes.", "🙂"),
            ("BOSS", "Let's review the 47-slide presentation.", "😈"),
            ("EMPLOYEE", "Please send my lunch to the meeting room.", "😭"),
        ],
        "description": "The five-minute meeting that lasts forever. Original office comedy short."
    }
]

def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_scene(story_title, speaker, line, face, index, total):
    # A simple original graphic-comedy layout. No third-party footage or characters.
    palettes = [("#101B36", "#263D69"), ("#172B35", "#315C61"), ("#302044", "#65416D"), ("#3B2630", "#75424A")]
    c1, c2 = palettes[index % len(palettes)]
    im = Image.new("RGB", (W, H), c1)
    pix = im.load()
    top = tuple(int(c1[i:i+2], 16) for i in (1,3,5))
    bot = tuple(int(c2[i:i+2], 16) for i in (1,3,5))
    for y in range(H):
        t = y / H
        col = tuple(int(top[k]*(1-t)+bot[k]*t) for k in range(3))
        for x in range(W):
            pix[x,y] = col
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((35, 45, W-35, 170), radius=28, fill="#F5F1E8")
    title_lines = textwrap.wrap(story_title, width=27)
    y = 65
    for tl in title_lines[:2]:
        d.text((W//2, y), tl, font=font(29, True), fill="#172033", anchor="mm")
        y += 42

    # Draw a friendly generic cartoon face/robot icon from shapes.
    cx, cy = W//2, 440
    d.ellipse((cx-150, cy-150, cx+150, cy+150), fill="#F5D6B8", outline="#172033", width=10)
    d.ellipse((cx-75, cy-35, cx-35, cy+10), fill="#172033")
    d.ellipse((cx+35, cy-35, cx+75, cy+10), fill="#172033")
    d.arc((cx-65, cy+5, cx+65, cy+100), start=10, end=170, fill="#172033", width=10)
    d.rounded_rectangle((cx-205, cy+135, cx+205, cy+300), radius=65, fill="#F5F1E8", outline="#172033", width=8)
    d.text((cx, cy+215), speaker, font=font(32, True), fill="#172033", anchor="mm")

    d.rounded_rectangle((38, 830, W-38, 1155), radius=34, fill="#FFFDF7", outline="#172033", width=7)
    words = textwrap.wrap(line, width=31)
    total_h = len(words) * 58
    yy = 992 - total_h//2
    for wordline in words:
        d.text((W//2, yy), wordline, font=font(39, True), fill="#172033", anchor="mm")
        yy += 58
    d.text((W//2, 1215), f"FOLLOW FOR MORE ORIGINAL AI COMEDY  •  {index+1}/{total}",
           font=font(18, True), fill="#FFFFFF", anchor="mm")
    return im

def main():
    random.seed(datetime.now(timezone.utc).strftime("%Y-%m-%d") + os.getenv("SLOT", "A"))
    story = random.choice(STORIES)
    # Store the selection so the uploader can read metadata.
    meta = {
        "title": story["title"] + " 😂 #Shorts",
        "description": story["description"] + "\n\n#shorts #comedy #aicomedy",
        "tags": ["shorts", "comedy", "aicomedy", "officecomedy", "funny"],
    }
    (OUT / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    scene_files = []
    for i, (speaker, line, face) in enumerate(story["scenes"]):
        p = OUT / f"scene_{i:02d}.png"
        draw_scene(story["title"], speaker, line, face, i, len(story["scenes"])).save(p)
        scene_files.append(p)

    # Generate narration using free system speech synthesis (espeak-ng).
    # Keep voice neutral; no imitation of real people.
    narration = " ".join(f"{speaker} says: {line}" for speaker, line, _ in story["scenes"])
    wav = OUT / "voice.wav"
    subprocess.run(["espeak-ng", "-v", "en", "-s", "158", "-w", str(wav), narration], check=True)

    concat = OUT / "scenes.txt"
    with concat.open("w", encoding="utf-8") as f:
        for p in scene_files:
            f.write(f"file '{p.resolve()}'\nduration 4.8\n")
        f.write(f"file '{scene_files[-1].resolve()}'\n")

    mp4 = OUT / "short.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-i", str(wav), "-vf", "scale=720:1280,format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-r", "30",
        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart",
        str(mp4)
    ], check=True)
    print(f"Created {mp4} using story: {story['title']}")

if __name__ == "__main__":
    main()
