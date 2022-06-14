use std::net::SocketAddr;

pub fn portal_client_addrs() -> Vec<SocketAddr> {
    vec![
        SocketAddr::from(([127, 0, 0, 1], 4000)),
        SocketAddr::from(([127, 0, 0, 1], 4001)),
    ]
}



pub fn portal_admin_addrs() -> Vec<SocketAddr> {
    vec![
        SocketAddr::from(([127, 0, 0, 1], 5000)),
        SocketAddr::from(([127, 0, 0, 1], 5001)),
    ]
}

pub fn pubsub_addr() -> SocketAddr {
    SocketAddr::from(([127, 0, 0, 1], 1843))
}
