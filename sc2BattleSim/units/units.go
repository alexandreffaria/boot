package units

import "fmt"

// UnitType defines the type of unit.
type UnitType string

const (
	Zergling UnitType = "Zergling"
	Marine   UnitType = "Marine"
	Zealot   UnitType = "Zealot"
)

// Unit represents a combat unit.
type Unit struct {
	Type        UnitType
	Name        string
	HP          int
	Damage      int
	AttackSpeed float64 // Attacks per second
	Cost        int
	Race        string
}

// Global stats for each unit type.
var UnitStats = map[UnitType]Unit{
	Zergling: {
		Type:        Zergling,
		HP:          35,
		Damage:      5,
		AttackSpeed: 1.5, // Attacks per second
		Cost:        25,
		Race:        "Zerg",
	},
	Marine: {
		Type:        Marine,
		HP:          45,
		Damage:      6,
		AttackSpeed: 0.86, // Attacks per second
		Cost:        50,
		Race:        "Terran",
	},
	Zealot: {
		Type:        Zealot,
		HP:          100,
		Damage:      8,
		AttackSpeed: 0.86, // Attacks per second
		Cost:        100,
		Race:        "Protoss",
	},
}

// NewUnit creates a new unit for a given unit type and an identifier.
func NewUnit(unitType UnitType, id int) *Unit {
	stat, exists := UnitStats[unitType]
	if !exists {
		// Fallback if unitType is unknown.
		stat = UnitStats[Zealot]
	}
	newUnit := stat // copy the stats
	newUnit.Name = fmt.Sprintf("%s #%d", unitType, id)
	return &newUnit
}

// CreateTeam initializes a team of units based on the race and unit count.
// For simplicity, if the player's race is "zerg", we create Zerglings;
// "terran" creates Marines; "protoss" creates Zealots.
func CreateTeam(race string, count int) []*Unit {
	var unitType UnitType
	switch race {
	case "zerg":
		unitType = Zergling
	case "terran":
		unitType = Marine
	case "protoss":
		unitType = Zealot
	default:
		unitType = Zealot
	}
	team := make([]*Unit, count)
	for i := 0; i < count; i++ {
		team[i] = NewUnit(unitType, i+1)
	}
	return team
}
