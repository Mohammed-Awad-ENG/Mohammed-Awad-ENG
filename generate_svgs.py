import urllib.request
import math
import sys
try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "requests"])
    from PIL import Image
import requests
from io import BytesIO

url = "https://github.com/Mohammed-Awad-ENG.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content)).convert('L')

# Resize image for ASCII
width = 50
aspect_ratio = img.height / img.width
height = int(aspect_ratio * width * 0.5)
img = img.resize((width, height))

chars = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]
try:
    pixels = list(img.get_flattened_data())
except AttributeError:
    pixels = list(img.getdata())

# Apply circular mask
cx = width / 2.0 - 0.5
cy = height / 2.0 - 0.5

new_pixels = []
for i, pixel in enumerate(pixels):
    x = i % width
    y = i // width
    
    # Normalized ellipse distance
    # We use width/2 and height/2 as the radii
    dx = (x - cx) / (width / 2.0)
    dy = (y - cy) / (height / 2.0)
    
    if dx*dx + dy*dy > 1.0:
        new_pixels.append(" ")
    else:
        new_pixels.append(chars[min(int(pixel/25.6), 9)] if pixel < 255 else " ")

new_pixels = ''.join(new_pixels)
ascii_lines = [new_pixels[index:index + width] for index in range(0, len(new_pixels), width)]

json_text = """
{
  "name": "Mohammed Awad",
  "title": "Full Stack Web Developer",
  "skills": {
    "mobile": ["Flutter", "Dart"],
    "frontend": [
      "React", "TypeScript", 
      "Tailwind CSS", "Sass"
    ],
    "backend": [
      "Node.js", "Python", 
      "C++"
    ],
    "api": ["Socket.io", "Express", "REST"],
    "database": [
      "MongoDB", "MySQL", 
      "SQLite"
    ]
  },
  "focus": "System Design & Integration",
  "mission": "Turning complex problems into
              elegant, functional solutions."
}
""".strip().split('\n')

def create_svg(filename, bg_color, text_color, ascii_color, prompt_color, string_color, bracket_color, theme_name):
    svg_width = 950
    svg_height = max(len(ascii_lines), len(json_text) + 4) * 16 + 80
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
    <rect width="{svg_width}" height="{svg_height}" fill="{bg_color}" rx="10" ry="10"/>
    '''
    
    # Mac style dots
    svg += f'''
    <circle cx="20" cy="20" r="6" fill="#ff5f56"/>
    <circle cx="40" cy="20" r="6" fill="#ffbd2e"/>
    <circle cx="60" cy="20" r="6" fill="#27c93f"/>
    '''
    if theme_name:
        svg += f'<text x="90" y="24" fill="{text_color}" font-family="Consolas, monospace" font-size="14" opacity="0.5">{theme_name}</text>\n'
    
    # ASCII Art
    y_offset = 60
    for line in ascii_lines:
        safe_line = line.replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&#160;')
        svg += f'<text x="20" y="{y_offset}" fill="{ascii_color}" font-family="Consolas, monospace" font-size="14" font-weight="bold">{safe_line}</text>\n'
        y_offset += 16
        
    # JSON Text
    x_offset = 450
    y_offset = 60
    
    prompt = f'<text x="{x_offset}" y="{y_offset}" fill="{prompt_color}" font-family="Consolas, monospace" font-size="14" font-weight="bold">mohammed@pro-dev:~$ cat profile.json</text>'
    svg += prompt + '\n'
    y_offset += 24
    
    in_string = False
    for line in json_text:
        formatted_line = ""
        parts = line.split('"')
        for i, part in enumerate(parts):
            if i > 0:
                in_string = not in_string
                formatted_line += f'<tspan fill="{string_color}">"</tspan>'
            
            if in_string:
                safe_part = part.replace('&', '&amp;')
                formatted_line += f'<tspan fill="{string_color}">{safe_part}</tspan>'
            else:
                safe_part = part.replace('&', '&amp;').replace(' ', '&#160;').replace('{', f'<tspan fill="{bracket_color}">{{</tspan>').replace('}', f'<tspan fill="{bracket_color}">}}</tspan>').replace('[', f'<tspan fill="{bracket_color}">[</tspan>').replace(']', f'<tspan fill="{bracket_color}">]</tspan>')
                formatted_line += f'<tspan fill="{text_color}">{safe_part}</tspan>'
            
        svg += f'<text x="{x_offset}" y="{y_offset}" font-family="Consolas, monospace" font-size="14">{formatted_line}</text>\n'
        y_offset += 18
        
    svg += '</svg>'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)

# Approach B: Classic Retro
create_svg('profile.svg', 
           bg_color='#000000', 
           text_color='#00ff00', 
           ascii_color='#00aa00', 
           prompt_color='#00ff00', 
           string_color='#00ff00', 
           bracket_color='#00ff00',
           theme_name='')

print("Generated profile.svg!")
