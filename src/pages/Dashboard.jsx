import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Droplet,
  Leaf,
  Zap,
  Circle,
  Thermometer,
  Wind,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Calendar,
  RefreshCw,
  Settings,
  Bell,
  Shield,
  Tag,
  MapPin,
  Clock
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 60000);
    return () => clearInterval(timer);
  }, []);

  // Mock sensor data
  const sensorData = [
    {
      name: 'Moisture',
      value: 68,
      unit: '%',
      status: 'Optimal',
      icon: Droplet,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
      borderColor: 'border-l-blue-500'
    },
    {
      name: 'Nitrogen',
      value: 42,
      unit: 'ppm',
      status: 'Low',
      icon: Leaf,
      color: 'text-green-400',
      bgColor: 'bg-green-500/10',
      borderColor: 'border-l-green-500'
    },
    {
      name: 'Phosphorus',
      value: 38,
      unit: 'ppm',
      status: 'Good',
      icon: Zap,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10',
      borderColor: 'border-l-yellow-500'
    },
    {
      name: 'Potassium',
      value: 55,
      unit: 'ppm',
      status: 'Good',
      icon: Circle,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10',
      borderColor: 'border-l-purple-500'
    },
    {
      name: 'Temp',
      value: 28,
      unit: '°C',
      status: 'Normal',
      icon: Thermometer,
      color: 'text-red-400',
      bgColor: 'bg-red-500/10',
      borderColor: 'border-l-red-500'
    },
    {
      name: 'Humidity',
      value: 72,
      unit: '%',
      status: 'High',
      icon: Wind,
      color: 'text-cyan-400',
      bgColor: 'bg-cyan-500/10',
      borderColor: 'border-l-cyan-500'
    },
  ];

  // Soil moisture trend data
  const moistureTrendData = [
    { time: '6AM', value: 72 },
    { time: '9AM', value: 68 },
    { time: '12PM', value: 58 },
    { time: '3PM', value: 52 },
    { time: '6PM', value: 56 },
    { time: '9PM', value: 64 },
    { time: 'Now', value: 68 },
  ];

  // Crop health index data
  const cropHealthData = [
    { day: 'Mon', value: 86 },
    { day: 'Tue', value: 89 },
    { day: 'Wed', value: 84 },
    { day: 'Thu', value: 88 },
    { day: 'Fri', value: 87 },
    { day: 'Sat', value: 91 },
    { day: 'Sun', value: 93 },
  ];

  // Recent alerts
  const recentAlerts = [
    {
      icon: AlertTriangle,
      color: 'text-yellow-400',
      message: 'Soil moisture dropping below optimal level in Field 2',
      time: '2h ago'
    },
    {
      icon: CheckCircle,
      color: 'text-green-400',
      message: 'NPK levels optimal for tomato growth',
      time: '5h ago'
    },
    {
      icon: CheckCircle,
      color: 'text-green-400',
      message: 'Grade A certification received for cotton batch',
      time: '1 day ago'
    },
  ];

  // Recent disease scans
  const recentScans = [
    {
      crop: 'Tomato',
      status: 'Healthy',
      confidence: 98,
      time: 'Today',
      icon: Leaf,
      statusColor: 'text-green-400',
      bgColor: 'bg-green-500/10'
    },
    {
      crop: 'Cotton',
      status: 'Early Blight',
      confidence: 94,
      time: 'Yesterday',
      icon: Leaf,
      statusColor: 'text-yellow-400',
      bgColor: 'bg-yellow-500/10'
    },
    {
      crop: 'Wheat',
      status: 'Healthy',
      confidence: 96,
      time: '2 days ago',
      icon: Leaf,
      statusColor: 'text-green-400',
      bgColor: 'bg-green-500/10'
    },
  ];

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-1">Farm Dashboard</h1>
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <MapPin className="h-4 w-4" />
                  <span>Gujarat, India</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="h-4 w-4" />
                  <span>Last updated: {formatTime(currentTime)}</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Button variant="outline" size="sm" className="gap-2">
                <RefreshCw className="h-4 w-4" />
                Refresh
              </Button>
              <Button variant="outline" size="sm" className="gap-2">
                <Settings className="h-4 w-4" />
                Settings
              </Button>
              <Button variant="outline" size="sm" className="gap-2 relative">
                <Bell className="h-4 w-4" />
                Alerts
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-6 space-y-6">
        {/* Sensor Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          {sensorData.map((sensor) => (
            <Card key={sensor.name} className={`glass-card border-l-4 ${sensor.borderColor}`}>
              <CardContent className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <sensor.icon className={`h-5 w-5 ${sensor.color}`} />
                  <Badge variant="outline" className={`text-xs ${sensor.color}`}>
                    {sensor.status}
                  </Badge>
                </div>
                <div className="space-y-1">
                  <p className="text-2xl font-bold text-foreground">
                    {sensor.value}
                    <span className="text-sm text-muted-foreground ml-1">{sensor.unit}</span>
                  </p>
                  <p className="text-sm text-muted-foreground">{sensor.name}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Soil Moisture Trend */}
          <Card className="glass-card lg:col-span-2">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Droplet className="h-5 w-5 text-blue-400" />
                  <CardTitle>Soil Moisture Trend</CardTitle>
                </div>
                <select className="bg-secondary text-foreground text-sm rounded-md px-3 py-1 border border-border">
                  <option>Today</option>
                  <option>Week</option>
                  <option>Month</option>
                </select>
              </div>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={moistureTrendData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis
                    dataKey="time"
                    stroke="hsl(var(--muted-foreground))"
                    style={{ fontSize: '12px' }}
                  />
                  <YAxis
                    stroke="hsl(var(--muted-foreground))"
                    style={{ fontSize: '12px' }}
                    domain={[0, 80]}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'hsl(var(--card))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px'
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#3b82f6"
                    strokeWidth={3}
                    dot={{ fill: '#3b82f6', r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Recent Alerts */}
          <Card className="glass-card">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Bell className="h-5 w-5 text-yellow-400" />
                <CardTitle>Recent Alerts</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {recentAlerts.map((alert, index) => (
                <div key={index} className="flex gap-3 p-3 rounded-lg bg-secondary/50 border border-border/50">
                  <alert.icon className={`h-5 w-5 ${alert.color} flex-shrink-0 mt-0.5`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-foreground leading-snug">{alert.message}</p>
                    <p className="text-xs text-muted-foreground mt-1">{alert.time}</p>
                  </div>
                </div>
              ))}
              <Button variant="outline" className="w-full">
                View All Alerts
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Bottom Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Crop Health Index */}
          <Card className="glass-card lg:col-span-2">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-400" />
                  <CardTitle>Crop Health Index</CardTitle>
                </div>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  <span>Last 7 days</span>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={cropHealthData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis
                    dataKey="day"
                    stroke="hsl(var(--muted-foreground))"
                    style={{ fontSize: '12px' }}
                  />
                  <YAxis
                    stroke="hsl(var(--muted-foreground))"
                    style={{ fontSize: '12px' }}
                    domain={[70, 100]}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'hsl(var(--card))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px'
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#22c55e"
                    strokeWidth={3}
                    dot={{ fill: '#22c55e', r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Recent Disease Scans */}
          <Card className="glass-card">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Leaf className="h-5 w-5 text-green-400" />
                <CardTitle>Recent Disease Scans</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              {recentScans.map((scan, index) => (
                <div key={index} className={`flex items-center justify-between p-3 rounded-lg ${scan.bgColor} border border-border/50`}>
                  <div className="flex items-center gap-3">
                    <scan.icon className={`h-5 w-5 ${scan.statusColor}`} />
                    <div>
                      <p className="font-medium text-foreground">{scan.crop}</p>
                      <p className={`text-sm ${scan.statusColor}`}>{scan.status}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-foreground">{scan.confidence}%</p>
                    <p className="text-xs text-muted-foreground">{scan.time}</p>
                  </div>
                </div>
              ))}
              <Button variant="outline" className="w-full border-accent/50 text-accent hover:bg-accent/10">
                View All Scans
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Trust Score Section */}
        <Card className="glass-card border-2 border-accent/30 glow-accent">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-6">
                <div className="w-16 h-16 rounded-full bg-accent/20 flex items-center justify-center">
                  <Shield className="h-8 w-8 text-accent" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-foreground mb-1">Trust Score</h3>
                  <p className="text-sm text-muted-foreground">Combined AI + Sensor Verification</p>
                </div>
              </div>

              <div className="flex items-center gap-8">
                <div className="text-center">
                  <p className="text-5xl font-bold text-accent mb-1">92</p>
                  <p className="text-sm text-muted-foreground">Overall</p>
                </div>
                <div className="text-center">
                  <p className="text-5xl font-bold text-green-400 mb-1">A</p>
                  <p className="text-sm text-muted-foreground">Grade</p>
                </div>
                <div className="text-center">
                  <p className="text-5xl font-bold text-yellow-400 mb-1">1.4x</p>
                  <p className="text-sm text-muted-foreground">Price Boost</p>
                </div>
              </div>

              <Button className="bg-accent hover:bg-accent/90 text-accent-foreground gap-2 px-6 py-6 text-lg font-semibold">
                <Tag className="h-5 w-5" />
                Generate Trust Tag
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default Dashboard;
