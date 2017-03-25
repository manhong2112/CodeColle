//  y
//  2 _|_|_
//  1 _|_|_
//  0  | |
//    0 1 2 x
use std::collections::LinkedList;
use std::io::stdin;

struct Step {
    x: i8,
    y: i8,
    who: i8
}
struct EachRecord {
    win: Vec<i8>,
    draw: Vec<i8>,
    lose: Vec<i8>
}
fn main() {
    let mut table : LinkedList<Step> = LinkedList::new();
    let mut record : [EachRecord; 19683];
    loop {
        if end_check(&table) {
            table.clear();
        }
        let mut input = String::new();
        match stdin().read_line(&mut input) {
            Ok(_) => {},
            Err(_) => continue,
        };
        let tmp: Vec<&str> = input.trim().split(' ').collect();
        let x = tmp[0].parse::<i8>().unwrap();
        let y = tmp[1].parse::<i8>().unwrap();
        check(&mut table, x, y, 1);
        print(&table);
    }
}

fn check(table: &mut LinkedList<Step>, x: i8, y: i8, who: i8) {
    table.push_back(Step { x: x, y: y, who: who});
}

fn end_check(table: &LinkedList<Step>) -> bool {
    return table.len() > 9;
}

fn add2record(table: &LinkedList<Step>, record: &mut [EachRecord; 19683]) {

}

fn print(table: &LinkedList<Step>) {
    let mut t : [[i8; 3]; 3] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
    for i in table.iter() {
        t[i.x as usize][i.y as usize] = i.who;
    }
    for y in (0..3).rev() {
        for x in 0..3 {
            print!("{}", t[x][y]);
        }
        println!();
    }
}