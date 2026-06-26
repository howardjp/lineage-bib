# Lineage BibTeX Initial Audit Report

Audit date: 26 June 2026

This report records a conservative, source-centric inventory of `lineage.bib`. No entry should be deleted or merged unless the underlying source identity is clear. The detailed old-to-new mappings are in [`migration.csv`](migration.csv).

## Summary

- Original entry count: **222**
- Duplicate BibTeX keys: **0**
- Keys already matching the required lowercase, hyphen-separated form: **11**
- Keys requiring format or source-identity normalization: **211**
- Entries containing a `filename` field: **25**
- Entries missing `filename`: **197**
- Existing `filename` values not identical to their current BibTeX keys: **17**
- High-confidence canonical source groups: **38**
- High-confidence duplicate entries removed by those groups: **46**
- Projected entry count after the high-confidence groups only: **176**
- Manual-review groups: **9** involving **21** entries

The projected count is deliberately conservative. It does not assume that every similarly titled FamilySearch record belongs to the same image group, and it does not collapse different volumes merely because they belong to one series.

## High-confidence consolidation groups

| Canonical key | Old entries | Net reduction | Evidence |
|---|---:|---:|---|
| `ancestry-massachusetts-town-vital-records-1620-1988` | 8 | 7 | Ancestry database title |
| `familysearch-medfield-records-007009438` | 3 | 2 | FamilySearch Image Group Number |
| `familysearch-medway-records-007010687` | 3 | 2 | FamilySearch Image Group Number |
| `ancestry-new-england-marriages-prior-to-1700` | 2 | 1 | Ancestry database title |
| `anderson-great-migration-begins-1995` | 2 | 1 | Same underlying publication |
| `ancestry-indiana-death-certificates-1899-2017` | 3 | 2 | Ancestry database title |
| `ancestry-us-find-a-grave-index-1600s-current` | 2 | 1 | Ancestry database title |
| `ancestry-1880-united-states-federal-census` | 2 | 1 | Ancestry database title |
| `ancestry-ohio-wills-probate-records-1786-1998` | 2 | 1 | Ancestry database title / exact record |
| `ancestry-us-quaker-meeting-records-1681-1994` | 2 | 1 | Ancestry collection 2189 |
| `familysearch-connecticut-vital-records-008272229` | 2 | 1 | FamilySearch Image Group Number |
| `familysearch-ohio-county-marriages-004016605` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004016605 or exact indexed-record URL |
| `familysearch-ohio-county-marriages-004030292` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004030292 or exact indexed-record URL |
| `familysearch-ohio-county-births-004016861` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004016861 or exact indexed-record URL |
| `familysearch-ohio-county-births-004017450` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004017450 or exact indexed-record URL |
| `familysearch-united-states-census-1920-004967549` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004967549 or exact indexed-record URL |
| `familysearch-ohio-deaths-004022913` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004022913 or exact indexed-record URL |
| `familysearch-ohio-deaths-004028080` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004028080 or exact indexed-record URL |
| `familysearch-ohio-county-marriages-005261999` | 2 | 1 | Same FamilySearch image group/digital folder identifier 005261999 or exact indexed-record URL |
| `familysearch-numident-di0001099` | 2 | 1 | Same FamilySearch image group/digital folder identifier DI0001099 or exact indexed-record URL |
| `familysearch-ohio-deaths-004109222` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004109222 or exact indexed-record URL |
| `familysearch-united-states-census-1900-004117743` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004117743 or exact indexed-record URL |
| `familysearch-kentucky-marriages-004263448` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004263448 or exact indexed-record URL |
| `familysearch-united-states-census-1910-004973199` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004973199 or exact indexed-record URL |
| `familysearch-world-war-i-draft-registration-005256033` | 2 | 1 | Same FamilySearch image group/digital folder identifier 005256033 or exact indexed-record URL |
| `familysearch-west-virginia-births-007499359` | 2 | 1 | Same FamilySearch image group/digital folder identifier 007499359 or exact indexed-record URL |
| `familysearch-ohio-deaths-004000569` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004000569 or exact indexed-record URL |
| `familysearch-ohio-county-marriages-004016206` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004016206 or exact indexed-record URL |
| `familysearch-ohio-county-marriages-004016278` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004016278 or exact indexed-record URL |
| `familysearch-ohio-deaths-004021648` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004021648 or exact indexed-record URL |
| `ancestry-civil-war-prisoner-of-war-records-1861-1865` | 2 | 1 | Same Ancestry database title/collection or exact database record |
| `ancestry-ohio-soldier-grave-registrations-1804-1958` | 2 | 1 | Same Ancestry database title/collection or exact database record |
| `familysearch-united-states-census-1920-004967469` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004967469 or exact indexed-record URL |
| `familysearch-united-states-census-1860-005170959` | 2 | 1 | Same FamilySearch image group/digital folder identifier 005170959 or exact indexed-record URL |
| `familysearch-united-states-census-1870-004278470` | 2 | 1 | Same FamilySearch image group/digital folder identifier 004278470 or exact indexed-record URL |
| `ancestry-social-security-applications-claims-1936-2007` | 2 | 1 | Same Ancestry database title/collection or exact database record |
| `ancestry-ohio-death-records-1908-2022` | 2 | 1 | Same Ancestry database title/collection or exact database record |
| `familysearch-worcester-probate-records-007704428` | 1 | 0 | Same FamilySearch image group/digital folder identifier 007704428 or exact indexed-record URL |

## Manual review required

### R1

Entries: `familysearch-breck-bethia-1673`, `familysearch-rocket-susanna-1675`, `familysearch-thompson-susanna-1712`, `familysearch:vital-morse-elizabeth-1655`

Likely Medfield town records, but the Image Group Number is not stated in these entries.

### R2

Entries: `newman:joseph:death:1893`, `rp:death:record:1881`

Possibly the same Ohio county death volume or image group; the entries use different indexed records and do not state a shared Image Group Number.

### R3

Entries: `wn:civil:war:abstract:1862`, `newman:wesley:soldier:profiles:1862`

Likely the same Historical Data Systems compilation, but the first entry lacks a stable database identifier or URL.

### R4

Entry: `joseph:cloud:birth:1743`

Possibly belongs with `ancestry-us-quaker-meeting-records-1681-1994`; its title says 1681–1935 and it lacks Ancestry collection ID 2189.

### R5

Entries: `nj:wills:1901`, `nj:wills:abstracts`, `daniels:will:1758`

Potential overlap among published New Jersey will abstracts and Ancestry database records, but the volumes and editions differ.

### R6

Entries: `newman:joseph:1850:census`, `jn:rn:wn:census:1850`

Likely the same household schedule; the non-FamilySearch entry lacks a URL and image-group identifier.

### R7

Entries: `newman:joseph:1860:census`, `jn:rn:wn:census:1860`

Likely the same household schedule; verify the NARA roll/page against the FamilySearch image.

### R8

Entries: `anderson:great:migration:2003`, `anderson:book:2007`

Different volumes in the *Great Migration, 1634–1635* series; retain separately unless series-level consolidation is intentionally adopted.

### R9

Entries: `snyder_fullmer_marriage_license_1938`, `snyder_williams_divorce_1933`, `snyder_williams_marriage_1927`

All three cite the same Newspapers.com image URL despite different dates and page locators; likely at least two URLs are wrong.

## Structural and metadata problems

1. **Required `filename` field.** 197 entries do not contain it. Of the 25 entries that do, 17 use a hyphenated filename that differs from the current colon-based key. The key and `filename` must be changed together.
2. **Key format.** 211 of 222 keys fail the required lowercase, hyphen-separated pattern. Some of the 11 syntactically valid keys remain person- or event-centric and still require source-level replacement.
3. **Duplicate field.** `mayo1996` contains two `editor` fields.
4. **Invalid field name.** `dixon:our:book:1932` contains `subtitle.` rather than `subtitle`.
5. **Placeholder URL.** `ancestry-daniel-bithiah-1754` contains `XXXXX:2495` in its URL.
6. **Case-sensitive key defect.** `mcneal:Kentucky:marriage:1907` contains an uppercase letter.
7. **Repository mismatch.** `daniels:will:1758` names FamilySearch as author but links to Ancestry.
8. **Generic URLs.** Numerous Ancestry entries point only to the Ancestry home page. These should retain database metadata and, when available, a stable record or collection URL.
9. **Access year used as publication year.** Several database entries use 2024 or 2025 as `year` even though that is the access date. Chicago-friendly metadata should separate publication/database year from `urldate`.
10. **Record data embedded in source titles.** Many titles name a person or event rather than the database, image group, volume, article, or publication. Those details belong in locators or notes.

## Possible citation problems

- `snyder_fullmer_marriage_license_1938`, `snyder_williams_divorce_1933`, and `snyder_williams_marriage_1927` cite the same Newspapers.com image despite different publication dates and pages. They must not be merged until the correct images are identified.
- `wgh:draft:card:1917` explicitly says that the FamilySearch indexed record was retired as a duplicate. A replacement or image-level citation should be located.
- `familysearch:probate:worcester-1748` identifies Film/Image Group 007704428 but uses a year-specific key. The migration table renames it to the source-level key `familysearch-worcester-probate-records-007704428`.
- Several census entries cite the same household through different indexed-person ARKs. Where a shared digital folder or archival page is explicit, they are consolidated; otherwise they remain review items.

## Work still required for a final cleaned bibliography

- Apply the approved mappings while merging complementary metadata and preserving all useful URLs and repository information.
- Create source-based keys for the remaining entries not yet represented in `migration.csv`.
- Add matching `filename` fields to every surviving entry.
- Replace record-level notes with reusable source metadata and move person, page, image, and case details into citation locators.
- Validate the result with `python scripts/audit_bib.py lineage.bib --strict`.

## Current status

The audit and migration decisions are complete for the high-confidence groups above. The bibliography itself has not yet been rewritten, because the repository interface available in this session exposes `lineage.bib` only in bounded read segments and requires complete-file replacement for an edit. Rewriting the 2,500-line blob without an exact local copy would risk data loss, contrary to the conservative rule.
