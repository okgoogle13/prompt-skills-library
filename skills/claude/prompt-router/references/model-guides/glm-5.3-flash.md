---
model: glm-5.3-flash
vendor: Z.ai
family: GLM
aliases: [glm-flash, glm-5.3-flashx, glm53-flash, zai-glm-5.3-flash, zai-org/GLM-5.3-Flash]
last_verified: 2026-10-13
status: current
---

# GLM-5.3-Flash

## Reasoning / Thinking
- Type: **forced on**. GLM-5.3 and GLM-5.3-Flash "no longer support disabling thinking" — `thinking.type: "disabled"` produces an error; `"enabled"` is the only permitted value.
- Depth exclusively via `reasoning_effort`: `low` | `high` | `max` (default and recommendation). On the standard API endpoint any other value produces an error ("Any other input will result in an error"). On the coding-plan endpoint `none`/`minimal`/`low` are mapped to `low`, `medium`/`high` to `high`, and `xhigh`/`max` to `max`. In the open weights a missing or unknown value silently falls back to `max` ("defaults to max if not passed (or if set to any other value)").
- There is **no zero-thinking path**; `low` is the floor, not "off". Thinking consumes additional tokens — re-size the token budget against thinking-free workloads.
- Reasoning output: non-streaming as `reasoning_content` alongside `content`; in the stream as `delta.reasoning_content` before `delta.content`.
- `clear_thinking`: preserved thinking is off by default on the standard API endpoint and on by default on the coding-plan endpoint; in the open weights' chat template `clear_thinking` is set to `false`. The model page recommends `clear_thinking: false` (agent and coding runs), while the model card explicitly recommends `clear_thinking=true` for pure chat scenarios. With preserved thinking, return the historical `reasoning_content` completely and unchanged.

## Prompting style
- Z.ai shows Flash mainly in **visually closed loops**: produce result → render or execute → compare against a reference (screenshot, template, original app) → refine. The official example prompts (UI rebuilds from screenshots, Office decks, financial analysis, video editing, Blender scenes, Godot prototype, computer use, CAD) each spell out this check loop explicitly, sometimes with a minimum number of rounds ("build → fixed-camera render → inspect → refine → re-render").
- Specify verifiable deliverables and evidence obligations: name output formats concretely (e.g. PPTX + PDF, MP4 + SRT, STEP/STL) and have uncertainties listed as assumptions. The Office example literally demands "Do not fabricate any business data; cite the source for all referenced information."
- For UI work, first have the design system analysed from the reference images, then build, then compare the rendered pages against the reference.
- Agent prompts in the official four-block scheme: **Goal**, **Context** (files, error messages, examples), **Constraints** (engineering rules), **Done when** (acceptance criterion); "put temporary instructions in the prompt, and put long-lived rules in project-level configuration files"; for complex tasks plan first, then implement; one session per task.
- There is no Flash-specific prompt-engineering page; further style statements are unverified.

## Strengths & weaknesses (prompt-relevant)
- Strengths: first natively multimodal model of the GLM-5 series (video, image, text, file as input), according to Z.ai stronger than GLM-5.2 at very low cost; DeepSWE v1.1 63.4 (GLM-5.2: 46.2), AutomationBench 48.8 (26.2), Z.ai Code Bench v1.0 29.0 at max effort (Claude Opus 4.8: 29.5).
- Architecture per the model card: 320B parameters total, 18B active, hybrid sparse/linear attention, **newly trained base model** (not the 5.2/5.3 base model); per the model page, 3.01× less attention compute and a 4.44× smaller KV cache than GLM-5.3. Open weights under MIT licence.
- `glm-5.3-flashx` is the same model line at about 200 tokens/s, but more expensive and (still) not in the GLM Coding Plan; `glm-5.3-flash` is available in the Coding Plan with three times the quota of GLM-5.3.
- Weaknesses and quirks: narrow `reasoning_effort` enum without `medium`/`xhigh`; behavioural differences from glm-5.3 despite the same version number, because the base model is different — how large they are, no source says (unverified); no published knowledge cutoff (unverified).

## Output & format conventions
- 1M tokens context, `max_tokens` up to 128K; input video/image/text/file, output text. The open model card names only image + text.
- Multimodal content as content blocks in `messages[].content[]`: `image_url` (URL recommended, or Base64 data URL; multiple blocks possible), `video_url`, `file` (`file_url`/`file_id`/`file_data`). A `file` block may not be combined with `image_url`/`video_url` in the same request. Limits per API reference: images < 5 MB and ≤ 6000×6000 px (JPG/PNG/JPEG), videos ≤ 200 MB (MP4/MKV/MOV), files ≤ 50 MB, up to 50 file URLs.
- The vision request schema (models `glm-5.3-flashx` — default there — and `glm-5.3-flash`) knows only the roles `user`, `system`, `assistant`, with no `tool` role and no `tool_calls` on the assistant; `tools` only type `function` (max. 128), `tool_choice` only `"auto"`; `stop` per description currently only one stop word.
- Contradiction in the docs: the model page lists structured output (JSON) and recommends `stream: true` plus `tool_stream: true`, but the vision schema in the API reference contains neither `response_format` nor `tool_stream` — whether both take effect for Flash is unverified. How tool results are returned without a `tool` role is likewise unverified.
- Recommended parameters per the model page: `temperature` 1, `top_p` 0.95, `reasoning_effort: max`.
- Prices per MTok: Flash $0.15 input / $0.03 cached input / $0.50 output; FlashX $0.37 / $0.075 / $1.25; cached-input storage free for a limited time (as of 2026-10-13). Release-notes entry: 2026-08-26.

## Migration notes
- **TO glm-5.3-flash**: remove `thinking.type: "disabled"` (error) and switch non-thinking paths to `enabled` + `reasoning_effort: low`; use only `low`/`high`/`max` — never carry over `none`/`minimal` as "off", because they fail on the standard API and silently run as `max` when self-hosted. Set `model` explicitly to `glm-5.3-flash` or `glm-5.3-flashx` (a price and speed decision; FlashX is not in the Coding Plan). Pass images, videos and documents as `image_url`/`video_url`/`file` blocks, and split file and image/video blocks across separate requests. JSON mode (`response_format`) is not documented in the API schema for this model — move format requirements into the prompt contract and validate the result. Reduce multiple stop sequences to one and remove `tool_choice` values other than `auto`. Add an explicit render-and-compare loop to visual tasks.
- **From glm-5.3 / glm-5.2**: same thinking contract as glm-5.3; still re-evaluate prompts, since Flash is built on a newly trained base model (glm-5.3, by contrast, uses the GLM-5.2 base model).
- **FROM glm-5.3-flash**: image, video and file inputs need a multimodal target — glm-5.3 and glm-5.2 are text-only. Target models without forced thinking need an explicit thinking setup; remove Z.ai-specific fields (`clear_thinking`, `tool_stream`, `reasoning_content` handling) or map them to the target's conventions; keep the render-and-compare loop in the prompt if the target can check visually, otherwise replace it with textual test criteria; check 1M-context and 128K-output assumptions against the target window.

## Sources
- https://docs.z.ai/guides/vlm/glm-5.3-flash — model IDs `glm-5.3-flash`/`glm-5.3-flashx`, "the first native multimodal model in the GLM-5 series", 1M context, 128K output, input video/image/text/file, capability list incl. structured output, FlashX about 200 tokens/s and not in the Coding Plan, Coding Plan quota 3× GLM-5.3, recommended parameters (`temperature` 1, `top_p` 0.95, `reasoning_effort: max`, `clear_thinking: false`, `stream` + `tool_stream`), `image_url` blocks with URL or Base64, the eight best-practice examples incl. "Do not fabricate any business data; cite the source for all referenced information", DeepSWE/AutomationBench/Z.ai Code Bench figures, 3.01×/4.44× versus GLM-5.3.
- https://docs.z.ai/guides/capabilities/thinking — forced thinking for GLM-5.3/5.3-FLASH ("no longer support disabling thinking"), `reasoning_effort` `max`/`high`/`low` with "Any other input will result in an error", coding-plan mapping, `reasoning_content` non-streaming and in the stream.
- https://docs.z.ai/guides/capabilities/thinking-mode — preserved thinking: off by default on the standard API endpoint, on at the coding-plan endpoint, mandatory unchanged return of `reasoning_content`.
- https://docs.z.ai/api-reference/llm/chat-completion — vision request schema: model enum `glm-5.3-flashx` (default) / `glm-5.3-flash`, roles without `tool`, content blocks `text`/`image_url`/`video_url`/`file`, file/image combination ban, size limits, `max_tokens` up to 128K, `tools` only `function`, `tool_choice` only `auto`, `stop` with "Currently, only one stop word is supported", no `response_format`/`tool_stream`.
- https://docs.z.ai/guides/overview/pricing — GLM-5.3-Flash $0.15/$0.03/$0.50, GLM-5.3-FlashX $0.37/$0.075/$1.25, cached-input storage "Limited-time Free".
- https://docs.z.ai/release-notes/new-released — 2026-08-26 GLM-5.3-Flash, native visual capabilities ("observe interfaces, rendering results, and interaction feedback").
- https://huggingface.co/zai-org/GLM-5.3-Flash — official model card: MIT licence, 320B/18B active, hybrid sparse/linear attention, "starts from a newly trained base model", image + text, `reasoning_effort` low/high/max with fallback to `max`, `clear_thinking` default `false` in the chat template and chat recommendation `clear_thinking=true`.
- https://docs.z.ai/devpack/resources/best-practice — Goal/Context/Constraints/Done when, three context layers, rule on temporary vs. long-lived instructions, plan before implementation, session hygiene (formulated model-independently).
