# Agnes Video - Duration, Resolution & Recommended Parameters

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

The API normalizes to the closest supported tier: `480p`, `720p`, `1080p`.

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
