use std::io;
use std::process::ExitCode;


fn simple_s(input:String)-> String{
    let a = rand::random_range(1..4);
    println!("Input is : {input} and a is {a}");
    
    let answer = if a == 1 {
        "Rock"
    } else if a == 2 {
        "Paper"
    } else {
        "Scissor"
    };
    
    println!("ANSWER IS : {answer}");
    return input
}


fn main() -> ExitCode {

    let mut input = String::new();
    match io::stdin().read_line(&mut input) {
        Ok(_) => {
            let cleaned_input = input.trim().to_lowercase();
            
            if !(cleaned_input == "rock" || cleaned_input == "paper" || cleaned_input == "scissor") {
                println!("Input doesn't match the game words");
                return ExitCode::from(42);
            }
            simple_s(cleaned_input);
            ExitCode::SUCCESS
        }
        Err(error) => {
            println!("error: {error}");
            ExitCode::FAILURE
            }
        }
    }
 
