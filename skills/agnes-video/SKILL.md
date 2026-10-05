---
name: agnes-video
description: Use when the user wants to generate videos via the Agnes Video API. Covers text-to-video, image-to-video, keyframe animation, motion assets. Requires AGNES_API_KEY.
user-invocable: true
---

# Agnes Video API

> **Prerequisite:** `AGNES_API_KEY` must be set in your shell environment. If unset, export it before proceeding: `export AGNES_API_KEY="your-key"`.

Third-party asynchronous video generation API (Sapiens AI). Three models:

| Model                   | ID                      | Best for                                                              |
| ----------------------- | ----------------------- | --------------------------------------------------------------------- |
| **2.5 Flash** (default) | `agnes-video-2.5-flash` | Currently free under promotion, same billing formula as 2.5           |
| **2.5**                 | `agnes-video-2.5`       | Latest quality tier, paid ($0.025-$0.055/sec depending on resolution) |
| **v2.0**                | `agnes-video-v2.0`      | Legacy model                                                          |

Use 2.5 Flash (free) unless the user explicitly requests 2.5 or v2.0.

## Endpoints

| Purpose                  | Method | URL                                                  |
| ------------------------ | ------ | ---------------------------------------------------- |
| Create task              | POST   | `https://apihub.agnes-ai.com/v1/videos`              |
| Get result (recommended) | GET    | `https://apihub.agnes-ai.com/agnesapi?video_id=<ID>` |
| Get result (legacy)      | GET    | `https://apihub.agnes-ai.com/v1/videos/<TASK_ID>`    |

Append `&model_name=<MODEL_ID>` to the recommended endpoint when using an upstream video ID or explicitly specifying the model.

## Parameters

| Parameter          | Type     | Required | Notes                                                                       |
| ------------------ | -------- | -------- | --------------------------------------------------------------------------- |
| `model`            | string   | Yes      | `agnes-video-2.5-flash` (default), `agnes-video-2.5`, or `agnes-video-v2.0` |
| `prompt`           | string   | Yes      | Text description of video content                                           |
| `image`            | string   | No       | Public HTTPS URL for image-to-video                                         |
| `mode`             | string   | Yes      | `ti2vid` (text/image-to-video) or `keyframes`                               |
| `size`             | string   | No       | `720P`, `1080P`, `1K`, or `2K` (default: `720P`)                            |
| `aspect_ratio`     | string   | No       | `16:9`, `9:16`, `1:1`, `4:3`, or `3:4` (default: `16:9`)                    |
| `seed`             | integer  | No       | Fixed seed for reproducibility                                              |
| `negative_prompt`  | string   | No       | Content to avoid                                                            |
| `extra_body.image` | string[] | No       | Keyframe input images (for keyframes mode)                                  |

## Workflow

1. POST create task -> get `video_id`
2. Poll GET `agnesapi?video_id=<ID>` until `status` is `completed` or `failed`
3. Download from `url` field

Statuses: `queued` -> `in_progress` -> `completed` | `failed`

## Prompt construction

- **Text-to-video**: `[Subject] + [Action] + [Scene] + [Camera Movement] + [Lighting] + [Style]`
- **Image-to-video**: Describe what should move and what should stay stable.
- **Keyframes**: Describe the transition between keyframes, maintaining identity and consistency.

## Response

```json
{
  "video_id": "video_xxx",
  "status": "completed",
  "url": "https://...",
  "seconds": "10.0",
  "size": "1280x768"
}
```

Use `video_id` (not `task_id`) to retrieve results. After normalization, `seconds` and `size` from response are source of truth.

## Gotchas

- Async workflow - always poll until `completed` or `failed`.
- `num_frames` must be `<= 441` and follow `8n + 1` rule.
- `frame_rate` range `1-60`. Higher = smoother but shorter duration.
- Video dimensions must be multiples of 64.
- Input images must be public HTTPS URLs.
- Timeout: tens of seconds to several minutes. Poll every 5-10s.
- Pricing (per resolution):
  - 720P: $0.025/sec
  - 1080P / 1K: $0.040/sec
  - 2K: $0.055/sec
  - Total billable seconds = output duration + input video duration
  - Input images: first 5 free, from 6th onward $0.005/image
  - **agnes-video-2.5-flash: currently free** under promotion.
- Error codes: `400`, `401`, `402`, `403`, `404`, `405`, `408`, `409`, `413`, `422`, `429`, `500`, `502`, `503`.

For curl examples, read `references/examples.md`. For duration/resolution tables and pricing, read `references/parameters.md`.
