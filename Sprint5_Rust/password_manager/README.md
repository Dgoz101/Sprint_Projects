# Overview

My goal was to challenge myself to learn a new language that I have never worked with before and really knew nothing about. I have heard some
things about Rust from peers and on the internet so I figured I would check it out. I chose to write a password manager that securely
stores site, username, and password entries in a JSON file on disk. Along the way, I explored: 

 - Declaring immutable and mutable variables with let and let mut 

 - Writing expressions, match statements, and if conditionals

 - Using loop and for loops for interactive menus and data iteration

 - Defining functions that take ownership or borrow references

 - Employing data structures (HashMap) and external crates (rand, serde, serde_json)

I learned a lot from this project that helped me to understand Rust’s ownership/borrowing rules, error handling with Result, and JSON
serialization techniques. It was nice to create a project that I see a lot of people in my life using and knowing that I can create something that
can be used all around the world one day.

[Software Demo Video](http://youtube.link.goes.here)

# Development Environment

 - Language & Toolchain: Rust 1.65+, Cargo, rustc

 - Editor: Visual Studio Code with rust-analyzer extension

Crates Used:

 - rand: for secure random password generation

 - serde + serde_json: for reading and writing entries to passwords.json

Platform: Windows 11

# Useful Websites

- [The Rust Book](https://doc.rust-lang.org/book/)
- [Rand Documentation](https://docs.rs/rand/)
- [Rust Tutorial](https://google.github.io/comprehensive-rust/)

# Future Work

 - Add AES encryption to the JSON file for secure at-rest storage

 - Implement a master password prompt and in-memory decryption timer

 - Support editing and deleting individual entries via CLI

 - Expose non-interactive flags for scripting use (e.g., --add, --generate)

 - Build a minimal TUI using crossterm or tui-rs for enhanced user experience