# Research Reading Notes
# Kaggle Agentic Workflow Sources

Generated: 2026-11-07
Order: s6e11_756276 → s6e3_686686 → s6e8_738592 → s6e5_703615 → s6e9_745013 → kgmon_playbook
Coverage record: .omg/drafts/coverage_record.json (all 6 sources: complete=True)

---

## Source 1: s6e11_756276.md
**File:** research/sources/s6e11_756276.md  
**Command:** `kaggle competitions topic-messages playground-series-s6e11 756276 -v`  
**Comment Count (recorded):** 5 | **Comment Count (computed from file):** 5 ✓  
**OmA Coverage:** 2 windows, complete=True, 4,930 bytes  
**Status:** READ

### What the author DID

1. Open-sourced previous 6 Kaggle Playground competition solutions (S6E3–S6E10), giving agents 500 models of source code to train on.  
   [QUOTED] source: s6e11_756276.md "code was written by agents with me guiding them" (L24, 9 words)

2. Framed the shared code as training material for other agents on future tabular competitions.  
   [PARAPHRASED] L24–L25: author stated the release gives agents source code to train on for current and future competitions.

### Claims made without evidence

1. Commenter (L44) claims solo model-by-model builders will increasingly be squeezed out:  
   [QUOTED] source: s6e11_756276.md "there will be less and less room for those of us who still build and test models one by one." (L44, 22 words)  
   *(This is a commenter prediction, not a measured result.)*

---

## Source 2: s6e3_686686.md
**File:** research/sources/s6e3_686686.md  
**Command:** `kaggle competitions topic-messages playground-series-s6e3 686686 -v`  
**Comment Count (recorded):** 101 | **Comment Count (computed from file):** 101 ✓  
**OmA Coverage:** 20 windows, complete=True, 79,090 bytes  
**Status:** READ

### What the author DID

1. Used GPT5.4, Gemini3.1, and ClaudeOpus4.6 to write all solution code; agents were instructed to follow the KGMON Playbook.  
   [QUOTED] source: s6e3_686686.md "All of this solution's code was written by GPT5.4, Gemini3.1, ClaudeOpus4.6" (L20, 13 words)

2. Agents wrote 600,000 lines of code in one month, built 850 models on 4xA100 GPUs, and ran 50 EDA scripts.  
   [QUOTED] source: s6e3_686686.md "They built and trained 850 models on 4xA100 GPU and wrote and ran 50 EDA scripts!" (L22, 16 words)

3. Prompted agents to perform their own EDA and use findings to generate new feature engineering ideas.  
   [QUOTED] source: s6e3_686686.md "GPT5.4, Gemini3.1, ClaudeOpus4.6 were prompted to perform their own EDA to determine the relationship" (L30, 14 words)

### Claims made without evidence

1. Author describes the agent output as "unbelievable" (L22) without providing comparative baselines against human-only runs.

---

## Source 3: s6e8_738592.md
**File:** research/sources/s6e8_738592.md  
**Command:** `kaggle competitions topic-messages playground-series-s6e8 738592 -v`  
**Comment Count (recorded):** 78 | **Comment Count (computed from file):** 78 ✓  
**OmA Coverage:** 13 windows, complete=True, 51,107 bytes  
**Status:** READ

### What the author DID

1. Phase 1: deployed a single Codex GPT 5.6 Sol autorun agent that read the competition, downloaded data, built a 380-model ensemble, and auto-submitted to the leaderboard over 4 days without human intervention. (L20, [PARAPHRASED])

2. Phase 2: introduced Fable 5 and a second GPT 5.6 Sol; challenged them to compete head-to-head on single NN and XGB model quality.  
   [QUOTED] source: s6e8_738592.md "challenged Codex GPT 5.6 Sol to compete against Claude Code Fable 5 to see who can make the best single NN model" (L24, 22 words)

3. Phase 3: asked Fable to build a `tar.gz` packet and prompt, manually uploaded to ChatGPT Pro in parallel, downloaded its ZIP discoveries, and fed them back to the coding agents. (L32, [PARAPHRASED])

4. Ran agents independently first without giving them prior knowledge, then progressively added clues, then full public knowledge.  
   [QUOTED] source: s6e8_738592.md "In the same way that the best human Kaggle team is where humans work independently first, i do this with my agents." (L232, 22 words)

5. After every 4–12 hour campaign, instructed agents to write down all their new discoveries into discovery.md files.  
   [QUOTED] source: s6e8_738592.md "After every 4-12 hour campaign, I had them write down all their new discoveries." (L450, 14 words)

6. Used 1M+ token context, never forced context compact, so agents could re-read all discovery files and avoid repeating experiments. (L452, [PARAPHRASED])

7. Used max thinking mode for breakthroughs and important EDA/feature engineering work; reduced thinking for routine coding. (L452, [PARAPHRASED])

### Independent discovery notes and exchange of findings: FOUND

**FOUND — independent-first approach (Msg 20, L232):**  
> [QUOTED] source: s6e8_738592.md "In the same way that the best human Kaggle team is where humans work independently first, i do this with my agents." (L232, 22 words)

**FOUND — exchange of findings between agents (Msg 45, L442 and L450):**  
In a comment thread (Msg 45), a commenter noted complementary strengths between Fable and Codex. Deotte confirmed:  
> [QUOTED] source: s6e8_738592.md "around Aug 28th, I shared lots of Fable's secrets with GPT which allowed GPT to use them" (L442, 17 words)  
> [QUOTED] source: s6e8_738592.md "After every 4-12 hour campaign, I had them write down all their new discoveries." (L450, 14 words)

### Claims made without evidence

1. L28: "confirms that frontier models are Grandmasters at data science modeling" — a single competition win is cited as confirmation; no controlled comparison is provided.

---

## Source 4: s6e5_703615.md
**File:** research/sources/s6e5_703615.md  
**Command:** `kaggle competitions topic-messages playground-series-s6e5 703615 -v`  
**Comment Count (recorded):** 26 | **Comment Count (computed from file):** 26 ✓  
**OmA Coverage:** 7 windows, complete=True, 24,619 bytes  
**Status:** READ

### What the author DID

1. Instructed Codex GPT5.5 to maintain a `local_leaderboard.md` file tracking the top 10 CV score models at all times.  
   [QUOTED] source: s6e5_703615.md "I asked Codex to maintain a `local_leaderboard.md` file with the top 10 CV score models." (L26, 15 words)

2. Let Codex run autonomously with 4x A100 GPUs in parallel, running experiments continuously until told to stop.  
   [PARAPHRASED] L26: author set a stop condition and let the agent run GPU experiments in parallel without further intervention.

3. Codex wrote experiments, ran code on GPU, logged results in the local leaderboard, analyzed results, and decided on further experiments — all autonomously.  
   [QUOTED] source: s6e5_703615.md "Codex wrote experiments, Codex ran the code on GPU, Codex logged the results (in local leaderboard), Codex analyzed the results" (L30, 20 words)

### Claims made without evidence

1. L24: "Its ability to plan and do data science is mind blowing!" — subjective assessment without comparative metric.

---

## Source 5: s6e9_745013.md
**File:** research/sources/s6e9_745013.md  
**Command:** `kaggle competitions topic-messages playground-series-s6e9 745013 -v`  
**Comment Count (recorded):** 26 | **Comment Count (computed from file):** 26 ✓  
**OmA Coverage:** 8 windows, complete=True, 29,551 bytes  
**Status:** READ

### What the author DID

1. Passed one codebase sequentially between three generations of AI agents (GPT-5.6 Sol + Fable 5, then GPT-6-Astra + Fable 5.1, then Opus 5.5), with two-week rest in between.  
   [QUOTED] source: s6e9_745013.md "We passed one codebase between three generations of AI agents, like the baton in a relay race:" (L18, 17 words)

2. Used code and markdown notes as the "baton" — agents inherited over 1 million lines of code from prior competitions plus 600 markdown note files.  
   [QUOTED] source: s6e9_745013.md "The baton was **our code and our notes**" (L48, 7 words including markup; literal text in file)

3. Each new agent leg built on the previous leg's CV score; the human coach set goals, chose final submissions, and passed the baton. (L48 section, [PARAPHRASED])

4. Fable 5.1 wrote a public EDA notebook that found the original data's purchase recipe; human uploaded it publicly. (L in team section, [PARAPHRASED])

### Claims made without evidence

1. "the last steps near the top of the mountain are the steepest" (mountain metaphor section) — used to explain diminishing CV gains across legs; not independently measured, but consistent with the numerical table shown.

---

## Source 6: kgmon_playbook.md
**File:** research/sources/kgmon_playbook.md  
**Command:** HTTP GET https://raw.githubusercontent.com/cdeotte/KGMON-Playbook-2026/main/README.md  
**Comment Count:** N/A (GitHub repository)  
**OmA Coverage:** 1 window, complete=True, 1,317 bytes  
**Status:** READ

### What the author DID

1. Structured the KGMON Playbook 2026 as a sequence of 7 notebooks covering EDA → Feature Engineering → Baselines → Stacking → Hill Climbing → Pseudo Label → Conclusion.  
   [QUOTED] source: kgmon_playbook.md "`07_Conclusion.ipynb`: Experiments Experiments Experiments!" (L38, 4 words excluding filename)

2. Published all playbook notebooks publicly on GitHub with explicit step ordering (01 through 07). (L32–L38, [PARAPHRASED])

### Claims made without evidence

1. README implies the playbook is a universal best practice for tabular data competitions; no ablation study comparing the playbook steps against alternatives is included in the README.
