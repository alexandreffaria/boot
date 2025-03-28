from manim import *
import numpy as np

class BigOScene(MovingCameraScene):
    def construct(self):
        # Set the background to transparent
        self.camera.background_color = None
        # Scale the camera frame down by 0.8333 so that everything appears 20% larger.
        self.camera.frame.scale(0.8)

        # Define the functions
        f_const = lambda x: 1
        f_log   = lambda x: np.log2(x+1)  # log base 2 for demonstration
        f_n     = lambda x: x
        f_n2    = lambda x: x**2
        f_n3    = lambda x: x**3

        # Stage 1: Axes for O(1), O(log n), O(n)
        axes1 = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 25, 5],
            x_length=8,
            y_length=4.5,
            tips=False,
        )
        x_label = axes1.get_x_axis_label("n")
        y_label = axes1.get_y_axis_label("f(n)")
        x_label.next_to(axes1.x_axis, RIGHT)
        y_label.next_to(axes1.y_axis, UP)

        # Stage 2: Axes for O(n^2) (n^2 at n=20 is 400)
        axes2 = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 400, 50],
            x_length=8,
            y_length=4.5,
            tips=False,
        )

        # Stage 3: Axes for O(n^3) (n^3 at n=20 is 8000)
        axes3 = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 8000, 1000],
            x_length=8,
            y_length=4.5,
            tips=False,
        )

        # Plot curves on the initial axes (axes1)
        graph1_const = axes1.plot(f_const, color=BLUE, x_range=[0, 20])
        graph1_log   = axes1.plot(f_log,   color=GREEN, x_range=[0, 20])
        graph1_n     = axes1.plot(f_n,     color=RED,   x_range=[0, 20])

        # Re-plot curves on axes2 for the next stage
        graph2_const = axes2.plot(f_const, color=BLUE, x_range=[0, 20])
        graph2_log   = axes2.plot(f_log,   color=GREEN, x_range=[0, 20])
        graph2_n     = axes2.plot(f_n,     color=RED,   x_range=[0, 20])
        graph2_n2    = axes2.plot(f_n2,    color=YELLOW, x_range=[0, 20])

        # Re-plot curves on axes3 for the final stage
        graph3_const = axes3.plot(f_const, color=BLUE, x_range=[0, 20])
        graph3_log   = axes3.plot(f_log,   color=GREEN, x_range=[0, 20])
        graph3_n     = axes3.plot(f_n,     color=RED,   x_range=[0, 20])
        graph3_n2    = axes3.plot(f_n2,    color=YELLOW, x_range=[0, 20])
        graph3_n3    = axes3.plot(f_n3,    color=ORANGE, x_range=[0, 20])

        # Stage A: Show axes1 and the first three curves.
        self.play(Create(axes1), FadeIn(x_label), FadeIn(y_label))
        self.wait(0.5)
        self.play(Create(graph1_const))
        self.wait(1.5)
        self.play(Create(graph1_log))
        self.wait(2.1)
        self.play(Create(graph1_n))
        self.wait(1)

        # Stage B: Transform to axes2 and add the O(n^2) curve.
        self.play(
            Transform(axes1, axes2),
            Transform(graph1_const, graph2_const),
            Transform(graph1_log,   graph2_log),
            Transform(graph1_n,     graph2_n),
        )
        # self.wait(1)
        self.play(Create(graph2_n2))
        # self.wait(1)

        # Stage C: Transform to axes3 and add the O(n^3) curve.
        self.play(
            Transform(axes1, axes3),  # 'axes1' is our current displayed axes
            Transform(graph1_const, graph3_const),
            Transform(graph1_log,   graph3_log),
            Transform(graph1_n,     graph3_n),
            Transform(graph2_n2,    graph3_n2),
        )
        # self.wait(1)
        self.play(Create(graph3_n3))
        # self.wait(2)
