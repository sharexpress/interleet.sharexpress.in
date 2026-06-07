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

  const isOpen = controlledOpen !== undefined ? controlledOpen : internalOpen;
  const setIsOpen = onOpenChange !== undefined ? onOpenChange : setInternalOpen;

  const handleUpgrade = async () => {
    setLoading(true);
    setSandboxOrder(null);
    try {
      // 1. Create order on backend
      const response = await API.post("/api/payment/create-order");
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
        key: orderData.key_id,
        amount: orderData.amount,
        currency: orderData.currency,
        name: "Interleet Premium",
        description: "Monthly subscription plan (Unlock all features)",
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
          <div className="flex items-center justify-center w-12 h-12 rounded-full bg-[#FF6500]/10 border border-[#FF6500]/20 text-[#FF6500] mb-2">
            <Lock className="w-5 h-5 animate-pulse" />
          </div>
          <DialogTitle className="text-2xl font-bold tracking-tight bg-gradient-to-r from-orange-200 via-[#FF6500] to-orange-600 bg-clip-text text-transparent">
            Upgrade to Pro Elite
          </DialogTitle>
          <DialogDescription className="text-zinc-400 text-sm">
            Elevate your engineering preparation to FAANG-grade level.
          </DialogDescription>
        </DialogHeader>

        {sandboxOrder ? (
          <div className="bg-[#FF6500]/10 border border-[#FF6500]/25 rounded-xl p-5 space-y-4 my-2 text-center">
            <div className="flex items-center justify-center gap-2 text-[#FF6500] font-semibold text-sm">
              <Sparkles className="w-4 h-4" />
              Razorpay Sandbox Simulator
            </div>
            <p className="text-xs text-zinc-400 leading-relaxed">
              No Razorpay credentials detected in backend <code>.env</code>. You can safely simulate a successful payment locally to unlock premium services.
            </p>
            <div className="border border-dashed border-zinc-800 bg-zinc-900/60 p-3 rounded text-left font-mono text-[11px] text-zinc-500 space-y-1">
              <div>Order ID: {sandboxOrder.order_id}</div>
              <div>Amount: ₹499 (INR)</div>
              <div>Currency: INR</div>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                className="flex-1 border-zinc-800 hover:bg-zinc-900 text-zinc-300"
                onClick={() => setSandboxOrder(null)}
                disabled={loading}
              >
                Back
              </Button>
              <Button
                className="flex-1 bg-[#FF6500] text-white font-semibold hover:bg-[#E05900]"
                onClick={handleSimulatePayment}
                disabled={loading}
              >
                {loading ? (
                  <Loader2 className="w-4 h-4 animate-spin mr-1.5" />
                ) : (
                  <ShieldCheck className="w-4 h-4 mr-1.5" />
                )}
                Simulate Payment
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-4 my-2">
            {/* Price Badge */}
            <div className="flex items-center justify-between p-4 rounded-xl bg-zinc-900/70 border border-zinc-800/80">
              <div>
                <div className="text-xs text-zinc-500 font-mono tracking-wider uppercase">Pro Membership</div>
                <div className="text-sm font-semibold text-zinc-300">Monthly Billing</div>
              </div>
              <div className="text-right">
                <span className="text-3xl font-extrabold text-white">₹499</span>
                <span className="text-xs text-zinc-500 ml-1">/ month</span>
              </div>
            </div>

            {/* Benefits list */}
            <div className="space-y-2.5 bg-zinc-900/40 p-4 rounded-xl border border-zinc-900">
              <div className="text-xs font-semibold text-zinc-400 mb-2 uppercase tracking-wide">Included Features:</div>
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
              className="w-full bg-gradient-to-r from-[#FF6500] to-orange-500 hover:from-[#E05900] hover:to-orange-600 text-white font-bold py-5 mt-2 rounded-xl transition-all shadow-lg hover:shadow-orange-500/10"
              onClick={handleUpgrade}
              disabled={loading}
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <span className="flex items-center justify-center gap-1.5">
                  <Star className="w-4 h-4 fill-zinc-950" />
                  Upgrade Now
                </span>
              )}
            </Button>
          </div>
        )}

        <div className="text-center text-[10px] text-zinc-600 mt-2">
          Secure checkout verified by Razorpay. Zero risk sandbox testing.
        </div>
      </DialogContent>
    </Dialog>
  );
}
