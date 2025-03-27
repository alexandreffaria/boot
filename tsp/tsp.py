from manim import *
import numpy as np
import random

class TSPScene1(Scene):
    def construct(self):
        # Fix the random seed for consistent layout
        random.seed(5)

        num_cities = 10
        min_dist = 1.0   # Minimum spacing between any two cities
        offset_label = 0 # Offset labels from edges
        shadow_offset = 0.01
        shadow_opacity = 0.85

        # Hardcoded distances for each edge (must match num_cities in length)
        distances = [21, 56, 46, 55, 49, 31, 38, 37, 28, 10]

        # Create VGroups for edges, labels, and city dots
        edges = VGroup()
        labels = VGroup()
        city_dots = VGroup()

        # Define a discrete grid of possible (x, y) points to pick from
        possible_x = list(range(-6, 7))  # -6..6
        possible_y = list(range(-3, 4))  # -3..3
        grid_positions = [
            np.array([float(x), float(y), 0])
            for x in possible_x
            for y in possible_y
        ]

        # Shuffle the grid so we pick random positions
        random.shuffle(grid_positions)

        # We'll store final chosen positions here
        positions = []
        # Pick positions from the grid until we have num_cities (or run out)
        for candidate_pos in grid_positions:
            if all(np.linalg.norm(candidate_pos - p) >= min_dist for p in positions):
                positions.append(candidate_pos)
                if len(positions) == num_cities:
                    break

        # Create Dot objects for each city
        for pos in positions:
            dot = Dot(point=pos, radius=0.2)
            city_dots.add(dot)

        # Identify leftmost (start) and rightmost (destination)
        x_positions = [p[0] for p in positions]
        leftmost_index = np.argmin(x_positions)
        rightmost_index = np.argmax(x_positions)

        # Color the start (leftmost) and destination (rightmost)
        city_dots[leftmost_index].set_color(GREEN)
        city_dots[rightmost_index].set_color(YELLOW)

        # Control layering
        edges.set_z_index(0)
        city_dots.set_z_index(1)
        labels.set_z_index(2)  # Labels (and shadows) on top

        # Animate city dots
        self.play(FadeIn(city_dots), run_time=2)
        self.wait(1)

        # Connect adjacent nodes in a loop, labeling with the hardcoded distances
        for i in range(num_cities):
            j = (i + 1) % num_cities
            start = positions[i]
            end = positions[j]

            # Create the edge in a darker grey
            edge = Line(start, end).set_color(GREY_E)
            edges.add(edge)

            # Pull distance from the hardcoded list
            distance_int = distances[i]

            # Create the main label
            distance_label = Tex(str(distance_int)).scale(0.8)
            distance_label.set_color(BLUE)  # Default Manim BLUE
            midpoint = (start + end) / 2
            distance_label.move_to(midpoint)

            # Offset the label perpendicular to the line
            direction_vector = np.array([end[1] - start[1], -(end[0] - start[0]), 0])
            norm = np.linalg.norm(direction_vector)
            if norm != 0:
                direction_vector = (direction_vector / norm) * offset_label
                distance_label.shift(direction_vector)

            # Drop shadow
            shadow = distance_label.copy()
            shadow.set_color(BLACK)
            shadow.set_opacity(shadow_opacity)
            shadow.scale(1.1)  # Make the shadow slightly larger
            # Shift the shadow slightly to mimic a light source
            shadow.shift(shadow_offset * (RIGHT + DOWN))

            shadow.set_z_index(2)
            distance_label.set_z_index(3)

            # Add both shadow and label to labels group
            labels.add(shadow, distance_label)

        # Animate edges behind the dots
        self.play(LaggedStartMap(Create, edges, lag_ratio=0.1), run_time=3)
        self.wait(1)

        # Animate labels
        self.play(LaggedStartMap(Write, labels, lag_ratio=0.1), run_time=3)
        self.wait(2)
