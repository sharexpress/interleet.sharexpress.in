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
import { Badge } from '@/components/ui/badge';
import { Box } from 'lucide-react';

export default function RuntimeBadge({ runtime }) {
  if (!runtime) return null;
  return (
    <Badge variant="outline" className="flex items-center gap-1.5 font-mono text-xs bg-muted/50 text-muted-foreground ml-2">
      <Box className="h-3 w-3" />
      {runtime.name} v{runtime.version}
    </Badge>
  );
}
