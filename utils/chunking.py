import re

def chunk_text(text: str, max_words: int = 400) -> list[str]:
    """
    Splits text into chunks of approximately `max_words` words,
    trying to avoid breaking sentences.
    """
    if not text:
        return []
        
    # Split text into sentences using simple regex (handles ., !, ?)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        word_count = len(sentence.split())
        
        # If adding this sentence exceeds our limit, and we already have content, finalize chunk
        if current_word_count + word_count > max_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = word_count
        else:
            current_chunk.append(sentence)
            current_word_count += word_count
            
    # Add the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks
