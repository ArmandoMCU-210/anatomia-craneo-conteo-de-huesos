def get_client_ip(req):
    """Obtiene la IP del cliente, respetando X-Forwarded-For si la app corre tras un proxy."""
    forwarded = req.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return req.remote_addr or "0.0.0.0"
