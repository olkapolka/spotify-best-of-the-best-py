"""
Text analysis utilities for extracting insights from text data
"""

import pandas as pd
from collections import Counter
from typing import List, Dict
import re


class TextAnalyzer:
    """Class for analyzing text data in the dataset"""
    
    def __init__(self, texts: List[str]):
        """
        Initialize TextAnalyzer with a list of texts
        
        Args:
            texts: List of text strings to analyze
        """
        self.texts = [str(text) for text in texts if pd.notna(text)]
        
    def get_word_frequency(self, top_n: int = 20) -> Dict[str, int]:
        """
        Get the most common words across all texts
        
        Args:
            top_n: Number of top words to return
            
        Returns:
            Dictionary of word frequencies
        """
        all_words = []
        for text in self.texts:
            # Simple word tokenization (lowercase and split)
            words = re.findall(r'\b\w+\b', text.lower())
            all_words.extend(words)
            
        word_counts = Counter(all_words)
        return dict(word_counts.most_common(top_n))
    
    def get_average_length(self) -> float:
        """
        Calculate average text length
        
        Returns:
            Average length of texts
        """
        if not self.texts:
            return 0.0
        return sum(len(text) for text in self.texts) / len(self.texts)
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Get comprehensive text statistics
        
        Returns:
            Dictionary containing various text statistics
        """
        if not self.texts:
            return {
                'total_texts': 0,
                'average_length': 0.0,
                'min_length': 0,
                'max_length': 0,
                'total_words': 0
            }
            
        lengths = [len(text) for text in self.texts]
        word_counts = [len(text.split()) for text in self.texts]
        
        return {
            'total_texts': len(self.texts),
            'average_length': sum(lengths) / len(lengths),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'total_words': sum(word_counts),
            'average_words': sum(word_counts) / len(word_counts)
        }
    
    def search_keyword(self, keyword: str, case_sensitive: bool = False) -> List[str]:
        """
        Search for texts containing a specific keyword
        
        Args:
            keyword: Keyword to search for
            case_sensitive: Whether search should be case-sensitive
            
        Returns:
            List of texts containing the keyword
        """
        results = []
        
        for text in self.texts:
            search_text = text if case_sensitive else text.lower()
            search_keyword = keyword if case_sensitive else keyword.lower()
            
            if search_keyword in search_text:
                results.append(text)
                
        return results
    
    def get_unique_values(self) -> List[str]:
        """
        Get unique text values
        
        Returns:
            List of unique text values
        """
        return list(set(self.texts))


def analyze_column_text(df: pd.DataFrame, column_name: str) -> Dict:
    """
    Analyze text data in a specific DataFrame column
    
    Args:
        df: Input DataFrame
        column_name: Name of the column to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")
    
    analyzer = TextAnalyzer(df[column_name].tolist())
    
    return {
        'statistics': analyzer.get_statistics(),
        'top_words': analyzer.get_word_frequency(20),
        'unique_count': len(analyzer.get_unique_values())
    }
