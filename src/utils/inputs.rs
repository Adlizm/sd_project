use std::io::stdin;

pub const USE_CID: u8 = 0x01;
pub const USE_TASK: u8 = 0x02;
pub const USE_BODY: u8 = 0x04;

type OString = Option<String>;

pub fn get(mask: u8) -> (OString, OString, OString) {
    let mut buf= String::new();

    let mut cid: OString = None;
    let mut task: OString = None;
    let mut body: OString = None;

    if(mask & USE_CID) != 0 {
        print!("\n\tcid: ");
        stdin().read_line(&mut buf).unwrap();
        cid = Some(buf.clone());
    }
    if(mask & USE_TASK) != 0 {
        print!("\n\ttask: ");
        stdin().read_line(&mut buf).unwrap();
        task = Some(buf.clone());
    }
    if(mask & USE_BODY) != 0 {
        print!("\n\tbody(json format): ");
        stdin().read_line(&mut buf).unwrap();
        body = Some(buf.clone());
    }
    (cid, task, body)
}

