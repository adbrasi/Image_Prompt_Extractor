import os
from PIL import Image
import re
import folder_paths

class ImagePromptExtractor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_path": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "character")
    FUNCTION = "extract_prompts"
    CATEGORY = "image"

    def extract_prompts(self, image_path):
        try:
            # Check if the path is relative to ComfyUI's input directory
            full_path = folder_paths.get_annotated_filepath(image_path)
            if full_path is None:
                full_path = image_path  # Use the provided path if it's not in the input directory

            with Image.open(full_path) as img:
                if img.format != 'PNG':
                    return "Not a PNG image", "Not a PNG image"

                parameters = img.info.get('parameters', '')
                
                # Extract positive prompt (everything before "Negative prompt:")
                positive_prompt = re.split(r'Negative prompt:', parameters, maxsplit=1)[0].strip()
                
                # Extract negative prompt
                negative_match = re.search(r'Negative prompt:(.*?)(?:Steps:|$)', parameters, re.DOTALL)
                negative_prompt = negative_match.group(1).strip() if negative_match else "No negative prompt found"

                return positive_prompt, negative_prompt

        except Exception as e:
            return f"Error: {str(e)}", f"Error: {str(e)}"

NODE_CLASS_MAPPINGS = {
    "ImagePromptExtractor": ImagePromptExtractor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImagePromptExtractor": "Image Prompt Extractor"
}
