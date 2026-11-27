---
name: recipe-table
description: "Convert a recipe into a colorized recipe summary table (Tabular Recipe Notation): ingredients down the left, each step a box spanning what it combines, read left to right. Use when the user wants a recipe reformatted, condensed to one glanceable page, or made printable, from pasted text, a URL, or a photo."
---

# Recipe Table

The format is Michael Chu's Tabular Recipe Notation from Cooking for
Engineers. Ingredients run down the left in order of first use. Each column to
the right is a later step, and a step's box spans exactly the rows it acts on.
Boxes in the same column can happen in any order. The rightmost box spans
everything and is the finished dish.

A recipe in this form is a tree: the final step is the root, each step's
inputs are ingredients or earlier steps, and ingredients are the leaves. Write
the tree as JSON; [scripts/render_recipe_table.py](scripts/render_recipe_table.py)
derives every row, column and span from it, so never place spans by hand.

## 1. Collect the source

- URL: prefer the page's schema.org `Recipe` JSON-LD (`recipeIngredient`,
  `recipeInstructions`, `recipeYield`) over the page prose.
- Photo or scan: transcribe it, write `?` for an unreadable quantity, and tell
  the user which ones.
- Keep the source's quantities, units, temperatures, times and doneness cues
  word for word. Convert units only when the user asks.

Done when every source ingredient and instruction is listed and each unclear
item is flagged.

## 2. Build the tree

Shape, as in [examples/stuffing-muffins.json](examples/stuffing-muffins.json):

```json
{"title": "…", "meta": ["Makes 12", "Oven 350°F"], "notes": [], "source": "…",
 "dish": {"step": "Bake", "note": "…", "inputs": [
   {"step": "Whisk", "kind": "combine", "inputs": [
     {"qty": "3", "item": "large eggs"}, {"qty": "½ cup", "item": "whole milk"}]}]}}
```

- **Root:** the last action (Bake, Serve, Chill). A step's inputs are the
  ingredients and earlier steps whose output goes into it.
- **Step:** `step` is one capitalized verb (Cut, Melt, Sauté, Toss). `note`
  holds heat level, time, temperature, vessel and doneness cue, in short
  phrases joined by semicolons.
- **Ingredient:** `qty` is the amount, or `to taste` / `as needed`. Put quick
  prep in `item` (`onion, diced`). Prep that takes real time or a tool becomes
  its own step (Cut bread into ¾-inch cubes).
- **Order:** list a step's inputs with the earliest-started branch first, so
  rows follow first use.
- **Oven and equipment:** preheating goes in `meta`. Greasing a pan with an
  ingredient becomes a step that feeds the step using the pan.
- **Same ingredient twice:** split it into two leaves with split amounts
  (`2 tbsp sugar, for topping`).
- **Ingredient removed and returned later:** this does not fit the grid. Keep
  one box and say it in that step's note or in `notes`.
- **`kind`:** `prep`, `combine`, `heat` or `rest` sets the box color. The
  script infers it from common verbs; set it when the verb is unusual or the
  guess is wrong.
- **`notes`:** make-ahead, storage or substitutions from the source, one line
  each. Leave it empty when the source has none.

Done when every source instruction maps to a step or a note and every
ingredient appears exactly once as a leaf (or once per split use).

## 3. Render and deliver

```bash
python3 scripts/render_recipe_table.py recipe.json -o recipe.html   # primary
python3 scripts/render_recipe_table.py recipe.json --format md      # fallback
```

The HTML is self-contained, follows the system light or dark theme, and
prints. Colors: a cream ingredient column with bold olive quantities; step
boxes tinted by kind (blue prep, amber combine, red heat, teal rest); a green
final box; amber chips on every temperature and time.

Show the HTML through the host's page, artifact or preview tool when it has
one; otherwise save the file and give its path. Where only Markdown renders,
send the `--format md` output: numbered steps in cook order, bold quantities,
and temperatures and times in code spans. Markdown has no merged cells or
arbitrary colors, and a code span is the one highlight most chat renderers
show.

Done when you have looked at the rendered table and every box label and note
reads cleanly with nothing clipped. The script guarantees the grid; the look
is yours to check.

## Worked example

Source: "Melt the butter in a skillet, add onion and celery, and cook over
medium-low 10–15 minutes until very soft. Toss with the bread cubes."

```json
{"step": "Toss", "note": "gently, in a large bowl", "inputs": [
  {"step": "Cut", "note": "¾-inch cubes", "inputs": [
    {"qty": "12 cups", "item": "slightly stale bread"}]},
  {"step": "Sauté", "note": "medium-low, 10–15 min, very soft, no browning", "inputs": [
    {"step": "Melt", "note": "in skillet", "inputs": [
      {"qty": "½ cup", "item": "butter (1 stick)"}]},
    {"qty": "1–1½ cups", "item": "onion, diced"},
    {"qty": "2 cups", "item": "celery, diced"}]}]}
```

Rendered: bread gets its own row with Cut beside it; butter's row has Melt;
onion and celery rows stay cream until Sauté, which spans butter, onion and
celery; Toss spans all four rows to the right.
