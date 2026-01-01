import re

def clean_question(question:str)->str:
        """
    Normalize user question for reliable retrieval.
    """
        question=question.strip()
        question=re.sub(r"\s+", " ", question)
        return question

