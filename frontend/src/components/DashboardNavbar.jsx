import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
  LayoutDashboard,
  FileText,
  Users,
  Settings,
  HelpCircle,
  LogOut,
  Bot,
  Database,
  Key,
  BarChart2,
  ChevronRight,
  ChevronDown,
  Search,
  Code,
  Globe,
  Cpu,
  Layers,
} from "lucide-react";

function DashboardNav({ closeMenu }) {
  const [expandedMenu, setExpandedMenu] = useState("");

  const toggleMenu = (menu) => {
    if (expandedMenu === menu) {
      setExpandedMenu("");
    } else {
      setExpandedMenu(menu);
    }
  };

  return (
    <div
      className={`flex flex-col bg-gray-900 text-white h-full z-60 fixed md:static  transition-transform duration-300 ease-in-out ${
        closeMenu ? "w-64 translate-x-0" : "-translate-x-full w-64"
      }`}
    >
      <div className="flex items-center justify-between h-16 border-b border-gray-800 px-4">
        <div className="flex items-center">
          <Cpu className="h-6 w-6 text-blue-400 mr-2" />
          <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            RAG AI Hub
          </span>
        </div>
        <Badge
          variant="outline"
          className="bg-blue-900/30 text-blue-300 border-blue-500 text-xs"
        >
          BETA
        </Badge>
      </div>
      <div className="flex items-center p-4 border-b border-gray-800 bg-gray-800/50">
        <Avatar className="h-8 w-8 mr-2">
          <AvatarImage src="/api/placeholder/32/32" alt="User" />
          <AvatarFallback className="bg-gray-700">U</AvatarFallback>
        </Avatar>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium truncate">Alex Johnson</p>
          <p className="text-xs text-gray-400 truncate">Pro Account</p>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto py-4">
        <div className="px-3 mb-2">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider ml-2 mb-1">
            MAIN
          </p>
        </div>
        <ul className="space-y-1 px-2">
          <li>
            <Button
              variant="ghost"
              className="w-full justify-start text-gray-300 hover:text-white hover:bg-gray-800"
            >
              <LayoutDashboard className="mr-2 h-4 w-4" />
              Dashboard
            </Button>
          </li>

          <li>
            <Button
              variant="ghost"
              className="w-full justify-between text-gray-300 hover:text-white hover:bg-gray-800"
              onClick={() => toggleMenu("agents")}
            >
              <div className="flex items-center">
                <Bot className="mr-2 h-4 w-4" />
                <span>AI Agents</span>
              </div>
              {expandedMenu === "agents" ? (
                <ChevronDown className="h-4 w-4" />
              ) : (
                <ChevronRight className="h-4 w-4" />
              )}
            </Button>
            {expandedMenu === "agents" && (
              <div className="pl-6 mt-1 space-y-1">
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full justify-start text-sm text-gray-400 hover:text-white hover:bg-gray-800"
                >
                  <Layers className="mr-2 h-3 w-3" /> All Agents
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full justify-start text-sm text-gray-400 hover:text-white hover:bg-gray-800"
                >
                  <Code className="mr-2 h-3 w-3" /> Create Agent
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full justify-start text-sm text-gray-400 hover:text-white hover:bg-gray-800"
                >
                  <Search className="mr-2 h-3 w-3" /> RAG Pipeline
                </Button>
              </div>
            )}
          </li>

          <li>
            <Button
              variant="ghost"
              className="w-full justify-between text-gray-300 hover:text-white hover:bg-gray-800"
              onClick={() => toggleMenu("integrations")}
            >
              <div className="flex items-center">
                <Globe className="mr-2 h-4 w-4" />
                <span>Integrations</span>
              </div>
              {expandedMenu === "integrations" ? (
                <ChevronDown className="h-4 w-4" />
              ) : (
                <ChevronRight className="h-4 w-4" />
              )}
            </Button>
            {expandedMenu === "integrations" && (
              <div className="pl-6 mt-1 space-y-1">
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full justify-start text-sm text-gray-400 hover:text-white hover:bg-gray-800"
                >
                  <Key className="mr-2 h-3 w-3" /> API Keys
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full justify-start text-sm text-gray-400 hover:text-white hover:bg-gray-800"
                >
                  <Database className="mr-2 h-3 w-3" /> Databases
                </Button>
              </div>
            )}
          </li>

          <li>
            <Button
              variant="ghost"
              className="w-full justify-start text-gray-300 hover:text-white hover:bg-gray-800"
            >
              <FileText className="mr-2 h-4 w-4" />
              Documents
            </Button>
          </li>

          <li>
            <Button
              variant="ghost"
              className="w-full justify-start text-gray-300 hover:text-white hover:bg-gray-800"
            >
              <BarChart2 className="mr-2 h-4 w-4" />
              Analytics
              <Badge className="ml-auto bg-blue-600 text-xs">New</Badge>
            </Button>
          </li>
        </ul>

        <div className="px-3 mt-6 mb-2">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider ml-2 mb-1">
            ADMIN
          </p>
        </div>
        <ul className="space-y-1 px-2">
          <li>
            <Button
              variant="ghost"
              className="w-full justify-start text-gray-300 hover:text-white hover:bg-gray-800"
            >
              <Users className="mr-2 h-4 w-4" />
              Users & Teams
            </Button>
          </li>
          <li>
            <Button
              variant="ghost"
              className="w-full justify-start text-gray-300 hover:text-white hover:bg-gray-800"
            >
              <Settings className="mr-2 h-4 w-4" />
              Settings
            </Button>
          </li>
        </ul>
      </nav>

      <div className="p-4 border-t border-gray-800 space-y-2">
        <Button
          variant="ghost"
          className="w-full justify-start text-gray-300 hover:text-white hover:bg-gray-800"
        >
          <HelpCircle className="mr-2 h-4 w-4" />
          Help & Support
        </Button>
        <Button
          variant="ghost"
          className="w-full justify-start text-red-400 hover:text-red-300 hover:bg-red-500/10"
        >
          <LogOut className="mr-2 h-4 w-4" />
          Log out
        </Button>
      </div>

      <div className="p-4 m-2 bg-gradient-to-br from-blue-900/40 to-purple-900/40 rounded-lg border border-blue-800/50">
        <p className="text-sm font-medium text-blue-300 mb-1">Upgrade to Pro</p>
        <p className="text-xs text-gray-400 mb-2">
          Get unlimited agents and advanced RAG features
        </p>
        <Button size="sm" className="w-full bg-blue-600 hover:bg-blue-700">
          Upgrade Now
        </Button>
      </div>
    </div>
  );
}

export default DashboardNav;
