"""
AgroGrade AI - Dataset Collection and Preparation
Automated dataset collection for leaf disease detection
"""

import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import requests
from urllib.parse import urlparse
import cv2
from PIL import Image, ImageEnhance
import albumentations as A
from tqdm import tqdm
import zipfile
import gdown

class DatasetCollector:
    """
    Automated dataset collection and preparation for leaf disease detection
    """
    
    def __init__(self, base_dir: str = "./ai_models/dataset"):
        self.base_dir = Path(base_dir)
        self.raw_dir = self.base_dir / "raw"
        self.processed_dir = self.base_dir / "processed"
        self.augmented_dir = self.base_dir / "augmented"
        
        # Create directories
        for dir_path in [self.base_dir, self.raw_dir, self.processed_dir, self.augmented_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Leaf disease classes for Indian agriculture
        self.disease_classes = {
            'healthy_leaf': {
                'description': 'Healthy plant leaves without any disease symptoms',
                'keywords': ['healthy leaf', 'normal leaf', 'green leaf'],
                'target_count': 1000
            },
            'bacterial_blight': {
                'description': 'Bacterial leaf blight with water-soaked lesions',
                'keywords': ['bacterial blight', 'leaf blight', 'bacterial spot'],
                'target_count': 800
            },
            'powdery_mildew': {
                'description': 'White powdery fungal growth on leaf surface',
                'keywords': ['powdery mildew', 'white mildew', 'fungal powder'],
                'target_count': 800
            },
            'leaf_spot': {
                'description': 'Circular or irregular spots on leaves',
                'keywords': ['leaf spot', 'brown spot', 'black spot'],
                'target_count': 800
            },
            'rust': {
                'description': 'Rust-colored pustules on leaf surface',
                'keywords': ['leaf rust', 'rust disease', 'orange rust'],
                'target_count': 600
            },
            'anthracnose': {
                'description': 'Dark sunken lesions on leaves',
                'keywords': ['anthracnose', 'leaf anthracnose', 'dark spots'],
                'target_count': 600
            },
            'mosaic_virus': {
                'description': 'Mosaic pattern on leaves due to viral infection',
                'keywords': ['mosaic virus', 'viral mosaic', 'leaf mosaic'],
                'target_count': 500
            },
            'curling': {
                'description': 'Leaf curling due to viral or environmental stress',
                'keywords': ['leaf curl', 'curling virus', 'leaf roll'],
                'target_count': 500
            }
        }
        
        print(f"🌿 Dataset Collector initialized")
        print(f"📁 Base directory: {self.base_dir}")
        print(f"🎯 Target classes: {len(self.disease_classes)}")
    
    def download_plant_village_dataset(self):
        """
        Download PlantVillage dataset - one of the largest plant disease datasets
        """
        print("📥 Downloading PlantVillage dataset...")
        
        # PlantVillage dataset URLs
        datasets = {
            'color': 'https://data.mendeley.com/public-files/datasets/tywbtsjrjv/files/d5652a28-c1d8-418b-9ccd-5238b737bdee/file_downloaded',
            'grayscale': 'https://data.mendeley.com/public-files/datasets/tywbtsjrjv/files/82d7e637-1c8d-4a6e-9c8a-5cf6a4e8c8e2/file_downloaded'
        }
        
        try:
            # Download color dataset
            color_url = "https://drive.google.com/uc?id=1H8H5x2p_t2s4J9Q9l2J4x5Q6R7S8T9U0"
            output_path = self.raw_dir / "plantvillage.zip"
            
            print("📥 Downloading PlantVillage dataset (this may take a while)...")
            gdown.download(color_url, str(output_path), quiet=False)
            
            # Extract dataset
            print("📂 Extracting dataset...")
            with zipfile.ZipFile(output_path, 'r') as zip_ref:
                zip_ref.extractall(self.raw_dir)
            
            print("✅ PlantVillage dataset downloaded and extracted")
            
        except Exception as e:
            print(f"⚠️ Error downloading PlantVillage: {e}")
            print("💡 You can manually download from: https://github.com/spMohanty/PlantVillage-Dataset")
    
    def download_kaggle_datasets(self):
        """
        Download additional datasets from Kaggle
        """
        print("📥 Setting up Kaggle datasets...")
        
        # Kaggle datasets for plant diseases
        kaggle_datasets = [
            {
                'name': 'plant-disease-recognition-dataset',
                'url': 'https://www.kaggle.com/datasets/rashikrahmanpritom/plant-disease-recognition-dataset'
            },
            {
                'name': 'plant-pathology-2021-fgvc8',
                'url': 'https://www.kaggle.com/c/plant-pathology-2021-fgvc8/data'
            },
            {
                'name': 'crop-diseases-classification',
                'url': 'https://www.kaggle.com/datasets/gpiosenka/crop-diseases-classification'
            }
        ]
        
        print("📋 Available Kaggle datasets:")
        for dataset in kaggle_datasets:
            print(f"   - {dataset['name']}: {dataset['url']}")
        
        print("\n💡 To download Kaggle datasets:")
        print("1. Install kaggle API: pip install kaggle")
        print("2. Setup Kaggle credentials: kaggle.json")
        print("3. Download: kaggle datasets download -d dataset-name")
    
    def organize_dataset(self):
        """
        Organize downloaded datasets into our class structure
        """
        print("🗂️ Organizing dataset into classes...")
        
        # Create class directories
        for class_name in self.disease_classes.keys():
            class_dir = self.processed_dir / class_name
            class_dir.mkdir(exist_ok=True)
        
        # Process PlantVillage dataset
        plantvillage_dir = self.raw_dir / "PlantVillage"
        if plantvillage_dir.exists():
            self.process_plantvillage_dataset()
        
        print("✅ Dataset organization completed")
    
    def process_plantvillage_dataset(self):
        """
        Process PlantVillage dataset and organize by our classes
        """
        print("🔄 Processing PlantVillage dataset...")
        
        # Mapping from PlantVillage classes to our classes
        class_mapping = {
            # Healthy
            'Apple___healthy': 'healthy_leaf',
            'Blueberry___healthy': 'healthy_leaf',
            'Cherry___healthy': 'healthy_leaf',
            'Corn___healthy': 'healthy_leaf',
            'Grape___healthy': 'healthy_leaf',
            'Orange___healthy': 'healthy_leaf',
            'Peach___healthy': 'healthy_leaf',
            'Pepper___healthy': 'healthy_leaf',
            'Potato___healthy': 'healthy_leaf',
            'Raspberry___healthy': 'healthy_leaf',
            'Soybean___healthy': 'healthy_leaf',
            'Squash___healthy': 'healthy_leaf',
            'Strawberry___healthy': 'healthy_leaf',
            'Tomato___healthy': 'healthy_leaf',
            
            # Bacterial diseases
            'Apple___Apple_scab': 'bacterial_blight',
            'Tomato___Bacterial_spot': 'bacterial_blight',
            'Pepper___Bacterial_spot': 'bacterial_blight',
            
            # Powdery mildew
            'Apple___Apple_scab': 'powdery_mildew',
            'Grape___Powdery_mildew': 'powdery_mildew',
            'Squash___Powdery_mildew': 'powdery_mildew',
            
            # Leaf spots
            'Corn___Cercospora_leaf_spot': 'leaf_spot',
            'Tomato___Early_blight': 'leaf_spot',
            'Tomato___Late_blight': 'leaf_spot',
            'Tomato___Leaf_Mold': 'leaf_spot',
            'Tomato___Septoria_leaf_spot': 'leaf_spot',
            'Tomato___Spider_mites': 'leaf_spot',
            
            # Rust
            'Corn___Common_rust': 'rust',
            
            # Other diseases
            'Apple___Cedar_apple_rust': 'rust',
            'Apple___Fire_blight': 'bacterial_blight',
        }
        
        processed_count = 0
        
        for pv_class, our_class in class_mapping.items():
            pv_class_dir = plantvillage_dir / pv_class
            if pv_class_dir.exists():
                our_class_dir = self.processed_dir / our_class
                
                # Copy and process images
                for img_path in pv_class_dir.glob("*.JPG"):
                    try:
                        # Read image
                        img = cv2.imread(str(img_path))
                        if img is not None:
                            # Resize to standard size
                            img = cv2.resize(img, (224, 224))
                            
                            # Save to our class directory
                            output_path = our_class_dir / f"{processed_count:06d}.jpg"
                            cv2.imwrite(str(output_path), img)
                            processed_count += 1
                            
                    except Exception as e:
                        print(f"⚠️ Error processing {img_path}: {e}")
        
        print(f"✅ Processed {processed_count} images from PlantVillage")
    
    def augment_dataset(self, target_per_class: int = 1000):
        """
        Augment dataset to balance classes and increase size
        """
        print("🔄 Augmenting dataset...")
        
        # Advanced augmentation pipeline
        augmentor = A.Compose([
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
        ])
        
        total_augmented = 0
        
        for class_name in self.disease_classes.keys():
            class_dir = self.processed_dir / class_name
            aug_class_dir = self.augmented_dir / class_name
            aug_class_dir.mkdir(exist_ok=True)
            
            # Get existing images
            existing_images = list(class_dir.glob("*.jpg"))
            existing_count = len(existing_images)
            
            if existing_count == 0:
                print(f"⚠️ No images found for {class_name}")
                continue
            
            # Calculate how many augmented images we need
            needed = max(0, target_per_class - existing_count)
            
            print(f"📊 {class_name}: {existing_count} existing, need {needed} augmented")
            
            # Generate augmented images
            for i in tqdm(range(needed), desc=f"Augmenting {class_name}"):
                # Select random source image
                source_img = np.random.choice(existing_images)
                
                try:
                    # Read image
                    img = cv2.imread(str(source_img))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    
                    # Apply augmentation
                    augmented = augmentor(image=img)['image']
                    
                    # Save augmented image
                    output_path = aug_class_dir / f"aug_{i:06d}.jpg"
                    augmented_bgr = cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(str(output_path), augmented_bgr)
                    
                    total_augmented += 1
                    
                except Exception as e:
                    print(f"⚠️ Error augmenting {source_img}: {e}")
        
        print(f"✅ Generated {total_augmented} augmented images")
    
    def create_dataset_splits(self, test_size: float = 0.2, val_size: float = 0.2):
        """
        Create train/val/test splits and save metadata
        """
        print("📊 Creating dataset splits...")
        
        splits_dir = self.base_dir / "splits"
        splits_dir.mkdir(exist_ok=True)
        
        dataset_info = {
            'classes': list(self.disease_classes.keys()),
            'splits': {},
            'total_images': 0,
            'created_date': str(Path.cwd())
        }
        
        total_images = 0
        
        for split in ['train', 'val', 'test']:
            split_dir = splits_dir / split
            split_dir.mkdir(exist_ok=True)
            
            split_info = {}
            
            for class_name in self.disease_classes.keys():
                class_split_dir = split_dir / class_name
                class_split_dir.mkdir(exist_ok=True)
                
                # Get images from both processed and augmented
                processed_images = list((self.processed_dir / class_name).glob("*.jpg"))
                augmented_images = list((self.augmented_dir / class_name).glob("*.jpg"))
                all_images = processed_images + augmented_images
                
                if not all_images:
                    print(f"⚠️ No images found for {class_name}")
                    continue
                
                # Shuffle and split
                np.random.shuffle(all_images)
                
                n_total = len(all_images)
                n_test = int(n_total * test_size)
                n_val = int(n_total * val_size)
                n_train = n_total - n_test - n_val
                
                if split == 'train':
                    split_images = all_images[:n_train]
                elif split == 'val':
                    split_images = all_images[n_train:n_train + n_val]
                else:  # test
                    split_images = all_images[n_train + n_val:]
                
                # Copy images to split directory
                for img_path in split_images:
                    dest_path = class_split_dir / img_path.name
                    if not dest_path.exists():
                        img = cv2.imread(str(img_path))
                        cv2.imwrite(str(dest_path), img)
                
                split_info[class_name] = len(split_images)
                total_images += len(split_images)
            
            dataset_info['splits'][split] = split_info
        
        dataset_info['total_images'] = total_images
        
        # Save dataset metadata
        with open(splits_dir / "dataset_info.json", 'w') as f:
            json.dump(dataset_info, f, indent=2)
        
        print(f"✅ Dataset splits created with {total_images} total images")
        print(f"📊 Split distribution:")
        for split, split_info in dataset_info['splits'].items():
            total = sum(split_info.values())
            print(f"   {split}: {total} images")
    
    def generate_dataset_report(self):
        """
        Generate comprehensive dataset report
        """
        print("📈 Generating dataset report...")
        
        report = {
            'dataset_summary': {},
            'class_distribution': {},
            'image_statistics': {},
            'recommendations': []
        }
        
        total_images = 0
        class_stats = {}
        
        for class_name in self.disease_classes.keys():
            processed_count = len(list((self.processed_dir / class_name).glob("*.jpg")))
            augmented_count = len(list((self.augmented_dir / class_name).glob("*.jpg")))
            total_class = processed_count + augmented_count
            
            class_stats[class_name] = {
                'processed': processed_count,
                'augmented': augmented_count,
                'total': total_class
            }
            
            total_images += total_class
        
        report['class_distribution'] = class_stats
        report['dataset_summary'] = {
            'total_classes': len(self.disease_classes),
            'total_images': total_images,
            'avg_images_per_class': total_images // len(self.disease_classes)
        }
        
        # Recommendations
        min_images = min(stats['total'] for stats in class_stats.values())
        max_images = max(stats['total'] for stats in class_stats.values())
        
        if min_images < 500:
            report['recommendations'].append("Consider collecting more images for underrepresented classes")
        
        if max_images / min_images > 3:
            report['recommendations'].append("Dataset is imbalanced - consider more augmentation")
        
        # Save report
        with open(self.base_dir / "dataset_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Dataset report generated")
        print(f"📊 Total images: {total_images}")
        print(f"🎯 Classes: {len(self.disease_classes)}")
        
        return report


def main():
    """Main dataset collection function"""
    
    print("🌿 AgroGrade AI - Dataset Collection")
    print("=" * 50)
    
    # Initialize collector
    collector = DatasetCollector()
    
    # Step 1: Download datasets
    print("\n📥 Step 1: Downloading datasets...")
    collector.download_plant_village_dataset()
    collector.download_kaggle_datasets()
    
    # Step 2: Organize dataset
    print("\n🗂️ Step 2: Organizing dataset...")
    collector.organize_dataset()
    
    # Step 3: Augment dataset
    print("\n🔄 Step 3: Augmenting dataset...")
    collector.augment_dataset(target_per_class=1000)
    
    # Step 4: Create splits
    print("\n📊 Step 4: Creating dataset splits...")
    collector.create_dataset_splits()
    
    # Step 5: Generate report
    print("\n📈 Step 5: Generating report...")
    report = collector.generate_dataset_report()
    
    print("\n✅ Dataset collection completed!")
    print(f"📁 Dataset location: {collector.base_dir}")
    print(f"🎯 Ready for training with {report['dataset_summary']['total_images']} images")
    
    print("\n🚀 Next steps:")
    print("1. Review the dataset in ./ai_models/dataset/splits")
    print("2. Run the training script: python leaf_disease_trainer.py")
    print("3. Monitor training with TensorBoard: tensorboard --logdir ./ai_models/training/logs")


if __name__ == "__main__":
    main()
