package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"strconv"
	"time"
)

type Block struct {
	Index     int
	Timestamp int64
	Data      string
	PrevHash  string
	Hash      string
	Proof     int
}

func calculateHash(block Block) string {
	record := strconv.Itoa(block.Index) + strconv.FormatInt(block.Timestamp, 10) + block.Data + block.PrevHash + strconv.Itoa(block.Proof)
	h := sha256.New()
	h.Write([]byte(record))
	hashed := h.Sum(nil)
	return hex.EncodeToString(hashed)
}

func proofOfWork(prevProof int) int {
	proof := 0
	for !isValidProof(prevProof, proof) {
		proof++
	}
	return proof
}

func isValidProof(prevProof, proof int) bool {
	data := strconv.Itoa(prevProof) + strconv.Itoa(proof)
	hash := sha256.Sum256([]byte(data))
	return hex.EncodeToString(hash[:])[:4] == "0000"
}

func generateBlock(oldBlock Block, data string) Block {
	newBlock := Block{
		Index:     oldBlock.Index + 1,
		Timestamp: time.Now().Unix(),
		Data:      data,
		PrevHash:  oldBlock.Hash,
	}
	newBlock.Proof = proofOfWork(oldBlock.Proof)
	newBlock.Hash = calculateHash(newBlock)
	return newBlock
}

func isBlockValid(newBlock, oldBlock Block) bool {
	if oldBlock.Index+1 != newBlock.Index {
		return false
	}
	if oldBlock.Hash != newBlock.PrevHash {
		return false
	}
	if !isValidProof(oldBlock.Proof, newBlock.Proof) {
		return false
	}
	return true
}

func main() {
	genesisBlock := Block{0, time.Now().Unix(), "Genesis Block", "0", "", 100}
	genesisBlock.Hash = calculateHash(genesisBlock)
	fmt.Println("创世区块:", genesisBlock)
}
