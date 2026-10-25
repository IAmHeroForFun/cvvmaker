"""
Storage repository and built-in starter resumes adhering to modern global standards.
"""
import os
import json
from typing import Optional
from .resume import (
    Resume,
    ContactInfo,
    ExperienceItem,
    EducationItem,
    ProjectItem,
    SkillCategory,
    CertificationItem,
)


def get_sample_software_engineer_resume() -> Resume:
    """A world-class modern tech resume template based on PAR / CAR results."""
    return Resume(
        title="Software Engineer Resume",
        target_role="Full Stack Software Engineer",
        summary=(
            "Results-driven Full Stack Software Engineer with 4+ years of experience architecting high-throughput "
            "web applications, microservices, and distributed pipelines. Proven track record of improving system latency by 35% "
            "and leading cross-functional teams in agile environments."
        ),
        contact=ContactInfo(
            full_name="Alex Rivera",
            headline="Full Stack Software Engineer",
            email="alex.rivera@example.com",
            phone="+1 (555) 019-2834",
            location="San Francisco, CA",
            linkedin="https://linkedin.com/in/alexrivera-dev",
            github="https://github.com/alexrivera-dev",
            website="https://alexrivera.dev"
        ),
        experience=[
            ExperienceItem(
                company="Nexus Cloud Solutions",
                position="Senior Software Engineer",
                location="San Francisco, CA",
                start_date="2022-03",
                end_date="Present",
                is_current=True,
                highlights=[
                    "Spearheaded redesign of the core messaging pipeline using Python, FastAPI, and Redis, cutting p99 latency by 42%.",
                    "Architected automated CI/CD deployment pipelines on Docker/Kubernetes, reducing release failure rates from 14% to under 1.5%.",
                    "Mentored 5 junior and mid-level developers through rigorous code reviews and bi-weekly architecture brown-bags."
                ]
            ),
            ExperienceItem(
                company="Apex Interactive",
                position="Software Engineer",
                location="Austin, TX",
                start_date="2020-01",
                end_date="2022-02",
                is_current=False,
                highlights=[
                    "Engineered customer dashboard serving 120,000+ daily active users using TypeScript, React, and GraphQL.",
                    "Optimized complex PostgreSQL queries and added multi-tier caching, trimming server memory overhead by 30%.",
                    "Collaborated directly with Product Managers and UX designers to deliver 8 high-priority features on schedule."
                ]
            )
        ],
        education=[
            EducationItem(
                institution="University of California, Berkeley",
                degree="Bachelor of Science",
                field_of_study="Computer Science",
                location="Berkeley, CA",
                start_date="2016",
                end_date="2020",
                grade_or_gpa="3.8 / 4.0",
                highlights=[
                    "Dean's Honors List (6 consecutive semesters)",
                    "Coursework: Distributed Systems, Algorithms, Database Systems, Cloud Computing"
                ]
            )
        ],
        projects=[
            ProjectItem(
                name="TelemetryFlow",
                role="Creator & Lead Developer",
                link="https://github.com/alexrivera-dev/telemetryflow",
                technologies="Python, Rust, ClickHouse, Docker",
                highlights=[
                    "Engineered an open-source real-time metrics aggregator handling up to 50k telemetry events/sec on modest hardware.",
                    "Acquired 1,200+ stars on GitHub and recognized in popular developer newsletters."
                ]
            )
        ],
        skill_categories=[
            SkillCategory(
                category="Programming Languages",
                skills=["Python", "TypeScript", "JavaScript", "Go", "SQL", "HTML/CSS"]
            ),
            SkillCategory(
                category="Frameworks & Libraries",
                skills=["FastAPI", "React", "Next.js", "Django", "Node.js", "PySide6/Qt"]
            ),
            SkillCategory(
                category="Cloud & DevOps",
                skills=["AWS (ECS, S3, RDS)", "Docker", "Kubernetes", "PostgreSQL", "Redis", "Git", "GitHub Actions"]
            )
        ],
        certifications=[
            CertificationItem(
                name="AWS Certified Solutions Architect – Associate",
                issuer="Amazon Web Services",
                issue_date="2023",
                credential_url="https://aws.amazon.com/verification"
            )
        ],
        selected_theme="modern_clean"
    )


def save_resume_to_file(resume: Resume, filepath: str) -> None:
    """Save resume to a JSON file."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(resume.to_json(indent=2))


def load_resume_from_file(filepath: str) -> Resume:
    """Load resume from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return Resume.from_json(f.read())
