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
        # Note: geometric embeddings (HOG+histogram) have lower cosine similarity than
        # full ArcFace ONNX embeddings, so thresholds are calibrated accordingly.
        # ArcFace ONNX (when available): use 0.85 / 0.70
        # Geometric fallback:            use 0.65 / 0.40
        high_thresh = 0.65
        low_thresh  = 0.40

        if similarity_score >= high_thresh:
            # Strong match — always allow if liveness is valid
            decision = "ALLOW"
            reason = "Strong facial structure match confirmed."
        elif similarity_score >= low_thresh:
            if liveness_valid:
                # Moderate match + liveness OK — allow regardless of device trust
                # (first-time devices will never be trusted, so we can't block here)
                decision = "ALLOW"
                reason = "Moderate facial structure match with valid liveness."
            else:
                decision = "CHALLENGE"
                reason = "Moderate match but liveness indicators are weak."
        else:
            decision = "DENY"
            reason = f"Face similarity score ({similarity_score:.3f}) is below the minimum threshold ({low_thresh})."

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
            "You are a biometric authentication security expert. "
            "Analyze a Face ID login attempt and decide: ALLOW, DENY, or CHALLENGE.\n\n"
            "IMPORTANT — this system uses a geometric HOG+histogram face embedding (NOT ArcFace ONNX), "
            "so similarity scores are LOWER than typical ArcFace systems. "
            "Use these adjusted thresholds:\n"
            "- score >= 0.65 + liveness valid → ALLOW\n"
            "- score >= 0.40 + liveness valid → ALLOW (moderate match)\n"
            "- score < 0.40 → DENY\n"
            "- Never CHALLENGE just because the device is untrusted on a first login.\n"
            "Output a JSON object matching the schema."
        )

        user_prompt = (
            f"--- Biometric Attempt ---\n"
            f"Cosine Similarity Score: {similarity_score:.4f}\n"
            f"Liveness Valid: {liveness_valid}\n"
            f"Device Trusted: {device_trusted}\n"
            f"Recent Failures (10m): {recent_failures_count}\n"
            f"IP Anomaly: {ip_anomaly}\n"
            f"Liveness Data: {liveness_data}\n"
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
