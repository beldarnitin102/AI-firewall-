# Role-based traffic policies

ROLE_POLICIES = {
    "admin": {
        "allowed_ports": [80, 443, 22, 21],
        "access_level": "FULL"
    },
    "user": {
        "allowed_ports": [80, 443],
        "access_level": "LIMITED"
    }
}

def enforce_policy(role, packet):
    src_port = packet[2]

    allowed_ports = ROLE_POLICIES.get(role, {}).get("allowed_ports", [])

    if src_port in allowed_ports:
        return "ALLOW"
    else:
        return "DENY"
