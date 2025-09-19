import json
from pathlib import Path
import openai

class LLMClient:
    def __init__(self, api_key: str = None, model: str = "gpt-4o-2024-08-06", lights: str = "", lighting_context: str = ""):
        if not api_key:
            raise ValueError("LLM API key not provided or missing from environment")

        self.client = openai.OpenAI(api_key=api_key)
        self.lights = lights
        self.lighting_context = lighting_context
        self.model = model

        schema_path = Path(__file__).parent / "schema.json"
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def generate_scene_design(self, scene_name, scene_description):
        messages = [
            {"role": "system", "content": "You are an expert lighting designer for immersive tabletop gaming sessions. Your response must conform to the provided JSON schema."},
            {"role": "system", "content": f"You have access to these lights: {self.lights}"},
        ]

        if self.lighting_context:
            messages.append({"role": "system", "content": f"And this additional context: {self.lighting_context}"})
        
        messages.append({"role": "user", "content": f"Please generate a lighting scheme for scene: {scene_name}, description: {scene_description}"})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "lighting_design_schema",
                    "strict": True,
                    "schema": self.schema
                }
            }
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse JSON from LLM output, which is unexpected with json_schema mode: " + content)