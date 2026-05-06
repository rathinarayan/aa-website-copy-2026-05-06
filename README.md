# Automate Accelerator website direction

Created on 2026-05-06.

This folder is the recommended working copy for the next AA website pass. It starts from the 2026-05-06 redesign baseline and tightens the whole site: page flow, StoryBrand homepage structure, aggregate proof, contact path, accessibility basics, metadata, and version control.

## Decision

Use a two-offer public architecture:

1. Growth engine - one outbound growth product where human-led delivery and AI-scalable outbound work sit together.
2. AI Solutions - standalone internal business AI for operations, documents, support, reporting, ordering, and similar workflows.

Do not create a separate public Workshop page. Keep the workshop as a short section inside `data.html`.

## Proof hierarchy

Lead with aggregate proof, not one named client.

The site proves breadth first, using the `AA_Clients_ICPs` artefacts as the current source:

- Hundreds of Australian B2B businesses across many niches since 2021.
- 82 historical ICPs successfully structured into the aggregate data set.
- 36 Australian B2B niche profiles mapped from those ICPs.
- 42 canonical decision-maker roles mapped by function.
- 4,821 raw title signals reviewed across the source data.
- Named case studies only where permission and audited numbers are clear.

This is important because AA serves many niches. One client story can accidentally make the business look narrower than it is.

## What was borrowed from variants

- v03: plain StoryBrand clarity.
- v04: defensible niche, data, role and source proof.
- v05: human-first partnership language.
- v06: trust layer with awards and client videos.
- v07: AI as a capability layer, with a simpler public architecture.
- Variant 08: Data and ICP Workshop as the week-one ritual.
- v09: workshop detail, compressed into the Data page.
- v10: footer and production navigation.
- v11: final baseline structure.

## Files

- `index.html` - home page and main credibility pack.
- `services.html` - Growth engine and AI Solutions.
- `ai.html` - AI positioning and FAQ.
- `data.html` - data process and workshop section.
- `case-studies.html` - aggregate proof layer and niche grid.
- `team.html` - founders, team structure and awards.
- `contact.html` - enquiry form and direct email path.
- `privacy.html` - plain privacy page for the marketing site.
- `terms.html` - plain terms page for the marketing site.
- `404.html` - branded page-not-found route.
- `styles.css` - shared design system.
- `assets/favicon.svg` - simple branded favicon.

## Launch blockers

- Audit aggregate numbers before publish.
- Decide whether a common proof metric by niche is legally and commercially safe to publish.
- Add real client video assets only where permission and audited context are clear.
- Add real award logo files.
- Add final founder headshots and bios.
- Confirm Melvin's public title.
- Confirm LinkedIn URL, ABN and booking link.
