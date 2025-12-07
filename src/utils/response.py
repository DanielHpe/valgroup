class Response:
    @staticmethod
    def handle_response(status: bool = False, message: str = "", data: dict = None) -> dict:
        if data is None:
            data = []

        return {
            "status": status,
            "message": message,
            "data": data
        }
