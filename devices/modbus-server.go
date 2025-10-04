package main

import (
	"encoding/binary"
	"fmt"
	"io"
	"log"
	"net"
	"os"
)

var coils []bool

func init() {
	coils = make([]bool, 10)
	// Optional: set some coils to true for simulation
	coils[0] = true
	coils[3] = true
	coils[7] = true
}
func main() {
	arguments := os.Args
	if len(arguments) == 1 {
		fmt.Println("Please provide the port number")
		return
	}

	port := ":" + arguments[1]
	l, err := net.Listen("tcp4", port)
	if err != nil {
		log.Fatal(err)
	}
	defer l.Close()

	fmt.Println("Listening on port", port)

	for {
		c, err := l.Accept()
		if err != nil {
			log.Println("Accept error:", err)
			continue
		}
		go handleConnection(c)
	}
}

func handleConnection(c net.Conn) {
	defer c.Close()
	header := make([]byte, 7)
	if _, err := io.ReadFull(c, header); err != nil {
		if err != io.EOF {
			log.Printf("read header error: %v", err)
		}
	}
	trId := binary.BigEndian.Uint16(header[0:2])
	prId := binary.BigEndian.Uint16(header[2:4])
	mdLen := binary.BigEndian.Uint16(header[4:6])
	unitID := header[6]
	length := mdLen - 1
	pdu := make([]byte, length)
	if _, err := io.ReadFull(c, pdu); err != nil {
		if err != io.EOF {
			log.Printf("read PDU error: %v", err)
		}
	}
	fc := pdu[0]
	respPDU := processPDU(fc, pdu)
	respLen := 1 + len(respPDU) // unit id + pdu
	respHeader := make([]byte, 7)
	binary.BigEndian.PutUint16(respHeader[0:2], trId)
	binary.BigEndian.PutUint16(respHeader[2:4], prId) // protocol id
	binary.BigEndian.PutUint16(respHeader[4:6], uint16(respLen))
	respHeader[6] = unitID
	fmt.Printf("%v", respHeader)
	// send header + pdu
	resp := append(respHeader, respPDU...)
	// Single write
	if _, err := c.Write(resp); err != nil {
		log.Printf("write response error: %v", err)
		return
	}
}
func processPDU(fc byte, pdu []byte) []byte {
	switch fc {
	case 1: //read coils
		if len(pdu) < 5 {
			return exceptionResponse(fc, 3) // illegal data value
		}
		addr := int(binary.BigEndian.Uint16(pdu[1:3]))
		qty := int(binary.BigEndian.Uint16(pdu[3:5]))
		return readCoilsResponse(fc, addr, qty)
	default:
		return exceptionResponse(fc, 3) // illegal data value
	}

}

func exceptionResponse(fc byte, exCode byte) []byte {
	// function code with MSB set
	return []byte{fc | 0x80, exCode}
}

func readCoilsResponse(fc byte, addr, qty int) []byte {
	if qty < 1 || qty > 2000 || addr < 0 || addr+qty > len(coils) {
		return exceptionResponse(fc, 3)
	}
	byteCount := (qty + 7) / 8
	resp := make([]byte, 2+byteCount) // fc + bytecount + data
	resp[0] = fc
	resp[1] = byte(byteCount)
	for i := 0; i < qty; i++ {
		if coils[addr+i] {
			byteIndex := i / 8
			bitIndex := i % 8
			resp[2+byteIndex] |= 1 << uint(bitIndex)
		}
	}
	return resp
}
