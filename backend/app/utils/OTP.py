import json
import uuid
import hashlib
from fastapi import HTTPException
from app.lib.redis import Redis_client


def hashOTP(OTP: str) -> str:
    return hashlib.sha256(OTP.encode()).hexdigest()


async def sendOTP(email: str, OTP: str):
    try:
        transactionID = str(uuid.uuid4())

        Redis_client.setex(
            f"otp:{transactionID}",
            300,
            json.dumps({"email": email, "hashedOTP": hashOTP(str(OTP)), "attempts": 0}),
        )

        print("OTP FOR TESTING =", OTP)
        print("Transaction ID =", transactionID)

        return {
            "transaction_ID": transactionID,
            "message": "OTP SENT SUCCESSFULLY",
            "success": True,
            "transactionID": transactionID,
        }

    except Exception as e:
        print(f"ERROR IN SENDING OTP: {e}")
        raise HTTPException(
            status_code=500, detail=f"ERROR IN SENDING OTP: {str(e)}"
        ) from e



async def VerifyOTPbyUtils(transactionID: str, OTP: str):
    try:
        key = f"otp:{transactionID}"
        data = Redis_client.get(key)

        if not data:
            return {"valid": False, "reason": "OTP expired or invalid transaction ID"}

        if isinstance(data, bytes):
            data = data.decode("utf-8")

        parsed = json.loads(data)

        email = parsed["email"]
        hashedOTP = parsed["hashedOTP"]
        attempts = parsed.get("attempts", 0)

        if attempts >= 5:
            Redis_client.delete(key)
            return {
                "valid": False,
                "reason": "Too many failed attempts. Please request a new OTP.",
            }

        userHashedOTP = hashOTP(str(OTP))

        if userHashedOTP == hashedOTP:
            Redis_client.delete(key)
            return {"valid": True, "reason": "Verified", "email": email}

        Redis_client.setex(
            key,
            300,
            json.dumps(
                {
                    "email": email,
                    "hashedOTP": hashedOTP,
                    "attempts": attempts + 1,
                }
            ),
        )

        remaining_attempts = 5 - (attempts + 1)
        return {
            "valid": False,
            "reason": f"Invalid OTP. {remaining_attempts} attempts remaining.",
        }

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {"valid": False, "reason": "Invalid OTP data format"}
    except KeyError as e:
        print(f"Missing key in OTP data: {e}")
        return {"valid": False, "reason": "Corrupted OTP data"}
    except Exception as e:
        print(f"Unexpected error in VerifyOTPbyUtils: {e}")
        return {"valid": False, "reason": "An error occurred during verification"}
