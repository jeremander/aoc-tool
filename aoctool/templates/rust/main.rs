// Advent of Code
// Date:     {{puzzle.date_string}}
// Language: {{language}}

use std::env;
use std::fs;
use std::process;

mod aoc{{puzzle.year}}{{'%02d' % puzzle.day}};
use aoc{{puzzle.year}}{{'%02d' % puzzle.day}}::{parse, part1, part2};


const INPUT_DATA_PATH: &str = "{{input_data_path}}";

fn solve(part: i32) -> Option<i64> {
    let solver = if part == 1 { part1 } else { part2 };
    let input_data = fs::read_to_string(INPUT_DATA_PATH).expect("Could not read file.");
    let value = parse(&input_data).expect("parse not implemented");
    solver(value)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let part: i32 = match args[1].parse() {
        Err(_) => { process::exit(1) },
        Ok(part) => part
    };
    let solution: i64 = solve(part).expect("part{part} not implemented");
    println!("{solution}");
}
