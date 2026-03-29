"""
Generate a simple placeholder image for when no meme is available.
Run this script once to create the placeholder.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder():
    """Create a simple placeholder image."""
    # Create a 800x600 image with a light gray background
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='#E0E0E0')
    draw = ImageDraw.Draw(img)
    
    # Draw a border
    border_color = '#999999'
    border_width = 5
    draw.rectangle(
        [(border_width, border_width), (width - border_width, height - border_width)],
        outline=border_color,
        width=border_width
    )
    
    # Add text in the center
    text = "No meme available\n\nAdd memes to the\ncorresponding folder!"
    
    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=None)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill='#666666', font=None, align='center')
    
    # Save the image
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'placeholder.png')
    
    img.save(output_path)
    print(f"Placeholder image created: {output_path}")

if __name__ == "__main__":
    create_placeholder()
