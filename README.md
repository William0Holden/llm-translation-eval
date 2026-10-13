# LLM vs. NMT: Korean→English Translation Evaluation

Course project for **PHIL 8400 (University of Georgia, Fall 2025)**. The project simulates a professional translation workflow and then benchmarks commercial neural MT engines, frontier LLMs, and locally run open-weight LLMs on a Korean→English medical text (a 229-segment excerpt of a spinal-cord-injury resource guide).

## Method

1. **Data preparation and CAT workflow (Part I).** Built a bilingual sentence-aligned spreadsheet of the excerpt, a glossary/term base, and translation memories, then ran a memoQ project with three pre-translation analyses:
   - TM1 (Wikipedia health TMs + WikiMatrix, ~300k segments): 94.45% no match, 5.55% in the 50–74% fuzzy band.
   - TM2 (project-specific TM): 44.76% 100% matches, 55.24% 95–99% matches.
   - Tweaked TM2: 41.86% 100%, 48.16% 95–99%, new lower fuzzy bands, 0.96% no match.
   Followed by a memoQ QA pass.
2. **Machine translation (Parts II–III).** Translated the Korean source into English with 15 systems (below). The LLMs got the same prompt:
   > The attached TXT file has 229 lines/cells. Each line contains a separate Korean sentence. Translate each Korean sentence to English, line by line, and copy your output below. Please do not provide any explanations; only translations, line by line. Provide your COMPLETE response in raw text so that it may be copied and pasted in the same format it was received in. Make sure the final output is same number of lines/cells. Return the sentences now

   Web LLMs used their reasoning modes (DeepSeek DeepThink, ChatGPT-5 thinking, Claude extended thinking). Where a model merged two source lines into one, the output was re-split to keep 229 aligned lines.
3. **Automatic evaluation (Part IV).** Scored every system with [MATEO](https://github.com/BramVanroy/mateo-demo) using **COMET, BLEU, chrF2 and TER**, with 95% confidence intervals and paired significance tests against a baseline system. Then computed Pearson (r) and Spearman (ρ) correlations between the metrics and pulled the sentences with the largest score differences between the best and worst systems.

## Systems

| Type | Systems |
|---|---|
| Commercial NMT | DeepL, Google Translate, ModernMT |
| Frontier LLMs (web) | GPT-5, Claude, DeepSeek |
| Local open-weight LLMs | Llama 3.2 1B, Llama 3.1 8B, Llama 3.3 70B (instruct, fp16); Qwen3 1.7B, Qwen3 8B (fp16); Gemma 3 27B (it, fp16); gpt-oss 20B, gpt-oss 120B; Aya 23 35B (q8_0) |

## Results

Two evaluation settings were run. All scores are MATEO system-level scores (higher is better except TER).

### A. Reference = published English edition (baseline: DeepL)

Source: `results/1_wh_mateo-eval_2903-3178_ko-en.xlsx`, CIs and p-values in `results/2_wh_mateo-eval-ci_2903-3178_ko-en.xlsx`.

| System | COMET | BLEU | chrF2 | TER |
|---|---:|---:|---:|---:|
| DeepL (baseline) | 86.46 | 27.91 | 56.40 | 71.90 |
| Claude | 86.14 | 30.29 | 57.35 | 69.96 |
| DeepSeek | 86.10 | 29.08 | 56.79 | 70.92 |
| GPT-5 | 85.89 | 28.02 | 57.02 | 68.72 |
| Gemma 3 27B | 85.82 | 26.91 | 55.68 | 75.49 |
| gpt-oss 120B | 85.64 | 24.12 | 53.99 | 76.26 |
| Google | 85.59 | 29.30 | 55.71 | 71.18 |
| gpt-oss 20B | 85.42 | 23.01 | 53.66 | 78.52 |
| Llama 3.3 70B | 85.39 | 25.60 | 54.85 | 77.45 |
| Aya 23 35B | 85.14 | 26.59 | 54.99 | 75.59 |
| Qwen3 8B | 85.12 | 22.74 | 52.84 | 79.71 |
| ModernMT | 84.16 | 24.16 | 52.49 | 76.73 |
| Llama 3.1 8B | 83.51 | 21.51 | 51.18 | 83.29 |
| Qwen3 1.7B | 83.27 | 19.66 | 49.55 | 84.20 |
| Llama 3.2 1B | 72.06 | 9.93 | 37.38 | 101.36 |

### B. Reference = DeepL output (published English scored as "human")

Source: `results/3_wh_mateo-eval-chart_2903-3178_ko-en.xlsx`, CIs in the slide deck.

| System | COMET | BLEU | chrF2 | TER |
|---|---:|---:|---:|---:|
| **DeepSeek** | **91.28** | **58.38** | **76.58** | **34.36** |
| Claude | 90.79 | 54.89 | 74.46 | 37.02 |
| gpt-oss 120B | 90.37 | 47.80 | 71.30 | 43.90 |
| gpt-oss 20B | 90.31 | 47.19 | 71.24 | 44.98 |
| GPT-5 | 90.31 | 50.44 | 72.50 | 39.04 |
| Gemma 3 27B | 90.30 | 49.12 | 72.04 | 44.61 |
| Google | 90.24 | 52.88 | 72.38 | 39.70 |
| Llama 3.3 70B | 89.92 | 46.18 | 70.10 | 47.84 |
| Qwen3 8B | 89.87 | 45.55 | 70.03 | 47.13 |
| Aya 23 35B | 89.14 | 43.99 | 67.58 | 51.24 |
| ModernMT | 87.90 | 39.15 | 63.29 | 54.61 |
| Llama 3.1 8B | 87.62 | 37.50 | 63.96 | 58.56 |
| Qwen3 1.7B | 87.31 | 35.22 | 62.33 | 59.98 |
| Human (published English) | 84.50 | 27.97 | 52.94 | 69.33 |
| Llama 3.2 1B | 74.05 | 15.52 | 42.75 | 89.56 |

### Metric agreement (setting B, `results/5_wh_mateo-eval-corr_2903-3178_ko-en.xlsx`)

| Pair | Pearson r | Spearman ρ |
|---|---:|---:|
| COMET–BLEU | 0.92 | 0.94 |
| COMET–chrF2 | 0.95 | 0.95 |
| BLEU–chrF2 | 0.98 | 0.98 |

### Takeaways

- The three frontier LLMs (Claude, DeepSeek, GPT-5) are slightly ahead of DeepL on BLEU, chrF2 and TER against the human reference, while DeepL keeps a small COMET lead; all are well ahead of ModernMT.
- Among local models, quality scales with size: Gemma 3 27B, gpt-oss and Llama 3.3 70B land close to the commercial systems, while Llama 3.2 1B falls far behind (TER above 100).
- The four metrics rank systems very consistently (r = 0.92–0.98).

## Repository layout

```
scripts/
  txt_to_csv.py            # convert one-sentence-per-line TXT files to single-column CSV
  glossary_to_csv.py       # convert the comma-separated glossary to UTF-8 CSV for memoQ
  combine_corpora.py       # merge EN-KO TMX corpora into one translation memory (100k–500k TUs)
  metric_correlations.py   # Pearson/Spearman correlations and ranks across COMET/BLEU/chrF2/TER
results/
  1_..6_*.xlsx             # system-level MATEO scores, CIs, chart/plot sheets, correlations
  eval_A_published_reference.csv, eval_B_deepl_as_reference.csv
  mateo-runs/run_*/        # raw MATEO exports per batch (system-level scores + CIs)
  memoq-analysis/          # memoQ pre-translation analysis exports (UTF-16 CSV)
reports/                   # Part I and Part III reports (.docx)
slides/                    # final results deck (.pptx)
```

The source text, reference translations, per-system translation outputs, sentence-level score sheets, translation memories and memoQ project files are not included (third-party material).

## Reproducing

1. **Prepare data.** One sentence per line, aligned: `src.ko.txt` (Korean), `ref.en.txt` (English reference), and one `<system>.en.txt` per system, all with the same number of lines.
2. **Local LLM translations with [Ollama](https://ollama.com).** Pull a model and send the prompt above together with the source lines, e.g.
   ```bash
   ollama pull qwen3:8b-fp16
   { cat prompt.txt; echo; cat src.ko.txt; } | ollama run qwen3:8b-fp16 > qwen3_8b-fp16.en.txt
   ```
   Check that the output has exactly as many lines as the source; fix any merged or split lines before scoring.
3. **Score with MATEO.**
   ```bash
   git clone https://github.com/BramVanroy/mateo-demo.git && cd mateo-demo
   pip install -e .
   cd src/mateo_st && streamlit run 01_🎈_MATEO.py
   ```
   On the *Evaluate* page, upload the reference and up to four system files (the first one is the significance baseline), select COMET, BLEU, chrF2 and TER, and export the system-level and sentence-level results. Batches with different systems can be combined afterwards, as done in `results/`.
4. **Metric correlations.**
   ```bash
   pip install pandas scipy openpyxl
   cd results && python ../scripts/metric_correlations.py
   ```
   Reads `5_wh_mateo-eval-corr_2903-3178_ko-en.xlsx` (columns `system, comet, BLEU, chrF2, TER`), prints r/ρ and ranks, and writes a `Correlations` sheet.

## Author

William Holden
