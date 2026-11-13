# Circular economy in dairy processing: data and code

Data and code for the review article:

> Sarker, S., Mahmud, T. *Circular Economy in Dairy Processing: A Critical Review of Intervention Transferability, with Bangladesh as Case Study.* Unpublished manuscript.

Repository author: **Tuhin Mahmud**

## Contents

```
data/      11 data files (10 CSV, 1 Excel)
code/      7 Python scripts
README.md
LICENSE
requirements.txt
```

### Data (`data/`)

| File | Content | Article |
|---|---|---|
| `Study_level_data.xlsx` | Setting, scale, feed strength and reported result of the 67 studies read in full; reference numbers follow the article | Table 3 |
| `Disclosure_audit_coding_sheet.csv` | Public-disclosure audit, 4 processors × 8 indicators | Appendix A, Table 6 |
| `S3_family_counts.csv` | OpenAlex record counts per intervention family (all / CE-framed) | Appendix B, Table B.1 |
| `S3_family_regions.csv` | Author-country shares by region | Figure 3b, Table 4 |
| `S3_family_years.csv` | Records per year, 2010–2026 | — |
| `S4_AD_energy_balance.csv` | Digester energy balance at measured influent COD | Section 6.5, Appendix C.1 |
| `S4_whey_corners.csv` | Whey ratio R at all parameter corners | Section 6.5, Appendix C.2 |
| `S6_effluent_strength_dataset.csv` | COD/BOD dataset by stream type | Figure 6a |
| `S6_national_whey_estimate.csv` | National chhana whey COD estimate | Table 7, Appendix C.3 |
| `S6_sensitivity.csv` | Share of uncertainty by input | Section 6.6, Appendix C.3 |
| `S6_robustness.csv` | Distribution, correlation and one-at-a-time checks | Section 6.6, Appendix C.3 |

The CSV files are the master copies; the scripts read and write them by name.

### Code (`code/`)

| Script | Produces | Article |
|---|---|---|
| `S3_openalex_family_counts.py` | `S3_*.csv` | Figures 3 and 7, Appendix B |
| `bounding_analysis.py` | `S4_*.csv` | Figure 5, Section 6.5 |
| `quant_synthesis.py` | `S6_effluent_strength_dataset.csv`, `S6_national_whey_estimate.csv`, `S6_sensitivity.csv` | Figure 6, Table 7 |
| `S6_robustness.py` | `S6_robustness.csv` | Section 6.6 |
| `fig1_overview.py` | — (no data) | Figure 1 |
| `fig1_transfer_filter.py` | — (conceptual) | Figure 2 |
| `fig3_milk_flow.py` | — | Figure 4 |

Script and output file names keep their original numbering; the **Article** column gives the figure and table numbers used in the paper.

## How to reproduce

```bash
pip install -r requirements.txt
python code/quant_synthesis.py
python code/S6_robustness.py
python code/bounding_analysis.py
python code/S3_openalex_family_counts.py --replot   # redraws Figures 3 and 7 from the saved CSVs
python code/fig1_overview.py
python code/fig1_transfer_filter.py
python code/fig3_milk_flow.py
```

Scripts read and write the CSV files in `data/` and save figures (PNG, PDF, TIFF) to a new `figures/` folder; they can be run from any directory.

To re-query OpenAlex instead of using the saved counts, get a free API key from <https://openalex.org/rest-api> and run
`python code/S3_openalex_family_counts.py YOUR_API_KEY` (or set the `OPENALEX_API_KEY` environment variable). Live counts change as OpenAlex is updated, so they will differ slightly from the saved CSVs, which were retrieved in November 2026.

Monte Carlo runs use a fixed seed (20260923), so re-running reproduces the CSV outputs exactly. Outputs were generated with Python 3.12, NumPy 2.4, Matplotlib 3.10 and SciPy 1.17, and were re-checked with NumPy 2.5, Matplotlib 3.11 and SciPy 1.18.

## License

Code: MIT License (see `LICENSE`). Data files: Creative Commons Attribution 4.0 International (CC BY 4.0).

## How to cite

Please cite the article above.
