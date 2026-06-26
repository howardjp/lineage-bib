# Lineage BibTeX

A source-centric BibTeX library for genealogical research and lineage-society documentation.

## Governing principle

The library contains **one BibTeX entry per underlying source**, not one entry per person, event, page, image, or extracted record.

Record-specific information belongs in the citation locator:

```latex
\fullcite[image 180 of 601]{familysearch-medfield-records-007009438}
```

It does not belong in a new BibTeX key when the cited material is part of a source already represented in the library.

## Canonical bibliography

The maintained bibliography is [`lineage.bib`](lineage.bib).

Every entry must include:

```bibtex
filename = {same-as-key},
```

The `filename` value must exactly match the entry key.

## Key conventions

Keys are lowercase, hyphen-separated, and source-based. Examples:

- `familysearch-medfield-records-007009438`
- `ancestry-massachusetts-town-vital-records-1620-1988`
- `jameson-biographical-sketches-medway-1886`
- `bond-genealogies-watertown-1860`
- `anderson-great-migration-begins-1995`

Do not put a person's name, event, page, image, case, or record number in a key unless it identifies the underlying source itself.

## Consolidation rules

- **FamilySearch image records:** consolidate by Image Group Number.
- **Ancestry databases:** consolidate by database title.
- **Books:** consolidate by publication.
- **Journal articles:** consolidate by article.
- **Probate, deed, church, and town records:** consolidate by volume or image group.
- **Page, image, volume, case, and record details:** place in the citation locator.

Do not merge entries unless the sources are clearly identical. Uncertain cases belong in the manual-review section of the audit report.

## Adding a source

1. Search `lineage.bib` for the source, database title, image-group number, author, title, repository, and URL.
2. If the source already exists, reuse its key and provide the appropriate locator.
3. If it is new, add one complete, Chicago-friendly BibTeX entry.
4. If it may duplicate another entry but the identity is uncertain, preserve both and flag the pair for review.

Preserve useful URLs, repositories, publishers, archival identifiers, and complementary notes. Normalize publisher and repository names only when the equivalence is clear.

## Validation

Run:

```bash
python scripts/validate_bib.py lineage.bib
```

The validator checks basic entry structure, unique keys, key format, and the required `filename` field.

## Cleanup records

Large consolidations should update:

- [`migration.csv`](migration.csv): old-to-new key mappings;
- [`audit-report.md`](audit-report.md): counts, merges, review items, metadata gaps, and possible citation problems.
