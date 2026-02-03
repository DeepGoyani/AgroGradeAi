import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Leaf, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  Calendar, 
  DollarSign,
  Users,
  Activity,
  BarChart3,
  Camera,
  Sprout,
  Droplets,
  Sun,
  Wind
} from 'lucide-react';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalAnalyses: 156,
    healthyCrops: 124,
    diseasedCrops: 32,
    avgQuality: 78.5,
    recentAnalyses: [
      { id: 1, crop: 'Tomato', disease: 'Healthy', confidence: 92, quality: 85, date: '2024-02-03' },
      { id: 2, crop: 'Wheat', disease: 'Leaf Spot', confidence: 87, quality: 72, date: '2024-02-03' },
      { id: 3, crop: 'Cotton', disease: 'Healthy', confidence: 95, quality: 88, date: '2024-02-02' },
      { id: 4, crop: 'Rice', disease: 'Bacterial Blight', confidence: 91, quality: 65, date: '2024-02-02' },
      { id: 5, crop: 'Potato', disease: 'Healthy', confidence: 89, quality: 82, date: '2024-02-01' },
    ],
    cropDistribution: {
      'Tomato': 45,
      'Wheat': 32,
      'Cotton': 28,
      'Rice': 25,
      'Potato': 18,
      'Okra': 8
    },
    diseaseTrends: [
      { disease: 'Healthy', count: 124, trend: 'up' },
      { disease: 'Leaf Spot', count: 18, trend: 'down' },
      { disease: 'Bacterial Blight', count: 14, trend: 'stable' },
    ]
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (!token || !userData) {
      window.location.href = '/login';
      return;
    }
    
    setUser(JSON.parse(userData));
    setLoading(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const healthyPercentage = stats.totalAnalyses > 0 ? 
    Math.round((stats.healthyCrops / stats.totalAnalyses) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <Leaf className="h-8 w-8 text-green-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AgroGrade Dashboard</h1>
                <p className="text-sm text-gray-500">Welcome back, {user?.full_name || user?.username}</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-green-600">
                {user?.farm_name || 'Farmer'}
              </Badge>
              <Button variant="outline" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Analyses</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalAnalyses}</div>
              <p className="text-xs text-muted-foreground">+12% from last month</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Healthy Crops</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats.healthyCrops}</div>
              <p className="text-xs text-muted-foreground">{healthyPercentage}% healthy rate</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Diseased Crops</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{stats.diseasedCrops}</div>
              <p className="text-xs text-muted-foreground">Requires attention</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Quality</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.avgQuality}%</div>
              <p className="text-xs text-muted-foreground">+5% improvement</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Analyses */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Analyses</CardTitle>
              <CardDescription>Your latest crop disease detections</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {stats.recentAnalyses.map((analysis) => (
                  <div key={analysis.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className={`w-2 h-2 rounded-full ${
                        analysis.disease === 'Healthy' ? 'bg-green-500' : 'bg-red-500'
                      }`} />
                      <div>
                        <p className="font-medium">{analysis.crop}</p>
                        <p className="text-sm text-gray-500">{analysis.disease}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">{analysis.confidence}%</p>
                      <p className="text-xs text-gray-500">{analysis.date}</p>
                    </div>
                  </div>
                ))}
              </div>
              <Button variant="outline" className="w-full mt-4" onClick={() => window.location.href = '/ai-analysis'}>
                <Camera className="h-4 w-4 mr-2" />
                New Analysis
              </Button>
            </CardContent>
          </Card>

          {/* Crop Distribution */}
          <Card>
            <CardHeader>
              <CardTitle>Crop Distribution</CardTitle>
              <CardDescription>Your analyzed crops breakdown</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(stats.cropDistribution).map(([crop, count]) => (
                  <div key={crop} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>{crop}</span>
                      <span>{count}</span>
                    </div>
                    <Progress value={(count / stats.totalAnalyses) * 100} className="h-2" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Environmental Conditions */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Environmental Conditions</CardTitle>
            <CardDescription>Current farming conditions</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="flex items-center space-x-3">
                <Droplets className="h-8 w-8 text-blue-500" />
                <div>
                  <p className="text-sm text-gray-500">Moisture</p>
                  <p className="font-medium">65%</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Sun className="h-8 w-8 text-yellow-500" />
                <div>
                  <p className="text-sm text-gray-500">Temperature</p>
                  <p className="font-medium">28°C</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Wind className="h-8 w-8 text-gray-500" />
                <div>
                  <p className="text-sm text-gray-500">Humidity</p>
                  <p className="font-medium">72%</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Sprout className="h-8 w-8 text-green-500" />
                <div>
                  <p className="text-sm text-gray-500">NPK Levels</p>
                  <p className="font-medium">Balanced</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
