import React, { useState, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Camera,
  AlertTriangle,
  CheckCircle,
  Upload,
  Loader2,
  Leaf,
  TrendingUp,
  Shield,
  RefreshCw
} from 'lucide-react';

const DiseaseScanner = () => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null); // Add missing error state

  const mockDiseases = [
    {
      name: "Early Blight",
      confidence: 94.7,
      severity: "Moderate",
      crop: "Tomato",
      description: "Fungal infection caused by Alternaria solani. Brown spots with concentric rings on leaves.",
      remedies: [
        { type: "Organic", name: "Neem Oil Spray", instructions: "Mix 5ml neem oil in 1L water. Spray every 7 days." },
        { type: "Organic", name: "Copper Fungicide", instructions: "Apply Bordeaux mixture (1%) on affected areas." },
        { type: "Prevention", name: "Crop Rotation", instructions: "Rotate with non-solanaceous crops for 2-3 years." },
      ],
    },
    {
      name: "Healthy",
      confidence: 98.2,
      severity: "None",
      crop: "General",
      description: "No disease detected. Your crop appears to be healthy with good leaf coloration and structure.",
      remedies: [
        { type: "Prevention", name: "Regular Monitoring", instructions: "Continue weekly inspections of your crops." },
        { type: "Nutrition", name: "Balanced Fertilizer", instructions: "Apply NPK fertilizer as per soil test recommendations." },
      ],
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

  const handleScan = async () => {
    if (!uploadedImage) return;

    setIsScanning(true);
    setError(null);

    try {
      // 1. Convert data URL to Blob
      const response = await fetch(uploadedImage);
      const blob = await response.blob();
      const file = new File([blob], "leaf_image.jpg", { type: "image/jpeg" });

      // 2. Prepare FormData
      const formData = new FormData();
      formData.append('image', file);
      formData.append('save_to_db', 'true');

      // 3. Call AI API
      const apiResponse = await fetch('http://localhost:8000/api/ai/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!apiResponse.ok) {
        throw new Error('Analysis failed');
      }

      const data = await apiResponse.json();
      const diseaseResult = data.disease_diagnosis;

      // 4. Map API response to UI State
      setScanResult({
        name: diseaseResult.disease.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        confidence: (diseaseResult.confidence * 100).toFixed(1),
        severity: diseaseResult.severity_percent > 0
          ? `${diseaseResult.severity_percent}% Severity`
          : "Healthy",
        description: diseaseResult.disease === 'healthy'
          ? "No disease detected. Plant appears healthy."
          : `Detected ${diseaseResult.disease} with ${diseaseResult.confidence * 100}% confidence.`,
        remedies: [
          ...diseaseResult.remedies.organic.map(r => ({ type: "Organic", name: "Solution", instructions: r })),
          ...diseaseResult.remedies.chemical.map(r => ({ type: "Chemical", name: "Treatment", instructions: r })),
          ...diseaseResult.remedies.prevention.map(r => ({ type: "Prevention", name: "Tip", instructions: r }))
        ].slice(0, 4),
        image_features: diseaseResult.image_features // Pass detailed metrics
      });

    } catch (err) {
      console.error(err);
      setError("Failed to analyze image. Please try again.");
    } finally {
      setIsScanning(false);
    }
  };

  const handleReset = () => {
    setUploadedImage(null);
    setScanResult(null);
    setIsScanning(false);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Disease Scanner</h1>
          <p className="text-xl text-gray-600">Advanced AI-powered crop disease detection</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Camera className="h-5 w-5 mr-2" />
                Upload Leaf Image
              </CardTitle>
              <CardDescription>
                Take a clear photo of the affected leaf for analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!uploadedImage ? (
                <div
                  className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all ${dragActive
                    ? "border-green-500 bg-green-50"
                    : "border-gray-300 hover:border-green-400"
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
                    Drag & drop your leaf image here
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
                      alt="Uploaded leaf"
                      className="w-full h-full object-cover"
                    />
                    {isScanning && (
                      <div className="absolute inset-0 bg-white/50 flex items-center justify-center">
                        <div className="text-center">
                          <Loader2 className="w-8 h-8 animate-spin text-green-600 mx-auto mb-2" />
                          <p className="text-green-600 font-medium">Analyzing with AI...</p>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="flex gap-3">
                    <Button
                      className="flex-1 bg-green-600 hover:bg-green-700"
                      onClick={handleScan}
                      disabled={isScanning}
                    >
                      {isScanning ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin mr-2" />
                          Scanning...
                        </>
                      ) : (
                        <>
                          <Shield className="w-4 h-4 mr-2" />
                          Scan Now
                        </>
                      )}
                    </Button>
                    <Button variant="outline" onClick={handleReset}>
                      <RefreshCw className="w-4 h-4 mr-2" />
                      Reset
                    </Button>
                  </div>
                  {error && <p className="text-red-500 text-sm text-center">{error}</p>}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Results Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Leaf className="h-5 w-5 mr-2" />
                Analysis Results
              </CardTitle>
              <CardDescription>
                AI-powered disease detection results
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!scanResult ? (
                <div className="text-center py-12">
                  <Camera className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">Upload an image to see results</p>
                </div>
              ) : (
                <div className="space-y-6">
                  <div
                    className={`p-4 rounded-xl border ${scanResult.name === "Healthy"
                      ? "border-green-500 bg-green-50"
                      : "border-red-500 bg-red-50"
                      }`}
                  >
                    <div className="flex items-start gap-4">
                      <div
                        className={`w-12 h-12 rounded-xl flex items-center justify-center ${scanResult.name === "Healthy" ? "bg-green-100" : "bg-red-100"
                          }`}
                      >
                        {scanResult.name === "Healthy" ? (
                          <CheckCircle className="w-6 h-6 text-green-600" />
                        ) : (
                          <AlertTriangle className="w-6 h-6 text-red-600" />
                        )}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold mb-1">{scanResult.name}</h3>
                        <p className="text-gray-600 mb-2">{scanResult.description}</p>
                        <div className="flex items-center gap-4 text-sm">
                          <Badge variant={scanResult.name === "Healthy" ? "default" : "destructive"}>
                            {scanResult.severity}
                          </Badge>
                          <span className="text-gray-500">Confidence: {scanResult.confidence}%</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Detailed Analysis Metrics (New Section) */}
                  {scanResult.image_features && (
                    <div className="p-4 bg-gray-50 rounded-xl border border-gray-200">
                      <h4 className="font-semibold mb-3 flex items-center">
                        <div className="w-2 h-2 rounded-full bg-blue-500 mr-2"></div>
                        Detailed Analysis Metrics
                      </h4>
                      <div className="space-y-3">
                        {/* Green Coverage */}
                        <div>
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-600">Green Leaf Coverage</span>
                            <span className="font-medium">{scanResult.image_features.green_coverage}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-1.5">
                            <div className="bg-green-500 h-1.5 rounded-full" style={{ width: `${Math.min(100, scanResult.image_features.green_coverage)}%` }}></div>
                          </div>
                        </div>

                        {/* Disease Indicators */}
                        <div>
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-600">Disease Symptoms Detected</span>
                            <span className="font-medium">{scanResult.image_features.disease_indicators}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-1.5">
                            <div className="bg-red-500 h-1.5 rounded-full" style={{ width: `${Math.min(100, scanResult.image_features.disease_indicators * 3)}%` }}></div>
                          </div>
                        </div>

                        {/* Lesion Count */}
                        <div className="flex justify-between items-center text-sm pt-1">
                          <span className="text-gray-600">Distinct Lesions / Spots</span>
                          <span className="font-medium bg-white px-2 py-0.5 rounded border">{scanResult.image_features.lesion_count} detected</span>
                        </div>

                        {/* EXTREME MODE: Texture Analysis */}
                        {scanResult.image_features.texture_complexity && (
                          <div className="pt-2 border-t border-gray-100">
                            <div className="flex justify-between text-sm mb-1">
                              <span className="text-gray-600">Surface Texture Complexity</span>
                              <span className="font-medium text-purple-700">{scanResult.image_features.texture_complexity}</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-1.5">
                              {/* Normalize roughly 0-1000 variance to 0-100% */}
                              <div className="bg-purple-500 h-1.5 rounded-full" style={{ width: `${Math.min(100, scanResult.image_features.texture_complexity / 2)}%` }}></div>
                            </div>
                            <p className="text-[10px] text-gray-400 mt-1 text-right">High variance = complex disease patterns</p>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  <div>
                    <h4 className="font-semibold mb-3">Recommended Actions:</h4>
                    <div className="space-y-2">
                      {scanResult.remedies.length > 0 ? scanResult.remedies.map((remedy, index) => (
                        <div key={index} className="p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center gap-2 mb-1">
                            <Badge variant="outline">{remedy.type}</Badge>
                            <span className="font-medium">{remedy.name}</span>
                          </div>
                          <p className="text-sm text-gray-600">{remedy.instructions}</p>
                        </div>
                      )) : (
                        <div className="p-3 bg-green-50 text-green-700 rounded-lg text-sm">
                          No actions needed. Plant is healthy!
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Features */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CheckCircle className="h-8 w-8 text-green-600" />
                <CardTitle>95% Accuracy</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Advanced AI models trained on thousands of crop images
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <TrendingUp className="h-8 w-8 text-blue-600" />
                <CardTitle>Real-time Analysis</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Get instant results with detailed disease information
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Leaf className="h-8 w-8 text-green-600" />
                <CardTitle>Multiple Crops</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Supports detection for various crop types
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DiseaseScanner;
