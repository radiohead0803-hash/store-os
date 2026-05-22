# Claude Design Automation

Use this reference when designing printable, sticker, thumbnail, detail-page, package, or marketing assets with Claude Design.

## Core Rule

Claude Design may generate and revise design assets, but a product cannot launch until print proof, copyright check, and operator approval are recorded.

## Design Automation Flow

```text
product idea -> design brief -> Claude Design prompt -> asset generation -> version record -> print/readability proof -> copyright/claims check -> operator approval -> listing asset publish
```

## Required Design Asset Types

| Asset | Purpose | Proof required |
|---|---|---|
| A4 reward board PDF | printable product core | A4 print readability photo or screenshot |
| sticker sheet | physical sticker production | size, cutline, bleed, safe area proof |
| thumbnail | product-page click asset | mobile readability proof |
| detail image | listing explanation | component/size/use clarity |
| instruction card | customer use guide | no misleading claim |
| package label | shipment branding | address/privacy-safe layout |

## Claude Design Prompt Structure

Always include:

1. Product name and target customer.
2. Output asset type and size.
3. Use scene.
4. Style constraints.
5. Text to include.
6. Print constraints.
7. Accessibility/readability constraints.
8. Things to avoid.
9. Required exports.
10. Proof checklist.

## Default Sticker Print Constraints

| Item | Default |
|---|---|
| Board | A4 vertical PDF |
| Sticker sheet | circle stickers, 30 pieces, vendor template if available |
| Bleed | follow vendor template; otherwise request 3 mm bleed note |
| Safe area | keep text/icons away from cutline |
| Color | pastel, high contrast enough for print |
| Text | Korean, large enough for elementary child and parent |
| Prohibited | copyrighted characters, guaranteed educational claims, tiny text |

## Design Version Rules

Store each generated asset as a `DesignAsset` record:

| Field | Required value |
|---|---|
| product_id | linked product |
| type | board_pdf, sticker_sheet, thumbnail, detail_image, instruction_card, package_label |
| prompt | original Claude Design prompt |
| file_url | storage path or placeholder |
| version | v1, v2, v3... |
| proof_status | pending, pass, conditional, fail |
| operator_approval | pending, approved, rejected |

## Design Failure Handling

| Failure | Action |
|---|---|
| text too small | regenerate with larger type and fewer sections |
| cutline unsafe | use vendor template and regenerate |
| copyright risk | remove asset and regenerate from generic shapes/icons |
| print color poor | create high-contrast and black-white version |
| AI output inconsistent | lock the approved layout and request only copy/color change |
| Claude Design unavailable | fallback to uploaded template or manual design tool, then record exception |

## Proof Checklist

- A4 output is readable on desktop and mobile preview.
- Text remains readable when printed or previewed at actual size.
- Sticker cutline and safe area are acceptable.
- No copyrighted character, trademark, or copied design style is used.
- No guaranteed education/performance claim exists.
- Thumbnail is readable at mobile size.
- Operator approval is recorded before listing publication.
