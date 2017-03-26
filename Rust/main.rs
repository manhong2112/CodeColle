//  y
//  2 _|_|_
//  1 _|_|_
//  0  | |
//    0 1 2 x
use std::collections::LinkedList;
use std::io::stdin;

struct Step {
    loc: Loc,
    who: i8
}

struct Loc {
    x: i8,
    y: i8,
}

struct EachRecord {
    win: Vec<Loc>,
    draw: Vec<Loc>,
    lose: Vec<Loc>
}
fn main() {
    let mut table : LinkedList<Step> = LinkedList::new();
    let mut record : [EachRecord; 19683];
    loop {
        if end_check(&table) {
            table.clear();
        }
        print(&table);
        let mut input = String::new();
        match stdin().read_line(&mut input) {
            Ok(_) => {},
            Err(_) => continue,
        };
        let tmp: Vec<&str> = input.trim().split(' ').collect();
        let x = tmp[0].parse::<i8>().unwrap();
        let y = tmp[1].parse::<i8>().unwrap();
        check(&mut table, x, y, 1);
    }
}

fn check(table: &mut LinkedList<Step>, x: i8, y: i8, who: i8) {
    table.push_back(Step { loc: Loc{x:x, y:y}, who: who});
}

fn end_check(table: &LinkedList<Step>) -> bool {
    return table.len() > 8;
}

fn add2record(table: &[[i8; 3]; 3], record: &mut [EachRecord; 19683]) {
    // Step(x, y, who) -> EachRecord[table]: 
    //                      win: Vec<Loc NextStep>,  draw: Vec<Loc>,  lose: Vec<Loc>
    let t = table_status(table);
}

fn table_status(table: &[[i8; 3]; 3]) -> i8 {
    // ret
    // 0 = unfinished
    // 1 = win 0
    // 2 = win 1
    // 3 = draw

    // xxx * 3 x      x
    //         x * 3   x  * 3
    //         x        x
    let t1 = test1(&table);
    let t2 = test2(&table);
    let t3 = test3(&table);
    return 0;
}

fn test1(table: &[[i8; 3]; 3]) -> i8 {
    for i in 0 .. 3 {
        if table[i][0] != 0 &&
           table[i][0] == table[i][1] &&
           table[i][1] == table[i][2] {
            return table[i][0];
        }
    }
    return 0;
}

fn test2(table: &[[i8; 3]; 3]) -> i8 {
    for i in 0 .. 3 {
        if table[0][i] != 0 &&
           table[1][i] == table[0][i] &&
           table[2][i] == table[1][i] {
            return table[0][i];
        }
    }
    return 0;
}

fn test3(table: &[[i8; 3]; 3]) -> i8 {
    //  y
    //  2 *|_|*
    //  1 _|*|_
    //  0 *| |*
    //    0 1 2 x
    if table[0][0] != 0 && table[0][0] == table[1][1] && table[1][1] == table[2][2] {
        return table[0][0];
    } else if table[2][0] != 0 && table[2][0] == table[1][1] && table[1][1] == table[0][2] {
        return table[2][0];
    } else {
        return 0;
    }
}

fn steplist2array(table: &LinkedList<Step>) -> [[i8; 3]; 3] {
    let mut t : [[i8; 3]; 3] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
    for i in table.iter() {
        t[i.loc.x as usize][i.loc.y as usize] = i.who;
    }
    return t;
}

fn print(table: &LinkedList<Step>) {
    let t = steplist2array(&table);
    for y in (0..3).rev() {
        for x in 0..3 {
            print!("{}", t[x][y]);
        }
        println!();
    }
}