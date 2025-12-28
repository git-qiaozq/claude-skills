---
name: maven-converter
description: Converts Java projects to standard Maven structure with automated directory reorganization, package name transformation (test→example), and pom.xml generation. Use when converting non-Maven Java projects to Maven, restructuring existing projects to Maven standards, or when user requests Maven project setup/conversion.
---

# Maven Converter

Automatically converts Java projects to Maven standard structure by reorganizing directories, updating package names, and generating build configuration.

## Quick Start

Run the conversion script on the target project:

```bash
python3 scripts/maven_converter.py [PROJECT_PATH] [OPTIONS]
```

**Common options:**
- `--dry-run`: Preview changes without modifying files
- `--group-id`: Set Maven groupId (default: com.example)
- `--artifact-id`: Set Maven artifactId (default: project directory name)
- `--version`: Set project version (default: 1.0-SNAPSHOT)

**Example:**
```bash
# Preview conversion
python3 scripts/maven_converter.py /path/to/project --dry-run

# Execute conversion with custom groupId
python3 scripts/maven_converter.py /path/to/project --group-id com.mycompany --artifact-id my-app
```

## What It Does

The converter performs these operations automatically:

1. **Creates Maven structure**
   - `src/main/java/` - Production source code
   - `src/main/resources/` - Production resources
   - `src/test/java/` - Test source code
   - `src/test/resources/` - Test resources

2. **Reorganizes files**
   - Analyzes package declarations in Java files
   - Moves files to appropriate Maven directories
   - Identifies test files (by annotations, imports, naming)
   - Copies resource files to Maven resource directories

3. **Transforms package names**
   - Replaces `test` with `example` in package declarations
   - Handles patterns: `test.*`, `*.test.*`, `*.test`
   - Updates all package statements in Java files
   - Examples:
     - `package test;` → `package example;`
     - `package com.test.app;` → `package com.example.app;`
     - `package com.app.test.utils;` → `package com.app.example.utils;`

4. **Generates pom.xml**
   - Creates standard Maven POM if not present
   - Includes JUnit 5 dependencies
   - Configures compiler plugin (Java 11)
   - Sets up build plugins (surefire, jar)
   - Uses UTF-8 encoding

5. **Cleans up**
   - Removes empty directories after file moves
   - Preserves existing Maven structure

## Workflow

### Step 1: Assess the Project

Before conversion, understand the project structure:

```bash
# View current structure
find /path/to/project -type f -name "*.java" | head -20

# Check for existing Maven setup
ls -la /path/to/project/pom.xml
ls -la /path/to/project/src/
```

### Step 2: Run Dry-Run

Always preview changes first:

```bash
python3 scripts/maven_converter.py /path/to/project --dry-run
```

Review the output to verify:
- File movements make sense
- Package transformations are correct
- No important files are missed

### Step 3: Execute Conversion

Run the actual conversion:

```bash
python3 scripts/maven_converter.py /path/to/project \
  --group-id com.company \
  --artifact-id project-name \
  --version 1.0.0
```

### Step 4: Verify Results

Check the converted structure:

```bash
# View Maven structure
tree /path/to/project/src -L 4

# Verify pom.xml
cat /path/to/project/pom.xml

# Test the build
cd /path/to/project
mvn clean compile
mvn test
```

### Step 5: Manual Adjustments

Review and adjust as needed:

1. **Check pom.xml**
   - Add project-specific dependencies
   - Set correct Java version if not 11
   - Configure main class if building executable JAR
   - Add additional plugins

2. **Verify package names**
   - Ensure all imports still resolve
   - Check for hardcoded package strings in code
   - Update documentation referencing old packages

3. **Review moved files**
   - Confirm test files in `src/test/java`
   - Confirm main code in `src/main/java`
   - Check resources in appropriate directories

## Custom POM Template

To use a custom pom.xml template instead of auto-generation:

1. Place your template at `assets/pom_template.xml`
2. Copy it to the project before conversion:
   ```bash
   cp assets/pom_template.xml /path/to/project/pom.xml
   ```
3. Run converter (will skip pom.xml generation if file exists)

The template in `assets/pom_template.xml` provides a starting point with:
- Standard Maven structure
- JUnit 5 configuration
- Common plugins (compiler, surefire, jar)
- Placeholder for dependencies and main class

## Limitations

- **Existing Maven projects**: Skips files already in `src/main/java` or `src/test/java`
- **Existing pom.xml**: Does not modify existing POM files
- **Complex packages**: Manual review needed for unusual package structures
- **Non-Java resources**: May need manual placement of specialized resources
- **Import statements**: Does not update import statements (only package declarations)

## Troubleshooting

**Files not moved correctly**
- Check package declarations match actual package structure
- Verify files have proper `.java` extension
- Check file encoding (script expects UTF-8)

**Package transformation issues**
- Review dry-run output for unexpected transformations
- Manually adjust package names if pattern doesn't match
- Update import statements referencing old package names

**Build failures after conversion**
- Run `mvn clean compile` to check compilation
- Verify all dependencies in pom.xml
- Check Java version matches compiler configuration
- Ensure resource files in correct directories

**Script errors**
- Verify Python 3 is installed: `python3 --version`
- Check file permissions on project directory
- Ensure no files are locked or in use
