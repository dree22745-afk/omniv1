# utils/image_generator.py

import google.generativeai as genai
import os
import time
import requests
from PIL import Image
from io import BytesIO
import base64

class ImageGenerator:
    """Image Generation using Gemini Imagen"""
    
    def __init__(self):
        api_key = os.environ.get('GEMINI_API_KEY', '')
        if not api_key:
            raise Exception("Gemini API key not found!")
        
        genai.configure(api_key=api_key)
        
        # Use Gemini Pro for image generation
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Image storage directory
        self.image_dir = "generated_images"
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
    
    def generate_image(self, prompt, scene_number, style="cinematic"):
        """Generate image for a scene"""
        
        try:
            # Enhance prompt with style and quality keywords
            enhanced_prompt = f"""
            {prompt}
            Style: {style}, professional photography, high quality, 4K, 
            cinematic lighting, detailed, sharp focus, professional color grading,
            suitable for video background, no text overlay, no watermark
            """
            
            # Generate image using Gemini
            response = self.model.generate_content(
                [
                    "Generate a high-quality image based on this description.",
                    enhanced_prompt
                ],
                generation_config={
                    'temperature': 0.8,
                    'top_p': 0.95,
                    'top_k': 40,
                }
            )
            
            # Save image
            image_path = f"{self.image_dir}/scene_{scene_number}.png"
            
            # Check if response contains image
            if hasattr(response, 'image') and response.image:
                with open(image_path, 'wb') as f:
                    f.write(response.image.data)
                return True, image_path
            
            # Alternative: Try text-based image generation
            else:
                # Fallback - create a placeholder image with text
                return self.create_placeholder_image(prompt, scene_number)
                
        except Exception as e:
            print(f"Image generation error: {str(e)}")
            return self.create_placeholder_image(prompt, scene_number)
    
    def create_placeholder_image(self, prompt, scene_number):
        """Create a placeholder image when generation fails"""
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a gradient background image
            width, height = 1920, 1080
            image = Image.new('RGB', (width, height), color=(20, 20, 40))
            draw = ImageDraw.Draw(image)
            
            # Add gradient effect
            for i in range(height):
                r = int(20 + (i / height) * 40)
                g = int(20 + (i / height) * 30)
                b = int(40 + (i / height) * 60)
                draw.line([(0, i), (width, i)], fill=(r, g, b))
            
            # Add scene number
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            text = f"Scene {scene_number}"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_x = (width - text_bbox[2]) // 2
            text_y = (height - text_bbox[3]) // 2
            
            draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
            
            # Add prompt preview
            prompt_preview = prompt[:80] + "..." if len(prompt) > 80 else prompt
            try:
                small_font = ImageFont.truetype("arial.ttf", 30)
            except:
                small_font = ImageFont.load_default()
            
            draw.text((100, height - 100), prompt_preview, fill=(200, 200, 200), font=small_font)
            
            # Save
            image_path = f"{self.image_dir}/scene_{scene_number}.png"
            image.save(image_path)
            
            return True, image_path
            
        except Exception as e:
            return False, f"Placeholder creation failed: {str(e)}"
    
    def generate_all_scene_images(self, scene_plan):
        """Generate images for all scenes"""
        
        image_paths = []
        
        for scene in scene_plan['scenes']:
            scene_num = scene['scene_number']
            prompt = scene['image_prompt']
            
            print(f"Generating image for scene {scene_num}...")
            
            success, path = self.generate_image(prompt, scene_num)
            
            if success:
                image_paths.append({
                    'scene_number': scene_num,
                    'path': path,
                    'prompt': prompt
                })
                print(f"Scene {scene_num} image saved: {path}")
            else:
                print(f"Failed to generate scene {scene_num}: {path}")
                image_paths.append({
                    'scene_number': scene_num,
                    'path': None,
                    'error': path
                })
            
            # Small delay to avoid rate limits
            time.sleep(1)
        
        return image_paths
    
    def cleanup_images(self):
        """Delete all generated images"""
        import shutil
        if os.path.exists(self.image_dir):
            shutil.rmtree(self.image_dir)
            os.makedirs(self.image_dir)