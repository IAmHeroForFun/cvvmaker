/**
 * FOLIO — Premium Editorial CV Maker Interaction Controller
 * Handles mobile navigation, template previews, modal dialogs, and smooth scrolling.
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initTemplateModals();
  initSmoothScroll();
  initBuilderModals();
});

/* -------------------------------------------------------------------------
 * 1. Mobile Navigation
 * ------------------------------------------------------------------------- */
function initMobileNav() {
  const toggleBtn = document.querySelector('.mobile-toggle');
  const drawer = document.querySelector('.mobile-nav-drawer');

  if (!toggleBtn || !drawer) return;

  toggleBtn.addEventListener('click', () => {
    const isOpen = drawer.classList.contains('open');
    if (isOpen) {
      drawer.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded', 'false');
    } else {
      drawer.classList.add('open');
      toggleBtn.setAttribute('aria-expanded', 'true');
    }
  });

  // Close drawer when clicking any nav link
  drawer.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      drawer.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded', 'false');
    });
  });
}

/* -------------------------------------------------------------------------
 * 2. Template Preview Data & Modal Interactions
 * ------------------------------------------------------------------------- */
const TEMPLATE_DETAILS = {
  classic: {
    name: "The Classic",
    tagline: "Traditional, structured, and timelessly professional.",
    font: "Georgia, serif",
    color: "#18181B",
    accent: "#B87333",
    layoutType: "Single-column corporate with serif headers",
    bestFor: "Finance, Management, Legal, Consulting, and Corporate roles",
    summary: "A distinguished serif layout emphasizing chronological leadership, formal achievement metrics, and institutional pedigree.",
    previewHtml: `
      <div style="font-family: Georgia, serif; color: #18181B; line-height: 1.45; max-width: 500px; margin: 0 auto; background: #FFF; padding: 28px; border: 1px solid #E7E0D7; border-radius: 4px; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
        <div style="text-align: center; border-bottom: 2px solid #18181B; padding-bottom: 12px; margin-bottom: 14px;">
          <h2 style="font-size: 1.6rem; letter-spacing: -0.01em; margin-bottom: 4px;">ELEANOR VANCE</h2>
          <div style="font-family: sans-serif; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em; color: #71717A;">Senior Director of Corporate Strategy</div>
          <div style="font-family: sans-serif; font-size: 0.75rem; color: #71717A; margin-top: 6px;">eleanor.vance@example.com · +1 (555) 349-2041 · New York, NY</div>
        </div>
        <div style="margin-bottom: 14px;">
          <div style="font-family: sans-serif; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.08em; border-bottom: 1px solid #71717A; padding-bottom: 2px; margin-bottom: 6px;">Executive Profile</div>
          <p style="font-size: 0.8rem; color: #3F3F46; text-align: justify; margin: 0;">Accomplished corporate strategist with 10+ years driving portfolio expansion and enterprise operational transformation across North American technology practices.</p>
        </div>
        <div>
          <div style="font-family: sans-serif; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.08em; border-bottom: 1px solid #71717A; padding-bottom: 2px; margin-bottom: 6px;">Professional Experience</div>
          <div style="font-size: 0.82rem; font-weight: bold;">
            Lead Strategy Principal — Apex Advisory <span style="font-weight: normal; font-size: 0.75rem; color: #71717A;">· 2021 – Present</span>
          </div>
          <ul style="font-size: 0.78rem; padding-left: 16px; margin-top: 4px; color: #3F3F46;">
            <li>Directed restructuring of $120M asset portfolio, realizing 22% recurring margin gains.</li>
            <li>Instituted global governance standards adopted across 14 cross-functional teams.</li>
          </ul>
        </div>
      </div>
    `
  },
  minimalist: {
    name: "The Minimalist",
    tagline: "Clean, simple, and whitespace-focused for effortless clarity.",
    font: "'Inter', sans-serif",
    color: "#18181B",
    accent: "#71717A",
    layoutType: "Ultra-lean single-column with generous breathing room",
    bestFor: "Software Engineers, Product Managers, Writers, and Analysts",
    summary: "Zero visual distractions. Engineered for ATS readability and instant scanning by executive hiring teams.",
    previewHtml: `
      <div style="font-family: 'Inter', sans-serif; color: #18181B; line-height: 1.5; max-width: 500px; margin: 0 auto; background: #FFF; padding: 28px; border: 1px solid #E7E0D7; border-radius: 4px; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
        <div style="margin-bottom: 20px;">
          <h2 style="font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 2px;">Marcus Aurel</h2>
          <div style="font-size: 0.82rem; color: #71717A;">Staff Infrastructure Architect · Zurich / Remote</div>
          <div style="font-size: 0.75rem; color: #A1A1AA; margin-top: 4px;">marcus.a@domain.io · github.com/marcusa · +41 44 201 8892</div>
        </div>
        <div style="margin-bottom: 16px;">
          <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #18181B; margin-bottom: 6px;">Background</div>
          <p style="font-size: 0.8rem; color: #52525B; margin: 0;">Specialist in distributed consensus protocols, high-availability telemetry pipelines, and Linux kernel networking.</p>
        </div>
        <div>
          <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #18181B; margin-bottom: 6px;">Experience</div>
          <div style="font-size: 0.82rem; font-weight: 600;">
            Staff SRE — CloudMesh Systems <span style="font-weight: 400; color: #71717A; font-size: 0.76rem;">· 2022 — Present</span>
          </div>
          <ul style="font-size: 0.78rem; padding-left: 14px; margin-top: 4px; color: #52525B;">
            <li>Architected zero-loss failover mechanism saving $450k annually in cloud spend.</li>
            <li>Maintained 99.999% SLA across 400+ multi-region Kubernetes clusters.</li>
          </ul>
        </div>
      </div>
    `
  },
  modern: {
    name: "The Modern",
    tagline: "Contemporary aesthetics with restrained copper accents.",
    font: "'Inter', sans-serif",
    color: "#18181B",
    accent: "#B87333",
    layoutType: "Contemporary dual-accent with tag chips and clean lines",
    bestFor: "Tech Leads, UX Designers, Marketers, and Startup Founders",
    summary: "Balanced proportions with tasteful copper indicators that guide the recruiter's eye directly to key achievements.",
    previewHtml: `
      <div style="font-family: 'Inter', sans-serif; color: #18181B; line-height: 1.5; max-width: 500px; margin: 0 auto; background: #FFF; padding: 28px; border: 1px solid #E7E0D7; border-radius: 4px; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
        <div style="border-left: 4px solid #B87333; padding-left: 14px; margin-bottom: 18px;">
          <h2 style="font-size: 1.6rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 2px;">JULIAN VANCE</h2>
          <div style="font-size: 0.82rem; font-weight: 600; color: #B87333; text-transform: uppercase; letter-spacing: 0.08em;">Principal Product Strategist</div>
          <div style="font-size: 0.75rem; color: #71717A; margin-top: 4px;">julian.vance@folio.studio · San Francisco, CA · portfolio.folio.design</div>
        </div>
        <div style="margin-bottom: 14px;">
          <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #18181B; border-bottom: 1px solid #E7E0D7; padding-bottom: 3px; margin-bottom: 6px;">Impact & Scope</div>
          <p style="font-size: 0.8rem; color: #3F3F46; margin: 0;">Design strategist translating complex technical constraints into intuitive multi-platform SaaS solutions with measured adoption growth.</p>
        </div>
        <div>
          <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #18181B; border-bottom: 1px solid #E7E0D7; padding-bottom: 3px; margin-bottom: 6px;">Selected Positions</div>
          <div style="font-size: 0.82rem; font-weight: 700;">
            Head of Product UX — Solstice Labs <span style="font-weight: 400; color: #71717A; font-size: 0.76rem;">· 2021 – Present</span>
          </div>
          <ul style="font-size: 0.78rem; padding-left: 14px; margin-top: 4px; color: #3F3F46;">
            <li>Scaled product experience from 20k to 1.2M active accounts in 18 months.</li>
            <li>Reduced checkout drop-off by 28% via quantitative heuristic UX audits.</li>
          </ul>
        </div>
      </div>
    `
  },
  creative: {
    name: "The Creative",
    tagline: "Distinctive, editorial, and unmistakably memorable.",
    font: "'DM Serif Display', serif",
    color: "#18181B",
    accent: "#B87333",
    layoutType: "Editorial two-tone header with magazine-level craft",
    bestFor: "Creative Directors, Architects, Researchers, and Media Leaders",
    summary: "Combines an editorial serif masthead with structured technical columns for professionals whose presentation must reflect their taste.",
    previewHtml: `
      <div style="font-family: 'Inter', sans-serif; color: #18181B; line-height: 1.5; max-width: 500px; margin: 0 auto; background: #FFF; padding: 28px; border: 1px solid #E7E0D7; border-radius: 4px; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">
        <div style="background: #FAF7F2; margin: -28px -28px 18px -28px; padding: 22px 28px; border-bottom: 1px solid #E7E0D7;">
          <h2 style="font-family: 'DM Serif Display', Georgia, serif; font-size: 1.8rem; font-weight: 400; margin-bottom: 2px;">Clara O'Connor</h2>
          <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #B87333;">Architectural Lead & Computational Designer</div>
          <div style="font-size: 0.75rem; color: #71717A; margin-top: 4px;">clara@oconnor-arch.co · London & Copenhagen</div>
        </div>
        <div style="margin-bottom: 14px;">
          <div style="font-family: 'DM Serif Display', Georgia, serif; font-size: 0.95rem; color: #18181B; border-bottom: 1px solid #B87333; padding-bottom: 2px; margin-bottom: 6px;">Editorial Statement</div>
          <p style="font-size: 0.8rem; color: #3F3F46; margin: 0;">Specializing in carbon-neutral timber installations, generative parametric modeling, and public institutional pavilions.</p>
        </div>
        <div>
          <div style="font-family: 'DM Serif Display', Georgia, serif; font-size: 0.95rem; color: #18181B; border-bottom: 1px solid #B87333; padding-bottom: 2px; margin-bottom: 6px;">Practice History</div>
          <div style="font-size: 0.82rem; font-weight: 600;">
            Senior Design Associate — Studio K <span style="font-weight: 400; color: #71717A; font-size: 0.76rem;">· 2020 – 2024</span>
          </div>
          <ul style="font-size: 0.78rem; padding-left: 14px; margin-top: 4px; color: #3F3F46;">
            <li>Recipient of the 2023 Nordic Sustainable Civic Architecture Merit Award.</li>
            <li>Managed delivery of 4 landmark cultural venues across Western Europe.</li>
          </ul>
        </div>
      </div>
    `
  }
};

function initTemplateModals() {
  const modalOverlay = document.getElementById('templateModal');
  if (!modalOverlay) return;

  const closeBtn = modalOverlay.querySelector('.modal-close-btn');
  const titleEl = document.getElementById('modalTemplateTitle');
  const subtitleEl = document.getElementById('modalTemplateSubtitle');
  const previewBox = document.getElementById('modalTemplatePreview');
  const bestForEl = document.getElementById('modalBestFor');
  const summaryEl = document.getElementById('modalSummary');
  const useBtn = document.getElementById('modalUseTemplateBtn');

  let currentTemplateKey = 'modern';

  document.querySelectorAll('[data-template]').forEach(button => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      const key = button.getAttribute('data-template');
      const data = TEMPLATE_DETAILS[key] || TEMPLATE_DETAILS['modern'];
      currentTemplateKey = key;

      titleEl.textContent = data.name;
      subtitleEl.textContent = data.tagline;
      previewBox.innerHTML = data.previewHtml;
      bestForEl.textContent = data.bestFor;
      summaryEl.textContent = data.summary;

      modalOverlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  });

  const closeModal = () => {
    modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
  };

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
      closeModal();
    }
  });

  if (useBtn) {
    useBtn.addEventListener('click', () => {
      closeModal();
      window.location.href = `editor.html?template=${currentTemplateKey}`;
    });
  }
}

/* -------------------------------------------------------------------------
 * 3. Builder & Sign-In Modals (Clear Integration Points)
 * ------------------------------------------------------------------------- */
function initBuilderModals() {
  const builderModal = document.getElementById('builderModal');
  const authModal = document.getElementById('authModal');

  // Trigger buttons for creating CV
  document.querySelectorAll('.trigger-create-cv').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      openBuilderModal('modern');
    });
  });

  // Trigger buttons for signing in / my resumes
  document.querySelectorAll('.trigger-auth').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (authModal) {
        authModal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  // Setup close handlers for all modals
  document.querySelectorAll('.modal-overlay').forEach(modal => {
    const close = modal.querySelector('.modal-close-btn');
    if (close) {
      close.addEventListener('click', () => {
        modal.classList.remove('active');
        document.body.style.overflow = '';
      });
    }
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });
}

function openBuilderModal(templateKey = 'modern') {
  const modal = document.getElementById('builderModal');
  if (!modal) return;
  const select = document.getElementById('builderTemplateSelect');
  if (select) select.value = templateKey;
  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
}

/* -------------------------------------------------------------------------
 * 4. Smooth Scrolling & Active Nav Spy
 * ------------------------------------------------------------------------- */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#' || !targetId) return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Highlight active section on scroll
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-menu .nav-link');

  window.addEventListener('scroll', () => {
    let current = '';
    const scrollY = window.pageYOffset;

    sections.forEach(sec => {
      const secTop = sec.offsetTop - 120;
      const secHeight = sec.offsetHeight;
      if (scrollY >= secTop && scrollY < secTop + secHeight) {
        current = '#' + sec.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === current) {
        link.classList.add('active');
      }
    });
  }, { passive: true });
}
