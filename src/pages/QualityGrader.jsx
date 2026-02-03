import React, { useState, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Star, 
  TrendingUp, 
  Award, 
  CheckCircle, 
  Upload,
  Loader2,
  Package,
  RefreshCw,
  Shield,
  Palette,
  Ruler,
  Sparkles
} from 'lucide-react';

const QualityGrader = () => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [isGrading, setIsGrading] = useState(false);
  const [gradeResult, setGradeResult] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const mockGrades = [
    {
      grade: "A",
      score: 92,
      label: "Premium Quality",
      color: "success",
      details: {
        colorUniformity: 95,
        sizeDistribution: 88,
        surfaceQuality: 93,
        freshness: 92,
      },
      trustScore: 94,
      priceMultiplier: 1.4,
    },
    {
      grade: "B",
      score: 75,
      label: "Standard Quality",
      color: "warning",
      details: {
        colorUniformity: 78,
        sizeDistribution: 72,
        surfaceQuality: 76,
        freshness: 74,
      },
      trustScore: 78,
      priceMultiplier: 1.15,
    },
    {
      grade: "C",
      score: 58,
      label: "Economy Quality",
      color: "destructive",
      details: {
        colorUniformity: 55,
        sizeDistribution: 60,
        surfaceQuality: 58,
        freshness: 59,
      },
      trustScore: 62,
      priceMultiplier: 0.9,
    },
  ];

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleFile = (file) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => setUploadedImage(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const simulateGrading = async () => {
    setIsGrading(true);
    await new Promise(resolve => setTimeout(resolve, 2000));
    const result = mockGrades[Math.floor(Math.random() * mockGrades.length)];
    setGradeResult(result);
    setIsGrading(false);
  };

  const handleReset = () => {
    setUploadedImage(null);
    setGradeResult(null);
    setIsGrading(false);
  };

  const getGradeClass = (grade) => {
    switch (grade) {
      case "A":
        return "bg-green-100 text-green-800 border-green-500";
      case "B":
        return "bg-yellow-100 text-yellow-800 border-yellow-500";
      case "C":
        return "bg-red-100 text-red-800 border-red-500";
      default:
        return "";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Quality Grader</h1>
          <p className="text-xl text-gray-600">Automated quality assessment for agricultural products</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Package className="h-5 w-5 mr-2" />
                Upload Product Image
              </CardTitle>
              <CardDescription>
                Upload a clear photo of your harvest for quality assessment
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!uploadedImage ? (
                <div
                  className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all ${
                    dragActive
                      ? "border-yellow-500 bg-yellow-50"
                      : "border-gray-300 hover:border-yellow-400"
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                  <p className="text-gray-600 font-medium mb-2">
                    Drag & drop your product image here
                  </p>
                  <p className="text-sm text-gray-500">
                    or click to browse • PNG, JPG up to 10MB
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="relative rounded-xl overflow-hidden aspect-video">
                    <img
                      src={uploadedImage}
                      alt="Uploaded product"
                      className="w-full h-full object-cover"
                    />
                    {isGrading && (
                      <div className="absolute inset-0 bg-white/50 flex items-center justify-center">
                        <div className="text-center">
                          <Loader2 className="w-8 h-8 animate-spin text-yellow-600 mx-auto mb-2" />
                          <p className="text-yellow-600 font-medium">Analyzing Quality...</p>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="flex gap-3">
                    <Button
                      className="flex-1 bg-yellow-600 hover:bg-yellow-700"
                      onClick={simulateGrading}
                      disabled={isGrading}
                    >
                      {isGrading ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin mr-2" />
                          Grading...
                        </>
                      ) : (
                        <>
                          <Award className="w-4 h-4 mr-2" />
                          Grade Quality
                        </>
                      )}
                    </Button>
                    <Button variant="outline" onClick={handleReset}>
                      <RefreshCw className="w-4 h-4 mr-2" />
                      Reset
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Results Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Star className="h-5 w-5 mr-2" />
                Grading Results
              </CardTitle>
              <CardDescription>
                AI-powered quality assessment results
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!gradeResult ? (
                <div className="text-center py-12">
                  <Package className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">Upload an image to see grading results</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Grade Badge */}
                  <div className="text-center py-6">
                    <div className={`w-32 h-32 mx-auto rounded-full ${getGradeClass(gradeResult.grade)} flex items-center justify-center shadow-lg border-4`}>
                      <div>
                        <div className="text-5xl font-bold">
                          {gradeResult.grade}
                        </div>
                        <div className="text-sm opacity-80">Grade</div>
                      </div>
                    </div>
                    <h3 className="text-2xl font-semibold mt-4">
                      {gradeResult.label}
                    </h3>
                    <p className="text-gray-600">Quality Score: {gradeResult.score}%</p>
                  </div>

                  {/* Quality Metrics */}
                  <div>
                    <h4 className="font-semibold mb-3">Quality Metrics:</h4>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Color Uniformity</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-green-500 h-2 rounded-full" 
                              style={{ width: `${gradeResult.details.colorUniformity}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium">{gradeResult.details.colorUniformity}%</span>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Size Distribution</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full" 
                              style={{ width: `${gradeResult.details.sizeDistribution}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium">{gradeResult.details.sizeDistribution}%</span>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Surface Quality</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-purple-500 h-2 rounded-full" 
                              style={{ width: `${gradeResult.details.surfaceQuality}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium">{gradeResult.details.surfaceQuality}%</span>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Freshness</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-yellow-500 h-2 rounded-full" 
                              style={{ width: `${gradeResult.details.freshness}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium">{gradeResult.details.freshness}%</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Trust Score and Price */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <Shield className="w-8 h-8 text-green-600 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-green-600">{gradeResult.trustScore}%</div>
                      <div className="text-sm text-gray-600">Trust Score</div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <TrendingUp className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-blue-600">{gradeResult.priceMultiplier}x</div>
                      <div className="text-sm text-gray-600">Price Multiplier</div>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Features */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Quality Factors</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader>
                <Palette className="h-8 w-8 text-green-600" />
                <CardTitle>Color</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">Vibrant, uniform color indicates freshness</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Ruler className="h-8 w-8 text-blue-600" />
                <CardTitle>Size</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">Consistent sizing for market standards</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Sparkles className="h-8 w-8 text-purple-600" />
                <CardTitle>Texture</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">Firm texture indicates good quality</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CheckCircle className="h-8 w-8 text-yellow-500" />
                <CardTitle>Appearance</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">No blemishes or damage</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QualityGrader;
