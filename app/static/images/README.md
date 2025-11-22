# Phrase Images Directory

This directory contains images for phrase detail pages. Images are automatically detected and displayed when present.

## File Naming Convention

Images must be named using the **phrase slug**:

```
<phrase-slug>.<extension>
```

Supported extensions (checked in order):
1. `.webp` (recommended for best compression)
2. `.jpg`
3. `.jpeg`
4. `.png`

## Examples

For the phrase "бить баклуши" (slug: `bit-baklushi`):
- `bit-baklushi.webp` ✅ Best option
- `bit-baklushi.jpg` ✅ Alternative
- `bit-baklushi.png` ✅ Alternative

For the phrase "делать из мухи слона" (slug: `delat-iz-mukhi-slona`):
- `delat-iz-mukhi-slona.webp`

## Image Requirements

- **Format**: WebP (recommended), JPEG, or PNG
- **Dimensions**: 800x600px or 600x600px recommended
- **File size**: Keep under 200KB for optimal performance
- **Content**: Relevant illustration or visual representation of the phrase meaning

## Optimizing Images

### Convert to WebP (best compression)
```bash
cwebp -q 80 input.jpg -o output.webp
```

### Resize images
```bash
# Using ImageMagick
convert input.jpg -resize 800x600 output.jpg

# Or using ffmpeg
ffmpeg -i input.jpg -vf scale=800:600 output.jpg
```

### Batch convert
```bash
# Convert all JPGs to WebP in current directory
for file in *.jpg; do
  cwebp -q 80 "$file" -o "${file%.jpg}.webp"
done
```

## How Images Are Used

When a phrase detail page is rendered:

1. The system checks for an image matching the phrase slug
2. If found, the image is:
   - Displayed on the phrase detail page
   - Included in Open Graph meta tags (social media previews)
   - Referenced in JSON-LD structured data
3. If not found, a fallback illustration is shown

## Social Media Integration

Images added here will automatically appear when sharing phrase pages on:
- Facebook
- Twitter
- LinkedIn
- WhatsApp
- Telegram
- And other social platforms supporting Open Graph

## Placeholder Images for Categories

You can also add category-specific images for better social sharing:

- `category-<category-slug>.jpg`
- `og-home.jpg` - Home page Open Graph image
- `og-phrase.jpg` - Default phrase page Open Graph image

## Notes

- Images are served with far-future cache headers (1 year)
- Use lazy loading attribute (`loading="lazy"`) for performance
- Alt text is automatically set to the phrase text
- No database changes needed - just upload and it works!
