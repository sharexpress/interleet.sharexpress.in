import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { Eye, EyeOff, Github, Mail } from "lucide-react";
import { AuthShell } from "@/components/auth/AuthShell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";



function LoginPage() {
  const [show, setShow] = useState(false);
  const navigate = useNavigate();
  return (
    <AuthShell
      title="Sign in to Interleet"
      subtitle="Welcome back. Pick up where you left off."
      footer={
      <>
          New here?{" "}
          <Link to="/signup" className="font-medium text-primary hover:underline">
            Create an account
          </Link>
        </>
      }>
      
      <div className="grid grid-cols-2 gap-2">
        <Button variant="outline" type="button" className="w-full">
          <Github className="mr-2 h-4 w-4" /> GitHub
        </Button>
        <Button variant="outline" type="button" className="w-full">
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
        
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" required placeholder="you@company.com" autoComplete="email" />
        </div>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="password">Password</Label>
            <Link to="/forgot" className="text-xs text-muted-foreground hover:text-foreground">
              Forgot password?
            </Link>
          </div>
          <div className="relative">
            <Input
              id="password"
              type={show ? "text" : "password"}
              required
              placeholder="••••••••"
              autoComplete="current-password"
              className="pr-10" />
            
            <button
              type="button"
              onClick={() => setShow((s) => !s)}
              className="absolute right-2 top-1/2 -translate-y-1/2 rounded p-1 text-muted-foreground hover:text-foreground"
              aria-label={show ? "Hide password" : "Show password"}>
              
              {show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </button>
          </div>
        </div>
        <label className="flex items-center gap-2 text-sm text-muted-foreground">
          <Checkbox defaultChecked /> Keep me signed in for 30 days
        </label>
        <Button type="submit" className="w-full">
          Sign in
        </Button>
      </form>
    </AuthShell>);

}
export default LoginPage;
