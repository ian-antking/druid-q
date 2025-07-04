import json
from pathlib import Path
import openai

class LLMClient:
    def __init__(self, api_key: str = None, model: str = "gpt-4", lights: str = "", lighting_context: str = ""):
        if not api_key:
            raise ValueError("LLM API key not provided or missing from environment")

        openai.api_key = api_key
        self.lights = lights
        self.lighting_context = lighting_context
        self.model = model

        with open(Path(__file__).parent / "schema.txt", "r", encoding="utf-8") as f:
            self.schema = f.read()

    def generate_scene_design(self, scene_name, scene_description):
        messages = [
            {"role": "system", "content": "You are an expert lighting designer for immersive tabletop gaming sessions."},
            {"role": "system", "content": f"You have access to these lights: {self.lights}"},
            {"role": "system", "content": f"Please provide your responses in a valid JSON array, using this schema: {self.schema}"},
            {"role": "system", "content": f"Please respond in JSON only, with no other text"}
        ]

        if self.lighting_context:
            messages.append({"role": "system", "content": f"And this additional context: {self.lighting_context}"})
        
        messages.append({"role": "user", "content": f"Please generate a lighting scheme for scene: {scene_name}, description: {scene_description}"})

        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse JSON from LLM output: " + content)
