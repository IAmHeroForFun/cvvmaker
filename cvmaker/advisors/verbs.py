"""
Curated action verbs categorised by resume impact areas.
Synthesized from 'The Damn Good Resume Guide' (Yana Parker) & 'Modernize Your Resume'.
"""
from typing import Dict, List

ACTION_VERBS_BY_CATEGORY: Dict[str, List[str]] = {
    "Leadership & Management": [
        "Spearheaded", "Directed", "Orchestrated", "Championed", "Guided",
        "Mentored", "Mobilized", "Delegated", "Supervised", "Coordinated",
        "Empowered", "Fostered", "Pioneered", "Steered", "Trained"
    ],
    "Engineering, Tech & Creation": [
        "Architected", "Engineered", "Designed", "Developed", "Implemented",
        "Constructed", "Automated", "Programmed", "Configured", "Deployed",
        "Refactored", "Formulated", "Integrated", "Built", "Optimized"
    ],
    "Optimization & Performance": [
        "Streamlined", "Accelerated", "Maximized", "Minimized", "Eliminated",
        "Revamped", "Overhauled", "Upgraded", "Strengthened", "Standardized",
        "Consolidated", "Enhanced", "Augmented", "Tailored", "Reengineered"
    ],
    "Research, Analysis & Problem-Solving": [
        "Analyzed", "Diagnosed", "Identified", "Investigated", "Evaluated",
        "Audited", "Discovered", "Modeled", "Synthesized", "Validated",
        "Benchmarked", "Quantified", "Mapped", "Assessed", "Parsed"
    ],
    "Communication, Sales & Client Success": [
        "Negotiated", "Influenced", "Presented", "Authored", "Secured",
        "Partnered", "Advocated", "Consulted", "Brokered", "Trained",
        "Facilitated", "Liaised", "Marketed", "Promoted", "Communicated"
    ]
}

# Flat set of lowercase verbs for rapid checking
ALL_ACTION_VERBS = {
    verb.lower()
    for verb_list in ACTION_VERBS_BY_CATEGORY.values()
    for verb in verb_list
}
