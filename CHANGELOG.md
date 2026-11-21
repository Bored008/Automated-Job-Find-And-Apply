# Changelog

All notable changes to **Automated-Job-Find-And-Apply** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-21

### Added
- **Multi-Platform ATS & Portal Sourcing**: Concurrent crawlers for Ashby ATS, Greenhouse, Lever, and Unstop (Jobs & Internships).
- **Zero-Token Automation Suite**:
  - `tools/unstop_direct_applier.py`: Deterministic REST API application script with deduplication checks.
  - `tools/universal_form_filler.js`: High-speed DOM evaluator for instant form population.
  - `extensions/job-search-autofill`: Chrome Extension (Manifest V3) for 1-click client-side autofill.
  - `extensions/autofill.user.js`: Standalone cross-browser Userscript.
  - `tools/application_queue_launcher.html`: Interactive local batch launcher for vetted positions.
- **Strict Guardrail & Scoring Engine**:
  - Filters positions strictly for 100% Remote or Sonipat / Delhi NCR.
  - Stack alignment for React, Next.js, TypeScript, Python, Tailwind CSS, and Figma (UI/UX Design).
- **Autonomous Gmail & OTP Resolver**: Real-time parsing of 6-digit email verification OTPs and receipt capture.
- **Google Calendar Sync**: Automatic scheduling of coding assessments and interview deadlines.
- **Obsidian Memory System**: Automated progress logging to daily logs and active context tracking.
