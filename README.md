# Protein Folding Statistics — Dataset Construction

Pipeline for building per-organism datasets that link protein structure (AlphaFold),
mRNA/codon-level translation dynamics, and residue-level solvent accessibility, for use
in downstream folding/translation statistics (part of the **ExpressinHost** project,
which aims to express industrially relevant proteins in model host organisms).

Three finalized datasets are included, covering *E. coli*, yeast (*Saccharomyces
cerevisiae*), and *Arabidopsis thaliana*.

## Contents

```
Dataset construction/
├── PROTOCOL dataset construction.docx   # Full step-by-step protocol (source of truth)
├── alphafold_pdb_downloader.html        # Standalone tool (by Thierry) for bulk AlphaFold PDB download
├── scripts/                             # Numbered pipeline scripts, run in order
│   └── alternate strategy_mRNA sequence retrieval/   # Fallback path for step 8 (see below)
└── finalised datasets/
    ├── E.coli_dataset.csv
    ├── Yeast_dataset.csv
    └── Arabidopsis_dataset.csv
```

Scripts were written per-organism with hardcoded local file paths (originally under
`/Users/jagjotarora/Documents/RSA project/<Organism>/...`) — they are templates to be
copied and re-pointed at your own paths/organism, not a one-command pipeline.

## Pipeline overview

The pipeline starts from a chosen organism's proteome on UniProt and progressively
enriches a single master CSV per organism until it carries structure, sequence,
translation-speed, and accessibility data for every protein.

| Step | Script | Purpose |
|---|---|---|
| 1 | `1_single domain proteins.py` | Query UniProt REST API per accession; keep only single-domain proteins (filters a UniProt search export of reviewed proteins, length 1–400 aa). |
| 2 | `2_csv to txt file.py` | Flatten the UniProt ID column into one comma-separated `.txt` string for bulk submission. |
| — | `alphafold_pdb_downloader.html` | Browser tool: paste the comma-separated IDs to bulk-download AlphaFold PDB structures + a `proteins.csv` (sequence length, pLDDT/`globalMetricValue`). |
| 3 | `3_merging csv files.py` | Merge multiple `proteins*.csv` outputs (downloads often come in batches). |
| 4 | `4_pLDT_filtering.py` | Keep only structures above a pLDDT confidence threshold (≥75, or ≥85 for *E. coli*). |
| 5 | `5_gtf to csv.py` | Parse a UCSC/NCBI RefSeq `.gtf` annotation file into a flat CSV (attribute column split into `gene_id`, `transcript_id`, `gene_name`, `exon_number`, `exon_id`). |
| 6 | `6_extracting gene names.py` | Look up each UniProt accession's gene name via the UniProt XML API. |
| 7 | `7_adding locations.py` | Join gene names against the GTF CSV to attach transcript CDS start/end and strand orientation. |
| 8a/8b | `8a_mRNA sequence retrieval + orientation.py` / `8b_mRNA sequence retrieval - orientation.py` | Extract the CDS nucleotide sequence from the genome FASTA using CDS start/end, split by strand: 8a for `+`, 8b for `-` (reverse-complemented). Outputs are merged back together with script 3. |
| — | `alternate strategy_mRNA sequence retrieval/` | Fallback if the GTF/FASTA approach fails for an organism: `getting NM ids.py` resolves RefSeq `NM_` IDs from UniProt, `removing empty NM rows.py` drops unresolved ones, `getting mRNA from NM ids.py` fetches the CDS directly from NCBI Entrez by `NM_` ID. |
| 9 | `9_mRNA cleaning.py` | Normalize retrieved sequences: `T`→`U`, force a leading `A` (for `AUG`), drop any sequence that still doesn't start with `AUG`. |
| 10 | `10_mRNA translation.py` | Translate cleaned mRNA to an amino-acid sequence (stops at first stop codon). |
| 11 | `11_PDB aa and ss retrieval.py` | Parse each downloaded PDB file with DSSP to extract the observed AA sequence and per-residue secondary-structure string; runs in parallel batches with cooldowns to avoid overload. |
| 12 | `12_translation columns check.py` | Sanity check: keep only rows where the translated AA sequence matches the AA sequence extracted from the PDB structure. |
| 13 | `13_making processed table.py` | Convert a raw per-organism codon-usage table (AA, tRNA anticodon, codon, tRNA gene copy number (GCN), wobble partner) into a processed table with per-codon **Rank** and **Speed** (tRNA abundance/wobble-adjusted) values. |
| 14 | `14_adding speed column.py` | Walk each mRNA sequence codon-by-codon and attach a per-codon **Speed** profile using the processed codon table. |
| 15 | `15_adding rank column.py` | Same, but attaches the per-codon **Rank** profile. |
| 16 | `16_adding SASA and RSA.py` | Compute per-residue Solvent-Accessible Surface Area (Shrake–Rupley) and Relative SASA (normalized against Miller et al. 1987 reference values) from the PDB structures. |
| 17 | `17_adding hydrophobicity values.py` | Attach a per-residue Kyte–Doolittle hydrophobicity profile from the extracted AA sequence. |

The protocol document (`PROTOCOL dataset construction.docx`) is the authoritative
walkthrough, including where to source the UniProt search, GTF/FASTA files, and
per-organism codon tables (see the ExpressinHost codon-table repo linked in the
protocol). Read it before rerunning the pipeline on a new organism.

## Finalized datasets

`finalised datasets/*.csv`, one row per protein:

| Column | Description |
|---|---|
| `uniprotAccession` | UniProt ID |
| `isReviewed` | UniProt review status |
| `globalMetricValue` | AlphaFold pLDDT confidence score |
| `sequenceLength` | Protein length (aa) |
| `gene_name` | Gene symbol |
| `transcript_CDS_start`, `transcript_CDS_end`, `orientation` *(E. coli only)* | CDS genomic coordinates and strand, from the GTF-based retrieval path |
| `NM_ID` *(Yeast/Arabidopsis only)* | RefSeq transcript ID, from the alternate NCBI retrieval path |
| `Retrieved_Sequence` / `Retrieved_sequence` | Cleaned mRNA (CDS) sequence |
| `Translated AA Sequence` | AA sequence translated from the mRNA |
| `Extracted AA Sequence` | AA sequence extracted from the AlphaFold PDB structure |
| `Secondary Structure Profile` | Per-residue DSSP secondary-structure string |
| `Speed_Profiles` | Per-codon translation speed values |
| `Rank_Profiles` | Per-codon tRNA abundance rank values |
| `SASA Profile` | Per-residue solvent-accessible surface area |
| `RSA Profile` | Per-residue relative solvent accessibility (% of max) |
| `Hydrophobicity values` | Per-residue Kyte–Doolittle hydrophobicity |

Note the *E. coli* dataset was built via the GTF/FASTA path (steps 5–8) and so carries
CDS coordinates instead of an `NM_ID`; yeast and Arabidopsis were built via the
alternate NCBI `NM_ID` path.

## Dependencies

Scripts rely on: `pandas`, `polars`, `numpy`, `requests`, `biopython` (`Bio.Seq`,
`Bio.SeqIO`, `Bio.PDB` incl. `DSSP`, `ShrakeRupley`, `PPBuilder`), `tqdm`, `pyarrow`,
`matplotlib`. DSSP requires the `mkdssp` binary available on `PATH`.
