#!/usr/bin/env python3
"""Rules simulator for "Good Steam", the DIVELUX sauna card game.

Plays thousands of random games with simple computer players and reports:
  - every game ends (hard cap on turns, never reached = no endless loops)
  - number of turns per game and per player
  - win rate by seat (does the first player have an edge?)
  - average and spread of the scores, how often players join rounds, ties

The rules below are the printed rules. Two kinds of computer players are used:
  "steady"  a sensible player (simple greedy rules with a little randomness)
  "random"  picks any legal move at random (used to look for stuck states)

Usage: python3 simulate.py [games_per_setting]       (default 4000)
Standard library only. CC BY 4.0, DIVELUX, https://diveluxsaunahat.com
"""
import random
import statistics
import sys
from collections import Counter

RITUALS = ("stones", "ladle", "birch", "lake")
LAKE = "lake"
HAT = "hat"

# ---- the printed rules -------------------------------------------------------------------------
RULES = dict(
    values=range(1, 8),      # ritual cards are numbered 1-7
    copies=2,                # two of each ritual and number: 4 rituals x 7 numbers x 2 = 56 cards
    hats=4,                  # + 4 Wool Hats = 60 cards in the deck
    hat_value=0,             # a hat stands in for Stones, Ladle or Birch (never the Lake) and counts 0 in a round;
                             # as a guest it joins any round and scores the Lake's number
    bench=4,                 # face-up cards in the middle ("the Bench")
    hand=5,                  # cards dealt to each player
    head_start=lambda n, seat: min(seat, 2),   # starting points: first player 0, second 1, everyone else 2
    gather=2,                # take two cards: from the Bench and/or the deck, in any mix
    limit=8,                 # hand limit at the end of your turn
    full_bonus=3,            # a round with all four rituals scores +3
    host_per_guest=1,        # the host scores +1 for every player who joins
    last_deck=20,            # "Last call": deck empty -> shuffle the Steam pile, count off 20 cards as the last deck
    leftover=-1,             # each card left in hand at the end: -1 (hats too)
)
MAX_TURNS = 1000             # safety cap; a game that hits it counts as "did not end"


def make_deck(R):
    deck = [(r, v) for r in RITUALS for v in R["values"] for _ in range(R["copies"])]
    deck += [(HAT, 0)] * R["hats"]
    return deck


def round_score(cards, R):
    s = sum(R["hat_value"] if r == HAT else v for r, v in cards)
    if len(cards) == 4:
        s += R["full_bonus"]
    return s


def legal_rounds(hand, R):
    """All rounds that can be hosted from this hand: 3 or 4 cards, a real Lake card, other cards all different
    rituals; a hat may stand in for any missing ritual except Lake."""
    lakes = [c for c in hand if c[0] == LAKE]
    if not lakes:
        return []
    out = []
    best = {}
    for c in hand:
        if c[0] in ("stones", "ladle", "birch"):
            best.setdefault(c[0], []).append(c)
    hats = [c for c in hand if c[0] == HAT]
    seen = set()
    for lake in set(lakes):
        # choose for each of the three other rituals: one of its cards, a hat, or nothing
        opts = []
        for r in ("stones", "ladle", "birch"):
            o = [None] + sorted(set(best.get(r, [])))
            if hats:
                o.append((HAT, 0))
            opts.append(o)
        for a in opts[0]:
            for b in opts[1]:
                for c in opts[2]:
                    pick = [x for x in (a, b, c) if x]
                    if len(pick) < 2:
                        continue
                    if sum(1 for x in pick if x[0] == HAT) > len(hats):
                        continue
                    key = tuple(sorted(pick + [lake]))
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append([lake] + pick)
    return out


def can_join(hand, lake_num):
    return [c for c in hand if (c[0] != HAT and c[1] == lake_num) or c[0] == HAT]


class Game:
    def __init__(self, n, R, players, rng):
        self.n, self.R, self.rng = n, R, rng
        self.deck = make_deck(R)
        rng.shuffle(self.deck)
        self.hands = []
        for seat in range(n):
            k = R["hand"]
            self.hands.append([self.deck.pop() for _ in range(k)])
        self.bench = [self.deck.pop() for _ in range(R["bench"])]
        self.score = [R["head_start"](n, seat) for seat in range(n)]
        self.players = players
        self.turns = 0
        self.hosts = 0
        self.joins = 0
        self.full = 0
        self.discarded = 0
        self.join_pts = 0
        self.used = []                     # the Steam pile: every card that has been played or discarded
        self.reshuffles = 1 if R.get("last_deck") else 0

    def restock(self):
        """Deck empty and a reshuffle left: the Steam pile becomes the new deck."""
        if not self.deck and self.reshuffles > 0 and self.used:
            self.deck, self.used = self.used, []
            self.rng.shuffle(self.deck)
            self.deck = self.deck[:self.R["last_deck"]]     # the rest goes back in the box
            self.reshuffles -= 1

    def last_lap(self):
        return not self.deck and (self.reshuffles == 0 or not self.used)

    def refill(self):
        while len(self.bench) < self.R["bench"]:
            self.restock()
            if not self.deck:
                break
            self.bench.append(self.deck.pop())

    def play(self):
        R = self.R
        seat = 0
        while True:
            self.turns += 1
            if self.turns > MAX_TURNS:
                return False
            p = self.players[seat]
            hand = self.hands[seat]
            act = p.choose(self, seat)
            if act[0] == "host":
                cards = act[1]
                for c in cards:
                    hand.remove(c)
                self.used.extend(cards)
                lake = [c for c in cards if c[0] == LAKE][0]
                pts = round_score(cards, R)
                self.hosts += 1
                if len(cards) == 4:
                    self.full += 1
                guests = 0
                for k in range(1, self.n):
                    s2 = (seat + k) % self.n
                    j = self.players[s2].join(self, s2, lake[1])
                    if j:
                        self.hands[s2].remove(j)
                        self.used.append(j)
                        self.score[s2] += lake[1]
                        self.join_pts += lake[1]
                        guests += 1
                        self.joins += 1
                pts += guests * R["host_per_guest"]
                self.score[seat] += pts
            else:  # gather: list of bench indexes (None = deck)
                took = 0
                for src in act[1]:
                    if src is None:
                        self.restock()
                        if self.deck:
                            hand.append(self.deck.pop())
                            took += 1
                    else:
                        hand.append(self.bench[src])
                        self.bench[src] = None
                        took += 1
                self.bench = [c for c in self.bench if c is not None]
                self.refill()
                while len(hand) > R["limit"]:
                    d = p.discard(self, seat)
                    hand.remove(d)
                    self.used.append(d)
                    self.discarded += 1
            # end: once the deck runs out, finish the lap, so everyone has had the same number of turns
            self.restock()
            if self.last_lap() and seat == self.n - 1:
                break
            seat = (seat + 1) % self.n
        for s in range(self.n):
            self.score[s] += R["leftover"] * len(self.hands[s])
        return True


class Steady:
    """A sensible player: hosts big rounds, waits a little for a full round, takes useful Bench cards."""

    def __init__(self, rng, patience=None):
        self.rng = rng
        self.patience = patience if patience is not None else rng.choice((0, 1, 1, 2))

    def value(self, hand, R):
        rs = legal_rounds(hand, R)
        return max((round_score(r, R) for r in rs), default=0)

    def choose(self, g, seat):
        R = g.R
        hand = g.hands[seat]
        rounds = legal_rounds(hand, R)
        endgame = g.reshuffles == 0 and len(g.deck) <= 2 * g.n
        if rounds:
            best = max(rounds, key=lambda r: (round_score(r, R) - 0.15 * r[0][1] * (g.n - 1), len(r)))
            full = len(best) == 4
            if full or endgame or len(hand) >= R["limit"] - self.patience or not g.deck:
                return ("host", best)
        # gather: score each bench card by how much it helps
        have = Counter(c[0] for c in hand)
        lakes = have[LAKE]

        def useful(c):
            r, v = c
            if r == HAT:
                return 6.5
            u = v
            if r == LAKE and lakes == 0:
                u += 4
            elif have[r] == 0:
                u += 3
            elif r == LAKE:
                u += 1
            return u

        picks = []
        bench = list(enumerate(g.bench))
        for _ in range(R["gather"]):
            cand = [(useful(c) + self.rng.random() * 1.5, i, c) for i, c in bench if i not in picks]
            if cand:
                u, i, c = max(cand)
                if u >= 6.0 or not g.deck:
                    picks.append(i)
                    have[c[0]] += 1
                    continue
            picks.append(None)
        return ("gather", picks)

    def join(self, g, seat, num):
        opts = can_join(g.hands[seat], num)
        if not opts:
            return None
        real = [c for c in opts if c[0] != HAT]
        if real:
            have = Counter(c[0] for c in g.hands[seat])
            # give away the card you have the most copies of; keep your only Lake
            real.sort(key=lambda c: (c[0] == LAKE and have[LAKE] == 1, -have[c[0]]))
            return real[0]
        return opts[0] if num >= 5 else None

    def discard(self, g, seat):
        hand = g.hands[seat]
        have = Counter(c[0] for c in hand)
        return min(hand, key=lambda c: (c[0] == HAT, c[1] - (2 if have[c[0]] > 2 else 0)))


class Eager(Steady):
    """Hosts a round as soon as it can."""

    def __init__(self, rng):
        super().__init__(rng, patience=99)


class FullOnly(Steady):
    """Waits for full rounds (all four rituals) unless the hand is full or the game is ending."""

    def choose(self, g, seat):
        hand = g.hands[seat]
        rounds = [r for r in legal_rounds(hand, g.R) if len(r) == 4]
        if rounds:
            return ("host", max(rounds, key=lambda r: round_score(r, g.R)))
        self.patience = 0
        return super().choose(g, seat)


class RandomPlayer:
    def __init__(self, rng):
        self.rng = rng

    def choose(self, g, seat):
        rounds = legal_rounds(g.hands[seat], g.R)
        if rounds and self.rng.random() < 0.5:
            return ("host", self.rng.choice(rounds))
        srcs = list(range(len(g.bench))) + [None] * g.R["gather"]
        self.rng.shuffle(srcs)
        picks, used = [], set()
        for s in srcs:
            if len(picks) == g.R["gather"]:
                break
            if s is None or s not in used:
                picks.append(s)
                if s is not None:
                    used.add(s)
        return ("gather", picks)

    def join(self, g, seat, num):
        opts = can_join(g.hands[seat], num)
        return self.rng.choice(opts) if opts and self.rng.random() < 0.7 else None

    def discard(self, g, seat):
        return self.rng.choice(g.hands[seat])


TYPES = {"steady": Steady, "eager": Eager, "full-only": FullOnly, "random": RandomPlayer}


def run(n, games, R, kinds=("steady",), seed=1):
    """kinds: player types; with several types each game gets a random mix (seats shuffled)."""
    rng = random.Random(seed * 1000 + n * 7 + len(kinds))
    wins = [0.0] * n
    type_wins, type_seats = Counter(), Counter()
    turns, scores, spreads, hosts, joins, fulls, jshare, unfinished, ties = [], [], [], [], [], [], [], 0, 0
    for _ in range(games):
        names = [rng.choice(kinds) for _ in range(n)]
        players = [TYPES[k](rng) for k in names]
        g = Game(n, R, players, rng)
        if not g.play():
            unfinished += 1
            continue
        top = max(g.score)
        w = [s for s in range(n) if g.score[s] == top]
        if len(w) > 1:
            ties += 1
        for s in w:
            wins[s] += 1 / len(w)
            type_wins[names[s]] += 1 / len(w)
        for k in names:
            type_seats[k] += 1
        turns.append(g.turns)
        scores.extend(g.score)
        spreads.append(top - min(g.score))
        hosts.append(g.hosts)
        joins.append(g.joins)
        fulls.append(g.full)
        jshare.append(g.join_pts / max(1, sum(g.score)))
    done = games - unfinished
    return dict(n=n, games=games, unfinished=unfinished, turns=turns, wins=[w / done for w in wins],
                score_mean=statistics.mean(scores), score_sd=statistics.pstdev(scores),
                spread=statistics.mean(spreads), hosts=statistics.mean(hosts), joins=statistics.mean(joins),
                fulls=statistics.mean(fulls), ties=ties / done, join_share=statistics.mean(jshare),
                # win rate of a player of this type relative to a fair share (1.0 = wins exactly 1/n of its games)
                strength={k: type_wins[k] / type_seats[k] * n for k in type_seats})


def minutes(r, n):
    """Rough play time: about 15 s per turn, plus 10 s and 5 s per player for each hosted round
    (lay it out, everyone checks for a matching number, write the points)."""
    return (statistics.mean(r["turns"]) * 15 + r["hosts"] * (10 + 5 * n)) / 60


def report(games):
    lines = []
    out = lines.append
    out(f"Good Steam - rules simulation ({games} games for every player count and player mix)")
    out("Rules as printed: 60 cards (4 rituals x numbers 1-7 x 2 copies + 4 Wool Hats), deal 5, Bench of 4,")
    out("gather 2, hand limit 8, full round +3, host +1 per guest, Last call deck of 20, -1 per card left in hand,")
    out("head start: first player 0 points, second 1, everyone else 2.")
    out("")
    out("1. Sensible players (all 'steady')")
    out("players | games ended | turns per game, mean (min-max) | turns each | est. minutes | win rate by seat (fair share) | score mean (sd) | rounds hosted | guests joining | full rounds | points from joining | ties")
    worst = 0
    for n in range(2, 7):
        r = run(n, games, RULES)
        t = r["turns"]
        worst = max([worst] + [abs(w - 1 / n) for w in r["wins"]])
        out(f"{n} | {r['games'] - r['unfinished']}/{r['games']} | {statistics.mean(t):.1f} ({min(t)}-{max(t)}) | "
            f"{statistics.mean(t) / n:.1f} | {minutes(r, n):.0f} | "
            + " / ".join(f"{w * 100:.1f}%" for w in r["wins"]) + f" ({100 / n:.1f}%)"
            + f" | {r['score_mean']:.1f} ({r['score_sd']:.1f}) | {r['hosts']:.1f} | {r['joins']:.1f} | {r['fulls']:.1f}"
            f" | {r['join_share'] * 100:.0f}% | {r['ties'] * 100:.1f}%")
    out(f"Largest gap between any seat's win rate and a fair share: {worst * 100:.1f} percentage points")
    out("")
    out("2. Stuck-state check: players who pick any legal move at random")
    out("players | games ended | turns per game, mean (min-max)")
    for n in range(2, 7):
        r = run(n, games, RULES, ("random",))
        t = r["turns"]
        out(f"{n} | {r['games'] - r['unfinished']}/{r['games']} | {statistics.mean(t):.1f} ({min(t)}-{max(t)})")
    out("")
    out("3. Strategy check: mixed tables (seats and types drawn at random). Strength 1.00 = wins its fair share.")
    out("players | steady | eager (hosts at once) | full-only (waits for 4 rituals) | random")
    for n in range(2, 7):
        r = run(n, games, RULES, ("steady", "eager", "full-only", "random"))
        st = r["strength"]
        out(f"{n} | " + " | ".join(f"{st.get(k, 0):.2f}" for k in ("steady", "eager", "full-only", "random")))
    out("")
    out("4. Without the head start (why it is in the rules): win rate by seat, steady players")
    for n in range(2, 7):
        r = run(n, games, dict(RULES, head_start=lambda n, s: 0))
        out(f"{n} players: " + " / ".join(f"{w * 100:.1f}%" for w in r["wins"]) + f"  (fair {100 / n:.1f}%)")
    return "\n".join(lines)


if __name__ == "__main__":
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    print(report(games))
