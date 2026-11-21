# Good Steam: a card game for the sauna lounge

An original printable card game by DIVELUX for 2–6 players, about 15–20 minutes, ages 8 and up.
Players host sauna "rounds" (heat, steam, whisk and a cool-down at the lake), friends join in with matching
cards, and the most points wins. No stakes, no drinking, no dares. Play it in the lounge or changing room,
not in the hot room: paper and heat don't mix, and nothing in the game is about staying in the heat.

Made by DIVELUX, makers of wool sauna hats: https://diveluxsaunahat.com ·
more free tools: https://diveluxsaunahat.com/pages/sauna-tools

## Files

| File | What it is |
|---|---|
| `sauna-card-game-letter.pdf` | US Letter, 16 pages |
| `sauna-card-game-a4.pdf` | A4, 16 pages |
| `sauna-card-game.html` | Source (fonts embedded). Add `?paper=a4` to the address for A4 |
| `preview.png` | Rules page and one card sheet with its backs |
| `simulation/simulate.py` | The rules simulator (Python 3, standard library only) |
| `simulation/report.txt` | Full simulation output |

Pages: 1 rules · 2 score sheet and printing notes · 3–16 card sheets (front, then its back).

## What is in the deck

63 cards, 2.5 x 3.5 in (poker size), nine per sheet with crop marks:

- 56 ritual cards: Stones (heat), Ladle (steam), Birch (whisk), Lake (cool-down), each numbered 1–7, two of each
- 4 Wool Hat cards (wild)
- 3 quick-rule cards (not shuffled in)

## Rules in short

- Deal 5 cards each. Lay 4 cards face up as the Bench. Head start on the score sheet: first player 0, second 1, everyone else 2.
- On your turn do one thing:
  - **Gather:** take 2 cards from the Bench and/or the deck, refill the Bench to 4. Hand limit 8 (discard to the Steam pile).
  - **Host a round:** lay down 3 or 4 cards of different rituals, one of them a Lake. A Wool Hat can stand in for Stones, Ladle or Birch (counts 0, never the Lake). Score the sum, +3 for all four rituals.
- **Joining in:** going left, every other player may add one card with the same number as the host's Lake (any ritual) or a Wool Hat. Each guest scores the Lake's number, the host scores +1 per guest.
- **Last call:** when the deck runs out, shuffle the Steam pile and count off 20 cards as the last deck. When that runs out, finish the lap so everyone has had the same number of turns. −1 for each card left in hand. Most points wins.

The full rules are on page 1 of the PDF.

## Printing

Print at 100% (actual size) on card stock, about 80–110 lb cover (216–300 gsm). Pages 3–16 double-sided,
"flip on long edge"; each back page follows its front page. All backs are the same design, laid out on the same
grid as the fronts, so small duplex shifts only move the frame a little. Print one test sheet first.
Cut on the crop marks. You also need a pencil and the score sheet (page 2, print as many as you like).

## Rules simulation

Before printing, the rules were tested with `simulation/simulate.py`: 4,000 games for every player count
(2–6) and every player mix, 80,000 games in total. Run it yourself with `python3 simulate.py 4000`.

Computer players used:

- **steady:** a sensible player (hosts big rounds, waits a little for a full round, takes useful Bench cards)
- **eager:** hosts a round as soon as it can
- **full-only:** waits for rounds with all four rituals
- **random:** picks any legal move at random (used to look for stuck states)

### Results with the printed rules (steady players)

| Players | Games that ended | Turns per game, mean (min–max) | Turns each | Est. minutes* | Win rate by seat (fair share) | Ties |
|---|---|---|---|---|---|---|
| 2 | 4000/4000 | 48.7 (42–52) | 24.4 | 17 | 52.2 / 47.8 % (50 %) | 1.7 % |
| 3 | 4000/4000 | 45.5 (39–48) | 15.2 | 17 | 34.6 / 32.4 / 33.0 % (33.3 %) | 4.2 % |
| 4 | 4000/4000 | 40.8 (36–44) | 10.2 | 16 | 24.8 / 25.8 / 24.7 / 24.7 % (25 %) | 4.4 % |
| 5 | 4000/4000 | 39.3 (35–45) | 7.9 | 17 | 21.9 / 20.8 / 20.8 / 19.0 / 17.6 % (20 %) | 5.9 % |
| 6 | 4000/4000 | 35.9 (30–36) | 6.0 | 16 | 16.4 / 16.0 / 19.2 / 16.6 / 15.8 / 15.9 % (16.7 %) | 7.0 % |

Largest gap between any seat and a fair share: 2.6 percentage points.

\* Play time is an estimate, not a measurement: about 15 seconds per turn plus 10 seconds and 5 seconds per player
for every hosted round (lay it out, everyone checks for a matching number, write the points). Real tables will vary.

### What the simulation showed

- **Every game ends.** 80,000 games, none hit the 1,000-turn safety cap, including 20,000 games of purely random
  moves (18–52 turns). The game cannot loop: every Gather removes cards from the deck or the Bench, the Steam pile
  is reshuffled only once, and the "finish the lap" rule ends the game.
- **First player edge, and the fix.** Without a head start the first player won 54 % of 2-player games, 38.6 % at
  3 players (fair 33.3 %) and 28.9 % at 4 players (fair 25 %). With the printed head start (0 / 1 / 2 / 2 ...)
  every seat lands within 2.6 points of a fair share.
- **Length.** The first version (one pass through the deck) was too short for 4–6 players (4–7 turns each). A full
  reshuffle made 2–3 player games too long. The "Last call" deck of 20 cards keeps every player count at about
  36–49 turns.
- **Skill matters, but no single trick wins.** In mixed tables (strength 1.00 = a fair share of wins), the steady
  and full-only players score 1.37–1.55, the eager player 0.86–0.95, random moves 0.03–0.24.
- **Everyone stays in the game.** Joining gives 10 % of all points at 2 players and 35 % at 6 players, so players
  score on other people's turns too.

The simulation covers the printed rules only. The optional "sauna break" house rule (skip a player who steps into
the sauna) was not simulated.

## License

Text, rules, layout and card art: CC BY 4.0 (Creative Commons Attribution 4.0 International).
Credit: DIVELUX, https://diveluxsaunahat.com. The simulator script is also CC BY 4.0.
Card illustrations come from the DIVELUX Sauna Illustrations (CC BY 4.0) and DIVELUX sauna icons (CC BY 4.0).
The DIVELUX name and logo are © DIVELUX Inc. and are not covered by the license.
Fonts in the PDFs: Bricolage Grotesque and Inter (SIL Open Font License 1.1).
