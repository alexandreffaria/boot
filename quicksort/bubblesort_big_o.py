from manim import *

class BubbleSortBigO(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 10],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN)

        # Labels for axes
        x_label = axes.get_x_axis_label("n")
        y_label = axes.get_y_axis_label("Time")

        self.play(Create(axes), run_time=.5)
        self.play(Write(x_label), Write(y_label), run_time=1)

        # Define O(n^2)
        n_squared = lambda x: x ** 2
        graph = axes.plot(n_squared, color=RED, x_range=[0, 10])

        # Label near the top right
        label = Tex(r"$O(n^2)$")
        label.to_corner(UP + RIGHT)


        # Animate it
        self.play(Create(graph),Write(label.set_color(RED)), run_time=3)
        self.wait(2)
