# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A dataset-construction pipeline (part of the **ExpressinHost** project) that builds
per-organism CSV datasets linking AlphaFold protein structure, mRNA/codon-level
translation dynamics, and residue-level solvent accessibility — used for downstream
folding/translation statistics. There is no application code, build system, or test
suite: this is a sequence of standalone, numbered Python scripts plus the finalized
output datasets. See `README.md` for the full pipeline-stage table and dataset column
reference; `Dataset construction/PROTOCOL dataset construction.docx` is the
authoritative step-by-step walkthrough (including where to source UniProt searches,
GTF/FASTA files, and per-organism codon tables).

## Repo layout

```
Dataset construction/
├── PROTOCOL dataset construction.docx   # authoritative protocol
├── alphafold_pdb_downloader.html        # browser tool for bulk AlphaFold PDB download
├── scripts/                             # numbered pipeline, run in order (1 -> 17)
│   └── alternate strategy_mRNA sequence retrieval/   # fallback for step 8
└── finalised datasets/                  # one CSV per organism, the published output
```

## Running the scripts

- **There is no runner, CLI, build, lint, or test step** — each numbered script in
  `scripts/` is a standalone, per-organism template. Every script builds its example
  paths from a `WORK_DIR = "Dataset construction/work"` constant defined right next to
  them (near the bottom of the file) — a local, untracked scratch directory for
  raw/intermediate per-organism files (genome FASTA/GTF, raw UniProt/AlphaFold
  downloads, PDB folders, per-step CSVs) that is `.gitignore`d and does not exist until
  you create and populate it yourself. Always check/adjust the organism name and exact
  filenames baked into a script's example paths before running it. Scripts never write
  into `finalised datasets/` directly — that holds only already-published output;
  promote a freshly-built dataset there yourself once validated.
- **Known issue, not yet fixed**: `scripts/alternate strategy_mRNA sequence retrieval/getting mRNA from NM ids.py`
  still hardcodes the original author's personal email (`jagjotarora07@gmail.com`) as
  the default for NCBI Entrez's required `email` param — replace it with your own
  before running that script.
- Scripts have no shared `requirements.txt`/`pyproject.toml`. Dependencies observed
  across the pipeline: `pandas`, `polars`, `numpy`, `requests`, `biopython` (`Bio.Seq`,
  `Bio.SeqIO`, `Bio.PDB` — `PDBParser`, `DSSP`, `ShrakeRupley`, `PPBuilder`), `tqdm`,
  `pyarrow`, `matplotlib`. Steps 11 and 16 (DSSP-based structure parsing) require the
  `mkdssp` binary available on `PATH`.
- Run scripts in numeric order (`1_single domain proteins.py` → ... →
  `17_adding hydrophobicity values.py`); each one reads the previous step's output CSV
  and writes an enriched CSV. Step 8 branches into two strategies (see below) that
  reconverge before step 9.

## Pipeline architecture

The pipeline progressively enriches a single master CSV per organism, starting from a
UniProt proteome query and ending with structure + translation-dynamics + accessibility
data for every protein:

1. **Selection** (1-2): filter UniProt hits to single-domain proteins; flatten IDs for
   bulk submission.
2. **Structure acquisition** (external tool → 3-4): bulk-download AlphaFold PDBs via
   `alphafold_pdb_downloader.html`, merge batched `proteins.csv` outputs, filter by
   pLDDT confidence (`globalMetricValue`).
3. **Gene/location mapping** (5-7): parse a UCSC/NCBI RefSeq `.gtf` into CSV, resolve
   gene names via UniProt, join to attach CDS start/end + strand.
4. **mRNA retrieval — two alternate strategies for step 8**, chosen per-organism
   depending on which GTF/FASTA sourcing actually works:
   - **GTF/FASTA path** (`8a`/`8b`): extract CDS sequence directly from the genome
     FASTA using CDS coordinates, split by strand (`8a` for `+`, `8b` for `-`,
     reverse-complemented), then merged with script `3`. Produces
     `transcript_CDS_start`/`end`/`orientation` columns. Used for the *E. coli*
     dataset.
   - **NCBI `NM_ID` path** (`scripts/alternate strategy_mRNA sequence retrieval/`):
     resolve RefSeq `NM_` IDs from UniProt, drop unresolved rows, fetch CDS directly
     from NCBI Entrez. Produces an `NM_ID` column instead. Used for the Yeast and
     Arabidopsis datasets.
   - This is **why the finalized dataset CSVs have different schemas** — always check
     which path an organism's data went through before assuming a column exists.
5. **Cleaning/translation** (9-10): normalize retrieved sequences (`T`→`U`, force
   leading `AUG`, drop non-conforming rows), translate to amino acids.
6. **Structure cross-check** (11-12): extract AA sequence + DSSP secondary-structure
   string from the downloaded PDB files (parallelized in batches with cooldowns to
   avoid rate limits); keep only rows where translated and structure-derived AA
   sequences match.
7. **Codon dynamics** (13-15): convert a raw per-organism codon-usage table (from the
   ExpressinHost codon-table repo linked in the protocol) into a processed table with
   per-codon tRNA-abundance **Rank** and wobble-adjusted **Speed**; walk each mRNA
   codon-by-codon to attach per-codon Speed and Rank profiles.
8. **Accessibility/hydrophobicity** (16-17): per-residue SASA (Shrake–Rupley) and RSA
   (normalized against Miller et al. 1987 reference values) from the PDB structures;
   per-residue Kyte–Doolittle hydrophobicity from the AA sequence.

## Dataset growth convention

New organism datasets are **appended**, not rewritten — existing finalized CSVs stay
untouched once published. Keep using plain git for the dataset CSVs (no Git LFS, no
Releases) as long as each file stays well under GitHub's 50MB warning threshold; this
holds for the planned scale (roughly 5-10 organisms total). Revisit that choice only if
a single file approaches ~50MB or a published dataset needs in-place correction.

Every change (new dataset, script edit, doc update) should be its own git commit with
a clean, descriptive, imperative message.
