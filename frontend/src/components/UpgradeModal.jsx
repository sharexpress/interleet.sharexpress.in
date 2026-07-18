/*
 * Copyright 2026 Sharexpress Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "sonner";
import { API } from "@/api/api";
import { GetCurrentUser } from "@/redux/slices/userSlice";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Lock, Check, Sparkles, Star, Loader2, ShieldCheck } from "lucide-react";

const loadRazorpayScript = () => {
  return new Promise((resolve) => {
    if (window.Razorpay) {
      resolve(true);
      return;
    }
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.onload = () => resolve(true);
    script.onerror = () => resolve(false);
    document.body.appendChild(script);
  });
};

export default function UpgradeModal({ trigger, open: controlledOpen, onOpenChange }) {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.user?.user);
  const [internalOpen, setInternalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [sandboxOrder, setSandboxOrder] = useState(null);
  const [plan, setPlan] = useState("monthly"); // "monthly" or "yearly"

  const isOpen = controlledOpen !== undefined ? controlledOpen : internalOpen;
  const setIsOpen = onOpenChange !== undefined ? onOpenChange : setInternalOpen;

  const handleUpgrade = async () => {
    setLoading(true);
    setSandboxOrder(null);
    try {
      const amount = plan === "monthly" ? 14900 : 89900;
      // 1. Create order on backend
      const response = await API.post("/api/payment/create-order", { amount });
      const orderData = response.data;

      if (!orderData.success) {
        toast.error("Failed to create subscription order. Try again.");
        setLoading(false);
        return;
      }

      // 2. If it is Mock Mode, show sandbox simulation UI in the modal
      if (orderData.is_mock) {
        setSandboxOrder(orderData);
        setLoading(false);
        toast.info("Sandbox mode: Complete simulation inside the modal.");
        return;
      }

      // 3. Load Razorpay script for live/test checkout
      const loaded = await loadRazorpayScript();
      if (!loaded) {
        toast.error("Failed to load Razorpay payment gateway.");
        setLoading(false);
        return;
      }

      // 4. Open Razorpay widget
      const options = {
        key: orderData.key_id || import.meta.env.VITE_RAZORPAY_KEY_ID,
        amount: orderData.amount,
        currency: orderData.currency,
        name: "Interleet Premium",
        description: plan === "monthly" ? "Monthly subscription plan (Unlock all features)" : "Yearly subscription plan (Save ~50%)",
        order_id: orderData.order_id,
        handler: async function (paymentRes) {
          setLoading(true);
          try {
            const verifyRes = await API.post("/api/payment/verify-payment", {
              order_id: orderData.order_id,
              payment_id: paymentRes.razorpay_payment_id,
              signature: paymentRes.razorpay_signature,
            });

            if (verifyRes.data.success) {
              toast.success("Welcome to Interleet Premium! Upgrade successful.");
              dispatch(GetCurrentUser());
              setIsOpen(false);
            } else {
              toast.error("Payment verification failed.");
            }
          } catch (err) {
            toast.error(err.response?.data?.detail || "Verification failed.");
          } finally {
            setLoading(false);
          }
        },
        prefill: {
          name: user?.full_name || user?.username || "",
          email: user?.email || "",
        },
        theme: {
          color: "#FF6500", // Brand Orange styling
        },
        modal: {
          ondismiss: function () {
            setLoading(false);
            toast.warning("Payment checkout cancelled.");
          },
        },
      };

      const rzp = new window.Razorpay(options);
      rzp.open();
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to initialize checkout.");
      setLoading(false);
    }
  };

  const handleSimulatePayment = async () => {
    if (!sandboxOrder) return;
    setLoading(true);
    try {
      const verifyRes = await API.post("/api/payment/verify-payment", {
        order_id: sandboxOrder.order_id,
        payment_id: "pay_mock_" + Math.random().toString(36).substring(2, 11),
        signature: "mock_signature_data",
      });

      if (verifyRes.data.success) {
        toast.success("Sandbox Upgrade Successful! You are now premium.");
        dispatch(GetCurrentUser());
        setIsOpen(false);
        setSandboxOrder(null);
      } else {
        toast.error("Sandbox verification failed.");
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Simulation failed.");
    } finally {
      setLoading(false);
    }
  };

  const benefits = [
    "Unlock all Premium coding challenges (Twitter, Virtualized Table, etc.)",
    "Unlimited AI Mock Interviews tailored to your target roles",
    "Full access to Domain Strengths dashboard analytics",
    "Opt-in directly to our premier hiring recruiter pipelines",
    "Premium Pro Elite status badge on leaderboards",
    "Priority 24/7 client & engineering support",
  ];

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      {trigger && <DialogTrigger asChild>{trigger}</DialogTrigger>}
      <DialogContent className="sm:max-w-[460px] bg-zinc-950 border-zinc-800 text-zinc-100">
        <DialogHeader className="flex flex-col items-center text-center space-y-2 pb-4">
          <div className="flex items-center justify-center w-12 h-12 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 mb-2">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          <DialogTitle className="text-2xl font-bold tracking-tight bg-gradient-to-r from-emerald-200 via-emerald-400 to-teal-500 bg-clip-text text-transparent">
            Interleet Pro is 100% Free!
          </DialogTitle>
          <DialogDescription className="text-zinc-400 text-sm">
            All engineering challenges, AI mock interviews, and system design tools are unlocked for everyone.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 my-2">
          <div className="space-y-2.5 bg-zinc-900/40 p-4 rounded-xl border border-zinc-900">
            <div className="text-xs font-semibold text-emerald-400 mb-2 uppercase tracking-wide">Included for Free:</div>
            {benefits.map((benefit, idx) => (
              <div key={idx} className="flex items-start gap-2.5 text-xs text-zinc-300">
                <div className="flex-shrink-0 mt-0.5 w-4 h-4 rounded-full bg-emerald-500/10 border border-emerald-500/25 flex items-center justify-center text-emerald-400">
                  <Check className="w-2.5 h-2.5" />
                </div>
                <span>{benefit}</span>
              </div>
            ))}
          </div>

          <Button
            className="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-black font-bold py-5 mt-2 rounded-xl transition-all shadow-lg"
            onClick={() => setIsOpen(false)}
          >
            Start Exploring Now
          </Button>
        </div>

        <div className="text-center text-[10px] text-zinc-500 mt-2">
          Enjoy unlimited access to all features. Happy coding!
        </div>
      </DialogContent>
    </Dialog>
  );
}
