from manim import *
import numpy as np
import math

class BigOAnimation(MovingCameraScene):
    def construct(self):
        # 1) Create a ValueTracker for the y-axis maximum.
        y_max_tracker = ValueTracker(20)

        # 2) Define Axes that update automatically with y_max_tracker.
        axes = always_redraw(
            lambda: Axes(
                x_range=[1, 6, 1],
                # y_range from 0 up to current y_max, with tick step = y_max/4
                y_range=[0, y_max_tracker.get_value(), y_max_tracker.get_value() / 4],
                x_length=10,
                y_length=6,
                axis_config={"include_numbers": True},
            )
        )
        axes_labels = always_redraw(
            lambda: axes.get_axis_labels(x_label="n", y_label="f(n)")
        )

        # 3) Animate creation of the Axes and labels.
        self.play(Create(axes), Write(axes_labels))

        # 4) Prepare an overall legend in the top-right corner (one label per curve).
        overall_legend = VGroup(
            Tex("$O(1)$", color=RED).scale(0.5),
            Tex("$O(\\log n)$", color=BLUE).scale(0.5),
            Tex("$O(n)$", color=GREEN).scale(0.5),
            Tex("$O(n\\log n)$", color=YELLOW).scale(0.5),
            Tex("$O(n^2)$", color=ORANGE).scale(0.5),
            Tex("$O(2^n)$", color=TEAL).scale(0.5),
            Tex("$O(n^3)$", color=PURPLE).scale(0.5),
            Tex("$O(n!)$", color=MAROON).scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
        # If you see errors about set_fixed_in_frame in Manim 0.19+, just remove this line:
        # overall_legend.set_fixed_in_frame(True)

        # 5) Define the functions
        f_const      = lambda x: 1
        f_log        = lambda x: np.log(x)
        f_linear     = lambda x: x
        f_nlogn      = lambda x: x * np.log(x)
        f_quadratic  = lambda x: x**2
        f_exponential= lambda x: 2**x
        f_cubic      = lambda x: x**3
        f_factorial  = lambda x: math.gamma(x+1)

        # 6) Create always_redraw curves but do NOT animate them yet.
        #    We'll animate their stroke from 0 to normal, so they look "drawn."
        graph_const  = always_redraw(lambda: axes.plot(f_const, x_range=[1,6], color=RED))
        graph_log    = always_redraw(lambda: axes.plot(f_log, x_range=[1,6], color=BLUE))
        graph_linear = always_redraw(lambda: axes.plot(f_linear, x_range=[1,6], color=GREEN))
        graph_nlogn  = always_redraw(lambda: axes.plot(f_nlogn, x_range=[1,6], color=YELLOW))
        graph_quad   = always_redraw(lambda: axes.plot(f_quadratic, x_range=[1,6], color=ORANGE))
        graph_exp    = always_redraw(lambda: axes.plot(f_exponential, x_range=[1,6], color=TEAL))
        graph_cubic  = always_redraw(lambda: axes.plot(f_cubic, x_range=[1,6], color=PURPLE))
        graph_fact   = always_redraw(lambda: axes.plot(f_factorial, x_range=[1,6], color=MAROON))

        # 7) Add all curves to the scene so they keep updating with always_redraw.
        #    We'll animate their stroke to make them appear.
        self.add(graph_const, graph_log, graph_linear, graph_nlogn,
                 graph_quad, graph_exp, graph_cubic, graph_fact)

        # Initially set each curve's stroke width to 0 so it's invisible.
        for g in (graph_const, graph_log, graph_linear, graph_nlogn,
                  graph_quad, graph_exp, graph_cubic, graph_fact):
            g.set_stroke(width=0)

        # --- Draw slow curves (O(1), O(log n), O(n), O(n log n)) one by one ---
        self.play(
            graph_const.animate.set_stroke(width=4),
            FadeIn(overall_legend[0]),
            run_time=1
        )
        self.play(
            graph_log.animate.set_stroke(width=4),
            FadeIn(overall_legend[1]),
            run_time=1
        )
        self.play(
            graph_linear.animate.set_stroke(width=4),
            FadeIn(overall_legend[2]),
            run_time=1
        )
        self.play(
            graph_nlogn.animate.set_stroke(width=4),
            FadeIn(overall_legend[3]),
            run_time=1
        )
        self.wait()

        # --- First zoom step:  y_max: 20 -> 100 ---
        self.play(y_max_tracker.animate.set_value(100), run_time=2)
        self.wait()

        # --- Draw first two fast curves (O(n^2), O(2^n)) ---
        self.play(
            graph_quad.animate.set_stroke(width=4),
            FadeIn(overall_legend[4]),
            run_time=1
        )
        self.play(
            graph_exp.animate.set_stroke(width=4),
            FadeIn(overall_legend[5]),
            run_time=1
        )
        self.wait()

        # --- Second zoom step: y_max: 100 -> 800 ---
        self.play(y_max_tracker.animate.set_value(800), run_time=2)
        self.wait()

        # --- Draw final two fast curves (O(n^3), O(n!)) ---
        self.play(
            graph_cubic.animate.set_stroke(width=4),
            FadeIn(overall_legend[6]),
            run_time=1
        )
        self.play(
            graph_fact.animate.set_stroke(width=4),
            FadeIn(overall_legend[7]),
            run_time=1
        )
        self.wait(2)
