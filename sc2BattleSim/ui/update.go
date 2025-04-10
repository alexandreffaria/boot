package ui

import (
	"fmt"
	"strconv"
	"time"

	"sc2battlesim/battle"
	"sc2battlesim/units"

	"github.com/charmbracelet/bubbles/list"
	tea "github.com/charmbracelet/bubbletea"
)

func tickCmd(delay time.Duration) tea.Cmd {
	return tea.Tick(delay, func(t time.Time) tea.Msg {
		return tickMsg(t)
	})
}

func (m *Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd

	switch m.State {
	case StateSetupP1Race:
		var listCmd tea.Cmd
		m.RaceList, listCmd = m.RaceList.Update(msg)
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			if selectedItem := m.RaceList.SelectedItem(); selectedItem != nil {
				m.Player1Race = string(selectedItem.(raceItem))
				m.TextInput.SetValue("")
				m.TextInput.Placeholder = fmt.Sprintf("Enter number of %s", unitNameForRace(m.Player1Race))
				m.State = StateSetupP1Count
				m.RaceList.Select(0)
			}
		}
		return m, listCmd

	case StateSetupP1Count:
		m.TextInput, cmd = m.TextInput.Update(msg)
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			count, err := strconv.Atoi(m.TextInput.Value())
			if err != nil || count <= 0 {
				m.BattleLog = append(m.BattleLog, "Invalid number for Player 1. Please enter a positive integer.")
				m.TextInput.SetValue("")
				return m, nil
			}
			m.Player1Count = count
			// Set up for Player 2 race selection.
			m.RaceList.SetItems([]list.Item{
				newRaceItem("zerg"),
				newRaceItem("terran"),
				newRaceItem("protoss"),
			})
			m.RaceList.Select(0)
			m.State = StateSetupP2Race
		}
		return m, cmd

	case StateSetupP2Race:
		var listCmd tea.Cmd
		m.RaceList, listCmd = m.RaceList.Update(msg)
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			if selectedItem := m.RaceList.SelectedItem(); selectedItem != nil {
				m.Player2Race = string(selectedItem.(raceItem))
				m.TextInput.SetValue("")
				m.TextInput.Placeholder = fmt.Sprintf("Enter number of %s", unitNameForRace(m.Player2Race))
				m.State = StateSetupP2Count
				m.RaceList.Select(0)
			}
		}
		return m, listCmd

	case StateSetupP2Count:
		m.TextInput, cmd = m.TextInput.Update(msg)
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			count, err := strconv.Atoi(m.TextInput.Value())
			if err != nil || count <= 0 {
				m.BattleLog = append(m.BattleLog, "Invalid number for Player 2. Please enter a positive integer.")
				m.TextInput.SetValue("")
				return m, nil
			}
			m.Player2Count = count
			m.TextInput.SetValue("")
			m.TextInput.Placeholder = "Enter battle speed multiplier (e.g., 1 for normal)"
			m.State = StateSetupMultiplier
		}
		return m, cmd

	case StateSetupMultiplier:
		m.TextInput, cmd = m.TextInput.Update(msg)
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			mul, err := strconv.ParseFloat(m.TextInput.Value(), 64)
			if err != nil || mul <= 0 {
				m.BattleLog = append(m.BattleLog, "Invalid multiplier. Please enter a positive number.")
				m.TextInput.SetValue("")
				return m, nil
			}
			m.Multiplier = mul
			// Create teams using the updated unit stats.
			team1 := units.CreateTeam(m.Player1Race, m.Player1Count)
			team2 := units.CreateTeam(m.Player2Race, m.Player2Count)
			m.Simulator = battle.NewBattleSimulator(team1, team2)
			startMsg := fmt.Sprintf("Battle started: %s vs %s at x%.2f speed.",
				m.Player1Race, m.Player2Race, m.Multiplier)
			m.BattleLog = append(m.BattleLog, startMsg)
			m.State = StateBattle
			return m, tickCmd(0)
		}
		return m, cmd

	case StateBattle:
		switch msg := msg.(type) {
		case tea.KeyMsg:
			if msg.String() == "q" || msg.String() == "ctrl+c" {
				return m, tea.Quit
			}
		case tickMsg:
			logStr, finished, delay := m.Simulator.Tick()
			m.BattleLog = append(m.BattleLog, logStr)
			if finished {
				// Determine winner from team counts.
				p1Count, p2Count := m.Simulator.GetTeamCounts()
				if p1Count > 0 {
					m.WinnerRace = unitNameForRace(m.Player1Race)
					m.WinnerCount = p1Count
				} else {
					m.WinnerRace = unitNameForRace(m.Player2Race)
					m.WinnerCount = p2Count
				}
				m.State = StateEnd
				return m, nil
			}
			effectiveDelay := time.Duration(float64(delay) / m.Multiplier)
			return m, tickCmd(effectiveDelay)
		}

	case StateEnd:
		if keyMsg, ok := msg.(tea.KeyMsg); ok && keyMsg.Type == tea.KeyEnter {
			return m, tea.Quit
		}
	}

	m.TextInput, cmd = m.TextInput.Update(msg)
	return m, cmd
}
