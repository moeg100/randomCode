use std::io;
use std::process::ExitCode;


fn resolve(computer:String, player:String) -> bool{
    if computer == "rock" && player == "paper"{
        return true;
    }
    else if computer == "scissor" && player == "rock"{
        return true;
    }
    else if computer == "paper" && player == "scissor"{
        return true;
    }
    
    else if computer == player{
        println!("Its Tie");
        return false;
    }
    
    else{
        return false;
    }
    
}

fn simple_s(input:String)-> String{
    let a = rand::random_range(1..4);
    println!("Input is : {input} and a is {a}");
    
    let answer = if a == 1 {
        "rock"
    } else if a == 2 {
        "paper"
    } else {
        "scissor"
    };
    
    println!("ANSWER IS : {answer}");
    
    
    let result = resolve(answer.to_string(), input.clone());
    println!("Result is {result}");
    
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
 
