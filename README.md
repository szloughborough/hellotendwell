# Tendwell

US household-upkeep research site. Python standard library, no paid APIs required to build.

## Build
`python release_build.py` creates `dist/`. Default is a noindex release candidate.

## Public release gate
Do not set `public_release_approved` until content/keyword review, exact affiliate checks, operator/contact details, domain ownership and browser QA are complete. Fill real operator and contact details in `release.json`. This flag is an operational sign-off, not an automated factual validation.

## Cloudflare Pages
Connect this private GitHub repository to a Pages project. Build command: `python release_build.py`. Output directory: `dist`. Use the main branch for production. Do not enable public release before the gate above passes. Add hellotendwell.com through Custom Domains and follow the account-provided DNS records; do not invent DNS targets.

Preview branches must leave public_release_approved false. No secrets, raw research, API credentials or Sites hosting identity belong in this repository. Product images are catalog assets already used by the site; their continued usage permissions remain those of their source programs.
