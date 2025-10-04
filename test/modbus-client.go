package main

import (
	"fmt"
	"log"
	"time"

	"github.com/goburrow/modbus"
)

func main() {
	handler := modbus.NewTCPClientHandler("127.0.0.1:502") // Modbus device IP
	handler.Timeout = 5 * time.Second
	handler.SlaveId = 1

	err := handler.Connect()
	if err != nil {
		log.Fatalf("Failed to connect: %v", err)
	}
	defer handler.Close()

	client := modbus.NewClient(handler)

	// Read 8 coils from address 0
	results, err := client.ReadCoils(0, 8)
	if err != nil {
		log.Fatalf("ReadCoils failed: %v", err)
	}

	// Print as raw bytes
	fmt.Printf("Coils raw bytes: %v\n", results)
}
