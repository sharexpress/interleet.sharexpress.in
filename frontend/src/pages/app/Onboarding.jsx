import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import { AuthShell } from "@/components/auth/AuthShell";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

function OnboardingPage() {
  const [step, setStep] = useState(1);

  const [form, setForm] = useState({
    username: "",
    full_name: "",
  });

  const nextStep = () => {
    if (step < 2) {
      setStep((prev) => prev + 1);
    }
  };

  const prevStep = () => {
    if (step > 1) {
      setStep((prev) => prev - 1);
    }
  };

  const handleChange = (key, value) => {
    setForm((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const handleSubmit = async () => {
    console.log(form);

    // API CALL
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
              <div className="space-y-3">
                <div>
                  <h2 className="text-[28px] font-semibold leading-tight tracking-tight text-white">
                    Claim your identity.
                  </h2>

                  <p className="mt-2 max-w-sm text-sm leading-6 text-zinc-400">
                    Your username becomes your public handle across coding challenges, rankings, and
                    interview reports.
                  </p>
                </div>
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
                    placeholder="John123"
                    className="h-12 pl-[122px] border-zinc-800 bg-zinc-950 text-white placeholder:text-zinc-500 transition-colors duration-200 focus-visible:ring-0 focus-visible:border-orange-500"
                  />
                </div>
              </div>

              <Button
                onClick={nextStep}
                disabled={!form.username.trim()}
                className="h-11 w-full bg-orange-500 font-medium text-white transition-all duration-200 hover:bg-orange-400 active:scale-[0.99]"
              >
                Continue
              </Button>
            </motion.div>
          )}

          {/* STEP 2 */}

          {step === 2 && (
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
              <div className="space-y-3">
                <div>
                  <h2 className="text-[28px] font-semibold leading-tight tracking-tight text-white">
                    Tell us your real name.
                  </h2>

                  <p className="mt-2 max-w-sm text-sm leading-6 text-zinc-400">
                    Used for recruiter visibility, interview evaluations, certificates, and verified
                    engineering profiles.
                  </p>
                </div>
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
                  className="h-12 border-zinc-800 bg-zinc-950 text-white placeholder:text-zinc-500 transition-colors duration-200 focus-visible:ring-0 focus-visible:border-orange-500"
                />
              </div>

              <div className="flex gap-3">
                <Button
                  variant="outline"
                  onClick={prevStep}
                  className="h-11 flex-1 border border-zinc-800 bg-zinc-950 text-white transition-colors duration-200 hover:bg-zinc-900 focus-visible:ring-0 focus-visible:ring-offset-0"
                >
                  Back
                </Button>

                <Button
                  onClick={nextStep}
                  disabled={!form.username.trim()}
                  className="h-11 w-1/2 bg-orange-500 font-medium text-white transition-all duration-200 hover:bg-orange-400 active:scale-[0.99]"
                >
                  Enter interleet
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
