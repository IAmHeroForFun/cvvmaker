"""
Offline Job Description Keyword Matcher.
Extracts key technical skills, tools, and domain keywords from a pasted job description
and compares them against the resume to highlight missing matching terms.
Requires zero external network or heavy ML models.
"""
import re
from collections import Counter
from typing import Dict, List, Set, Any, Tuple
from ..models.resume import Resume

# Common English stop words to ignore during frequency analysis
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but",
    "by", "can", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for",
    "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
    "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just",
    "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "same", "she",
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom",
    "why", "with", "would", "you", "your", "yours", "yourself", "yourselves",
    # Resume-specific common filler terms
    "responsibilities", "requirements", "experience", "candidate", "qualifications", "working",
    "ability", "role", "position", "preferred", "including", "knowledge", "environment",
    "opportunity", "equal", "employment", "years", "plus", "must", "well"
}


def extract_keywords(text: str, top_n: int = 30) -> List[Tuple[str, int]]:
    """Extracts high-significance keyword tokens from raw job posting text."""
    # Find words with potential programming characters (e.g., C++, C#, .NET, Node.js)
    raw_tokens = re.findall(r"\b[A-Za-z0-9+#\.\-]{2,25}\b", text.lower())
    
    cleaned_tokens = [
        t.strip(".") for t in raw_tokens
        if t.strip(".") not in STOP_WORDS and not t.isdigit() and len(t.strip(".")) > 2
    ]
    
    counts = Counter(cleaned_tokens)
    return counts.most_common(top_n)


def match_resume_to_job(resume: Resume, job_description: str) -> Dict[str, Any]:
    """
    Compares resume text against job description keywords.
    Returns:
      - match_percentage: int (0 to 100)
      - matched_keywords: list of strings
      - missing_keywords: list of strings
    """
    if not job_description.strip():
        return {
            "match_percentage": 0,
            "matched_keywords": [],
            "missing_keywords": []
        }

    # Aggregate all resume text
    resume_text_parts = [
        resume.target_role,
        resume.summary,
        " ".join([h for exp in resume.experience for h in exp.highlights]),
        " ".join([f"{exp.position} {exp.company}" for exp in resume.experience]),
        " ".join([f"{edu.degree} {edu.field_of_study}" for edu in resume.education]),
        " ".join([f"{proj.name} {proj.technologies} " + " ".join(proj.highlights) for proj in resume.projects]),
        " ".join([f"{cat.category} " + " ".join(cat.skills) for cat in resume.skill_categories]),
        " ".join([cert.name for cert in resume.certifications]),
    ]
    full_resume_text = " ".join(resume_text_parts).lower()

    # Extract top job keywords
    top_job_tokens = extract_keywords(job_description, top_n=25)
    if not top_job_tokens:
        return {"match_percentage": 100, "matched_keywords": [], "missing_keywords": []}

    matched = []
    missing = []

    for word, _freq in top_job_tokens:
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, full_resume_text):
            matched.append(word)
        else:
            missing.append(word)

    total = len(top_job_tokens)
    match_pct = int(round((len(matched) / total) * 100)) if total > 0 else 0

    return {
        "match_percentage": match_pct,
        "matched_keywords": matched,
        "missing_keywords": missing
    }
