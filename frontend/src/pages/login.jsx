import { useNavigate } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import {
  sendOTP,
  verifyOTP,
  googleLogin,
  githubLogin,
  getCurrentUser,
  setEmail,
  clearError,
  resetAuthFlow,
} from "@/redux/slices/userSlice";

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

  const {
    loading,
    error,
    authStep: step,
    email,
    transactionID,
    isAuthenticated,
    onboardingCompleted,
  } = useSelector((state) => state.user);

  const [otpDigits, setOtpDigits] = useState(Array(OTP_LENGTH).fill(""));
  const [cooldown, setCooldown] = useState(0);

  const inputRefs = useRef([]);

  useEffect(() => {
    if (cooldown <= 0) return;
    const id = setInterval(() => setCooldown((c) => c - 1), 1000);
    return () => clearInterval(id);
  }, [cooldown]);

  useEffect(() => {
    if (!isAuthenticated) return;
    navigate(onboardingCompleted ? "/app/dashboard" : "/onboarding");
  }, [isAuthenticated, onboardingCompleted, navigate]);

  console.log(onboardingCompleted);
  useEffect(() => {
    if (step === "otp" && otpDigits.every((d) => d !== "")) {
      handleVerifyOTP();
    }
  }, [otpDigits]);

  const handleSendOTP = async (e) => {
    e?.preventDefault();
    dispatch(clearError());
    const result = await dispatch(sendOTP(email));
    if (sendOTP.fulfilled.match(result)) {
      setCooldown(RESEND_COOLDOWN);
      setTimeout(() => inputRefs.current[0]?.focus(), 100);
    }
  };

  const handleResend = async () => {
    setOtpDigits(Array(OTP_LENGTH).fill(""));
    dispatch(clearError());
    await handleSendOTP();
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
    pasted.split("").forEach((char, i) => (updated[i] = char));
    setOtpDigits(updated);
    const nextEmpty = Math.min(pasted.length, OTP_LENGTH - 1);
    inputRefs.current[nextEmpty]?.focus();
  };

  const handleVerifyOTP = async (e) => {
    e?.preventDefault();
    if (loading) return;
    dispatch(clearError());

    const result = await dispatch(verifyOTP({ transactionID, otp: otpDigits.join("") }));

    if (verifyOTP.fulfilled.match(result)) {
      // verify_otp returns no user — fetch it to get onboarding status for redirect
      await dispatch(getCurrentUser());
    } else {
      setOtpDigits(Array(OTP_LENGTH).fill(""));
      setTimeout(() => inputRefs.current[0]?.focus(), 50);
    }
  };

  return (
    <AuthShell
      title={step === "email" ? "Sign in to Interleet" : "Check your inbox"}
      subtitle={
        step === "email"
          ? "Welcome back. Pick up where you left off."
          : `We sent a 6-digit code to ${email}`
      }
    >
      {step === "email" && (
        <>
          <div className="grid grid-cols-2 gap-2">
            {/* GitHub */}
            <Button
              variant="outline"
              type="button"
              onClick={() => dispatch(githubLogin())}
              className="w-full border-zinc-700 bg-zinc-950 text-white transition-all duration-200 ease-out hover:bg-zinc-900 hover:border-zinc-600 active:scale-[0.98]"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 128 128"
                className="mr-2 h-4 w-4 shrink-0"
              >
                <g fill="#ffffff">
                  <path
                    fillRule="evenodd"
                    clipRule="evenodd"
                    d="M64 5.103c-33.347 0-60.388 27.035-60.388 60.388 0 26.682 17.303 49.317 41.297 57.303 3.017.56 4.125-1.31 4.125-2.905 0-1.44-.056-6.197-.082-11.243-16.8 3.653-20.345-7.125-20.345-7.125-2.747-6.98-6.705-8.836-6.705-8.836-5.48-3.748.413-3.67.413-3.67 6.063.425 9.257 6.223 9.257 6.223 5.386 9.23 14.127 6.562 17.573 5.02.542-3.903 2.107-6.568 3.834-8.076-13.413-1.525-27.514-6.704-27.514-29.843 0-6.593 2.36-11.98 6.223-16.21-.628-1.52-2.695-7.662.584-15.98 0 0 5.07-1.623 16.61 6.19C53.7 35 58.867 34.327 64 34.304c5.13.023 10.3.694 15.127 2.033 11.526-7.813 16.59-6.19 16.59-6.19 3.287 8.317 1.22 14.46.593 15.98 3.872 4.23 6.215 9.617 6.215 16.21 0 23.194-14.127 28.3-27.574 29.796 2.167 1.874 4.097 5.55 4.097 11.183 0 8.08-.07 14.583-.07 16.572 0 1.607 1.088 3.49 4.148 2.897 23.98-7.994 41.263-30.622 41.263-57.294C124.388 32.14 97.35 5.104 64 5.104z"
                  />
                </g>
              </svg>
              GitHub
            </Button>

            {/* Google */}
            <Button
              variant="outline"
              type="button"
              onClick={() => dispatch(googleLogin())}
              className="w-full border-zinc-700 bg-zinc-950 text-white transition-all duration-200 ease-out hover:bg-zinc-900 hover:border-zinc-600 active:scale-[0.98]"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 128 128"
                className="mr-2 h-4 w-4 shrink-0"
              >
                <path
                  fill="#fff"
                  d="M44.59 4.21a63.28 63.28 0 004.33 120.9 67.6 67.6 0 0032.36.35 57.13 57.13 0 0025.9-13.46 57.44 57.44 0 0016-26.26 74.33 74.33 0 001.61-33.58H65.27v24.69h34.47a29.72 29.72 0 01-12.66 19.52 36.16 36.16 0 01-13.93 5.5 41.29 41.29 0 01-15.1 0A37.16 37.16 0 0144 95.74a39.3 39.3 0 01-14.5-19.42 38.31 38.31 0 010-24.63 39.25 39.25 0 019.18-14.91A37.17 37.17 0 0176.13 27a34.28 34.28 0 0113.64 8q5.83-5.8 11.64-11.63c2-2.09 4.18-4.08 6.15-6.22A61.22 61.22 0 0087.2 4.59a64 64 0 00-42.61-.38z"
                />
                <path
                  fill="#e33629"
                  d="M44.59 4.21a64 64 0 0142.61.37 61.22 61.22 0 0120.35 12.62c-2 2.14-4.11 4.14-6.15 6.22Q95.58 29.23 89.77 35a34.28 34.28 0 00-13.64-8 37.17 37.17 0 00-37.46 9.74 39.25 39.25 0 00-9.18 14.91L8.76 35.6A63.53 63.53 0 0144.59 4.21z"
                />
                <path
                  fill="#f8bd00"
                  d="M3.26 51.5a62.93 62.93 0 015.5-15.9l20.73 16.09a38.31 38.31 0 000 24.63q-10.36 8-20.73 16.08a63.33 63.33 0 01-5.5-40.9z"
                />
                <path
                  fill="#587dbd"
                  d="M65.27 52.15h59.52a74.33 74.33 0 01-1.61 33.58 57.44 57.44 0 01-16 26.26c-6.69-5.22-13.41-10.4-20.1-15.62a29.72 29.72 0 0012.66-19.54H65.27V52.15z"
                />
                <path
                  fill="#319f43"
                  d="M8.75 92.4l20.73-16.08A39.3 39.3 0 0044 95.74a37.16 37.16 0 0014.08 6.08 41.29 41.29 0 0015.1 0 36.16 36.16 0 0013.93-5.5c6.69 5.22 13.41 10.4 20.1 15.62a57.13 57.13 0 01-25.9 13.47 67.6 67.6 0 01-32.36-.35 63 63 0 01-23-11.59A63.73 63.73 0 018.75 92.4z"
                />
              </svg>
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
            {error && <p className="text-sm text-red-400">{error}</p>}
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Sending code…" : "Continue"}
            </Button>
          </form>
        </>
      )}

      {/* ── OTP step ── */}
      {step === "otp" && (
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

          {error && <p className="text-center text-sm text-red-400">{error}</p>}

          <Button
            type="submit"
            className="w-full"
            disabled={loading || otpDigits.some((d) => d === "")}
          >
            {loading ? "Verifying…" : "Verify code"}
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
