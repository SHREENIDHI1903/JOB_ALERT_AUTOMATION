import ollama
import json
import logging

logger = logging.getLogger(__name__)

class JobAgent:
    def __init__(self, model="llama3.2:3b"):
        self.model = model

    def analyze_job(self, job_data, user_preferences):
        """
        Uses Ollama to analyze and score a job based on user preferences.
        """
        prompt = f"""
        You are a career assistant. Analyze the following job posting against the user's preferences.
        
        User Preferences:
        {user_preferences}
        
        Job Details:
        Title: {job_data['title']}
        Company: {job_data['company']}
        Location: {job_data['location']}
        
        Tasks:
        1. Score the job from 0 to 10 based on how well it matches the preferences.
        2. Provide a brief 1-sentence explanation for the score.
        
        Return ONLY a JSON object in this format:
        {{"score": 8.5, "explanation": "The job matches the Python requirement and location preference."}}
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            
            # Extract JSON from response more robustly
            content = response['message']['content']
            
            # 1. Try to find JSON between backticks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            # 2. Try to find the first '{' and last '}'
            try:
                start = content.find("{")
                end = content.rfind("}")
                if start != -1 and end != -1:
                    content = content[start:end+1]
            except:
                pass

            result = json.loads(content)
            
            # Ensure score is a float
            score = float(result.get('score', 0.0))
            explanation = result.get('explanation', "No explanation provided.")
            
            return score, explanation
            
        except Exception as e:
            logger.error(f"AI Analysis failed: {e}")
            return 0.0, f"Analysis Error: {e}"
