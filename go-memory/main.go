package main

import (
	"fmt"
	"runtime"
	"time"

	"golang.org/x/text/message"
)

func hammerCPU(duration time.Duration, clockGHz float64) {
	numCPU := runtime.NumCPU()
	runtime.GOMAXPROCS(numCPU)
	fmt.Printf("🔧 Hammering %d cores at 100%% for %v...\n", numCPU, duration)

	done := make(chan uint64)

	for i := 0; i < numCPU; i++ {
		go func(id int) {
			start := time.Now()
			var iterations uint64 = 0
			for time.Since(start) < duration {
				iterations++
			}
			done <- iterations
		}(i)
	}

	var totalIterations uint64 = 0
	p := message.NewPrinter(message.MatchLanguage("en"))

	for i := 0; i < numCPU; i++ {
		iter := <-done
		p.Printf("🧠 Core %2d: %,d iterations\n", i, iter)
		totalIterations += iter
	}

	totalSeconds := duration.Seconds()
	totalGHz := clockGHz * float64(numCPU)
	estimatedCycles := totalGHz * totalSeconds * 1e9 // GHz * seconds = cycles
	// Note: this assumes 1 instruction per cycle

	p.Println("===================================")
	p.Printf("🔥 Total calculations:     %d\n", totalIterations)
	p.Printf("⚡ Estimated cycles used: %.3e (%.0f GHz total x %.1f sec)\n",
		estimatedCycles, totalGHz, totalSeconds)
	p.Println("===================================")
}

func hogMemory(sizeGB int, duration time.Duration) {
	fmt.Printf("🐘 Allocating %d GB of RAM...\n", sizeGB)
	size := sizeGB * 1024 * 1024 * 1024

	startAlloc := time.Now()
	data := make([]byte, size)
	allocTime := time.Since(startAlloc)
	fmt.Printf("✅ Allocation took: %v (%.2f GB/s)\n", allocTime,
		float64(sizeGB)/allocTime.Seconds())

	fmt.Println("🚶 Touching memory to commit pages...")
	startTouch := time.Now()
	pageSize := 4096
	pagesTouched := 0
	for i := 0; i < len(data); i += pageSize {
		data[i] = byte(i % 256)
		pagesTouched++
	}
	touchTime := time.Since(startTouch)

	fmt.Printf("✅ Touching took:    %v (%.2f GB/s, %d pages touched)\n",
		touchTime,
		float64(sizeGB)/touchTime.Seconds(),
		pagesTouched)

	fmt.Printf("🛌 Holding memory for %v...\n", duration)
	time.Sleep(duration)

	// Optional: Clear memory to release it sooner
	for i := range data {
		data[i] = 0
	}

	fmt.Println("🧹 Memory released.")
}

func main() {
	fmt.Println("🚀 Starting system stress test...")

	clockSpeedGHz := 5.25
	hammerCPU(0 * time.Second, clockSpeedGHz)
	hogMemory(50, 10*time.Second)

	fmt.Println("✅ Test complete. Time to cool off.")
}
