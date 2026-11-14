# Manual tests (not covered by the single-turn harness)

## M1 — Prompt supplied in a follow-up turn (extends eval #11)

1. Send: `Optimise a prompt for Sonnet 5.5`
2. Confirm the router names `claude-sonnet-5-5`, asks once for the prompt, and reads no guide.
3. Send the prompt alone in the next message, e.g.
   `Summarise {{ticket}} in three bullets for the on-call engineer.`
4. Pass if: it completes the optimise route without re-asking for the model, reads only
   `migrate-prompt/model-guides/claude-sonnet-5-5.md`, and keeps `{{ticket}}`.

## M2 — Registry entry whose guide file is missing (extends eval #12)

Eval #12 covers a name absent from the registry. A registry row with no file cannot be tested
without changing `migrate-prompt/`, which is out of bounds.

- Use a sandboxed copy only if a safe method becomes available (e.g. a throwaway copy of both
  skills in a temp HOME). Never rename or move files in the live `migrate-prompt/`.
- Otherwise verify by reading the router: when the Read of `<guides>/<id>.md` fails, it must
  list the closest valid ids and stop, with no plugin-cache or memory fallback.
