import React from 'react';
import { CheckCircle, XCircle, Clock, CircleDashed } from 'lucide-react';

export default function ExecutionTimeline({ steps }) {
  if (!steps || steps.length === 0) return null;

  return (
    <div className="space-y-4 pt-2">
      {steps.map((step, idx) => {
        const isLast = idx === steps.length - 1;
        const Icon = step.status === 'passed' ? CheckCircle 
                   : step.status === 'failed' ? XCircle 
                   : CircleDashed;
        const color = step.status === 'passed' ? 'text-emerald-400'
                    : step.status === 'failed' ? 'text-red-400'
                    : 'text-slate-400';
        
        return (
          <div key={step.id} className="relative flex gap-4">
            {!isLast && (
              <div className="absolute left-2.5 top-6 bottom-[-16px] w-[2px] bg-border" />
            )}
            <div className={`relative z-10 bg-[#1E1E1E] sm:bg-background ${color}`}>
              <Icon className="h-5 w-5 bg-background rounded-full" />
            </div>
            <div className="flex-1 pb-1">
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm text-foreground/90">{step.title}</span>
                <span className="flex items-center gap-1 text-[10px] text-muted-foreground font-mono">
                  <Clock className="h-3 w-3" />
                  {step.durationMs}ms
                </span>
              </div>
              {step.stderr && (
                <pre className="mt-2 rounded-md border border-red-500/20 bg-red-500/10 p-2 text-xs font-mono text-red-400 overflow-x-auto">
                  {step.stderr}
                </pre>
              )}
              {step.stdout && step.status !== 'passed' && !step.stderr && (
                <pre className="mt-2 rounded-md border border-white/10 bg-white/5 p-2 text-xs font-mono text-slate-300 overflow-x-auto">
                  {step.stdout}
                </pre>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
