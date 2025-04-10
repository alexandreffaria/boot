package battle

import (
	"fmt"
	"math/rand"
	"time"

	"sc2battlesim/units"
)

type BattleSimulator struct {
	Team1           []*units.Unit
	Team2           []*units.Unit
	CurrentAttacker *units.Unit
	CurrentDefender *units.Unit
	AttackerTeam    int // 1 if the current attacker is from Team1, 2 if from Team2

	BattleOver bool
}

func NewBattleSimulator(team1, team2 []*units.Unit) *BattleSimulator {
	bs := &BattleSimulator{
		Team1: team1,
		Team2: team2,
	}
	bs.Start()
	return bs
}

func (b *BattleSimulator) Start() {
	rand.Seed(time.Now().UnixNano())
	if len(b.Team1) > 0 && len(b.Team2) > 0 {
		u1 := b.Team1[rand.Intn(len(b.Team1))]
		u2 := b.Team2[rand.Intn(len(b.Team2))]
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
func (b *BattleSimulator) Tick() (log string, finished bool, delay time.Duration) {
	if b.BattleOver {
		return "Battle is over.", true, 0
	}

	attacker := b.CurrentAttacker
	defender := b.CurrentDefender
	damage := attacker.Damage
	defender.HP -= damage
	log = fmt.Sprintf("%s attacked %s for %d damage. %s HP remaining: %d",
		attacker.Name, defender.Name, damage, defender.Name, defender.HP)

	if defender.HP <= 0 {
		log += fmt.Sprintf("\n%s has died!", defender.Name)
		if b.AttackerTeam == 1 {
			b.removeUnitFromTeam(2, defender)
			if len(b.Team2) == 0 {
				log += fmt.Sprintf("\n%s win the battle!", b.Team1[0].Race)
				b.BattleOver = true
				return log, true, 0
			}
			b.CurrentDefender = b.Team2[rand.Intn(len(b.Team2))]
		} else {
			b.removeUnitFromTeam(1, defender)
			if len(b.Team1) == 0 {
				log += fmt.Sprintf("\n%s win the battle!", b.Team2[0].Race)
				b.BattleOver = true
				return log, true, 0
			}
			b.CurrentDefender = b.Team1[rand.Intn(len(b.Team1))]
		}
		log += fmt.Sprintf("\n%s enters the battle.", b.CurrentDefender.Name)
		delay = time.Duration((1.0 / attacker.AttackSpeed) * float64(time.Second))
		return log, false, delay
	}

	// Swap roles so both sides trade blows.
	b.CurrentAttacker, b.CurrentDefender = b.CurrentDefender, b.CurrentAttacker
	b.AttackerTeam = 3 - b.AttackerTeam
	delay = time.Duration((1.0 / b.CurrentAttacker.AttackSpeed) * float64(time.Second))
	return log, false, delay
}

// GetTeamCounts returns the number of units remaining in Team1 and Team2.
func (b *BattleSimulator) GetTeamCounts() (int, int) {
	return len(b.Team1), len(b.Team2)
}
