from .model import LocalLLM

class TextSummarizer:
    def __init__(self):
        """Initialize the text summarizer with a local LLM."""
        self.llm = LocalLLM()

    def summarize(self, text: str, max_length: int = 150) -> str:
        """
        Summarize the given text using the local LLM.
        
        Args:
            text (str): The input text to summarize
            max_length (int): Maximum length of the summary in words
            
        Returns:
            str: The generated summary
        """
        prompt = f"""Please provide a concise summary of the following text in no more than {max_length} words. Do not add any new information or commentary.:

Text: {text}

Summary:"""
        
        return self.llm.generate_response(prompt)

    def bullet_points(self, text: str, num_points: int = 5) -> str:
        """
        Extract key points from the text in bullet point format.
        
        Args:
            text (str): The input text to analyze
            num_points (int): Number of key points to extract
            
        Returns:
            str: Bullet points of key information
        """
        prompt = f"""Extract {num_points} main points from the following text in bullet point format:

Text: {text}

Key points:"""
        
        return self.llm.generate_response(prompt)