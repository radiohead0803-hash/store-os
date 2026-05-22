# Patent, Copyright, Trademark, and Design-Right Precheck

This reference defines the preliminary AI/rule screening workflow. It is not legal advice and must not replace qualified review where risk is material.

## Required workflow
1. Run `ip-precheck` against listings, printable text, image prompts, and store import staging files.
2. Block public use when severity is `high` unless the operator records a rights/license exception.
3. Use generated search queries for KIPRIS trademark, patent/design search, copyright office checks, and platform brand-policy checks.
4. Record source logs for any design element, icon, font, photo, prompt, or template used in a public asset.
5. Require human approval before using characters, brand names, school/education result claims, celebrity likeness, or copied design layouts.

## High-risk indicators
- Famous characters or franchise names.
- Brand/logos, confusingly similar product titles, or protected mascots.
- Claims such as 100% guarantee, guaranteed academic improvement, medical/psychological outcomes, or absolute refund refusal.
- New mechanical structures, unique sticker mechanisms, packaging devices, or design shapes that may touch patent/design rights.

## Output gate
`ip_precheck.csv` must be attached to the proof dossier before public listing, image publication, store import, or paid ad launch.
