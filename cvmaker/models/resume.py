"""
Data models for resume representations.
Fully serializable to/from dictionary and JSON (JSON Resume compatible format).
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json


@dataclass
class ContactInfo:
    full_name: str = ""
    headline: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""  # City, Country or City, State
    linkedin: str = ""
    github: str = ""
    website: str = ""


@dataclass
class ExperienceItem:
    company: str = ""
    position: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    is_current: bool = False
    highlights: List[str] = field(default_factory=list)


@dataclass
class EducationItem:
    institution: str = ""
    degree: str = ""
    field_of_study: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    grade_or_gpa: str = ""
    highlights: List[str] = field(default_factory=list)


@dataclass
class ProjectItem:
    name: str = ""
    role: str = ""
    link: str = ""
    technologies: str = ""
    highlights: List[str] = field(default_factory=list)


@dataclass
class SkillCategory:
    category: str = ""  # e.g., "Languages", "Frameworks", "Tools", "Leadership"
    skills: List[str] = field(default_factory=list)


@dataclass
class CertificationItem:
    name: str = ""
    issuer: str = ""
    issue_date: str = ""
    credential_url: str = ""


@dataclass
class Resume:
    title: str = "My Resume"
    target_role: str = ""
    summary: str = ""
    contact: ContactInfo = field(default_factory=ContactInfo)
    experience: List[ExperienceItem] = field(default_factory=list)
    education: List[EducationItem] = field(default_factory=list)
    projects: List[ProjectItem] = field(default_factory=list)
    skill_categories: List[SkillCategory] = field(default_factory=list)
    certifications: List[CertificationItem] = field(default_factory=list)
    selected_theme: str = "modern_clean"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Resume":
        contact_data = data.get("contact", {})
        contact = ContactInfo(**contact_data) if isinstance(contact_data, dict) else ContactInfo()

        experience = [
            ExperienceItem(**item) if isinstance(item, dict) else item
            for item in data.get("experience", [])
        ]
        education = [
            EducationItem(**item) if isinstance(item, dict) else item
            for item in data.get("education", [])
        ]
        projects = [
            ProjectItem(**item) if isinstance(item, dict) else item
            for item in data.get("projects", [])
        ]
        skill_categories = [
            SkillCategory(**item) if isinstance(item, dict) else item
            for item in data.get("skill_categories", [])
        ]
        certifications = [
            CertificationItem(**item) if isinstance(item, dict) else item
            for item in data.get("certifications", [])
        ]

        return cls(
            title=data.get("title", "My Resume"),
            target_role=data.get("target_role", ""),
            summary=data.get("summary", ""),
            contact=contact,
            experience=experience,
            education=education,
            projects=projects,
            skill_categories=skill_categories,
            certifications=certifications,
            selected_theme=data.get("selected_theme", "modern_clean")
        )

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "Resume":
        return cls.from_dict(json.loads(json_str))
