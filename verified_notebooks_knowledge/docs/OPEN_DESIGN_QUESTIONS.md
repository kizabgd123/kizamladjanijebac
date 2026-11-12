# OPEN DESIGN QUESTIONS & UNVERIFIED SPECIFICATIONS

**Project:** HALO RAG STUDIO  
**Status:** ACTIVE AUDIT  

---

## 1. MRMMIA Defense: Privacy Mechanism Gap
- **Reference in brainstorm plan:** "MRMMIA Defense: Multi-Recall Memory Membership Inference Attack protection against adversarial memory extraction... DP Privacy Budget epsilon=0.5".
- **Current Technical Finding:** The brainstorm plan asserts $\epsilon=0.5$ differential privacy noise injected into agent memory. However, no authoritative mathematical formulation, noise distribution (Laplace / Gaussian), or formal privacy accounting mechanism is defined in the source materials.
- **Classification:** `UNVERIFIED / DESIGN GAP`
- **Mitigation & Policy:**
  - Do NOT claim formal mathematical Differential Privacy until a proven accountant (e.g. Google DP or Opacus) is integrated.
  - Implement memory access redaction, token masking, and explicit metadata scrubbing as the empirical privacy barrier.
  - Re-evaluate when formal DP bounds are mathematically specified.

---

## 2. EvalSafetyGap: 3-Layer Safety Metric Standard
- **Reference in brainstorm plan:** "EvalSafetyGap: Layered evaluation reporting separating Capabilities/Performance, Behavioral Robustness, and Compliance."
- **Current Technical Finding:** While the 3 layers provide clear categorical taxonomy, exact automated scoring formulas for the "Behavioral Robustness" and "Compliance" layers are non-standard across off-the-shelf RAGAS classes.
- **Classification:** `PARTIALLY SPECIFIED / DOMAIN ADAPTATION REQUIRED`
- **Mitigation & Policy:**
  - Layer 1 (Capabilities/Performance): Standard RAGAS (Context Relevance, Faithfulness, Answer Relevance).
  - Layer 2 (Behavioral Robustness): Tested via adversarial noise injection and contradictory chunk permutation (Noise Sensitivity).
  - Layer 3 (Compliance): Tested via AST sandbox violation detection, citation completeness checks, and refusal of out-of-corpus queries.
