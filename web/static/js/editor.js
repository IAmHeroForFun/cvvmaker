/**
 * FOLIO — Studio CV Editor & Live A4 Preview Controller
 * Handles two-panel state, live DOM updates, dynamic item management,
 * undo/redo history, local vault auto-save, and print-to-PDF.
 */

// Sample high-caliber profile for quick start
const SAMPLE_RESUME_DATA = {
  selected_theme: 'modern',
  contact: {
    full_name: "Julian Vance",
    headline: "Principal Product Strategist",
    email: "julian.vance@folio.studio",
    phone: "+1 (555) 203-8819",
    location: "San Francisco, CA",
    linkedin: "linkedin.com/in/julianvance",
    github: "github.com/julianvance",
    website: "julianvance.design"
  },
  summary: "Accomplished design strategist with 8+ years leading cross-functional teams in architecting high-throughput SaaS applications. Proven track record turning complex technical infrastructure constraints into elegant, human-centered product workflows.",
  experience: [
    {
      company: "Solstice Platforms",
      position: "Principal Product Designer",
      location: "San Francisco, CA",
      start_date: "2021",
      end_date: "Present",
      is_current: true,
      highlights: [
        "Spearheaded design system unification across 4 web apps, reducing release cycles by 40%.",
        "Redesigned core onboarding funnel, lifting monthly active users from 120k to 1.8M in 14 months.",
        "Authored executive technical specs and partnered with engineering on React/TypeScript components."
      ]
    },
    {
      company: "Nexus Collective",
      position: "Senior Product Strategist",
      location: "New York, NY",
      start_date: "2018",
      end_date: "2021",
      is_current: false,
      highlights: [
        "Delivered 14 enterprise client discovery engagements, achieving a 98% CSAT score.",
        "Instituted quantitative heuristic UX audit rituals, decreasing checkout drop-off by 28%."
      ]
    }
  ],
  education: [
    {
      institution: "UC Berkeley",
      degree: "B.S. in Cognitive Science",
      field_of_study: "Human-Computer Interaction",
      start_date: "2014",
      end_date: "2018",
      grade_or_gpa: "3.9 GPA · Honors"
    }
  ],
  projects: [
    {
      name: "Pulse Analytics Engine",
      role: "Lead Designer & Architect",
      technologies: "React, D3.js, Tailwind, Python",
      link: "github.com/julianvance/pulse",
      highlights: [
        "Architected an open-source real-time telemetry dashboard adopted by 12k+ developers."
      ]
    }
  ],
  skills: "Product Strategy, Systems Architecture, UI/UX Design, React, TypeScript, User Research, Heuristic Audits, Agile Leadership, Prototyping",
  certifications: [
    {
      name: "Enterprise Design Thinking Leader",
      issuer: "IBM Design Program",
      issue_date: "2023",
      credential_url: "credentials.folio.studio/7841"
    }
  ],
  achievements: [
    {
      title: "Fast Company Innovation by Design Nominee",
      organization: "Fast Company",
      year: "2023",
      description: "Recognized for contributions to carbon-neutral enterprise cloud workflows."
    }
  ]
};

// Application State
let resumeState = JSON.parse(JSON.stringify(SAMPLE_RESUME_DATA));
let historyStack = [];
let historyIndex = -1;
let isUndoRedoAction = false;
let autoSaveTimer = null;
let currentZoom = 1.0;

document.addEventListener('DOMContentLoaded', () => {
  // Check URL query parameters for template
  const urlParams = new URLSearchParams(window.location.search);
  const tplParam = urlParams.get('template');
  if (tplParam && ['modern', 'classic', 'minimalist', 'creative'].includes(tplParam)) {
    resumeState.selected_theme = tplParam;
  }

  // Load from local storage if existing draft exists
  const savedDraft = localStorage.getItem('folio_resume_draft');
  if (savedDraft) {
    try {
      const parsed = JSON.parse(savedDraft);
      if (parsed && parsed.contact && parsed.contact.full_name) {
        resumeState = parsed;
      }
    } catch (e) {
      console.warn("Could not parse saved draft, using default state.");
    }
  }

  // Initialize UI & Bindings
  initTemplateSelector();
  initFormBindings();
  initDynamicListManagers();
  initHistoryControls();
  initZoomControls();
  initMobileViewSwitch();
  initPDFExport();
  initDOCXExport();
  
  // Populate form with current state
  populateFormFromState();
  
  // Push initial snapshot
  pushHistorySnapshot();
  
  // Render preview & calculate progress
  renderLivePreview();
  updateProgressCalculation();
});

/* -------------------------------------------------------------------------
 * 1. Form & Live Preview Data Binding
 * ------------------------------------------------------------------------- */
function initFormBindings() {
  // Bind simple text inputs
  const bindInput = (id, path) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('input', () => {
      setDeepValue(resumeState, path, el.value);
      handleDataChange();
    });
  };

  bindInput('inFullName', 'contact.full_name');
  bindInput('inHeadline', 'contact.headline');
  bindInput('inEmail', 'contact.email');
  bindInput('inPhone', 'contact.phone');
  bindInput('inLocation', 'contact.location');
  bindInput('inLinkedin', 'contact.linkedin');
  bindInput('inGithub', 'contact.github');
  bindInput('inWebsite', 'contact.website');
  bindInput('inSummary', 'summary');
  bindInput('inSkills', 'skills');
}

function setDeepValue(obj, path, value) {
  const parts = path.split('.');
  let curr = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    if (!curr[parts[i]]) curr[parts[i]] = {};
    curr = curr[parts[i]];
  }
  curr[parts[parts.length - 1]] = value;
}

function handleDataChange() {
  renderLivePreview();
  updateProgressCalculation();
  triggerAutoSave();
  
  if (!isUndoRedoAction) {
    debounceHistorySnapshot();
  }
}

/* -------------------------------------------------------------------------
 * 2. Populate Form From State
 * ------------------------------------------------------------------------- */
function populateFormFromState() {
  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.value = val || '';
  };

  const c = resumeState.contact || {};
  setVal('inFullName', c.full_name);
  setVal('inHeadline', c.headline);
  setVal('inEmail', c.email);
  setVal('inPhone', c.phone);
  setVal('inLocation', c.location);
  setVal('inLinkedin', c.linkedin);
  setVal('inGithub', c.github);
  setVal('inWebsite', c.website);
  setVal('inSummary', resumeState.summary);
  setVal('inSkills', resumeState.skills);

  const tplSelect = document.getElementById('templateSelect');
  if (tplSelect) tplSelect.value = resumeState.selected_theme || 'modern';

  renderExperienceFormList();
  renderEducationFormList();
  renderProjectsFormList();
  renderCertificationsFormList();
  renderAchievementsFormList();
}

/* -------------------------------------------------------------------------
 * 3. Dynamic Lists (Experience, Education, Projects, etc.)
 * ------------------------------------------------------------------------- */
function initDynamicListManagers() {
  document.getElementById('btnAddExperience')?.addEventListener('click', () => {
    resumeState.experience.push({
      company: "",
      position: "",
      location: "",
      start_date: "",
      end_date: "",
      is_current: false,
      highlights: [""]
    });
    renderExperienceFormList();
    handleDataChange();
  });

  document.getElementById('btnAddEducation')?.addEventListener('click', () => {
    resumeState.education.push({
      institution: "",
      degree: "",
      field_of_study: "",
      start_date: "",
      end_date: "",
      grade_or_gpa: ""
    });
    renderEducationFormList();
    handleDataChange();
  });

  document.getElementById('btnAddProject')?.addEventListener('click', () => {
    resumeState.projects.push({
      name: "",
      role: "",
      technologies: "",
      link: "",
      highlights: [""]
    });
    renderProjectsFormList();
    handleDataChange();
  });

  document.getElementById('btnAddCert')?.addEventListener('click', () => {
    if (!resumeState.certifications) resumeState.certifications = [];
    resumeState.certifications.push({
      name: "",
      issuer: "",
      issue_date: "",
      credential_url: ""
    });
    renderCertificationsFormList();
    handleDataChange();
  });

  document.getElementById('btnAddAchievement')?.addEventListener('click', () => {
    if (!resumeState.achievements) resumeState.achievements = [];
    resumeState.achievements.push({
      title: "",
      organization: "",
      year: "",
      description: ""
    });
    renderAchievementsFormList();
    handleDataChange();
  });
}

// Experience Form List
function renderExperienceFormList() {
  const container = document.getElementById('experienceListContainer');
  if (!container) return;
  container.innerHTML = '';

  resumeState.experience.forEach((exp, idx) => {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
      <div class="item-card-header">
        <span class="item-card-title">Position #${idx + 1}</span>
        <button type="button" class="btn-remove-item" data-remove-exp="${idx}">✕ Remove</button>
      </div>
      <div class="form-grid-2">
        <div class="form-group">
          <label class="form-label">Position / Job Title*</label>
          <input type="text" class="form-input exp-position" value="${escapeHtml(exp.position)}" placeholder="e.g. Senior Software Engineer">
        </div>
        <div class="form-group">
          <label class="form-label">Company Name*</label>
          <input type="text" class="form-input exp-company" value="${escapeHtml(exp.company)}" placeholder="e.g. Acme Corp">
        </div>
      </div>
      <div class="form-grid-2">
        <div class="form-group">
          <label class="form-label">Location</label>
          <input type="text" class="form-input exp-location" value="${escapeHtml(exp.location)}" placeholder="e.g. San Francisco or Remote">
        </div>
        <div class="form-group">
          <label class="form-label">Dates</label>
          <div style="display:flex; gap: 8px; align-items:center;">
            <input type="text" class="form-input exp-start" value="${escapeHtml(exp.start_date)}" placeholder="Start (2021)">
            <span>–</span>
            <input type="text" class="form-input exp-end" value="${escapeHtml(exp.end_date)}" placeholder="End / Present" ${exp.is_current ? 'disabled' : ''}>
          </div>
          <label style="font-size:0.75rem; color:var(--text-muted); display:inline-flex; align-items:center; gap:4px; margin-top:4px; cursor:pointer;">
            <input type="checkbox" class="exp-current" ${exp.is_current ? 'checked' : ''}> Currently working here
          </label>
        </div>
      </div>
      <div class="form-group" style="margin-bottom:0;">
        <label class="form-label">Key Accomplishments (One bullet per line)</label>
        <textarea class="form-textarea exp-bullets" placeholder="• Spearheaded feature migration, boosting uptime by 25%">${escapeHtml((exp.highlights || []).join('\n'))}</textarea>
        <div class="par-tip-box">
          <strong>💡 Pro Tip (CAR Principle):</strong> Use Action Verb + Context + Quantifiable Metric (e.g. "Optimized API latency by 35% across 200k daily users").
        </div>
      </div>
    `;

    // Bind inputs
    card.querySelector('.exp-position').addEventListener('input', (e) => { exp.position = e.target.value; handleDataChange(); });
    card.querySelector('.exp-company').addEventListener('input', (e) => { exp.company = e.target.value; handleDataChange(); });
    card.querySelector('.exp-location').addEventListener('input', (e) => { exp.location = e.target.value; handleDataChange(); });
    card.querySelector('.exp-start').addEventListener('input', (e) => { exp.start_date = e.target.value; handleDataChange(); });
    
    const endInput = card.querySelector('.exp-end');
    endInput.addEventListener('input', (e) => { exp.end_date = e.target.value; handleDataChange(); });

    card.querySelector('.exp-current').addEventListener('change', (e) => {
      exp.is_current = e.target.checked;
      if (exp.is_current) {
        exp.end_date = "Present";
        endInput.value = "Present";
        endInput.disabled = true;
      } else {
        endInput.disabled = false;
        exp.end_date = "";
        endInput.value = "";
      }
      handleDataChange();
    });

    card.querySelector('.exp-bullets').addEventListener('input', (e) => {
      exp.highlights = e.target.value.split('\n').filter(b => b.trim() !== '');
      handleDataChange();
    });

    card.querySelector('[data-remove-exp]').addEventListener('click', () => {
      resumeState.experience.splice(idx, 1);
      renderExperienceFormList();
      handleDataChange();
    });

    container.appendChild(card);
  });
}

// Education Form List
function renderEducationFormList() {
  const container = document.getElementById('educationListContainer');
  if (!container) return;
  container.innerHTML = '';

  resumeState.education.forEach((edu, idx) => {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
      <div class="item-card-header">
        <span class="item-card-title">Degree #${idx + 1}</span>
        <button type="button" class="btn-remove-item" data-remove-edu="${idx}">✕ Remove</button>
      </div>
      <div class="form-grid-2">
        <div class="form-group">
          <label class="form-label">Degree & Major*</label>
          <input type="text" class="form-input edu-degree" value="${escapeHtml(edu.degree)}" placeholder="e.g. B.S. in Computer Science">
        </div>
        <div class="form-group">
          <label class="form-label">University / Institution*</label>
          <input type="text" class="form-input edu-school" value="${escapeHtml(edu.institution)}" placeholder="e.g. UC Berkeley">
        </div>
      </div>
      <div class="form-grid-2" style="margin-bottom:0;">
        <div class="form-group">
          <label class="form-label">Graduation Year / Dates</label>
          <input type="text" class="form-input edu-dates" value="${escapeHtml(edu.end_date)}" placeholder="e.g. 2018 or 2020 – 2024">
        </div>
        <div class="form-group">
          <label class="form-label">GPA or Academic Honors</label>
          <input type="text" class="form-input edu-gpa" value="${escapeHtml(edu.grade_or_gpa)}" placeholder="e.g. 3.9 GPA · Dean's List">
        </div>
      </div>
    `;

    card.querySelector('.edu-degree').addEventListener('input', (e) => { edu.degree = e.target.value; handleDataChange(); });
    card.querySelector('.edu-school').addEventListener('input', (e) => { edu.institution = e.target.value; handleDataChange(); });
    card.querySelector('.edu-dates').addEventListener('input', (e) => { edu.end_date = e.target.value; handleDataChange(); });
    card.querySelector('.edu-gpa').addEventListener('input', (e) => { edu.grade_or_gpa = e.target.value; handleDataChange(); });
    card.querySelector('[data-remove-edu]').addEventListener('click', () => {
      resumeState.education.splice(idx, 1);
      renderEducationFormList();
      handleDataChange();
    });

    container.appendChild(card);
  });
}

// Projects Form List
function renderProjectsFormList() {
  const container = document.getElementById('projectsListContainer');
  if (!container) return;
  container.innerHTML = '';

  resumeState.projects.forEach((proj, idx) => {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
      <div class="item-card-header">
        <span class="item-card-title">Project #${idx + 1}</span>
        <button type="button" class="btn-remove-item" data-remove-proj="${idx}">✕ Remove</button>
      </div>
      <div class="form-grid-2">
        <div class="form-group">
          <label class="form-label">Project Name*</label>
          <input type="text" class="form-input proj-name" value="${escapeHtml(proj.name)}" placeholder="e.g. Pulse Analytics Engine">
        </div>
        <div class="form-group">
          <label class="form-label">Your Role</label>
          <input type="text" class="form-input proj-role" value="${escapeHtml(proj.role)}" placeholder="e.g. Lead Developer">
        </div>
      </div>
      <div class="form-grid-2">
        <div class="form-group">
          <label class="form-label">Technologies Used</label>
          <input type="text" class="form-input proj-tech" value="${escapeHtml(proj.technologies)}" placeholder="e.g. Python, Docker, AWS">
        </div>
        <div class="form-group">
          <label class="form-label">Live Link / GitHub URL</label>
          <input type="text" class="form-input proj-link" value="${escapeHtml(proj.link)}" placeholder="e.g. github.com/username/project">
        </div>
      </div>
      <div class="form-group" style="margin-bottom:0;">
        <label class="form-label">Accomplishments & Impact</label>
        <textarea class="form-textarea proj-bullets" placeholder="• Deployed containerized pipeline serving 10k users">${escapeHtml((proj.highlights || []).join('\n'))}</textarea>
      </div>
    `;

    card.querySelector('.proj-name').addEventListener('input', (e) => { proj.name = e.target.value; handleDataChange(); });
    card.querySelector('.proj-role').addEventListener('input', (e) => { proj.role = e.target.value; handleDataChange(); });
    card.querySelector('.proj-tech').addEventListener('input', (e) => { proj.technologies = e.target.value; handleDataChange(); });
    card.querySelector('.proj-link').addEventListener('input', (e) => { proj.link = e.target.value; handleDataChange(); });
    card.querySelector('.proj-bullets').addEventListener('input', (e) => {
      proj.highlights = e.target.value.split('\n').filter(b => b.trim() !== '');
      handleDataChange();
    });
    card.querySelector('[data-remove-proj]').addEventListener('click', () => {
      resumeState.projects.splice(idx, 1);
      renderProjectsFormList();
      handleDataChange();
    });

    container.appendChild(card);
  });
}

// Certifications Form List
function renderCertificationsFormList() {
  const container = document.getElementById('certificationsListContainer');
  if (!container) return;
  container.innerHTML = '';

  (resumeState.certifications || []).forEach((cert, idx) => {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
      <div class="item-card-header">
        <span class="item-card-title">Credential #${idx + 1}</span>
        <button type="button" class="btn-remove-item" data-remove-cert="${idx}">✕ Remove</button>
      </div>
      <div class="form-grid-2" style="margin-bottom:0;">
        <div class="form-group">
          <label class="form-label">Certification Name*</label>
          <input type="text" class="form-input cert-name" value="${escapeHtml(cert.name)}" placeholder="e.g. AWS Certified Solutions Architect">
        </div>
        <div class="form-group">
          <label class="form-label">Issuing Body & Year</label>
          <input type="text" class="form-input cert-issuer" value="${escapeHtml(cert.issuer)}" placeholder="e.g. Amazon Web Services (2023)">
        </div>
      </div>
    `;

    card.querySelector('.cert-name').addEventListener('input', (e) => { cert.name = e.target.value; handleDataChange(); });
    card.querySelector('.cert-issuer').addEventListener('input', (e) => { cert.issuer = e.target.value; handleDataChange(); });
    card.querySelector('[data-remove-cert]').addEventListener('click', () => {
      resumeState.certifications.splice(idx, 1);
      renderCertificationsFormList();
      handleDataChange();
    });

    container.appendChild(card);
  });
}

// Achievements Form List
function renderAchievementsFormList() {
  const container = document.getElementById('achievementsListContainer');
  if (!container) return;
  container.innerHTML = '';

  (resumeState.achievements || []).forEach((ach, idx) => {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
      <div class="item-card-header">
        <span class="item-card-title">Honor #${idx + 1}</span>
        <button type="button" class="btn-remove-item" data-remove-ach="${idx}">✕ Remove</button>
      </div>
      <div class="form-grid-2">
        <div class="form-group">
          <label class="form-label">Award / Honor Title*</label>
          <input type="text" class="form-input ach-title" value="${escapeHtml(ach.title)}" placeholder="e.g. Hackathon 1st Place Winner">
        </div>
        <div class="form-group">
          <label class="form-label">Organization & Year</label>
          <input type="text" class="form-input ach-org" value="${escapeHtml(ach.organization)}" placeholder="e.g. MIT Hackathon · 2023">
        </div>
      </div>
      <div class="form-group" style="margin-bottom:0;">
        <label class="form-label">Brief Context</label>
        <input type="text" class="form-input ach-desc" value="${escapeHtml(ach.description)}" placeholder="e.g. Selected from 250+ competing teams.">
      </div>
    `;

    card.querySelector('.ach-title').addEventListener('input', (e) => { ach.title = e.target.value; handleDataChange(); });
    card.querySelector('.ach-org').addEventListener('input', (e) => { ach.organization = e.target.value; handleDataChange(); });
    card.querySelector('.ach-desc').addEventListener('input', (e) => { ach.description = e.target.value; handleDataChange(); });
    card.querySelector('[data-remove-ach]').addEventListener('click', () => {
      resumeState.achievements.splice(idx, 1);
      renderAchievementsFormList();
      handleDataChange();
    });

    container.appendChild(card);
  });
}

/* -------------------------------------------------------------------------
 * 4. Real-time Live A4 Preview Renderer
 * ------------------------------------------------------------------------- */
function renderLivePreview() {
  const sheet = document.getElementById('resumeCanvas');
  if (!sheet) return;

  const tpl = resumeState.selected_theme || 'modern';
  sheet.className = `a4-sheet tpl-${tpl}`;

  const c = resumeState.contact || {};
  const fullName = c.full_name || 'YOUR FULL NAME';
  const headline = c.headline || '';

  // Contacts
  const contactParts = [];
  if (c.email) contactParts.push(`<span>${escapeHtml(c.email)}</span>`);
  if (c.phone) contactParts.push(`<span>• ${escapeHtml(c.phone)}</span>`);
  if (c.location) contactParts.push(`<span>• ${escapeHtml(c.location)}</span>`);
  if (c.linkedin) contactParts.push(`<span>• ${escapeHtml(c.linkedin)}</span>`);
  if (c.github) contactParts.push(`<span>• ${escapeHtml(c.github)}</span>`);
  if (c.website) contactParts.push(`<span>• ${escapeHtml(c.website)}</span>`);

  let html = `
    <header class="doc-header">
      <div class="doc-name">${escapeHtml(fullName)}</div>
      ${headline ? `<div class="doc-headline">${escapeHtml(headline)}</div>` : ''}
      <div class="doc-contacts">${contactParts.join(' ')}</div>
    </header>
  `;

  // Summary
  if (resumeState.summary && resumeState.summary.trim()) {
    html += `
      <section class="doc-section">
        <div class="doc-sec-title">Professional Summary</div>
        <p class="doc-p">${escapeHtml(resumeState.summary)}</p>
      </section>
    `;
  }

  // Experience
  if (resumeState.experience && resumeState.experience.length > 0) {
    html += `<section class="doc-section"><div class="doc-sec-title">Work Experience</div>`;
    resumeState.experience.forEach(exp => {
      if (!exp.position && !exp.company) return;
      const dateStr = [exp.start_date, exp.is_current ? 'Present' : exp.end_date].filter(Boolean).join(' – ');
      html += `
        <div class="doc-entry">
          <div class="doc-entry-row">
            <span class="doc-entry-bold">${escapeHtml(exp.position)}</span>
          </div>
          <div class="doc-entry-sub">${escapeHtml(exp.company)}${exp.location ? ` · ${escapeHtml(exp.location)}` : ''}${dateStr ? ` · <span class="doc-inline-date">${escapeHtml(dateStr)}</span>` : ''}</div>
          ${exp.highlights && exp.highlights.length > 0 ? `
            <ul class="doc-bullets">
              ${exp.highlights.map(h => `<li>${escapeHtml(h)}</li>`).join('')}
            </ul>
          ` : ''}
        </div>
      `;
    });
    html += `</section>`;
  }

  // Projects
  if (resumeState.projects && resumeState.projects.length > 0) {
    html += `<section class="doc-section"><div class="doc-sec-title">Selected Projects</div>`;
    resumeState.projects.forEach(p => {
      if (!p.name) return;
      html += `
        <div class="doc-entry">
          <div class="doc-entry-row">
            <span class="doc-entry-bold">${escapeHtml(p.name)}</span>
            ${p.role ? `<span style="font-size: 9pt; color: #52525B; font-weight: 500;">— ${escapeHtml(p.role)}</span>` : ''}
          </div>
          ${p.technologies ? `<div class="doc-tech-stack"><strong>Technologies:</strong> ${escapeHtml(p.technologies)}</div>` : ''}
          ${p.link ? `<div style="font-size:8pt; color:var(--accent-copper); margin-top:2px; margin-bottom:2px;">${escapeHtml(p.link)}</div>` : ''}
          ${p.highlights && p.highlights.length > 0 ? `
            <ul class="doc-bullets">
              ${p.highlights.map(h => `<li>${escapeHtml(h)}</li>`).join('')}
            </ul>
          ` : ''}
        </div>
      `;
    });
    html += `</section>`;
  }

  // Skills
  if (resumeState.skills && resumeState.skills.trim()) {
    html += `
      <section class="doc-section">
        <div class="doc-sec-title">Core Competencies & Technical Skills</div>
        <p class="doc-p" style="font-weight:500;">${escapeHtml(resumeState.skills)}</p>
      </section>
    `;
  }

  // Education
  if (resumeState.education && resumeState.education.length > 0) {
    html += `<section class="doc-section"><div class="doc-sec-title">Education</div>`;
    resumeState.education.forEach(edu => {
      if (!edu.degree && !edu.institution) return;
      html += `
        <div class="doc-entry">
          <div class="doc-entry-row">
            <span class="doc-entry-bold">${escapeHtml(edu.degree)}</span>
          </div>
          <div class="doc-entry-sub">${escapeHtml(edu.institution)}${edu.end_date ? ` · <span class="doc-inline-date">${escapeHtml(edu.end_date)}</span>` : ''}${edu.grade_or_gpa ? ` · ${escapeHtml(edu.grade_or_gpa)}` : ''}</div>
        </div>
      `;
    });
    html += `</section>`;
  }

  // Certifications
  if (resumeState.certifications && resumeState.certifications.length > 0) {
    html += `<section class="doc-section"><div class="doc-sec-title">Certifications & Credentials</div><ul class="doc-bullets">`;
    resumeState.certifications.forEach(cert => {
      if (!cert.name) return;
      html += `<li><strong>${escapeHtml(cert.name)}</strong>${cert.issuer ? ` – ${escapeHtml(cert.issuer)}` : ''}</li>`;
    });
    html += `</ul></section>`;
  }

  // Achievements
  if (resumeState.achievements && resumeState.achievements.length > 0) {
    html += `<section class="doc-section"><div class="doc-sec-title">Honors & Achievements</div><ul class="doc-bullets">`;
    resumeState.achievements.forEach(ach => {
      if (!ach.title) return;
      html += `<li><strong>${escapeHtml(ach.title)}</strong> ${ach.organization ? `(${escapeHtml(ach.organization)})` : ''} ${ach.description ? `— ${escapeHtml(ach.description)}` : ''}</li>`;
    });
    html += `</ul></section>`;
  }

  sheet.innerHTML = html;
}

/* -------------------------------------------------------------------------
 * 5. Undo / Redo History Stack
 * ------------------------------------------------------------------------- */
function initHistoryControls() {
  const btnUndo = document.getElementById('btnUndo');
  const btnRedo = document.getElementById('btnRedo');

  if (btnUndo) btnUndo.addEventListener('click', performUndo);
  if (btnRedo) btnRedo.addEventListener('click', performRedo);

  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') {
      if (e.shiftKey) {
        e.preventDefault();
        performRedo();
      } else {
        e.preventDefault();
        performUndo();
      }
    } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y') {
      e.preventDefault();
      performRedo();
    }
  });
}

let historyDebounceTimer = null;
function debounceHistorySnapshot() {
  clearTimeout(historyDebounceTimer);
  historyDebounceTimer = setTimeout(() => {
    pushHistorySnapshot();
  }, 400);
}

function pushHistorySnapshot() {
  const snapshot = JSON.stringify(resumeState);
  if (historyStack[historyIndex] === snapshot) return;

  historyStack = historyStack.slice(0, historyIndex + 1);
  historyStack.push(snapshot);
  if (historyStack.length > 30) historyStack.shift();
  historyIndex = historyStack.length - 1;
  updateHistoryButtons();
}

function performUndo() {
  if (historyIndex > 0) {
    historyIndex--;
    applyHistorySnapshot(historyStack[historyIndex]);
  }
}

function performRedo() {
  if (historyIndex < historyStack.length - 1) {
    historyIndex++;
    applyHistorySnapshot(historyStack[historyIndex]);
  }
}

function applyHistorySnapshot(snapshotJson) {
  isUndoRedoAction = true;
  try {
    resumeState = JSON.parse(snapshotJson);
    populateFormFromState();
    renderLivePreview();
    updateProgressCalculation();
    triggerAutoSave();
    updateHistoryButtons();
  } finally {
    isUndoRedoAction = false;
  }
}

function updateHistoryButtons() {
  const btnUndo = document.getElementById('btnUndo');
  const btnRedo = document.getElementById('btnRedo');
  if (btnUndo) btnUndo.disabled = (historyIndex <= 0);
  if (btnRedo) btnRedo.disabled = (historyIndex >= historyStack.length - 1);
}

/* -------------------------------------------------------------------------
 * 6. Auto-Save & Draft Management
 * ------------------------------------------------------------------------- */
function triggerAutoSave() {
  const statusPill = document.getElementById('saveStatusPill');
  const statusText = document.getElementById('saveStatusText');
  if (statusPill && statusText) {
    statusPill.classList.add('saving');
    statusText.textContent = "Saving...";
  }

  clearTimeout(autoSaveTimer);
  autoSaveTimer = setTimeout(() => {
    localStorage.setItem('folio_resume_draft', JSON.stringify(resumeState));
    if (statusPill && statusText) {
      statusPill.classList.remove('saving');
      statusText.textContent = "Saved to Local Vault";
    }
  }, 350);
}

/* -------------------------------------------------------------------------
 * 7. Template Selection & Zoom Controls
 * ------------------------------------------------------------------------- */
function initTemplateSelector() {
  const sel = document.getElementById('templateSelect');
  if (!sel) return;
  sel.value = resumeState.selected_theme || 'modern';
  sel.addEventListener('change', () => {
    resumeState.selected_theme = sel.value;
    handleDataChange();
  });
}

function initZoomControls() {
  const sheet = document.getElementById('resumeCanvas');
  const zoomIn = document.getElementById('btnZoomIn');
  const zoomOut = document.getElementById('btnZoomOut');
  const zoomLabel = document.getElementById('zoomLabel');

  const updateZoom = (z) => {
    currentZoom = Math.min(1.4, Math.max(0.6, z));
    if (sheet) sheet.style.transform = `scale(${currentZoom})`;
    if (zoomLabel) zoomLabel.textContent = `${Math.round(currentZoom * 100)}%`;
  };

  if (zoomIn) zoomIn.addEventListener('click', () => updateZoom(currentZoom + 0.1));
  if (zoomOut) zoomOut.addEventListener('click', () => updateZoom(currentZoom - 0.1));
}

/* -------------------------------------------------------------------------
 * 8. Progress Indicator & Section Stepper
 * ------------------------------------------------------------------------- */
function updateProgressCalculation() {
  const sections = [
    { key: 'personal', done: Boolean(resumeState.contact.full_name && resumeState.contact.email) },
    { key: 'summary', done: Boolean(resumeState.summary && resumeState.summary.length > 20) },
    { key: 'experience', done: Boolean(resumeState.experience && resumeState.experience.length > 0) },
    { key: 'education', done: Boolean(resumeState.education && resumeState.education.length > 0) },
    { key: 'projects', done: Boolean(resumeState.projects && resumeState.projects.length > 0) },
    { key: 'skills', done: Boolean(resumeState.skills && resumeState.skills.length > 5) },
    { key: 'certifications', done: Boolean(resumeState.certifications && resumeState.certifications.length > 0) },
    { key: 'achievements', done: Boolean(resumeState.achievements && resumeState.achievements.length > 0) }
  ];

  let completedCount = 0;
  sections.forEach(sec => {
    const chip = document.querySelector(`[data-section-step="${sec.key}"]`);
    if (chip) {
      if (sec.done) {
        chip.classList.add('completed');
      } else {
        chip.classList.remove('completed');
      }
    }
    if (sec.done) completedCount++;
  });

  const percentage = Math.round((completedCount / sections.length) * 100);
  const fillBar = document.getElementById('progressFillBar');
  const fillText = document.getElementById('progressPercentText');

  if (fillBar) fillBar.style.width = `${percentage}%`;
  if (fillText) fillText.textContent = `${percentage}% Complete`;
}

/* -------------------------------------------------------------------------
 * 9. Mobile Segmented Switcher
 * ------------------------------------------------------------------------- */
function initMobileViewSwitch() {
  const switchEdit = document.getElementById('btnSwitchEdit');
  const switchPreview = document.getElementById('btnSwitchPreview');
  const workspace = document.querySelector('.studio-workspace');

  if (!switchEdit || !switchPreview || !workspace) return;

  switchEdit.addEventListener('click', () => {
    workspace.classList.remove('show-preview');
    switchEdit.classList.add('active');
    switchPreview.classList.remove('active');
  });

  switchPreview.addEventListener('click', () => {
    workspace.classList.add('show-preview');
    switchPreview.classList.add('active');
    switchEdit.classList.remove('active');
  });
}

/* -------------------------------------------------------------------------
 * 10. PDF Export
 * ------------------------------------------------------------------------- */
function initPDFExport() {
  const btnPDF = document.getElementById('btnDownloadPDF');
  if (btnPDF) {
    btnPDF.addEventListener('click', () => {
      // Temporarily set document.title to candidate name so the browser defaults the PDF filename cleanly
      const originalTitle = document.title;
      const fullName = (resumeState.contact && resumeState.contact.full_name) 
        ? resumeState.contact.full_name.trim() 
        : 'Resume';
      const cleanFileName = `${fullName.replace(/\s+/g, '_')}_Resume`;
      
      document.title = cleanFileName;
      
      // Trigger native browser print which uses @media print A4 stylesheet
      window.print();
      
      // Restore original studio document title
      setTimeout(() => {
        document.title = originalTitle;
      }, 1000);
    });
  }

  // Sample Profile button
  document.getElementById('btnLoadSample')?.addEventListener('click', () => {
    if (confirm("Load the pre-configured executive tech profile? Your current unsaved form fields will be replaced.")) {
      resumeState = JSON.parse(JSON.stringify(SAMPLE_RESUME_DATA));
      populateFormFromState();
      handleDataChange();
      pushHistorySnapshot();
    }
  });

  // Export JSON draft
  document.getElementById('btnExportJson')?.addEventListener('click', () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(resumeState, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `${(resumeState.contact.full_name || 'Resume').replace(/\s+/g, '_')}_Draft.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/* -------------------------------------------------------------------------
 * 11. Genuine Client-Side Office Open XML (.docx) Generator
 * ------------------------------------------------------------------------- */
function initDOCXExport() {
  const btnDOCX = document.getElementById('btnDownloadDOCX');
  if (btnDOCX) {
    btnDOCX.addEventListener('click', () => {
      exportResumeToDocx();
    });
  }
}

function escapeXml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

const CRC32_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    }
    table[n] = c;
  }
  return table;
})();

function crc32(uint8Array) {
  let crc = 0 ^ (-1);
  for (let i = 0; i < uint8Array.length; i++) {
    crc = (crc >>> 8) ^ CRC32_TABLE[(crc ^ uint8Array[i]) & 0xFF];
  }
  return (crc ^ (-1)) >>> 0;
}

function createSimpleZip(files) {
  const encoder = new TextEncoder();
  const fileEntries = [];
  let offset = 0;

  for (const [name, content] of Object.entries(files)) {
    const data = typeof content === 'string' ? encoder.encode(content) : content;
    const nameBytes = encoder.encode(name);
    const crc = crc32(data);
    const size = data.length;

    const localHeader = new Uint8Array(30 + nameBytes.length);
    const view = new DataView(localHeader.buffer);
    view.setUint32(0, 0x04034b50, true);
    view.setUint16(4, 20, true);
    view.setUint16(6, 0, true);
    view.setUint16(8, 0, true);
    view.setUint16(10, 0, true);
    view.setUint16(12, 0, true);
    view.setUint32(14, crc, true);
    view.setUint32(18, size, true);
    view.setUint32(22, size, true);
    view.setUint16(26, nameBytes.length, true);
    view.setUint16(28, 0, true);
    localHeader.set(nameBytes, 30);

    fileEntries.push({
      nameBytes,
      data,
      crc,
      size,
      offset,
      localHeader
    });

    offset += localHeader.length + size;
  }

  const centralEntries = [];
  let centralDirSize = 0;

  for (const entry of fileEntries) {
    const cd = new Uint8Array(46 + entry.nameBytes.length);
    const view = new DataView(cd.buffer);
    view.setUint32(0, 0x02014b50, true);
    view.setUint16(4, 20, true);
    view.setUint16(6, 20, true);
    view.setUint16(8, 0, true);
    view.setUint16(10, 0, true);
    view.setUint16(12, 0, true);
    view.setUint16(14, 0, true);
    view.setUint32(16, entry.crc, true);
    view.setUint32(20, entry.size, true);
    view.setUint32(24, entry.size, true);
    view.setUint16(28, entry.nameBytes.length, true);
    view.setUint16(30, 0, true);
    view.setUint16(32, 0, true);
    view.setUint16(34, 0, true);
    view.setUint16(36, 0, true);
    view.setUint32(38, 0, true);
    view.setUint32(42, entry.offset, true);
    cd.set(entry.nameBytes, 46);

    centralEntries.push(cd);
    centralDirSize += cd.length;
  }

  const eocd = new Uint8Array(22);
  const eocdView = new DataView(eocd.buffer);
  eocdView.setUint32(0, 0x06054b50, true);
  eocdView.setUint16(4, 0, true);
  eocdView.setUint16(6, 0, true);
  eocdView.setUint16(8, fileEntries.length, true);
  eocdView.setUint16(10, fileEntries.length, true);
  eocdView.setUint32(12, centralDirSize, true);
  eocdView.setUint32(16, offset, true);
  eocdView.setUint16(20, 0, true);

  const totalLength = offset + centralDirSize + eocd.length;
  const out = new Uint8Array(totalLength);
  let writePos = 0;

  for (const entry of fileEntries) {
    out.set(entry.localHeader, writePos);
    writePos += entry.localHeader.length;
    out.set(entry.data, writePos);
    writePos += entry.data.length;
  }

  for (const cd of centralEntries) {
    out.set(cd, writePos);
    writePos += cd.length;
  }

  out.set(eocd, writePos);
  return out;
}

function exportResumeToDocx() {
  const c = resumeState.contact || {};
  const fullName = c.full_name || 'Resume';
  const headline = c.headline || '';
  
  const contactsList = [c.email, c.phone, c.location, c.linkedin, c.github, c.website].filter(Boolean);
  const contactsStr = contactsList.join('   •   ');

  let bodyXml = '';

  // 1. Header (Name, Headline, Contacts)
  bodyXml += `
    <w:p>
      <w:pPr><w:jc w:val="center"/><w:spacing w:after="80"/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:sz w:val="44"/><w:color w:val="18181B"/></w:rPr><w:t>${escapeXml(fullName)}</w:t></w:r>
    </w:p>
  `;

  if (headline) {
    bodyXml += `
      <w:p>
        <w:pPr><w:jc w:val="center"/><w:spacing w:after="100"/></w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:sz w:val="22"/><w:color w:val="B87333"/></w:rPr><w:t>${escapeXml(headline)}</w:t></w:r>
      </w:p>
    `;
  }

  if (contactsStr) {
    bodyXml += `
      <w:p>
        <w:pPr><w:jc w:val="center"/><w:spacing w:after="220"/><w:pBdr><w:bottom w:val="single" w:sz="12" w:space="8" w:color="18181B"/></w:pBdr></w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="18"/><w:color w:val="52525B"/></w:rPr><w:t>${escapeXml(contactsStr)}</w:t></w:r>
      </w:p>
    `;
  }

  function addSecHeading(title) {
    return `
      <w:p>
        <w:pPr><w:spacing w:before="240" w:after="80"/><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="B87333"/></w:pBdr></w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:caps/><w:sz w:val="22"/><w:color w:val="18181B"/></w:rPr><w:t>${escapeXml(title)}</w:t></w:r>
      </w:p>
    `;
  }

  // 2. Professional Summary
  if (resumeState.summary && resumeState.summary.trim()) {
    bodyXml += addSecHeading('Professional Summary');
    bodyXml += `
      <w:p>
        <w:pPr><w:spacing w:after="160"/></w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="20"/><w:color w:val="27272A"/></w:rPr><w:t>${escapeXml(resumeState.summary)}</w:t></w:r>
      </w:p>
    `;
  }

  // 3. Work Experience
  if (resumeState.experience && resumeState.experience.length > 0) {
    bodyXml += addSecHeading('Work Experience');
    resumeState.experience.forEach(exp => {
      if (!exp.position && !exp.company) return;
      const dateStr = [exp.start_date, exp.is_current ? 'Present' : exp.end_date].filter(Boolean).join(' – ');
      const sub = [exp.company, exp.location, dateStr].filter(Boolean).join(' · ');

      bodyXml += `
        <w:p>
          <w:pPr><w:spacing w:before="120" w:after="30"/></w:pPr>
          <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:sz w:val="21"/><w:color w:val="18181B"/></w:rPr><w:t>${escapeXml(exp.position)}</w:t></w:r>
        </w:p>
        <w:p>
          <w:pPr><w:spacing w:after="80"/></w:pPr>
          <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:i/><w:sz w:val="19"/><w:color w:val="52525B"/></w:rPr><w:t>${escapeXml(sub)}</w:t></w:r>
        </w:p>
      `;

      if (exp.highlights && exp.highlights.length > 0) {
        exp.highlights.forEach(bullet => {
          if (!bullet.trim()) return;
          bodyXml += `
            <w:p>
              <w:pPr><w:ind w:left="360"/><w:spacing w:after="40"/></w:pPr>
              <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="19"/><w:color w:val="27272A"/></w:rPr><w:t>•  ${escapeXml(bullet)}</w:t></w:r>
            </w:p>
          `;
        });
      }
    });
  }

  // 4. Selected Projects
  if (resumeState.projects && resumeState.projects.length > 0) {
    bodyXml += addSecHeading('Selected Projects');
    resumeState.projects.forEach(p => {
      if (!p.name) return;
      bodyXml += `
        <w:p>
          <w:pPr><w:spacing w:before="120" w:after="30"/></w:pPr>
          <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:sz w:val="21"/><w:color w:val="18181B"/></w:rPr><w:t>${escapeXml(p.name)} ${p.role ? `— ${escapeXml(p.role)}` : ''}</w:t></w:r>
        </w:p>
      `;
      if (p.technologies) {
        bodyXml += `
          <w:p>
            <w:pPr><w:spacing w:after="40"/></w:pPr>
            <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:sz w:val="18"/><w:color w:val="52525B"/></w:rPr><w:t>Technologies: </w:t></w:r>
            <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="18"/><w:color w:val="52525B"/></w:rPr><w:t>${escapeXml(p.technologies)}</w:t></w:r>
          </w:p>
        `;
      }
      if (p.link) {
        bodyXml += `
          <w:p>
            <w:pPr><w:spacing w:after="40"/></w:pPr>
            <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="17"/><w:color w:val="B87333"/></w:rPr><w:t>${escapeXml(p.link)}</w:t></w:r>
          </w:p>
        `;
      }
      if (p.highlights && p.highlights.length > 0) {
        p.highlights.forEach(bullet => {
          if (!bullet.trim()) return;
          bodyXml += `
            <w:p>
              <w:pPr><w:ind w:left="360"/><w:spacing w:after="40"/></w:pPr>
              <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="19"/><w:color w:val="27272A"/></w:rPr><w:t>•  ${escapeXml(bullet)}</w:t></w:r>
            </w:p>
          `;
        });
      }
    });
  }

  // 5. Skills
  if (resumeState.skills && resumeState.skills.trim()) {
    bodyXml += addSecHeading('Core Competencies & Skills');
    bodyXml += `
      <w:p>
        <w:pPr><w:spacing w:after="160"/></w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="20"/><w:color w:val="27272A"/></w:rPr><w:t>${escapeXml(resumeState.skills)}</w:t></w:r>
      </w:p>
    `;
  }

  // 6. Education
  if (resumeState.education && resumeState.education.length > 0) {
    bodyXml += addSecHeading('Education');
    resumeState.education.forEach(edu => {
      if (!edu.degree && !edu.institution) return;
      const sub = [edu.institution, edu.end_date, edu.grade_or_gpa].filter(Boolean).join(' · ');
      bodyXml += `
        <w:p>
          <w:pPr><w:spacing w:before="100" w:after="30"/></w:pPr>
          <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:sz w:val="21"/><w:color w:val="18181B"/></w:rPr><w:t>${escapeXml(edu.degree)}</w:t></w:r>
        </w:p>
        <w:p>
          <w:pPr><w:spacing w:after="80"/></w:pPr>
          <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="19"/><w:color w:val="52525B"/></w:rPr><w:t>${escapeXml(sub)}</w:t></w:r>
        </w:p>
      `;
    });
  }

  // 7. Certifications
  if (resumeState.certifications && resumeState.certifications.length > 0) {
    bodyXml += addSecHeading('Certifications & Credentials');
    resumeState.certifications.forEach(cert => {
      if (!cert.name) return;
      const certDesc = [cert.name, cert.issuer, cert.issue_date].filter(Boolean).join(' – ');
      bodyXml += `
        <w:p>
          <w:pPr><w:ind w:left="360"/><w:spacing w:after="40"/></w:pPr>
          <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="19"/><w:color w:val="27272A"/></w:rPr><w:t>•  ${escapeXml(certDesc)}</w:t></w:r>
        </w:p>
      `;
    });
  }

  // 8. Achievements
  if (resumeState.achievements && resumeState.achievements.length > 0) {
    bodyXml += addSecHeading('Honors & Achievements');
    resumeState.achievements.forEach(ach => {
      if (!ach.title) return;
      const achDesc = `${ach.title} ${ach.organization ? `(${ach.organization})` : ''} ${ach.description ? `— ${ach.description}` : ''}`;
      bodyXml += `
        <w:p>
          <w:pPr><w:ind w:left="360"/><w:spacing w:after="40"/></w:pPr>
          <w:r><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="19"/><w:color w:val="27272A"/></w:rPr><w:t>•  ${escapeXml(achDesc)}</w:t></w:r>
        </w:p>
      `;
    });
  }

  const documentXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    ${bodyXml}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/>
    </w:sectPr>
  </w:body>
</w:document>`;

  const contentTypesXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>`;

  const relsXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>`;

  const docRelsXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>`;

  const stylesXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="20"/>
        <w:color w:val="18181B"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
</w:styles>`;

  const files = {
    '[Content_Types].xml': contentTypesXml,
    '_rels/.rels': relsXml,
    'word/_rels/document.xml.rels': docRelsXml,
    'word/document.xml': documentXml,
    'word/styles.xml': stylesXml
  };

  const zipBytes = createSimpleZip(files);
  const blob = new Blob([zipBytes], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
  const filename = `${(fullName || 'Resume').replace(/\s+/g, '_')}_Resume.docx`;

  const downloadAnchor = document.createElement('a');
  downloadAnchor.href = URL.createObjectURL(blob);
  downloadAnchor.download = filename;
  document.body.appendChild(downloadAnchor);
  downloadAnchor.click();
  setTimeout(() => {
    downloadAnchor.remove();
    URL.revokeObjectURL(downloadAnchor.href);
  }, 1000);
}
