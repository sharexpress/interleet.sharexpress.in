import { Link } from "react-router-dom";
import { useState } from "react";
import { ArrowLeft, MailCheck } from "lucide-react";
import { AuthShell } from "@/components/auth/AuthShell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";



function ForgotPage() {
  const [sent, setSent] = useState(false);
  return (
    <AuthShell
      title={sent ? "Check your inbox" : "Reset your password"}
      subtitle={
      sent ?
      "We've sent you a link to reset your password. It's valid for 60 minutes." :
      "Enter the email on your account and we'll send you a reset link."
      }
      footer={
      <Link to="/login" className="inline-flex items-center gap-1.5 text-primary hover:underline">
          <ArrowLeft className="h-3.5 w-3.5" /> Back to sign in
        </Link>
      }>
      
      {sent ?
      <div className="rounded-lg border border-success/30 bg-success/10 p-4 text-sm text-success">
          <div className="flex items-center gap-2">
            <MailCheck className="h-4 w-4" />
            <span className="font-medium">Email sent</span>
          </div>
          <p className="mt-1 text-success/80">Didn't get it? Check spam or try again in 60s.</p>
        </div> :

      <form
        className="space-y-4"
        onSubmit={(e) => {
          e.preventDefault();
          setSent(true);
        }}>
        
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" required placeholder="you@company.com" />
          </div>
          <Button type="submit" className="w-full">
            Send reset link
          </Button>
        </form>
      }
    </AuthShell>);

}
export default ForgotPage;
