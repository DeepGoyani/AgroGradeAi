import { motion } from "framer-motion";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import { Button } from "@/components/ui/button";
import {
  Droplets,
  Leaf,
  Thermometer,
  Zap,
  AlertTriangle,
  TrendingUp,
  Award,
  Shield,
  Bell,
  Settings,
  Calendar,
  MapPin,
  RefreshCw,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";

// Mock sensor data
const sensorData = {
  moisture: 68,
  nitrogen: 42,
  phosphorus: 38,
  potassium: 55,
  temperature: 28,
  humidity: 72,
};

const moistureHistory = [
  { time: "6AM", value: 72 },
  { time: "9AM", value: 68 },
  { time: "12PM", value: 55 },
  { time: "3PM", value: 48 },
  { time: "6PM", value: 52 },
  { time: "9PM", value: 65 },
  { time: "Now", value: 68 },
];

const cropHealth = [
  { day: "Mon", health: 85 },
  { day: "Tue", health: 88 },
  { day: "Wed", health: 82 },
  { day: "Thu", health: 90 },
  { day: "Fri", health: 87 },
  { day: "Sat", health: 92 },
  { day: "Sun", health: 94 },
];

const recentScans = [
  { id: 1, crop: "Tomato", result: "Healthy", confidence: 98, date: "Today" },
  { id: 2, crop: "Cotton", result: "Early Blight", confidence: 94, date: "Yesterday" },
  { id: 3, crop: "Wheat", result: "Healthy", confidence: 96, date: "2 days ago" },
];

const alerts = [
  { id: 1, type: "warning", message: "Soil moisture dropping below optimal level in Field 2", time: "2h ago" },
  { id: 2, type: "info", message: "NPK levels optimal for tomato growth", time: "5h ago" },
  { id: 3, type: "success", message: "Grade A certification received for cotton batch", time: "1 day ago" },
];

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="pt-24 pb-16">
        <div className="container mx-auto px-4">
          {/* Dashboard Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col md:flex-row md:items-center md:justify-between mb-8"
          >
            <div>
              <h1 className="font-display text-3xl md:text-4xl font-bold mb-2">
                Farm Dashboard
              </h1>
              <p className="text-muted-foreground flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                Gujarat, India • Last updated: 2 min ago
              </p>
            </div>
            <div className="flex gap-3 mt-4 md:mt-0">
              <Button variant="outline" size="sm">
                <RefreshCw className="w-4 h-4" />
                Refresh
              </Button>
              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4" />
                Settings
              </Button>
              <Button variant="hero" size="sm">
                <Bell className="w-4 h-4" />
                Alerts
              </Button>
            </div>
          </motion.div>

          {/* Stats Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-8">
            {[
              { label: "Moisture", value: sensorData.moisture, unit: "%", icon: Droplets, color: "moisture", status: "Optimal" },
              { label: "Nitrogen", value: sensorData.nitrogen, unit: "ppm", icon: Leaf, color: "nitrogen", status: "Low" },
              { label: "Phosphorus", value: sensorData.phosphorus, unit: "ppm", icon: Zap, color: "phosphorus", status: "Good" },
              { label: "Potassium", value: sensorData.potassium, unit: "ppm", icon: Shield, color: "potassium", status: "Good" },
              { label: "Temp", value: sensorData.temperature, unit: "°C", icon: Thermometer, color: "destructive", status: "Normal" },
              { label: "Humidity", value: sensorData.humidity, unit: "%", icon: Droplets, color: "accent", status: "High" },
            ].map((item, i) => (
              <motion.div
                key={item.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className={`glass-card p-4 rounded-xl sensor-${item.label.toLowerCase()}`}
              >
                <div className="flex items-center justify-between mb-2">
                  <item.icon className={`w-5 h-5 text-${item.color}`} />
                  <span className={`text-xs px-2 py-0.5 rounded-full bg-${item.color}/20 text-${item.color}`}>
                    {item.status}
                  </span>
                </div>
                <div className="text-2xl font-bold">
                  {item.value}
                  <span className="text-sm font-normal text-muted-foreground">{item.unit}</span>
                </div>
                <div className="text-sm text-muted-foreground">{item.label}</div>
              </motion.div>
            ))}
          </div>

          <div className="grid lg:grid-cols-3 gap-6 mb-8">
            {/* Moisture Chart */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="lg:col-span-2 glass-card p-6 rounded-2xl"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-display text-xl font-semibold flex items-center gap-2">
                  <Droplets className="w-5 h-5 text-moisture" />
                  Soil Moisture Trend
                </h2>
                <select className="text-sm bg-secondary border border-border rounded-lg px-3 py-1.5">
                  <option>Today</option>
                  <option>This Week</option>
                  <option>This Month</option>
                </select>
              </div>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={moistureHistory}>
                    <defs>
                      <linearGradient id="moistureGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="hsl(200, 70%, 50%)" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="hsl(200, 70%, 50%)" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis dataKey="time" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                    <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "hsl(var(--card))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: "8px",
                      }}
                    />
                    <Area
                      type="monotone"
                      dataKey="value"
                      stroke="hsl(200, 70%, 50%)"
                      strokeWidth={2}
                      fill="url(#moistureGradient)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </motion.div>

            {/* Alerts Panel */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="glass-card p-6 rounded-2xl"
            >
              <h2 className="font-display text-xl font-semibold flex items-center gap-2 mb-4">
                <Bell className="w-5 h-5 text-warning" />
                Recent Alerts
              </h2>
              <div className="space-y-3">
                {alerts.map((alert) => (
                  <div
                    key={alert.id}
                    className={`p-3 rounded-lg border ${
                      alert.type === "warning"
                        ? "border-warning/30 bg-warning/10"
                        : alert.type === "success"
                        ? "border-success/30 bg-success/10"
                        : "border-accent/30 bg-accent/10"
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      {alert.type === "warning" ? (
                        <AlertTriangle className="w-4 h-4 text-warning mt-0.5" />
                      ) : alert.type === "success" ? (
                        <Award className="w-4 h-4 text-success mt-0.5" />
                      ) : (
                        <Leaf className="w-4 h-4 text-accent mt-0.5" />
                      )}
                      <div className="flex-1">
                        <p className="text-sm">{alert.message}</p>
                        <p className="text-xs text-muted-foreground mt-1">{alert.time}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <Button variant="ghost" className="w-full mt-4" size="sm">
                View All Alerts
              </Button>
            </motion.div>
          </div>

          <div className="grid lg:grid-cols-2 gap-6">
            {/* Crop Health Chart */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="glass-card p-6 rounded-2xl"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-display text-xl font-semibold flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-success" />
                  Crop Health Index
                </h2>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="w-4 h-4" />
                  Last 7 days
                </div>
              </div>
              <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={cropHealth}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis dataKey="day" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                    <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} domain={[70, 100]} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "hsl(var(--card))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: "8px",
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="health"
                      stroke="hsl(var(--success))"
                      strokeWidth={3}
                      dot={{ fill: "hsl(var(--success))", strokeWidth: 2 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </motion.div>

            {/* Recent Scans */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="glass-card p-6 rounded-2xl"
            >
              <h2 className="font-display text-xl font-semibold flex items-center gap-2 mb-4">
                <Leaf className="w-5 h-5 text-accent" />
                Recent Disease Scans
              </h2>
              <div className="space-y-3">
                {recentScans.map((scan) => (
                  <div
                    key={scan.id}
                    className="flex items-center gap-4 p-3 rounded-lg bg-secondary/30 border border-border/50"
                  >
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                      scan.result === "Healthy" ? "bg-success/20" : "bg-warning/20"
                    }`}>
                      <Leaf className={`w-5 h-5 ${
                        scan.result === "Healthy" ? "text-success" : "text-warning"
                      }`} />
                    </div>
                    <div className="flex-1">
                      <div className="font-medium">{scan.crop}</div>
                      <div className="text-sm text-muted-foreground">{scan.result}</div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-accent">{scan.confidence}%</div>
                      <div className="text-xs text-muted-foreground">{scan.date}</div>
                    </div>
                  </div>
                ))}
              </div>
              <Button variant="outline" className="w-full mt-4" size="sm">
                View All Scans
              </Button>
            </motion.div>
          </div>

          {/* Trust Score Card */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="mt-8 glass-card p-8 rounded-2xl bg-gradient-to-br from-accent/10 via-card to-success/10"
          >
            <div className="flex flex-col md:flex-row md:items-center gap-6">
              <div className="flex items-center gap-4">
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-accent to-success flex items-center justify-center shadow-lg">
                  <Shield className="w-10 h-10 text-primary-foreground" />
                </div>
                <div>
                  <h3 className="font-display text-2xl font-bold">Trust Score</h3>
                  <p className="text-muted-foreground">Combined AI + Sensor Verification</p>
                </div>
              </div>
              <div className="flex-1 flex items-center gap-8">
                <div className="text-center">
                  <div className="text-4xl font-bold text-accent">92</div>
                  <div className="text-sm text-muted-foreground">Overall</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-success">A</div>
                  <div className="text-sm text-muted-foreground">Grade</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-bold text-warning">1.4x</div>
                  <div className="text-sm text-muted-foreground">Price Boost</div>
                </div>
              </div>
              <Button variant="trust" size="lg">
                <Award className="w-5 h-5" />
                Generate Trust Tag
              </Button>
            </div>
          </motion.div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Dashboard;
