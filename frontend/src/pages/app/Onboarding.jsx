import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import { CompleteOnboarding } from "@/redux/slices/userSlice";

import { AuthShell } from "@/components/auth/AuthShell";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { GetCurrentUser } from "@/redux/slices/userSlice";
function OnboardingPage() {
  const dispatch = useDispatch();

  const navigate = useNavigate();

  const { user, loading, error, onboardingCompleted, isAuthenticated } = useSelector(
    (state) => state.user,
  );

  const [step, setStep] = useState(1);

  const [form, setForm] = useState({
    username: "",
    full_name: "",
  });

  useEffect(() => {
    dispatch(GetCurrentUser());
  }, [dispatch]);

  console.log(onboardingCompleted);

  useEffect(() => {
    if (!isAuthenticated) return;

    navigate(onboardingCompleted ? "/app/dashboard" : "/onboarding");
  }, [isAuthenticated, onboardingCompleted, navigate]);

  useEffect(() => {
    if (!user) return;

    setForm((prev) => ({
      ...prev,
      full_name: user.user.full_name || "",
      username: user.username || "",
    }));
  }, [user]);

  useEffect(() => {
    if (onboardingCompleted) {
      navigate("/app/dashboard");
    }
  }, [onboardingCompleted, navigate]);

  const handleChange = (key, value) => {
    setForm((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const nextStep = () => {
    if (!form.username.trim()) return;

    setStep(2);
  };

  const prevStep = () => {
    setStep(1);
  };

  const handleSubmit = async () => {
    const result = await dispatch(
      CompleteOnboarding({
        username: form.username,
        full_name: form.full_name,
      }),
    );

    if (CompleteOnboarding.fulfilled.match(result)) {
      navigate("/app/dashboard");
    }
  };

  return (
    <AuthShell
      title="Complete your profile"
      subtitle="Set up your Interleet identity before entering the arena."
    >
      <div className="relative overflow-hidden">
        {/* Progress */}

        <div className="mb-8">
          <div className="flex items-center justify-between text-[11px] uppercase tracking-[0.2em] text-zinc-500">
            <span>Profile Setup</span>

            <span>0{step} / 02</span>
          </div>

          <div className="mt-3 h-[2px] w-full overflow-hidden rounded-full bg-zinc-800">
            <motion.div
              initial={false}
              animate={{
                width: step === 1 ? "50%" : "100%",
              }}
              transition={{
                duration: 0.35,
                ease: "easeOut",
              }}
              className="h-full bg-orange-500"
            />
          </div>
        </div>

        <AnimatePresence mode="wait">
          {/* STEP 1 */}

          {step === 1 && (
            <motion.div
              key="fullname-step"
              initial={{
                opacity: 0,
                y: 20,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              exit={{
                opacity: 0,
                y: -20,
              }}
              transition={{
                duration: 0.25,
              }}
              className="space-y-7"
            >
              <div>
                <h2 className="text-[28px] font-semibold leading-tight tracking-tight text-white">
                  Confirm your identity.
                </h2>

                <p className="mt-2 max-w-sm text-sm leading-6 text-zinc-400">
                  This name will appear on your recruiter profile, certificates, and interview
                  reports.
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="full_name" className="text-sm font-medium text-zinc-300">
                  Full name
                </Label>

                <Input
                  id="full_name"
                  value={form.full_name}
                  onChange={(e) => handleChange("full_name", e.target.value)}
                  placeholder="John Doe"
                  className="h-12 border-zinc-800 bg-zinc-950 text-white placeholder:text-zinc-500 transition-colors duration-200 focus-visible:border-orange-500 focus-visible:ring-0"
                />
              </div>

              {error && <p className="text-sm text-red-400">{error}</p>}

              <Button
                onClick={() => setStep(2)}
                disabled={!form.full_name.trim()}
                className="h-11 w-full bg-orange-500 font-medium text-white transition-all duration-200 hover:bg-orange-400 active:scale-[0.99]"
              >
                Continue
              </Button>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div
              key="username-step"
              initial={{
                opacity: 0,
                y: 20,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              exit={{
                opacity: 0,
                y: -20,
              }}
              transition={{
                duration: 0.25,
              }}
              className="space-y-7"
            >
              <div>
                <h2 className="text-[28px] font-semibold leading-tight tracking-tight text-white">
                  Claim your username.
                </h2>

                <p className="mt-2 max-w-sm text-sm leading-6 text-zinc-400">
                  Your username becomes your public engineering identity across Interleet.
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="username" className="text-sm font-medium text-zinc-300">
                  Username
                </Label>

                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-sm text-zinc-500">
                    interleet.com/
                  </span>

                  <Input
                    id="username"
                    value={form.username}
                    onChange={(e) => handleChange("username", e.target.value)}
                    placeholder="john123"
                    className="h-12 border-zinc-800 bg-zinc-950 pl-[122px] text-white placeholder:text-zinc-500 transition-colors duration-200 focus-visible:border-orange-500 focus-visible:ring-0"
                  />
                </div>
              </div>

              {error && <p className="text-sm text-red-400">{error}</p>}

              <div className="flex gap-3">
                <Button
                  variant="outline"
                  onClick={() => setStep(1)}
                  className="h-11 flex-1 border border-zinc-800 bg-zinc-950 text-white transition-colors duration-200 hover:bg-zinc-900 focus-visible:ring-0"
                >
                  Back
                </Button>

                <Button
                  onClick={handleSubmit}
                  disabled={!form.username.trim() || loading}
                  className="h-11 flex-1 bg-orange-500 font-medium text-white transition-all duration-200 hover:bg-orange-400 active:scale-[0.99]"
                >
                  {loading ? "Please wait..." : "Enter Interleet"}
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </AuthShell>
  );
}

export default OnboardingPage;
