#!/usr/bin/env python3
"""
Maven Project Converter Script

Converts a Java project to standard Maven structure with the following features:
1. Creates standard Maven directory structure (src/main/java, src/test/java, etc.)
2. Moves existing Java files to appropriate Maven directories
3. Replaces 'test' package names with 'example'
4. Updates package declarations in source files
5. Generates or updates pom.xml
"""

import os
import re
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Set
import xml.etree.ElementTree as ET
from xml.dom import minidom


class MavenConverter:
    def __init__(self, project_path: str, dry_run: bool = False):
        self.project_path = Path(project_path).resolve()
        self.dry_run = dry_run
        self.maven_structure = {
            'src/main/java': [],
            'src/main/resources': [],
            'src/test/java': [],
            'src/test/resources': []
        }
        self.moved_files: List[Dict[str, str]] = []

    def log(self, message: str):
        """Print log message."""
        prefix = "[DRY RUN] " if self.dry_run else ""
        print(f"{prefix}{message}")

    def find_java_files(self) -> List[Path]:
        """Find all Java files in the project."""
        java_files = []
        for root, dirs, files in os.walk(self.project_path):
            # Skip existing Maven structure and build directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'target', 'build', 'out', '.idea']]

            for file in files:
                if file.endswith('.java'):
                    java_files.append(Path(root) / file)
        return java_files

    def find_resource_files(self) -> List[Path]:
        """Find resource files (properties, xml, etc.)."""
        resource_extensions = {'.properties', '.xml', '.yml', '.yaml', '.json', '.txt'}
        resource_files = []

        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'target', 'build', 'out', '.idea', 'src']]

            for file in files:
                if any(file.endswith(ext) for ext in resource_extensions):
                    # Exclude pom.xml and build files
                    if file not in ['pom.xml', 'build.gradle', 'build.xml']:
                        resource_files.append(Path(root) / file)
        return resource_files

    def extract_package_from_file(self, file_path: Path) -> str:
        """Extract package declaration from Java file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'^\s*package\s+([\w.]+)\s*;', content, re.MULTILINE)
                if match:
                    return match.group(1)
        except Exception as e:
            self.log(f"Warning: Could not read {file_path}: {e}")
        return ""

    def is_test_file(self, file_path: Path) -> bool:
        """Determine if a Java file is a test file."""
        content = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            pass

        # Check for test indicators
        test_indicators = [
            '@Test',
            'import org.junit',
            'import org.testng',
            'extends TestCase',
            'Test' in file_path.name
        ]

        return any(indicator in content for indicator in test_indicators)

    def convert_package_name(self, package: str) -> str:
        """Convert package name from 'test' to 'example'."""
        # Replace 'test' with 'example' in package name
        # Handle cases like: test.*, *.test.*, *.test
        parts = package.split('.')
        converted_parts = ['example' if part == 'test' else part for part in parts]
        return '.'.join(converted_parts)

    def determine_maven_path(self, file_path: Path, package: str, is_test: bool) -> Path:
        """Determine the Maven standard path for a file."""
        # Convert package to path
        package_path = package.replace('.', '/')

        # Convert 'test' to 'example' in path
        package_path = package_path.replace('/test/', '/example/')
        if package_path.startswith('test/'):
            package_path = 'example/' + package_path[5:]
        if package_path.endswith('/test'):
            package_path = package_path[:-4] + 'example'
        if package_path == 'test':
            package_path = 'example'

        # Determine base path
        if is_test:
            base = self.project_path / 'src' / 'test' / 'java'
        else:
            base = self.project_path / 'src' / 'main' / 'java'

        return base / package_path / file_path.name

    def update_package_declaration(self, file_path: Path):
        """Update package declaration in Java file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find and replace package declaration
            def replace_package(match):
                old_package = match.group(1)
                new_package = self.convert_package_name(old_package)
                if old_package != new_package:
                    self.log(f"  Updating package: {old_package} -> {new_package}")
                return f"package {new_package};"

            new_content = re.sub(
                r'^\s*package\s+([\w.]+)\s*;',
                replace_package,
                content,
                flags=re.MULTILINE
            )

            if not self.dry_run and new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

        except Exception as e:
            self.log(f"Error updating {file_path}: {e}")

    def create_maven_structure(self):
        """Create Maven standard directory structure."""
        self.log("Creating Maven directory structure...")

        for dir_path in self.maven_structure.keys():
            full_path = self.project_path / dir_path
            if not self.dry_run:
                full_path.mkdir(parents=True, exist_ok=True)
            self.log(f"  Created: {dir_path}")

    def move_java_files(self):
        """Move Java files to Maven structure."""
        self.log("\nAnalyzing and moving Java files...")

        java_files = self.find_java_files()

        for java_file in java_files:
            # Skip if already in Maven structure
            if 'src/main/java' in str(java_file) or 'src/test/java' in str(java_file):
                continue

            package = self.extract_package_from_file(java_file)
            is_test = self.is_test_file(java_file)

            # Determine target path
            if package:
                target_path = self.determine_maven_path(java_file, package, is_test)
            else:
                # No package declaration - put in root of appropriate directory
                base = 'src/test/java' if is_test else 'src/main/java'
                target_path = self.project_path / base / java_file.name

            self.log(f"  {java_file.relative_to(self.project_path)} -> {target_path.relative_to(self.project_path)}")

            if not self.dry_run:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(java_file), str(target_path))

            self.moved_files.append({
                'from': str(java_file),
                'to': str(target_path),
                'type': 'test' if is_test else 'main'
            })

    def move_resource_files(self):
        """Move resource files to Maven structure."""
        self.log("\nMoving resource files...")

        resource_files = self.find_resource_files()

        for resource_file in resource_files:
            # Try to determine if it's a test resource
            is_test_resource = 'test' in str(resource_file).lower()

            base = 'src/test/resources' if is_test_resource else 'src/main/resources'
            target_path = self.project_path / base / resource_file.name

            self.log(f"  {resource_file.relative_to(self.project_path)} -> {target_path.relative_to(self.project_path)}")

            if not self.dry_run:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                if target_path.exists():
                    self.log(f"    Warning: {target_path.name} already exists, skipping")
                else:
                    shutil.copy2(str(resource_file), str(target_path))

    def update_package_declarations(self):
        """Update all package declarations to replace 'test' with 'example'."""
        self.log("\nUpdating package declarations...")

        java_files = list((self.project_path / 'src').rglob('*.java'))

        for java_file in java_files:
            self.update_package_declaration(java_file)

    def generate_pom_xml(self, group_id: str = "com.example", artifact_id: str = None, version: str = "1.0-SNAPSHOT"):
        """Generate or update pom.xml."""
        pom_path = self.project_path / 'pom.xml'

        if pom_path.exists():
            self.log("\npom.xml already exists, skipping generation")
            self.log("  You may need to manually update package references in pom.xml")
            return

        if artifact_id is None:
            artifact_id = self.project_path.name

        self.log(f"\nGenerating pom.xml...")

        pom_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>{group_id}</groupId>
    <artifactId>{artifact_id}</artifactId>
    <version>{version}</version>
    <packaging>jar</packaging>

    <name>{artifact_id}</name>
    <description>Maven project generated by maven-converter</description>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <junit.version>5.9.2</junit.version>
    </properties>

    <dependencies>
        <!-- JUnit 5 -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-api</artifactId>
            <version>${{junit.version}}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>${{junit.version}}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>${{maven.compiler.source}}</source>
                    <target>${{maven.compiler.target}}</target>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.0.0</version>
            </plugin>
        </plugins>
    </build>
</project>
'''

        if not self.dry_run:
            with open(pom_path, 'w', encoding='utf-8') as f:
                f.write(pom_content)

        self.log(f"  Generated: pom.xml")
        self.log(f"    groupId: {group_id}")
        self.log(f"    artifactId: {artifact_id}")
        self.log(f"    version: {version}")

    def cleanup_empty_dirs(self):
        """Remove empty directories after conversion."""
        self.log("\nCleaning up empty directories...")

        for root, dirs, files in os.walk(self.project_path, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                # Skip Maven structure and special directories
                if 'src' in str(dir_path) or dir_name in ['.git', '.idea']:
                    continue
                try:
                    if not any(dir_path.iterdir()):
                        if not self.dry_run:
                            dir_path.rmdir()
                        self.log(f"  Removed empty: {dir_path.relative_to(self.project_path)}")
                except:
                    pass

    def convert(self, group_id: str = "com.example", artifact_id: str = None, version: str = "1.0-SNAPSHOT"):
        """Execute full Maven conversion."""
        self.log(f"{'='*60}")
        self.log(f"Maven Project Converter")
        self.log(f"Project: {self.project_path}")
        self.log(f"{'='*60}\n")

        # Create Maven structure
        self.create_maven_structure()

        # Move files
        self.move_java_files()
        self.move_resource_files()

        # Update package declarations
        self.update_package_declarations()

        # Generate pom.xml
        self.generate_pom_xml(group_id, artifact_id, version)

        # Cleanup
        self.cleanup_empty_dirs()

        self.log(f"\n{'='*60}")
        self.log(f"Conversion {'simulation' if self.dry_run else 'completed'}!")
        self.log(f"Moved {len(self.moved_files)} Java files")
        self.log(f"{'='*60}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert Java project to Maven standard structure'
    )
    parser.add_argument(
        'project_path',
        nargs='?',
        default='.',
        help='Path to the project directory (default: current directory)'
    )
    parser.add_argument(
        '--group-id',
        default='com.example',
        help='Maven groupId (default: com.example)'
    )
    parser.add_argument(
        '--artifact-id',
        help='Maven artifactId (default: project directory name)'
    )
    parser.add_argument(
        '--version',
        default='1.0-SNAPSHOT',
        help='Project version (default: 1.0-SNAPSHOT)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate conversion without making changes'
    )

    args = parser.parse_args()

    converter = MavenConverter(args.project_path, dry_run=args.dry_run)
    converter.convert(
        group_id=args.group_id,
        artifact_id=args.artifact_id,
        version=args.version
    )


if __name__ == '__main__':
    main()
