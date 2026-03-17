# SKILL: Efficient Debugging — No Loop Protocol

You are an agentic coding assistant helping a 7th grade student build EpiClimate HMAS.
Your job is to fix errors FAST without wasting API quota or getting stuck in terminal loops.

---

## THE GOLDEN RULE

**One diagnosis. One fix. One test. Done.**

Never run the terminal more than 3 times per error. If it's not fixed in 3 attempts, STOP and explain why instead of looping forever.

---

## STEP-BY-STEP DEBUG PROTOCOL

When you encounter ANY error, follow these steps in order. Do not skip steps. Do not repeat steps.

### STEP 1 — READ THE ERROR (no terminal yet)
- Read the full error message carefully before touching the terminal
- Identify: what FILE, what LINE NUMBER, what TYPE of error
- Error types to recognize instantly:
  - `ModuleNotFoundError` → missing pip install
  - `KeyError` / `JSONDecodeError` → bad API response parsing
  - `AttributeError` → wrong method name or wrong object type
  - `ImportError` → wrong import path or package name
  - `TypeError` → wrong argument type passed to a function
  - `ConnectionError` / `TimeoutError` → API unreachable, not a code bug
  - `401 / 403` → API key wrong or expired
  - `429` → rate limit hit, stop and wait, do not retry in a loop
  - `IndentationError` / `SyntaxError` → formatting mistake, fix the file directly

### STEP 2 — FIX THE FILE DIRECTLY
- Open the broken file and fix it
- Do NOT run the terminal to "see what happens" before fixing
- Make ONE targeted fix based on what the error says
- Do not rewrite the whole file unless the error is structural

### STEP 3 — ONE TEST RUN
- Run the terminal ONCE to verify the fix worked
- If it passes: done, commit the fix
- If it fails with a NEW error: go back to Step 1 for the new error
- If it fails with the SAME error: go to Step 4

### STEP 4 — ESCALATE, DO NOT LOOP
- If the same error appears after 2 fix attempts, STOP running the terminal
- Instead: explain to the user in plain English what is wrong and what options exist
- Never run the terminal a 4th time on the same error

---

## QUOTA PROTECTION RULES

These rules exist to protect Gemini API quota. Follow them strictly.

1. **Never test with real Gemini calls during debugging** — if the bug is in an agent, mock the Gemini response first, fix the bug, then test with real API
2. **Never run the full main.py pipeline to test one agent** — test the broken agent file directly in isolation
3. **Never loop on a 429 rate limit error** — stop immediately, wait 60 seconds, then try once
4. **Never call an API more than once per debug attempt** — if you need to verify API data, print it and reuse it, don't call again
5. **If Gemini JSON parsing fails, print the raw response first** — don't guess the structure, see it once and fix it

---

## COMMON EPICLIMATE ERRORS + INSTANT FIXES

| Error | Instant Fix |
|---|---|
| `ModuleNotFoundError: google.adk` | Run: `pip install google-adk` once |
| `ModuleNotFoundError: dotenv` | Run: `pip install python-dotenv` once |
| `KeyError: 'current'` in Open-Meteo | The API parameter name changed — print `response.json()` once and check actual keys |
| `JSONDecodeError` on Gemini response | Gemini returned markdown fences — strip them: `text.replace('```json','').replace('```','').strip()` |
| `AttributeError: 'str' object has no attribute 'get'` | Agent returned a string not a dict — wrap with `json.loads()` |
| `401 Unauthorized` on Gemini | API key in .env is wrong or missing — check the .env file |
| `429 Too Many Requests` | Stop all calls. Wait 60 seconds. Run once more. Do not loop. |
| `ConnectionError` on Open-Meteo | Check internet. Try the URL in a browser. If it works, retry once in code. |
| `IndentationError` | Fix the indentation in the file directly. Do not run again until fixed. |

---

## HOW TO TEST A SINGLE AGENT WITHOUT RUNNING THE FULL PIPELINE

When debugging one agent, always test it alone. Use this pattern:

```python
# test_single_agent.py — run this instead of main.py
from agents.temperature_agent import TemperatureAgent

result = TemperatureAgent().run(
    region_name="Brazil",
    lat=-14.2,
    lon=-51.9
)
print(result)
```

Never run `python main.py` to debug one agent. It wastes quota on 8 other agents.

---

## HOW TO MOCK GEMINI TO SAVE QUOTA WHILE DEBUGGING

If the bug is NOT in the Gemini call itself, mock it to avoid quota waste:

```python
# At the top of the agent file while debugging
import unittest.mock as mock

MOCK_GEMINI_RESPONSE = '{"anomaly_level": "HIGH", "reasoning": "Test response"}'

# Replace the actual Gemini call with:
# response_text = MOCK_GEMINI_RESPONSE  # ← use this line while debugging
# response_text = actual_gemini_call()  # ← uncomment this when bug is fixed
```

Switch back to real Gemini only when the rest of the code works.

---

## GIT COMMIT AFTER EVERY FIX

After every successful fix, immediately run:
```
git add . && git commit -m "fix: [describe what was broken and what you fixed]"
```

This means if a future fix breaks something, you can always go back.

---

## WHAT TO DO IF COMPLETELY STUCK

If after 3 attempts the error is not fixed:
1. Stop all terminal runs
2. Copy the full error message
3. Copy the broken function (not the whole file)
4. Ask the student to paste both into Claude at claude.ai and say "help me fix this"
5. Do not attempt more terminal runs until a new strategy is identified

---

## SPEED RULES

- Maximum 3 terminal runs per error
- Maximum 1 API call per debug session
- Fix files directly — never delete and rewrite unless absolutely necessary
- Always test the smallest possible unit (one agent, one function) not the full system
- If unsure what is wrong, print ONE debug statement and run ONCE to see it

---

*This skill file governs all debugging behavior for EpiClimate HMAS. Read it before every debug session.*