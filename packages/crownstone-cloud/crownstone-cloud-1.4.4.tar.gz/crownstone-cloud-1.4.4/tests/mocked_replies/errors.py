auth_error = {
    "error": {
        "statusCode": 401,
        "name": "Authentication failed",
        "message": "Authentication fail",
        "code": "LOGIN_FAILED",
    }
}

not_verified = {
    "error": {
        "statusCode": 401,
        "name": "Authentication failed",
        "message": "Authentication fail",
        "code": "LOGIN_FAILED_EMAIL_NOT_VERIFIED",
    }
}

access_token_expired = {
    "error": {
        "statusCode": 401,
        "name": "Authentication failed",
        "message": "Authentication fail",
        "code": "INVALID_TOKEN",
    }
}