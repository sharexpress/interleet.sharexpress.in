import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { GetCurrentUser } from "@/redux/slices/userSlice";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { toast } from "sonner";
import { API } from "@/api/api";
import {
  Sparkles,
  Flame,
  Trophy,
  Award,
  Percent,
  FileText,
  CheckCircle2,
  XCircle,
  Lock,
  ShoppingBag,
  Coins,
  PartyPopper,
  X,
  Shirt,
  GlassWater,
  BookOpen,
  Layers,
  ArrowUpRight
} from "lucide-react";

// Helper to map icon names to Lucide icons
const IconMap = {
  Sparkles: Sparkles,
  FileText: FileText,
  Award: Award,
  Percent: Percent,
  Shirt: Shirt,
  GlassWater: GlassWater,
  BookOpen: BookOpen,
  Layers: Layers
};

// Helper for category label colors
const getCategoryDetails = (itemId) => {
  if (["premium_30_days", "resume_review", "renewal_discount"].includes(itemId)) {
    return { label: "Digital Pass", color: "bg-blue-500/10 text-blue-400 border-blue-500/20" };
  }
  if (["interleet_tshirt", "interleet_bottle", "interleet_notebook", "interleet_stickers"].includes(itemId)) {
    return { label: "Physical Swag", color: "bg-amber-500/10 text-amber-400 border-amber-500/20" };
  }
  return { label: "Cosmetic Accent", color: "bg-purple-500/10 text-purple-400 border-purple-500/20" };
};

function StorePage() {
  const { user } = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [redeemingId, setRedeemingId] = useState(null);
  
  // Celebration Modal State
  const [showCelebration, setShowCelebration] = useState(false);
  const [redeemedItem, setRedeemedItem] = useState(null);

  const fetchStoreItems = async () => {
    try {
      const res = await API.get("/api/store/items");
      if (res.data && res.data.success) {
        setItems(res.data.items);
      }
    } catch (err) {
      console.error("Failed to fetch store items", err);
      toast.error("Failed to load store rewards.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchStoreItems();
    }
  }, [user]);

  if (!user) return null;

  // XP, Level calculations
  const xp = user.xp ?? user.total_xp ?? 0;
  const level = Math.floor(xp / 1000) + 1;
  const xpInLevel = xp % 1000;
  const progressPercent = (xpInLevel / 1000) * 100;
  const xpToNext = 1000 - xpInLevel;

  const handleRedeem = async (item) => {
    setRedeemingId(item.id);
    try {
      const res = await API.post("/api/store/redeem", { item_id: item.id });
      if (res.data && res.data.success) {
        toast.success(res.data.message || `Redeemed ${item.title}!`);
        setRedeemedItem(item);
        setShowCelebration(true);
        
        // Refresh redux user state and local items
        await dispatch(GetCurrentUser());
        await fetchStoreItems();
      }
    } catch (err) {
      console.error("Redemption failed", err);
      const detail = err.response?.data?.detail || "Redemption failed.";
      toast.error(detail);
    } finally {
      setRedeemingId(null);
    }
  };

  // Filter items by category
  const digitalItems = items.filter(i => ["premium_30_days", "resume_review", "renewal_discount"].includes(i.id));
  const swagItems = items.filter(i => ["interleet_tshirt", "interleet_bottle", "interleet_notebook", "interleet_stickers"].includes(i.id));
  const cosmeticItems = items.filter(i => ["exclusive_badge"].includes(i.id));

  // Render cards helper
  const renderItemsGrid = (filteredList) => {
    if (filteredList.length === 0) {
      return (
        <div className="py-16 text-center border border-dashed border-zinc-800 rounded-2xl bg-zinc-950/20">
          <p className="text-zinc-500 text-sm font-mono">No rewards available in this category.</p>
        </div>
      );
    }

    return (
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-2">
        {filteredList.map((item) => {
          const ItemIcon = IconMap[item.badge_icon] || Sparkles;
          const { eligibility, requirements, user_stats } = item;
          const cat = getCategoryDetails(item.id);
          
          return (
            <Card 
              key={item.id} 
              className={`flex flex-col justify-between border-zinc-800 bg-zinc-950/60 backdrop-blur-md p-6 hover:-translate-y-1.5 hover:shadow-2xl hover:shadow-[#FF6500]/5 hover:border-primary/45 transition-all duration-300 relative group overflow-hidden ${
                eligibility.already_redeemed ? "opacity-75" : ""
              }`}
            >
              {/* Premium Gradient Top-Border */}
              <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-zinc-800 to-transparent group-hover:via-primary/50 transition-all duration-500" />
              
              {/* Glass subtle gradient overlay */}
              <div className="absolute inset-0 bg-gradient-to-br from-white/[0.01] to-transparent pointer-events-none" />

              <div>
                {/* Header Row */}
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className={`font-mono text-[9px] uppercase tracking-wider py-0.5 px-2 ${cat.color}`}>
                        {cat.label}
                      </Badge>
                      {eligibility.already_redeemed && (
                        <Badge className="bg-zinc-800 text-zinc-400 border-zinc-700 text-[9px] py-0 px-1.5">Claimed</Badge>
                      )}
                    </div>
                    <h3 className="font-extrabold text-base text-white tracking-tight group-hover:text-primary transition-colors mt-1">
                      {item.title}
                    </h3>
                    <p className="text-xs text-muted-foreground leading-relaxed pr-2">
                      {item.description}
                    </p>
                  </div>
                  <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-zinc-900 border border-zinc-800 text-primary shadow-[0_0_15px_rgba(255,101,0,0.08)] group-hover:border-primary/30 group-hover:text-primary group-hover:shadow-primary/10 transition-all duration-300">
                    <ItemIcon className="h-5 w-5" />
                  </span>
                </div>

                {/* Eligibility Setup Check List */}
                <div className="mt-5 bg-zinc-900/40 border border-zinc-900 rounded-xl p-4.5 space-y-3">
                  <h4 className="text-[9px] font-mono font-bold uppercase tracking-widest text-zinc-400 border-b border-zinc-850 pb-2 flex items-center justify-between">
                    <span>Unlock Contract Requirements</span>
                    {eligibility.eligible ? (
                      <span className="text-emerald-400 text-[8px] font-sans font-semibold bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">Active</span>
                    ) : eligibility.already_redeemed ? (
                      <span className="text-zinc-500 text-[8px] font-sans font-semibold bg-zinc-850 px-2 py-0.5 rounded-full">Completed</span>
                    ) : (
                      <span className="text-rose-400 text-[8px] font-sans font-semibold bg-rose-500/10 px-2 py-0.5 rounded-full border border-rose-500/20 flex items-center gap-1">
                        <Lock className="h-2.5 w-2.5" /> Locked
                      </span>
                    )}
                  </h4>

                  <ul className="space-y-2 text-xs">
                    {/* XP Check */}
                    <li className="flex items-center justify-between">
                      <span className="text-zinc-400 font-medium">Vault XP Balance:</span>
                      <span className="flex items-center gap-2">
                        <span className="font-mono text-zinc-300 font-semibold">{requirements.xp.toLocaleString()} XP</span>
                        {eligibility.xp_eligible ? (
                          <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" />
                        ) : (
                          <span className="flex items-center gap-1 text-[10px] text-rose-500 font-medium">
                            (Need {requirements.xp - user_stats.xp} more)
                            <XCircle className="h-4 w-4 text-rose-500 shrink-0" />
                          </span>
                        )}
                      </span>
                    </li>

                    {/* Streak Check */}
                    {requirements.streak > 0 && (
                      <li className="flex items-center justify-between">
                        <span className="text-zinc-400 font-medium">Required Consistancy Streak:</span>
                        <span className="flex items-center gap-2">
                          <span className="font-mono text-zinc-300 font-semibold">{requirements.streak} Days</span>
                          {eligibility.streak_eligible ? (
                            <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" />
                          ) : (
                            <span className="flex items-center gap-1 text-[10px] text-rose-500 font-medium">
                              (Current: {user_stats.streak}d)
                              <XCircle className="h-4 w-4 text-rose-500 shrink-0" />
                            </span>
                          )}
                        </span>
                      </li>
                    )}

                    {/* Challenges Check */}
                    {requirements.challenges > 0 && (
                      <li className="flex items-center justify-between">
                        <span className="text-zinc-400 font-medium">Arena Challenge Completions:</span>
                        <span className="flex items-center gap-2">
                          <span className="font-mono text-zinc-300 font-semibold">{requirements.challenges} Solved</span>
                          {eligibility.challenges_eligible ? (
                            <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" />
                          ) : (
                            <span className="flex items-center gap-1 text-[10px] text-rose-500 font-medium">
                              (Current: {user_stats.challenges_solved})
                              <XCircle className="h-4 w-4 text-rose-500 shrink-0" />
                            </span>
                          )}
                        </span>
                      </li>
                    )}
                  </ul>
                </div>
              </div>

              {/* Actions Footer */}
              <div className="mt-6 pt-4 border-t border-zinc-900/60 flex items-center justify-between gap-4">
                <div className="flex flex-col min-w-0">
                  <span className="text-[9px] font-mono uppercase tracking-widest text-muted-foreground">Exchange Rate</span>
                  <span className="font-mono font-black text-lg text-white flex items-center gap-1 mt-0.5">
                    {item.cost.toLocaleString()} <span className="text-[10px] font-sans font-bold text-amber-500">XP</span>
                  </span>
                </div>

                <div className="flex-1 max-w-[200px]">
                  {eligibility.already_redeemed ? (
                    <Button className="w-full bg-zinc-900/80 text-zinc-500 border border-zinc-800/80 cursor-not-allowed text-xs font-semibold" disabled>
                      Redeemed
                    </Button>
                  ) : (
                    <Button
                      className={`w-full text-xs font-bold transition-all duration-300 ${
                        eligibility.eligible
                          ? "bg-[#FF6500] hover:bg-orange-600 text-white shadow-lg shadow-[#FF6500]/15 hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
                          : "bg-zinc-900 text-zinc-600 border border-zinc-850 cursor-not-allowed"
                      }`}
                      onClick={() => eligibility.eligible && handleRedeem(item)}
                      disabled={!eligibility.eligible || redeemingId === item.id}
                    >
                      {redeemingId === item.id ? (
                        <span className="flex items-center gap-1.5 justify-center">
                          <Sparkles className="h-3.5 w-3.5 animate-spin" /> Processing
                        </span>
                      ) : eligibility.eligible ? (
                        <span className="flex items-center gap-1 justify-center">
                          Unlock Reward <ArrowUpRight className="h-3 w-3 shrink-0" />
                        </span>
                      ) : (
                        "Locked"
                      )}
                    </Button>
                  )}
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    );
  };

  return (
    <AppShell>
      <PageHeader
        title="XP Rewards Store"
        description="Exchange your hard-earned XP to unlock elite perks, premium passes, badges, and subscription benefits."
      />

      <div className="space-y-6 px-4 py-6 md:px-8 max-w-7xl mx-auto">
        {/* User Balance Overview Card */}
        <Card className="border-zinc-800 bg-gradient-to-r from-zinc-950 via-[#FF6500]/5 to-zinc-950 p-6 flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl relative overflow-hidden">
          {/* Subtle background glow */}
          <div className="pointer-events-none absolute inset-y-0 right-0 w-[300px] bg-[radial-gradient(ellipse_at_right,theme(colors.primary/8),transparent_70%)]" />
          
          <div className="flex items-center gap-4 relative z-10 w-full md:w-auto">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-[#FF6500]/10 border border-[#FF6500]/25 text-[#FF6500] shadow-[0_0_20px_rgba(255,101,0,0.12)]">
              <Coins className="h-7 w-7 animate-pulse" />
            </div>
            <div className="space-y-1">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                Vault Exchange Balance
              </h3>
              <p className="text-xs text-muted-foreground">
                Earn XP by completing coding challenges, solving design tasks, and doing AI mock interviews.
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-8 w-full md:w-auto justify-between md:justify-end relative z-10">
            <div className="text-left md:text-right">
              <span className="block text-[10px] font-mono uppercase tracking-widest text-muted-foreground">Available Balance</span>
              <span className="text-2xl font-black text-white font-mono tracking-tight flex items-center gap-1.5 md:justify-end mt-0.5">
                {xp.toLocaleString()} <span className="text-sm font-bold text-[#FF6500] uppercase font-sans">XP</span>
              </span>
            </div>
            
            <div className="text-left md:text-right min-w-[150px]">
              <span className="block text-[10px] font-mono uppercase tracking-widest text-muted-foreground mb-1">Level {level} Progress</span>
              <Progress value={progressPercent} className="h-1.5 bg-zinc-800 border-none" />
              <span className="block text-[9px] font-mono text-muted-foreground mt-1">
                {xpToNext} XP to Level {level + 1}
              </span>
            </div>

            <div className="flex gap-4">
              <div className="text-center bg-zinc-900 border border-zinc-850 rounded-xl px-4 py-2 min-w-[75px]">
                <span className="block text-[9px] font-mono uppercase tracking-wider text-muted-foreground">Streak</span>
                <span className="text-sm font-extrabold text-chart-3 flex items-center justify-center gap-1 mt-0.5">
                  <Flame className="h-3.5 w-3.5 fill-chart-3" />
                  {user.streak_count || user.streak || 0}d
                </span>
              </div>
              <div className="text-center bg-zinc-900 border border-zinc-850 rounded-xl px-4 py-2 min-w-[75px]">
                <span className="block text-[9px] font-mono uppercase tracking-wider text-muted-foreground">Solved</span>
                <span className="text-sm font-extrabold text-white flex items-center justify-center gap-1 mt-0.5">
                  <Trophy className="h-3.5 w-3.5 text-yellow-500" />
                  {user.solved || user.total_challenges_solved || 0}
                </span>
              </div>
            </div>
          </div>
        </Card>

        {/* Tabbed Rewards List */}
        <Tabs defaultValue="all" className="w-full space-y-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-zinc-900 pb-2">
            <TabsList className="bg-zinc-950/80 border border-zinc-900">
              <TabsTrigger value="all" className="font-semibold text-xs py-1.5">All Items</TabsTrigger>
              <TabsTrigger value="digital" className="font-semibold text-xs py-1.5">Memberships & AI</TabsTrigger>
              <TabsTrigger value="swag" className="font-semibold text-xs py-1.5">Official Swag</TabsTrigger>
              <TabsTrigger value="badges" className="font-semibold text-xs py-1.5">Accents</TabsTrigger>
            </TabsList>
            
            <Badge variant="outline" className="font-mono text-[10px] text-muted-foreground py-1 bg-zinc-950 border-zinc-900 px-3">
              Standard swap rates apply
            </Badge>
          </div>

          <TabsContent value="all" className="mt-0">
            {loading ? (
              <div className="py-24 text-center text-muted-foreground">
                <Sparkles className="h-8 w-8 animate-spin mx-auto text-[#FF6500] mb-3" />
                <p className="font-mono text-sm">Evaluating eligibility contracts...</p>
              </div>
            ) : renderItemsGrid(items)}
          </TabsContent>

          <TabsContent value="digital" className="mt-0">
            {renderItemsGrid(digitalItems)}
          </TabsContent>

          <TabsContent value="swag" className="mt-0">
            {renderItemsGrid(swagItems)}
          </TabsContent>

          <TabsContent value="badges" className="mt-0">
            {renderItemsGrid(cosmeticItems)}
          </TabsContent>
        </Tabs>
      </div>

      {/* Premium Celebration Modal */}
      {showCelebration && redeemedItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in">
          <Card className="max-w-md w-full border-[#FF6500]/40 bg-zinc-950 p-6 relative overflow-hidden text-center shadow-2xl glow-soft">
            {/* Background fireworks circles */}
            <div className="absolute -top-12 -left-12 h-36 w-36 rounded-full bg-primary/5 blur-3xl" />
            <div className="absolute -bottom-12 -right-12 h-36 w-36 rounded-full bg-orange-500/5 blur-3xl" />

            <button
              onClick={() => setShowCelebration(false)}
              className="absolute top-4 right-4 text-zinc-400 hover:text-white transition-colors"
            >
              <X className="h-5 w-5" />
            </button>

            <div className="flex h-16 w-16 mx-auto items-center justify-center rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 mb-4 animate-bounce">
              <PartyPopper className="h-8 w-8" />
            </div>

            <h3 className="text-xl font-extrabold text-white tracking-tight">
              Redemption Successful!
            </h3>
            <p className="text-xs text-muted-foreground mt-1 px-4">
              Your transaction has been processed in the database. The benefits have been applied directly to your account details.
            </p>

            <div className="my-6 p-4 rounded-xl bg-zinc-900/80 border border-zinc-850 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 border border-primary/20 text-[#FF6500]">
                  {IconMap[redeemedItem.badge_icon] ? (
                    (() => {
                      const Icon = IconMap[redeemedItem.badge_icon];
                      return <Icon className="h-5 w-5" />;
                    })()
                  ) : (
                    <Sparkles className="h-5 w-5" />
                  )}
                </span>
                <div className="text-left">
                  <p className="text-xs font-bold text-white">{redeemedItem.title}</p>
                  <p className="text-[10px] text-emerald-400 font-medium font-mono">Activated & Active</p>
                </div>
              </div>
              <div className="text-right font-mono">
                <span className="block text-[8px] text-muted-foreground uppercase">Deduction</span>
                <span className="text-xs font-black text-rose-500">-{redeemedItem.cost} XP</span>
              </div>
            </div>

            <Button
              className="w-full bg-[#FF6500] hover:bg-orange-600 text-white font-bold border-none"
              onClick={() => setShowCelebration(false)}
            >
              Acknowledge & Continue
            </Button>
          </Card>
        </div>
      )}
    </AppShell>
  );
}

export default StorePage;
