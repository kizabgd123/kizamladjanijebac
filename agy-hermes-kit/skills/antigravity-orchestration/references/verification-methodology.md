# Antigravity 2.0 Verification Methodology

## Test Coverage (28 tests)

### Config Validation (6 tests)
- 5 agents with unique IDs
- Required fields present (agent_id, role, target_directories, primary_model, enforced_rules, status)
- Field types and non-empty scope
- Statuses valid (idle/running/error)
- Scopes are relative and stay inside repo (no absolute paths, no '..')
- Notebook ID is valid UUID (in memory-agent enforced_rules)

### Scope Collision Detection (9 tests)
- Happy path: real pool has 7 unique dirs, 0 collisions
- Exact duplicate raises ScopeCollisionError
- Trailing slash and whitespace normalised (os.path.normpath)
- Collision on second directory of multi-scope agent
- All collisions reported at once
- Real pool with injected collision raises
- Parent/child overlap detected (tests vs tests/unit)
- Dot-slash spelling detected (./tests vs tests)
- tests vs tests_old do NOT collide (component-based, not string prefix)

### Directory Existence (3 tests)
- All present → True, no output
- Missing dir reports agent_id and path
- Multiple missing all listed

### Main Exit Codes (6 tests)
- Pass exits 0
- Collision exits 1, no PASSED in output
- Missing dir exits 1, no PASSED in output
- Collision checked before filesystem (ordering)
- Malformed config raises JSONDecodeError
- Missing target_directories key raises KeyError

### Agent Pool Status (4 tests)
- Lists all 5 agents, exit 0
- Status icons: idle→🟢, running→🟡, error→🔴

## check_collisions() Implementation Notes

- Uses os.path.normpath for path normalization
- Uses component-based prefix matching (split on os.sep)
- "tests" and "tests/unit" collide (parent/child)
- "tests" and "./tests" collide (same after normpath)
- "tests" and "tests_old" do NOT collide (different components)
- "tests/" and "  tests" collide (after strip + normpath)

## Model Availability Findings (tested via google.genai, GEMINI_API_KEY)

| Config Model | Provider path | In catalog? | Minimal call | Error |
|---|---|---|---|---|
| gemini-3.5-flash | google.genai | yes | SUCCESS (OK) | — |
| gemma-4-31b-it | google.genai | yes | SUCCESS (OK) | — |
| gemini-3.8-flash | google.genai | yes | FAIL | RemoteProtocolError (server disconnected); retry hangs |

Note: existence in the catalog is not enough — gemini-3.8-flash is listed but not callable. Provider differs from earlier notes (gemini CLI / ollama); the actual working path here is google.genai with GEMINI_API_KEY.

## Scope Enforcement Gap

No runtime enforcement exists. check_collisions() is pre-dispatch only.
An agent can write to any file regardless of its declared scope.
To enforce: add file path validation in agent execution code.
