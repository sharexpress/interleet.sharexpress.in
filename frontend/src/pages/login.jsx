import { useNavigate } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import {
  SendOTP,
  VerifyOTP,
  googleLogin,
  githubLogin,
  GetCurrentUser,
  setEmail,
  clearError,
  resetAuthFlow,
} from "@/redux/slices/userSlice";

import github from "@/assets/github.png";
import google from "@/assets/Google.png";

import { AuthShell } from "@/components/auth/AuthShell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";

const OTP_LENGTH = 6;
const RESEND_COOLDOWN = 30;

function LoginPage() {
  const navigate = useNavigate();

  const dispatch = useDispatch();

  const { loading, error, authStep, email, transactionID, isAuthenticated, onboardingCompleted } =
    useSelector((state) => state.user);

  const [otpDigits, setOtpDigits] = useState(Array(OTP_LENGTH).fill(""));

  const [cooldown, setCooldown] = useState(0);

  const inputRefs = useRef([]);

  useEffect(() => {
    dispatch(GetCurrentUser());
  }, [dispatch]);

  useEffect(() => {
    if (!isAuthenticated) return;

    navigate(onboardingCompleted ? "/app/dashboard" : "/onboarding");
  }, [isAuthenticated, onboardingCompleted, navigate]);

  useEffect(() => {
    if (authStep === "otp" && otpDigits.every((digit) => digit !== "")) {
      handleVerifyOTP();
    }
  }, [otpDigits]);

  useEffect(() => {
    if (cooldown <= 0) return;

    const timer = setInterval(() => {
      setCooldown((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [cooldown]);

  const handleSendOTP = async (e) => {
    e?.preventDefault();

    dispatch(clearError());

    const result = await dispatch(SendOTP(email));

    if (SendOTP.fulfilled.match(result)) {
      setCooldown(RESEND_COOLDOWN);

      setTimeout(() => {
        inputRefs.current[0]?.focus();
      }, 100);
    }
  };

  const handleResend = async () => {
    setOtpDigits(Array(OTP_LENGTH).fill(""));

    dispatch(clearError());

    await handleSendOTP();
  };

  const handleVerifyOTP = async (e) => {
    e?.preventDefault();

    if (loading) return;

    dispatch(clearError());

    const result = await dispatch(
      VerifyOTP({
        transactionID,
        otp: otpDigits.join(""),
      }),
    );

    if (VerifyOTP.fulfilled.match(result)) {
      await dispatch(GetCurrentUser());
    } else {
      setOtpDigits(Array(OTP_LENGTH).fill(""));

      setTimeout(() => {
        inputRefs.current[0]?.focus();
      }, 50);
    }
  };

  const handleOTPChange = (value, index) => {
    if (!/^\d?$/.test(value)) return;

    dispatch(clearError());

    const updated = [...otpDigits];

    updated[index] = value;

    setOtpDigits(updated);

    if (value && index < OTP_LENGTH - 1) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleOTPKeyDown = (e, index) => {
    if (e.key === "Backspace" && !otpDigits[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }

    if (e.key === "ArrowLeft" && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }

    if (e.key === "ArrowRight" && index < OTP_LENGTH - 1) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handlePaste = (e) => {
    e.preventDefault();

    const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, OTP_LENGTH);

    if (!pasted) return;

    const updated = Array(OTP_LENGTH).fill("");

    pasted.split("").forEach((char, index) => {
      updated[index] = char;
    });

    setOtpDigits(updated);

    const nextIndex = Math.min(pasted.length, OTP_LENGTH - 1);

    inputRefs.current[nextIndex]?.focus();
  };

  return (
    <AuthShell
      title={authStep === "email" ? "Sign in to Interleet" : "Check your inbox"}
      subtitle={
        authStep === "email"
          ? "Welcome back. Pick up where you left off."
          : `We sent a 6-digit code to ${email}`
      }
    >
      {authStep === "email" && (
        <>
          <div className="grid grid-cols-2 gap-2">
            {/* GITHUB */}

            <Button
              variant="outline"
              type="button"
              onClick={() => dispatch(githubLogin())}
              className="w-full border   border-zinc-200 bg-white text-black transition-all duration-200 ease-out hover:border-zinc-300 hover:bg-zinc-100 hover:text-black active:scale-[0.98]"
            >
              <img src={github} alt="GitHub" className="mr-2 h-4 w-4 object-contain" />
              GitHub
            </Button>

            {/* GOOGLE */}

            <Button
              variant="outline"
              type="button"
              onClick={() => dispatch(googleLogin())}
              className="w-full border order-[0.1px]b border-zinc-700 bg-zinc-950 text-white transition-all duration-200 ease-out hover:border-zinc-600 hover:bg-zinc-900 active:scale-[0.98]"
            >
              <img src={google} alt="Google" className="mr-2 h-4 w-4 object-contain" />
              Google
            </Button>
          </div>

          <div className="relative my-5 flex items-center">
            <Separator className="flex-1" />

            <span className="px-3 font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
              or
            </span>

            <Separator className="flex-1" />
          </div>

          <form className="space-y-4" onSubmit={handleSendOTP}>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>

              <Input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => dispatch(setEmail(e.target.value))}
                placeholder="you@company.com"
                autoComplete="email"
              />
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Sending code..." : "Continue"}
            </Button>
          </form>
        </>
      )}

      {authStep === "otp" && (
        <form className="space-y-6" onSubmit={handleVerifyOTP}>
          <div className="flex items-center justify-center gap-2">
            {otpDigits.map((digit, index) => (
              <Input
                key={index}
                ref={(el) => (inputRefs.current[index] = el)}
                value={digit}
                onChange={(e) => handleOTPChange(e.target.value, index)}
                onKeyDown={(e) => handleOTPKeyDown(e, index)}
                onPaste={index === 0 ? handlePaste : undefined}
                maxLength={1}
                inputMode="numeric"
                autoComplete="one-time-code"
                className="h-12 w-12 text-center text-lg font-semibold"
              />
            ))}
          </div>

          <Button
            type="submit"
            className="w-full"
            disabled={loading || otpDigits.some((digit) => digit === "")}
          >
            {loading ? "Verifying..." : "Verify code"}
          </Button>

          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <button
              type="button"
              onClick={() => {
                dispatch(resetAuthFlow());

                setOtpDigits(Array(OTP_LENGTH).fill(""));
              }}
              className="transition-colors hover:text-foreground"
            >
              ← Change email
            </button>

            <button
              type="button"
              onClick={handleResend}
              disabled={cooldown > 0 || loading}
              className="transition-colors hover:text-foreground disabled:pointer-events-none disabled:opacity-40"
            >
              {cooldown > 0 ? `Resend in ${cooldown}s` : "Resend code"}
            </button>
          </div>
        </form>
      )}
    </AuthShell>
  );
}

export default LoginPage;
