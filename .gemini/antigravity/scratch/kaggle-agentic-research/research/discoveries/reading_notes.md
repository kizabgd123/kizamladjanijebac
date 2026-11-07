# Reading Notes: Agentic Research Workflows on Kaggle (2026)

This document collects documented, concrete practices adopted by top competitive data scientists using agentic research workflows on Kaggle in 2026.

---

## Source: `s6e11_756276.md`
- **Location:** Kaggle Playground Series s6e11 Discussion, Topic #756276 ("Sharing Code for 500 Models!")
- **Author:** Chris Deotte
- **Status:** READ

### Practice 1: Human-Guided Agent Code Generation
- **Practice:** The author guided LLM agents to write all solution code across six consecutive competitions rather than writing models manually.
- **Quote:** [QUOTED] source: s6e11_756276.md "All of these solutions' code was written by agents with me guiding them."
- **Location:** Opening post, paragraph 2.

### Practice 2: Open-Sourcing Agent Training Repositories
- **Practice:** The author shared 500 complete model source scripts to serve as training corpora and few-shot bases for future data science agents.
- **Quote:** [QUOTED] source: s6e11_756276.md "This shared code gives everyone's agents 500 models of source code to train their agents for current and future tabular data competitions!"
- **Location:** Opening post, paragraph 2.

---

## Source: `s6e9_745013.md`
- **Location:** Kaggle Playground Series s6e9 Discussion, Topic #745013 ("1st Place - The AI Relay!")
- **Author:** Chris Deotte
- **Status:** READ

### Practice 1: Multi-Generational Agent Relay
- **Practice:** The author operated a 3-stage relay where successive generations of frontier models iteratively improved upon the previous agent's codebase.
- **Quote:** [QUOTED] source: s6e9_745013.md "We passed one codebase between three generations of AI agents, like the baton in a relay race:"
- **Location:** Opening post, section "1st Place - The AI Relay", paragraph 2.

### Practice 2: Persistent Notes as State Transfer
- **Practice:** To overcome session context wiping between agent runs, the author used shared code files and written markdown notes as the state-handoff mechanism.
- **Quote:** [QUOTED] source: s6e9_745013.md "The baton was our code and our notes."
- **Location:** Opening post, section "The Baton Is The Notes", paragraph 1.

### Practice 3: Human Role Evolution to Referee
- **Practice:** The human practitioner stopped micromanaging agent execution and acted as a referee evaluating handoffs and making final submission calls.
- **Paraphrase:** [PARAPHRASED] The author shifted from direct coder to manager, then coach, and ultimately referee as inter-agent handoffs matured.
- **Location:** Opening post, section "The Relay Race", paragraph 1.

---

## Source: `s6e8_738592.md`
- **Location:** Kaggle Playground Series s6e8 Discussion, Topic #738592 ("1st Place - Distributed Intelligence - NVIDIA Inference Hub")
- **Author:** Chris Deotte
- **Status:** READ

### Practice 1: Competitive Agent Pairing
- **Practice:** The author paired two different frontier agents against each other to independently build single NN and XGB models.
- **Quote:** [QUOTED] source: s6e8_738592.md "We then challenged Codex GPT 5.6 Sol to compete against Claude Code Fable 5 to see who can make the best single NN model"
- **Location:** Opening post, section "Phase 2 - GPT 5.6 Sol battles Fable 5", paragraph 1.

### Practice 2: Dynamic Cross-Pollination of Tips
- **Practice:** When one competing agent stalled, the author transferred techniques and tips discovered by the leading agent to the trailing agent.
- **Quote:** [QUOTED] source: s6e8_738592.md "When one was lagging, we would share tips from the leading agent to the trailing agent and soon the trailing agent would take the lead!"
- **Location:** Opening post, section "Phase 2 - GPT 5.6 Sol battles Fable 5", paragraph 1.

### Practice 3: Background Batch Reasoning via Archive Uploads
- **Practice:** The author had an agent prepare tar.gz bundles and structured prompts for long-running deep reasoning instances to discover non-obvious feature transformations.
- **Paraphrase:** [PARAPHRASED] Bundled tar.gz code and prompt packages were uploaded for multi-hour background reasoning runs to uncover new feature engineering patterns.
- **Location:** Opening post, section "Phase 3 - ChatGPT Pro - Swarm Intelligence!", paragraph 1.

---

## Source: `s6e5_703615.md`
- **Location:** Kaggle Playground Series s6e5 Discussion, Topic #703615 ("2nd Place - Autonomous Codex Yolo!")
- **Author:** Chris Deotte
- **Status:** READ

### Practice 1: Autonomous Multi-Hour Experiment Loops
- **Practice:** The author ran autonomous CLI agent loops across multiple A100 GPUs without human micro-management.
- **Quote:** [QUOTED] source: s6e5_703615.md "Codex wrote experiments, Codex ran the code on GPU, Codex logged the results (in local leaderboard), Codex analyzed the results"
- **Location:** Opening post, section "Codex Runs Experiments", paragraph 2.

### Practice 2: Local Markdown Leaderboard as Source of Truth
- **Practice:** The agent maintained a versioned markdown file tracking top-10 cross-validation models to guide subsequent experiments.
- **Quote:** [QUOTED] source: s6e5_703615.md "I asked Codex to maintain a local_leaderboard.md file with the top 10 CV score models."
- **Location:** Opening post, section "Codex Runs Experiments", paragraph 1.

---

## Source: `s6e3_686686.md`
- **Location:** Kaggle Playground Series s6e3 Discussion, Topic #686686 ("1st Place - GPT5.4, Gemini3.1, ClaudeOpus4.6 - KGMON Playbook!")
- **Author:** Chris Deotte
- **Status:** READ

### Practice 1: Hardware-Accelerated Multi-Agent Implementation
- **Practice:** Multiple LLMs authored 600,000 lines of code accelerated by GPU computing and RAPIDS libraries.
- **Quote:** [QUOTED] source: s6e3_686686.md "All of this solution's code was written by GPT5.4, Gemini3.1, ClaudeOpus4.6 and experimentation was accelerated with GPU"
- **Location:** Opening post, section "GPT5.4, Gemini3.1, ClaudeOpus4.6 and 4xA100 GPUs!", paragraph 1.

### Practice 2: Methodological Playbook Grounding
- **Practice:** Agents were constrained to follow a strict sequential engineering playbook rather than improvising pipelines.
- **Quote:** [QUOTED] source: s6e3_686686.md "These agents learned to understand and follow the KGMON Playbook for tabular data and finish 1st place!"
- **Location:** Opening post, section "GPT5.4, Gemini3.1, ClaudeOpus4.6 and 4xA100 GPUs!", paragraph 1.

---

## Source: `kgmon_playbook.md`
- **Location:** Public GitHub Repository `cdeotte/KGMON-Playbook-2026`
- **Author:** Chris Deotte et al. (NVIDIA Kaggle Grandmasters Team)
- **Status:** READ

### Practice 1: Sequential 7-Stage Tabular Methodology
- **Practice:** The workflow enforces seven explicit, ordered pipeline phases from exploratory data analysis to pseudo-labeling.
- **Paraphrase:** [PARAPHRASED] The playbook prescribes seven strictly ordered notebook milestones: EDA, Feature Engineering, Baselines, Stacking, Hill Climbing, Pseudo Labeling, and Conclusion.
- **Location:** Repository root notebooks 01 through 07.

---

## Source: `s6e4_irrigation_need` (Topic #701104)
- **Location:** Kaggle Playground Series s6e4
- **Status:** [NOT READ]
- **Reason:** Outside core scope focus; priority was given to the requested S6E11, S6E9, S6E8, S6E5, and S6E3 writeups and Playbook repo.
