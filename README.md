# Hitori (Python)

A playable version of **Hitori**, the Japanese logic puzzle, written in Python as a first-year university project (Computer Engineering, University of Parma).

> **Status:** playable, work in progress. See *Known issues* below.

## The puzzle

Shade some cells black so that:

1. No number appears more than once in any row or column (among the unshaded cells).
2. No two black cells touch horizontally or vertically.
3. All unshaded cells form one connected area.

## Features

- 6 levels, from 5×5 (easy) to 15×15 (impossible), loaded from CSV files
- Level selection menu (button in the bottom-right corner)
- Live error highlighting: adjacent black cells turn **red**, and circled cells with duplicate numbers in the same row or column are marked
- Status bar showing progress or the rule currently broken
- Automatic win detection

## Controls

| Input | Action |
|---|---|
| Left click | Cycle a cell: circle (keep white) → black → clear |
| Menu button (bottom right) | Choose a level (1–6) |
| `Esc` | Quit |

## How to run

Requires **Python 3.10+** and **pygame-ce**.

```bash
pip install pygame-ce
python3 main.py
```

The level files (`*.csv`) and `Menu.png` must be in the same folder as `main.py`.

## Project structure

| File | Contents |
|---|---|
| `main.py` | Entry point: loads level 1 and starts the GUI |
| `hitori0.py` | Game logic: board state, rule checks, win detection, level loading |
| `boardgamegui.py` | Mouse input, board drawing, level-selection menu |
| `boardgame.py` | Abstract board-game interface *(course-provided)* |
| `g2d.py` | Simple 2D graphics wrapper on pygame *(course-provided)* |
| `*.csv` | Puzzle levels, one row of comma-separated numbers per line |

## Known issues / next steps

- [ ] Right click currently shades every unmarked cell black instead of acting on a single cell
- [ ] After choosing a level, the board only appears after the first click
- [ ] Add an undo button and a timer

## What I learned

*(Write 2–4 sentences here in your own words.)*

## Credits

- `boardgame.py` and `g2d.py`: course framework by [Michele Tomaiuolo](https://tomamic.github.io/), MIT License.
