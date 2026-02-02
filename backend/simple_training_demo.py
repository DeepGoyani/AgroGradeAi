"""
AgroGrade AI - Simplified Training Pipeline Demo
Demonstrates the training process without heavy dependencies
"""

import os
import json
import time
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

# TensorFlow for model training
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks

class SimplifiedLeafDiseaseTrainer:
    """
    Simplified training pipeline for demonstration
    """
    
    def __init__(self):
        self.num_classes = 8
        self.class_names = [
            'healthy_leaf', 'bacterial_blight', 'powdery_mildew',
            'leaf_spot', 'rust', 'anthracnose', 'mosaic_virus', 'curling'
        ]
        self.input_shape = (224, 224, 3)
        
        print(f"🌿 Simplified Leaf Disease Trainer Initialized")
        print(f"🎯 Classes: {', '.join(self.class_names)}")
    
    def create_model(self) -> tf.keras.Model:
        """
        Create a simplified CNN model for leaf disease detection
        """
        print("🏗️ Creating CNN model...")
        
        # Input layer
        inputs = layers.Input(shape=self.input_shape)
        
        # Data augmentation
        x = layers.RandomFlip("horizontal")(inputs)
        x = layers.RandomRotation(0.1)(x)
        x = layers.RandomZoom(0.1)(x)
        
        # Convolutional blocks
        x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.25)(x)
        
        x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.3)(x)
        
        x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.35)(x)
        
        x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.4)(x)
        
        # Dense layers
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(512, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.5)(x)
        
        x = layers.Dense(256, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.4)(x)
        
        # Output layer
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        model = models.Model(inputs, outputs, name="leaf_disease_classifier")
        
        return model
    
    def compile_model(self, model: tf.keras.Model):
        """
        Compile the model with optimizer and metrics
        """
        print("⚙️ Compiling model...")
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=1e-4),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def create_synthetic_dataset(self, num_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create synthetic dataset for demonstration
        """
        print(f"📊 Creating synthetic dataset with {num_samples} samples...")
        
        # Generate synthetic images
        X = np.random.rand(num_samples, *self.input_shape).astype(np.float32)
        
        # Generate synthetic labels
        y = np.random.randint(0, self.num_classes, num_samples)
        y = keras.utils.to_categorical(y, self.num_classes)
        
        # Split into train/val/test
        split1 = int(0.7 * num_samples)
        split2 = int(0.85 * num_samples)
        
        X_train, y_train = X[:split1], y[:split1]
        X_val, y_val = X[split1:split2], y[split1:split2]
        X_test, y_test = X[split2:], y[split2:]
        
        print(f"✅ Dataset created:")
        print(f"   Training: {len(X_train)} samples")
        print(f"   Validation: {len(X_val)} samples")
        print(f"   Test: {len(X_test)} samples")
        
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)
    
    def train_model(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 20
    ) -> Dict:
        """
        Train the model
        """
        print(f"🚀 Training model for {epochs} epochs...")
        
        # Setup callbacks
        callbacks_list = [
            callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=5,
                restore_best_weights=True,
                mode='max'
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_accuracy',
                factor=0.5,
                patience=3,
                min_lr=1e-7,
                mode='max'
            )
        ]
        
        # Train model
        start_time = time.time()
        
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=callbacks_list,
            verbose=1
        )
        
        training_time = time.time() - start_time
        
        print(f"✅ Training completed in {training_time:.2f} seconds")
        
        return {
            'history': history,
            'training_time': training_time
        }
    
    def evaluate_model(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """
        Evaluate the trained model
        """
        print("📈 Evaluating model...")
        
        # Get predictions
        y_pred_proba = self.model.predict(X_test, verbose=0)
        y_pred = np.argmax(y_pred_proba, axis=1)
        y_true = np.argmax(y_test, axis=1)
        
        # Calculate metrics
        accuracy = np.mean(y_true == y_pred)
        
        # Get top predictions
        top_3_indices = np.argsort(y_pred_proba, axis=1)[:, -3:][:, ::-1]
        
        print(f"🎯 Test Accuracy: {accuracy:.4f}")
        
        return {
            'accuracy': accuracy,
            'predictions': y_pred.tolist(),
            'true_labels': y_true.tolist(),
            'top_3_predictions': top_3_indices.tolist()
        }
    
    def save_model(self, model_name: str = "leaf_disease_demo"):
        """
        Save the trained model
        """
        print("💾 Saving model...")
        
        # Create models directory
        models_dir = Path(__file__).parent / "model_weights"
        models_dir.mkdir(exist_ok=True)
        
        # Save model
        model_path = models_dir / f"{model_name}.h5"
        self.model.save(model_path)
        
        # Save metadata
        metadata = {
            'model_name': model_name,
            'num_classes': self.num_classes,
            'class_names': self.class_names,
            'input_shape': self.input_shape,
            'training_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'accuracy': float(self.evaluation_results['accuracy'])
        }
        
        metadata_path = models_dir / f"{model_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Model saved to: {model_path}")
        print(f"📋 Metadata saved to: {metadata_path}")
        
        return model_path


def main():
    """
    Main training function
    """
    print("🌿 AgroGrade AI - Simplified Training Demo")
    print("=" * 50)
    
    # Initialize trainer
    trainer = SimplifiedLeafDiseaseTrainer()
    
    # Create model
    model = trainer.create_model()
    model = trainer.compile_model(model)
    trainer.model = model
    
    print(f"📋 Model Summary:")
    model.summary()
    
    # Create synthetic dataset
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = trainer.create_synthetic_dataset(1000)
    
    # Train model
    training_results = trainer.train_model(X_train, y_train, X_val, y_test, epochs=20)
    
    # Evaluate model
    evaluation_results = trainer.evaluate_model(X_test, y_test)
    trainer.evaluation_results = evaluation_results
    
    # Save model
    model_path = trainer.save_model("leaf_disease_demo_model")
    
    print("\n🎉 Training completed successfully!")
    print(f"📊 Final Accuracy: {evaluation_results['accuracy']:.4f}")
    print(f"💾 Model saved: {model_path}")
    print(f"🚀 Ready for integration!")
    
    # Show how to use the model
    print("\n📱 How to use the trained model:")
    print("1. The model is saved in ai_models/model_weights/")
    print("2. Update the enhanced_disease_detector.py to use this model")
    print("3. Test with the frontend at http://localhost:8080/ai-analysis")
    print("4. The AI will now use your trained model for leaf detection!")


if __name__ == "__main__":
    main()
