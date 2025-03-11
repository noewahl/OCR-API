from llama_cpp import Llama
import os

class LocalLLM:
    def __init__(self, model_path: str = "models/llama-2-7b-chat.Q4_K_M.gguf"):
        """Initialize the local LLM model."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        self.model = Llama(
            model_path=model_path,
            n_ctx=2048,  # Context window
            n_threads=4   # Number of CPU threads to use
        )

    def generate_response(self, prompt: str, max_tokens: int = 512) -> str:
        """Generate a response from the model."""
        response = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.95,
            repeat_penalty=1.1
        )
        return response['choices'][0]['text']