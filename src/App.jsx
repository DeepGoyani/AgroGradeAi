import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import DiseaseScanner from "./pages/DiseaseScanner";
import QualityGrader from "./pages/QualityGrader";
import Dashboard from "./pages/Dashboard";
import Marketplace from "./pages/Marketplace";
import NotFound from "./pages/NotFound";
import AuthPage from "./components/AuthPage";
import ProtectedRoute from "./components/ProtectedRoute";
import AIAnalysisInterface from "./components/AIAnalysisInterface";
import Navigation from "./components/Navigation";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Navigation />
        <Routes>
          <Route path="/login" element={<AuthPage />} />
          <Route path="/" element={<Index />} />
          <Route path="/scanner" element={<DiseaseScanner />} />
          <Route path="/grader" element={<QualityGrader />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/marketplace" element={<Marketplace />} />
          <Route path="/ai-analysis" element={<AIAnalysisInterface />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
