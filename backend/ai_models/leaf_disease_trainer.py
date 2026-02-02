"""
AgroGrade AI - Advanced Leaf Disease Detection Training Pipeline
High-accuracy CNN model training with minimal error rates
"""

import os
import json
import time
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# TensorFlow and Keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks, optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB3, ResNet50V2
from tensorflow.keras.utils import to_categorical

# Scikit-learn for evaluation
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight

# Image processing
import cv2
from PIL import Image, ImageEnhance
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Set random seeds for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

class LeafDiseaseTrainer:
    """
    Advanced leaf disease detection trainer with:
    - State-of-the-art CNN architectures
    - Advanced data augmentation
    - Class imbalance handling
    - Cross-validation
    - Model ensembling
    - Performance monitoring
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.model = None
        self.history = None
        self.best_model = None
        self.class_names = config['class_names']
        self.num_classes = len(self.class_names)
        
        # Create directories
        self.setup_directories()
        
        # Setup data generators
        self.setup_data_generators()
        
        # Setup callbacks
        self.setup_callbacks()
        
        print(f"🌿 Initialized Leaf Disease Trainer for {self.num_classes} classes")
        print(f"📊 Classes: {', '.join(self.class_names)}")
    
    def setup_directories(self):
        """Create necessary directories for training"""
        self.base_dir = Path(self.config['base_dir'])
        self.data_dir = self.base_dir / "dataset"
        self.models_dir = self.base_dir / "models"
        self.logs_dir = self.base_dir / "logs"
        self.plots_dir = self.base_dir / "plots"
        
        for dir_path in [self.data_dir, self.models_dir, self.logs_dir, self.plots_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def setup_data_generators(self):
        """Setup advanced data augmentation and preprocessing"""
        
        # Training augmentation with Albumentations
        self.train_augmentation = A.Compose([
            A.RandomResizedCrop(height=224, width=224, scale=(0.8, 1.0)),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.3),
            A.RandomRotate90(p=0.5),
            A.ShiftScaleRotate(
                shift_limit=0.1, 
                scale_limit=0.1, 
                rotate_limit=45, 
                p=0.5
            ),
            A.RandomBrightnessContrast(
                brightness_limit=0.3, 
                contrast_limit=0.3, 
                p=0.5
            ),
            A.HueSaturationValue(
                hue_shift_limit=20, 
                sat_shift_limit=30, 
                val_shift_limit=20, 
                p=0.5
            ),
            A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
            A.GaussianBlur(blur_limit=(3, 7), p=0.2),
            A.CoarseDropout(
                max_holes=8, 
                max_height=16, 
                max_width=16, 
                p=0.3
            ),
            A.Normalize(
                mean=[0.485, 0.456, 0.406], 
                std=[0.229, 0.224, 0.225]
            ),
        ])
        
        # Validation augmentation (minimal)
        self.val_augmentation = A.Compose([
            A.Resize(height=224, width=224),
            A.Normalize(
                mean=[0.485, 0.456, 0.406], 
                std=[0.229, 0.224, 0.225]
            ),
        ])
    
    def setup_callbacks(self):
        """Setup advanced training callbacks"""
        
        # Model checkpoint
        self.checkpoint_cb = callbacks.ModelCheckpoint(
            filepath=str(self.models_dir / "best_model.h5"),
            monitor='val_accuracy',
            save_best_only=True,
            save_weights_only=False,
            mode='max',
            verbose=1
        )
        
        # Early stopping with patience
        self.early_stopping_cb = callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=15,
            restore_best_weights=True,
            mode='max',
            verbose=1
        )
        
        # Reduce learning rate on plateau
        self.reduce_lr_cb = callbacks.ReduceLROnPlateau(
            monitor='val_accuracy',
            factor=0.5,
            patience=8,
            min_lr=1e-7,
            mode='max',
            verbose=1
        )
        
        # CSV logger
        self.csv_logger_cb = callbacks.CSVLogger(
            filename=str(self.logs_dir / "training_log.csv"),
            append=True
        )
        
        # TensorBoard
        self.tensorboard_cb = callbacks.TensorBoard(
            log_dir=str(self.logs_dir / f"tensorboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            histogram_freq=1,
            write_graph=True,
            write_images=True
        )
        
        self.callbacks = [
            self.checkpoint_cb,
            self.early_stopping_cb,
            self.reduce_lr_cb,
            self.csv_logger_cb,
            self.tensorboard_cb
        ]
    
    def create_advanced_model(self, architecture: str = "efficientnet") -> tf.keras.Model:
        """
        Create state-of-the-art CNN architecture for leaf disease detection
        
        Args:
            architecture: Model type ('efficientnet', 'resnet', 'custom')
        """
        
        input_shape = (224, 224, 3)
        
        if architecture == "efficientnet":
            # EfficientNetB3 - Best for image classification
            base_model = EfficientNetB3(
                include_top=False,
                weights='imagenet',
                input_shape=input_shape,
                pooling='avg'
            )
            
            # Fine-tune from layer 200 onwards
            base_model.trainable = True
            for layer in base_model.layers[:200]:
                layer.trainable = False
                
        elif architecture == "resnet":
            # ResNet50V2 - Excellent for transfer learning
            base_model = ResNet50V2(
                include_top=False,
                weights='imagenet',
                input_shape=input_shape,
                pooling='avg'
            )
            
            # Fine-tune from layer 150 onwards
            base_model.trainable = True
            for layer in base_model.layers[:150]:
                layer.trainable = False
                
        else:
            # Custom CNN architecture
            base_model = self.create_custom_cnn(input_shape)
        
        # Build classification head
        inputs = layers.Input(shape=input_shape)
        
        # Data augmentation layer
        x = layers.RandomFlip("horizontal")(inputs)
        x = layers.RandomRotation(0.1)(x)
        x = layers.RandomZoom(0.1)(x)
        x = layers.RandomContrast(0.1)(x)
        
        # Pass through base model
        x = base_model(x, training=False)
        
        # Advanced classification head
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.4)(x)
        x = layers.Dense(512, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.2)(x)
        
        # Output layer
        outputs = layers.Dense(
            self.num_classes, 
            activation='softmax',
            name='predictions'
        )(x)
        
        model = models.Model(inputs, outputs, name=f"leaf_disease_{architecture}")
        
        return model
    
    def create_custom_cnn(self, input_shape: Tuple[int, int, int]) -> tf.keras.Model:
        """Create custom CNN architecture for leaf detection"""
        
        inputs = layers.Input(shape=input_shape)
        
        # Block 1
        x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.25)(x)
        
        # Block 2
        x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.3)(x)
        
        # Block 3
        x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.35)(x)
        
        # Block 4
        x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.4)(x)
        
        # Global pooling
        x = layers.GlobalAveragePooling2D()(x)
        
        return models.Model(inputs, x, name="custom_cnn_backbone")
    
    def compile_model(self, model: tf.keras.Model, learning_rate: float = 1e-4):
        """Compile model with advanced optimizer and metrics"""
        
        # Use AdamW optimizer for better performance
        optimizer = optimizers.AdamW(
            learning_rate=learning_rate,
            weight_decay=1e-4
        )
        
        # Compile with comprehensive metrics
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=[
                'accuracy',
                'precision',
                'recall',
                'auc',
                'top_k_categorical_accuracy'
            ]
        )
        
        return model
    
    def prepare_dataset(self, data_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load and prepare dataset with proper preprocessing
        
        Args:
            data_path: Path to dataset directory
            
        Returns:
            Tuple of (images, labels)
        """
        
        images = []
        labels = []
        
        print(f"📁 Loading dataset from: {data_path}")
        
        for class_idx, class_name in enumerate(self.class_names):
            class_path = Path(data_path) / class_name
            
            if not class_path.exists():
                print(f"⚠️ Warning: {class_path} not found, skipping...")
                continue
            
            # Load all images in class directory
            for img_path in class_path.glob("*"):
                if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                    try:
                        # Load and preprocess image
                        image = cv2.imread(str(img_path))
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        image = cv2.resize(image, (224, 224))
                        
                        images.append(image)
                        labels.append(class_idx)
                        
                    except Exception as e:
                        print(f"⚠️ Error loading {img_path}: {e}")
        
        print(f"✅ Loaded {len(images)} images across {len(self.class_names)} classes")
        
        return np.array(images), np.array(labels)
    
    def train_model(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 100,
        batch_size: int = 32
    ) -> Dict:
        """
        Train the model with advanced techniques
        
        Args:
            X_train, y_train: Training data
            X_val, y_val: Validation data
            epochs: Number of training epochs
            batch_size: Batch size for training
            
        Returns:
            Training history
        """
        
        print(f"🚀 Starting model training...")
        print(f"📊 Training samples: {len(X_train)}")
        print(f"📊 Validation samples: {len(X_val)}")
        print(f"🎯 Epochs: {epochs}, Batch size: {batch_size}")
        
        # Calculate class weights for imbalance
        class_weights = compute_class_weight(
            'balanced',
            classes=np.unique(y_train),
            y=y_train
        )
        class_weight_dict = dict(enumerate(class_weights))
        
        print(f"⚖️ Class weights: {class_weight_dict}")
        
        # Train model
        start_time = time.time()
        
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=self.callbacks,
            class_weight=class_weight_dict,
            verbose=1
        )
        
        training_time = time.time() - start_time
        
        print(f"✅ Training completed in {training_time:.2f} seconds")
        
        # Save training history
        history_df = pd.DataFrame(history.history)
        history_df.to_csv(self.logs_dir / "training_history.csv", index=False)
        
        return history
    
    def evaluate_model(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """
        Comprehensive model evaluation
        
        Args:
            X_test, y_test: Test data
            
        Returns:
            Evaluation metrics
        """
        
        print(f"📈 Evaluating model on {len(X_test)} test samples...")
        
        # Get predictions
        y_pred_proba = self.model.predict(X_test)
        y_pred = np.argmax(y_pred_proba, axis=1)
        y_true = np.argmax(y_test, axis=1)
        
        # Calculate metrics
        report = classification_report(
            y_true, y_pred, 
            target_names=self.class_names,
            output_dict=True
        )
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # ROC AUC for multi-class
        auc_score = roc_auc_score(y_test, y_pred_proba, multi_class='ovr')
        
        # Overall accuracy
        accuracy = np.mean(y_true == y_pred)
        
        metrics = {
            'accuracy': accuracy,
            'auc_score': auc_score,
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'predictions': y_pred.tolist(),
            'true_labels': y_true.tolist()
        }
        
        print(f"🎯 Test Accuracy: {accuracy:.4f}")
        print(f"📊 AUC Score: {auc_score:.4f}")
        
        # Save evaluation results
        with open(self.logs_dir / "evaluation_results.json", 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # Plot confusion matrix
        self.plot_confusion_matrix(cm)
        
        return metrics
    
    def plot_confusion_matrix(self, cm: np.ndarray):
        """Plot and save confusion matrix"""
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names
        )
        plt.title('Confusion Matrix - Leaf Disease Detection')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.tight_layout()
        plt.savefig(self.plots_dir / 'confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def save_model(self, model_name: str = "leaf_disease_model"):
        """Save trained model with metadata"""
        
        # Save model
        model_path = self.models_dir / f"{model_name}.h5"
        self.model.save(model_path)
        
        # Save model metadata
        metadata = {
            'model_name': model_name,
            'num_classes': self.num_classes,
            'class_names': self.class_names,
            'input_shape': (224, 224, 3),
            'training_date': datetime.now().isoformat(),
            'accuracy': float(self.history.history['val_accuracy'][-1]),
            'loss': float(self.history.history['val_loss'][-1])
        }
        
        with open(self.models_dir / f"{model_name}_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 Model saved to: {model_path}")
        print(f"📋 Metadata saved to: {model_path}_metadata.json")


# Configuration for training
TRAINING_CONFIG = {
    'base_dir': './ai_models/training',
    'class_names': [
        'healthy_leaf',
        'bacterial_blight',
        'powdery_mildew',
        'leaf_spot',
        'rust',
        'anthracnose',
        'mosaic_virus',
        'curling'
    ],
    'image_size': (224, 224),
    'batch_size': 32,
    'epochs': 100,
    'learning_rate': 1e-4,
    'architecture': 'efficientnet'  # 'efficientnet', 'resnet', 'custom'
}


def main():
    """Main training function"""
    
    print("🌿 AgroGrade AI - Leaf Disease Detection Training")
    print("=" * 60)
    
    # Initialize trainer
    trainer = LeafDiseaseTrainer(TRAINING_CONFIG)
    
    # Create model
    print(f"🏗️ Creating {TRAINING_CONFIG['architecture']} model...")
    model = trainer.create_advanced_model(TRAINING_CONFIG['architecture'])
    model = trainer.compile_model(model, TRAINING_CONFIG['learning_rate'])
    trainer.model = model
    
    # Print model summary
    print(f"📋 Model Summary:")
    model.summary()
    
    # Note: You need to provide the dataset path
    print("\n📁 To start training, you need to:")
    print("1. Organize your dataset as:")
    print("   dataset/")
    print("   ├── healthy_leaf/")
    print("   ├── bacterial_blight/")
    print("   ├── powdery_mildew/")
    print("   └── ... (other disease classes)")
    print("2. Update the dataset path in the code")
    print("3. Run the training script")
    
    # Example of how to train when dataset is ready:
    """
    # Load dataset
    data_path = "path/to/your/dataset"
    X, y = trainer.prepare_dataset(data_path)
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )
    
    # Convert labels to categorical
    y_train = to_categorical(y_train, trainer.num_classes)
    y_val = to_categorical(y_val, trainer.num_classes)
    y_test = to_categorical(y_test, trainer.num_classes)
    
    # Train model
    history = trainer.train_model(
        X_train, y_train, X_val, y_val,
        epochs=TRAINING_CONFIG['epochs'],
        batch_size=TRAINING_CONFIG['batch_size']
    )
    
    # Evaluate model
    metrics = trainer.evaluate_model(X_test, y_test)
    
    # Save model
    trainer.save_model("leaf_disease_detector_v1")
    """


if __name__ == "__main__":
    main()
