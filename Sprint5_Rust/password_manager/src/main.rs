use rand::{distributions::Uniform, thread_rng, Rng};
use serde::{Deserialize, Serialize};
use serde_json;
use std::{
    collections::HashMap,
    fs::File,
    io::{self, BufReader, BufWriter, Write},
    path::Path,
};

#[derive(Serialize, Deserialize)]
struct Entry {
    username: String,
    password: String,
}

fn load_entries() -> HashMap<String, Entry> {
    let path = Path::new("passwords.json");
    if path.exists() {
        if let Ok(file) = File::open(path) {
            let reader = BufReader::new(file);
            if let Ok(map) = serde_json::from_reader(reader) {
                return map;
            }
        }
    }
    HashMap::new()
}

fn save_entries(entries: &HashMap<String, Entry>) -> io::Result<()> {
    let file = File::create("passwords.json")?;
    let writer = BufWriter::new(file);
    serde_json::to_writer_pretty(writer, entries)?;
    Ok(())
}

fn main() {
    let greeting = "Welcome to Password Manager!";
    println!("{}", greeting);

    let mut entries = load_entries();

    loop {
        println!("\n=== Menu ===");
        println!("1) Add entry");
        println!("2) Generate password");
        println!("3) View entries");
        println!("4) Exit");
        print!("Enter choice: ");
        io::stdout().flush().unwrap();

        let mut choice = String::new();
        io::stdin().read_line(&mut choice).unwrap();
        let choice = choice.trim();

        match choice {
            "1" => {
                add_entry(&mut entries);
                let _ = save_entries(&entries);
            }
            "2" => {
                generate_and_add(&mut entries);
                let _ = save_entries(&entries);
            }
            "3" => view_entries(&entries),
            "4" => {
                println!("Goodbye!");
                break;
            }
            _ => println!("Invalid choice, try again."),
        }
    }
}

fn add_entry(entries: &mut HashMap<String, Entry>) {
    let site     = prompt("Enter site/app name: ");
    let username = prompt("Enter username: ");
    let pwd      = prompt("Enter password: ");
    entries.insert(
        site.clone(),
        Entry {
            username: username.clone(),
            password: pwd.clone(),
        },
    );
    println!("Added entry for `{}` (user: `{}`).", site, username);
}

fn generate_and_add(entries: &mut HashMap<String, Entry>) {
    let site     = prompt("Enter site/app name: ");
    let username = prompt("Enter username: ");

    let len: usize = prompt("Password length: ")
        .parse()
        .unwrap_or(12);

    let upper   = prompt("Include uppercase? (y/N): ").eq_ignore_ascii_case("y");
    let numbers = prompt("Include numbers? (y/N): ").eq_ignore_ascii_case("y");
    let symbols = prompt("Include symbols? (y/N): ").eq_ignore_ascii_case("y");

    let pwd = generate_password(len, upper, numbers, symbols);
    entries.insert(
        site.clone(),
        Entry {
            username: username.clone(),
            password: pwd.clone(),
        },
    );
    println!(
        "Generated & saved for `{}` (user: `{}`): {}",
        site, username, pwd
    );
}

fn view_entries(entries: &HashMap<String, Entry>) {
    if entries.is_empty() {
        println!("No entries yet.");
    } else {
        println!("\nSaved entries:");
        for (site, entry) in entries {
            println!(
                "- {} → user: `{}`, pass: `{}`",
                site, entry.username, entry.password
            );
        }
    }
}

fn generate_password(
    length: usize,
    include_upper: bool,
    include_numbers: bool,
    include_symbols: bool,
) -> String {
    let mut pool = String::from("abcdefghijklmnopqrstuvwxyz");
    if include_upper   { pool.push_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); }
    if include_numbers { pool.push_str("0123456789"); }
    if include_symbols { pool.push_str("!@#$%^&*()-_=+"); }

    let chars: Vec<char> = pool.chars().collect();
    let mut rng = thread_rng();
    let die = Uniform::from(0..chars.len());

    (0..length)
        .map(|_| {
            let idx = rng.sample(die);
            chars[idx]
        })
        .collect()
}

fn prompt(msg: &str) -> String {
    print!("{}", msg);
    io::stdout().flush().unwrap();
    let mut buf = String::new();
    io::stdin().read_line(&mut buf).unwrap();
    buf.trim().to_string()
}
