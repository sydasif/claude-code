# Agnes Video - Duration, Resolution, Pricing & Recommended Parameters

## Pricing

All prices in USD. **agnes-video-2.5-flash is currently free** under promotion.

| Resolution | Unit price |
| ---------- | ---------- |
| 720P       | $0.025/sec |
| 1080P / 1K | $0.040/sec |
| 2K         | $0.055/sec |

**Billing formula:**

```text
Total cost = (output seconds + input video seconds) × resolution unit price
           + max(0, input images - 5) × $0.005/image
```

- Total billable duration includes both output and input video durations
- First 5 input images are free; each image from the 6th onward costs $0.005
- `agnes-video-2.5-flash` uses the same formula but is currently $0 for all items

## Duration formula

```
seconds = num_frames / frame_rate
```

`num_frames` must be `<= 441` and follow the `8n + 1` rule. `frame_rate` range: `1-60`.

| Target Duration | Recommended Parameters              |
| --------------- | ----------------------------------- |
| ~3 seconds      | `num_frames: 81`, `frame_rate: 24`  |
| ~5 seconds      | `num_frames: 121`, `frame_rate: 24` |
| ~10 seconds     | `num_frames: 241`, `frame_rate: 24` |
| ~18 seconds     | `num_frames: 441`, `frame_rate: 24` |

## Resolution tiers

The API normalizes to the closest supported tier: `480p`, `720p`, `1080p`, `2K`.

| Aspect Ratio | Recommended Use Case                           |
| ------------ | ---------------------------------------------- |
| `16:9`       | Landscape, product demos, YouTube-style        |
| `9:16`       | Vertical short videos, TikTok / Reels / Shorts |
| `1:1`        | Square social media feeds                      |
| `4:3`        | Traditional landscape, presentations           |
| `3:4`        | Vertical presentations, portrait-focused       |

## Recommended parameters

| Scenario                  | Recommended Settings                                              |
| ------------------------- | ----------------------------------------------------------------- |
| Standard video generation | `width: 1152`, `height: 768`, `num_frames: 121`, `frame_rate: 24` |
| Social short videos       | `num_frames: 81` or `121`, `frame_rate: 24`                       |
| Longer videos             | Increase `num_frames` or reduce `frame_rate`                      |
| Smoother motion           | Use `frame_rate: 24` or `30`                                      |
| Reproducible results      | Set a fixed `seed`                                                |
| Keyframe transition       | Use `extra_body.mode: "keyframes"`                                |
| Avoid unwanted content    | Use `negative_prompt`                                             |
