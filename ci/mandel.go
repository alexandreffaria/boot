package main

import (
	"fmt"
	"math/cmplx"
	"time"
)

const (
	w      = 120 // terminal width (chars)
	h      = 40  // terminal height (lines)
	frames = 300 // how many frames to render
	iters  = 80  // mandelbrot iterations
)

// gradient of characters from light to dark (feel free to tweak)
var ramp = []rune(" .:-=+*#%@")

func mandelbrot(cx, cy float64) int {
	c := complex(cx, cy)
	z := complex(0, 0)
	for i := 0; i < iters; i++ {
		z = z*z + c
		if cmplx.Abs(z) > 2 {
			return i
		}
	}
	return iters
}

func tone(i int) rune {
	if i >= iters {
		return ramp[len(ramp)-1]
	}
	idx := int(float64(i) / float64(iters-1) * float64(len(ramp)-1))
	if idx < 0 {
		idx = 0
	}
	if idx >= len(ramp) {
		idx = len(ramp) - 1
	}
	return ramp[idx]
}

func clear() {
	fmt.Print("\033[2J\033[H") // ANSI clear + home
}

func frame(cx, cy, scale float64) {
	aspect := 2.0 // accounts for character cell aspect ratio
	for y := 0; y < h; y++ {
		iy := (float64(y)/float64(h) - 0.5) * scale
		for x := 0; x < w; x++ {
			ix := (float64(x)/float64(w) - 0.5) * scale * aspect
			i := mandelbrot(ix+cx, iy+cy)
			fmt.Printf("%c", tone(i))
		}
		fmt.Println()
	}
}

func main() {
	// target point to zoom into (seahorse valley near -0.743643887, 0.131825904)
	targetX := -0.743643887037151
	targetY := 0.13182590420533

	// start pos and scale
	cx, cy := -0.5, 0.0
	scale := 3.2 // larger = zoomed out

	// easing over frames
	for f := 0; f < frames; f++ {
		t := float64(f) / float64(frames-1)
		// smoothstep-ish easing
		e := t * t * (3 - 2*t)

		// interpolate center toward target
		cxf := cx + (targetX-cx)*e
		cyf := cy + (targetY-cy)*e

		// exponential zoom
		zoom := 0.0003 + (scale-0.03)*(1.0-(e)) // end near 0.03
		clear()
		fmt.Printf("ASCII Mandelbrot zoom — frame %d/%d\n", f+1, frames)
		fmt.Printf("center=(%.12f, %.12f) scale=%.4f iters=%d\n\n", cxf, cyf, zoom, iters)
		frame(cxf, cyf, zoom)
		time.Sleep(33 * time.Millisecond) // ~30 fps
	}
}
