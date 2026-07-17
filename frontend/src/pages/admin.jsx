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

import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { toast } from "sonner";
import { API } from "@/api/api";
import { GetCurrentUser } from "@/redux/slices/userSlice";
import { FetchChallenges } from "@/redux/slices/challengesSlice";
import { AppShell, PageHeader } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  ShieldCheck,
  Lock,
  Loader2,
  Plus,
  Edit2,
  Trash2,
  Star,
  Globe,
  Settings,
  FolderCode,
  ArrowLeft,
  X,
  Play,
  Users,
  Briefcase,
  Layers,
  Sparkles,
  Bot,
  Mail,
  Send
} from "lucide-react";

export default function AdminPage() {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.user);
  const challenges = useSelector((state) => state.challenges.items);
  const challengesLoading = useSelector((state) => state.challenges.loading);

  // General App/Admin states
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);

  // Tab selections
  const [dashboardTab, setDashboardTab] = useState("challenges");

  // Loaded admin lists
  const [usersList, setUsersList] = useState([]);
  const [usersLoading, setUsersLoading] = useState(false);

  const [presetsList, setPresetsList] = useState([]);
  const [presetsLoading, setPresetsLoading] = useState(false);

  const [sdChallenges, setSdChallenges] = useState([]);
  const [sdTemplates, setSdTemplates] = useState([]);
  const [sdLoading, setSdLoading] = useState(false);

  // CRUD modal controls
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [formMode, setFormMode] = useState("create"); // "create" | "edit"
  const [activeFormTab, setActiveFormTab] = useState("basic"); // "basic" | "code" | "tests"
  const [editingSlug, setEditingSlug] = useState(null);

  // Challenge Form fields
  const [title, setTitle] = useState("");
  const [slug, setSlug] = useState("");
  const [domain, setDomain] = useState("Backend");
  const [difficulty, setDifficulty] = useState("Medium");
  const [summary, setSummary] = useState("");
  const [description, setDescription] = useState("");
  const [xp, setXp] = useState(100);
  const [minutes, setMinutes] = useState(30);
  const [tagsText, setTagsText] = useState("");
  const [isPremium, setIsPremium] = useState(false);
  const [javascript, setJavascript] = useState("");
  const [typescript, setTypescript] = useState("");
  const [python, setPython] = useState("");
  const [go, setGo] = useState("");
  const [testCases, setTestCases] = useState([]);

  // Preset CRUD states (AI Interview Roles)
  const [isPresetModalOpen, setIsPresetModalOpen] = useState(false);
  const [presetId, setPresetId] = useState("");
  const [presetTitle, setPresetTitle] = useState("");
  const [presetDesc, setPresetDesc] = useState("");
  const [presetDuration, setPresetDuration] = useState(45);
  const [presetFormMode, setPresetFormMode] = useState("create");

  // System Design Challenge CRUD states
  const [isSdChallengeModalOpen, setIsSdChallengeModalOpen] = useState(false);
  const [sdChallengeId, setSdChallengeId] = useState("");
  const [sdChallengeTitle, setSdChallengeTitle] = useState("");
  const [sdChallengeDifficulty, setSdChallengeDifficulty] = useState("Medium");
  const [sdChallengeTags, setSdChallengeTags] = useState("");
  const [sdChallengeBrief, setSdChallengeBrief] = useState("");
  const [sdChallengeReqs, setSdChallengeReqs] = useState("");
  const [sdChallengeHints, setSdChallengeHints] = useState("");
  const [sdChallengeFormMode, setSdChallengeFormMode] = useState("create");

  // System Design Template CRUD states
  const [isSdTemplateModalOpen, setIsSdTemplateModalOpen] = useState(false);
  const [sdTemplateId, setSdTemplateId] = useState("");
  const [sdTemplateName, setSdTemplateName] = useState("");
  const [sdTemplateCategory, setSdTemplateCategory] = useState("General");
  const [sdTemplateDesc, setSdTemplateDesc] = useState("");
  const [sdTemplateNodesJson, setSdTemplateNodesJson] = useState("[]");
  const [sdTemplateEdgesJson, setSdTemplateEdgesJson] = useState("[]");
  const [sdTemplateFormMode, setSdTemplateFormMode] = useState("create");

  // Mail Dispatcher states
  // Mail Dispatcher states
  const [mailSubject, setMailSubject] = useState("🚀 Boost Your Placements Prep: 79 Interactive Coding Challenges Live!");
  const [mailTemplate, setMailTemplate] = useState(`<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Boost Your Placement Coding Prep on Interleet</title>
</head>
<body style="margin: 0; padding: 0; background-color: #050505; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #ffffff;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #050505; padding: 40px 20px;">
    <tr>
      <td align="center">
        <!-- Main Card Container -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 500px; background-color: #0f0f0f; border: 1px solid #1f1f1f; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
          <!-- Top Accent Line -->
          <tr>
            <td height="4" style="background-color: #ff6500; line-height: 4px; font-size: 4px;">&nbsp;</td>
          </tr>
          
          <!-- Content Padding -->
          <tr>
            <td style="padding: 40px 30px; text-align: left;">
              
              <!-- Brand Header -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 24px;">
                <tr>
                  <td align="center">
                    <img src="cid:logo" alt="Interleet Logo" style="height: 45px; width: auto; max-width: 180px; object-fit: contain; margin: 0 auto; display: block;" />
                  </td>
                </tr>
              </table>

              <!-- Main Title -->
              <h1 style="font-size: 20px; font-weight: 800; margin: 0 0 4px 0; color: #ffffff; text-align: center; letter-spacing: -0.5px;">
                Get Placements Ready on Interleet
              </h1>
              <p style="font-size: 13px; color: #ff6500; text-align: center; margin: 0 0 24px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                Interactive Coding Sandbox for Placements Prep
              </p>
              
              <!-- Greeting -->
              <p style="font-size: 14px; line-height: 1.6; color: #ffffff; margin: 0 0 16px 0;">
                Hey {{username}},
              </p>
              
              <!-- Body Description -->
              <p style="font-size: 14px; line-height: 1.6; color: #a1a1a1; margin: 0 0 20px 0;">
                Campus placements and coding rounds (like TCS, Infosys, and startups) are just around the corner. To stand out from thousands of candidates, practicing static MCQs won't cut it. You need real, hands-on execution.
              </p>
              
              <p style="font-size: 14px; line-height: 1.6; color: #a1a1a1; margin: 0 0 20px 0;">
                Interleet has just added <strong>20 brand-new Frontend challenges</strong> alongside our <strong>50+ Backend, Database, and DevOps challenges</strong>. You can code in JavaScript, Python, Go, Java, C++, or Rust with real-time feedback and validation!
              </p>

              <!-- Features Box -->
              <div style="background-color: #141414; border: 1px solid #262626; border-radius: 8px; padding: 20px; margin: 24px 0;">
                <h3 style="font-size: 13px; margin: 0 0 12px 0; color: #ff6500; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Placement Topics Covered:</h3>
                <ul style="margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.8; color: #d4d4d8; list-style-type: square;">
                  <li><strong>Data Structures & Algorithms</strong>: Array, Linked List, Monotonic Queue, Sorting.</li>
                  <li><strong>SQL & Databases</strong>: Multi-table JOIN builders and schema index advisors.</li>
                  <li><strong>Interactive UI Components</strong>: Star Ratings, Shopping Carts, Autocomplete drop-downs.</li>
                  <li><strong>Full-Stack APIs</strong>: Build and deploy RESTful services with SQLite and MongoDB.</li>
                </ul>
              </div>

              <p style="font-size: 14px; line-height: 1.6; color: #a1a1a1; margin: 0 0 28px 0;">
                No setups, no packages, no dependencies. Just click, open the interactive compiler, and write code to pass the behavioral test cases!
              </p>
              
              <!-- CTA Button -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td align="center">
                    <a href="https://interleet.sharexpress.in/app/challenges" style="background-color: #ff6500; color: #ffffff !important; text-decoration: none !important; padding: 14px 28px; font-size: 14px; font-weight: 700; border-radius: 6px; display: inline-block; box-shadow: 0 4px 12px rgba(255, 101, 0, 0.3); border: none; outline: none; text-align: center;">
                      <span style="color: #ffffff !important; text-decoration: none !important;">Start Practicing Now</span>
                    </a>
                  </td>
                </tr>
              </table>

            </td>
          </tr>
          
          <!-- Footer -->
          <tr>
            <td style="background-color: #0a0a0a; border-top: 1px solid #1f1f1f; padding: 20px; text-align: center;">
              <p style="font-size: 11px; color: #525252; margin: 0 0 4px 0;">
                You received this because you are a registered user of Interleet.
              </p>
              <p style="font-size: 11px; color: #3f3f46; margin: 0; text-transform: uppercase; letter-spacing: 1px;">
                &copy; 2026 Interleet. All rights reserved.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`);
  const [testEmail, setTestEmail] = useState("");
  const [dispatchingMail, setDispatchingMail] = useState(false);


  // Fetch admin items
  useEffect(() => {
    if (user?.role === "admin") {
      if (dashboardTab === "challenges") {
        dispatch(FetchChallenges());
      } else if (dashboardTab === "users") {
        fetchUsers();
      } else if (dashboardTab === "interviews") {
        fetchPresets();
      } else if (dashboardTab === "systemdesign") {
        fetchSystemDesign();
      }
    }
  }, [user, dashboardTab, dispatch]);

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    if (!email.trim() || !code.trim()) {
      toast.error("Please enter email and special code.");
      return;
    }
    setLoginLoading(true);
    try {
      const response = await API.post("/auth/admin/login", { email, code });
      if (response.data.success) {
        toast.success("Welcome, Administrator.");
        dispatch(GetCurrentUser());
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Invalid credentials.");
    } finally {
      setLoginLoading(false);
    }
  };

  // User Actions
  const fetchUsers = async () => {
    setUsersLoading(true);
    try {
      const response = await API.get("/api/admin/users");
      setUsersList(response.data);
    } catch (err) {
      toast.error("Failed to load users list.");
    } finally {
      setUsersLoading(false);
    }
  };

  const handleUpdateUser = async (uId, fields) => {
    try {
      await API.patch(`/api/admin/users/${uId}`, fields);
      toast.success("User configuration updated.");
      fetchUsers();
    } catch (err) {
      toast.error("Failed to update user status.");
    }
  };

  const handleSendMail = async (isTest = false) => {
    if (!mailSubject.trim() || !mailTemplate.trim()) {
      toast.error("Subject and Template are required.");
      return;
    }
    if (isTest && !testEmail.trim()) {
      toast.error("Please provide a test target email address.");
      return;
    }

    if (!isTest && !window.confirm("ARE YOU SURE? This will send this email campaign to ALL registered users immediately!")) {
      return;
    }

    setDispatchingMail(true);
    try {
      const payload = {
        subject: mailSubject,
        html_template: mailTemplate,
        test_email: isTest ? testEmail.trim() : undefined,
      };
      const response = await API.post("/api/admin/mail/send", payload);
      if (response.data.success) {
        toast.success(isTest ? "Test email dispatched." : "Bulk email campaign queued in background.");
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to dispatch email.");
    } finally {
      setDispatchingMail(false);
    }
  };


  // Preset Actions (AI Interview Roles)
  const fetchPresets = async () => {
    setPresetsLoading(true);
    try {
      const response = await API.get("/api/admin/presets");
      setPresetsList(response.data);
    } catch (err) {
      toast.error("Failed to load interview presets.");
    } finally {
      setPresetsLoading(false);
    }
  };

  const handleOpenPresetCreate = () => {
    setPresetFormMode("create");
    setPresetId("");
    setPresetTitle("");
    setPresetDesc("");
    setPresetDuration(45);
    setIsPresetModalOpen(true);
  };

  const handleOpenPresetEdit = (p) => {
    setPresetFormMode("edit");
    setPresetId(p.id);
    setPresetTitle(p.title);
    setPresetDesc(p.description);
    setPresetDuration(p.duration_minutes);
    setIsPresetModalOpen(true);
  };

  const handleSavePreset = async () => {
    if (!presetId.trim() || !presetTitle.trim()) {
      toast.error("ID and Title are required.");
      return;
    }
    try {
      await API.post(`/api/admin/presets/${presetId}`, {
        title: presetTitle,
        description: presetDesc,
        duration_minutes: parseInt(presetDuration) || 45
      });
      toast.success("Preset saved successfully.");
      setIsPresetModalOpen(false);
      fetchPresets();
    } catch (err) {
      toast.error("Failed to save preset.");
    }
  };

  const handleDeletePreset = async (pId) => {
    if (!window.confirm("Archive this interview preset?")) return;
    try {
      await API.delete(`/api/admin/presets/${pId}`);
      toast.success("Preset deleted.");
      fetchPresets();
    } catch (err) {
      toast.error("Failed to delete preset.");
    }
  };

  // System Design Actions
  const fetchSystemDesign = async () => {
    setSdLoading(true);
    try {
      const response = await API.get("/api/admin/system-design/challenges");
      setSdChallenges(response.data);
      const resTemplates = await API.get("/api/admin/system-design/templates");
      setSdTemplates(resTemplates.data);
    } catch (err) {
      toast.error("Failed to load System Design details.");
    } finally {
      setSdLoading(false);
    }
  };

  // SD Challenge CRUD
  const handleOpenSdChallengeCreate = () => {
    setSdChallengeFormMode("create");
    setSdChallengeId("");
    setSdChallengeTitle("");
    setSdChallengeDifficulty("Medium");
    setSdChallengeTags("");
    setSdChallengeBrief("");
    setSdChallengeReqs("");
    setSdChallengeHints("");
    setIsSdChallengeModalOpen(true);
  };

  const handleOpenSdChallengeEdit = (c) => {
    setSdChallengeFormMode("edit");
    setSdChallengeId(c.id);
    setSdChallengeTitle(c.title);
    setSdChallengeDifficulty(c.difficulty || "Medium");
    setSdChallengeTags(c.tags ? c.tags.join(", ") : "");
    setSdChallengeBrief(c.brief || "");
    setSdChallengeReqs(c.requirements ? c.requirements.join("\n") : "");
    setSdChallengeHints(c.hints ? c.hints.join("\n") : "");
    setIsSdChallengeModalOpen(true);
  };

  const handleSaveSdChallenge = async () => {
    if (!sdChallengeId.trim() || !sdChallengeTitle.trim()) {
      toast.error("ID and Title are required.");
      return;
    }
    try {
      await API.post(`/api/admin/system-design/challenges/${sdChallengeId}`, {
        title: sdChallengeTitle,
        difficulty: sdChallengeDifficulty,
        tags: sdChallengeTags.split(",").map(t => t.trim()).filter(Boolean),
        brief: sdChallengeBrief,
        requirements: sdChallengeReqs.split("\n").map(r => r.trim()).filter(Boolean),
        hints: sdChallengeHints.split("\n").map(h => h.trim()).filter(Boolean)
      });
      toast.success("System Design challenge saved.");
      setIsSdChallengeModalOpen(false);
      fetchSystemDesign();
    } catch (err) {
      toast.error("Failed to save challenge.");
    }
  };

  const handleDeleteSdChallenge = async (id) => {
    if (!window.confirm("Delete this simulator challenge?")) return;
    try {
      await API.delete(`/api/admin/system-design/challenges/${id}`);
      toast.success("Challenge deleted.");
      fetchSystemDesign();
    } catch (err) {
      toast.error("Failed to delete challenge.");
    }
  };

  // SD Template CRUD
  const handleOpenSdTemplateCreate = () => {
    setSdTemplateFormMode("create");
    setSdTemplateId("");
    setSdTemplateName("");
    setSdTemplateCategory("General");
    setSdTemplateDesc("");
    setSdTemplateNodesJson("[]");
    setSdTemplateEdgesJson("[]");
    setIsSdTemplateModalOpen(true);
  };

  const handleOpenSdTemplateEdit = (t) => {
    setSdTemplateFormMode("edit");
    setSdTemplateId(t.id);
    setSdTemplateName(t.name);
    setSdTemplateCategory(t.category || "General");
    setSdTemplateDesc(t.description || "");
    setSdTemplateNodesJson(JSON.stringify(t.nodes || [], null, 2));
    setSdTemplateEdgesJson(JSON.stringify(t.edges || [], null, 2));
    setIsSdTemplateModalOpen(true);
  };

  const handleSaveSdTemplate = async () => {
    if (!sdTemplateId.trim() || !sdTemplateName.trim()) {
      toast.error("ID and Name are required.");
      return;
    }
    let nodes, edges;
    try {
      nodes = JSON.parse(sdTemplateNodesJson);
      edges = JSON.parse(sdTemplateEdgesJson);
    } catch (e) {
      toast.error("Invalid Nodes or Edges JSON syntax.");
      return;
    }
    try {
      await API.post(`/api/admin/system-design/templates/${sdTemplateId}`, {
        name: sdTemplateName,
        category: sdTemplateCategory,
        description: sdTemplateDesc,
        nodes,
        edges
      });
      toast.success("System Design template saved.");
      setIsSdTemplateModalOpen(false);
      fetchSystemDesign();
    } catch (err) {
      toast.error("Failed to save template.");
    }
  };

  const handleDeleteSdTemplate = async (id) => {
    if (!window.confirm("Delete this template model?")) return;
    try {
      await API.delete(`/api/admin/system-design/templates/${id}`);
      toast.success("Template deleted.");
      fetchSystemDesign();
    } catch (err) {
      toast.error("Failed to delete template.");
    }
  };

  // Coding Challenge form methods
  const handleResetForm = () => {
    setTitle("");
    setSlug("");
    setDomain("Backend");
    setDifficulty("Medium");
    setSummary("");
    setDescription("");
    setXp(100);
    setMinutes(30);
    setTagsText("");
    setIsPremium(false);
    setJavascript("");
    setTypescript("");
    setPython("");
    setGo("");
    setTestCases([]);
    setEditingSlug(null);
    setActiveFormTab("basic");
  };

  const handleOpenCreate = () => {
    handleResetForm();
    setFormMode("create");
    setIsFormOpen(true);
  };

  const handleOpenEdit = (c) => {
    setFormMode("edit");
    setEditingSlug(c.slug);
    setTitle(c.title || "");
    setSlug(c.slug || "");
    setDomain(c.domain || "Backend");
    setDifficulty(c.difficulty || "Medium");
    setSummary(c.summary || "");
    setDescription(c.description || "");
    setXp(c.xp || 100);
    setMinutes(c.minutes || 30);
    setTagsText(c.tags ? c.tags.join(", ") : "");
    setIsPremium(c.is_premium || false);
    setJavascript(c.starter_code?.javascript || "");
    setTypescript(c.starter_code?.typescript || "");
    setPython(c.starter_code?.python || "");
    setGo(c.starter_code?.go || "");
    setTestCases(c.test_cases || []);
    setIsFormOpen(true);
  };

  const handleAddTestCase = () => {
    const newId = `test_${Date.now()}`;
    setTestCases([
      ...testCases,
      { id: newId, name: `Test Case ${testCases.length + 1}`, stdin: "", expected_output: "", hidden: false, weight: 1 }
    ]);
  };

  const handleRemoveTestCase = (id) => {
    setTestCases(testCases.filter((tc) => tc.id !== id));
  };

  const handleUpdateTestCase = (id, field, value) => {
    setTestCases(testCases.map((tc) => (tc.id === id ? { ...tc, [field]: value } : tc)));
  };

  const handleSubmitForm = async () => {
    if (!title.trim() || !slug.trim() || !summary.trim()) {
      toast.error("Title, Slug, and Summary are required.");
      return;
    }
    const payload = {
      title,
      slug,
      domain,
      difficulty,
      summary,
      description,
      xp: parseInt(xp) || 0,
      minutes: parseInt(minutes) || 0,
      tags: tagsText.split(",").map(t => t.trim()).filter(Boolean),
      is_premium: isPremium,
      starter_code: { javascript, typescript, python, go },
      test_cases: testCases
    };
    try {
      if (formMode === "create") {
        await API.post("/challenges/create", payload);
        toast.success("Coding challenge created.");
      } else {
        await API.patch(`/challenges/${editingSlug}`, payload);
        toast.success("Coding challenge updated.");
      }
      setIsFormOpen(false);
      dispatch(FetchChallenges());
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to save challenge.");
    }
  };

  const handleDeleteChallenge = async (cSlug) => {
    if (!window.confirm("Archive this challenge?")) return;
    try {
      await API.delete(`/challenges/${cSlug}`);
      toast.success("Challenge archived.");
      dispatch(FetchChallenges());
    } catch (err) {
      toast.error("Failed to archive challenge.");
    }
  };

  const handleTogglePublish = async (cSlug) => {
    try {
      await API.post(`/challenges/${cSlug}/publish`);
      toast.success("Publish status updated.");
      dispatch(FetchChallenges());
    } catch (err) {
      toast.error("Failed to toggle publish status.");
    }
  };

  const handleToggleFeatured = async (cSlug) => {
    try {
      await API.post(`/challenges/${cSlug}/featured`);
      toast.success("Featured status updated.");
      dispatch(FetchChallenges());
    } catch (err) {
      toast.error("Failed to toggle featured status.");
    }
  };

  // If not logged in as Admin, render Login Page
  if (user?.role !== "admin") {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-black px-4 text-zinc-100">
        <Card className="w-full max-w-md bg-zinc-950 border-zinc-800/80 p-8 space-y-6 shadow-2xl relative overflow-hidden">
          <div className="absolute -top-12 -left-12 w-24 h-24 bg-[#FF6500]/10 rounded-full blur-2xl pointer-events-none" />
          
          <div className="flex flex-col items-center text-center space-y-2">
            <div className="flex items-center justify-center w-14 h-14 rounded-full bg-[#FF6500]/10 border border-[#FF6500]/30 text-[#FF6500] mb-2">
              <ShieldCheck className="w-7 h-7" />
            </div>
            <h2 className="text-2xl font-bold tracking-tight text-white">Admin Authentication</h2>
            <p className="text-xs text-zinc-400">Strictly restricted to platform operators only.</p>
          </div>

          <form onSubmit={handleAdminLogin} className="space-y-4 pt-2">
            <div className="space-y-1">
              <label className="text-xs font-semibold text-zinc-400">Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@interleet.com"
                className="w-full rounded-md border border-zinc-800 bg-zinc-900 px-3.5 py-2 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-[#FF6500]/70"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-semibold text-zinc-400">Special Access Code</label>
              <input
                type="password"
                required
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="••••"
                className="w-full rounded-md border border-zinc-800 bg-zinc-900 px-3.5 py-2 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-[#FF6500]/70"
              />
            </div>

            <Button
              type="submit"
              disabled={loginLoading}
              className="w-full bg-[#FF6500] hover:bg-[#E05900] text-white font-bold py-5 mt-4 rounded-md transition-all cursor-pointer"
            >
              {loginLoading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Access Control Center"}
            </Button>
          </form>

          <div className="text-center pt-2">
            <Link to="/app/dashboard" className="inline-flex items-center gap-1.5 text-xs text-zinc-500 hover:text-zinc-350">
              <ArrowLeft className="w-3.5 h-3.5" /> Back to Dashboard
            </Link>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <AppShell>
      <PageHeader
        title="Control Center"
        description="Dynamic platform configuration dashboard."
        badge="Ops"
        actions={
          <div className="flex gap-2">
            <Button variant="outline" asChild className="border-zinc-800 text-zinc-300 hover:bg-zinc-900">
              <Link to="/app/dashboard">
                <ArrowLeft className="w-4 h-4 mr-1.5" /> Back to Main App
              </Link>
            </Button>
            {dashboardTab === "challenges" && (
              <Button onClick={handleOpenCreate} className="bg-[#FF6500] hover:bg-[#E05900] text-white font-bold cursor-pointer">
                <Plus className="w-4 h-4 mr-1.5" /> New Coding Prompt
              </Button>
            )}
            {dashboardTab === "interviews" && (
              <Button onClick={handleOpenPresetCreate} className="bg-[#FF6500] hover:bg-[#E05900] text-white font-bold cursor-pointer">
                <Plus className="w-4 h-4 mr-1.5" /> New Interview Preset
              </Button>
            )}
            {dashboardTab === "systemdesign" && (
              <div className="flex gap-2">
                <Button onClick={handleOpenSdChallengeCreate} variant="outline" className="border-zinc-800 text-zinc-300 hover:bg-zinc-900">
                  <Plus className="w-4 h-4 mr-1.5" /> SD Challenge
                </Button>
                <Button onClick={handleOpenSdTemplateCreate} className="bg-[#FF6500] hover:bg-[#E05900] text-white font-bold cursor-pointer">
                  <Plus className="w-4 h-4 mr-1.5" /> SD Template
                </Button>
              </div>
            )}
          </div>
        }
      />

      <div className="px-4 py-6 md:px-8 space-y-6">
        <Tabs value={dashboardTab} onValueChange={setDashboardTab} className="w-full">
          <TabsList className="bg-zinc-950 border border-zinc-900 p-1">
            <TabsTrigger value="challenges" className="cursor-pointer">Coding Challenges</TabsTrigger>
            <TabsTrigger value="interviews" className="cursor-pointer">AI Interviews</TabsTrigger>
            <TabsTrigger value="systemdesign" className="cursor-pointer">System Design</TabsTrigger>
            <TabsTrigger value="users" className="cursor-pointer">Users & Roles</TabsTrigger>
            <TabsTrigger value="mail" className="cursor-pointer">Mail Dispatcher</TabsTrigger>
          </TabsList>

          {/* TAB: CODING CHALLENGES */}
          <TabsContent value="challenges" className="mt-4">
            <Card className="overflow-hidden border-zinc-850 bg-zinc-950 p-0">
              <table className="w-full text-sm">
                <thead className="bg-zinc-900/60 text-left text-xs text-zinc-400 font-mono tracking-wider">
                  <tr>
                    <th className="px-5 py-3.5 uppercase font-medium">Title</th>
                    <th className="px-5 py-3.5 uppercase font-medium">Domain</th>
                    <th className="px-5 py-3.5 uppercase font-medium">Difficulty</th>
                    <th className="px-5 py-3.5 uppercase font-medium text-center">Premium</th>
                    <th className="px-5 py-3.5 uppercase font-medium text-center">Featured</th>
                    <th className="px-5 py-3.5 uppercase font-medium text-center">Status</th>
                    <th className="px-5 py-3.5 text-right font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-850 text-zinc-300">
                  {challengesLoading ? (
                    <tr>
                      <td colSpan={7} className="text-center py-10">
                        <Loader2 className="w-6 h-6 animate-spin mx-auto text-[#FF6500]" />
                      </td>
                    </tr>
                  ) : challenges.map((c) => (
                    <tr key={c.slug} className="hover:bg-zinc-900/20 transition-colors">
                      <td className="px-5 py-4 font-medium text-zinc-100">{c.title}</td>
                      <td className="px-5 py-4">{c.domain}</td>
                      <td className="px-5 py-4">{c.difficulty}</td>
                      <td className="px-5 py-4 text-center">
                        <Badge variant="outline" className={c.is_premium ? "text-amber-500 border-amber-500/20" : "text-zinc-600 border-transparent"}>
                          {c.is_premium ? "Premium" : "Free"}
                        </Badge>
                      </td>
                      <td className="px-5 py-4 text-center">
                        <button onClick={() => handleToggleFeatured(c.slug)} className="text-zinc-400 hover:text-white cursor-pointer">
                          {c.is_featured ? <Star className="w-4 h-4 text-[#FF6500] fill-[#FF6500]" /> : <Star className="w-4 h-4 text-zinc-700" />}
                        </button>
                      </td>
                      <td className="px-5 py-4 text-center">
                        <button onClick={() => handleTogglePublish(c.slug)} className="cursor-pointer">
                          <Badge variant="outline" className={c.is_published ? "text-emerald-400 border-emerald-500/20" : "text-zinc-500 border-zinc-850"}>
                            {c.is_published ? "Published" : "Draft"}
                          </Badge>
                        </button>
                      </td>
                      <td className="px-5 py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <Button variant="ghost" size="icon" className="h-7 w-7 text-zinc-400" onClick={() => handleOpenEdit(c)}>
                            <Edit2 className="w-3.5 h-3.5" />
                          </Button>
                          <Button variant="ghost" size="icon" className="h-7 w-7 text-red-500/80" onClick={() => handleDeleteChallenge(c.slug)}>
                            <Trash2 className="w-3.5 h-3.5" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>
          </TabsContent>

          {/* TAB: AI INTERVIEW PRESETS */}
          <TabsContent value="interviews" className="mt-4">
            <Card className="overflow-hidden border-zinc-850 bg-zinc-950 p-0">
              <table className="w-full text-sm">
                <thead className="bg-zinc-900/60 text-left text-xs text-zinc-400 font-mono tracking-wider">
                  <tr>
                    <th className="px-5 py-3.5 uppercase font-medium">Preset ID</th>
                    <th className="px-5 py-3.5 uppercase font-medium">Role Title</th>
                    <th className="px-5 py-3.5 uppercase font-medium">Description</th>
                    <th className="px-5 py-3.5 uppercase font-medium text-center">Duration</th>
                    <th className="px-5 py-3.5 text-right font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-850 text-zinc-300">
                  {presetsLoading ? (
                    <tr>
                      <td colSpan={5} className="text-center py-10">
                        <Loader2 className="w-6 h-6 animate-spin mx-auto text-[#FF6500]" />
                      </td>
                    </tr>
                  ) : presetsList.map((p) => (
                    <tr key={p.id} className="hover:bg-zinc-900/20 transition-colors">
                      <td className="px-5 py-4 font-mono text-xs text-zinc-400">{p.id}</td>
                      <td className="px-5 py-4 font-medium text-zinc-100">{p.title}</td>
                      <td className="px-5 py-4 text-xs text-zinc-400 max-w-xs truncate">{p.description}</td>
                      <td className="px-5 py-4 text-center font-mono text-xs">{p.duration_minutes}m</td>
                      <td className="px-5 py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <Button variant="ghost" size="icon" className="h-7 w-7 text-zinc-400" onClick={() => handleOpenPresetEdit(p)}>
                            <Edit2 className="w-3.5 h-3.5" />
                          </Button>
                          <Button variant="ghost" size="icon" className="h-7 w-7 text-red-500/80" onClick={() => handleDeletePreset(p.id)}>
                            <Trash2 className="w-3.5 h-3.5" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>
          </TabsContent>

          {/* TAB: SYSTEM DESIGN SIMULATOR */}
          <TabsContent value="systemdesign" className="mt-4 space-y-6">
            <Card className="overflow-hidden border-zinc-850 bg-zinc-950 p-0">
              <div className="border-b border-zinc-850 px-4 py-3 bg-zinc-900/40">
                <p className="text-xs font-semibold text-zinc-400 uppercase tracking-wide font-mono">Sim Challenges</p>
              </div>
              <table className="w-full text-sm">
                <thead className="bg-zinc-900/60 text-left text-xs text-zinc-400 font-mono tracking-wider">
                  <tr>
                    <th className="px-5 py-3.5 uppercase font-medium">Challenge ID</th>
                    <th className="px-5 py-3.5 uppercase font-medium">Title</th>
                    <th className="px-5 py-3.5 uppercase font-medium">Difficulty</th>
                    <th className="px-5 py-3.5 uppercase font-medium text-center">Tags</th>
                    <th className="px-5 py-3.5 text-right font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-850 text-zinc-300">
                  {sdLoading ? (
                    <tr>
                      <td colSpan={5} className="text-center py-10">
                        <Loader2 className="w-6 h-6 animate-spin mx-auto text-[#FF6500]" />
                      </td>
                    </tr>
                  ) : sdChallenges.map((c) => (
                    <tr key={c.id} className="hover:bg-zinc-900/20 transition-colors">
                      <td className="px-5 py-4 font-mono text-xs text-zinc-400">{c.id}</td>
                      <td className="px-5 py-4 font-medium text-zinc-100">{c.title}</td>
                      <td className="px-5 py-4 font-mono text-xs">{c.difficulty}</td>
                      <td className="px-5 py-4 text-center text-xs text-zinc-400">{c.tags ? c.tags.join(", ") : ""}</td>
                      <td className="px-5 py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <Button variant="ghost" size="icon" className="h-7 w-7 text-zinc-400" onClick={() => handleOpenSdChallengeEdit(c)}>
                            <Edit2 className="w-3.5 h-3.5" />
                          </Button>
                          <Button variant="ghost" size="icon" className="h-7 w-7 text-red-500/80" onClick={() => handleDeleteSdChallenge(c.id)}>
                            <Trash2 className="w-3.5 h-3.5" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>

            <Card className="overflow-hidden border-zinc-850 bg-zinc-950 p-0">
              <div className="border-b border-zinc-850 px-4 py-3 bg-zinc-900/40">
                <p className="text-xs font-semibold text-zinc-400 uppercase tracking-wide font-mono">Canvas Architecture Templates</p>
              </div>
              <table className="w-full text-sm">
                <thead className="bg-zinc-900/60 text-left text-xs text-zinc-400 font-mono tracking-wider">
                  <tr>
                    <th className="px-5 py-3.5 uppercase font-medium">Template ID</th>
                    <th className="px-5 py-3.5 uppercase font-medium">Name</th>
                    <th className="px-5 py-3.5 uppercase font-medium">Category</th>
                    <th className="px-5 py-3.5 uppercase font-medium text-center">Nodes / Edges</th>
                    <th className="px-5 py-3.5 text-right font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-850 text-zinc-300">
                  {sdLoading ? (
                    <tr>
                      <td colSpan={5} className="text-center py-10">
                        <Loader2 className="w-6 h-6 animate-spin mx-auto text-[#FF6500]" />
                      </td>
                    </tr>
                  ) : sdTemplates.map((t) => (
                    <tr key={t.id} className="hover:bg-zinc-900/20 transition-colors">
                      <td className="px-5 py-4 font-mono text-xs text-zinc-400">{t.id}</td>
                      <td className="px-5 py-4 font-medium text-zinc-100">{t.name}</td>
                      <td className="px-5 py-4 text-xs">{t.category}</td>
                      <td className="px-5 py-4 text-center font-mono text-xs text-zinc-400">
                        {t.nodes?.length || 0} nodes / {t.edges?.length || 0} edges
                      </td>
                      <td className="px-5 py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <Button variant="ghost" size="icon" className="h-7 w-7 text-zinc-400" onClick={() => handleOpenSdTemplateEdit(t)}>
                            <Edit2 className="w-3.5 h-3.5" />
                          </Button>
                          <Button variant="ghost" size="icon" className="h-7 w-7 text-red-500/80" onClick={() => handleDeleteSdTemplate(t.id)}>
                            <Trash2 className="w-3.5 h-3.5" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>
          </TabsContent>

          {/* TAB: USERS & ROLES */}
          <TabsContent value="users" className="mt-4">
            <Card className="overflow-hidden border-zinc-850 bg-zinc-950 p-0">
              <table className="w-full text-sm">
                <thead className="bg-zinc-900/60 text-left text-xs text-zinc-400 font-mono tracking-wider">
                  <tr>
                    <th className="px-5 py-3.5 uppercase font-medium">Username</th>
                    <th className="px-5 py-3.5 uppercase font-medium">Email</th>
                    <th className="px-5 py-3.5 uppercase font-medium">Role</th>
                    <th className="px-5 py-3.5 uppercase font-medium text-center">Subscription</th>
                    <th className="px-5 py-3.5 uppercase font-medium text-center">Status</th>
                    <th className="px-5 py-3.5 text-right font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-850 text-zinc-300">
                  {usersLoading ? (
                    <tr>
                      <td colSpan={6} className="text-center py-10">
                        <Loader2 className="w-6 h-6 animate-spin mx-auto text-[#FF6500]" />
                      </td>
                    </tr>
                  ) : usersList.map((u) => (
                    <tr key={u.user_id} className="hover:bg-zinc-900/20 transition-colors">
                      <td className="px-5 py-4 font-medium text-zinc-100">@{u.username || "unset"}</td>
                      <td className="px-5 py-4 font-mono text-xs">{u.email}</td>
                      <td className="px-5 py-4">
                        <select
                          value={u.role || "user"}
                          onChange={(e) => handleUpdateUser(u.user_id, { role: e.target.value })}
                          className="bg-zinc-900 border border-zinc-800 text-xs rounded text-zinc-100 focus:outline-none p-1 font-semibold cursor-pointer"
                        >
                          <option value="user">User</option>
                          <option value="recruiter">Recruiter</option>
                          <option value="admin">Admin</option>
                        </select>
                      </td>
                      <td className="px-5 py-4 text-center">
                        <button
                          onClick={() => handleUpdateUser(u.user_id, { is_premium: !u.is_premium })}
                          className="cursor-pointer"
                        >
                          <Badge variant="outline" className={u.is_premium ? "text-[#FF6500] border-[#FF6500]/20 bg-[#FF6500]/5" : "text-zinc-500 border-zinc-850"}>
                            {u.is_premium ? "Premium Pro" : "Free"}
                          </Badge>
                        </button>
                      </td>
                      <td className="px-5 py-4 text-center">
                        <button
                          onClick={() => handleUpdateUser(u.user_id, { is_active: !u.is_active })}
                          className="cursor-pointer"
                        >
                          <Badge variant="outline" className={u.is_active ? "text-emerald-400 border-emerald-500/20 bg-emerald-500/5" : "text-red-500 border-red-500/20 bg-red-500/5"}>
                            {u.is_active ? "Active" : "Inactive"}
                          </Badge>
                        </button>
                      </td>
                      <td className="px-5 py-4 text-right font-mono text-xs text-zinc-400">
                        Rating: {u.overall_rating || 0}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>
          </TabsContent>

          {/* TAB: MAIL DISPATCHER */}
          <TabsContent value="mail" className="mt-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left Panel: Creator */}
              <div className="space-y-4">
                <Card className="border-zinc-850 bg-zinc-950 p-6 space-y-4">
                  <div className="flex items-center gap-2 border-b border-zinc-850 pb-4">
                    <Mail className="h-5 w-5 text-indigo-400" />
                    <div>
                      <h3 className="font-bold text-white text-base">Create Campaign</h3>
                      <p className="text-xs text-zinc-400">Design and send bulk HTML emails to all active platform users.</p>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Subject Line</label>
                    <input
                      type="text"
                      className="w-full bg-zinc-900 border border-zinc-800 rounded-md px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
                      placeholder="e.g. 🚀 20 New Interactive Frontend Challenges Are Live!"
                      value={mailSubject}
                      onChange={(e) => setMailSubject(e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">HTML Template Code</label>
                      <span className="text-[10px] text-zinc-500">Inject: <code className="text-zinc-300">{"{{username}}"}</code>, logo: <code className="text-zinc-300">{"cid:logo"}</code></span>
                    </div>
                    <textarea
                      className="w-full h-[320px] bg-zinc-900 border border-zinc-800 rounded-md p-3 text-xs text-zinc-300 font-mono focus:outline-none focus:border-indigo-500 resize-y"
                      value={mailTemplate}
                      onChange={(e) => setMailTemplate(e.target.value)}
                    />
                  </div>

                  <div className="pt-4 border-t border-zinc-850 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                    <div className="flex items-center gap-2">
                      <input
                        type="email"
                        className="bg-zinc-900 border border-zinc-800 rounded-md px-3 py-1.5 text-xs text-white focus:outline-none focus:border-indigo-500 w-44"
                        placeholder="test@example.com"
                        value={testEmail}
                        onChange={(e) => setTestEmail(e.target.value)}
                      />
                      <Button
                        variant="secondary"
                        size="xs"
                        className="text-xs"
                        disabled={dispatchingMail}
                        onClick={() => handleSendMail(true)}
                      >
                        {dispatchingMail ? <Loader2 className="h-3 w-3 animate-spin" /> : "Send Test"}
                      </Button>
                    </div>

                    <Button
                      className="bg-orange-500 hover:bg-orange-600 text-white font-bold text-xs"
                      disabled={dispatchingMail}
                      onClick={() => handleSendMail(false)}
                    >
                      {dispatchingMail ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Sending...
                        </>
                      ) : (
                        <>
                          <Send className="mr-2 h-4 w-4" />
                          Send to All Users
                        </>
                      )}
                    </Button>
                  </div>
                </Card>
              </div>

              {/* Right Panel: Interactive Live Render Preview */}
              <div className="space-y-4">
                <Card className="border-zinc-850 bg-zinc-950 p-6 flex flex-col h-[570px]">
                  <div className="flex items-center justify-between border-b border-zinc-850 pb-4 mb-4">
                    <div>
                      <h3 className="font-bold text-white text-base">Live Preview</h3>
                      <p className="text-xs text-zinc-400">Real-time render of your customized HTML template.</p>
                    </div>
                  </div>
                  <div className="flex-1 bg-white rounded-md overflow-hidden border border-zinc-200">
                    <iframe
                      title="Email Preview"
                      className="w-full h-full border-none"
                      srcDoc={mailTemplate
                        .replace(/\{\{username\}\}/g, "Jane Doe")
                        .replace(/cid:logo/g, "https://interleet.sharexpress.in/assets/logo.png")
                      }
                    />
                  </div>
                </Card>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </div>

      {/* MODAL: CODING CHALLENGE CREATOR & EDITOR */}
      <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
        <DialogContent className="max-w-[760px] max-h-[85vh] overflow-y-auto bg-zinc-950 border-zinc-850 text-zinc-100 p-0">
          <DialogHeader className="px-6 py-4 border-b border-zinc-850">
            <DialogTitle className="text-lg font-bold text-white flex items-center gap-2">
              <FolderCode className="w-5 h-5 text-[#FF6500]" />
              {formMode === "create" ? "Configure Coding Prompt" : `Edit Prompt: ${title}`}
            </DialogTitle>
            <DialogDescription className="text-zinc-450 text-xs">
              Configure code templates, difficulty, points reward, and validation test cases.
            </DialogDescription>
          </DialogHeader>

          {/* Form Tabs */}
          <div className="px-6 py-2 border-b border-zinc-850 bg-zinc-900/30 flex gap-2">
            {[
              { id: "basic", label: "Basic Info", icon: Settings },
              { id: "code", label: "Starter Code Templates", icon: Loader2 },
              { id: "tests", label: "Validation Test Cases", icon: ShieldCheck }
            ].map((t) => (
              <button
                key={t.id}
                onClick={() => setActiveFormTab(t.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-md transition-colors cursor-pointer ${
                  activeFormTab === t.id
                    ? "bg-[#FF6500]/10 text-[#FF6500] border border-[#FF6500]/20"
                    : "text-zinc-400 hover:text-zinc-200 border border-transparent"
                }`}
              >
                <t.icon className="w-3.5 h-3.5" />
                {t.label}
              </button>
            ))}
          </div>

          <div className="p-6 space-y-4">
            {activeFormTab === "basic" && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <label className="text-xs font-semibold text-zinc-400">Title</label>
                    <input
                      type="text"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      placeholder="e.g. Build a Token Bucket Rate Limiter"
                      className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm text-zinc-105 focus:outline-none focus:border-[#FF6500]/70"
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-semibold text-zinc-400">Slug</label>
                    <input
                      type="text"
                      value={slug}
                      onChange={(e) => setSlug(e.target.value)}
                      placeholder="e.g. token-bucket-rate-limiter"
                      disabled={formMode === "edit"}
                      className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm text-zinc-105 focus:outline-none focus:border-[#FF6500]/70 disabled:opacity-50"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <label className="text-xs font-semibold text-zinc-400">Domain</label>
                    <select
                      value={domain}
                      onChange={(e) => setDomain(e.target.value)}
                      className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm text-zinc-105 focus:outline-none focus:border-[#FF6500]/70"
                    >
                      <option value="Frontend">Frontend</option>
                      <option value="Backend">Backend</option>
                      <option value="Fullstack">Fullstack</option>
                      <option value="DevOps">DevOps</option>
                      <option value="Databases">Databases</option>
                      <option value="APIs">APIs</option>
                      <option value="System Design">System Design</option>
                    </select>
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-semibold text-zinc-400">Difficulty</label>
                    <select
                      value={difficulty}
                      onChange={(e) => setDifficulty(e.target.value)}
                      className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm text-zinc-105 focus:outline-none focus:border-[#FF6500]/70"
                    >
                      <option value="Easy">Easy</option>
                      <option value="Medium">Medium</option>
                      <option value="Hard">Hard</option>
                      <option value="Expert">Expert</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="space-y-1">
                    <label className="text-xs font-semibold text-zinc-400">XP Reward</label>
                    <input
                      type="number"
                      value={xp}
                      onChange={(e) => setXp(e.target.value)}
                      className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-semibold text-zinc-400">Estimated Minutes</label>
                    <input
                      type="number"
                      value={minutes}
                      onChange={(e) => setMinutes(e.target.value)}
                      className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
                    />
                  </div>
                  <div className="flex items-center gap-2 pt-6">
                    <input
                      id="premium-lock"
                      type="checkbox"
                      checked={isPremium}
                      onChange={(e) => setIsPremium(e.target.checked)}
                      className="w-4 h-4 text-[#FF6500] bg-zinc-900 border-zinc-800 rounded focus:ring-[#FF6500]/50"
                    />
                    <label htmlFor="premium-lock" className="text-xs font-semibold text-zinc-300 flex items-center gap-1 cursor-pointer">
                      <Star className="w-3.5 h-3.5 text-amber-500 fill-amber-500/10" /> Is Premium Lock
                    </label>
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-semibold text-zinc-400">Tags (comma-separated)</label>
                  <input
                    type="text"
                    value={tagsText}
                    onChange={(e) => setTagsText(e.target.value)}
                    placeholder="concurrency, redis, rate-limiting"
                    className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-semibold text-zinc-400">Short Summary (displayed on cards)</label>
                  <input
                    type="text"
                    value={summary}
                    onChange={(e) => setSummary(e.target.value)}
                    placeholder="Short description..."
                    className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-semibold text-zinc-400">Problem Description (Markdown)</label>
                  <textarea
                    rows={5}
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Full specifications..."
                    className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm focus:outline-none"
                  />
                </div>
              </div>
            )}

            {activeFormTab === "code" && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <label className="text-xs font-mono font-semibold text-zinc-400">JavaScript</label>
                    <textarea
                      rows={5}
                      value={javascript}
                      onChange={(e) => setJavascript(e.target.value)}
                      placeholder="// JS stub..."
                      className="w-full rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2 text-xs font-mono focus:outline-none"
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-mono font-semibold text-zinc-400">TypeScript</label>
                    <textarea
                      rows={5}
                      value={typescript}
                      onChange={(e) => setTypescript(e.target.value)}
                      placeholder="// TS stub..."
                      className="w-full rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2 text-xs font-mono focus:outline-none"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <label className="text-xs font-mono font-semibold text-zinc-400">Python</label>
                    <textarea
                      rows={5}
                      value={python}
                      onChange={(e) => setPython(e.target.value)}
                      placeholder="# Python stub..."
                      className="w-full rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2 text-xs font-mono focus:outline-none"
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-mono font-semibold text-zinc-400">Go</label>
                    <textarea
                      rows={5}
                      value={go}
                      onChange={(e) => setGo(e.target.value)}
                      placeholder="// Go stub..."
                      className="w-full rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2 text-xs font-mono focus:outline-none"
                    />
                  </div>
                </div>
              </div>
            )}

            {activeFormTab === "tests" && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-zinc-400">Assert correct execution standard.</span>
                  <Button variant="outline" size="sm" onClick={handleAddTestCase} className="border-zinc-800 hover:bg-zinc-900 text-xs">
                    <Plus className="w-3.5 h-3.5 mr-1" /> Add test case
                  </Button>
                </div>
                <div className="space-y-4 max-h-[350px] overflow-y-auto pr-1">
                  {testCases.map((tc) => (
                    <Card key={tc.id} className="border-zinc-850 bg-zinc-900/30 p-4 space-y-3 relative">
                      <button onClick={() => handleRemoveTestCase(tc.id)} className="absolute top-2 right-2 text-zinc-500 hover:text-red-400">
                        <X className="w-4 h-4" />
                      </button>
                      <div className="grid grid-cols-3 gap-3">
                        <div className="space-y-1 col-span-2">
                          <label className="text-[10px] text-zinc-500 font-semibold">Test Case Name</label>
                          <input
                            type="text"
                            value={tc.name}
                            onChange={(e) => handleUpdateTestCase(tc.id, "name", e.target.value)}
                            className="w-full rounded border border-zinc-800 bg-zinc-900 px-2 py-1 text-xs text-zinc-100"
                          />
                        </div>
                        <div className="space-y-1">
                          <label className="text-[10px] text-zinc-500 font-semibold">Weight</label>
                          <input
                            type="number"
                            value={tc.weight}
                            onChange={(e) => handleUpdateTestCase(tc.id, "weight", parseInt(e.target.value) || 1)}
                            className="w-full rounded border border-zinc-800 bg-zinc-900 px-2 py-1 text-xs text-zinc-100"
                          />
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-3">
                        <div className="space-y-1">
                          <label className="text-[10px] text-zinc-500 font-mono">STDIN Input</label>
                          <textarea
                            rows={2}
                            value={tc.stdin}
                            onChange={(e) => handleUpdateTestCase(tc.id, "stdin", e.target.value)}
                            className="w-full rounded border border-zinc-800 bg-zinc-900 px-2 py-1 text-xs font-mono"
                          />
                        </div>
                        <div className="space-y-1">
                          <label className="text-[10px] text-zinc-500 font-mono">Expected Output</label>
                          <textarea
                            rows={2}
                            value={tc.expected_output}
                            onChange={(e) => handleUpdateTestCase(tc.id, "expected_output", e.target.value)}
                            className="w-full rounded border border-zinc-800 bg-zinc-900 px-2 py-1 text-xs font-mono"
                          />
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          id={`hide-${tc.id}`}
                          checked={tc.hidden}
                          onChange={(e) => handleUpdateTestCase(tc.id, "hidden", e.target.checked)}
                          className="w-3.5 h-3.5 text-[#FF6500] bg-zinc-900 border-zinc-800 rounded focus:ring-[#FF6500]/50"
                        />
                        <label htmlFor={`hide-${tc.id}`} className="text-[10px] text-zinc-400 cursor-pointer">
                          Hidden test case (secret verification check)
                        </label>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </div>

          <DialogFooter className="px-6 py-4 border-t border-zinc-850 flex gap-2">
            <Button variant="outline" onClick={() => setIsFormOpen(false)} className="border-zinc-800 hover:bg-zinc-900 text-zinc-300">
              Cancel
            </Button>
            <Button onClick={handleSubmitForm} className="bg-[#FF6500] hover:bg-[#E05900] text-white font-bold cursor-pointer">
              Save changes
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* MODAL: AI INTERVIEW PRESET DIALOG */}
      <Dialog open={isPresetModalOpen} onOpenChange={setIsPresetModalOpen}>
        <DialogContent className="max-w-[500px] bg-zinc-950 border-zinc-850 text-zinc-100">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-white">
              <Bot className="w-5 h-5 text-[#FF6500]" />
              {presetFormMode === "create" ? "Add AI Interview Role Preset" : "Edit Preset"}
            </DialogTitle>
            <DialogDescription className="text-zinc-450 text-xs">
              Configure the AI role specifications for candidates mock prep.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 my-2">
            <div className="space-y-1">
              <label className="text-xs font-semibold text-zinc-400">Preset Slug ID (lowercase, no spaces)</label>
              <input
                type="text"
                value={presetId}
                onChange={(e) => setPresetId(e.target.value)}
                placeholder="e.g. devops-lead"
                disabled={presetFormMode === "edit"}
                className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none disabled:opacity-50"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-zinc-400">Role Title</label>
              <input
                type="text"
                value={presetTitle}
                onChange={(e) => setPresetTitle(e.target.value)}
                placeholder="e.g. Senior DevOps Lead"
                className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-zinc-400">Duration (Minutes)</label>
              <input
                type="number"
                value={presetDuration}
                onChange={(e) => setPresetDuration(e.target.value)}
                className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-zinc-400">Description / Focus Areas</label>
              <textarea
                rows={3}
                value={presetDesc}
                onChange={(e) => setPresetDesc(e.target.value)}
                placeholder="CI/CD pipelines, Docker, Kubernetes, AWS, infrastructure..."
                className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm focus:outline-none"
              />
            </div>
          </div>

          <DialogFooter className="pt-2 flex gap-2">
            <Button variant="outline" onClick={() => setIsPresetModalOpen(false)} className="border-zinc-800 text-zinc-300 hover:bg-zinc-900">
              Cancel
            </Button>
            <Button onClick={handleSavePreset} className="bg-[#FF6500] hover:bg-[#E05900] text-white font-bold cursor-pointer">
              Save preset
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* MODAL: SYSTEM DESIGN CHALLENGE DIALOG */}
      <Dialog open={isSdChallengeModalOpen} onOpenChange={setIsSdChallengeModalOpen}>
        <DialogContent className="max-w-[600px] max-h-[85vh] overflow-y-auto bg-zinc-950 border-zinc-850 text-zinc-100">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-white">
              <Globe className="w-5 h-5 text-[#FF6500]" />
              {sdChallengeFormMode === "create" ? "Add Simulator Prompt" : "Edit Simulator Prompt"}
            </DialogTitle>
            <DialogDescription className="text-zinc-450 text-xs">
              Configure the brief prompt description and requirements list for the architecture sandbox.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 my-2">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-zinc-400">Challenge ID Slug</label>
                <input
                  type="text"
                  value={sdChallengeId}
                  onChange={(e) => setSdChallengeId(e.target.value)}
                  placeholder="e.g. rate-limiter"
                  disabled={sdChallengeFormMode === "edit"}
                  className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none disabled:opacity-50"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-zinc-400">Title</label>
                <input
                  type="text"
                  value={sdChallengeTitle}
                  onChange={(e) => setSdChallengeTitle(e.target.value)}
                  placeholder="e.g. Design a Rate Limiter"
                  className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-zinc-400">Difficulty</label>
                <select
                  value={sdChallengeDifficulty}
                  onChange={(e) => setSdChallengeDifficulty(e.target.value)}
                  className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
                >
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-zinc-400">Tags (comma-separated)</label>
                <input
                  type="text"
                  value={sdChallengeTags}
                  onChange={(e) => setSdChallengeTags(e.target.value)}
                  placeholder="Web, Concurrency, Redis"
                  className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-zinc-400">Brief Summary</label>
              <textarea
                rows={2}
                value={sdChallengeBrief}
                onChange={(e) => setSdChallengeBrief(e.target.value)}
                placeholder="Architect a robust rate-limiting service..."
                className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-zinc-400">Core Requirements (One per line)</label>
              <textarea
                rows={3}
                value={sdChallengeReqs}
                onChange={(e) => setSdChallengeReqs(e.target.value)}
                placeholder="Generate unique identifiers&#10;Sub-100ms request validation&#10;Track active client windows"
                className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-2 text-xs font-mono focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-zinc-400">Hints & Best Practices (One per line)</label>
              <textarea
                rows={3}
                value={sdChallengeHints}
                onChange={(e) => setSdChallengeHints(e.target.value)}
                placeholder="Cache client buckets in Redis&#10;Apply sliding window filter"
                className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-2 text-xs font-mono focus:outline-none"
              />
            </div>
          </div>

          <DialogFooter className="pt-2 flex gap-2">
            <Button variant="outline" onClick={() => setIsSdChallengeModalOpen(false)} className="border-zinc-800 text-zinc-300 hover:bg-zinc-900">
              Cancel
            </Button>
            <Button onClick={handleSaveSdChallenge} className="bg-[#FF6500] hover:bg-[#E05900] text-white font-bold cursor-pointer">
              Save challenge
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* MODAL: SYSTEM DESIGN TEMPLATE DIALOG */}
      <Dialog open={isSdTemplateModalOpen} onOpenChange={setIsSdTemplateModalOpen}>
        <DialogContent className="max-w-[700px] max-h-[85vh] overflow-y-auto bg-zinc-950 border-zinc-850 text-zinc-100 p-0">
          <DialogHeader className="px-6 py-4 border-b border-zinc-850">
            <DialogTitle className="flex items-center gap-2 text-white">
              <Layers className="w-5 h-5 text-[#FF6500]" />
              {sdTemplateFormMode === "create" ? "Add Prebuilt Architecture Template" : "Edit Template Model"}
            </DialogTitle>
            <DialogDescription className="text-zinc-450 text-xs">
              Upload ready-made canvas configuration structures using custom Nodes & Edges layout variables.
            </DialogDescription>
          </DialogHeader>

          <div className="p-6 space-y-4">
            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-zinc-400">Template ID Slug</label>
                <input
                  type="text"
                  value={sdTemplateId}
                  onChange={(e) => setSdTemplateId(e.target.value)}
                  placeholder="e.g. custom-microservices"
                  disabled={sdTemplateFormMode === "edit"}
                  className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none disabled:opacity-50"
                />
              </div>

              <div className="space-y-1 col-span-2">
                <label className="text-xs font-semibold text-zinc-400">Name</label>
                <input
                  type="text"
                  value={sdTemplateName}
                  onChange={(e) => setSdTemplateName(e.target.value)}
                  placeholder="e.g. Microservices Web App Grid"
                  className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-zinc-400">Category</label>
                <input
                  type="text"
                  value={sdTemplateCategory}
                  onChange={(e) => setSdTemplateCategory(e.target.value)}
                  placeholder="Streaming, Messaging..."
                  className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
                />
              </div>
              <div className="space-y-1 col-span-2">
                <label className="text-xs font-semibold text-zinc-400">Description</label>
                <input
                  type="text"
                  value={sdTemplateDesc}
                  onChange={(e) => setSdTemplateDesc(e.target.value)}
                  placeholder="Pre-arranged nodes template display details..."
                  className="w-full rounded border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-sm focus:outline-none"
                />
              </div>
            </div>

            <div className="space-y-2">
              <div className="space-y-1">
                <label className="text-xs font-mono font-semibold text-zinc-400">Nodes Layout Array JSON</label>
                <textarea
                  rows={4}
                  value={sdTemplateNodesJson}
                  onChange={(e) => setSdTemplateNodesJson(e.target.value)}
                  placeholder="[ { 'id': 'n1', 'type': 'infra', 'position': {'x': 100, 'y': 200}, 'data': {'kind': 'client'} } ]"
                  className="w-full rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2 text-xs font-mono focus:outline-none"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-mono font-semibold text-zinc-400">Edges Connectors Array JSON</label>
                <textarea
                  rows={4}
                  value={sdTemplateEdgesJson}
                  onChange={(e) => setSdTemplateEdgesJson(e.target.value)}
                  placeholder="[ { 'id': 'e1', 'source': 'n1', 'target': 'n2', 'animated': true } ]"
                  className="w-full rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2 text-xs font-mono focus:outline-none"
                />
              </div>
            </div>
          </div>

          <DialogFooter className="px-6 py-4 border-t border-zinc-850 flex gap-2">
            <Button variant="outline" onClick={() => setIsSdTemplateModalOpen(false)} className="border-zinc-800 text-zinc-300 hover:bg-zinc-900">
              Cancel
            </Button>
            <Button onClick={handleSaveSdTemplate} className="bg-[#FF6500] hover:bg-[#E05900] text-white font-bold cursor-pointer">
              Save template
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </AppShell>
  );
}
