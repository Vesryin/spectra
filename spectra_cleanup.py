#!/usr/bin/env python3
"""
SpectraAI Project Cleanup Script
Removes unnecessary files and organizes the project structure.
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple

class SpectraCleanup:
    """Clean up SpectraAI project files and directories."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.removed_items: List[str] = []
        self.potential_issues: List[str] = []
    
    def clean_python_cache(self) -> None:
        """Remove Python cache files and directories."""
        print("🐍 Cleaning Python cache files...")
        
        # Remove __pycache__ directories
        for cache_dir in self.project_root.rglob("__pycache__"):
            if cache_dir.is_dir():
                shutil.rmtree(cache_dir)
                self.removed_items.append(f"Cache directory: {cache_dir}")
                print(f"   ✓ Removed: {cache_dir}")
        
        # Remove .pyc files
        for pyc_file in self.project_root.rglob("*.pyc"):
            pyc_file.unlink()
            self.removed_items.append(f"Cache file: {pyc_file}")
            print(f"   ✓ Removed: {pyc_file}")
    
    def clean_temporary_files(self) -> None:
        """Remove temporary and backup files."""
        print("🗑️  Cleaning temporary files...")
        
        temp_extensions = [
            "*.tmp", "*.bak", "*.swp", "*~", "*.log",
            "*.old", "*.orig", "*.rej", "*.DS_Store"
        ]
        
        for extension in temp_extensions:
            for temp_file in self.project_root.rglob(extension):
                if temp_file.is_file():
                    temp_file.unlink()
                    self.removed_items.append(f"Temp file: {temp_file}")
                    print(f"   ✓ Removed: {temp_file}")
    
    def identify_duplicates(self) -> List[Path]:
        """Identify potential duplicate files."""
        print("🔍 Identifying potential duplicate files...")
        
        duplicates = []
        
        # Common duplicate naming patterns
        duplicate_patterns = [
            "*_old.*", "*_backup.*", "*_copy.*", "*_test.*",
            "*_original.*", "*_prev.*", "*_previous.*",
            "old_*", "backup_*", "copy_*", "temp_*",
            "*_v1.*", "*_v2.*", "*_deprecated.*"
        ]
        
        for pattern in duplicate_patterns:
            for dup_file in self.project_root.rglob(pattern):
                if dup_file.is_file() and dup_file.suffix == ".py":
                    duplicates.append(dup_file)
                    print(f"   ⚠️  Potential duplicate: {dup_file}")
        
        return duplicates
    
    def clean_empty_directories(self) -> None:
        """Remove empty directories."""
        print("📁 Removing empty directories...")
        
        # Walk bottom-up to handle nested empty directories
        for root, dirs, files in os.walk(self.project_root, topdown=False):
            for dirname in dirs:
                dir_path = Path(root) / dirname
                try:
                    # Skip important directories even if empty
                    if dirname in ["data", "logs", "cache", ".git"]:
                        continue
                    
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        self.removed_items.append(f"Empty directory: {dir_path}")
                        print(f"   ✓ Removed: {dir_path}")
                except (OSError, PermissionError):
                    pass
    
    def validate_project_structure(self) -> None:
        """Validate that essential project files exist."""
        print("✅ Validating project structure...")
        
        essential_files = [
            "main.py",
            "requirements.txt",
            "README.md",
            "config/settings.py",
            "core/memory.py",
            "logic/brain.py"
        ]
        
        for file_path in essential_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                self.potential_issues.append(f"Missing essential file: {file_path}")
                print(f"   ⚠️  Missing: {file_path}")
            else:
                print(f"   ✓ Found: {file_path}")
    
    def run_cleanup(self) -> Tuple[List[str], List[str]]:
        """Run the complete cleanup process."""
        print("🚀 Starting SpectraAI Project Cleanup...\n")
        
        self.clean_python_cache()
        print()
        
        self.clean_temporary_files()
        print()
        
        duplicates = self.identify_duplicates()
        print()
        
        self.clean_empty_directories()
        print()
        
        self.validate_project_structure()
        print()
        
        # Summary
        print("=" * 50)
        print(f"✅ Cleanup completed!")
        print(f"📊 Removed {len(self.removed_items)} items")
        
        if duplicates:
            print(f"⚠️  Found {len(duplicates)} potential duplicates")
            print("   Review these files manually:")
            for dup in duplicates:
                print(f"   - {dup}")
        
        if self.potential_issues:
            print(f"⚠️  Found {len(self.potential_issues)} potential issues")
            for issue in self.potential_issues:
                print(f"   - {issue}")
        
        return self.removed_items, duplicates

def main():
    """Main cleanup function."""
    project_path = "F:\\SpectraAI\\spectra"
    
    if not Path(project_path).exists():
        print(f"❌ Project path does not exist: {project_path}")
        return
    
    cleaner = SpectraCleanup(project_path)
    removed_items, duplicates = cleaner.run_cleanup()
    
    print("\n🎉 SpectraAI cleanup completed successfully!")

if __name__ == "__main__":
    main()