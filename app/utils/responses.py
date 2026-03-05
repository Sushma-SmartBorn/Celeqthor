

def success_response(
    data: any = None,
    message: str = "Success",
    status: int = 200
) -> dict:
    return {
        "status": status,
        "message": message,
        "data": data if data is not None else []
    }

def error_response(
    message: str,
    status: int = 400,
    data: any = None
) -> dict:
    return {
        "status": status,
        "message": message,
        "data": data if data is not None else []
    }
