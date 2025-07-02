package main

import (
	"fmt"
)

func main() {
	// Initial slice
	slice := []int{4, 5, 3}
	fmt.Println("Before append:")
	fmt.Printf("  slice: %v\n", slice)
	fmt.Printf("  len: %d, cap: %d\n", len(slice), cap(slice))
	fmt.Printf("  address of backing array: %p\n", &slice[0])

	// Append new value
	slice = append(slice, 2)

	fmt.Println("\nAfter append:")
	fmt.Printf("  slice: %v\n", slice)
	fmt.Printf("  len: %d, cap: %d\n", len(slice), cap(slice))
	fmt.Printf("  address of backing array: %p\n", &slice[0])
}
