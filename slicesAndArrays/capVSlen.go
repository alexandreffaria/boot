package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type SliceStat struct {
	Len int `json:"len"`
	Cap int `json:"cap"`
}

func main() {
	var s []int
	var stats []SliceStat

	for i := 0; i < 10000; i++ {
		s = append(s, i)
		stats = append(stats, SliceStat{
			Len: len(s),
			Cap: cap(s),
		})
	}

	file, err := os.Create("slice_growth.json")
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	err = encoder.Encode(stats)
	if err != nil {
		fmt.Println("Error encoding JSON:", err)
		return
	}

	fmt.Println("✅ Data written to slice_growth.json")
	}
