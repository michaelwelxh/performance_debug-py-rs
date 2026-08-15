
///Write a Rust program using tokio that fetches from 3 mock endpoints concurrently and merges the results; 
// benchmark it with criterion .

// -> need to set up rust on pc  ->>>>> MSVC build tools do tommorow


use tokio::task;

// define the attribute tag 
#[tokio::main]
// making sure to mark the function as async

async fn main() {

    //  spawn 3 conmcurrnet tasks
    let task1 = tokio::spawn(async {endpoint1(5);});
    let task2 = tokio::spawn(async {endpoint1(5);});
    let task3 = tokio::spawn(async {endpoint1(5);});

    // await the task finnifng 
    let (res1, res2, res3) = tokio::try_join!(task1, task2, task3).unwrap();

    // sum 
    let total = res1 + res2 + res3;
    println!("The value of total is: {total}");

}

fn endpoint1(x: i32) -> i32 {
    x*2
    println!("The value of x is: {x}");
}
fn endpoint2(x: i32) -> i32 {
    x+3
    println!("The value of x is: {x}");
}
fn endpoint_sub(x: i32) -> i32 {
    x-1
    println!("The value of x is: {x}");
}


