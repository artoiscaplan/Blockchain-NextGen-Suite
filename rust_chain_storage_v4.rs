use std::collections::HashMap;
use std::fs::{File, OpenOptions};
use std::io::{Read, Write};
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Block {
    pub index: u64,
    pub hash: String,
    pub prev_hash: String,
    pub transactions: Vec<Transaction>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Transaction {
    pub sender: String,
    pub receiver: String,
    pub amount: f64,
}

pub struct ChainStorage {
    db: HashMap<u64, Block>,
    path: String,
}

impl ChainStorage {
    pub fn new(path: &str) -> Self {
        let mut storage = ChainStorage {
            db: HashMap::new(),
            path: path.to_string(),
        };
        storage.load();
        storage
    }

    pub fn put_block(&mut self, block: Block) {
        self.db.insert(block.index, block.clone());
        self.save();
    }

    pub fn get_block(&self, index: u64) -> Option<Block> {
        self.db.get(&index).cloned()
    }

    pub fn get_latest_block(&self) -> Option<Block> {
        let max_idx = self.db.keys().max().cloned();
        max_idx.and_then(|idx| self.get_block(idx))
    }

    pub fn len(&self) -> usize {
        self.db.len()
    }

    fn save(&self) {
        let file = File::create(&self.path).unwrap();
        serde_json::to_writer(file, &self.db).unwrap();
    }

    fn load(&mut self) {
        if let Ok(mut file) = File::open(&self.path) {
            let mut content = String::new();
            file.read_to_string(&mut content).unwrap();
            if !content.is_empty() {
                self.db = serde_json::from_str(&content).unwrap_or_default();
            }
        }
    }

    pub fn create_snapshot(&self, snapshot_path: &str) {
        let mut file = OpenOptions::new().create(true).write(true).open(snapshot_path).unwrap();
        serde_json::to_writer_pretty(&mut file, &self.db).unwrap();
    }
}

fn main() {
    let storage = ChainStorage::new("chain.db");
    println!("Storage initialized, blocks count: {}", storage.len());
}
