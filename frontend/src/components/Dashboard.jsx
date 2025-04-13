import React, { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import {
  Activity,
  CreditCard,
  DollarSign,
  Download,
  Users,
  Database,
  Key,
  Bot,
  Search,
  Plus,
  Settings,
  Code,
  Zap,
  FileText,
  Globe,
  Box,
  Layers,
  Copy,
  Eye,
  EyeOff,
  RefreshCw,
  BarChart2,
  Cpu,
  Clipboard,
  LayoutDashboard,
  Menu,
} from "lucide-react";

import DashboardNav from "./DashboardNavbar";
import RecentActivity from "./RecentActivity";

import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "@/components/ui/command";

// Sample data
const usageData = [
  { name: "Jan", queries: 1250, tokens: 45000 },
  { name: "Feb", queries: 1800, tokens: 62000 },
  { name: "Mar", queries: 2200, tokens: 78000 },
  { name: "Apr", queries: 2800, tokens: 95000 },
  { name: "May", queries: 3300, tokens: 110000 },
  { name: "Jun", queries: 4100, tokens: 140000 },
  { name: "Jul", queries: 4800, tokens: 165000 },
];

const modelUsageData = [
  { name: "GPT-4", value: 45 },
  { name: "Claude", value: 25 },
  { name: "Gemini", value: 20 },
  { name: "Llama 3", value: 10 },
];

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

const sampleAgents = [
  {
    id: 1,
    name: "Customer Support Bot",
    model: "GPT-4",
    database: "Supabase",
    status: "active",
    queries: 1240,
    lastUsed: "2 hours ago",
  },
  {
    id: 2,
    name: "Legal Document Analysis",
    model: "Claude Opus",
    database: "Postgres",
    status: "active",
    queries: 876,
    lastUsed: "1 day ago",
  },
  {
    id: 3,
    name: "Product Recommendation Engine",
    model: "Gemini Pro",
    database: "Supabase",
    status: "inactive",
    queries: 2310,
    lastUsed: "3 days ago",
  },
  {
    id: 4,
    name: "Technical Documentation Assistant",
    model: "Llama 3",
    database: "MongoDB",
    status: "active",
    queries: 543,
    lastUsed: "4 hours ago",
  },
];

const sampleApiKeys = [
  {
    provider: "OpenAI",
    key: "sk-abc123********",
    status: "active",
    created: "2025-02-10",
  },
  {
    provider: "Anthropic",
    key: "sk-ant-********",
    status: "active",
    created: "2025-03-01",
  },
  {
    provider: "Google AI",
    key: "AIza********",
    status: "active",
    created: "2025-02-15",
  },
  {
    provider: "Supabase",
    key: "sbp_********",
    status: "active",
    created: "2025-01-20",
  },
];

function Dashboard() {
  const [open, setOpen] = useState(false);
  const [showNewAgentForm, setShowNewAgentForm] = useState(false);
  const [showNewKeyForm, setShowNewKeyForm] = useState(false);
  const [visibleKeys, setVisibleKeys] = useState({});
  const [closeMenu, setCloseMenu] = useState(false);
  const toggleKeyVisibility = (provider) => {
    setVisibleKeys({
      ...visibleKeys,
      [provider]: !visibleKeys[provider],
    });
  };
  const toggleMenu = () => {
    setCloseMenu(!closeMenu);
  };
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };
  const closeNavbar = () => {
    setOpen(!open);
  };
  useEffect(() => {
    const down = (e) => {
      if (e.key === "k" && e.ctrlKey) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };

    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  return (
    <>
      <div className="flex h-screen bg-neutral-100 relative    dark:bg-neutral-900">
        <div className={`${closeMenu ? "w-64":"w-0"} transition-all duration-300`}>
          <DashboardNav closeMenu={closeMenu} />
        </div>
        <main className="flex-1 w-full p-6 overflow-y-auto">
          <div className="flex items-center justify-between mb-6">
            <div>
              <Menu className="h-6 w-6 cursor-pointer" onClick={toggleMenu} />
            </div>
            <h1 className="text-3xl font-bold">RAG AI Agents</h1>
            <div className="flex items-center space-x-4">
              <div
                className="relative"
                onClick={() => {
                  setOpen(true);
                }}
              >
                <Input
                  type="text"
                  placeholder="Search..."
                  className="w-64 p-2 cursor-pointer"
                />
                <div className="absolute inset-y-0 right-0 flex items-center pr-3 border shadow rounded m-1 p-1 justify-center cursor-pointer">
                  ctrl+k
                </div>
              </div>
              <CommandDialog open={open} onOpenChange={setOpen}>
                <CommandInput placeholder="Search agents, models, or commands..." />
                <CommandList>
                  <CommandEmpty>No results found.</CommandEmpty>
                  <CommandGroup heading="Agents">
                    <CommandItem>
                      <Bot className="mr-2 h-4 w-4" />
                      <span>Create new agent</span>
                    </CommandItem>
                    <CommandItem>
                      <Search className="mr-2 h-4 w-4" />
                      <span>Search agents</span>
                    </CommandItem>
                  </CommandGroup>
                  <CommandSeparator />
                  <CommandGroup heading="API Keys">
                    <CommandItem>
                      <Key className="mr-2 h-4 w-4" />
                      <span>Add new API key</span>
                    </CommandItem>
                    <CommandItem>
                      <Database className="mr-2 h-4 w-4" />
                      <span>Manage database connections</span>
                    </CommandItem>
                  </CommandGroup>
                  <CommandSeparator />
                  <CommandGroup heading="Navigation">
                    <CommandItem>
                      <LayoutDashboard className="mr-2 h-4 w-4" />
                      <span>Dashboard</span>
                      <CommandShortcut>⌘D</CommandShortcut>
                    </CommandItem>
                    <CommandItem>
                      <Bot className="mr-2 h-4 w-4" />
                      <span>Agents</span>
                      <CommandShortcut>⌘A</CommandShortcut>
                    </CommandItem>
                    <CommandItem>
                      <Key className="mr-2 h-4 w-4" />
                      <span>API Keys</span>
                      <CommandShortcut>⌘K</CommandShortcut>
                    </CommandItem>
                    <CommandItem>
                      <Settings className="mr-2 h-4 w-4" />
                      <span>Settings</span>
                      <CommandShortcut>⌘S</CommandShortcut>
                    </CommandItem>
                  </CommandGroup>
                </CommandList>
              </CommandDialog>
              <Button>
                <Download className="mr-2 h-4 w-4" /> Export Reports
              </Button>
            </div>
          </div>

          <Tabs defaultValue="overview" className="space-y-4">
            <TabsList className="bg-gray-200">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="agents">Agents</TabsTrigger>
              <TabsTrigger value="apikeys">API Keys</TabsTrigger>
              <TabsTrigger value="settings">Settings</TabsTrigger>
            </TabsList>

            {/* OVERVIEW TAB */}
            <TabsContent value="overview" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Active Agents
                    </CardTitle>
                    <Bot className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">24</div>
                    <p className="text-xs text-muted-foreground">
                      +3 from last week
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Total Queries
                    </CardTitle>
                    <Search className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">47,842</div>
                    <p className="text-xs text-muted-foreground">
                      +12.5% from last month
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Token Usage
                    </CardTitle>
                    <Code className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">1.4M</div>
                    <p className="text-xs text-muted-foreground">
                      +8.2% from last month
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Database Connections
                    </CardTitle>
                    <Database className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">7</div>
                    <p className="text-xs text-muted-foreground">
                      3 Supabase, 4 others
                    </p>
                  </CardContent>
                </Card>
              </div>

              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4">
                  <CardHeader>
                    <CardTitle>Usage Metrics</CardTitle>
                    <CardDescription>
                      Query and token usage over time
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pl-2">
                    <ResponsiveContainer width="100%" height={350}>
                      <LineChart data={usageData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis yAxisId="left" />
                        <YAxis yAxisId="right" orientation="right" />
                        <Tooltip />
                        <Line
                          yAxisId="left"
                          type="monotone"
                          dataKey="queries"
                          stroke="#8884d8"
                          name="Queries"
                        />
                        <Line
                          yAxisId="right"
                          type="monotone"
                          dataKey="tokens"
                          stroke="#82ca9d"
                          name="Tokens"
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                <Card className="col-span-3">
                  <CardHeader>
                    <CardTitle>Model Usage Distribution</CardTitle>
                    <CardDescription>
                      AI models by usage percentage
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={250}>
                      <PieChart>
                        <Pie
                          data={modelUsageData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                          label={({ name, percent }) =>
                            `${name}: ${(percent * 100).toFixed(0)}%`
                          }
                        >
                          {modelUsageData.map((entry, index) => (
                            <Cell
                              key={`cell-${index}`}
                              fill={COLORS[index % COLORS.length]}
                            />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Agent Activity</CardTitle>
                  <CardDescription>
                    Latest interactions and performance metrics
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <RecentActivity />
                </CardContent>
              </Card>
            </TabsContent>

            {/* AGENTS TAB */}
            <TabsContent value="agents" className="space-y-4">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold">Manage AI Agents</h2>
                <Button onClick={() => setShowNewAgentForm(!showNewAgentForm)}>
                  <Plus className="mr-2 h-4 w-4" /> Create New Agent
                </Button>
              </div>

              {showNewAgentForm && (
                <Card className="mb-6">
                  <CardHeader>
                    <CardTitle>Create New RAG Agent</CardTitle>
                    <CardDescription>
                      Configure your new AI agent with database connections
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-4">
                        <div>
                          <Label htmlFor="agent-name">Agent Name</Label>
                          <Input
                            id="agent-name"
                            placeholder="e.g., Customer Support Bot"
                          />
                        </div>
                        <div>
                          <Label htmlFor="agent-model">LLM Model</Label>
                          <Select defaultValue="gpt4">
                            <SelectTrigger id="agent-model">
                              <SelectValue placeholder="Select model" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="gpt4">OpenAI GPT-4</SelectItem>
                              <SelectItem value="claude">
                                Anthropic Claude
                              </SelectItem>
                              <SelectItem value="gemini">
                                Google Gemini
                              </SelectItem>
                              <SelectItem value="llama3">
                                Meta Llama 3
                              </SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div>
                          <Label htmlFor="database-type">Database Type</Label>
                          <Select defaultValue="supabase">
                            <SelectTrigger id="database-type">
                              <SelectValue placeholder="Select database" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="supabase">Supabase</SelectItem>
                              <SelectItem value="postgres">
                                PostgreSQL
                              </SelectItem>
                              <SelectItem value="mongo">MongoDB</SelectItem>
                              <SelectItem value="pinecone">Pinecone</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                      <div className="space-y-4">
                        <div>
                          <Label htmlFor="connection-string">
                            Connection String/URL
                          </Label>
                          <Input
                            id="connection-string"
                            placeholder="e.g., https://yourproject.supabase.co"
                          />
                        </div>
                        <div>
                          <Label htmlFor="collection-name">
                            Collection/Table Name
                          </Label>
                          <Input
                            id="collection-name"
                            placeholder="e.g., knowledge_base"
                          />
                        </div>
                        <div className="flex items-center space-x-2 pt-4">
                          <Switch id="agent-active" />
                          <Label htmlFor="agent-active">
                            Activate agent immediately
                          </Label>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-end space-x-2">
                    <Button
                      variant="outline"
                      onClick={() => setShowNewAgentForm(false)}
                    >
                      Cancel
                    </Button>
                    <Button>Create Agent</Button>
                  </CardFooter>
                </Card>
              )}

              <div className="grid grid-cols-1 gap-4">
                {sampleAgents.map((agent) => (
                  <Card key={agent.id}>
                    <CardHeader className="pb-2">
                      <div className="flex justify-between items-center">
                        <CardTitle className="text-lg">{agent.name}</CardTitle>
                        <Badge
                          variant={
                            agent.status === "active" ? "default" : "secondary"
                          }
                        >
                          {agent.status === "active" ? "Active" : "Inactive"}
                        </Badge>
                      </div>
                      <CardDescription>
                        Model: {agent.model} • Database: {agent.database}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="pb-2">
                      <div className="flex justify-between text-sm">
                        <div>
                          <span className="font-medium">Queries:</span>{" "}
                          {agent.queries.toLocaleString()}
                        </div>
                        <div>
                          <span className="font-medium">Last used:</span>{" "}
                          {agent.lastUsed}
                        </div>
                      </div>
                    </CardContent>
                    <CardFooter className="flex justify-end space-x-2">
                      <Button variant="outline" size="sm">
                        <Zap className="mr-2 h-4 w-4" /> Test
                      </Button>
                      <Button variant="outline" size="sm">
                        <FileText className="mr-2 h-4 w-4" /> Logs
                      </Button>
                      <Button variant="outline" size="sm">
                        <Settings className="mr-2 h-4 w-4" /> Configure
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* API KEYS TAB */}
            <TabsContent value="apikeys" className="space-y-4">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold">API Key Management</h2>
                <Button onClick={() => setShowNewKeyForm(!showNewKeyForm)}>
                  <Plus className="mr-2 h-4 w-4" /> Add New API Key
                </Button>
              </div>

              {showNewKeyForm && (
                <Card className="mb-6">
                  <CardHeader>
                    <CardTitle>Add New API Key</CardTitle>
                    <CardDescription>
                      Enter your API key for integration
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-4">
                        <div>
                          <Label htmlFor="provider">API Provider</Label>
                          <Select defaultValue="openai">
                            <SelectTrigger id="provider">
                              <SelectValue placeholder="Select provider" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="openai">OpenAI</SelectItem>
                              <SelectItem value="anthropic">
                                Anthropic
                              </SelectItem>
                              <SelectItem value="google">Google AI</SelectItem>
                              <SelectItem value="supabase">Supabase</SelectItem>
                              <SelectItem value="other">Other</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div>
                          <Label htmlFor="api-key">API Key</Label>
                          <Input
                            id="api-key"
                            type="password"
                            placeholder="Enter your API key"
                          />
                        </div>
                      </div>
                      <div className="space-y-4">
                        <div>
                          <Label htmlFor="key-name">Key Name (Optional)</Label>
                          <Input
                            id="key-name"
                            placeholder="e.g., Production OpenAI"
                          />
                        </div>
                        <div className="flex items-center space-x-2 pt-4">
                          <Switch id="key-active" defaultChecked />
                          <Label htmlFor="key-active">
                            Activate key immediately
                          </Label>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-end space-x-2">
                    <Button
                      variant="outline"
                      onClick={() => setShowNewKeyForm(false)}
                    >
                      Cancel
                    </Button>
                    <Button>Save API Key</Button>
                  </CardFooter>
                </Card>
              )}

              <div className="grid grid-cols-1 gap-4">
                {sampleApiKeys.map((key) => (
                  <Card key={key.provider}>
                    <CardHeader className="pb-2">
                      <div className="flex justify-between items-center">
                        <CardTitle className="text-lg">
                          {key.provider}
                        </CardTitle>
                        <Badge
                          variant={
                            key.status === "active" ? "default" : "secondary"
                          }
                        >
                          {key.status === "active" ? "Active" : "Inactive"}
                        </Badge>
                      </div>
                      <CardDescription>Created: {key.created}</CardDescription>
                    </CardHeader>
                    <CardContent className="pb-2">
                      <div className="flex justify-between items-center">
                        <div className="font-mono bg-gray-100 p-2 rounded flex-1 mr-2">
                          {visibleKeys[key.provider]
                            ? key.key.replace("********", "abcdefgh1234")
                            : key.key}
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => toggleKeyVisibility(key.provider)}
                        >
                          {visibleKeys[key.provider] ? (
                            <EyeOff className="h-4 w-4" />
                          ) : (
                            <Eye className="h-4 w-4" />
                          )}
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => copyToClipboard(key.key)}
                        >
                          <Copy className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardContent>
                    <CardFooter className="flex justify-end space-x-2">
                      <Button variant="outline" size="sm">
                        <RefreshCw className="mr-2 h-4 w-4" /> Rotate
                      </Button>
                      <Button variant="outline" size="sm">
                        <Settings className="mr-2 h-4 w-4" /> Configure
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            </TabsContent>

            {/* SETTINGS TAB */}
            <TabsContent value="settings" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Platform Settings</CardTitle>
                  <CardDescription>
                    Configure global settings for your RAG platform
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-4">
                    <h3 className="text-lg font-medium">
                      Default LLM Configurations
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="default-model">Default LLM Model</Label>
                        <Select defaultValue="gpt4">
                          <SelectTrigger id="default-model">
                            <SelectValue placeholder="Select model" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="gpt4">OpenAI GPT-4</SelectItem>
                            <SelectItem value="claude">
                              Anthropic Claude
                            </SelectItem>
                            <SelectItem value="gemini">
                              Google Gemini
                            </SelectItem>
                            <SelectItem value="llama3">Meta Llama 3</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div>
                        <Label htmlFor="default-temperature">
                          Default Temperature
                        </Label>
                        <Input
                          id="default-temperature"
                          type="number"
                          defaultValue="0.7"
                          min="0"
                          max="1"
                          step="0.1"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="text-lg font-medium">
                      Database Connections
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="default-db">Default Database</Label>
                        <Select defaultValue="supabase">
                          <SelectTrigger id="default-db">
                            <SelectValue placeholder="Select database" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="supabase">Supabase</SelectItem>
                            <SelectItem value="postgres">PostgreSQL</SelectItem>
                            <SelectItem value="mongo">MongoDB</SelectItem>
                            <SelectItem value="pinecone">Pinecone</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div>
                        <Label htmlFor="embedding-model">Embedding Model</Label>
                        <Select defaultValue="open-embed">
                          <SelectTrigger id="embedding-model">
                            <SelectValue placeholder="Select embedding model" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="open-embed">
                              OpenAI Embeddings
                            </SelectItem>
                            <SelectItem value="cohere">
                              Cohere Embeddings
                            </SelectItem>
                            <SelectItem value="sentence">
                              Sentence Transformers
                            </SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="text-lg font-medium">RAG Settings</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="chunk-size">Default Chunk Size</Label>
                        <Input
                          id="chunk-size"
                          type="number"
                          defaultValue="1000"
                        />
                      </div>
                      <div>
                        <Label htmlFor="chunk-overlap">Chunk Overlap</Label>
                        <Input
                          id="chunk-overlap"
                          type="number"
                          defaultValue="200"
                        />
                      </div>
                      <div>
                        <Label htmlFor="top-k">Top K Results</Label>
                        <Input id="top-k" type="number" defaultValue="5" />
                      </div>
                      <div>
                        <Label htmlFor="similarity-threshold">
                          Similarity Threshold
                        </Label>
                        <Input
                          id="similarity-threshold"
                          type="number"
                          defaultValue="0.75"
                          min="0"
                          max="1"
                          step="0.01"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <h3 className="text-lg font-medium">Advanced Settings</h3>
                    <div className="flex justify-between items-center">
                      <div>
                        <Label htmlFor="query-caching" className="text-base">
                          Enable Query Caching
                        </Label>
                        <p className="text-sm text-gray-500">
                          Store and reuse results for similar queries
                        </p>
                      </div>
                      <Switch id="query-caching" defaultChecked />
                    </div>
                    <div className="flex justify-between items-center">
                      <div>
                        <Label htmlFor="usage-tracking" className="text-base">
                          Detailed Usage Tracking
                        </Label>
                        <p className="text-sm text-gray-500">
                          Track token usage and query performance
                        </p>
                      </div>
                      <Switch id="usage-tracking" defaultChecked />
                    </div>
                    <div className="flex justify-between items-center">
                      <div>
                        <Label htmlFor="error-logging" className="text-base">
                          Enhanced Error Logging
                        </Label>
                        <p className="text-sm text-gray-500">
                          Detailed logs for debugging and optimization
                        </p>
                      </div>
                      <Switch id="error-logging" defaultChecked />
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="flex justify-end space-x-2">
                  <Button variant="outline">Reset to Defaults</Button>
                  <Button>Save Settings</Button>
                </CardFooter>
              </Card>
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </>
  );
}

export default Dashboard;
