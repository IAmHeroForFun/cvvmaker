"""
Integration and component tests for CV Maker.
"""
import os
import unittest
from cvmaker.models.resume import Resume, ContactInfo, ExperienceItem
from cvmaker.models.storage import get_sample_software_engineer_resume, save_resume_to_file, load_resume_from_file
from cvmaker.templates.engine import TemplateEngine
from cvmaker.advisors.verbs import ACTION_VERBS_BY_CATEGORY, ALL_ACTION_VERBS
from cvmaker.advisors.ats_rules import analyze_bullet_point, scan_for_red_flags
from cvmaker.advisors.keyword_matcher import match_resume_to_job
from cvmaker.exporter.docx_exporter import DocxExporter


class TestCVMaker(unittest.TestCase):

    def test_resume_serialization(self):
        resume = get_sample_software_engineer_resume()
        json_data = resume.to_json()
        loaded = Resume.from_json(json_data)
        self.assertEqual(loaded.contact.full_name, "Alex Rivera")
        self.assertEqual(len(loaded.experience), 2)
        self.assertEqual(loaded.experience[0].company, "Nexus Cloud Solutions")

    def test_template_rendering(self):
        engine = TemplateEngine()
        resume = get_sample_software_engineer_resume()
        html_clean = engine.render_resume(resume, "modern_clean")
        self.assertIn("Alex Rivera", html_clean)
        self.assertIn("Nexus Cloud Solutions", html_clean)

        html_classic = engine.render_resume(resume, "classic_executive")
        self.assertIn("Alex Rivera", html_classic)
        self.assertIn("Areas of Expertise", html_classic)

    def test_action_verbs_and_rules(self):
        self.assertIn("spearheaded", ALL_ACTION_VERBS)
        self.assertIn("architected", ALL_ACTION_VERBS)

        # High-impact CAR bullet
        strong_bullet = "Spearheaded migration to microservices, slashing API latency by 35% across 200k daily users."
        res_strong = analyze_bullet_point(strong_bullet)
        self.assertGreaterEqual(res_strong["score"], 80)
        self.assertTrue(res_strong["has_metric"])

        # Weak passive bullet
        weak_bullet = "Responsible for handling database maintenance."
        res_weak = analyze_bullet_point(weak_bullet)
        self.assertLess(res_weak["score"], 60)
        self.assertFalse(res_weak["has_metric"])

    def test_red_flag_scanner(self):
        bad_text = "Marital Status: Married, Date of Birth: 1990-01-01, Current CTC: 20 LPA"
        flags = scan_for_red_flags(bad_text)
        self.assertGreaterEqual(len(flags), 3)

        clean_resume = get_sample_software_engineer_resume()
        clean_flags = scan_for_red_flags(clean_resume.to_json())
        self.assertEqual(len(clean_flags), 0)

    def test_offline_job_keyword_matcher(self):
        resume = get_sample_software_engineer_resume()
        job_posting = """
        Looking for a Senior Software Engineer with strong experience in Python, Docker, Kubernetes,
        and PostgreSQL. Nice to have experience with Rust, AWS, and GraphQL.
        """
        match = match_resume_to_job(resume, job_posting)
        self.assertGreater(match["match_percentage"], 50)
        self.assertIn("python", match["matched_keywords"])
        self.assertIn("docker", match["matched_keywords"])

    def test_docx_export(self):
        if DocxExporter.is_available():
            engine = TemplateEngine()
            resume = get_sample_software_engineer_resume()
            html = engine.render_resume(resume)
            out_docx = "/tmp/test_cv_export.docx"
            if os.path.exists(out_docx):
                os.remove(out_docx)
            success, msg = DocxExporter.export_html_to_docx(html, out_docx)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(out_docx))
            self.assertGreater(os.path.getsize(out_docx), 1000)
            if os.path.exists(out_docx):
                os.remove(out_docx)


if __name__ == "__main__":
    unittest.main()
