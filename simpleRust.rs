use std::io;
use std::process::ExitCode;
use rand::Rng;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Choice {
    Rock,
    Paper,
    Scissor,
}

impl Choice {
    fn from_str(s: &str) -> Option<Self> {
        match s {
            "rock" => Some(Choice::Rock),
            "paper" => Some(Choice::Paper),
            "scissor" => Some(Choice::Scissor),
            _ => None,
        }
    }
}

/// Returns true if player wins, false if computer wins or tie
fn resolve(computer: Choice, player: Choice) -> Option<bool> {
    match (computer, player) {
        (c, p) if c == p => {
            println!("It's a tie!");
            Some(false)
        }
        (Choice::Rock, Choice::Paper) => Some(true),
        (Choice::Scissor, Choice::Rock) => Some(true),
        (Choice::Paper, Choice::Scissor) => Some(true),
        _ => Some(false),
    }
}

fn play_round(player_choice: Choice) -> bool {
    let mut rng = rand::thread_rng();
    let computer_choice = match rng.gen_range(0..3) {
        0 => Choice::Rock,
        1 => Choice::Paper,
        _ => Choice::Scissor,
    };

    println!("Computer played: {:?}", computer_choice);
    
    match resolve(computer_choice, player_choice) {
        Some(true) => {
            println!("Player wins!");
            true
        }
        Some(false) => {
            println!("Computer wins or tie!");
            false
        }
        None => false,
    }
}

fn main() -> ExitCode {
    loop {
        println!("Enter your choice (rock, paper, scissor) or 'quit' to exit:");
        
        let mut input = String::new();
        match io::stdin().read_line(&mut input) {
            Ok(_) => {
                let cleaned_input = input.trim().to_lowercase();
                
                if cleaned_input == "quit" {
                    break;
                }
                
                match Choice::from_str(&cleaned_input) {
                    Some(choice) => {
                        if play_round(choice) {
                            continue;
                        } else {
                            break;
                        }
                    }
                    None => {
                        println!("Invalid input! Please enter: rock, paper, or scissor");
                    }
                }
            }
            Err(error) => {
                eprintln!("Error reading input: {}", error);
                return ExitCode::FAILURE;
            }
        }
    }
    
    ExitCode::SUCCESS
}
