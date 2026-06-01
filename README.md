# Air Traffic Collision Avoidance (TCAS-style)

A simplified version of the TCAS system real planes use. Aircraft fly across the
sky on different headings, and the system constantly checks every pair of planes.
If two are *predicted* to get too close, it flags a conflict (red) and nudges
them apart so they don't collide. Shown on a radar-style display.

## how it works

- each plane's position is projected ~40 frames into the future
- for every pair, find the closest they'll get
- if that's under the safe distance → conflict → apply an avoidance vector that
  pushes them apart while keeping their cruise speed
- red rings/lines show conflicts being actively resolved

## run

```bash
pip install pygame
python sim.py
```

tags: ai, aviation, collision-avoidance, simulation, pygame, safety

predicting the future positions and steering away before it happens is the whole trick.
