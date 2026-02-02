"""
AgroGrade AI - Model Training Orchestration
Complete training pipeline with automated dataset preparation
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "ai_models"))

from ai_models.dataset_collector import DatasetCollector
from ai_models.leaf_disease_trainer import LeafDiseaseTrainer, TRAINING_CONFIG

class ModelTrainingOrchestrator:
    """
    Complete ML pipeline orchestration for leaf disease detection
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.base_dir = Path(config['base_dir'])
        
        # Initialize components
        self.dataset_collector = DatasetCollector(str(self.base_dir / "dataset"))
        self.trainer = None
        
        print(f"🚀 Training Orchestrator initialized")
        print(f"📁 Base directory: {self.base_dir}")
    
    def prepare_training_data(self, force_download: bool = False):
        """
        Prepare training dataset
        """
        print("📊 Preparing training dataset...")
        
        if force_download or not self._check_dataset_exists():
            print("📥 Downloading and organizing dataset...")
            self.dataset_collector.download_plant_village_dataset()
            self.dataset_collector.organize_dataset()
            self.dataset_collector.augment_dataset(target_per_class=1000)
            self.dataset_collector.create_dataset_splits()
        else:
            print("✅ Dataset already exists, skipping download")
        
        # Generate report
        report = self.dataset_collector.generate_dataset_report()
        return report
    
    def _check_dataset_exists(self) -> bool:
        """Check if dataset already exists"""
        splits_dir = self.base_dir / "dataset" / "splits"
        info_file = splits_dir / "dataset_info.json"
        return splits_dir.exists() and info_file.exists()
    
    def train_model(self, architecture: str = "efficientnet", epochs: int = 100):
        """
        Train the leaf disease detection model
        """
        print(f"🧠 Training {architecture} model...")
        
        # Update config
        training_config = TRAINING_CONFIG.copy()
        training_config['base_dir'] = str(self.base_dir / "training")
        training_config['architecture'] = architecture
        training_config['epochs'] = epochs
        
        # Initialize trainer
        self.trainer = LeafDiseaseTrainer(training_config)
        
        # Create model
        model = self.trainer.create_advanced_model(architecture)
        model = self.trainer.compile_model(model, training_config['learning_rate'])
        self.trainer.model = model
        
        # Load dataset
        dataset_path = str(self.base_dir / "dataset" / "splits" / "train")
        X_train, y_train = self.trainer.prepare_dataset(dataset_path)
        
        # Load validation data
        val_path = str(self.base_dir / "dataset" / "splits" / "val")
        X_val, y_val = self.trainer.prepare_dataset(val_path)
        
        # Load test data
        test_path = str(self.base_dir / "dataset" / "splits" / "test")
        X_test, y_test = self.trainer.prepare_dataset(test_path)
        
        # Convert to categorical
        from tensorflow.keras.utils import to_categorical
        y_train = to_categorical(y_train, self.trainer.num_classes)
        y_val = to_categorical(y_val, self.trainer.num_classes)
        y_test = to_categorical(y_test, self.trainer.num_classes)
        
        # Train model
        history = self.trainer.train_model(
            X_train, y_train, X_val, y_val,
            epochs=epochs,
            batch_size=training_config['batch_size']
        )
        
        # Evaluate model
        metrics = self.trainer.evaluate_model(X_test, y_test)
        
        # Save model
        model_name = f"leaf_disease_{architecture}_{int(time.time())}"
        self.trainer.save_model(model_name)
        
        return {
            'history': history,
            'metrics': metrics,
            'model_name': model_name
        }
    
    def optimize_model(self, model_path: str):
        """
        Optimize trained model for production
        """
        print("⚡ Optimizing model for production...")
        
        import tensorflow as tf
        
        # Load model
        model = tf.keras.models.load_model(model_path)
        
        # Convert to TensorFlow Lite
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        
        # Enable quantization
        converter.target_spec.supported_types = [tf.float16]
        
        tflite_model = converter.convert()
        
        # Save TFLite model
        tflite_path = model_path.replace('.h5', '_optimized.tflite')
        with open(tflite_path, 'wb') as f:
            f.write(tflite_model)
        
        print(f"✅ Model optimized and saved to: {tflite_path}")
        
        return tflite_path
    
    def deploy_model(self, model_path: str):
        """
        Deploy model to production AI pipeline
        """
        print("🚀 Deploying model to production...")
        
        # Copy model to AI models directory
        import shutil
        production_dir = Path(__file__).parent / "model_weights"
        production_dir.mkdir(exist_ok=True)
        
        # Copy main model
        model_name = "leaf_disease_classifier.h5"
        shutil.copy2(model_path, production_dir / model_name)
        
        # Copy metadata
        metadata_path = model_path.replace('.h5', '_metadata.json')
        if Path(metadata_path).exists():
            shutil.copy2(metadata_path, production_dir / "model_metadata.json")
        
        print(f"✅ Model deployed to: {production_dir}")
        print("🎯 Ready for production use!")
        
        return production_dir / model_name


def main():
    """Main training orchestration"""
    
    parser = argparse.ArgumentParser(description="Train AgroGrade AI Leaf Disease Detection Model")
    parser.add_argument("--mode", choices=["prepare", "train", "optimize", "deploy", "full"], 
                       default="full", help="Training mode")
    parser.add_argument("--architecture", choices=["efficientnet", "resnet", "custom"], 
                       default="efficientnet", help="Model architecture")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--force-download", action="store_true", 
                       help="Force dataset download even if exists")
    
    args = parser.parse_args()
    
    print("🌿 AgroGrade AI - Model Training Pipeline")
    print("=" * 60)
    
    # Configuration
    config = {
        'base_dir': './ai_models',
        'mode': args.mode,
        'architecture': args.architecture,
        'epochs': args.epochs,
        'force_download': args.force_download
    }
    
    # Initialize orchestrator
    orchestrator = ModelTrainingOrchestrator(config)
    
    try:
        if args.mode in ["prepare", "full"]:
            print("\n📊 Step 1: Preparing training data...")
            dataset_report = orchestrator.prepare_training_data(args.force_download)
            print(f"✅ Dataset ready: {dataset_report['dataset_summary']['total_images']} images")
        
        if args.mode in ["train", "full"]:
            print(f"\n🧠 Step 2: Training {args.architecture} model...")
            training_results = orchestrator.train_model(args.architecture, args.epochs)
            
            accuracy = training_results['metrics']['accuracy']
            print(f"✅ Training completed!")
            print(f"🎯 Test Accuracy: {accuracy:.4f}")
            print(f"💾 Model saved: {training_results['model_name']}")
            
            model_path = f"./ai_models/training/models/{training_results['model_name']}.h5"
        
        if args.mode in ["optimize", "full"] and 'model_path' in locals():
            print(f"\n⚡ Step 3: Optimizing model...")
            optimized_path = orchestrator.optimize_model(model_path)
            print(f"✅ Model optimized: {optimized_path}")
        
        if args.mode in ["deploy", "full"] and 'model_path' in locals():
            print(f"\n🚀 Step 4: Deploying model...")
            deployed_path = orchestrator.deploy_model(model_path)
            print(f"✅ Model deployed: {deployed_path}")
        
        print("\n🎉 Training pipeline completed successfully!")
        
        if args.mode == "full":
            print("\n🚀 Your trained model is now ready for production!")
            print("📱 Test it at: http://localhost:8080/ai-analysis")
            print("🔧 Backend API: http://localhost:8000/api/ai/analyze")
    
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
