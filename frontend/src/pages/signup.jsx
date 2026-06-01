import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { Eye, EyeOff, Github, Mail, Check } from "lucide-react";
import { AuthShell } from "@/components/auth/AuthShell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";



function strength(pw) {
  let s = 0;
  if (pw.length >= 8) s++;
  if (/[A-Z]/.test(pw)) s++;
  if (/[0-9]/.test(pw)) s++;
  if (/[^A-Za-z0-9]/.test(pw)) s++;
  return s;
}

function SignupPage() {
  const [show, setShow] = useState(false);
  const [pw, setPw] = useState("");
  const navigate = useNavigate();
  const s = strength(pw);
  const labels = ["Too short", "Weak", "Okay", "Good", "Strong"];
  const colors = ["bg-destructive", "bg-destructive", "bg-warning", "bg-chart-1", "bg-success"];

  return (
    <AuthShell
      title="Create your Interleet account"
      subtitle="Start practicing real-world engineering in 60 seconds."
      footer={
      <>
          Already have an account?{" "}
          <Link to="/login" className="font-medium text-primary hover:underline">
            Sign in
          </Link>
        </>
      }>
      
      <div className="grid grid-cols-2 gap-2">
        <Button variant="outline" type="button">
          <Github className="mr-2 h-4 w-4" /> GitHub
        </Button>
        <Button variant="outline" type="button">
          <Mail className="mr-2 h-4 w-4" /> Google
        </Button>
      </div>
      <div className="relative my-5 flex items-center">
        <Separator className="flex-1" />
        <span className="px-3 font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
          or
        </span>
        <Separator className="flex-1" />
      </div>
      <form
        className="space-y-4"
        onSubmit={(e) => {
          e.preventDefault();
          navigate("/app/dashboard");
        }}>
        
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-2">
            <Label htmlFor="first">First name</Label>
            <Input id="first" required placeholder="Alex" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="last">Last name</Label>
            <Input id="last" required placeholder="Morgan" />
          </div>
        </div>
        <div className="space-y-2">
          <Label htmlFor="email">Work email</Label>
          <Input id="email" type="email" required placeholder="you@company.com" />
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <div className="relative">
            <Input
              id="password"
              type={show ? "text" : "password"}
              required
              value={pw}
              onChange={(e) => setPw(e.target.value)}
              placeholder="At least 8 characters"
              className="pr-10" />
            
            <button
              type="button"
              onClick={() => setShow((v) => !v)}
              className="absolute right-2 top-1/2 -translate-y-1/2 rounded p-1 text-muted-foreground hover:text-foreground">
              
              {show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </button>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex flex-1 gap-1">
              {[0, 1, 2, 3].map((i) =>
              <span
                key={i}
                className={`h-1 flex-1 rounded-full ${i < s ? colors[s] : "bg-muted"}`} />

              )}
            </div>
            <span className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
              {labels[s]}
            </span>
          </div>
        </div>
        <Button type="submit" className="w-full">
          Create account
        </Button>
        <p className="flex items-start gap-2 text-xs text-muted-foreground">
          <Check className="mt-0.5 h-3.5 w-3.5 text-success" />
          By signing up you agree to our Terms and acknowledge our Privacy Policy.
        </p>
      </form>
    </AuthShell>);

}
export default SignupPage;
