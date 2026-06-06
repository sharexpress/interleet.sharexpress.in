import logging
from typing import Dict, Any
from pydantic import BaseModel, Field
from app.ai.services.ai_client import ai_client

logger = logging.getLogger(__name__)

class AuthDecisionSchema(BaseModel):
    decision: str = Field(..., description="ALLOW, DENY, or CHALLENGE")
    confidence_score: float = Field(..., description="Overall confidence score from 0.0 to 1.0")
    liveness_valid: bool = Field(..., description="True if biometric liveness verification passed")
    threat_detected: bool = Field(..., description="True if anomalies, replay attacks, or spoof attempts are detected")
    reasoning: str = Field(..., description="Explanation of the decision and factors analyzed")


class LangChainAuthDecisionService:
    @staticmethod
    def programmatic_decision(
        similarity_score: float,
        liveness_valid: bool,
        device_trusted: bool,
        recent_failures_count: int,
        ip_anomaly: bool,
        liveness_data: Dict[str, Any]
    ) -> AuthDecisionSchema:
        """Rule-based security fallback in case the AI Client / LLM is unavailable."""
        logger.info("Executing rule-based biometric verification fallback")
        
        threat_detected = False
        reasoning_parts = []
        
        # 1. Check severe security factors
        if recent_failures_count >= 5:
            threat_detected = True
            reasoning_parts.append("Rate limiting triggered: too many recent failures.")
        if ip_anomaly and not device_trusted:
            reasoning_parts.append("IP address anomaly detected on untrusted device.")
            
        # 2. Score mapping
        # Let's assess threshold bounds (0.70 is standard high confidence for ArcFace vectors)
        if threat_detected:
            return AuthDecisionSchema(
                decision="DENY",
                confidence_score=float(similarity_score * 0.5),
                liveness_valid=liveness_valid,
                threat_detected=True,
                reasoning="Authentication blocked due to multiple threat indicators: " + " ".join(reasoning_parts)
            )
            
        # Biometric decision matrix
        if similarity_score >= 0.85:
            if liveness_valid:
                decision = "ALLOW"
                reason = "Strong facial structure match with valid liveness parameters."
            else:
                decision = "CHALLENGE"
                reason = "Strong facial structure match, but liveness indicators are weak or incomplete."
        elif similarity_score >= 0.70:
            if liveness_valid and device_trusted:
                decision = "ALLOW"
                reason = "Moderate facial structure match with valid liveness on a trusted device."
            elif liveness_valid:
                decision = "CHALLENGE"
                reason = "Moderate facial structure match and valid liveness, but device is untrusted. Issuing additional challenge."
            else:
                decision = "CHALLENGE"
                reason = "Moderate facial structure match, but missing liveness confirmation."
        else:
            decision = "DENY"
            reason = f"Face similarity score ({similarity_score:.2f}) is below the minimum authorization threshold."
            
        return AuthDecisionSchema(
            decision=decision,
            confidence_score=similarity_score,
            liveness_valid=liveness_valid,
            threat_detected=threat_detected,
            reasoning=reason
        )

    @staticmethod
    async def evaluate_auth_request(
        similarity_score: float,
        liveness_valid: bool,
        device_trusted: bool,
        recent_failures_count: int,
        ip_anomaly: bool,
        liveness_data: Dict[str, Any]
    ) -> AuthDecisionSchema:
        """
        Evaluate Face ID login request using LangChain LLM reasoning and threat modeling.
        Falls back to rule-based verification on any LLM provider error.
        """
        system_prompt = (
            "You are a computer vision security expert and biometrics risk analyzer. "
            "Analyze the biometric and context metrics of a Face ID login attempt. "
            "Determine if the user should be: \n"
            "- ALLOW: Match is secure, liveness is verified, no threat indicators.\n"
            "- DENY: Low similarity, spoofing signs, or high security risk.\n"
            "- CHALLENGE: Match is borderline, or device is untrusted. Needs challenge step.\n\n"
            "Evaluate factors carefully: check Face Similarity (usually >0.70 is match, >0.85 is strong), "
            "liveness validation status, device fingerprint trust status, recent failure count, "
            "and IP anomaly indicators."
        )
        
        user_prompt = (
            f"--- Biometric Attempt Telemetry ---\n"
            f"Face Embedding Cosine Similarity: {similarity_score:.4f}\n"
            f"Biometric Liveness Verification Result: {liveness_valid}\n"
            f"Liveness Telemetry: {liveness_data}\n"
            f"Is Device Fingerprint Trusted: {device_trusted}\n"
            f"Recent Login Failures (last 10m): {recent_failures_count}\n"
            f"IP Anomaly Indicator: {ip_anomaly}\n\n"
            f"Output the evaluation as a JSON object matching the requested schema."
        )
        
        try:
            decision = await ai_client.generate_json(
                system=system_prompt,
                user=user_prompt,
                schema=AuthDecisionSchema,
                temperature=0.1
            )
            logger.info("LangChain biometrics analysis returned: %s (Confidence: %.2f)", decision.decision, decision.confidence_score)
            return decision
        except Exception as e:
            logger.error("LangChain authentication analysis failed: %s. Relying on programmatic rules.", e)
            return LangChainAuthDecisionService.programmatic_decision(
                similarity_score=similarity_score,
                liveness_valid=liveness_valid,
                device_trusted=device_trusted,
                recent_failures_count=recent_failures_count,
                ip_anomaly=ip_anomaly,
                liveness_data=liveness_data
            )
