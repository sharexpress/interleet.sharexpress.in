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

import React from 'react';
import { CheckCircle2, Server } from 'lucide-react';

export default function EnvironmentCard({ runtime }) {
  if (!runtime || !runtime.services) return null;
  return (
    <div className="mt-5 rounded-lg border border-border bg-card overflow-hidden">
      <div className="flex items-center gap-2 bg-muted/40 px-3 py-2 border-b border-border">
        <Server className="h-4 w-4 text-muted-foreground" />
        <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Available Resources</h3>
      </div>
      <div className="p-3 space-y-2">
        {runtime.services.map((svc, i) => (
          <div key={i} className="flex items-center gap-2 text-sm text-foreground/80">
            <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
            <span className="font-mono text-xs">{svc}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
