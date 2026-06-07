import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException

# Mock the database before importing controllers
import app.controllers.passkey_controller as pc
from app.models.passkey_models import (
    PasskeyRegisterOptionsRequest,
    PasskeyRegisterVerifyRequest,
    PasskeyLoginOptionsRequest,
    PasskeyLoginVerifyRequest,
)

class TestPasskeySecurity(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Reset database mock
        pc.db = MagicMock()
        pc.db.users = MagicMock()
        pc.db.webauthn_credentials = MagicMock()

    @patch("app.controllers.passkey_controller.generate_registration_options")
    async def test_register_options_generates_correctly(self, mock_gen_options):
        # Arrange
        payload = PasskeyRegisterOptionsRequest(email="user@company.com")
        request = MagicMock()
        request.headers = {"origin": "http://localhost:5173"}
        request.session = {}
        
        user_doc = {"user_id": "user123", "email": "user@company.com"}
        pc.db.users.find_one = AsyncMock(return_value=user_doc)

        mock_options = MagicMock()
        mock_options.challenge = b"test_challenge_bytes_12345"
        mock_gen_options.return_value = mock_options

        # Act
        with patch("app.controllers.passkey_controller.options_to_json", return_value='{"challenge": "test"}'):
            res = await pc.PasskeyController.register_options(payload, request)

        # Assert
        self.assertEqual(res, {"challenge": "test"})
        self.assertEqual(request.session["registration_challenge"], b"test_challenge_bytes_12345".hex())
        self.assertEqual(request.session["registration_user_id"], "user123")
        self.assertEqual(request.session["registration_rp_id"], "localhost")
        self.assertEqual(request.session["registration_origin"], "http://localhost:5173")

    @patch("app.controllers.passkey_controller.verify_registration_response")
    async def test_register_verify_saves_credentials(self, mock_verify):
        # Arrange
        payload = PasskeyRegisterVerifyRequest(
            email="user@company.com",
            credential={"id": "cred_id_123", "type": "public-key"}
        )
        request = MagicMock()
        request.session = {
            "registration_challenge": b"challenge_123".hex(),
            "registration_user_id": "user123",
            "registration_rp_id": "localhost",
            "registration_origin": "http://localhost:5173",
        }

        mock_verified = MagicMock()
        mock_verified.credential_id = b"cred_id_bytes"
        mock_verified.credential_public_key = b"pubkey_bytes"
        mock_verified.sign_count = 0
        mock_verify.return_value = mock_verified

        pc.db.webauthn_credentials.update_one = AsyncMock()
        pc.db.users.update_one = AsyncMock()

        # Act
        res = await pc.PasskeyController.register_verify(payload, request)

        # Assert
        self.assertTrue(res["success"])
        pc.db.webauthn_credentials.update_one.assert_called_once()
        pc.db.users.update_one.assert_called_once_with(
            {"user_id": "user123"},
            {"$set": {"passkey_registered": True, "face_registered": True, "updated_at": unittest.mock.ANY}}
        )
        self.assertNotIn("registration_challenge", request.session)

    @patch("app.controllers.passkey_controller.generate_authentication_options")
    async def test_login_options_finds_stored_keys(self, mock_gen_auth_options):
        # Arrange
        payload = PasskeyLoginOptionsRequest(email="user@company.com")
        request = MagicMock()
        request.headers = {"origin": "http://localhost:5173"}
        request.session = {}

        user_doc = {"user_id": "user123", "email": "user@company.com"}
        pc.db.users.find_one = AsyncMock(return_value=user_doc)

        cred_doc = [{"userId": "user123", "credentialId": "0102030405060708090a", "publicKey": "0a0b0c0d", "signCount": 0}]
        pc.db.webauthn_credentials.find = MagicMock()
        pc.db.webauthn_credentials.find().to_list = AsyncMock(return_value=cred_doc)

        mock_options = MagicMock()
        mock_options.challenge = b"auth_challenge_bytes"
        mock_gen_auth_options.return_value = mock_options

        # Act
        with patch("app.controllers.passkey_controller.options_to_json", return_value='{"challenge": "test"}'):
            res = await pc.PasskeyController.login_options(payload, request)

        # Assert
        self.assertEqual(res, {"challenge": "test"})
        self.assertEqual(request.session["authentication_challenge"], b"auth_challenge_bytes".hex())
        self.assertEqual(request.session["authentication_user_id"], "user123")

    @patch("app.controllers.passkey_controller.verify_authentication_response")
    @patch("app.controllers.passkey_controller.base64url_to_bytes")
    async def test_login_verify_authenticates_user(self, mock_b64_to_bytes, mock_verify_auth):
        # Arrange
        payload = PasskeyLoginVerifyRequest(
            email="user@company.com",
            credential={"id": "base64url_cred_id"}
        )
        request = MagicMock()
        request.session = {
            "authentication_challenge": b"auth_challenge".hex(),
            "authentication_user_id": "user123",
            "authentication_rp_id": "localhost",
            "authentication_origin": "http://localhost:5173",
        }
        response = MagicMock()

        mock_b64_to_bytes.return_value = b"cred_bytes"
        
        cred_doc = {"_id": "mock_id", "userId": "user123", "credentialId": b"cred_bytes".hex(), "publicKey": b"pub_key".hex(), "signCount": 5}
        pc.db.webauthn_credentials.find_one = AsyncMock(return_value=cred_doc)
        pc.db.webauthn_credentials.update_one = AsyncMock()

        user_doc = {"user_id": "user123", "email": "user@company.com", "username": "testuser"}
        pc.db.users.find_one = AsyncMock(return_value=user_doc)
        pc.db.users.update_one = AsyncMock()

        mock_verified = MagicMock()
        mock_verified.new_sign_count = 6
        mock_verify_auth.return_value = mock_verified

        # Act
        with patch("app.controllers.passkey_controller.generate_token") as mock_gen_token:
            res = await pc.PasskeyController.login_verify(payload, request, response)

            # Assert
            self.assertTrue(res["success"])
            self.assertEqual(res["user"]["user_id"], "user123")
            mock_gen_token.assert_called_once_with("user123", response)
            pc.db.webauthn_credentials.update_one.assert_called_once()
            self.assertNotIn("authentication_challenge", request.session)

if __name__ == "__main__":
    unittest.main()
