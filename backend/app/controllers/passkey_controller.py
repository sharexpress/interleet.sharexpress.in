import logging
import urllib.parse
import json
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import HTTPException, Response, Request
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
    base64url_to_bytes,
)
from webauthn.helpers.structs import (
    AttestationConveyancePreference,
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    PublicKeyCredentialDescriptor,
)

from app.core.db import get_db
from app.utils.JWT import generate_token
from app.models.passkey_models import (
    PasskeyRegisterOptionsRequest,
    PasskeyRegisterVerifyRequest,
    PasskeyLoginOptionsRequest,
    PasskeyLoginVerifyRequest,
)

logger = logging.getLogger(__name__)
db = get_db()

class PasskeyController:
    @classmethod
    def _get_rp_details(cls, request: Request) -> tuple[str, str]:
        """Dynamically gets relying party ID (domain) and origin from request headers."""
        origin = request.headers.get("origin", "http://localhost:5173")
        parsed_origin = urllib.parse.urlparse(origin)
        rp_id = parsed_origin.hostname or "localhost"
        return rp_id, origin

    @classmethod
    async def register_options(
        cls,
        payload: PasskeyRegisterOptionsRequest,
        request: Request,
        current_user: Optional[dict] = None,
    ):
        """Generates options for registering a new passkey."""
        try:
            email = None
            if current_user and current_user.get("user"):
                user = current_user["user"]
                email = user.get("email")
            else:
                email = payload.email.strip().lower() if payload.email else None

            if not email:
                raise HTTPException(
                    status_code=400,
                    detail="Email is required for passkey registration."
                )

            user = await db.users.find_one({"email": email})
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User account not found."
                )

            rp_id, origin = cls._get_rp_details(request)

            registration_options = generate_registration_options(
                rp_id=rp_id,
                rp_name="Interleet Platform",
                user_name=email,
                user_id=str(user["user_id"]).encode("utf-8"),
                user_display_name=user.get("full_name", email),
                attestation=AttestationConveyancePreference.NONE,
                authenticator_selection=AuthenticatorSelectionCriteria(
                    authenticator_attachment=AuthenticatorAttachment.PLATFORM, # Focuses on device biometrics (Apple Face ID/Touch ID)
                    user_verification=UserVerificationRequirement.REQUIRED,
                ),
            )

            # Store verification details in session
            request.session["registration_challenge"] = registration_options.challenge.hex()
            request.session["registration_user_id"] = str(user["user_id"])
            request.session["registration_rp_id"] = rp_id
            request.session["registration_origin"] = origin

            logger.info("Generated passkey registration options for user: %s", email)
            return json.loads(options_to_json(registration_options))

        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Failed to generate passkey registration options: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def register_verify(
        cls,
        payload: PasskeyRegisterVerifyRequest,
        request: Request,
        current_user: Optional[dict] = None,
    ):
        """Verifies the registered passkey credential response and stores it."""
        try:
            expected_challenge = request.session.pop("registration_challenge", None)
            user_id = request.session.pop("registration_user_id", None)
            expected_rp_id = request.session.pop("registration_rp_id", None)
            expected_origin = request.session.pop("registration_origin", None)

            if not expected_challenge or not user_id:
                raise HTTPException(
                    status_code=400,
                    detail="Registration session expired or invalid. Please try again."
                )

            verification = verify_registration_response(
                credential=payload.credential,
                expected_challenge=bytes.fromhex(expected_challenge),
                expected_rp_id=expected_rp_id,
                expected_origin=expected_origin,
                require_user_verification=True,
            )

            credential_id_hex = verification.credential_id.hex()

            # Insert passkey credential into database
            await db.webauthn_credentials.update_one(
                {"credentialId": credential_id_hex},
                {
                    "$set": {
                        "userId": user_id,
                        "credentialId": credential_id_hex,
                        "publicKey": verification.credential_public_key.hex(),
                        "signCount": verification.sign_count,
                        "createdAt": datetime.utcnow(),
                    }
                },
                upsert=True,
            )

            # Flag user as biometric registered
            await db.users.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "passkey_registered": True,
                        "face_registered": True, # Also marks face as registered for seamless auth integration
                        "updated_at": datetime.utcnow(),
                    }
                },
            )

            logger.info("Successfully registered WebAuthn Passkey for user ID: %s", user_id)
            return {"success": True, "message": "Passkey registered successfully"}

        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Failed to verify passkey registration: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def login_options(
        cls,
        payload: PasskeyLoginOptionsRequest,
        request: Request,
    ):
        """Generates options for authenticating with a passkey (1-1 matching)."""
        try:
            email = payload.email.strip().lower()
            user = await db.users.find_one({"email": email})
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User account not found."
                )

            # Retrieve registered credentials for the user
            credentials = await db.webauthn_credentials.find({"userId": str(user["user_id"])}).to_list(length=10)
            if not credentials:
                raise HTTPException(
                    status_code=400,
                    detail="No biometrics or passkeys registered for this email address."
                )

            rp_id, origin = cls._get_rp_details(request)

            allow_credentials = [
                PublicKeyCredentialDescriptor(id=bytes.fromhex(c["credentialId"]))
                for c in credentials
            ]

            authentication_options = generate_authentication_options(
                rp_id=rp_id,
                allow_credentials=allow_credentials,
                user_verification=UserVerificationRequirement.REQUIRED,
            )

            # Save verification options to session
            request.session["authentication_challenge"] = authentication_options.challenge.hex()
            request.session["authentication_user_id"] = str(user["user_id"])
            request.session["authentication_rp_id"] = rp_id
            request.session["authentication_origin"] = origin

            logger.info("Generated passkey authentication options for email: %s", email)
            return json.loads(options_to_json(authentication_options))

        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Failed to generate passkey login options: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def login_verify(
        cls,
        payload: PasskeyLoginVerifyRequest,
        request: Request,
        response: Response,
    ):
        """Verifies the passkey authentication signature and signs the user in."""
        try:
            expected_challenge = request.session.pop("authentication_challenge", None)
            user_id = request.session.pop("authentication_user_id", None)
            expected_rp_id = request.session.pop("authentication_rp_id", None)
            expected_origin = request.session.pop("authentication_origin", None)

            if not expected_challenge or not user_id:
                raise HTTPException(
                    status_code=400,
                    detail="Authentication session expired or invalid. Please retry."
                )

            # Map the incoming base64url credential id to our hex credentialId
            raw_credential_id = payload.credential.get("id")
            if not raw_credential_id:
                raise HTTPException(status_code=400, detail="Invalid credential payload structure.")

            credential_id_bytes = base64url_to_bytes(raw_credential_id)
            credential_id_hex = credential_id_bytes.hex()

            cred = await db.webauthn_credentials.find_one({
                "userId": user_id,
                "credentialId": credential_id_hex,
            })
            if not cred:
                raise HTTPException(
                    status_code=401,
                    detail="This credential is not registered to this user account."
                )

            verification = verify_authentication_response(
                credential=payload.credential,
                expected_challenge=bytes.fromhex(expected_challenge),
                expected_rp_id=expected_rp_id,
                expected_origin=expected_origin,
                credential_public_key=bytes.fromhex(cred["publicKey"]),
                credential_current_sign_count=cred["signCount"],
                require_user_verification=True,
            )

            # Update sign count in database
            await db.webauthn_credentials.update_one(
                {"_id": cred["_id"]},
                {"$set": {"signCount": verification.new_sign_count}}
            )

            # Fetch user and sign in
            user = await db.users.find_one({"user_id": user_id})
            if not user:
                raise HTTPException(status_code=404, detail="User account not found.")

            # Update login timestamps
            await db.users.update_one(
                {"user_id": user_id},
                {"$set": {"last_login": datetime.utcnow(), "updated_at": datetime.utcnow()}},
            )

            # Generate JWT cookie
            generate_token(user_id, response)

            logger.info("Successfully authenticated user via WebAuthn Passkey: %s", user.get("email"))

            return {
                "success": True,
                "message": "Authenticated successfully via native biometrics",
                "user": {
                    "user_id": user_id,
                    "email": user.get("email"),
                    "username": user.get("username"),
                    "full_name": user.get("full_name"),
                    "onboarding_completed": user.get("onboarding_completed", False),
                    "avatar": user.get("avatar"),
                },
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Failed to verify passkey authentication response: %s", e)
            raise HTTPException(status_code=401, detail="Biometric verification failed.")
