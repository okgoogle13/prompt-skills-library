# Context pack fixture

## Task
Prepare a concise account-status summary for an internal operations team. Return only JSON inside the `<result>` tags with keys `status` and `rationale`. Keep the account identifier exactly as supplied: `{{account_id}}`.

## Unique requirements
- Include the account's current operational status.
- Explain the reason for that status using the supplied evidence only.
- Preserve uncertainty when the evidence does not establish a definitive cause.
- Do not infer missing dates, owners or actions.

## Repeated instructions (intentional duplication for this test)
- Be accurate and do not invent facts.
- Use only the supplied evidence.
- Be accurate; do not make anything up.
- Do not invent facts; rely only on the supplied evidence.
- Return valid JSON inside `<result>` tags.
- The output must be JSON and must use `<result>` tags.

## Source A — 2026-10-02
The account is marked `active`. The latest operations note says service was restored, but it does not identify the root cause.

## Source B — 2026-09-14
An older support note says the account was `suspended` pending verification. It does not confirm whether verification was completed.

## Irrelevant history
The team previously discussed office catering, a planned social event, preferred meeting-room layouts, and an unrelated laptop purchase. None of those topics concerns this account.

## Output contract
Return exactly:
<result>
{"status":"...","rationale":"..."}
</result>
