from manim import *
import random
import numpy as np

config.background_opacity = 0


# Variables to tweak easily
NODE_RADIUS = 0.15  # Increased node size by 50% (0.1 to 0.15)
PADDING = 2         # Added padding to ensure nodes are not too close to the edges
FRAME_WIDTH = 8     # Width of the frame (used for padding)
FRAME_HEIGHT = 6    # Height of the frame to use more vertical space
SEED_VALUE = 42     # Seed for reproducibility
SHIFT_Y = 2         # Shift the entire graph upwards by 2 units
NUM_ATTEMPTS = 30   # Number of search attempts to visualize
ANIMATION_SPEED = 0.5  # Global speed multiplier for animations (can be adjusted)
DISTANCE_MULTIPLIER = 3  # Multiplier for edge distances
INTRODUCTION_SPEED = 1.0  # Speed of initial graph construction

class TSPAnimation(Scene):
    def construct(self):
        # Fixed seed for reproducibility
        random.seed(SEED_VALUE)
        np.random.seed(SEED_VALUE)

        # Create the 10 city graph
        num_cities = 10
        
        # Random positions for the cities, with adjusted vertical spacing and wider distribution
        positions = [
            np.array([random.uniform(-FRAME_WIDTH + PADDING, FRAME_WIDTH - PADDING),
                      random.uniform(-FRAME_HEIGHT + PADDING, FRAME_HEIGHT - PADDING), 0]) 
            for _ in range(num_cities)
        ]
        
        # Select two random cities for start and end
        start_city_index = random.randint(0, num_cities - 1)
        end_city_index = random.randint(0, num_cities - 1)
        while start_city_index == end_city_index:  # Ensure start and end cities are different
            end_city_index = random.randint(0, num_cities - 1)

        # Set the start and end city positions
        positions[start_city_index] = np.array([-FRAME_WIDTH + PADDING, 0, 0])  # Far left
        positions[end_city_index] = np.array([FRAME_WIDTH - PADDING, 0, 0])    # Far right

        # Shift the positions up
        shift_vector = UP * SHIFT_Y

        # Create the lines connecting cities (edges)
        edges = []
        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                edge = Line(positions[i] + shift_vector, positions[j] + shift_vector, color=GREY_A, stroke_width=5)
                edges.append(edge)
        
        # Animate edges gradually
        for edge in edges:
            self.play(Create(edge), run_time=0.1 * INTRODUCTION_SPEED)

        # Create the nodes
        cities = []
        for i in range(num_cities):
            city = Dot(radius=NODE_RADIUS, color=BLUE)
            city.move_to(positions[i] + shift_vector)
            cities.append(city)
            
            # Special coloring for start and end cities
            if i == start_city_index:
                city.set_color(GREEN)
            elif i == end_city_index:
                city.set_color(YELLOW)
            
            # Animate the appearance of each city
            self.play(Create(city), run_time=0.3 * INTRODUCTION_SPEED)

        self.wait(1 * INTRODUCTION_SPEED)

        # Calculate distances
        def calculate_distance(p1, p2):
            return np.linalg.norm(p1 - p2) * DISTANCE_MULTIPLIER
        
        distances = {}
        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                dist = calculate_distance(positions[i], positions[j])
                distances[(i, j)] = dist
                distances[(j, i)] = dist
        
        # Create a label for each edge to show the distance
        # distance_labels = {}
        # for (i, j), dist in distances.items():
        #     label = Tex(f"{int(dist)}", color=BLUE).scale(0.5)
        #     label.move_to((positions[i] + positions[j]) / 2 + shift_vector)
        #     distance_labels[(i, j)] = label
        #     self.play(Write(label), run_time=0.1 * INTRODUCTION_SPEED)

        # Cumulative distance display
        cumulative_dist_text = Tex("0", color=YELLOW).scale(1).to_edge(UP)
        self.add(cumulative_dist_text)

        # Run the search process multiple times
        for attempt in range(NUM_ATTEMPTS):
            # Reset for each attempt
            current_node = start_city_index
            path = []
            visited_nodes = set([current_node])
            current_total_distance = 0  # Reset distance for each search
            
            # Store the path lines to fade out later
            path_lines = []
            
            # Keep going until we reach the destination node
            while current_node != end_city_index:
                # Get unvisited neighbors
                neighbors = [i for i in range(num_cities) if i != current_node and i not in visited_nodes]
                if not neighbors:
                    break

                # Pick a random connected node
                next_node = random.choice(neighbors)
                path.append((current_node, next_node))

                # Create the path between nodes BEFORE adding nodes
                search_path = Line(cities[current_node].get_center(), 
                                   cities[next_node].get_center(), 
                                   color=RED, 
                                   stroke_width=5)  # Thicker line to stand out
                path_lines.append(search_path)
                
                # Add path line with speed-adjusted animation
                self.play(Create(search_path), run_time=0.3 * ANIMATION_SPEED)

                # Update the current attempt distance
                dist = distances[(current_node, next_node)]
                current_total_distance += dist
                
                # Update cumulative distance display for current search
                cumulative_dist_text.become(Tex(f"{int(current_total_distance)}", color=YELLOW).scale(1).to_edge(UP))
                
                # Now add the nodes AFTER drawing the path
                self.add(cities[current_node])
                self.add(cities[next_node])

                # Highlight current nodes
                cities[start_city_index].set_color(GREEN)  # Start node always green
                cities[end_city_index].set_color(YELLOW)   # End node always yellow
                cities[current_node].set_color(GREEN)      # Current node is green
                cities[next_node].set_color(RED)           # Next node is red

                self.wait(0.3 * ANIMATION_SPEED)

                # Move to the next node
                current_node = next_node
                visited_nodes.add(current_node)

            # Simulate full path traversal if destination reached
            if current_node == end_city_index:
                # Reset node colors
                for city in cities:
                    city.set_color(BLUE)
                cities[start_city_index].set_color(GREEN)
                cities[end_city_index].set_color(YELLOW)
                
                # Keep the path lines visible for this attempt
                self.wait(0.5 * ANIMATION_SPEED)
                
                # Fade out the path lines faster
                self.play(*[FadeOut(line, run_time=0.3 * ANIMATION_SPEED) for line in path_lines])
                
                # Reset cumulative distance to 0 for next search
                cumulative_dist_text.become(Tex("0", color=YELLOW).scale(1).to_edge(UP))
            
            self.wait(0.3 * ANIMATION_SPEED)

        # End the animation
        self.wait(2)