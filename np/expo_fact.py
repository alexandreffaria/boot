from manim import *
import numpy as np
import math

class BigOScene(MovingCameraScene):
    def construct(self):
        # Set the background to transparent and scale the camera frame.
        self.camera.background_color = None
        self.camera.frame.scale(0.8)

        #####################################################
        # Part 1: Classic Big-O Functions
        #####################################################
        # Define functions for the classic stage.
        f_const = lambda x: 1
        f_log   = lambda x: np.log2(x+1)
        f_n     = lambda x: x
        f_n2    = lambda x: x**2
        f_n3    = lambda x: x**3

        # Axes for Stage A: O(1), O(log n), O(n)
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

        # Axes for Stage B: To reveal O(n²) (up to 400)
        axes2 = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 400, 50],
            x_length=8,
            y_length=4.5,
            tips=False,
        )

        # Axes for Stage C: To reveal O(n³) (up to 8000)
        axes3 = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 8000, 1000],
            x_length=8,
            y_length=4.5,
            tips=False,
        )

        # Plot curves on axes1.
        graph1_const = axes1.plot(f_const, color=BLUE, x_range=[0, 20])
        graph1_log   = axes1.plot(f_log,   color=GREEN, x_range=[0, 20])
        graph1_n     = axes1.plot(f_n,     color=RED,   x_range=[0, 20])

        # Plot O(n²) on axes2.
        graph2_const = axes2.plot(f_const, color=BLUE, x_range=[0, 20])
        graph2_log   = axes2.plot(f_log,   color=GREEN, x_range=[0, 20])
        graph2_n     = axes2.plot(f_n,     color=RED,   x_range=[0, 20])
        graph2_n2    = axes2.plot(f_n2,    color=YELLOW, x_range=[0, 20])

        # Plot O(n³) on axes3.
        graph3_const = axes3.plot(f_const, color=BLUE, x_range=[0, 20])
        graph3_log   = axes3.plot(f_log,   color=GREEN, x_range=[0, 20])
        graph3_n     = axes3.plot(f_n,     color=RED,   x_range=[0, 20])
        graph3_n2    = axes3.plot(f_n2,    color=YELLOW, x_range=[0, 20])
        graph3_n3    = axes3.plot(f_n3,    color=ORANGE, x_range=[0, 20])

        # Stage A: Show axes1 and the first three curves.
        self.play(Create(axes1), FadeIn(x_label), FadeIn(y_label))
        self.wait(0.5)
        self.play(Create(graph1_const), run_time=1)
        self.play(Create(graph1_log), run_time=1)
        self.play(Create(graph1_n), run_time=1)
        self.wait(1)

        # Stage B: Transform to axes2 and add O(n²).
        self.play(
            Transform(axes1, axes2),
            Transform(graph1_const, graph2_const),
            Transform(graph1_log,   graph2_log),
            Transform(graph1_n,     graph2_n),
        )
        self.play(Create(graph2_n2), run_time=1)
        self.wait(1)

        # Stage C: Transform to axes3 and add O(n³).
        self.play(
            Transform(axes1, axes3),
            Transform(graph1_const, graph3_const),
            Transform(graph1_log,   graph3_log),
            Transform(graph1_n,     graph3_n),
            ReplacementTransform(graph2_n2, graph3_n2),  # Use ReplacementTransform here
        )
        self.play(Create(graph3_n3), run_time=1)
        self.wait(1)

        #####################################################
        # Part 2: Exponential vs. Factorial
        #####################################################
        # Define new functions.
        f_exp = lambda x: 2**x
        f_fact = lambda x: math.gamma(x+1)  # n! = Gamma(n+1)

        # Stage D: Zoom out for O(2^n).
        # Create new axes for the exponential function.
        axes4 = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 1.2e6, 200000],  # 2^20 ≈ 1e6; a little extra room.
            x_length=8,
            y_length=4.5,
            tips=False,
        )
        # Plot the exponential curve on axes4.
        graph_exp = axes4.plot(f_exp, color=PURPLE, x_range=[0, 20])

        # Transform from the current classic view (axes3) to the exponential axes.
        self.play(
            Transform(axes1, axes4),
            # Re-plot the classic curves on axes4 for a smooth transition.
            Transform(graph3_const, axes4.plot(f_const, color=BLUE, x_range=[0, 20])),
            Transform(graph3_log,   axes4.plot(f_log, color=GREEN, x_range=[0, 20])),
            Transform(graph3_n,     axes4.plot(f_n, color=RED, x_range=[0, 20])),
            Transform(graph3_n2,    axes4.plot(f_n2, color=YELLOW, x_range=[0, 20])),
            Transform(graph3_n3,    axes4.plot(f_n3, color=ORANGE, x_range=[0, 20])),
        )
        # Now add the exponential curve.
        self.play(Create(graph_exp), run_time=2)
        self.wait(2)

        # Stage E: Zoom out further for O(n!).
        # For clarity, restrict the domain for factorial to 0–10.
        axes5 = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 4e6, 500000],  # 10! is ~3.6e6; a bit of extra headroom.
            x_length=8,
            y_length=4.5,
            tips=False,
        )
        # Plot the exponential curve on axes5 (re-plotted on the new domain).
        graph_exp_new = axes5.plot(f_exp, color=PURPLE, x_range=[0, 10])
        # Plot the factorial curve on axes5.
        graph_fact = axes5.plot(f_fact, color=GOLD, x_range=[0, 10])

        # Transform from the exponential axes to the factorial axes.
        self.play(
            Transform(axes1, axes5),
            Transform(graph_exp, graph_exp_new),
        )
        # Now add the factorial curve.
        self.play(Create(graph_fact), run_time=2)
        self.wait(2)
