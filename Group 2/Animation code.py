from manim import *

class TowerOfHanoi(Scene):
    def construct(self):
        n = 5  # number of disks

        rods = self.create_rods()
        disks, stacks = self.create_disks(n, rods[0])

        self.add(rods)
        self.add(*disks)
        self.wait()

        moves = self.hanoi(n, 0, 2)
        for src, dst in moves:
            self.move_disk(stacks, rods, src, dst)

        self.wait()

    # ----------------- Hanoi logic -----------------

    def hanoi(self, n, start, end):
        if n == 1:
            return [(start, end)]
        other = 3 - (start + end)
        return (
            self.hanoi(n - 1, start, other)
            + [(start, end)]
            + self.hanoi(n - 1, other, end)
        )

    # ----------------- Scene helpers -----------------

    def create_rods(self):
        base = Rectangle(width=9, height=0.3, color=WHITE,fill_opacity=1)
        base.set_color=WHITE
        base.shift(DOWN * 3)

        rods = VGroup()
        for x in [-3, 0, 3]:
            rod = Rectangle(width=0.2, height=4, color=WHITE,fill_opacity=1)
            rod.shift(base.get_top() + UP * (2+base.stroke_width/100) + RIGHT * x)
            rods.add(rod)

        return VGroup(*rods, base)

    def create_disks(self, n, rod):
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        disks = []
        stacks = [[], [], []]

        width = 2.5
        height = 0.3
        for i in range(n):
            disk = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.15,
                fill_opacity=1,
                fill_color=colors[i % len(colors)],
            )
            disk.move_to(
                rod.get_bottom() + UP * (0.15 + i * 0.3)
            )
            disks.append(disk)
            stacks[0].append(disk)
            width -= 0.3

        return disks, stacks

    def move_disk(self, stacks, rods, src, dst):
        disk = stacks[src].pop()

        lift = disk.animate.shift(UP * 2)
        move = disk.animate.move_to(
            rods[dst].get_bottom() + UP * 0.045
        )

        if stacks[dst]:
            move = disk.animate.next_to(stacks[dst][-1], UP, buff=0)

        self.play(lift, run_time=0.3)
        self.play(move, run_time=0.5)

        stacks[dst].append(disk)
