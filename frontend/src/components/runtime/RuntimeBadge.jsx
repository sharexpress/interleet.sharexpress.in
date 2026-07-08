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
