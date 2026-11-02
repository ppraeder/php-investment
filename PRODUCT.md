# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Potential contacts who want to understand PHP-Investment GmbH and find a way to contact the company.

## Product Purpose

A simple company landing page. Success means visitors understand the company's basic purpose and can find its contact details.

## Capabilities and Constraints

- The existing German-language website introduces PHP-Investment GmbH as a Beteiligungs- und Holdinggesellschaft with a long-term entrepreneurial focus.
- The scope is company information and contact, with supporting Impressum and Datenschutz pages.
- Contact is through the published email address; the current website has no contact form, accounts, or transactions.
- Preserve the existing static HTML/CSS architecture: no production JavaScript, build step, database, or external runtime dependencies.
- The repository specifies Hetzner Webhosting deployment, system fonts, and no cookies, tracking, analytics, CDNs, or external embeds.
- Local development uses `python3 -m http.server 8080`; structural checks use `python3 scripts/check_site.py`.

## Brand Commitments

Use the existing company name, PHP-Investment GmbH, and German-language content. Preserve factual company and contact information unless the user supplies corrections.

## Evidence on Hand

- `index.html`: company introduction and published contact details.
- `impressum.html` and `datenschutz.html`: existing legal information.
- `README.md`: architecture, deployment instructions, and historical publication checklist. Some checklist items may be stale; compare them with current source before relying on them.
- No investment performance claims, portfolio evidence, testimonials, or customer claims have been supplied for this initialization.

## Product Principles

- Keep the landing page focused on introducing the company and enabling contact.
- Make company information and contact details easy to find and understand.
- Preserve the lightweight, privacy-conscious implementation.
- Base factual claims on supplied company information.

## Open Decisions

No narrower audience segment or additional company positioning has been confirmed. No new features are requested.
