from manim import *
import math

class QuicksortBigO(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=[0, 100, 10],
            y_range=[0, 500, 50],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN)

        # Labels for axes
        x_label = axes.get_x_axis_label("n")
        y_label = axes.get_y_axis_label("Time")

        self.play(Create(axes), run_time=2)
        self.play(Write(x_label), Write(y_label), run_time=1.5)

        # Define the function O(n log n)
        n_log_n = lambda x: x * math.log(x)
        nlogn_graph = axes.plot(n_log_n, color=BLUE, x_range=[1, 100])
        
        # Position label in the top right
        label = Tex(r"$O(n \log n)$")
        label.to_corner(UP + RIGHT)

        # Animate the graph and label
        self.play(Create(nlogn_graph), Write(label.set_color(BLUE)), run_time=3)
        self.wait(2)
