# Replicate Hardware Options

Available hardware SKUs for model creation and deployments:

| SKU | Name | Use Case |
|-----|------|----------|
| `cpu` | CPU | Lightweight models, text processing |
| `gpu-t4` | Nvidia T4 GPU | Cost-effective inference, smaller models |
| `gpu-l40s` | Nvidia L40S GPU | Balanced performance and cost |
| `gpu-l40s-2x` | 2x Nvidia L40S GPU | Larger models requiring more VRAM |
| `gpu-a100-large` | Nvidia A100 (80GB) GPU | High-performance inference, large models |
| `gpu-a100-large-2x` | 2x Nvidia A100 (80GB) GPU | Very large models, maximum VRAM |
| `gpu-h100` | Nvidia H100 GPU | Latest generation, highest performance |

## Hardware Selection Guidelines

- **Image generation models (SDXL, Flux)**: `gpu-a100-large` or `gpu-l40s`
- **Large language models**: `gpu-a100-large` or higher
- **Smaller inference tasks**: `gpu-t4` for cost efficiency
- **Fine-tuning/training**: `gpu-a100-large` or `gpu-h100` recommended

To list current hardware options:
```bash
replicate hardware list
```
