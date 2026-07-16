import React from "react";
import { 
  ShieldAlert, Sparkles, Trophy, Flame, Target, Award, Wrench, 
  Paintbrush, Rocket, Plug, Database, Key, GraduationCap, 
  Mic, Gem, Star, Users, Swords, UserCheck
} from "lucide-react";

/**
 * Renders a premium 3D PNG badge (from MinIO) or a highly-stylized inline SVG
 * fallback designed to resemble LeetCode's gamified achievement assets.
 */
export function BadgeIcon({ id, imageUrl, name, className = "w-10 h-10" }) {
  // If we have a custom S3 MinIO image url, render the PNG with high-performance styling
  if (imageUrl && !imageUrl.includes("badge_bronze") && !imageUrl.includes("badge_silver") && !imageUrl.includes("badge_gold") && !imageUrl.includes("badge_diamond")) {
    return (
      <img 
        src={imageUrl} 
        alt={name || "Badge"} 
        className={`${className} object-contain transition-transform duration-300 hover:scale-110`}
      />
    );
  }

  // Fallback to gorgeous custom vector inline SVGs for the remaining badges to prevent duplicates
  switch (id) {
    case "twenty_five_solves": // Code Warrior (Gold Bolt)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="gold-bolt" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#FBBF24" />
              <stop offset="100%" stopColor="#D97706" />
            </linearGradient>
            <filter id="glow-bolt" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>
          <path d="M50 5 L85 20 V55 C85 75 50 95 50 95 C50 95 15 75 15 55 V20 L50 5Z" fill="#18181B" stroke="#D97706" strokeWidth="3" />
          <path d="M52 25 L32 50 H48 L44 75 L68 45 H52 L56 25Z" fill="url(#gold-bolt)" filter="url(#glow-bolt)" />
        </svg>
      );

    case "fifty_solves": // Legend of the Arena (Platinum Wreath)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="plat-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#E2E8F0" />
              <stop offset="50%" stopColor="#94A3B8" />
              <stop offset="100%" stopColor="#475569" />
            </linearGradient>
            <filter id="plat-glow">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feComposite in="SourceGraphic" operator="over" />
            </filter>
          </defs>
          <circle cx="50" cy="50" r="42" fill="#0F172A" stroke="url(#plat-grad)" strokeWidth="4" />
          <path d="M35 60 C30 50 30 35 40 25 C45 35 45 45 35 60 Z" fill="url(#plat-grad)" />
          <path d="M65 60 C70 50 70 35 60 25 C55 35 55 45 65 60 Z" fill="url(#plat-grad)" />
          <path d="M40 38 L50 28 L60 38 L50 48 Z" fill="#E2E8F0" filter="url(#plat-glow)" />
          <path d="M44 65 H56 L50 75 Z" fill="#94A3B8" />
        </svg>
      );

    case "frontend_specialist": // Frontend Specialist (Neon Paint Layer)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="front-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#EC4899" />
              <stop offset="100%" stopColor="#8B5CF6" />
            </linearGradient>
          </defs>
          <rect x="15" y="15" width="70" height="70" rx="15" fill="#18181B" stroke="url(#front-grad)" strokeWidth="3" />
          <circle cx="35" cy="45" r="12" fill="none" stroke="#EC4899" strokeWidth="3" />
          <path d="M50 35 L70 55 M50 55 L70 35" stroke="#8B5CF6" strokeWidth="4" strokeLinecap="round" />
          <path d="M30 70 H70" stroke="#E2E8F0" strokeWidth="3" strokeLinecap="round" />
        </svg>
      );

    case "backend_specialist": // Backend Specialist (Gold Gears)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="back-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#F59E0B" />
              <stop offset="100%" stopColor="#10B981" />
            </linearGradient>
          </defs>
          <path d="M50 15 L85 35 V75 L50 90 L15 75 V35 Z" fill="#111827" stroke="url(#back-grad)" strokeWidth="3" />
          <circle cx="50" cy="50" r="18" fill="none" stroke="#F59E0B" strokeWidth="4" />
          {/* Gear teeth */}
          <path d="M50 25 V32 M50 68 V75 M25 50 H32 M68 50 H75" stroke="#F59E0B" strokeWidth="4" strokeLinecap="round" />
          <circle cx="50" cy="50" r="6" fill="#10B981" />
        </svg>
      );

    case "devops_specialist": // DevOps Specialist (Neon Rocket)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="dev-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#06B6D4" />
              <stop offset="100%" stopColor="#3B82F6" />
            </linearGradient>
          </defs>
          <rect x="15" y="15" width="70" height="70" rx="35" fill="#0F172A" stroke="url(#dev-grad)" strokeWidth="3" />
          <path d="M50 25 C50 25 58 40 58 55 C58 65 54 70 50 70 C46 70 42 65 42 55 C42 40 50 25 50 25 Z" fill="url(#dev-grad)" />
          <path d="M44 65 L35 75 L38 58 Z" fill="#3B82F6" />
          <path d="M56 65 L65 75 L62 58 Z" fill="#3B82F6" />
          <circle cx="50" cy="45" r="4" fill="#0F172A" />
        </svg>
      );

    case "api_architect": // API Architect (Linked Plugs)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="api-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#10B981" />
              <stop offset="100%" stopColor="#059669" />
            </linearGradient>
          </defs>
          <path d="M50 8 L90 30 V70 L50 92 L10 70 V30 Z" fill="#18181B" stroke="url(#api-grad)" strokeWidth="3" />
          <rect x="35" y="32" width="30" height="15" rx="3" fill="#10B981" />
          <path d="M42 47 V58 M58 47 V58" stroke="#E2E8F0" strokeWidth="4" strokeLinecap="round" />
          <path d="M50 58 C50 70 40 75 50 82" stroke="#059669" strokeWidth="3" fill="none" />
        </svg>
      );

    case "database_guru": // Database Guru (Storage Disks)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="db-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#3B82F6" />
              <stop offset="100%" stopColor="#1D4ED8" />
            </linearGradient>
          </defs>
          <path d="M20 25 C20 15 80 15 80 25 V75 C80 85 20 85 20 75 Z" fill="#0F172A" stroke="url(#db-grad)" strokeWidth="3" />
          <path d="M20 25 C20 35 80 35 80 25" stroke="url(#db-grad)" strokeWidth="3" fill="none" />
          <path d="M20 45 C20 55 80 55 80 45" stroke="url(#db-grad)" strokeWidth="3" fill="none" />
          <path d="M20 65 C20 75 80 75 80 65" stroke="url(#db-grad)" strokeWidth="3" fill="none" />
          <circle cx="50" cy="25" r="4" fill="#3B82F6" />
          <circle cx="50" cy="45" r="4" fill="#3B82F6" />
          <circle cx="50" cy="65" r="4" fill="#3B82F6" />
        </svg>
      );

    case "streak_30": // Iron Will (Locked Fire Shield)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="iron-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#EF4444" />
              <stop offset="100%" stopColor="#B91C1C" />
            </linearGradient>
          </defs>
          <path d="M50 10 L82 25 V55 C82 72 50 88 50 88 C50 88 18 72 18 55 V25 Z" fill="#18181B" stroke="url(#iron-grad)" strokeWidth="4" />
          <path d="M50 30 C50 30 58 42 58 52 C58 58 54 62 50 62 C46 62 42 58 42 52 C42 42 50 30 50 30 Z" fill="url(#iron-grad)" />
          <rect x="42" y="52" width="16" height="12" rx="3" fill="#E2E8F0" />
          <path d="M46 52 V46 C46 42 54 42 54 46 V52" stroke="#E2E8F0" strokeWidth="2.5" fill="none" />
        </svg>
      );

    case "first_interview": // Interview Scholar (Gold Cap)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="sch-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#F59E0B" />
              <stop offset="100%" stopColor="#D97706" />
            </linearGradient>
          </defs>
          <circle cx="50" cy="50" r="42" fill="#111827" stroke="url(#sch-grad)" strokeWidth="3" />
          <path d="M22 45 L50 32 L78 45 L50 58 Z" fill="url(#sch-grad)" />
          <path d="M35 50 V62 C35 68 65 68 65 62 V50" stroke="url(#sch-grad)" strokeWidth="3" fill="none" />
          <path d="M72 45 V68 L76 72" stroke="#D97706" strokeWidth="2" fill="none" />
        </svg>
      );

    case "five_interviews": // Interview Veteran (Neon Mic)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="vet-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#8B5CF6" />
              <stop offset="100%" stopColor="#EC4899" />
            </linearGradient>
          </defs>
          <rect x="18" y="18" width="64" height="64" rx="16" fill="#18181B" stroke="url(#vet-grad)" strokeWidth="3" />
          <rect x="42" y="30" width="16" height="26" rx="8" fill="url(#vet-grad)" />
          <path d="M36 43 C36 55 64 55 64 43" stroke="#E2E8F0" strokeWidth="3.5" fill="none" strokeLinecap="round" />
          <path d="M50 55 V66 M42 66 H58" stroke="#E2E8F0" strokeWidth="4.5" strokeLinecap="round" />
        </svg>
      );

    case "ace_interview": // Interview Ace (Cyan Gem)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="ace-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#06B6D4" />
              <stop offset="100%" stopColor="#0891B2" />
            </linearGradient>
          </defs>
          <path d="M50 10 L85 25 V55 C85 75 50 90 50 90 C50 90 15 75 15 55 V25 Z" fill="#0F172A" stroke="url(#ace-grad)" strokeWidth="3" />
          <path d="M50 25 L72 40 L50 75 L28 40 Z" fill="url(#ace-grad)" />
          <path d="M50 25 V75 M28 40 H72" stroke="#0891B2" strokeWidth="1.5" />
        </svg>
      );

    case "first_follower": // Rising Star (Glowing Star)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="star-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#FBBF24" />
              <stop offset="100%" stopColor="#F59E0B" />
            </linearGradient>
          </defs>
          <path d="M50 8 L88 32 L78 75 L50 92 L22 75 L12 32 Z" fill="#18181B" stroke="url(#star-grad)" strokeWidth="3" />
          <path d="M50 25 L57 41 L75 42 L61 54 L66 71 L50 62 L34 71 L39 54 L25 42 L43 41 Z" fill="url(#star-grad)" />
        </svg>
      );

    case "ten_followers": // Community Builder (Nodes Connection)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="com-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#10B981" />
              <stop offset="100%" stopColor="#3B82F6" />
            </linearGradient>
          </defs>
          <circle cx="50" cy="50" r="42" fill="#0F172A" stroke="url(#com-grad)" strokeWidth="3" />
          <circle cx="50" cy="32" r="6" fill="#10B981" />
          <circle cx="32" cy="62" r="6" fill="#3B82F6" />
          <circle cx="68" cy="62" r="6" fill="#3B82F6" />
          <circle cx="50" cy="53" r="10" fill="#10B981" />
          <path d="M50 38 V43 M37 57 L43 53 M63 57 L57 53 M50 32 L32 62 H68 Z" stroke="#E2E8F0" strokeWidth="2.5" fill="none" />
        </svg>
      );

    case "first_contest": // Arena Fighter (Colliding Gloves)
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="fighter-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#EF4444" />
              <stop offset="100%" stopColor="#F59E0B" />
            </linearGradient>
          </defs>
          <path d="M50 8 L90 30 V70 L50 92 L10 70 V30 Z" fill="#111827" stroke="url(#fighter-grad)" strokeWidth="3" />
          <circle cx="50" cy="50" r="16" fill="url(#fighter-grad)" />
          <path d="M50 34 V66 M34 50 H66" stroke="#111827" strokeWidth="4" strokeLinecap="round" />
        </svg>
      );

    default: // Generic Tier Badges Fallback (if any new or legacy badges appear)
      if (imageUrl && imageUrl.includes("badge_silver")) {
        return (
          <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="42" fill="#0F172A" stroke="#94A3B8" strokeWidth="3" />
            <path d="M50 25 L65 35 V65 L50 75 L35 65 V35 Z" fill="#94A3B8" />
          </svg>
        );
      }
      if (imageUrl && imageUrl.includes("badge_gold")) {
        return (
          <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="42" fill="#18181B" stroke="#F59E0B" strokeWidth="3" />
            <path d="M50 25 L65 35 V65 L50 75 L35 65 V35 Z" fill="#F59E0B" />
          </svg>
        );
      }
      if (imageUrl && imageUrl.includes("badge_diamond")) {
        return (
          <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="42" fill="#0F172A" stroke="#3B82F6" strokeWidth="3" />
            <path d="M50 25 L65 35 V65 L50 75 L35 65 V35 Z" fill="#3B82F6" />
          </svg>
        );
      }
      // Bronze / Common default
      return (
        <svg className={className} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="42" fill="#18181B" stroke="#B45309" strokeWidth="3" />
          <path d="M50 25 L65 35 V65 L50 75 L35 65 V35 Z" fill="#B45309" />
        </svg>
      );
  }
}
