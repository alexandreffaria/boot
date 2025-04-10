package ui

import (
	"fmt"

	"github.com/charmbracelet/lipgloss"
)

// unitNameForRace returns the display name for a given race.
// (Defined here only.)
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

// View implements the tea.Model View method.
func (m *Model) View() string {
	var s string
	switch m.State {
	case StateSetupP1Race:
		s = "Player 1: Select your race:\n" + m.RaceList.View()
	case StateSetupP1Count:
		s = fmt.Sprintf("Player 1 (%s selected):\nEnter number of %s:\n%s",
			m.Player1Race, unitNameForRace(m.Player1Race), m.TextInput.View())
	case StateSetupP2Race:
		s = "Player 2: Select your race:\n" + m.RaceList.View()
	case StateSetupP2Count:
		s = fmt.Sprintf("Player 2 (%s selected):\nEnter number of %s:\n%s",
			m.Player2Race, unitNameForRace(m.Player2Race), m.TextInput.View())
	case StateSetupMultiplier:
		s = "Enter battle speed multiplier (1 for normal, >1 for faster, <1 for slower):\n" + m.TextInput.View()
	case StateBattle:
		headerStyle := lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#FFB86C"))
		logStyle := lipgloss.NewStyle().Border(lipgloss.RoundedBorder()).Padding(1, 2)
		footerStyle := lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#8BE9FD"))
		header := headerStyle.Render("Battle in Progress (press 'q' to quit)")
		bLog := ""
		for _, line := range m.BattleLog {
			bLog += line + "\n"
		}
		logPane := logStyle.Render(bLog)
		p1Count, p2Count := m.Simulator.GetTeamCounts()
		footer := footerStyle.Render(fmt.Sprintf("%s: %d remaining | %s: %d remaining",
			unitNameForRace(m.Player1Race), p1Count, unitNameForRace(m.Player2Race), p2Count))
		s = fmt.Sprintf("%s\n\n%s\n\n%s", header, logPane, footer)
	case StateEnd:
		endHeaderStyle := lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#50FA7B"))
		endLogStyle := lipgloss.NewStyle().Border(lipgloss.DoubleBorder()).Padding(1, 2)
		header := endHeaderStyle.Render("Battle Concluded")
		winnerMsg := fmt.Sprintf("%s win the battle with %d remaining!", m.WinnerRace, m.WinnerCount)
		logPane := endLogStyle.Render(winnerMsg)
		exitMsg := "\nPress Enter to exit."
		s = fmt.Sprintf("%s\n\n%s%s", header, logPane, exitMsg)
	}
	return s
}
