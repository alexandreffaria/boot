package battle

import (
	"fmt"
	"math/rand"
	"time"

	"sc2battlesim/units"
)

// BattleSimulator holds the state for a battle.
type BattleSimulator struct {
	Team1 []*units.Unit
	Team2 []*units.Unit

	CurrentAttacker *units.Unit
	CurrentDefender *units.Unit
	AttackerTeam    int // 1 if the current attacker is from Team1, 2 if from Team2

	BattleOver bool
}

// NewBattleSimulator creates a new battle simulation from two teams.
func NewBattleSimulator(team1, team2 []*units.Unit) *BattleSimulator {
	bs := &BattleSimulator{
		Team1: team1,
		Team2: team2,
	}
	bs.Start()
	return bs
}

// Start initializes the first round by selecting one random unit from each team,
// then randomly choosing which unit attacks first.
func (b *BattleSimulator) Start() {
	rand.Seed(time.Now().UnixNano())
	if len(b.Team1) > 0 && len(b.Team2) > 0 {
		u1 := b.Team1[rand.Intn(len(b.Team1))]
		u2 := b.Team2[rand.Intn(len(b.Team2))]
		// Randomly decide who attacks first.
		if rand.Intn(2) == 0 {
			b.CurrentAttacker = u1
			b.CurrentDefender = u2
			b.AttackerTeam = 1
		} else {
			b.CurrentAttacker = u2
			b.CurrentDefender = u1
			b.AttackerTeam = 2
		}
	} else {
		b.BattleOver = true
	}
}

// removeUnitFromTeam removes the given unit from the specified team.
func (b *BattleSimulator) removeUnitFromTeam(team int, unit *units.Unit) {
	if team == 1 {
		for i, u := range b.Team1 {
			if u == unit {
				b.Team1 = append(b.Team1[:i], b.Team1[i+1:]...)
				break
			}
		}
	} else {
		for i, u := range b.Team2 {
			if u == unit {
				b.Team2 = append(b.Team2[:i], b.Team2[i+1:]...)
				break
			}
		}
	}
}

// Tick simulates one attack tick.
// The attacker deals its damage to the defender.
// If the defender survives, the roles swap (so both sides get a chance to hit).
// If the defender dies, a new opponent is chosen (if available) and the winner’s race is used when the battle ends.
// The next tick delay is computed as 1 / (attack speed of the attacking unit).
func (b *BattleSimulator) Tick() (log string, finished bool, delay time.Duration) {
	if b.BattleOver {
		return "Battle is over.", true, 0
	}

	attacker := b.CurrentAttacker
	defender := b.CurrentDefender

	// Attacker deals damage.
	damage := attacker.Damage
	defender.HP -= damage
	log = fmt.Sprintf("%s attacked %s for %d damage. %s HP remaining: %d",
		attacker.Name, defender.Name, damage, defender.Name, defender.HP)

	if defender.HP <= 0 {
		log += fmt.Sprintf("\n%s has died!", defender.Name)
		// Remove defender from its team and check for battle over.
		if b.AttackerTeam == 1 {
			b.removeUnitFromTeam(2, defender)
			if len(b.Team2) == 0 {
				winningRace := b.Team1[0].Race // all units in Team1 share the same race
				log += fmt.Sprintf("\n%s win the battle!", winningRace)
				b.BattleOver = true
				return log, true, 0
			}
			// Choose new opponent from Team2.
			b.CurrentDefender = b.Team2[rand.Intn(len(b.Team2))]
		} else {
			b.removeUnitFromTeam(1, defender)
			if len(b.Team1) == 0 {
				winningRace := b.Team2[0].Race
				log += fmt.Sprintf("\n%s win the battle!", winningRace)
				b.BattleOver = true
				return log, true, 0
			}
			// Choose new opponent from Team1.
			b.CurrentDefender = b.Team1[rand.Intn(len(b.Team1))]
		}
		log += fmt.Sprintf("\n%s enters the battle.", b.CurrentDefender.Name)
		delay = time.Duration((1.0 / attacker.AttackSpeed) * float64(time.Second))
		return log, false, delay
	}

	// If the defender is still alive, swap roles.
	b.CurrentAttacker, b.CurrentDefender = b.CurrentDefender, b.CurrentAttacker
	// Swap the team indicator (1 becomes 2, 2 becomes 1).
	b.AttackerTeam = 3 - b.AttackerTeam
	// Next tick delay based on the new attacker's attack speed.
	delay = time.Duration((1.0 / b.CurrentAttacker.AttackSpeed) * float64(time.Second))
	return log, false, delay
}
