import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { Card } from "@/components/ui/card";
import { DifficultyPill, DomainTag } from "@/components/domain/Tags";
import { Clock, Sparkles, Users, Lock } from "lucide-react";
import UpgradeModal from "@/components/UpgradeModal";

export function ChallengeCard({ c }) {
  const user = useSelector((state) => state.user?.user);
  const isLocked = c.is_premium && !user?.is_premium;

  const cardContent = (
    <Card className="h-full gap-3 border-border bg-card p-5 transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:shadow-md cursor-pointer">
      <div className="flex items-center justify-between">
        <DomainTag d={c.domain} />
        <div className="flex items-center gap-1.5">
          {c.is_premium && (
            <span className="inline-flex items-center gap-0.5 rounded-full bg-[#FF6500]/15 px-2 py-0.5 text-[10px] font-bold text-[#FF6500] border border-[#FF6500]/25">
              <Lock className="h-2.5 w-2.5" /> PRO
            </span>
          )}
          <DifficultyPill d={c.difficulty} />
        </div>
      </div>
      <h3 className="text-base font-semibold leading-snug tracking-tight group-hover:text-primary">
        {c.title || "null"}
      </h3>
      <p className="line-clamp-2 text-sm text-muted-foreground">{c.summary}</p>
      <div className="mt-1 flex flex-wrap gap-1.5">
        {c.tags.map((t) => (
          <span
            key={t}
            className="rounded-md border border-border bg-muted/40 px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground"
          >
            {t}
          </span>
        ))}
      </div>
      <div className="mt-3 flex items-center justify-between border-t border-border pt-3 text-xs text-muted-foreground">
        <span className="inline-flex items-center gap-1">
          <Clock className="h-3.5 w-3.5" />
          {c.minutes}m
        </span>
        <span className="inline-flex items-center gap-1">
          <Sparkles className="h-3.5 w-3.5" />
          {c.xp} XP
        </span>
        <span className="inline-flex items-center gap-1">
          <Users className="h-3.5 w-3.5" />
          {c.completion}%
        </span>
      </div>
    </Card>
  );

  if (isLocked) {
    return (
      <UpgradeModal
        trigger={
          <div className="group block">
            {cardContent}
          </div>
        }
      />
    );
  }

  return (
    <Link to={`/app/challenges/${c.slug}`} className="group block">
      {cardContent}
    </Link>
  );
}
