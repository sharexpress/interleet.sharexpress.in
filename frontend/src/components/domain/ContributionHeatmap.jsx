/**
 * ContributionHeatmap — LeetCode-style 52-week × 7-day contribution grid
 * Features: month labels, hover tooltips, brand-colored intensity, responsive
 */
import { useMemo, useState } from "react";

const DAYS_IN_WEEK = 7;
const WEEKS_DESKTOP = 53;
const WEEKS_MOBILE = 26;

// Brand-themed intensity colors (Interleet orange gradient)
const INTENSITY_COLORS = [
  "rgba(39, 39, 42, 0.4)",      // 0 contributions
  "rgba(255, 101, 0, 0.20)",    // 1 contribution
  "rgba(255, 101, 0, 0.45)",    // 2 contributions
  "rgba(255, 101, 0, 0.70)",    // 3 contributions
  "rgba(255, 101, 0, 1.0)",     // 4+ contributions
];

const MONTH_LABELS = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

const DAY_LABELS = ["", "Mon", "", "Wed", "", "Fri", ""];

function getDateStr(d) {
  return d.toISOString().split("T")[0];
}

function formatDate(dateStr) {
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export default function ContributionHeatmap({ heatmap = {}, className = "" }) {
  const [hoveredDay, setHoveredDay] = useState(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });

  const { grid, monthPositions, totalContributions, longestStreak, todayStr } =
    useMemo(() => {
      const today = new Date();
      const todayStr = getDateStr(today);
      const currentYear = today.getFullYear();

      // Start date: January 1st of the current year
      const startDate = new Date(currentYear, 0, 1);
      // Align to the previous Sunday
      const dayOfWeek = startDate.getDay();
      startDate.setDate(startDate.getDate() - dayOfWeek);

      const grid = [];
      const monthPositions = [];
      let lastMonth = -1;

      for (let w = 0; w < WEEKS_DESKTOP; w++) {
        const weekCells = [];
        for (let d = 0; d < DAYS_IN_WEEK; d++) {
          const cellDate = new Date(startDate);
          cellDate.setDate(startDate.getDate() + w * 7 + d);
          const dateStr = getDateStr(cellDate);
          const count = heatmap[dateStr] || 0;

          weekCells.push({ dateStr, count, weekIdx: w, dayIdx: d });

          // Track month positions for labels (first Sunday of each month of the current year)
          const month = cellDate.getMonth();
          if (month !== lastMonth && d === 0 && cellDate.getFullYear() === currentYear) {
            monthPositions.push({ month, weekIdx: w });
            lastMonth = month;
          }
        }
        grid.push(weekCells);
      }

      // Calculate totals
      const totalContributions = Object.values(heatmap).reduce(
        (a, b) => a + b,
        0
      );

      // Calculate longest streak
      let longestStreak = 0;
      let currentStreak = 0;
      const totalDays = WEEKS_DESKTOP * DAYS_IN_WEEK;
      for (let i = 0; i < totalDays; i++) {
        const d = new Date(startDate);
        d.setDate(startDate.getDate() + i);
        const dStr = getDateStr(d);
        if (heatmap[dStr] && heatmap[dStr] > 0) {
          currentStreak++;
          longestStreak = Math.max(longestStreak, currentStreak);
        } else {
          currentStreak = 0;
        }
      }

      return { grid, monthPositions, totalContributions, longestStreak, todayStr };
    }, [heatmap]);

  const monthBoundaryWeeks = useMemo(() => {
    return new Set(monthPositions.map(p => p.weekIdx).filter(w => w > 0));
  }, [monthPositions]);

  const handleMouseEnter = (e, cell) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setHoveredDay(cell);
    setTooltipPos({
      x: rect.left + rect.width / 2,
      y: rect.top - 8,
    });
  };

  const handleMouseLeave = () => {
    setHoveredDay(null);
  };

  return (
    <div className={`relative w-full ${className}`}>
      {/* Month Labels (GitHub-style linear alignment) */}
      <div className="flex gap-1">
        {/* Spacer to match Day Labels width */}
        <div className="w-6 shrink-0" />
        
        {/* Month Labels Container */}
        <div className="relative flex-1 h-4">
          {monthPositions.map((mp, idx) => {
            const prevWeek = idx > 0 ? monthPositions[idx - 1].weekIdx : -3;
            if (mp.weekIdx - prevWeek < 2) return null;
            return (
              <span
                key={`${mp.month}-${mp.weekIdx}`}
                className="absolute text-[9px] font-mono text-muted-foreground uppercase tracking-wider whitespace-nowrap"
                style={{
                  left: `${(mp.weekIdx / WEEKS_DESKTOP) * 100}%`,
                }}
              >
                {MONTH_LABELS[mp.month]}
              </span>
            );
          })}
        </div>
      </div>

      <div className="flex gap-1 mt-1.5">
        {/* Day of Week Labels */}
        <div className="flex flex-col justify-between py-[2px] pr-1 shrink-0 w-6">
          {DAY_LABELS.map((label, i) => (
            <span
              key={i}
              className="h-[11px] text-[8px] font-mono text-muted-foreground flex items-center justify-end"
            >
              {label}
            </span>
          ))}
        </div>

        {/* Grid (GitHub-style contiguous layout) */}
        <div className="flex gap-[3px] w-full flex-1 overflow-hidden">
          {grid.map((week, weekIdx) => (
            <div key={weekIdx} className="flex-1 flex flex-col gap-[3px]">
              {week.map((cell) => {
                const bucket = Math.min(cell.count, 4);
                const isToday = cell.dateStr === todayStr;
                return (
                  <span
                    key={cell.dateStr}
                    style={{ backgroundColor: INTENSITY_COLORS[bucket] }}
                    className={`w-full aspect-square rounded-[2px] transition-all duration-200 cursor-pointer
                      ${isToday ? "ring-1 ring-[#FF6500]/60 ring-offset-1 ring-offset-zinc-950" : ""}
                      hover:scale-150 hover:z-10`}
                    onMouseEnter={(e) => handleMouseEnter(e, cell)}
                    onMouseLeave={handleMouseLeave}
                  />
                );
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Summary */}
      <div className="flex items-center justify-between mt-3">
        <p className="text-[11px] text-muted-foreground font-mono">
          <span className="text-white font-semibold">
            {totalContributions}
          </span>{" "}
          contributions in the last year
          {longestStreak > 0 && (
            <span className="ml-2 text-[#FF6500]">
              · {longestStreak}-day longest streak
            </span>
          )}
        </p>

        {/* Legend */}
        <div className="flex items-center gap-1 text-[9px] text-muted-foreground font-mono">
          <span>Less</span>
          {INTENSITY_COLORS.map((bg, i) => (
            <span
              key={i}
              style={{ backgroundColor: bg }}
              className="h-[9px] w-[9px] rounded-[2px]"
            />
          ))}
          <span>More</span>
        </div>
      </div>

      {/* Tooltip */}
      {hoveredDay && (
        <div
          className="fixed z-50 px-2.5 py-1.5 rounded-md bg-zinc-900 border border-zinc-700 shadow-lg text-xs font-mono pointer-events-none"
          style={{
            left: tooltipPos.x,
            top: tooltipPos.y,
            transform: "translate(-50%, -100%)",
          }}
        >
          <span className="text-white font-semibold">
            {hoveredDay.count}{" "}
            {hoveredDay.count === 1 ? "contribution" : "contributions"}
          </span>
          <span className="text-muted-foreground ml-1">
            on {formatDate(hoveredDay.dateStr)}
          </span>
        </div>
      )}
    </div>
  );
}
