import math
import random
import sys
import pygame
# honestly when i wrote the code , only god and i knew what it works , now only god knows , if you do understand the code you have my respect hahahah
W, H = 900, 700
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("air traffic collision avoidance (TCAS-style)")
font = pygame.font.SysFont("consolas", 16)
clock = pygame.time.Clock()

SAFE_DIST = 90        # planes closer than this are a conflict
LOOKAHEAD = 40        # frames ahead we predict positions


class Plane:
    _id = 0
    def __init__(self):
        
        edge = random.choice("LRTB")
        if edge == "L": self.x, self.y, ang = 0, random.uniform(0, H), 0
        elif edge == "R": self.x, self.y, ang = W, random.uniform(0, H), math.pi
        elif edge == "T": self.x, self.y, ang = random.uniform(0, W), 0, math.pi / 2
        else: self.x, self.y, ang = random.uniform(0, W), H, -math.pi / 2
        ang += random.uniform(-0.5, 0.5)
        self.vx, self.vy = math.cos(ang) * 2.2, math.sin(ang) * 2.2
        Plane._id += 1
        self.id = Plane._id
        self.conflict = False

    def future(self, t):
        return self.x + self.vx * t, self.y + self.vy * t


planes = [Plane() for _ in range(7)]


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


running = True
frame = 0
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    frame += 1
    for p in planes:
        p.conflict = False

    
    for i in range(len(planes)):
        for j in range(i + 1, len(planes)):
            a, b = planes[i], planes[j]
            
            closest = min(dist(a.future(t), b.future(t)) for t in range(LOOKAHEAD))
            if closest < SAFE_DIST:
                a.conflict = b.conflict = True
                ax, ay = a.x - b.x, a.y - b.y
                d = math.hypot(ax, ay) or 1
                a.vx += ax / d * 0.06
                a.vy += ay / d * 0.06
                b.vx -= ax / d * 0.06
                b.vy -= ay / d * 0.
                for pl in (a, b):
                    s = math.hypot(pl.vx, pl.vy)
                    pl.vx, pl.vy = pl.vx / s * 2.2, pl.vy / s * 2.2

    # move + respawn planes that leave the screen
    for k, p in enumerate(planes):
        p.x += p.vx
        p.y += p.vy
        if p.x < -20 or p.x > W + 20 or p.y < -20 or p.y > H + 20:
            planes[k] = Plane()

    # obviously we need a radar display lol
    screen.fill((6, 18, 12))
    for r in range(80, max(W, H), 80):
        pygame.draw.circle(screen, (16, 46, 30), (W // 2, H // 2), r, 1)
    pygame.draw.line(screen, (16, 46, 30), (W // 2, 0), (W // 2, H))
    pygame.draw.line(screen, (16, 46, 30), (0, H // 2), (W, H // 2))

    for i in range(len(planes)):
        for j in range(i + 1, len(planes)):
            a, b = planes[i], planes[j]
            if a.conflict and b.conflict and dist((a.x, a.y), (b.x, b.y)) < SAFE_DIST * 1.6:
                pygame.draw.line(screen, (220, 60, 60), (a.x, a.y), (b.x, b.y), 1)

    for p in planes:
        col = (255, 90, 90) if p.conflict else (90, 230, 140)
        ang = math.atan2(p.vy, p.vx)
        tip = (p.x + 12 * math.cos(ang), p.y + 12 * math.sin(ang))
        l = (p.x + 7 * math.cos(ang + 2.5), p.y + 7 * math.sin(ang + 2.5))
        r = (p.x + 7 * math.cos(ang - 2.5), p.y + 7 * math.sin(ang - 2.5))
        pygame.draw.polygon(screen, col, [tip, l, r])
        if p.conflict:
            pygame.draw.circle(screen, (220, 60, 60), (int(p.x), int(p.y)), int(SAFE_DIST / 2), 1)

    conflicts = sum(p.conflict for p in planes) // 2
    screen.blit(font.render(f"aircraft: {len(planes)}   active conflicts: {conflicts}", True, (140, 230, 170)), (14, 14))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
