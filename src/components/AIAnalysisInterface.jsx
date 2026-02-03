import React, { useState, useCallback } from 'react';
import { Upload, Camera, AlertCircle, CheckCircle, Loader2, Leaf, Shield, TrendingUp } from 'lucide-react';

const AIAnalysisInterface = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleImageSelect = useCallback((event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
        setResults(null);
        setError(null);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const analyzeImage = useCallback(async () => {
    if (!selectedImage) return;

    setAnalyzing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedImage);
      formData.append('sensor_data', JSON.stringify({
        moisture: 65.5,
        temperature: 28.4,
        humidity: 72.3,
        npk: { n: 120, p: 45, k: 80 }
      }));
      formData.append('farmer_id', 'frontend_user_001');
      formData.append('save_to_db', 'true');

      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/ai/analyze', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setAnalyzing(false);
    }
  }, [selectedImage]);

  const getGradeColor = (grade) => {
    switch (grade) {
      case 'A': return 'text-green-500 bg-green-500/10 border-green-500/20';
      case 'B': return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20';
      case 'C': return 'text-red-500 bg-red-500/10 border-red-500/20';
      default: return 'text-gray-500 bg-gray-500/10 border-gray-500/20';
    }
  };

  const getTrustColor = (score) => {
    if (score >= 80) return 'text-green-500';
    if (score >= 60) return 'text-yellow-500';
    return 'text-red-500';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Leaf className="w-8 h-8 text-primary" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              AgroGrade AI Analysis
            </h1>
          </div>
          <p className="text-muted-foreground text-lg">
            Upload a crop leaf image for instant AI-powered disease detection and quality grading
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="space-y-6">
            <div className="glass-card p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Camera className="w-5 h-5" />
                Upload Image
              </h2>
              
              <div className="space-y-4">
                {/* Image Upload Area */}
                <div 
                  className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
                  onClick={() => document.getElementById('image-upload').click()}
                >
                  {preview ? (
                    <div className="space-y-4">
                      <img 
                        src={preview} 
                        alt="Preview" 
                        className="max-h-64 mx-auto rounded-lg shadow-lg"
                      />
                      <p className="text-sm text-muted-foreground">Click to change image</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <Upload className="w-12 h-12 mx-auto text-muted-foreground" />
                      <div>
                        <p className="text-lg font-medium">Click to upload image</p>
                        <p className="text-sm text-muted-foreground">or drag and drop</p>
                        <p className="text-xs text-muted-foreground mt-2">
                          PNG, JPG, WEBP up to 10MB
                        </p>
                      </div>
                    </div>
                  )}
                  <input
                    id="image-upload"
                    type="file"
                    accept="image/*"
                    onChange={handleImageSelect}
                    className="hidden"
                  />
                </div>

                {/* Analyze Button */}
                <button
                  onClick={analyzeImage}
                  disabled={!selectedImage || analyzing}
                  className="w-full py-3 px-4 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {analyzing ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Leaf className="w-4 h-4" />
                      Analyze with AI
                    </>
                  )}
                </button>

                {/* Error Display */}
                {error && (
                  <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg flex items-center gap-3">
                    <AlertCircle className="w-5 h-5 text-destructive" />
                    <p className="text-destructive">{error}</p>
                  </div>
                )}
              </div>
            </div>

            {/* Sensor Data Display */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Simulated Sensor Data
              </h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="p-3 bg-muted/30 rounded-lg">
                  <p className="text-muted-foreground">Moisture</p>
                  <p className="font-semibold">65.5%</p>
                </div>
                <div className="p-3 bg-muted/30 rounded-lg">
                  <p className="text-muted-foreground">Temperature</p>
                  <p className="font-semibold">28.4°C</p>
                </div>
                <div className="p-3 bg-muted/30 rounded-lg">
                  <p className="text-muted-foreground">Humidity</p>
                  <p className="font-semibold">72.3%</p>
                </div>
                <div className="p-3 bg-muted/30 rounded-lg">
                  <p className="text-muted-foreground">NPK Ratio</p>
                  <p className="font-semibold">120:45:80</p>
                </div>
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {results ? (
              <>
                {/* Analysis Results */}
                <div className="glass-card p-6">
                  <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-success" />
                    Analysis Results
                  </h2>
                  
                  <div className="space-y-4">
                    {/* Crop Detection */}
                    <div className="p-4 bg-muted/30 rounded-lg">
                      <h3 className="font-medium mb-2">Crop Detection</h3>
                      <div className="flex items-center justify-between">
                        <span className="text-2xl font-bold capitalize">
                          {results.crop_detection.crop}
                        </span>
                        <span className="text-sm text-muted-foreground">
                          {Math.round(results.crop_detection.confidence * 100)}% confidence
                        </span>
                      </div>
                    </div>

                    {/* Disease Analysis */}
                    <div className="p-4 bg-muted/30 rounded-lg">
                      <h3 className="font-medium mb-2">Disease Analysis</h3>
                      <div className="flex items-center justify-between">
                        <span className="capitalize">
                          {results.disease_diagnosis.disease.replace('_', ' ')}
                        </span>
                        <span className={`text-sm px-2 py-1 rounded ${
                          results.disease_diagnosis.severity === 'low' ? 'bg-green-500/10 text-green-500' :
                          results.disease_diagnosis.severity === 'medium' ? 'bg-yellow-500/10 text-yellow-500' :
                          'bg-red-500/10 text-red-500'
                        }`}>
                          {results.disease_diagnosis.severity}
                        </span>
                      </div>
                    </div>

                    {/* Quality Grade */}
                    <div className="p-4 bg-muted/30 rounded-lg">
                      <h3 className="font-medium mb-2">Quality Grade</h3>
                      <div className="flex items-center justify-between">
                        <span className={`text-2xl font-bold px-3 py-1 rounded-lg border ${getGradeColor(results.quality_grade.grade)}`}>
                          Grade {results.quality_grade.grade}
                        </span>
                        <span className="text-sm text-muted-foreground">
                          Score: {results.quality_grade.score}/100
                        </span>
                      </div>
                    </div>

                    {/* Trust Score */}
                    <div className="p-4 bg-muted/30 rounded-lg">
                      <h3 className="font-medium mb-2 flex items-center gap-2">
                        <Shield className="w-4 h-4" />
                        Trust Analysis
                      </h3>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span>Trust Score</span>
                          <span className={`font-bold ${getTrustColor(results.trust_analysis.trust_score)}`}>
                            {results.trust_analysis.trust_score}/100
                          </span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span>Market Ready</span>
                          <span className={`px-2 py-1 rounded text-sm ${
                            results.trust_analysis.market_ready 
                              ? 'bg-green-500/10 text-green-500' 
                              : 'bg-red-500/10 text-red-500'
                          }`}>
                            {results.trust_analysis.market_ready ? '✅ Ready' : '❌ Not Ready'}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Processing Info */}
                    <div className="text-xs text-muted-foreground border-t pt-4">
                      <p>Processing time: {results.processing_time_ms}ms</p>
                      <p>Analysis ID: {results.inference_id}</p>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="glass-card p-12 text-center">
                <Leaf className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
                <h3 className="text-xl font-semibold mb-2">Ready for Analysis</h3>
                <p className="text-muted-foreground">
                  Upload an image to see AI-powered crop analysis results here
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAnalysisInterface;
