# Contributing to Automated-Job-Find-And-Apply

Thank you for your interest in contributing to **Automated-Job-Find-And-Apply**!

## How to Contribute

1. **Fork the Repository**: Create a personal fork on GitHub.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/Bored008/Automated-Job-Find-And-Apply.git
   cd Automated-Job-Find-And-Apply
   ```
3. **Create a Feature Branch**:
   ```bash
   git checkout -b feat/your-feature-name
   ```
4. **Make Changes**:
   - Ensure scripts follow Python 3.10+ conventions.
   - Adhere to the Zero-Token Automation Protocol (use deterministic scripts or DOM injectors; avoid repetitive LLM token waste).
   - Test any new portal scrapers or form injectors.
5. **Commit and Push**:
   ```bash
   git commit -m "feat: add support for new ATS portal"
   git push origin feat/your-feature-name
   ```
6. **Open a Pull Request**: Submit your PR with a concise description of the changes and testing evidence.

## Guidelines & Principles
- **Efficiency**: Prioritize lightweight REST APIs and client-side scripts over heavy vision agent loops.
- **Privacy & Safety**: Never commit `.env`, session cookies, or personal credentials.
