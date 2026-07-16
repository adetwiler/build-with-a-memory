# Credits

This method is mostly my own research and practice, but not all of it. Where an idea came from someone else, I name them here.

## The mindset shift

The push that got this whole thing going was an hour-long talk by **Matt Pocock** ([aihero.dev](https://www.aihero.dev)) about how he works with AI coding agents. I had been toying with the idea of committing project memory for a while, but that talk flipped how I thought about it. It stopped being a loose habit and became a real way of working, and it is the reason I can run several projects at once now instead of losing the thread on all of them. The memory network in this repo grew out of that shift.

## Grilling the decisions (pillar 5)

Adapted from **Matt Pocock's `grill-with-docs` skill** ([mattpocock/skills](https://github.com/mattpocock/skills), [aihero.dev/skills](https://www.aihero.dev/skills)).

I changed how it works to fit how I build: every question is one tap-to-pick prompt that carries my recommended answer, and the session ends by writing an ADR that names the alternatives it beat. That reshaping is the point of this whole repo, so take it and bend it to your own workflow rather than adopting mine as-is.

(Pocock's `wayfinder` skill orchestrates over grill-with-docs for work too big for one session. I do not use it here, but it is worth a look.)

## Everything else

The judge-panel pillar (pillar 6) is grounded in the LLM-as-judge reliability literature, cited in [`research/landscape-2026.md`](research/landscape-2026.md). The rest of the pillars come from my own work building with agents day to day, and where they sit next to other people's tools that is mapped in the same research shelf. If you find a place where this borrows an idea I have not credited, tell me and I will fix it here.
