# StarCraft 2 Battle Simulator

A terminal-based application that simulates battles between basic StarCraft 2 units (Zerglings, Marines, and Zealots).

## Features

- Select and configure armies with different unit compositions
- Simulate battles between two armies
- View detailed battle results including:
  - Winner determination
  - Battle duration
  - Remaining units
  - HP statistics

## Units

The simulator includes the following basic StarCraft 2 units:

| Unit      | HP  | Damage | Attack Speed | DPS  | Cost |
|-----------|-----|--------|--------------|------|------|
| Zergling  | 35  | 5      | 1.5          | 7.5  | 25   |
| Marine    | 45  | 6      | 0.86         | 5.2  | 50   |
| Zealot    | 100 | 8      | 0.86         | 6.9  | 100  |

## How to Run

```bash
go run .
```

Or build and run the executable:

```bash
go build
./sc2battlesim
```

## Controls

- **Tab/Shift+Tab**: Navigate between input fields
- **Up/Down**: Navigate between input fields
- **Enter**: Run the battle simulation
- **R**: Reset the inputs
- **Q**: Quit the application

## Battle Simulation

The battle simulation uses a simplified model that considers:
- Total HP of each army
- Total DPS (Damage Per Second) of each army
- Time to defeat calculation

The winner is determined by which army would defeat the other first, based on their total HP and DPS values.

## Example

1. Configure Army 1 with 10 Zerglings, 5 Marines, and 2 Zealots
2. Configure Army 2 with 20 Zerglings, 10 Marines, and 0 Zealots
3. Press Enter to run the simulation
4. View the results to see which army would win and how many units would remain

## Implementation Details

This application is built using:
- Go programming language
- [Bubble Tea](https://github.com/charmbracelet/bubbletea) - A TUI framework for Go
- [Bubbles](https://github.com/charmbracelet/bubbles) - Common UI components for Bubble Tea
- [Lipgloss](https://github.com/charmbracelet/lipgloss) - Styling for terminal applications