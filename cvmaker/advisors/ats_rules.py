"""
Bullet Point Quality Analyzer & ATS Compliance Rules.
Checks for:
1. Strong leading action verbs (vs weak/passive phrasing like 'Responsible for')
2. Measurable impact / quantifiable results (numbers, %, $, timeframes)
3. Ideal length and conciseness (avoids run-on or overly brief bullets)
4. Red-flag outdated personal information (marital status, DOB, etc.)
"""
import re
from typing import List, Dict, Any, Tuple
from .verbs import ALL_ACTION_VERBS

# Weak or passive openers that dilute resume impact
WEAK_OPENERS = [
    r"^responsible for",
    r"^duties included",
    r"^worked on",
    r"^handled",
    r"^helped with",
    r"^assisted in",
    r"^participated in",
    r"^tasked with",
    r"^involved in",
    r"^in charge of",
]

# Patterns representing metrics and quantifiable outcomes
METRIC_PATTERNS = [
    r"\b\d+%",                    # Percentages (e.g. 25%, 100%)
    r"[\$€£₹]\s?\d+",             # Currency amounts ($50k, ₹20L)
    r"\b\d+\s?(k|m|b|x)\b",       # Multipliers or shorthand (10x, 50k, 2M)
    r"\b\d+\+?\s?(users|clients|customers|students|engineers|developers|members|projects|features|teams)\b",
    r"\b(reduced|increased|improved|saved|cut|boosted|grew)\b.*\b\d+", # Action + Number
    r"\b\d+\s?(hours|days|weeks|months|seconds|ms)\b",
]

# Red-flag personal info from outdated templates
RED_FLAG_PATTERNS = [
    (r"\bmarital status\b", "Marital status should be removed to comply with global non-discrimination standards."),
    (r"\bdate of birth\b|\bd\.o\.b\b", "Date of birth is unnecessary and can introduce age bias."),
    (r"\breligion\b|\bcaste\b", "Religious or personal background info should not appear on professional resumes."),
    (r"\bcurrent ctc\b|\bexpected ctc\b|\bsalary\b", "Compensation details should be negotiated during interviews, not disclosed on the resume."),
    (r"\bdeclaration\b.*declare that", "Formal 'declaration' statements are obsolete and waste space."),
]


def analyze_bullet_point(text: str) -> Dict[str, Any]:
    """
    Evaluates a single resume bullet point and returns score (0-100) and suggestions.
    """
    text_clean = text.strip()
    if not text_clean:
        return {"score": 0, "issues": ["Bullet is empty"], "suggestions": []}

    issues: List[str] = []
    suggestions: List[str] = []
    score = 100

    # 1. Check for weak openers
    for pattern in WEAK_OPENERS:
        if re.search(pattern, text_clean, re.IGNORECASE):
            score -= 30
            issues.append("Begins with passive phrasing (e.g., 'Responsible for').")
            suggestions.append("Start with a powerful action verb like 'Spearheaded', 'Engineered', 'Orchestrated', or 'Streamlined'.")
            break

    # 2. Check if first word is an action verb
    words = re.findall(r"\b[A-Za-z]+(?:'[a-z]+)?\b", text_clean)
    if words:
        first_word = words[0].lower()
        if first_word not in ALL_ACTION_VERBS and not any(re.search(p, text_clean, re.IGNORECASE) for p in WEAK_OPENERS):
            score -= 15
            issues.append(f"Opening word '{words[0]}' may not be a strong action verb.")
            suggestions.append("Consider replacing the opening word with a recognized action verb.")

    # 3. Check for quantifiable metrics (PAR / CAR principle)
    has_metric = any(re.search(pat, text_clean, re.IGNORECASE) for pat in METRIC_PATTERNS)
    if not has_metric:
        score -= 25
        issues.append("No quantifiable metrics or numbers detected.")
        suggestions.append("Add measurable impact: How much did you improve efficiency, save time, grow users, or reduce costs? (e.g., 'cutting latency by 35%').")

    # 4. Check length (Ideal is ~12 to 28 words)
    word_count = len(words)
    if word_count < 7:
        score -= 20
        issues.append("Bullet is very short; lacks context or outcome.")
        suggestions.append("Expand using the CAR format: Challenge/Context + Action taken + Result achieved.")
    elif word_count > 35:
        score -= 15
        issues.append("Bullet is quite long (run-on sentence).")
        suggestions.append("Split into two punchy bullets or trim filler words for better readability.")

    return {
        "score": max(10, min(100, score)),
        "issues": issues,
        "suggestions": suggestions,
        "has_metric": has_metric,
        "starts_with_action_verb": (score > 70)
    }


def scan_for_red_flags(full_text: str) -> List[Tuple[str, str]]:
    """Scans resume content for outdated or risky resume content."""
    findings = []
    for pattern, explanation in RED_FLAG_PATTERNS:
        if re.search(pattern, full_text, re.IGNORECASE):
            findings.append((pattern, explanation))
    return findings
