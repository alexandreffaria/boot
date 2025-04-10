package ui

import (
	"fmt"
	"io"
	"time"

	"github.com/charmbracelet/bubbles/list"
	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
)

// State defines the various stages in our UI.
type State int

const (
	StateSetupP1Race State = iota
	StateSetupP1Count
	StateSetupP2Race
	StateSetupP2Count
	StateSetupMultiplier
	StateBattle
	StateEnd
)

// Model holds all the data needed for the TUI.
type Model struct {
	State State

	// Components for text input and race selection.
	TextInput textinput.Model
	RaceList  list.Model

	// Setup values.
	Player1Race  string
	Player2Race  string
	Player1Count int
	Player2Count int
	Multiplier   float64

	// Winner information computed at battle end.
	WinnerRace  string
	WinnerCount int

	// Battle simulation.
	Simulator BattleSimulatorInterface
	BattleLog []string
}

// BattleSimulatorInterface defines the methods used by the UI to interact with the battle simulation.
type BattleSimulatorInterface interface {
	Tick() (log string, finished bool, delay time.Duration)
	GetTeamCounts() (int, int)
}

// tickMsg is used to schedule battle ticks.
type tickMsg time.Time

// NewModel creates an initial Model with default component settings.
func NewModel() *Model {
	ti := textinput.New()
	ti.Placeholder = "Enter value"
	ti.Focus()
	ti.CharLimit = 20
	ti.Width = 30

	items := []list.Item{
		newRaceItem("zerg"),
		newRaceItem("terran"),
		newRaceItem("protoss"),
	}
	rl := list.New(items, newRaceItemDelegate(), 20, 5)
	rl.Title = "Select Race"
	rl.SetShowStatusBar(false)
	rl.SetFilteringEnabled(false)
	rl.DisableQuitKeybindings()

	return &Model{
		State:     StateSetupP1Race,
		TextInput: ti,
		RaceList:  rl,
		BattleLog: []string{},
	}
}

// Init implements the tea.Model interface.
func (m *Model) Init() tea.Cmd {
	// textinput.Model in your version does not have Blink(), so just return nil.
	return nil
}

// --- Race Item and Delegate Definitions ---

type raceItem string

func newRaceItem(r string) raceItem {
	return raceItem(r)
}

func (r raceItem) Title() string {
	return string(r)
}

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

func (r raceItem) FilterValue() string {
	return string(r)
}

type raceItemDelegate struct{}

func newRaceItemDelegate() raceItemDelegate {
	return raceItemDelegate{}
}

func (d raceItemDelegate) Height() int {
	return 1
}

func (d raceItemDelegate) Spacing() int {
	return 0
}

func (d raceItemDelegate) Update(msg tea.Msg, list *list.Model) tea.Cmd {
	return nil
}

// Render writes the item to w. (Note: No 'sel' parameter now. We determine selection from m.Index().)
func (d raceItemDelegate) Render(w io.Writer, m list.Model, index int, item list.Item) {
	ri, ok := item.(raceItem)
	if !ok {
		return
	}
	sel := index == m.Index()
	if sel {
		fmt.Fprintf(w, "> %s", ri.Title())
	} else {
		fmt.Fprintf(w, "  %s", ri.Title())
	}
}
