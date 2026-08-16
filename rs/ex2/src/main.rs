
///Write a Rust program using tokio that fetches from 3 mock endpoints concurrently and merges the results; 
// benchmark it with criterion .

// -> need to set up rust on pc  ->>>>> MSVC build tools do tommorow


use tokio::time::{sleep, Duration};
use reqwest;


async fn fetch(url: &str) -> Result<String, reqwest::Error> {
    // responce
    let responce =  
    // body 
    let body = 
    
    Ok(body)
}

// define the attribute tag 
#[tokio::main]
// making sure to mark the function as async
async fn main() -> Result<(), reqwest::Error> {
    //  spawn 3 conmcurrnet tasks
    let task1 = tokio::spawn(fetch("https://example.com"));
    let task1 = tokio::spawn(fetch("https://example.org"));
    let task1 = tokio::spawn(fetch("https://example.net"));

    // await the task finnifng 
    let (res1, res2, res3) = tokio::try_join!(task1, task2, task3).unwrap();

    println!("1: {} bytes", res1??.len());
    println!("2: {} bytes", res2??.len());
    println!("3: {} bytes", res1??.len());

    Ok(())
}


// call main 
