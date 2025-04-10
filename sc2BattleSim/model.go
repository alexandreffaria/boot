package main

import (
	"fmt"
	"strconv"
	"time"

	"github.com/charmbracelet/lipgloss"

	"github.com/charmbracelet/bubbles/list"
	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"

	"sc2battlesim/battle"
	"sc2battlesim/units"
)

// Define the different states our UI can be in.
type state int

const (
	stateSetupP1Race state = iota
	stateSetupP1Count
	stateSetupP2Race
	stateSetupP2Count
	stateSetupMultiplier
	stateBattle
	stateEnd
)

// model holds our TUI state.
type model struct {
	state state

	// For text entry.
	textInput textinput.Model

	// For race selection.
	raceList list.Model

	// Setup values.
	player1Race  string
	player2Race  string
	player1Count int
	player2Count int
	multiplier   float64

	// Battle simulation.
	simulator *battle.BattleSimulator
	battleLog []string
}

// raceItem implements list.Item interface so we can display our race choices.
type raceItem string

func (r raceItem) Title() string { return string(r) }
func (r raceItem) Description() string {
	switch r {
	case "zerg":
		return "Zerglings"
	case "terran":
		return "Marines"
	case "protoss":
		return "Zealots"
	default:
		return ""
	}
}
func (r raceItem) FilterValue() string { return string(r) }

// initialModel initializes our model with both a text input and a list for race selection.
func initialModel() model {
	// Initialize text input.
	ti := textinput.New()
	ti.Placeholder = "Enter value"
	ti.Focus()
	ti.CharLimit = 20
	ti.Width = 30

	// Prepare a list of race options.
	items := []list.Item{
		raceItem("zerg"),
		raceItem("terran"),
		raceItem("protoss"),
	}
	// Create the list with a default size.
	const defaultWidth = 20
	rl := list.New(items, list.NewDefaultDelegate(), defaultWidth, 5)
	rl.Title = "Select Race"
	rl.SetShowStatusBar(false)
	rl.SetFilteringEnabled(false)
	rl.DisableQuitKeybindings()

	return model{
		state:     stateSetupP1Race,
		textInput: ti,
		raceList:  rl,
		battleLog: []string{},
	}
}

func (m model) Init() tea.Cmd {
	// In our initial states we want to update the list or text input.
	switch m.state {
	case stateSetupP1Race, stateSetupP2Race:
		return nil
	default:
		return textinput.Blink
	}
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd

	switch m.state {
	// --- Player 1 Race Selection ---
	case stateSetupP1Race:
		// Delegate updates to the list component.
		m.raceList, cmd = m.raceList.Update(msg)
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			if selectedItem := m.raceList.SelectedItem(); selectedItem != nil {
				m.player1Race = string(selectedItem.(raceItem))
				// Switch to text input for unit count.
				m.textInput.SetValue("")
				m.textInput.Placeholder = fmt.Sprintf("Enter number of %s", unitNameForRace(m.player1Race))
				m.state = stateSetupP1Count
				// Reset the list for next use.
				m.raceList.Select(0)
			}
		}
		return m, cmd

	// --- Player 1 Unit Count ---
	case stateSetupP1Count:
		m.textInput, cmd = m.textInput.Update(msg)
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			count, err := strconv.Atoi(m.textInput.Value())
			if err != nil || count <= 0 {
				m.battleLog = append(m.battleLog, "Invalid number for Player 1. Please enter a positive integer.")
				m.textInput.SetValue("")
				return m, nil
			}
			m.player1Count = count
			// Set up for Player 2 race selection.
			m.raceList.SetItems([]list.Item{
				raceItem("zerg"),
				raceItem("terran"),
				raceItem("protoss"),
			})
			m.raceList.Select(0)
			m.state = stateSetupP2Race
		}
		return m, cmd

	// --- Player 2 Race Selection ---
	case stateSetupP2Race:
		m.raceList, cmd = m.raceList.Update(msg)
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			if selectedItem := m.raceList.SelectedItem(); selectedItem != nil {
				m.player2Race = string(selectedItem.(raceItem))
				// Switch to text input for unit count of Player 2.
				m.textInput.SetValue("")
				m.textInput.Placeholder = fmt.Sprintf("Enter number of %s", unitNameForRace(m.player2Race))
				m.state = stateSetupP2Count
				m.raceList.Select(0)
			}
		}
		return m, cmd

	// --- Player 2 Unit Count ---
	case stateSetupP2Count:
		m.textInput, cmd = m.textInput.Update(msg)
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			count, err := strconv.Atoi(m.textInput.Value())
			if err != nil || count <= 0 {
				m.battleLog = append(m.battleLog, "Invalid number for Player 2. Please enter a positive integer.")
				m.textInput.SetValue("")
				return m, nil
			}
			m.player2Count = count
			// Switch to battle speed multiplier input.
			m.textInput.SetValue("")
			m.textInput.Placeholder = "Enter battle speed multiplier (e.g., 1 for normal)"
			m.state = stateSetupMultiplier
		}
		return m, cmd

	// --- Battle Speed Multiplier Input ---
	case stateSetupMultiplier:
		m.textInput, cmd = m.textInput.Update(msg)
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			mul, err := strconv.ParseFloat(m.textInput.Value(), 64)
			if err != nil || mul <= 0 {
				m.battleLog = append(m.battleLog, "Invalid multiplier. Please enter a positive number.")
				m.textInput.SetValue("")
				return m, nil
			}
			m.multiplier = mul
			// Create teams using the selected races and counts.
			team1 := units.CreateTeam(m.player1Race, m.player1Count)
			team2 := units.CreateTeam(m.player2Race, m.player2Count)
			m.simulator = battle.NewBattleSimulator(team1, team2)
			startMsg := fmt.Sprintf("Battle started: %s vs %s at x%.2f speed.",
				m.player1Race, m.player2Race, m.multiplier)
			m.battleLog = append(m.battleLog, startMsg)
			m.state = stateBattle
			return m, tickCmd(0)
		}
		return m, cmd

	// --- Battle Simulation ---
	case stateBattle:
		switch msg := msg.(type) {
		case tea.KeyMsg:
			// Allow quitting.
			if msg.String() == "q" || msg.String() == "ctrl+c" {
				return m, tea.Quit
			}
		case tickMsg:
			logStr, finished, delay := m.simulator.Tick()
			m.battleLog = append(m.battleLog, logStr)
			if finished {
				m.state = stateEnd
				return m, nil
			}
			// Adjust delay using multiplier.
			effectiveDelay := time.Duration(float64(delay) / m.multiplier)
			return m, tickCmd(effectiveDelay)
		}

	// --- End State ---
	case stateEnd:
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			return m, tea.Quit
		}
	}

	// In states that use textInput, update it by default.
	m.textInput, cmd = m.textInput.Update(msg)
	return m, cmd
}

// tickMsg is used to schedule battle ticks.
type tickMsg time.Time

func tickCmd(delay time.Duration) tea.Cmd {
	return tea.Tick(delay, func(t time.Time) tea.Msg { return tickMsg(t) })
}

// unitNameForRace returns the display name for a given race.
func unitNameForRace(r string) string {
	switch r {
	case "zerg":
		return "Zerglings"
	case "terran":
		return "Marines"
	case "protoss":
		return "Zealots"
	default:
		return "Units"
	}
}

func (m model) View() string {
	var s string
	switch m.state {
	// --- Views for Setup States ---
	case stateSetupP1Race:
		s = "Player 1: Select your race:\n" + m.raceList.View()
	case stateSetupP1Count:
		s = fmt.Sprintf("Player 1 (%s selected):\nEnter number of %s:\n%s",
			m.player1Race, unitNameForRace(m.player1Race), m.textInput.View())
	case stateSetupP2Race:
		s = "Player 2: Select your race:\n" + m.raceList.View()
	case stateSetupP2Count:
		s = fmt.Sprintf("Player 2 (%s selected):\nEnter number of %s:\n%s",
			m.player2Race, unitNameForRace(m.player2Race), m.textInput.View())
	case stateSetupMultiplier:
		s = "Enter battle speed multiplier (1 for normal, >1 for faster, <1 for slower):\n" + m.textInput.View()

	// --- Battle View ---
	case stateBattle:
		// Create styled header, log, and footer.
		headerStyle := lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#FFB86C"))
		logStyle := lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).Padding(1, 2)
		footerStyle := lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#8BE9FD"))

		header := headerStyle.Render("Battle in Progress (press 'q' to quit)")
		bLog := ""
		for _, line := range m.battleLog {
			bLog += line + "\n"
		}
		logPane := logStyle.Render(bLog)
		// Get current unit counts.
		var p1Count, p2Count int
		if m.simulator != nil {
			p1Count = len(m.simulator.Team1)
			p2Count = len(m.simulator.Team2)
		}
		footer := footerStyle.Render(fmt.Sprintf("%s: %d remaining | %s: %d remaining",
			unitNameForRace(m.player1Race), p1Count, unitNameForRace(m.player2Race), p2Count))
		s = fmt.Sprintf("%s\n\n%s\n\n%s", header, logPane, footer)

	// --- End View ---
	case stateEnd:
		s = "Battle concluded.\n\n"
		for _, line := range m.battleLog {
			s += line + "\n"
		}
		s += "\nPress Enter to exit."
	}
	return s
}
