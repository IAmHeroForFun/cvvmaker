"""
Jinja2 Template Rendering Engine.
Loads HTML themes, populates them with Resume model data, and returns final HTML.
"""
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from ..models.resume import Resume

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "themes")

THEMES = {
    "modern_clean": "Modern Clean (Tech & Corporate)",
    "classic_executive": "Classic Executive (Traditional & Serif)"
}


class TemplateEngine:
    def __init__(self, template_dir: str = TEMPLATE_DIR):
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(["html", "xml"])
        )

    def render_resume(self, resume: Resume, theme_name: str = None) -> str:
        theme = theme_name or resume.selected_theme or "modern_clean"
        template_file = f"{theme}.html"
        
        try:
            template = self.env.get_template(template_file)
        except Exception:
            # Fallback to modern_clean
            template = self.env.get_template("modern_clean.html")
            
        return template.render(resume=resume)
