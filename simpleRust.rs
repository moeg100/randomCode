use std::io;

fn simple_s(input:String)-> String{
    let a = rand::random_range(1..3);
    println!("Input is : {input} and a is {a}");
    
    let mut answer;
    if a == 1 {
        answer = "Rock";
    }
    else if a == 2 {
        answer = "Paper";
        
    }
    else {
        answer = "Scissor";
    }
    println!("ANSWER IS : {answer}");
    return input
}


fn main() {

    let mut input = String::new();
    match io::stdin().read_line(&mut input) {
        Ok(n) => {
            //println!("{n} bytes read");
            //println!("{input}");
            simple_s(input);
        }
        Err(error) => println!("error: {error}"),
    }
 
}
