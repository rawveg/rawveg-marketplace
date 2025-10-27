# FLUX 1.1 Pro Model Optimization Guide

This reference provides technical details for using the FLUX 1.1 Pro model on Replicate via the MCP server.

## Model Information

**Model identifier**: `black-forest-labs/flux-1.1-pro`
**Provider**: Replicate (accessed via installed Replicate MCP server)
**Documentation**: https://replicate.com/black-forest-labs/flux-1.1-pro

## Using the Replicate MCP Server

The Replicate MCP server is already installed and provides direct access to create predictions. Use the `mcp__replicate__create_predictions` tool to generate images.

### Required Parameters

```typescript
{
  version: "black-forest-labs/flux-1.1-pro",  // Model identifier
  input: {
    prompt: string,              // Your Midjourney-style prompt
    aspect_ratio: "16:9",        // Default widescreen format
    output_format: "png",        // PNG for highest quality
    safety_tolerance: number     // Optional: 1-5, default is 2
  }
}
```

### MCP Server Tool Usage

Call the tool with these parameters:
```json
{
  "version": "black-forest-labs/flux-1.1-pro",
  "input": {
    "prompt": "[Your enhanced Midjourney-style prompt here]",
    "aspect_ratio": "16:9",
    "output_format": "png"
  }
}
```

The tool will return a prediction object with status and output URL when complete.

## FLUX 1.1 Pro Specifications

### Supported Aspect Ratios
- **1:1** - Square (1024×1024)
- **16:9** - Widescreen (1360×768) ← **Recommended default**
- **21:9** - Ultrawide (1536×640)
- **3:2** - Classic photo (1216×832)
- **2:3** - Portrait (832×1216)
- **4:5** - Portrait (960×1200)
- **5:4** - Landscape (1200×960)
- **9:16** - Vertical (768×1360)
- **9:21** - Vertical ultrawide (640×1536)

**Default**: 16:9 for cinematic, editorial-quality outputs

### Output Formats
- **png** - Highest quality, lossless ← **Recommended**
- **jpg** - Smaller file size, some quality loss
- **webp** - Modern format, good compression

### Safety Tolerance
Range: 1-5 (default: 2)
- **1**: Most restrictive
- **2**: Default, balanced ← **Recommended**
- **5**: Least restrictive

For Midjourney-style artistic content, use default (2) or higher (3-4).

## FLUX 1.1 Pro Strengths

### What FLUX Does Exceptionally Well

1. **Photorealism**
   - Near-perfect photographic quality
   - Accurate physical materials and textures
   - Realistic lighting and shadows
   - Natural human anatomy and proportions

2. **Text Rendering**
   - Accurate text in images (unlike most AI models)
   - Legible typography and signage
   - Proper letter spacing and formatting

3. **Complex Compositions**
   - Multiple subjects with accurate spatial relationships
   - Detailed backgrounds without quality loss
   - Consistent style across entire image

4. **Color Accuracy**
   - Precise color reproduction
   - Accurate skin tones
   - Faithful material colors (less stylized than Midjourney)

5. **Fine Details**
   - Intricate textures and patterns
   - Sharp focus with excellent clarity
   - High resolution output (up to 1536px on longest side)

### Optimizing for FLUX's Strengths

**Leverage photorealism:**
```
"ultra-realistic portrait, photographic quality, accurate skin texture with visible pores,
natural lighting, highly detailed, 8k resolution"
```

**Include text when needed:**
```
"vintage neon sign reading 'OPEN', glowing red letters, weathered metal frame,
urban nighttime photography, highly detailed"
```

**Request complex scenes:**
```
"bustling Tokyo street at night, multiple neon signs with Japanese text, crowds of people,
reflections on wet pavement, cinematic street photography, rich detail throughout"
```

**Specify accurate colors:**
```
"sunset over ocean, accurate warm orange and pink tones, natural color gradient,
photographic color accuracy, no oversaturation"
```

## Adapting Midjourney Prompts for FLUX

### Key Adaptations

1. **Be More Explicit About Artistic Treatment**

   Midjourney automatically adds artistic elevation; FLUX is more literal.

   ❌ Midjourney approach: "portrait of a woman"
   ✅ FLUX adaptation: "editorial portrait of a woman, professional color grading, cinematic lighting, artistic photography"

2. **Specify Color Grading Clearly**

   ❌ Too vague: "beautiful colors"
   ✅ Specific: "warm color grading with orange and teal tones, cinematic color treatment"

3. **Request Composition Explicitly**

   ❌ Implicit: "dramatic photo"
   ✅ Explicit: "low angle composition, dramatic perspective, carefully framed, rule of thirds"

4. **Add "Cinematic" for Elevation**

   Include "cinematic" for Midjourney-quality elevation:
   - "cinematic photography"
   - "cinematic lighting"
   - "cinematic composition"
   - "cinematic color grading"

5. **Emphasize Professional Quality**

   Add explicit quality markers:
   - "professional photography"
   - "editorial quality"
   - "award-winning"
   - "museum quality"
   - "expert color grading"

### FLUX-Specific Prompt Enhancements

**For Midjourney-level polish, add:**

```
Base prompt: "Woman in red dress in field"

Enhanced for FLUX:
"Woman in flowing red dress standing in golden wheat field, editorial fashion photography,
cinematic composition with subject centered, golden hour lighting, warm color grading with
rich earth tones, shot on Canon R5 85mm f/1.4, shallow depth of field, professional color
grading, highly detailed, award-winning photography"
```

**Quality enhancement formula:**
```
[Subject and scene] + [professional category] + [lighting specifics] +
[color treatment] + [technical specs] + [quality markers]
```

## Comparison: FLUX vs Midjourney

### Where FLUX Excels Over Midjourney
- ✅ More accurate photorealism
- ✅ Better text rendering
- ✅ More literal interpretation (pro and con)
- ✅ Higher detail retention in complex scenes
- ✅ More accurate colors and materials

### Where Midjourney Has Edge
- 🎨 Automatic artistic elevation
- 🎨 More "creative" interpretation
- 🎨 Stronger default stylization
- 🎨 Better at abstract/artistic concepts

### Bridging the Gap

To achieve Midjourney's artistic quality with FLUX:

1. **Always include style descriptors**: "editorial", "cinematic", "artistic"
2. **Specify color treatment**: Don't rely on automatic enhancement
3. **Request composition**: Explicitly describe framing and perspective
4. **Add quality terms**: "professional", "expert", "award-winning"
5. **Reference artistic styles**: Mention photographers, movements, or films

## Prompt Engineering Strategies for FLUX

### Strategy 1: Technical Photography Anchor

Ground the prompt in photographic reality:
```
"shot on [camera/lens], [aperture], [lighting setup], [film stock or processing]"
```

Example:
```
"shot on Hasselblad H6D, 80mm f/2.8, studio softbox lighting, professional color grading"
```

### Strategy 2: Cinematic Reference

Reference films or cinematographers for immediate style:
```
"cinematography inspired by [film/cinematographer], [specific visual qualities]"
```

Example:
```
"cinematography inspired by Blade Runner 2049, orange and teal color grading, volumetric fog,
dramatic lighting"
```

### Strategy 3: Artistic Movement Context

Place the image in an artistic tradition:
```
"[art movement] photography, [key characteristics], [notable practitioner]"
```

Example:
```
"contemporary portrait photography, intimate and natural, inspired by Annie Leibovitz,
editorial quality"
```

### Strategy 4: Layered Quality Modifiers

Stack quality terms strategically:
```
[technical quality] + [artistic quality] + [professional category]
```

Example:
```
"highly detailed, 8k resolution + cinematic composition, expert color grading +
award-winning editorial photography"
```

### Strategy 5: Environmental Storytelling

Rich environmental details enhance the Midjourney aesthetic:
```
[subject] in [detailed environment], [atmospheric conditions], [mood through details]
```

Example:
```
"vintage car on coastal highway, scattered clouds in blue sky, late afternoon golden light,
sense of nostalgia and freedom"
```

## Common FLUX Optimization Patterns

### Portrait Photography
```
[Subject] [expression/pose], editorial portrait photography, [lighting direction and quality],
[color treatment], shot on [camera] [lens] [aperture], [background treatment],
professional color grading, highly detailed, [quality marker]
```

### Landscape/Environment
```
[Location], [time of day], [weather/atmosphere], cinematic landscape photography,
[composition], [lighting quality], shot on [camera] [lens], [color grading],
[artistic reference], 8k resolution, highly detailed
```

### Product Photography
```
[Product] on [surface/setting], editorial product photography, [lighting setup],
[background], shot on [camera] [lens], [material emphasis], professional color grading,
tack sharp focus, commercial photography quality
```

### Architectural Photography
```
[Structure], [perspective], architectural photography, [time/lighting], [mood],
shot on [camera] [tilt-shift lens], [compositional elements], professional color grading,
highly detailed, [quality marker]
```

### Fashion Editorial
```
[Subject] in [clothing], [pose/movement], high fashion editorial, [setting], [lighting],
[aesthetic], shot on [camera] [lens], [artistic reference], [color treatment],
award-winning fashion photography
```

## Workflow Recommendations

### Step 1: Understand User Intent
Clarify what the user wants to create - subject, mood, style, purpose.

### Step 2: Select Prompt Pattern
Choose appropriate pattern from midjourney-style-guide.md based on genre.

### Step 3: Build Layered Prompt
Construct prompt following the 5-layer structure from style guide.

### Step 4: Apply FLUX Adaptations
Enhance with explicit quality terms, color grading, and technical specs.

### Step 5: Verify Quality
Check against the style guide checklist (40-75 words, all elements present).

### Step 6: Generate via MCP Server
Use `mcp__replicate__create_predictions` with optimized parameters.

### Step 7: Offer Variations
Provide 2-3 alternative prompts emphasizing different aspects if requested.

## Parameter Selection Guide

### When to Use Different Aspect Ratios

**16:9 (Default)**:
- Cinematic scenes
- Landscapes
- Editorial spreads
- Professional photography

**1:1 (Square)**:
- Social media posts
- Profile pictures
- Product shots
- Symmetrical compositions

**2:3 / 4:5 (Portrait)**:
- Fashion photography
- Portrait photography
- Magazine covers
- Vertical social media

**3:2 (Classic Photo)**:
- Traditional photography
- Print photography
- Gallery prints

**21:9 (Ultrawide)**:
- Panoramic landscapes
- Epic cinematic shots
- Wide establishing shots

### Safety Tolerance Selection

**Level 2 (Default)**: Most Midjourney-style content
**Level 3-4**: Artistic nude photography, mature themes (when appropriate)
**Level 1**: Family-friendly, corporate, conservative contexts

## Advanced Techniques

### Multi-Element Composition
For complex scenes, structure hierarchically:
```
[Primary subject] + [secondary elements] + [background] + [atmosphere] + [technical specs]
```

Example:
```
"Elderly fisherman mending nets in foreground, weathered fishing boat in middle ground,
misty harbor in background, early morning fog, golden hour lighting, cinematic composition,
shot on ARRI Alexa 35mm, warm color grading, highly detailed, documentary photography style"
```

### Color Palette Control
Specify complete color schemes:
```
[Primary color] with [secondary colors], [color relationship], [color mood]
```

Example:
```
"deep teal ocean with warm orange sunset, complementary color scheme, rich color saturation,
cinematic color grading"
```

### Mood Through Details
Build atmosphere through specific environmental details:
```
[Subject] + [small environmental details] + [lighting that reinforces mood] + [color that reinforces mood]
```

Example:
```
"Woman reading by window, dust particles visible in sunbeams, soft afternoon light,
warm golden tones, sense of peaceful solitude, intimate and contemplative"
```

## Troubleshooting Common Issues

### Issue: Output Too Literal, Not Artistic Enough
**Solution**: Add "cinematic", "editorial", "artistic photography", "professional color grading"

### Issue: Colors Too Flat
**Solution**: Specify "rich color saturation", "tonal depth", "expert color grading", reference film stock

### Issue: Composition Too Centered
**Solution**: Explicitly request "rule of thirds", "dynamic composition", "carefully framed"

### Issue: Lighting Too Uniform
**Solution**: Describe complete lighting setup with direction, quality, and motivation

### Issue: Missing Midjourney Polish
**Solution**: Add quality stack: "highly detailed + professional color grading + award-winning + editorial quality"

## Best Practices Summary

1. ✅ Always include "cinematic" or "editorial" for artistic elevation
2. ✅ Specify color grading explicitly (don't rely on defaults)
3. ✅ Use technical photography terms to anchor realism
4. ✅ Reference artistic styles or practitioners when appropriate
5. ✅ Keep prompts 40-75 words for optimal results
6. ✅ Layer quality modifiers strategically
7. ✅ Describe lighting with direction and quality
8. ✅ Request specific composition techniques
9. ✅ Use 16:9 aspect ratio for Midjourney-style cinematic quality
10. ✅ Choose PNG output format for maximum quality
