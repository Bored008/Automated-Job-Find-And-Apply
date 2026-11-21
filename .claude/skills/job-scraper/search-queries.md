# Search Queries for Job Scraper

<!-- SETUP: Customize these queries based on your skills, target roles, and location -->

## Installed portal CLIs (primary for `/scrape`)

`/scrape` discovers every portal skill under `.agents/skills/*/SKILL.md` and runs its CLI first. None ship with AI Job Search: copy the ones for your market from [community-portals](https://github.com/Bored008/Automated-Job-Find-And-Apply) (e.g. `linkedin-search`, `freehire-search` under `portals/global/`), or build one with `/add-portal`. You do **not** need a matching `site:` line below for those CLIs to run.

The `site:` query templates in this file are the **WebSearch fallback** — for portals without a CLI, company career pages, or when a CLI fails.

**Language scope:** write every query category in every language listed in your CLAUDE.md Languages table (typically 1-2, sometimes more). A posting requiring a language you have *not* declared, as a job condition, is excluded before scoring; a posting requiring a *higher level* than you declared in a language you *do* work in is flagged for your own judgment, not excluded — see `04-job-evaluation.md`'s Language Gate, the single source of truth for this rule. Translate each category's keywords rather than machine-translating word-for-word (e.g. "Frontend Developer" -> "Desarrollador Frontend", not a literal word-for-word translation) if you work in more than one language.

## Search Sites

Primary:
- **linkedin.com/jobs** - LinkedIn job listings (filter: India / Delhi NCR, Sonipat, Remote); also covered by the community `linkedin-search` CLI once installed
- **workatastartup.com & ycombinator.com/jobs** - Y Combinator startup directory and direct hiring for engineering and design roles (Remote / India)
- **unstop.com** (`unstop.com/jobs` & `unstop.com/internships`) - Premier Indian student and early-career hiring portal for tech internships, fresher roles, and developer hackathons
- **micro1.ai/jobs** (`jobs.micro1.ai`) - AI-vetted global remote hiring platform for top Frontend, Full-Stack, Python, and UI/UX Engineers
- **wellfound.com/jobs** - Startup and product engineering roles
- **instahyre.com** - Tech, frontend, and product design roles
- **naukri.com** - Major general job board in India (requires verifying individual posting active status)

Secondary (company career pages & ATS boards via Google):
- Direct ATS boards: `jobs.ashbyhq.com`, `boards.greenhouse.io`, `jobs.lever.co`
- Direct Google searches with `site:` filters for target startups and tech studios

## Query Categories

Queries are grouped by priority.

### Priority 1: Frontend & Full-Stack Web Development

These match your core engineering stack: React, Next.js, TypeScript, Node.js, and modern CSS.

#### Plain terms (portal CLIs)

```
frontend developer
full stack developer
next.js developer
react developer
```

#### WebSearch-only (`site:` fallback)

```
site:linkedin.com/jobs "frontend developer" "next.js" "delhi" OR "remote"
site:linkedin.com/jobs "full stack developer" "react" "node.js" "delhi" OR "remote"
site:workatastartup.com/companies ("frontend" OR "full stack") ("India" OR "remote")
site:ycombinator.com/jobs ("frontend" OR "full stack") ("India" OR "remote")
site:unstop.com/jobs ("frontend developer" OR "react developer" OR "next.js")
site:unstop.com/internships ("frontend" OR "web developer" OR "full stack")
site:micro1.ai/jobs ("frontend" OR "full stack" OR "react")
site:jobs.micro1.ai ("frontend" OR "react" OR "full stack")
site:wellfound.com/jobs "frontend developer" "typescript" "remote"
site:jobs.ashbyhq.com ("frontend" OR "react") ("India" OR "Remote")
```

### Priority 2: UI/UX & Product Design

These match your product design, Figma, wireframing, and design system capabilities.

#### Plain terms (portal CLIs)

```
ui ux designer
product designer
figma designer
```

#### WebSearch-only (`site:` fallback)

```
site:linkedin.com/jobs "ui/ux designer" "figma" "delhi" OR "remote"
site:linkedin.com/jobs "product designer" "design systems" "delhi" OR "remote"
site:workatastartup.com/companies ("product designer" OR "ui/ux") ("India" OR "remote")
site:unstop.com/internships ("ui/ux designer" OR "product designer")
site:unstop.com/jobs ("ui/ux designer" OR "product designer")
site:micro1.ai/jobs ("designer" OR "ui/ux" OR "product designer")
site:wellfound.com/jobs "product designer" "figma"
site:jobs.ashbyhq.com ("product designer" OR "ui/ux") ("India" OR "Remote")
```

### Priority 3: Design Engineering & Creative Technologist

Hybrid roles at the intersection of design craft and frontend code (Figma to Next.js/animations).

#### Plain terms (portal CLIs)

```
design engineer
ui engineer
creative technologist
frontend design
```

#### WebSearch-only (`site:` fallback)

```
site:linkedin.com/jobs "design engineer" "react" "figma" "delhi" OR "remote"
site:linkedin.com/jobs "ui engineer" "tailwind" "delhi" OR "remote"
site:wellfound.com/jobs "design engineer" "next.js"
```

### Priority 4: Software Engineer Intern / Early-Career Developer

Early-career and internship roles matching your current college schedule.

#### Plain terms (portal CLIs)

```
software engineer intern
frontend intern
web developer intern
```

#### WebSearch-only (`site:` fallback)

```
site:unstop.com/internships ("web developer intern" OR "frontend intern" OR "software intern")
site:unstop.com/jobs ("frontend" OR "full stack" OR "developer") ("fresher" OR "0-1 years")
site:linkedin.com/jobs "software engineer intern" "react" "delhi" OR "remote"
site:linkedin.com/jobs "frontend intern" "next.js" "delhi" OR "remote"
site:workatastartup.com/companies "intern" ("software" OR "frontend")
site:wellfound.com/jobs "frontend intern" "remote"
```

## Location Filter

When evaluating results, verify the job location is compatible with your college schedule in Sonipat:
- **Ideal:** Sonipat, Murthal, Remote
- **Acceptable (Onsite/Hybrid):** Delhi (metro-accessible), North/Central Delhi
- **Hybrid only (2-3 days max onsite):** Noida, Gurgaon, South Delhi, Greater Noida (daily commute is borderline)
- **Too far (unless 100% Remote):** Bangalore, Mumbai, Pune, Hyderabad, or any role requiring relocation outside Sonipat/Delhi NCR

## Language Filter

Your working languages and levels are in CLAUDE.md's Languages table. When filtering scraped results, apply `04-job-evaluation.md`'s Language Gate: a posting requiring a language you haven't declared at all is excluded; a posting requiring a higher level than you declared in a language you do work in is not excluded, flag it clearly instead (see `job-scraper/SKILL.md`'s Step 3 "Quick Fit Assessment" for how the flag surfaces in `/scrape` output). Postings simply *written* in a language you don't work in, that don't require it on the job, are fine.

## Date Filter

Only include jobs posted within the last 14 days, matching `/scrape` Step 1b.3: use a supported recency filter or filter the returned publication dates client-side. A future application deadline does not bypass this discovery window; `/rank` handles deadline expiry and urgency separately after discovery. If a posting date cannot be determined, include it but flag as "date unknown".

## Adapting Queries

If the user specifies a focus area, select queries from the matching category and also generate 2-3 custom queries for that focus. For example:
- "/scrape [focus_area]" -> relevant category queries + custom focus-specific queries
